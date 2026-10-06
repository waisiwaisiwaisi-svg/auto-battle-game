# ヨイマント（あく・ゴースト × コウモリの 魔物）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく 描きなおし、胴は 小さく 丸く。翼の マントは 大きい まま）
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

META = dict(id='yoimanto', name='ヨイマント', types=['dark', 'ghost'], base='コウモリの 魔物', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1238',
    'R': '#8e78b4', 'Q': '#4e3c76', 'P': '#2c2048',      # 毛と マントの 外がわ
    'C': '#e84a6c', 'D': '#9c2246', 'E': '#581634',      # マントの 内がわ（深紅）
    'g': '#c4fff2', 'G': '#44dac6', 'h': '#1e8a96',      # 霊火
    'w': '#ffffff', 's': '#c2b8d6',                      # 白目と その 影
}
LIGHT = set('RCgw')
EYE_BOX = (37, 12, 9, 6)   # 目（idle0 の 64x64 座標）
RAMP = {'1': 'RQP', '2': 'CDE', '3': 'gGh', '6': 'QPP'}

# ---------- 下書き用の 小道具 ----------
def G(): return grid(64, 64)
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def put(g, x, y, rows): stamp(g, rows, x, y)
def stroke(g, x0, y0, x1, y1, r0, r1, ch, tipch=None, tipt=.8):
    """先が 細くなる 筆（羽の あたり用）"""
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n * 2 + 1):
        t = i / (n * 2); cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t; r = r0 + (r1 - r0) * t
        for y in range(int(cy - r - 2), int(cy + r + 3)):
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + .3 and 0 <= y < len(g) and 0 <= x < len(g[0]):
                    g[y][x] = tipch if (tipch and t >= tipt) else ch
def ink(g, p):
    """p（下書きの 1パーツ）を 黒の ふちごと g に 重ねる。下の パーツとの さかいに 線が できる"""
    H, W = len(p), len(p[0])
    for y in range(H):
        for x in range(W):
            if p[y][x] != '.': continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and p[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): g[y][x] = 'k'
    for y in range(H):
        for x in range(W):
            if p[y][x] != '.': g[y][x] = p[y][x]
def shade(g, ramps=RAMP, dk=1.0):
    """光は 左上：上と 左の ふちに 三日月の 明、右下に 影（ふち＝空白か 黒線）"""
    H, W = len(g), len(g[0])
    def e(y, x): return not (0 <= y < H and 0 <= x < W) or g[y][x] in '.k'
    def run(y, x, dy, dx, lim):
        n = 1
        while n <= lim and not e(y + dy * n, x + dx * n): n += 1
        return n
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c not in ramps: continue
            hi, md, lo = ramps[c]
            up, lf, ul = run(y, x, -1, 0, 3), run(y, x, 0, -1, 3), run(y, x, -1, -1, 3)
            dn, rt, dr = run(y, x, 1, 0, 4), run(y, x, 0, 1, 4), run(y, x, 1, 1, 4)
            L = 3 * (up == 1) + 2 * (lf == 1) + (ul == 1) + 1.5 * (up == 2) + .8 * (ul == 2)
            D = 3 * (dn == 1) + 2.5 * (rt == 1) + (dr == 1) + 1.5 * (dn == 2) + 1.2 * (rt == 2) + .8 * (dr == 2) + .5 * (dn == 3)
            D *= dk
            out[y][x] = md if L == D else hi if L > D else lo
    return out
def recolor(g, m): return [[m.get(c, c) for c in r] for r in g]
INNER = {'R': 'C', 'Q': 'D', 'P': 'E'}
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'C': 'D', 'D': 'E', 'E': 'l'}

# ---------- 霊火（マントの すその 先で ゆらぐ）----------
FL = [outline(['hGh', 'gGG', '.gG', '.g.', '..g']), outline(['hGh', 'GGg', 'Gg.', '.g.', 'g..'])]
def flame(g, x, y, v):
    f = FL[v]
    for j, r in enumerate(f):
        for i, c in enumerate(r):
            X, Y = x - 2 + i, y - 1 + j
            if c != '.' and 0 <= Y < 64 and 0 <= X < 64 and (g[Y][X] in '.k' or c != 'k'): g[Y][X] = c

# ---------- 翼（マントの ような コウモリの 翼。すそは ぼろぼろで 霊火に とける）----------
WP = {
    'up':   dict(s=(34, 27), w=(24, 12), tips=[(22, 0), (10, 3), (3, 12), (4, 25)], end=(26, 40)),
    'mid':  dict(s=(34, 27), w=(21, 21), tips=[(11, 7), (2, 14), (0, 27), (6, 40)], end=(28, 46)),
    'down': dict(s=(34, 27), w=(25, 33), tips=[(13, 23), (4, 34), (6, 47), (16, 55)], end=(30, 52)),
}
def wing(pose, far=False, inner=False, v=0):
    P = WP[pose]; (sx, sy), (wx, wy) = P['s'], P['w']; T = P['tips']
    g = G()
    # 膜：指の 先を むすぶ ふちを 手首がわへ えぐる（ぼろぼろの すそ）
    edge = [T[0]]
    for (ax, ay), (bx, by) in zip(T + [P['end']], T[1:] + [P['end']]):
        mx, my = (ax + bx) / 2, (ay + by) / 2
        edge += [(round(mx + (wx - mx) * .42), round(my + (wy - my) * .42)), (bx, by)]
    p = G(); poly(p, [(sx + 1, sy - 2), (wx, wy)] + edge + [(sx + 2, sy + 10)], '1'); ink(g, p)
    g = shade(g, dk=.8)
    def segd(px, py, A, B):
        (x0, y0), (x1, y1) = A, B; vx, vy = x1 - x0, y1 - y0; L = vx * vx + vy * vy or 1
        t = max(0, min(1, ((px - x0) * vx + (py - y0) * vy) / L)); return ((px - x0 - vx * t) ** 2 + (py - y0 - vy * t) ** 2) ** .5
    segs = [((sx, sy), (wx, wy))] + [((wx, wy), t) for t in T]
    # 膜：骨の そばは 中間色、骨から はなれた すそは 影（境は 市松）
    for y in range(64):
        for x in range(64):
            if g[y][x] not in 'QP': continue
            d = min(segd(x, y, A, B) for A, B in segs)
            ck = (x + y) % 2 == 0
            g[y][x] = 'Q' if d < 2.5 or (d < 4 and ck) else 'P'
    # 骨：黒線なしの 明るい すじ（上が 明、下が 中間）
    for (A, B), r in zip(segs, [1] + [0] * len(T)):
        (x0, y0), (x1, y1) = A, B; n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
            if g[y][x] != '.':
                g[y][x] = 'R'
                if r and y + 1 < 64 and g[y + 1][x] != '.': g[y + 1][x] = 'R'
                if y + 1 + r < 64 and g[y + 1 + r][x] in 'QP': g[y + 1 + r][x] = 'Q'
    # 手首の かぎ爪
    put(g, wx - 1, wy - 3, ['.k.', 'kwk', 'kRk'])
    if inner: g = recolor(g, INNER)
    if far: g = recolor(g, DARK)
    for i, (tx, ty) in enumerate(T + [P['end']]):
        flame(g, tx, ty + 1, (i + v) % 2)
    return rows_of(g)

def cape():
    """ため：マントで 体を つつむ"""
    g = G()
    Y = lambda y: round(23 + (y - 23) * .66)
    p = G(); poly(p, [(x, Y(y)) for x, y in [(31, 23), (42, 24), (47, 31), (48, 42), (45, 52), (40, 50), (36, 54), (32, 50), (27, 52), (26, 40), (28, 29)]], '1'); ink(g, p)
    g = shade(g, dk=.8)
    for x0, y0, y1 in ((33, 27, 41), (38, 26, 40), (43, 27, 41)):     # ひだ（骨）
        for y in range(y0, y1):
            if g[y][x0] in 'RQP': g[y][x0] = 'P'
            if g[y][x0 - 1] in 'Q': g[y][x0 - 1] = 'R'
    for i, (x, y) in enumerate([(27, 43), (36, 45), (45, 43)]): flame(g, x, y, i % 2)
    return rows_of(g)

# ---------- 胴と 足 ----------
def body():
    g = G()
    p = G(); ellipse(p, 39, 32, 7, 7.5, '1'); ink(g, p)
    g = shade(g)
    # 胸の 毛（明るい ふさ）と 霊火の 紋
    put(g, 38, 27, ['.R.', 'RQR', '.R.'])
    put(g, 40, 31, ['.h.', 'hGh', '.g.'])
    return rows_of(g)
FEET = outline([   # 足：さかさまに ぶら下がる ための かぎ爪（根もとは 胴に 食いこむ）
    'QP...QP.',
    'QP...QP.',
    'QP...QP.',
    'PwP..PwP',
    'w.w..w.w',
])

# ---------- 頭（大きな 耳、霊火の 目、牙）----------
HEAD = [   # 手打ち：大きな 頭（たて 16）、しかめた 顔、深紅の 鼻、長い 牙
    '.....kkkkkkkkkk.......',
    '...kkRRRRRRRRRRkk.....',
    '..kRRRQQQQQQQQQRRk....',
    '.kRRQQQQQQQQQQQQQRk...',
    'kRQQQQQQQQQQQQQQQQRk..',
    'kRQQQQQQQQQQQQQQQQQRk.',
    'kQQQQQQQQQQQQQQQQQQQRk',
    'kQQQQQQQQQQQQQQQQQkkDk',
    'kQQQQQQQQQQQQQQQQkCDDk',
    'kQQQQQQQQQQQQQQQQQkkk.',
    'kPQQQQQQQQkkkkkkkkkk..',
    'kPQQQQQQQkwkQQQQQkwk..',
    '.kPQQQQQQkwkPPPPPkwk..',
    '..kPQQQQQQkkkkkkkkk...',
    '...kPPPPPPPPkk........',
    '....kkkkkkkk..........',
]
def head():
    g = G()
    for (bx, by, tx, ty) in [(34, 13, 27, 0), (45, 12, 49, 0)]:
        p = G(); stroke(p, bx, by, tx, ty, 3.6, .5, '1'); ink(g, p)
    # 耳の あいだの とがった 毛
    for (bx, by, tx, ty) in [(39, 11, 37, 5), (42, 11, 42, 5)]:
        p = G(); stroke(p, bx, by, tx, ty, 1.5, .5, '1'); ink(g, p)
    g = shade(g)
    for (x0, y0, x1, y1) in [(32, 10, 28, 3), (46, 8, 48, 3)]:
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
            if g[y][x] in 'RQP': g[y][x] = 'D' if i < n - 1 else 'C'
    put(g, 30, 9, HEAD)
    return rows_of(g)
# 目（C：三白眼）：太い まゆの 下、白目（w／影 s）が 大きく、小さな 赤い 瞳（C／D／芯 E）が 上の 前に 寄って にらむ。下まぶたの 線は 太く 濃い
EYE = ['kkkk.....', '.kkkkkkk.', '.kwwwwCDk', '.kswwwDEk', '..kkkkkkk', '...PPPPP.']
EYE_ALT = {
    'blink': ['kkkk.....', '.kkkkkkk.', '.kQQQQQQk', '.kkkkkkkk', '..PPPPPP.', '.........'],
    'atk0|atk1|atk2': ['kkkk.....', '.kkkkkkkk', '.kwwwwCDk', '.kwwwwDEk', '.kswwwwwk', '..kkkkkkk'],
    'hit': ['.........', 'kkkkkkkk.', '.Rkk.kkR.', '..RkkkR..', '.kkR.Rkk.', '.........'],
    'ko': ['.........', '.kR..kR..', '..kRkR...', '...kR....', '..kRkR...', '.kR..kR..'],
}
MOUTH = [   # 攻撃：大きく 開く 口
    'kkkkkkkk.',
    'kwkkkkwk.',
    'kwEDDDwk.',
    'kEDCCDDk.',
    'kEDDDDk..',
    '.kwkkwk..',
    '..kkkk...',
]
FIRE_A = [['.g.', 'gGg', 'Ghk']]

# ---------- 霊火の さけび（攻撃）----------
SHRIEK = [
    '.g.......gg....',
    '..G........G...',
    '...G........G..',
    '...GG.......Gh.',
    '....G........Gh',
    '....G........Gh',
    '....G........Gh',
    '...GG.......Gh.',
    '...G........G..',
    '..G........G...',
    '.g.......gg....',
]
WISP = outline(['.g..', 'gGg.', 'GhGg', '.hh.'])
SMALL = outline(['.g.', 'gGh', '.h.'])

def layers():
    W = {(p, v): wing(p, v=v) for p in WP for v in (0, 1)}
    WI = wing('up', inner=True)
    WF = {p: wing(p, False, True) for p in WP}
    return [
        dict(n='wingB', g='wingB', x=5, y=-3, rows=WF['up'], alt={'walk0|atk1|hit': WF['up'], 'walk2|atk0': WF['mid'], 'walk1|walk3|atk2': WF['mid']}),
        dict(n='feet', g='body', x=35, y=37, rows=FEET),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='mouth', g='head', x=40, y=19, rows=MOUTH, only='atk1|atk2|hit'),
        dict(n='eye', g='head', x=37, y=12, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W[('mid', 0)], alt={'idle1|idle3': W[('mid', 1)], 'walk0|hit': W[('up', 0)], 'walk2': W[('down', 1)], 'walk1|walk3|atk2': W[('mid', 1)], 'atk1': WI}, not_='atk0'),
        dict(n='cape', g='wingF', x=0, y=0, rows=cape(), only='atk0'),
        dict(n='shriek', g='root', x=50, y=9, rows=outline(SHRIEK), only='atk1'),
        dict(n='wisp', g='root', x=56, y=24, rows=WISP, only='atk1|atk2'),
        dict(n='wisp2', g='root', x=60, y=14, rows=SMALL, only='atk2'),
        dict(n='shriek2', g='root', x=54, y=9, rows=outline(SHRIEK[:]), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {'body': (0, -1), 'head': (0, 1)},
    'idle3': {'body': (0, 0)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 1), 'head': (0, 1)},
    'atk1': {'root': (3, -2), 'head': (1, 0)},
    'atk2': {'root': (4, -1), 'head': (1, 0)},
    'hit': {'root': (-4, -1), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root'}
