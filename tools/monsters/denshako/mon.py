# デンシャコ（でんき・かくとう × シャコ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：電気を おびた 金の こぶし（捕脚の こぶ ⇔ ボクシングの こぶし）
META = dict(id='denshako', name='デンシャコ', types=['elec', 'fighting'], base='シャコ', size='M')
PAL = {
    'k': '#101018', 'l': '#15283e',
    'A': '#8ee0e8', 'B': '#3c98b4', 'D': '#1f5470',      # 甲羅（青緑）
    'O': '#ffa250', 'P': '#d05a28', 'o': '#7a2a1a',      # 脚・尾扇（だいだい）
    'Y': '#fff27a', 'y': '#f0aa20', 'g': '#9a5410',      # 金の こぶし・目
    'w': '#ffffff', 'C': '#9cf6ff',                      # 光・火花
    't': '#c8c8d8', 'r': '#b81c34',                      # テープ・口の 中
}
LIGHT = set('AOYwCt')
KEEP_BLACK = set('wYCr')
# ---------- 下書きの 道具（あたり → 左上光の 3段 → 輪郭。目・牙・模様・線は 手で 打つ）----------
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, poly, line
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def E(g, cx, cy, rx, ry, ch='1'): ellipse(g, cx, cy, rx, ry, ch)
def P(g, pts, ch='1'): poly(g, pts, ch)
def Ln(g, x0, y0, x1, y1, ch): line(g, x0, y0, x1, y1, ch)
def dots(g, ch, pts, on=None):
    """手で 1ドットずつ 打つ（on を 指定すると その 色の 上だけ）"""
    for x, y in pts:
        if 0 <= x < N and 0 <= y < N and (on is None or g[y][x] in on): g[y][x] = ch
def hand(g, x, y, rows):
    """手打ちの 絵（文字の 行）を はりつける。'.' は すける"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= x + i < N and 0 <= y + j < N: g[y + j][x + i] = c
def shade(g, ramps, lw=1, dw=2):
    """マスクに 光（左上）：上・左の ふち lw は 明、下・右の ふち dw は 暗"""
    src = [r[:] for r in g]
    for y in range(N):
        for x in range(N):
            m = src[y][x]
            if m not in ramps: continue
            Lc, Mc, Dc = ramps[m]
            def run(dy, dx):
                i = 1
                while i < 9 and at(src, x + dx * i, y + dy * i) == m: i += 1
                return i
            dr = min(run(1, 0), run(0, 1) + 1); ul = min(run(-1, 0), run(0, -1))
            g[y][x] = Dc if dr <= dw else Lc if ul <= lw else Mc
def part(draw, ramps, lw=1, dw=2, post=None, cut=()):
    """1つの パーツ：draw で 形 → 陰影 → post で 手打ち → 輪郭。cut の 四角では 輪郭を 開けて 体と つなぐ"""
    g = G(); draw(g); shade(g, ramps, lw, dw)
    if post: post(g)
    rows = [list(r) for r in outline(rows_of(g))]
    for (x0, y0, x1, y1) in cut:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if rows[y + 1][x + 1] == 'k' and at(g, x, y) == '.': rows[y + 1][x + 1] = '.'
    return [''.join(r) for r in rows]
def L(n, gr, rows, **kw): return dict(n=n, g=gr, x=-1, y=-1, rows=rows, **kw)
def H(n, gr, x, y, rows, **kw): return dict(n=n, g=gr, x=x, y=y, rows=rows, **kw)

SH = {'1': 'ABD'}; OR = {'2': 'OPo'}; GD = {'3': 'Yyg'}

# ---- 尾扇（だいだいの 扇。とげ 3本）----
def tail_d(g):
    P(g, [(17, 50), (7, 45), (6, 48), (10, 52), (5, 54), (6, 57), (12, 56), (9, 60), (13, 60), (18, 56)], '2')
def tail_p(g):
    Ln(g, 16, 51, 9, 47, 'o'); Ln(g, 16, 54, 8, 55, 'o'); Ln(g, 16, 56, 12, 59, 'o')
    dots(g, 'O', [(7, 46), (8, 46), (6, 54), (7, 54)], 'P')
TAIL = part(tail_d, OR, post=tail_p)
# ---- 腹（節の ある 短い 胴。地面に ふせて 尾へ）----
def abd_d(g):
    E(g, 24, 51, 8, 6.5); E(g, 17, 53, 5, 4.5)
def abd_p(g):
    for x, y0, y1 in ((16, 49, 57), (21, 45, 57), (26, 45, 57)):
        for y in range(y0, y1):
            if g[y][x] != '.': g[y][x] = 'l'
            if at(g, x + 1, y) in 'BD' and y < y0 + 4: g[y][x + 1] = 'A'
    dots(g, 'A', [(19, 48), (23, 46), (24, 46), (28, 46)], 'BD')
    dots(g, 'y', [(24, 49), (29, 50)], 'BAD')            # 節の 電気の つぶ
ABD = part(abd_d, SH, dw=2, post=abd_p)
# ---- 胸（丸く 小さい）----
def body_d(g):
    E(g, 34, 46, 8, 9)
def body_p(g):
    Ln(g, 28, 46, 34, 40, 'l'); Ln(g, 29, 52, 40, 42, 'l')
    dots(g, 'A', [(30, 46), (31, 45), (32, 44), (31, 52), (33, 50), (35, 48)], 'BD')
    for x in range(30, 41): 
        if g[55][x] != '.': g[55][x] = 'l'
BODY = part(body_d, SH, dw=3, post=body_p)
# ---- 頭（よろいの かぶと。前に とがった 鼻先の 板）----
def head_d(g):
    P(g, [(29, 29), (31, 24), (36, 21), (44, 20), (53, 22), (58, 26), (60, 29), (56, 32), (51, 36), (43, 38), (33, 38), (29, 35)]); E(g, 45, 20, 5.5, 4.5)
def head_p(g):
    # かぶとの ふち（後ろの 板の 段）と 鼻先の 板
    Ln(g, 34, 23, 32, 35, 'l'); dots(g, 'A', [(33, 24), (33, 26), (33, 28)], 'BD')
    Ln(g, 51, 22, 59, 28, 'l')
    for x in range(52, 59): dots(g, 'A', [(x, 23 + (x - 52) * 6 // 7)], 'BD')
    # ほおの 甲羅の 線
    Ln(g, 36, 31, 44, 34, 'l')
    dots(g, 'A', [(36, 23), (37, 22), (38, 22), (40, 21)], 'B')
    # 口：するどい 牙が 並ぶ
    hand(g, 47, 31, ['kkkkkkkkk', 'wkwkwkwk.', '.k.k.k.k.'])
def head_open(g):
    head_p(g)
    hand(g, 46, 31, ['kkkkkkkkkk', 'wkwkwkwkk.', 'krrrrrrk..', 'kwkwkwk...'])
HEAD = part(head_d, SH, dw=3, post=head_p)
HEAD_OPEN = part(head_d, SH, dw=3, post=head_open)
# 触角（後ろへ 2本、先に 平たい 鱗片）
def ant_d(g):
    Ln(g, 37, 23, 31, 15, '1'); Ln(g, 38, 23, 32, 15, '1'); Ln(g, 41, 21, 38, 13, '1'); Ln(g, 42, 21, 39, 13, '1')
    P(g, [(29, 13), (26, 11), (27, 9), (31, 11), (33, 16), (31, 17)], '2')
ANT = part(ant_d, {'1': 'ABD', '2': 'OPo'}, dw=1)
# ---- 目：白い 光＋金の 虹彩（明 Y・暗 y）＋たての ひとみ。厚い まゆ板で かこむ ----
EYE = ['kkk.....', '.kkkkkk.', '.kwYYkYk', '..kyykyk', '...kkkk.']
EYE_ALT = {
    'blink': ['kkk.....', '.kkkkkk.', '..kkkkkk', '........', '........'],
    'atk0|atk1|atk2': ['kkkk....', '.kkkkkkk', '.kwwYkYk', '..kyykk.', '...kkk..'],
    'hit': ['kkk.....', '.kkkkkk.', '..kk....', '....kkk.', '..kk....'],
    'ko': ['........', '.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
}
# ---- 脚（短く 太い 2本）----
def leg_d(x, top=50):
    def d(g): P(g, [(x, top), (x + 5, top), (x + 5, 57), (x + 7, 58), (x + 7, 60), (x - 1, 60), (x, 57)], '2')
    return d
def leg_p(x):
    def p(g): dots(g, 'w', [(x + 1, 59), (x + 4, 59), (x + 6, 59)])
    return p
LEG_F = part(leg_d(36), OR, post=leg_p(36), cut=((35, 50, 42, 52),))
LEG_B = part(leg_d(28), {'2': 'Poo'}, post=leg_p(28))
# ---- 捕脚の こぶし（見せ所）：うで（甲羅）＋金の こぶ＋手首の テープ ----
def arm(cx, cy, ax=38, ay=43, r=7.5):
    def d(g):
        # うで：胸の 中から こぶしへ（つけ根は 胸に 3ドット もぐる）
        for i in range(0, 11):
            t = i / 10; x = ax + (cx - r - ax) * t; y = ay + (cy - ay) * t
            E(g, x, y, 2.8, 2.8, '1')
        E(g, cx, cy, r, r, '3')
    def p(g):
        # 指の みぞ（ボクシングの グローブ）と 光の 三日月
        for k in (-4, -1, 2):
            for j in range(-1, 5):
                dots(g, 'g', [(int(cx + 1 + j), int(cy + k + (j > 1)))], 'Yy')
        dots(g, 'w', [(int(cx - 4), int(cy - 4)), (int(cx - 3), int(cy - 5)), (int(cx - 5), int(cy - 3))], 'Yy')
        # 親指
        Ln(g, int(cx - 3), int(cy + 4), int(cx + 3), int(cy + 4), 'g')
        # 手首の テープ（かくとう）
        wx = int(cx - r) - 1
        for y in range(int(cy - 4), int(cy + 5)):
            for x in (wx - 1, wx, wx + 1):
                if g[y][x] != '.': g[y][x] = 'l' if (y - int(cy)) % 3 == 0 else 't'
    return part(d, {'1': 'ABD', '3': 'Yyg'}, dw=2, post=p)
ARM = arm(51, 45, r=8.5); ARM_BACK = arm(45, 47, r=8); ARM_PUNCH = arm(56, 43, ax=40, ay=43, r=8.5); ARM_2 = arm(55, 44, r=8.5)
# ---- 電気（こぶしに ふれて はじける。atk の 稲妻は はなれた エフェクト＝意図的）----
SPARK1 = ['..k.....', '.kCk.k..', '.kwCkCk.', 'kCkwCwk.', '.k.kwk..', '...kk...']
SPARK2 = ['.....k..', '..k.kCk.', '.kCkwCk.', '.kwCwk..', 'kCkk....', '.k......']
BOLT = [
    '..........kk......',
    '...kk....kwCk..kk.',
    '..kwCk..kwCk..kwCk',
    'kkwCwCkkwCCkkkwCk.',
    'CwwwwwwwwwwwwwwwCk',
    'kkCwCkkwCwCkkCwk..',
    '..kCk..kCkkwCk.kk.',
    '...k....k..kCk....',
    '............k.....',
]
BOLT2 = ['..kk.....', '.kwCk.kk.', 'kwCwkkwCk', 'CwwwwwwCk', 'kCkkCwk..', '.k...k...']

def layers():
    return [
        L('legB', 'legB', LEG_B, not_='ko'),
        L('ant', 'head', ANT),
        L('tail', 'tail', TAIL),
        L('abd', 'body', ABD),
        L('body', 'body', BODY),
        L('legA', 'legA', LEG_F),
        L('head', 'head', HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        H('eye', 'head', 41, 19, EYE, alt=EYE_ALT),
        L('arm', 'arm', ARM, alt={'atk0': ARM_BACK, 'atk1': ARM_PUNCH, 'atk2': ARM_2}),
        H('spk', 'arm', 52, 32, SPARK1, alt={'idle1|idle3|walk1|walk3': SPARK2}, not_='atk0|atk1|atk2|hit|ko'),
        H('bolt', 'arm', 64, 38, BOLT, only='atk1'),
        H('bolt2', 'arm', 63, 41, BOLT2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'head': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, -1)}, 'idle3': {'arm': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1), 'tail': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1), 'tail': (0, -1)},
    'atk0': {'body': (-1, 1), 'tail': (1, 0)}, 'atk1': {'root': (4, 0)}, 'atk2': {'root': (3, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'arm': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'arm': 'body', 'body': 'root', 'tail': 'body', 'legA': 'root', 'legB': 'root'}
