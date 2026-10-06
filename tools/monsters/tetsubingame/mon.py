# テツビンガメ（はがね・ほのお × カメ）手打ち GBA風・デフォルメ（2〜3頭身）
META = dict(id='tetsubingame', name='テツビンガメ', types=['steel', 'fire'], base='カメ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1c1e',
    'I': '#aab2c8', 'J': '#6a7088', 'K': '#3a3e50',
    'Y': '#ffe46a', 'O': '#ff8a28', 'R': '#c8361c',
    'F': '#e6b070', 'G': '#b06a3c', 'H': '#62321e',
    'S': '#eef2f6', 'T': '#a6aec0',
    'w': '#ffffff',
}
LIGHT = set('IYFSw')
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
RAMP = {'i': 'IJK', 'f': 'FGH', 'r': 'YOR', 's': 'SST'}
DARKER = {'I': 'J', 'J': 'K', 'K': 'l', 'F': 'G', 'G': 'H', 'H': 'l', 'w': 'G'}
def dark(rows): return recolor(rows, DARKER)


# ---- 甲羅＝鉄瓶（見せ所）：あられ もようの 丸い 鉄の 器、ふた・つまみ・つる（とって）----
def shell(hot=False):
    W, H = 32, 33; g = G(W, H)
    thick(g, [(4, 17), (4, 10), (7, 5), (12, 2), (17, 1), (22, 2), (26, 5), (28, 10), (28, 17)], 'h', 2)   # つる
    ell(g, 16, 31, 15.5, 19, 'i')                                   # 器
    for y in range(29, H):
        for x in range(W): g[y][x] = '.' if g[y][x] == '.' else 'i'
    for y in range(28, 31):                                         # 底の ふち：熱で 赤く 光る
        for x in range(W):
            if g[y][x] == 'i': g[y][x] = 'r'
    ell(g, 16, 13.5, 8, 2.6, 'j')                                   # ふた
    ell(g, 16, 11, 2, 1.5, 'n')                                     # つまみ
    edge(g, 'j'); edge(g, 'n'); edge(g, 'r'); edge(g, 'h')
    shade(g, {'i': 'IJK', 'h': 'IJK', 'j': 'IIJ', 'n': 'IJK', 'r': 'YOR' if hot else 'OOR'}, hl=1, dk=3, dr=2)
    # あられ（鉄の つぶ）：手で 置く。光の 側は 明るく、右下は 影
    for y in range(17, 28, 3):
        for x in range(3 + (y // 3) % 2 * 2, 30, 4):
            if g[y][x] in 'IJ' and g[y + 1][x + 1] in 'IJK':
                g[y][x] = 'I'; g[y + 1][x + 1] = 'K'
    for x in range(2, 31, 3):                                      # ふちの 刻み
        if g[29][x] in 'YOR': g[29][x] = 'R'
    if hot: at(g, 9, 29, 'Y'); at(g, 21, 29, 'Y')
    return done(g)

# ---- 首＝注ぎ口：鉄の 筒が 前へ 上がり、その 先から 首が 出る ----
def spout():
    g = G(14, 12)
    pl(g, [(0, 4), (8, 1), (13, 0), (13, 6), (8, 7), (0, 11)], 'i')
    edge(g, 'i')
    shade(g, RAMP, dk=2, dr=1)
    at(g, 11, 0, 'k'); at(g, 11, 1, 'I'); at(g, 11, 2, 'I'); at(g, 11, 3, 'J'); at(g, 11, 4, 'J'); at(g, 11, 5, 'K')   # 口の 輪
    return done(g, open_left=2)

# ---- 頭：大きく、かぎ形の くちばし（ワニガメ風）、するどい 目 ----
def head(eye=None, mouth=0, ko=False):
    g = G(21, 18)
    ell(g, 9, 9, 8.5, 7.5, 'f')
    pl(g, [(10, 3), (17, 4), (20, 8), (19, 12), (16, 10), (10, 12)], 'f')          # 鼻先
    if mouth: pl(g, [(10, 12), (17, 11), (19, 16), (12, 16), (6, 15)], 'f')
    pl(g, [(13, 4), (17, 4), (20, 8), (19, 12), (17, 10), (13, 9)], 'i')          # 鉄の くちばし（注ぎ口の 先と 同じ 鉄）
    pl(g, [(2, 4), (7, 0), (8, 4)], 'f')                                            # 後ろへ 反る 頭の とげ
    edge(g, 'i')
    shade(g, RAMP, hl=1, dk=3, dr=1)
    at(g, 4, 10, 'O'); at(g, 5, 11, 'R'); at(g, 3, 6, 'G'); at(g, 4, 8, 'GH'); at(g, 2, 11, 'H')         # うろこ
    at(g, 18, 6, 'k')                                               # 鼻の あな
    if mouth:
        at(g, 9, 11, 'kkkkkkkkkkk', '.kRRRRRRRkk', '.kROOOORRk.', '.kRRRRRk...', '.kkkkkkk...')
        at(g, 17, 11, 'kw'); at(g, 10, 12, 'w'); at(g, 14, 12, 'w')
    else:
        at(g, 8, 12, 'kkkkkkkkkkkk'); at(g, 18, 12, 'w'); at(g, 18, 13, 'k')   # かぎ形の くちばしの 先
        at(g, 7, 11, 'k')
    if ko: e = ['k...k', '.k.k.', '..k..', '.k.k.', 'k...k']
    else: e = eye or ['kkk.....', '.kkkkkk.', 'kwYYOkk.', 'kYOOkRk.', '.kkkkk..']
    at(g, 7, 3, *e)
    return done(g)
EYE_BLINK = ['kkk.....', '.kkkkkk.', 'kGGGGGk.', 'kkkkkkk.', '.HHHHH..']
EYE_HIT = ['k.......', '.kkk....', 'kOOkkkk.', '.kkkkOk.', '........']
EYE_ATK = ['kkk.....', '.kkkkkk.', 'kwwYYkk.', 'kYYOkOk.', '.kkkkk..']

# ---- 足：短く 太い 四つ足、白い つめ ----
LEG_M = ['.ffffff.', 'ffffffff', 'ffffffff', 'ffffffff', 'ffffffff', '.fffffff', '.fffffff', '.ffffffff', 'fffffffff']
def leg():
    g = pix.grid_of(LEG_M); shade(g, RAMP, dk=1)
    at(g, 2, 3, 'G'); at(g, 5, 2, 'G')
    r = done(g, open_top=2)
    r[-1] = r[-1][:5] + 'kwkwk' + r[-1][10:]
    return r
TAIL = ['....kk', '..kkGHk', 'kkFGHk.', 'kGGkk..', '.kk....']

# ---- 湯気と 炎の 息（エフェクト：はなれて いるのは 意図的）----
def breath(big=False):
    w, h = (22, 14) if big else (14, 10)
    g = G(w, h)
    for cx, cy, r, m in ([(4, 7, 3.6, 'r'), (9, 6, 4.2, 's'), (14, 8, 4, 's'), (18, 6, 3.4, 's')] if big else [(3, 5, 3, 'r'), (8, 4, 3.5, 's'), (11, 6, 2.6, 's')]):
        ell(g, cx, cy, r, r * .85, m)
    shade(g, RAMP, hl=2, dk=2, dr=2)
    return done(g)
WISP = ['..kkk..', '.kSSTk.', 'kSSTk..', '.kTk....', '..kSk..', '...kTk.', '...kk..']
WISP2 = ['.kkk...', 'kSSTk..', '.kSSTk.', '..kTk..', '.kSk...', 'kTk....', '.kk....']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='wisp', g='lid', x=19, y=11, rows=WISP, alt={'idle1|idle3|walk1|walk3': WISP2}, not_='ko|hit|' + NB),
        dict(n='tail', g='body', x=3, y=47, rows=TAIL),
        dict(n='legHF', g='legB', x=12, y=48, rows=dark(leg())),
        dict(n='legFF', g='legB', x=31, y=48, rows=dark(leg())),
        dict(n='spout', g='neck', x=31, y=34, rows=spout()),
        dict(n='shell', g='body', x=5, y=19, rows=shell(), alt={'idle1|idle3|walk1|walk3|atk0|' + NB: shell(True)}),
        dict(n='legH', g='legA', x=8, y=49, rows=leg()),
        dict(n='legF', g='legA', x=27, y=49, rows=leg()),
        dict(n='head', g='head', x=41, y=23, rows=head(),
             alt={'blink': head(EYE_BLINK), 'hit': head(EYE_HIT), 'atk0': head(EYE_ATK), NB: head(EYE_ATK, 1), 'ko': head(ko=True)}),
        dict(n='breath', g='fx', x=60, y=34, rows=breath(), alt={'atk2': breath(True)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'body': (0, 1), 'neck': (0, 1), 'head': (0, 1)}, 'idle3': {'body': (0, 1), 'neck': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'neck': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'neck': (0, -1), 'head': (0, 1)},
    'atk0': {'neck': (-2, 1), 'head': (-4, 2)}, 'atk1': {'root': (2, 0), 'neck': (1, 0), 'head': (2, 0)}, 'atk2': {'root': (3, 0), 'neck': (1, 0), 'head': (2, 0), 'fx': (2, 0)},
    'hit': {'root': (-3, 0), 'neck': (-1, 1), 'head': (-3, 2)},
    'ko': {'_flip': True},
}
PARENT = {'lid': 'body', 'head': 'neck', 'neck': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
