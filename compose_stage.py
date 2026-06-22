# -*- coding: utf-8 -*-
"""
舞台主图屏幕替换合成脚本
做法：自动检测主图中各 LED 屏的青色边框 → 提取四角点 → 透视变换贴入替换图
输出：output_result.jpg（高清，2560x1440）

对应关系（按用户说明）：
  center      <- center.jpg       中间大屏：征途回响 青春当歌
  left_outer  <- left_outer.jpg   左最外竖屏：矢志不渝听党话 跟党走 / 厚植爱国情怀
  left_inner  <- left_inner.jpg   左内侧竖屏：红金音符
  right_inner <- right_outer.jpg  右内侧竖屏：红金音符
  right_outer <- right_inner.jpg  右最外竖屏：强化思想引领 / 铸牢理想信念
"""
import numpy as np
import cv2
from PIL import Image

MAIN = "images/main.jpg"

# 中间三块屏（左内侧+中间+右内侧）作为一整块连续画面，统一铺 center.jpg，
# 使飘带横跨三块屏连续对齐。
CENTRAL = ["left_inner", "center", "right_inner"]
CENTRAL_IMG = "images/center.jpg"

# 左右最外侧的文字竖屏单独贴
OUTER = {
    "left_outer":  "images/left_outer.jpg",   # 矢志不渝听党话 跟党走 / 厚植爱国情怀
    "right_outer": "images/right_inner.jpg",   # 强化思想引领 / 铸牢理想信念
}
NAMES = ["left_outer", "left_inner", "center", "right_inner", "right_outer"]


def order(p):
    p = np.array(p, float)
    s = p[:, 0] + p[:, 1]
    d = p[:, 0] - p[:, 1]
    return [p[np.argmin(s)], p[np.argmax(d)], p[np.argmax(s)], p[np.argmin(d)]]


def detect_quads(main_bgr):
    rgb = cv2.cvtColor(main_bgr, cv2.COLOR_BGR2RGB).astype(int)
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mask = (((B > 140) & (G > 110) & (R < 140) & (B - R > 40))).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    m = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=1)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w < 60 or h < 150 or w * h < 8000:
            continue
        big.append((x, c))
    big.sort(key=lambda z: z[0])
    quads = {}
    for (x, c), nm in zip(big, NAMES):
        peri = cv2.arcLength(c, True)
        quad = None
        for f in (0.02, 0.03, 0.04, 0.05):
            ap = cv2.approxPolyDP(c, f * peri, True).reshape(-1, 2)
            if len(ap) == 4:
                quad = order(ap)
                break
        if quad is None:
            quad = order(cv2.boxPoints(cv2.minAreaRect(c)))
        quads[nm] = np.array([[int(round(p[0])), int(round(p[1]))] for p in quad],
                             dtype=np.float32)
    return quads


# 向外扩张的像素数：用于完全盖住屏幕原有的青色 LED 边框
EXPAND = 8


def expand_quad(q, e=EXPAND):
    """把四边形按 [TL,TR,BR,BL] 顺序，沿各角的外侧方向扩张 e 像素。"""
    q = np.array(q, dtype=np.float32)
    signs = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=np.float32)
    return q + signs * e


def paste(out, src_im, dst_quad, mask_polys):
    """把 src_im 透视映射到 dst_quad，并按 mask_polys（多个多边形）合成到 out。"""
    H, W = out.shape[:2]
    h, w = src_im.shape[:2]
    src = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(src, dst_quad.astype(np.float32))
    warp = cv2.warpPerspective(src_im, M, (W, H), flags=cv2.INTER_LANCZOS4,
                               borderMode=cv2.BORDER_REPLICATE)
    mask = np.zeros((H, W), np.uint8)
    for poly in mask_polys:
        cv2.fillConvexPoly(mask, np.round(poly).astype(np.int32), 255, cv2.LINE_AA)
    a = (mask.astype(np.float32) / 255.0)[..., None]
    return (warp.astype(np.float32) * a + out.astype(np.float32) * (1 - a)).astype(np.uint8)


def main():
    main_bgr = cv2.cvtColor(np.array(Image.open(MAIN).convert("RGB")),
                            cv2.COLOR_RGB2BGR)
    H, W = main_bgr.shape[:2]
    quads = detect_quads(main_bgr)
    out = main_bgr.copy()

    # —— 中间三块屏：统一铺一张连续的 center.jpg ——
    # 用三块屏的整体外接四边形作为映射目标，保证飘带横跨连续；
    # 再用各屏自身（外扩后）的多边形作为蒙版，缝隙保持原样（深色接缝，符合多屏物理结构）。
    pts = np.vstack([quads[n] for n in CENTRAL])
    x0, y0 = pts[:, 0].min(), pts[:, 1].min()
    x1, y1 = pts[:, 0].max(), pts[:, 1].max()
    union = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], dtype=np.float32)
    union = expand_quad(union)
    central_src = cv2.cvtColor(np.array(Image.open(CENTRAL_IMG).convert("RGB")),
                               cv2.COLOR_RGB2BGR)
    masks = [expand_quad(quads[n]) for n in CENTRAL]
    out = paste(out, central_src, union, masks)

    # —— 左右最外侧文字竖屏 ——
    for nm, path in OUTER.items():
        src_im = cv2.cvtColor(np.array(Image.open(path).convert("RGB")),
                              cv2.COLOR_RGB2BGR)
        out = paste(out, src_im, expand_quad(quads[nm]), [expand_quad(quads[nm])])

    cv2.imwrite("output_result.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 98])
    print("已生成 output_result.jpg", out.shape)


if __name__ == "__main__":
    main()
