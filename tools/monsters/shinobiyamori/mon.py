# シノビヤモリ（あく・かくとう × ヤモリ）手打ち GBA風・デフォルメ（2〜3頭身）
META = dict(id='shinobiyamori', name='シノビヤモリ', types=['dark', 'fighting'], base='ヤモリ', size='M')
PAL = {
    'k': '#101018', 'l': '#33221a',
    'A': '#f0d878', 'B': '#c49a48', 'C': '#6e4e2a',
    'N': '#6e6490', 'M': '#423a5e', 'O': '#221d36',
    'R': '#f05050', 'D': '#8e2028',
    'S': '#eef2fa', 'T': '#8a92b0',
    'Y': '#86f4e4', 'E': '#2a9a9c',
    'w': '#ffffff',
}
LIGHT = set('ANRSYw')
import pix
from pix import grid, rows_of, outline, ellipse, poly, line, recolor


# ---- 下書きの 道具（あたりは 図形で、仕上げは 手で 打つ）----
def G(w, h): return grid(w, h)
def ell(g, cx, cy, rx, ry, ch): ellipse(g, cx, cy, rx, ry, ch); return g
def pl(g, pts, ch): poly(g, pts, ch); return g
def thick(g, pts, ch, w=2):
    """太い 線（尾・首などの あたり）"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for dx in range(w):
            for dy in range(w): line(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, ch)
    return g
def edge(g, mats, ch='k'):
    """素材の さかい目に 内側の 線（あとで エンジンが 濃い色に する）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if src[y][x] not in mats: continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and src[yy][xx] not in mats and src[yy][xx] not in '.k': g[y][x] = ch; break
    return g
def shade(g, ramps, hl=1, dk=2, dr=1):
    """光は 左上：上・左の ふち hl ドットは 明、下の ふち dk・右の ふち dr ドットは 暗"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, m):
        n = 0
        while n < 9 and 0 <= y + dy * (n + 1) < H and 0 <= x + dx * (n + 1) < W and src[y + dy * (n + 1)][x + dx * (n + 1)] == m: n += 1
        return n
    for y in range(H):
        for x in range(W):
            m = src[y][x]
            if m not in ramps: continue
            L, M, D = ramps[m]
            u, l, d, r = run(y, x, -1, 0, m), run(y, x, 0, -1, m), run(y, x, 1, 0, m), run(y, x, 0, 1, m)
            c = M
            if d < dk or r < dr: c = D
            elif u < hl or l < hl: c = L
            g[y][x] = c
    return g
def at(g, x, y, *rows):
    """手打ち：( x, y ) から 文字を 置く（空白と '.' は そのまま）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c not in ' .' and 0 <= y + j < len(g) and 0 <= x + i < len(g[y + j]): g[y + j][x + i] = c
    return g
def done(g, open_top=0, open_left=0):
    """輪郭を つける。付け根側の 輪郭を 開けて 体に なじませる"""
    rows = [list(r) for r in outline(rows_of(g))]
    for y in range(open_top): rows[y] = ['.' if c == 'k' else c for c in rows[y]]
    for r in rows:
        for x in range(open_left):
            if r[x] == 'k': r[x] = '.'
    return [''.join(r) for r in rows]
SK = {'g': 'ABC', 'n': 'NMO', 'r': 'RRD', 'a': 'AAB', 's': 'SST'}
DARKER = {'A': 'B', 'B': 'C', 'C': 'l', 'N': 'M', 'M': 'O', 'O': 'l', 'S': 'T', 'R': 'D'}
def dark(rows): return recolor(rows, DARKER)


# ---- 胴：忍び装束（紺）に 赤い 帯 ----
def body():
    g = G(22, 21)
    ell(g, 11, 11, 8.5, 8.5, 'n')
    pl(g, [(1, 12), (21, 9), (21, 12), (1, 15)], 'r')              # 赤い 帯（ななめ）
    pl(g, [(10, 1), (19, 2), (20, 9), (13, 12)], 'a')               # 前の あいた 装束から のぞく 腹
    edge(g, 'r'); edge(g, 'a')
    shade(g, SK, hl=1, dk=3, dr=2)
    at(g, 15, 4, 'B'); at(g, 14, 7, 'BB')
    at(g, 6, 5, 'M'); at(g, 5, 6, 'M'); at(g, 8, 17, 'O')            # 布の しわ（手打ち）
    at(g, 4, 11, 'kk')                                               # 帯の むすび目
    return done(g)

# ---- 足：短く がにまた、指先は 丸い 吸盤 ----
LEG_M = [
    '..gggggg...',
    '.gggggggg..',
    '.ggggggggg.',
    '..gggggggg.',
    '...ggggg...',
    '...gggggg..',
    '..gggggggg.',
    '.gggggggggg',
]
def leg():
    g = [list(r) for r in LEG_M]; shade(g, SK, dk=1)
    at(g, 6, 3, 'C'); at(g, 4, 2, 'C')
    r = [list(x) for x in done(g, open_top=2)]
    at(r, 0, 8, 'kA'); at(r, 10, 7, 'kA'); at(r, 6, 9, 'kAk.kA')     # 指先の 吸盤
    return rows_of(r)

# ---- 尾：太く 先へ 細る、くるりと 巻く（しまもよう）----
def tail():
    g = G(20, 15)
    thick(g, [(18, 5), (12, 8), (7, 10), (3, 9), (2, 6), (3, 3)], 'g', 3)
    thick(g, [(4, 2), (6, 1)], 'g', 2)
    shade(g, SK, dk=1)
    for x, y in ((14, 7), (15, 7), (9, 9), (10, 9), (5, 10), (2, 7), (3, 4)): g[y][x] = 'C' if g[y][x] != '.' else '.'
    return done(g)

# ---- 頭：平たく 大きい ヤモリの 頭、上に 大きな 目、ずきんを かぶる ----
def head(ko=False, eye=None, mouth=0):
    g = G(31, 21)
    ell(g, 14.5, 11.5, 14, 8, 'g')                                  # 頭（横に 広い）
    hood = G(31, 21); ell(hood, 9, 8, 10.5, 8, 'n')
    for y in range(21):
        for x in range(31):
            if hood[y][x] == 'n' and g[y][x] == 'g' and (y < 10 - x // 6 or x < 6): g[y][x] = 'n'
    ell(g, 19, 6.5, 6, 4, 'g')                                  # 目の もり上がり
    edge(g, 'n')
    shade(g, SK, hl=1, dk=3, dr=1)
    at(g, 3, 9, 'MMM'); at(g, 6, 4, 'OO')                            # ずきんの しわ
    at(g, 22, 9, 'k'); at(g, 26, 10, 'k')                            # 鼻の あな
    for x, y in ((11, 11), (8, 14), (16, 10), (12, 16)): at(g, x, y, 'C')     # ヒョウもん
    # 口：横に 長く さけた 口と 小さな 牙
    if mouth:
        at(g, 13, 13, '.kkkkkkkkkkkkkkk', 'kDDDDDDDDDDDDDkk', '.kwkDDDDDDwkkk', '..kkkkkkkkkk')
    else:
        at(g, 13, 14, 'kkkkkkkkkkkkkkkk', '.kwk.....kwk')
        at(g, 13, 13, 'k')
    # 目：白い 光＋黄と 金の 虹彩＋たての ひとみ、まゆの 線
    if ko: e = ['.k...k.', '..k.k..', '...k...', '..k.k..']
    else: e = eye or ['kkkk....', 'kwYYYkYk', 'kYEEEkEk', '.kkkkkk.']
    at(g, 15, 4, *e)
    at(g, 14, 3, 'kkkk')                                              # まゆの ひさし
    return done(g)
EYE_BLINK = ['kkkk....', 'kBBBBBBk', 'kkkkkkkk', '.BBBBBB.']
EYE_HIT = ['k.......', '.kkkk...', 'kEEEkkkk', '.kkkkEk.']
EYE_ATK = ['kkkk....', 'kwwYYkYk', 'kYYEEkEk', '.kkkkkk.']

# ---- ずきんの 布（赤い 結び布）：後ろへ なびく ----
def scarf(ph=0):
    g = G(17, 11)
    if ph: thick(g, [(16, 3), (11, 2), (6, 4), (1, 2)], 'r', 2); thick(g, [(16, 5), (11, 7), (6, 6), (1, 9)], 'r', 2)
    else: thick(g, [(16, 3), (11, 1), (6, 3), (1, 1)], 'r', 2); thick(g, [(16, 5), (11, 6), (6, 8), (1, 7)], 'r', 2)
    shade(g, SK, dk=1)
    return done(g)

# ---- 手（見せ所）：4本の 指先の 吸盤が 手裏剣の 刃に なる ----
import math
def hand(spin=0, star=True):
    g = G(23, 23); c = 11
    thick(g, [(0, 10), (8, 10)], 'g', 4); ell(g, 8, 11.5, 3.5, 4.5, 'g')        # 手首と てのひら
    a0 = 0 if spin else math.pi / 4
    pts = []
    for i in range(8):
        r = 11.5 if i % 2 == 0 else 3.8
        a = a0 + i * math.pi / 4
        pts.append((c + .5 + r * math.cos(a), c + .5 + r * math.sin(a)))
    if star: pl(g, pts, 's')                                          # 大きな 手裏剣（見せ所）
    edge(g, 's')
    thick(g, [(8, 9), (9, 4)], 'g', 2); thick(g, [(8, 13), (9, 18)], 'g', 2)      # 上と 下の 指で はさむ
    for cx, cy in ((10, 3.5), (10, 19.5)): ell(g, cx, cy, 2, 2, 'a')               # 指先の 吸盤
    if star: ell(g, 11.5, 11.5, 1.3, 1.3, 'o')                                              # 手裏剣の 穴
    edge(g, 'a')
    shade(g, SK, dk=1)
    at(g, 7, 12, 'C'); at(g, 6, 13, 'CC')
    g = [['k' if c == 'o' else c for c in r] for r in g]
    return done(g)
def arm():
    g = G(12, 7)
    thick(g, [(0, 1), (11, 2)], 'g', 4)
    shade(g, SK, dk=1)
    return done(g, open_left=2)

# ---- 投げた 手裏剣（エフェクト：はなれて いるのは 意図的）----
SLASH = ['.....kk..', '...kkwk..', '..kSwk...', '.kSwk....', '.kSk.....', 'kSwk.....', 'kSwk.....', '.kSk.....', '.kSwk....', '..kSwk...', '...kkwk..', '.....kk..']
STAR = ['....k....', '...kSk...', '...kTk...', '.kkkTkkk.', 'kSTTkTTSk', '.kkkTkkk.', '...kTk...', '...kSk...', '....k....']
STAR2 = ['k.......k', '.kSk.kSk.', '.kTTkTTk.', '..kTkTk..', '...kkk...', '..kTkTk..', '.kTTkTTk.', '.kSk.kSk.', 'k.......k']

def thrown():
    g = G(15, 15); pts = []
    for i in range(8):
        r = 7.5 if i % 2 == 0 else 2.6; a = i * math.pi / 4 + .3
        pts.append((7.5 + r * math.cos(a), 7.5 + r * math.sin(a)))
    pl(g, pts, 's'); shade(g, SK, dk=1); g[7][7] = 'k'
    return done(g)
NB = 'atk1|atk2'
H0 = head()
def layers():
    return [
        dict(n='scarf', g='scarf', x=11, y=17, rows=scarf(), alt={'idle1|idle3|walk1|walk3|atk1|atk2|hit': scarf(1)}),
        dict(n='tail', g='tail', x=3, y=42, rows=tail()),
        dict(n='legF', g='legB', x=17, y=51, rows=dark(leg())),
        dict(n='armF', g='armB', x=20, y=38, rows=dark(arm())),
        dict(n='body', g='body', x=17, y=31, rows=body()),
        dict(n='leg', g='legA', x=27, y=51, rows=leg()),
        dict(n='head', g='head', x=26, y=15, rows=H0,
             alt={'blink': head(eye=EYE_BLINK), 'hit': head(eye=EYE_HIT), 'atk0': head(eye=EYE_ATK), NB: head(eye=EYE_ATK, mouth=1), 'ko': head(ko=True)}),
        dict(n='arm', g='armA', x=31, y=39, rows=arm()),
        dict(n='hand', g='armA', x=39, y=31, rows=hand(), alt={'atk0|atk1': hand(1), 'atk2': hand(0, False)}),
        dict(n='slash', g='fx', x=59, y=30, rows=pix.flip_h(SLASH), only='atk1'),
        dict(n='star', g='fx', x=58, y=33, rows=thrown(), only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'armA': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1), 'armA': (0, 0)}, 'idle3': {'body': (0, 1), 'armA': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'tail': (0, 1)}, 'walk1': {'body': (0, -1), 'tail': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'tail': (0, 1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'armA': (-3, -2), 'armB': (-1, 0), 'tail': (-1, 0)},
    'atk1': {'root': (3, 0), 'armA': (3, 1)}, 'atk2': {'root': (4, 0), 'armA': (4, 1), 'fx': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'armA': (-2, -1), 'scarf': (1, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'scarf': 'head', 'armA': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
