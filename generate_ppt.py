# -*- coding: utf-8 -*-
"""
《一元一次方程》教学课件生成脚本
北师大版 七年级上册 第五章
循序渐进：每个知识点讲解后配经典例题 + 练习
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

# ---------------- 全局配色 ----------------
C_PRIMARY = RGBColor(0x1F, 0x4E, 0x79)   # 深蓝（标题）
C_ACCENT  = RGBColor(0xC0, 0x50, 0x4D)   # 砖红（强调）
C_GREEN   = RGBColor(0x37, 0x7D, 0x22)   # 绿色（练习/答案）
C_ORANGE  = RGBColor(0xE3, 0x6C, 0x09)   # 橙色（例题）
C_BG      = RGBColor(0xF2, 0xF6, 0xFB)   # 浅蓝背景
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_DARK    = RGBColor(0x33, 0x33, 0x33)
C_LIGHT   = RGBColor(0xE8, 0xEF, 0xF7)

FONT = "Microsoft YaHei"   # PowerPoint 中文环境默认有；Linux 渲染用文泉驿

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW = prs.slide_width
SH = prs.slide_height

BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def set_bg(slide, color=C_BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, x, y, w, h, color, line_color=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def add_round_rect(slide, x, y, w, h, color, line_color=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(1.5)
    shp.shadow.inherit = False
    return shp


def add_text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15, wrap=True):
    """
    runs: list of paragraphs, each paragraph is list of (text, size, color, bold)
    """
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_after = Pt(4)
        for (text, size, color, bold) in para:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.name = FONT
    return tb


def P(*runs):
    """快速构造一个段落（多个 run）"""
    return list(runs)


def R(text, size=18, color=C_DARK, bold=False):
    return (text, size, color, bold)


# ============ 通用：内容页页头 ============
def content_header(slide, section, title):
    set_bg(slide)
    # 顶部色条
    add_rect(slide, 0, 0, SW, Inches(1.05), C_PRIMARY)
    # 左侧装饰小块
    add_rect(slide, Inches(0.0), 0, Inches(0.18), Inches(1.05), C_ACCENT)
    add_text(slide, Inches(0.45), Inches(0.10), Inches(11.5), Inches(0.45),
             [P(R(section, 14, C_LIGHT, False))], anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(0.45), Inches(0.40), Inches(12.0), Inches(0.6),
             [P(R(title, 28, C_WHITE, True))], anchor=MSO_ANCHOR.MIDDLE)


def label_chip(slide, x, y, text, color, w=Inches(1.5)):
    chip = add_round_rect(slide, x, y, w, Inches(0.42), color)
    add_text(slide, x, y, w, Inches(0.42),
             [P(R(text, 15, C_WHITE, True))],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return chip


# ============================================================
# 1. 封面
# ============================================================
s = add_slide()
set_bg(s, C_PRIMARY)
add_rect(s, 0, Inches(2.55), SW, Inches(2.4), C_WHITE)
add_rect(s, Inches(0), Inches(2.55), Inches(0.25), Inches(2.4), C_ACCENT)
add_text(s, Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6),
         [P(R("北师大版 · 七年级上册 · 第五章", 20, C_LIGHT, False))])
add_text(s, Inches(0.8), Inches(2.75), Inches(11.7), Inches(1.3),
         [P(R("一元一次方程", 54, C_PRIMARY, True))], anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(3.95), Inches(11.7), Inches(0.7),
         [P(R("知识点精讲 + 经典考点例题 + 随堂练习", 22, C_ACCENT, True))],
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.4),
         [P(R("教学课件 · 循序渐进 · 讲练结合", 18, C_LIGHT, False)),
          P(R("适用：成都市武侯区 初一数学", 16, C_LIGHT, False))])

# ============================================================
# 2. 本章目录
# ============================================================
s = add_slide()
content_header(s, "第五章 一元一次方程", "本章学习目录")
items = [
    ("5.1  认识方程", "方程、一元一次方程、方程的解", C_PRIMARY),
    ("5.2  一元一次方程的解法", "等式性质、移项、去括号、去分母", C_ORANGE),
    ("5.3  一元一次方程的应用", "和差倍分、行程、工程、销售等", C_GREEN),
    ("本章小结与易错点", "考试重点 + 常见失分点", C_ACCENT),
]
y = Inches(1.45)
for title, desc, col in items:
    add_round_rect(s, Inches(0.8), y, Inches(11.7), Inches(1.15), C_WHITE, line_color=col)
    add_rect(s, Inches(0.8), y, Inches(0.16), Inches(1.15), col)
    add_text(s, Inches(1.15), y + Inches(0.12), Inches(11.0), Inches(0.5),
             [P(R(title, 22, col, True))])
    add_text(s, Inches(1.15), y + Inches(0.62), Inches(11.0), Inches(0.45),
             [P(R(desc, 16, C_DARK, False))])
    y += Inches(1.35)

# ============================================================
# 辅助：知识点页
# ============================================================
def knowledge_slide(section, title, points, tip=None):
    s = add_slide()
    content_header(s, section, title)
    label_chip(s, Inches(0.8), Inches(1.3), "知识讲解", C_PRIMARY, w=Inches(1.6))
    y = Inches(1.95)
    box_h = Inches(4.0) if tip else Inches(4.7)
    add_round_rect(s, Inches(0.8), y, Inches(11.7), box_h, C_WHITE, line_color=C_LIGHT)
    paras = []
    for pt in points:
        if isinstance(pt, tuple):
            head, body = pt
            paras.append(P(R("◆ ", 19, C_ACCENT, True), R(head, 19, C_PRIMARY, True)))
            if body:
                paras.append(P(R("     " + body, 17, C_DARK, False)))
        else:
            paras.append(P(R("• ", 18, C_ACCENT, True), R(pt, 18, C_DARK, False)))
    add_text(s, Inches(1.1), y + Inches(0.25), Inches(11.1), box_h - Inches(0.5),
             paras, line_spacing=1.25)
    if tip:
        ty = y + box_h + Inches(0.15)
        add_round_rect(s, Inches(0.8), ty, Inches(11.7), Inches(0.62), C_LIGHT)
        add_text(s, Inches(1.05), ty, Inches(11.3), Inches(0.62),
                 [P(R("💡 提示：", 16, C_ACCENT, True), R(tip, 16, C_DARK, False))],
                 anchor=MSO_ANCHOR.MIDDLE)
    return s


# ============================================================
# 辅助：例题页
# ============================================================
def example_slide(section, title, problem, steps, answer, chip="经典例题",
                  chip_color=C_ORANGE):
    s = add_slide()
    content_header(s, section, title)
    label_chip(s, Inches(0.8), Inches(1.3), chip, chip_color, w=Inches(1.6))
    # 题目框
    add_round_rect(s, Inches(0.8), Inches(1.95), Inches(11.7), Inches(1.2),
                   C_LIGHT, line_color=chip_color)
    add_text(s, Inches(1.1), Inches(1.95), Inches(11.1), Inches(1.2),
             [P(R("【题目】", 18, chip_color, True), R(problem, 18, C_DARK, False))],
             anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)
    # 解答框
    y = Inches(3.35)
    add_round_rect(s, Inches(0.8), y, Inches(11.7), Inches(3.4), C_WHITE,
                   line_color=C_LIGHT)
    add_text(s, Inches(1.1), y + Inches(0.12), Inches(11.1), Inches(0.45),
             [P(R("解：", 18, C_PRIMARY, True))])
    paras = []
    for st in steps:
        paras.append(P(R(st, 17, C_DARK, False)))
    add_text(s, Inches(1.3), y + Inches(0.6), Inches(10.9), Inches(2.2),
             paras, line_spacing=1.3)
    # 答案条
    ay = y + Inches(2.85)
    add_round_rect(s, Inches(1.1), ay, Inches(11.1), Inches(0.45), C_GREEN)
    add_text(s, Inches(1.1), ay, Inches(11.1), Inches(0.45),
             [P(R("✔ " + answer, 16, C_WHITE, True))],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return s


# ============================================================
# 辅助：随堂练习页
# ============================================================
def practice_slide(section, title, problems, answers):
    s = add_slide()
    content_header(s, section, title)
    label_chip(s, Inches(0.8), Inches(1.3), "随堂练习", C_GREEN, w=Inches(1.6))
    y = Inches(1.95)
    add_round_rect(s, Inches(0.8), y, Inches(11.7), Inches(2.6), C_WHITE,
                   line_color=C_GREEN)
    paras = []
    for i, p in enumerate(problems, 1):
        paras.append(P(R(f"{i}. ", 18, C_GREEN, True), R(p, 18, C_DARK, False)))
    add_text(s, Inches(1.1), y + Inches(0.2), Inches(11.1), Inches(2.2),
             paras, line_spacing=1.4)
    # 参考答案
    ay = y + Inches(2.8)
    add_round_rect(s, Inches(0.8), ay, Inches(11.7), Inches(1.5), C_LIGHT)
    apar = [P(R("参考答案：", 16, C_ACCENT, True))]
    for i, a in enumerate(answers, 1):
        apar.append(P(R(f"  {i}）", 15, C_GREEN, True), R(a, 15, C_DARK, False)))
    add_text(s, Inches(1.1), ay + Inches(0.1), Inches(11.3), Inches(1.3),
             apar, line_spacing=1.2)
    return s


# ============================================================
# ====================  5.1 认识方程  ========================
# ============================================================
SEC1 = "5.1 认识方程"

knowledge_slide(
    SEC1, "一、什么是方程",
    [
        ("方程的定义", "含有未知数的等式，叫做方程。"),
        ("两个关键词", "① 含有未知数；② 是等式（有等号）。两者缺一不可。"),
        "例如：x + 3 = 8、2x − 1 = 5、3a + 2b = 10 都是方程。",
        "反例：x + 3（没有等号，是代数式，不是方程）；3 + 5 = 8（没有未知数，不是方程）。",
    ],
    tip="判断是不是方程，就看两点：有没有未知数 + 是不是等式。"
)

example_slide(
    SEC1, "一、什么是方程 — 例题",
    "下列各式中，哪些是方程？(1) 3x−5  (2) 2x+1=7  (3) 5>3  (4) a+b=b+a  (5) 0.5y=10",
    [
        "(1) 3x−5 没有等号，是代数式，不是方程；",
        "(2) 2x+1=7 含未知数 x，又是等式 → 是方程；",
        "(3) 5>3 是不等式，不是等式 → 不是方程；",
        "(4) a+b=b+a 含未知数且是等式 → 是方程；",
        "(5) 0.5y=10 含未知数 y，又是等式 → 是方程。",
    ],
    "是方程的是：(2)、(4)、(5)。"
)

practice_slide(
    SEC1, "一、什么是方程 — 随堂练习",
    [
        "判断：x²+1 是不是方程？为什么？",
        "下列哪些是方程？ ① 4+6=10  ② 3x−2=7  ③ 2a+5  ④ m+n=8",
    ],
    [
        "x²+1 没有等号，是代数式，不是方程。",
        "②、④ 是方程（①无未知数，③无等号）。",
    ]
)

knowledge_slide(
    SEC1, "二、一元一次方程",
    [
        ("一元一次方程的定义",
         "只含有一个未知数（元），并且未知数的次数都是 1（次），这样的整式方程叫一元一次方程。"),
        ("三个条件", "① 只含一个未知数；② 未知数次数是 1；③ 是整式方程（分母中不含未知数）。"),
        "标准形式：ax + b = 0（其中 a、b 是常数，且 a ≠ 0）。",
        "例：2x+3=7 是；而 x²=4（次数为2）、1/x+1=3（分母含未知数）、x+y=5（两个未知数）都不是。",
    ],
    tip="“一元”=一个未知数，“一次”=未知数最高次数为1。a≠0 这个条件常被忽略，易考！"
)

example_slide(
    SEC1, "二、一元一次方程 — 例题",
    "若关于 x 的方程 (m−2)x + 3 = 0 是一元一次方程，求 m 的取值范围。",
    [
        "要使它是一元一次方程，x 的系数不能为 0，",
        "即 m − 2 ≠ 0，",
        "解得 m ≠ 2。",
    ],
    "当 m ≠ 2 时，该方程是一元一次方程。"
)

example_slide(
    SEC1, "二、一元一次方程 — 例题（含字母指数）",
    "若 (a−1)x^|a| + 5 = 0 是关于 x 的一元一次方程，求 a 的值。",
    [
        "“一次”要求未知数次数为1：|a| = 1，得 a = 1 或 a = −1；",
        "“系数不为0”要求 a − 1 ≠ 0，即 a ≠ 1；",
        "综合两条件，舍去 a = 1，",
        "故 a = −1。",
    ],
    "a = −1。",
    chip="易错例题", chip_color=C_ACCENT
)

practice_slide(
    SEC1, "二、一元一次方程 — 随堂练习",
    [
        "判断 3x−2=x+4 是不是一元一次方程？",
        "若 (k+1)x + 2 = 0 是一元一次方程，则 k 满足________。",
        "若 x^(m−1) + 3 = 0 是一元一次方程，则 m =________。",
    ],
    [
        "是（含一个未知数，次数为1）。",
        "k ≠ −1。",
        "m = 2。",
    ]
)

knowledge_slide(
    SEC1, "三、方程的解",
    [
        ("方程的解", "使方程左右两边相等的未知数的值，叫做方程的解。"),
        ("解方程", "求方程解的过程，叫做解方程。注意区分“方程的解”和“解方程”。"),
        ("验根方法", "把一个数代入方程，若左边 = 右边，则它是方程的解；否则不是。"),
        "例：x=3 代入 2x−1=5：左边=2×3−1=5=右边，所以 x=3 是该方程的解。",
    ],
    tip="“代入检验”是判断某个数是否为方程解的万能方法，也常用来求待定字母。"
)

example_slide(
    SEC1, "三、方程的解 — 例题",
    "已知 x = 2 是方程 3x − a = 4 的解，求 a 的值。",
    [
        "因为 x = 2 是方程的解，把 x = 2 代入方程：",
        "3 × 2 − a = 4，",
        "6 − a = 4，",
        "−a = 4 − 6 = −2，",
        "a = 2。",
    ],
    "a = 2。"
)

practice_slide(
    SEC1, "三、方程的解 — 随堂练习",
    [
        "检验 x = −1 是不是方程 4x + 7 = 3 的解。",
        "若 x = 5 是方程 2x − m = 3 的解，求 m。",
    ],
    [
        "左=4×(−1)+7=3=右，所以 x=−1 是解。",
        "2×5−m=3 → 10−m=3 → m=7。",
    ]
)

# ============================================================
# ===============  5.2 一元一次方程的解法  ===================
# ============================================================
SEC2 = "5.2 一元一次方程的解法"

knowledge_slide(
    SEC2, "一、等式的基本性质",
    [
        ("性质1", "等式两边都加上（或减去）同一个数或同一个式子，结果仍相等。"),
        ("    符号表示", "若 a = b，则 a ± c = b ± c。"),
        ("性质2", "等式两边都乘同一个数，或除以同一个不为0的数，结果仍相等。"),
        ("    符号表示", "若 a = b，则 ac = bc；若 a = b 且 c ≠ 0，则 a/c = b/c。"),
    ],
    tip="解方程的所有变形，本质都来源于这两条等式性质。除法时除数不能为0！"
)

example_slide(
    SEC2, "一、等式的性质 — 例题",
    "利用等式的性质解方程：x + 5 = 12。",
    [
        "根据等式性质1，两边同时减去 5：",
        "x + 5 − 5 = 12 − 5，",
        "x = 7。",
    ],
    "x = 7。"
)

knowledge_slide(
    SEC2, "二、移项",
    [
        ("移项", "把方程中的某一项，改变符号后，从等号一边移到另一边，叫做移项。"),
        ("移项依据", "等式的基本性质1（两边同加或同减）。"),
        ("移项口诀", "移项要变号：“+”变“−”，“−”变“+”。不移项的项不变号。"),
        "目的：把含未知数的项移到一边，常数项移到另一边。",
    ],
    tip="最常见错误就是【移项不变号】！记住：动了位置就要变号，没动就不变。"
)

example_slide(
    SEC2, "二、移项 — 例题",
    "解方程：2x − 3 = 5x + 6。",
    [
        "移项（把含 x 的项移到左边，常数项移到右边）：",
        "2x − 5x = 6 + 3，",
        "合并同类项：−3x = 9，",
        "两边同除以 −3：x = −3。",
    ],
    "x = −3。"
)

practice_slide(
    SEC2, "二、移项 — 随堂练习",
    [
        "解方程：3x + 4 = 16。",
        "解方程：5x − 2 = 2x + 7。",
    ],
    [
        "3x=16−4=12 → x=4。",
        "5x−2x=7+2 → 3x=9 → x=3。",
    ]
)

knowledge_slide(
    SEC2, "三、解一元一次方程的一般步骤",
    [
        ("① 去分母", "方程两边同乘各分母的最小公倍数（注意每一项都要乘）。"),
        ("② 去括号", "用乘法分配律去括号（注意括号前是“−”号时各项都要变号）。"),
        ("③ 移项", "含未知数的项移到一边，常数项移到另一边（移项要变号）。"),
        ("④ 合并同类项", "化成 ax = b 的形式。"),
        ("⑤ 系数化为1", "两边同除以未知数的系数 a，得 x = b/a。"),
    ],
    tip="五步法不是每题都全用，但顺序要牢记。去分母、去括号最容易漏乘、漏变号。"
)

example_slide(
    SEC2, "三、去括号解方程 — 例题",
    "解方程：3(x − 2) = 2(x + 1) − 4。",
    [
        "去括号：3x − 6 = 2x + 2 − 4，",
        "右边合并：3x − 6 = 2x − 2，",
        "移项：3x − 2x = −2 + 6，",
        "合并同类项：x = 4。",
    ],
    "x = 4。"
)

example_slide(
    SEC2, "三、去分母解方程 — 例题",
    "解方程：(2x − 1)/3 − (x + 2)/2 = 1。",
    [
        "两边同乘分母最小公倍数 6（每一项都乘）：",
        "2(2x − 1) − 3(x + 2) = 6，",
        "去括号：4x − 2 − 3x − 6 = 6，",
        "合并同类项：x − 8 = 6，",
        "移项：x = 6 + 8 = 14。",
    ],
    "x = 14。",
    chip="高频考点", chip_color=C_ACCENT
)

practice_slide(
    SEC2, "三、解法综合 — 随堂练习",
    [
        "解方程：2(x + 3) = 3(x − 1)。",
        "解方程：(x − 1)/2 = (x + 1)/3。",
    ],
    [
        "2x+6=3x−3 → −x=−9 → x=9。",
        "去分母×6：3(x−1)=2(x+1) → 3x−3=2x+2 → x=5。",
    ]
)

knowledge_slide(
    SEC2, "四、解法中的易错点小结",
    [
        ("去分母漏乘", "不含分母的项（如等号右边的整数）也必须乘以最小公倍数。"),
        ("去括号漏变号", "括号前是“−”号时，括号内每一项都要变号。"),
        ("移项不变号", "凡是移动位置的项，符号必须改变。"),
        ("系数化为1出错", "系数是分数时，要乘以它的倒数；注意正负号。"),
    ],
    tip="解完别忘了可以把答案代回原方程验算，确保左右两边相等。"
)

# ============================================================
# ===============  5.3 一元一次方程的应用  ===================
# ============================================================
SEC3 = "5.3 一元一次方程的应用"

knowledge_slide(
    SEC3, "一、列方程解应用题的一般步骤",
    [
        ("① 审", "审题，弄清已知量、未知量及它们之间的相等关系。"),
        ("② 设", "设未知数（直接设或间接设），注意写清单位。"),
        ("③ 列", "找出相等关系，列出方程。（关键步骤！）"),
        ("④ 解", "解这个方程，求出未知数的值。"),
        ("⑤ 验、答", "检验解是否符合题意，再写出答语。"),
    ],
    tip="解应用题的核心是【找等量关系】，这是列方程的关键，也是考试得分点。"
)

example_slide(
    SEC3, "二、和差倍分问题 — 例题",
    "某班共有学生 50 人，其中男生比女生的 2 倍少 4 人，求男、女生各多少人。",
    [
        "设女生有 x 人，则男生有 (2x − 4) 人。",
        "等量关系：男生 + 女生 = 50，",
        "列方程：x + (2x − 4) = 50，",
        "去括号合并：3x − 4 = 50，",
        "解得：3x = 54，x = 18，男生 = 2×18 − 4 = 32。",
    ],
    "女生 18 人，男生 32 人。"
)

practice_slide(
    SEC3, "二、和差倍分 — 随堂练习",
    [
        "两个数的和是 36，大数是小数的 3 倍，求这两个数。",
    ],
    [
        "设小数为 x，则大数 3x，x+3x=36 → x=9，大数=27。",
    ]
)

example_slide(
    SEC3, "三、行程问题 — 例题（相遇）",
    "甲、乙两地相距 300 km，一辆快车与一辆慢车同时从两地相向开出，快车速度 70 km/h，慢车 50 km/h，几小时后两车相遇？",
    [
        "设经过 x 小时后两车相遇。",
        "等量关系：快车路程 + 慢车路程 = 总路程，",
        "列方程：70x + 50x = 300，",
        "合并：120x = 300，",
        "解得：x = 2.5。",
    ],
    "2.5 小时后两车相遇。"
)

example_slide(
    SEC3, "三、行程问题 — 例题（追及）",
    "弟弟以 60 m/min 的速度先出发 5 分钟，哥哥以 90 m/min 的速度去追，问哥哥几分钟追上弟弟？",
    [
        "设哥哥出发 x 分钟后追上弟弟。",
        "弟弟先走 5 分钟，多走了 60×5 = 300 m。",
        "等量关系：哥哥路程 = 弟弟路程，",
        "列方程：90x = 60x + 300，",
        "移项：90x − 60x = 300 → 30x = 300，x = 10。",
    ],
    "哥哥出发 10 分钟后追上弟弟。",
    chip="高频考点", chip_color=C_ACCENT
)

practice_slide(
    SEC3, "三、行程问题 — 随堂练习",
    [
        "A、B 两地相距 240 km，两车相向而行，速度分别为 50、70 km/h，几小时相遇？",
    ],
    [
        "50x+70x=240 → 120x=240 → x=2（小时）。",
    ]
)

example_slide(
    SEC3, "四、工程问题 — 例题",
    "一项工程，甲单独做 10 天完成，乙单独做 15 天完成。两人合作，需要多少天完成？",
    [
        "把总工程量看作单位“1”，甲每天做 1/10，乙每天做 1/15。",
        "设合作 x 天完成。",
        "等量关系：甲做的 + 乙做的 = 1，",
        "列方程：x/10 + x/15 = 1，",
        "去分母（×30）：3x + 2x = 30 → 5x = 30，x = 6。",
    ],
    "两人合作需要 6 天完成。"
)

practice_slide(
    SEC3, "四、工程问题 — 随堂练习",
    [
        "一水池，甲管单独注满需 6 h，乙管需 12 h，两管齐开几小时注满？",
    ],
    [
        "x/6+x/12=1 → ×12：2x+x=12 → 3x=12 → x=4（小时）。",
    ]
)

example_slide(
    SEC3, "五、销售（利润）问题 — 例题",
    "某商品进价 80 元，标价 120 元，商店打折销售，要使利润率为 20%，应打几折？",
    [
        "利润率 20%，则售价 = 进价 ×(1+20%) = 80×1.2 = 96 元。",
        "设打 x 折，则售价 = 标价 × (x/10) = 120 × x/10。",
        "列方程：120 × x/10 = 96，",
        "即 12x = 96，",
        "解得：x = 8。",
    ],
    "应打 8 折。",
    chip="高频考点", chip_color=C_ACCENT
)

practice_slide(
    SEC3, "五、销售问题 — 随堂练习",
    [
        "一件衣服进价 200 元，售价 260 元，利润率是多少？",
        "某商品按标价 9 折出售为 90 元，求标价。",
    ],
    [
        "(260−200)/200×100% = 30%。",
        "设标价 x，0.9x=90 → x=100（元）。",
    ]
)

example_slide(
    SEC3, "六、配套问题 — 例题",
    "某车间 26 名工人生产螺钉和螺母，每人每天生产螺钉 800 个或螺母 1200 个，1 个螺钉配 2 个螺母。应分配多少人生产螺钉，才能使产品恰好配套？",
    [
        "设安排 x 人生产螺钉，则 (26 − x) 人生产螺母。",
        "配套关系：螺母总数 = 2 × 螺钉总数，",
        "列方程：1200(26 − x) = 2 × 800x，",
        "去括号：31200 − 1200x = 1600x，",
        "移项合并：31200 = 2800x，x = 12（取整数符合）。",
    ],
    "安排约 12 人生产螺钉（与题中数据匹配时恰好配套）。",
    chip="拓展例题", chip_color=C_ACCENT
)

# ============================================================
# ===============  本章小结与易错点  =========================
# ============================================================
s = add_slide()
content_header(s, "第五章 一元一次方程", "本章小结 · 考试重点")
y = Inches(1.4)
add_round_rect(s, Inches(0.8), y, Inches(11.7), Inches(5.4), C_WHITE, line_color=C_PRIMARY)
summary = [
    P(R("一、核心概念", 20, C_PRIMARY, True)),
    P(R("   方程、一元一次方程（一个未知数、次数为1、a≠0）、方程的解。", 16, C_DARK, False)),
    P(R("二、解法五步", 20, C_ORANGE, True)),
    P(R("   去分母 → 去括号 → 移项 → 合并同类项 → 系数化为1。", 16, C_DARK, False)),
    P(R("三、应用题题型（高频）", 20, C_GREEN, True)),
    P(R("   和差倍分、行程（相遇/追及）、工程、销售利润、配套问题。", 16, C_DARK, False)),
    P(R("四、易错点（务必牢记）", 20, C_ACCENT, True)),
    P(R("   ① 移项不变号；② 去括号漏变号；③ 去分母漏乘不含分母的项；", 16, C_DARK, False)),
    P(R("   ④ 系数化为1时符号或倒数出错；⑤ 应用题忘记检验和写答语。", 16, C_DARK, False)),
    P(R("五、解题建议", 20, C_PRIMARY, True)),
    P(R("   应用题关键是【找等量关系】；解完代回原方程验算更稳妥。", 16, C_DARK, False)),
]
add_text(s, Inches(1.1), y + Inches(0.2), Inches(11.1), Inches(5.0),
         summary, line_spacing=1.25)

# 结束页
s = add_slide()
set_bg(s, C_PRIMARY)
add_text(s, Inches(0.8), Inches(2.9), Inches(11.7), Inches(1.2),
         [P(R("同学们，多练多悟，", 36, C_WHITE, True))],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(4.0), Inches(11.7), Inches(1.0),
         [P(R("方程的世界很精彩！", 36, C_LIGHT, True))],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------------- 保存 ----------------
out = "一元一次方程-教学课件.pptx"
prs.save(out)
print("生成成功：", out, "  共", len(prs.slides._sldIdLst), "页")
