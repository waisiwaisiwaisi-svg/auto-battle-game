# ハスガッパ（くさ・みず × 河童）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：水かきの ついた 大きな 爪の 手
META = dict(id='hasugappa', name='ハスガッパ', types=['grass', 'water'], base='河童', size='M')
PAL = {
    'k': '#101018', 'l': '#16301e',
    'A': '#a6e27c', 'B': '#4c9e4c', 'D': '#245c36',      # 肌（みどり）
    'F': '#d8f49a',                                      # 蓮の 葉の 光
    'S': '#dccb7c', 'T': '#9c8a42', 'U': '#584620',      # 蓮の 実の 甲羅
    'Y': '#ffde66', 'O': '#c8801e',                      # くちばし・爪の 根
    'R': '#ff6a4a', 'r': '#a01c28',                      # 目（赤い 虹彩）
    'w': '#ffffff', 'C': '#8ee4ff', 'c': '#3a88d8',      # 光・水
}
LIGHT = set('AFSYwC')
KEEP_BLACK = set('wR')
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

SK = {'1': 'ABD'}; SKD = {'1': 'BDD'}
# ---- 甲羅＝蓮の 実（穴に 種が のぞく）----
def shell_d(g):
    P(g, [(14, 34), (22, 30), (28, 33), (29, 48), (22, 52), (15, 48), (12, 41)], '2')
def shell_p(g):
    for (x, y) in ((17, 35), (22, 34), (16, 41), (21, 40), (18, 46), (23, 46)):
        hand(g, x, y, ['UU', 'UY'])
    Ln(g, 14, 38, 27, 36, 'T'); Ln(g, 14, 44, 27, 43, 'T')
SHELL = part(shell_d, {'2': 'STU'}, lw=2, dw=2, post=shell_p)
# ---- 胴（小さく 丸い。おなかは 明るい）----
def body_d(g): E(g, 30, 42.5, 8.5, 9)
def body_p(g):
    for y in range(37, 50):
        for x in range(31, 37):
            if g[y][x] in 'B' and (x - 33) ** 2 + (y - 44) ** 2 < 14: g[y][x] = 'A'
    Ln(g, 30, 40, 30, 49, 'D')
BODY = part(body_d, SK, dw=3, post=body_p)
# ---- 足（短く 太い。水かきの 足）----
def leg(x, ramp, cut=True):
    def d(g):
        P(g, [(x, 47), (x + 6, 47), (x + 6, 56), (x + 9, 58), (x + 9, 61), (x - 1, 61), (x, 57)])
    def p(g):
        dots(g, 'w', [(x + 3, 60), (x + 6, 60), (x + 9, 60)]); dots(g, 'D', [(x + 4, 59), (x + 7, 59)], 'ABD')
    return part(d, {'1': ramp}, post=p, cut=((x - 1, 46, x + 7, 49),) if cut else ())
LEG_F = leg(31, 'ABD'); LEG_B = leg(22, 'BDD', False)
# ---- 頭（くちばし＋蓮の 葉の 皿）----
def head_d(g):
    E(g, 35, 23, 11, 9.5)
    P(g, [(42, 22), (52, 23), (56, 26), (52, 30), (42, 31)], '3')
def head_p(g, open_=False):
    # 首の 下の 影
    for x in range(26, 44): dots(g, 'D', [(x, 31)], 'AB')
    # くちばしの 線（ぎざぎざ）
    if not open_:
        hand(g, 44, 26, ['kkkkkkkkkkk', '.k.kwk.kwk.'])
    else:
        hand(g, 43, 25, ['kkkkkkkkkkkk', 'kwkwkwkwkk..', 'krrrrrrrk...', 'kwkwkwkk....'])
    dots(g, 'w', [(46, 23), (47, 23)], 'YO')
    # ほおの 水の すじ
    dots(g, 'D', [(30, 25), (31, 26), (29, 27), (30, 28)], 'AB')
HEAD = part(head_d, {'1': 'ABD', '3': 'YOO'}, lw=2, dw=3, post=head_p)
HEAD_OPEN = part(head_d, {'1': 'ABD', '3': 'YOO'}, lw=2, dw=3, post=lambda g: head_p(g, True))
# 皿＝蓮の 葉（丸く 平ら、まん中から すじ。前に 切れこみ）
def leaf_d(g):
    E(g, 33, 13, 14, 4.5, '4')
def leaf_p(g, drop=0):
    for ang in range(-6, 7, 2):
        Ln(g, 33, 14, 33 + ang * 2, 9 if abs(ang) < 5 else 12, 'B')
    Ln(g, 33, 14, 21, 14, 'B'); Ln(g, 33, 14, 45, 15, 'B')
    dots(g, 'D', [(33, 14), (34, 14)])
    for x in range(20, 47):                      # 葉の ふちは 少し めくれて 濃い
        if at(g, x, 17) != '.': g[17][x] = 'D'
    dots(g, '.', [(46, 12), (47, 13), (46, 13)])  # 前の 切れこみ
    hand(g, 26 + drop, 10, ['wC', 'Cc'])          # 葉の 上の しずく
LEAF = part(leaf_d, {'4': 'FAB'}, lw=1, dw=1, post=leaf_p)
LEAF2 = part(leaf_d, {'4': 'FAB'}, lw=1, dw=1, post=lambda g: leaf_p(g, 1))
# ---- 目：白い 光＋赤い 虹彩（明 R・暗 r）＋たての ひとみ。太い まゆ ----
EYE = ['kkkk....', '.kkkkkk.', '.kwRRkRk', '..krrkrk', '...kkkk.']
EYE_ALT = {
    'blink': ['kkkk....', '.kkkkkk.', '..kkkkkk'],
    'atk0|atk1|atk2': ['kkkkk...', '.kkkkkkk', '.kwwRkRk', '..krrkk.', '...kkk..'],
    'hit': ['kkk.....', '..kk....', '....kkk.', '..kk....'],
    'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
}
# ---- 手：水かきの 大きな 爪（見せ所）。腕の つけ根は 胴に 3ドット もぐる ----
def arm(hx, hy, sx=34, sy=39, ramp='ABD'):
    def d(g):
        for i in range(11):
            t = i / 10; E(g, sx + (hx - sx) * t, sy + (hy - sy) * t, 3, 3, '1')
        # 水かき（指の 間の 大きな 膜）
        P(g, [(hx, hy - 5), (hx + 8, hy - 9), (hx + 12, hy - 2), (hx + 11, hy + 5), (hx + 6, hy + 8), (hx, hy + 5)], '5')
        E(g, hx, hy, 5.5, 5.5, '1')
    def p(g):
        # 3本の 太い 指と 白く するどい 爪
        for (fx, fy), (ax, ay), (bx, by) in (((hx + 2, hy - 3), (hx + 7, hy - 8), (hx + 12, hy - 12)),
                                             ((hx + 4, hy), (hx + 11, hy - 1), (hx + 17, hy - 3)),
                                             ((hx + 2, hy + 3), (hx + 7, hy + 7), (hx + 12, hy + 10))):
            Ln(g, fx, fy, ax, ay, 'D'); Ln(g, fx, fy - 1, ax, ay - 1, 'A'); Ln(g, fx + 1, fy, ax + 1, ay, 'B')
            Ln(g, ax, ay, bx, by, 'w'); Ln(g, ax, ay + 1, bx, by + 1, 'C'); Ln(g, ax + 1, ay + 1, bx - 1, by + 1, 'C'); dots(g, 'O', [(ax, ay)])
        for x, y in ((hx + 6, hy - 4), (hx + 8, hy + 3)): dots(g, 'C', [(x, y), (x + 1, y)], 'FAB')
        dots(g, 'A', [(hx - 3, hy - 3), (hx - 2, hy - 4), (hx - 1, hy - 4)], 'BD')
    return part(d, {'1': ramp, '5': 'FAB'}, dw=1, post=p)
ARM = arm(44, 43); ARM_UP = arm(39, 47); ARM_HIT = arm(49, 41); ARM_2 = arm(47, 45)
ARM_B = arm(21, 45, sx=27, sy=39, ramp='BDD')
# ---- 水の 斬撃（攻撃。はなれた エフェクト＝意図的）----
SLASH = [
    '......kkk...',
    '....kkCwCk..',
    '...kCwwCck..',
    '..kCwCckk...',
    '.kCwCk......',
    '.kwCk.......',
    'kCwk........',
    'kwCk........',
    'kCwk........',
    '.kwCk.......',
    '.kCwCk......',
    '..kCwCckk...',
    '...kCwwCck..',
    '....kkCwCk..',
    '......kkk...',
]
SPL = ['k.kk.', 'Ck.Ck', '.kCwk', 'kCk..']

def layers():
    return [
        L('armB', 'body', ARM_B, not_='ko'),
        L('legB', 'legB', LEG_B),
        L('shell', 'body', SHELL),
        L('body', 'body', BODY),
        L('legA', 'legA', LEG_F),
        H('head', 'head', -1, 1, HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        H('leaf', 'leaf', -1, 1, LEAF, alt={'idle1|idle2|walk1|walk3': LEAF2}),
        H('eye', 'head', 34, 19, EYE, alt=EYE_ALT),
        L('arm', 'arm', ARM, alt={'atk0': ARM_UP, 'atk1': ARM_HIT, 'atk2': ARM_2}),
        H('slash', 'arm', 63, 34, SLASH, only='atk1'),
        H('spl', 'arm', 63, 44, SPL, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'head': (0, 0)}, 'idle2': {'body': (0, 1), 'leaf': (0, -1)}, 'idle3': {'arm': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 0), 'head': (-1, 1)}, 'atk1': {'root': (3, 0), 'head': (1, 0)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'arm': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'leaf': 'head', 'head': 'body', 'arm': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
