# チョウリュウ（フェアリー・ドラゴン × 蝶の 竜）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく、胴は 短く 太く、翅は 大きい まま）
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline

META = dict(id='choryu', name='チョウリュウ', types=['fairy', 'dragon'], base='蝶の 竜', size='L')
PAL = {
    'k': '#101018', 'l': '#2c1030',
    'A': '#e278b4', 'B': '#a03c80', 'D': '#5a1c52',      # うろこ（こい 赤むらさき）
    'E': '#f2d6dc', 'F': '#b88ca4',                      # 腹の 板（うすい 骨色）
    'X': '#a6ecff', 'W': '#3c8ee6', 'Z': '#1c3784',      # 蝶の 翅（青の ステンドグラス）
    'Y': '#ffd23a', 'y': '#c87818', 'r': '#e8304a',                      # 目・翅の 目玉もよう
    'w': '#ffffff', 'U': '#efe4d2', 'V': '#a49280',      # 牙・つの（骨）
}
LIGHT = set('AEXYwU')
KEEP_BLACK = set('Yyr')

# ---------- 下書きの 道具 ----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def ink(g, p):
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.7 + (B(x, y + 1) - B(x, y - 1)) * 2.4 for y in range(64) for x in range(64) if m[y][x]}
def shade(p, ramps, r=2, hi=.32, lo=-.28):
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def tube(p, path, rad, belly=None, ch='1'):
    """道すじに そって 丸い 管。belly：進む 向きの 右がわ（＝下がわ）を 腹の 板に"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) or 1; nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        n = int(L * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    dx, dy = x + .5 - cx, y + .5 - cy
                    if dx * dx + dy * dy <= r * r and 0 <= x < 64 and 0 <= y < 64:
                        b = belly is not None and (dx * nx + dy * ny) < -r * belly
                        if p[y][x] == '.' or (p[y][x] == '2' and not b): p[y][x] = '2' if b else ch
DARK = {'A': 'B', 'B': 'D', 'D': 'l', 'E': 'F', 'F': 'D', 'X': 'W', 'W': 'Z', 'Z': 'l', 'U': 'V', 'w': 'U', 'Y': 'r'}
def dark(g): return [[DARK.get(c, c) for c in r] for r in g]

# ---------- 蝶の 翅：つけねは 濃い 青、外へ 明るく。黒い 翅脈、ふちは 黒に 水色の 点 ----------
FORE = {
    'up':   [(37, 28), (33, 17), (29, 8), (24, 2), (16, 1), (10, 5), (12, 13), (20, 22), (31, 30)],
    'mid':  [(37, 28), (30, 19), (22, 12), (14, 9), (7, 12), (6, 19), (13, 25), (31, 31)],
    'down': [(37, 29), (28, 26), (18, 25), (9, 26), (4, 31), (9, 35), (24, 36), (34, 33)],
}
HIND = {   # 後翅：目玉もようと 長い 燕尾
    'up':   [(35, 31), (25, 26), (15, 25), (9, 29), (10, 35), (5, 41), (14, 38), (26, 36), (33, 34)],
    'mid':  [(35, 32), (25, 30), (15, 31), (10, 36), (12, 41), (7, 47), (16, 43), (27, 38), (33, 35)],
    'down': [(35, 33), (24, 35), (14, 37), (7, 41), (8, 46), (3, 52), (13, 48), (25, 42), (33, 37)],
}
def wingpart(pts, veins, spot=None):
    p = G(); poly(p, pts, '2'); bx, by = pts[0]
    cells = [(x, y) for y in range(64) for x in range(64) if p[y][x] == '2']
    far = max(math.hypot(x - bx, y - by) for x, y in cells)
    g = G()
    for x, y in cells:
        d = math.hypot(x - bx, y - by) / far; ck = (x + y) % 2 == 0
        g[y][x] = 'Z' if d < .3 or (d < .36 and ck) else 'W' if d < .62 or (d < .68 and ck) else 'X'
    # 外の ふち：黒い 帯に 水色の 点（2ドット）
    for x, y in cells:
        edge = min((math.hypot(x - ex, y - ey) for ex, ey in [(a, b) for (a, b) in [(xx, yy) for yy in range(max(0, y - 2), min(64, y + 3)) for xx in range(max(0, x - 2), min(64, x + 3))] if p[b][a] == '.']), default=9)
        if edge <= 1.5 and math.hypot(x - bx, y - by) / far > .45:
            g[y][x] = 'X' if (x * 3 + y * 2) % 7 == 0 else 'l'
    # 翅脈：つけねから ふちの 点へ（黒）
    for (ex, ey) in veins:
        n = max(abs(ex - bx), abs(ey - by))
        for i in range(3, n):
            x, y = round(bx + (ex - bx) * i / n), round(by + (ey - by) * i / n)
            if g[y][x] in 'XWZ': g[y][x] = 'l'
    if spot:   # 目玉もよう（にらむ 赤い 目）
        sx, sy = spot
        stamp(g, ['.lll.', 'lrrrl', 'lrYkl', 'lrrrl', '.lll.'], sx - 2, sy - 2)
    o = G(); ink(o, g); return o
def wing(pose, far=False):
    fp, hp = FORE[pose], HIND[pose]
    g = wingpart(hp, hp[2:6:1], spot=((hp[1][0] + hp[3][0]) // 2 + 1, (hp[1][1] + hp[3][1]) // 2 + 3))
    f = wingpart(fp, fp[2:6])
    for y in range(64):
        for x in range(64):
            if f[y][x] != '.': g[y][x] = f[y][x]
    if far: g = dark(g)
    return rows_of(g)
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < 64 and 0 <= y + dy < 64: g[y + dy][x + dx] = c
    return rows_of(g)

# ---------- 体：S字に くねる ヘビの ような 竜（デフォルメ：短く 太く）。腹は 骨色の 板 ----------
PATH = [(47, 27), (45, 32), (41, 37), (35, 41), (28, 43), (21, 45), (15, 48), (12, 52), (12, 56), (16, 59)]
RAD = [5.2, 5.6, 6.0, 5.8, 5.2, 4.4, 3.5, 2.6, 1.8, 1.0]
def along(t):
    """道すじの 長さ t（0〜1）の 点と 向き"""
    segs = [(PATH[i], PATH[i + 1]) for i in range(len(PATH) - 1)]
    Ls = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; d = t * sum(Ls)
    for (a, b), L in zip(segs, Ls):
        if d <= L or (a, b) == segs[-1]:
            u = min(1, d / L); return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        d -= L
def body():
    p = G(); tube(p, PATH, RAD, belly=.45)
    s = shade(p, {'1': 'ABD', '2': 'EEF'}, r=2)
    # 腹の 板の 区切り（ななめの 線を 手で）
    for t in (.08, .17, .26, .35, .44, .53, .62):
        (cx, cy), (dx, dy) = along(t)
        for k in range(1, 7):
            x, y = round(cx + dy * k * .9), round(cy - dx * k * .9)
            if 0 <= y < 64 and 0 <= x < 64 and s[y][x] == 'E': s[y][x] = 'F'
    # 背の うろこ（山形の 光と 影）
    for t in (.2, .3, .4, .5, .6, .7):
        (cx, cy), (dx, dy) = along(t); r = 2
        x, y = round(cx - dy * r), round(cy + dx * r)
        if s[y][x] in 'AB': s[y][x] = 'D'
        if s[y - 1][x - 1] in 'AB': s[y - 1][x - 1] = 'A'
    g = G(); ink(g, s)
    # 背の とげ（骨色、後ろへ 向く）：根もとは うろこに 食いこむ
    for t in (.14, .26, .38, .5, .62):
        (cx, cy), (dx, dy) = along(t); r = RAD[min(len(RAD) - 1, int(t * (len(RAD) - 1)))]
        x, y = round(cx - dy * (r - .5)), round(cy + dx * (r - .5))
        stamp(g, ['kk..', 'kUkk', '.kUVk', '..kVk'], x - 2, y - 2)
    # 尾の 先：花びらの 刃（ひれ）
    stamp(g, ['..kk......', '.kXXkk....', 'kXXWWZkk..', '.kXWWZZZkk', '..kWZZkk..', '...kkk....'], 14, 56)
    return g

# ---------- 頭（デフォルメで 大きく）：くさび形の 竜の 頭、骨の つの、牙 ----------
class Part:
    def __init__(s, pts, fill=None):
        p = G(); poly(p, pts, '1')
        if fill: fill(p)
        s.g = shade(p, {'1': 'ABD', '2': 'EEF'}, r=2)
    def P(s, pts, ch, only=None):
        for x, y in pts:
            if 0 <= y < 64 and 0 <= x < 64 and (only is None or s.g[y][x] in only): s.g[y][x] = ch
    def S(s, x0, y0, rows):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': s.P([(x0 + i, y0 + j)], c)
    def rows(s): o = G(); ink(o, s.g); return rows_of(o)
EYE = ['kwYYkYk', 'kYyykyk', '.kkyykk']
EYE_ALT = {
    'blink': ['BBBBBBB', 'kkkkkkk', '.BBBBBB'],
    'atk0|atk1|atk2': ['kwwYkYk', 'kYYYkYk', '.kkYYkk'],
    'hit': ['BkkBBBB', 'BBBkkkk', 'BkkBBBB'],
    'ko': ['BkBBkBB', 'BBkkBBB', 'BkBBkBB'],
}
def jaw(p, open_):
    """下あご：骨色の 板。開くと 赤い 口の 中と 牙"""
    if open_:
        poly(p, [(50, 27), (63, 24), (62.5, 32), (52, 33), (46, 31)], '2')
        poly(p, [(51, 27.5), (62.5, 25), (62, 30), (52, 30)], 'r')
    else:
        poly(p, [(45, 28), (61, 26.5), (60, 28.5), (52, 30), (46, 30.5)], '2')
def head(open_=False, eye=None):
    h = Part([(38, 23), (41, 18), (45, 15), (50, 14), (54, 16), (58, 18), (62, 20), (63.5, 23), (63, 26), (60, 27.5), (52, 28), (47, 30), (42, 30), (38, 27)], lambda p: jaw(p, open_))
    # まゆの ひさし（黒い 線）と その 上の 光
    h.P([(43, 17), (44, 17), (45, 18), (46, 18), (47, 19), (48, 19), (49, 19), (50, 19), (51, 19), (52, 20), (53, 20), (54, 21)], 'k')
    h.P([(44, 16), (45, 16), (46, 17), (47, 17), (48, 18), (49, 18), (50, 18), (51, 18), (52, 19)], 'A')
    h.P([(55, 18), (56, 18), (57, 19), (58, 19), (59, 20), (60, 20)], 'A')               # 鼻すじの 光
    h.S(46, 20, eye or EYE)
    h.P([(41, 22), (40, 23), (40, 24), (41, 26), (42, 27)], 'D', 'B')                 # ほおの すじ
    h.P([(61, 22), (60, 22)], 'k')                                  # 鼻の あな
    if open_:
        h.P([(53, 28), (56, 27), (59, 26), (62, 25)], 'w'); h.P([(55, 30), (58, 30), (61, 29)], 'w')
        h.P([(52, 27), (53, 27), (54, 27), (55, 26), (56, 26), (57, 26), (58, 25), (59, 25), (60, 25), (61, 24), (62, 24)], 'k', 'Br')
    else:
        h.P([(45, 28), (46, 28), (47, 28), (48, 28), (49, 27), (50, 27), (51, 27), (52, 27), (53, 27), (54, 27), (55, 27), (56, 27), (57, 26), (58, 26), (59, 26), (60, 26), (61, 26)], 'k')
        h.P([(58, 27), (55, 28), (51, 28)], 'w')
    return h.rows()
HEAD = head(); HEAD_OPEN = head(True)
HEAD_EYES = {k: head(eye=v) for k, v in EYE_ALT.items() if 'atk' not in k}
HEAD_EYES['atk0'] = head(eye=EYE_ALT['atk0|atk1|atk2']); HEAD_EYES['atk1|atk2'] = head(True, EYE_ALT['atk0|atk1|atk2'])
HORN = [   # 骨の つの：額から 後ろへ 大きく そる（根もとは 頭に 食いこむ）
    'kk............',
    'kUkk..........',
    '.kUUkk........',
    '..kUUUkk......',
    '...kUUUVkk....',
    '....kkUUVVkk..',
    '......kkUVVVVk',
    '........kVVVVV',
    '.........kVVVV',
]
HORN2 = ['kk.......', 'kVkk.....', '.kVVkk...', '..kkVVkk.', '....kVVVV', '.....kVVV']
# 小さな 前足（胸から 生える。付け根は 胴に もぐる）
CLAW = ['kBBBk.', 'kABBDk', 'kABDDk', '.kBDDk', '.kUkUk', '..k.k.']

# ---------- 鱗粉の ブレス（攻撃）と きらめき ----------
BREATH = [
    '.............X....',
    '........X.......XW',
    '....w.......w....X',
    '..X....XWX.....X..',
    'XXWX..XWwWX...XWwW',
    'WwYwWXXWwYwWXXWwYw',
    'XXWX..XWwWX...XWwW',
    '..X....XWX.....X..',
    '....w.......w....X',
    '........X.......XW',
    '.............X....',
]
BREATH2 = [
    '.....X......w..',
    '..w.....XWX....',
    '......XWwWX...X',
    'X..w...XWX.....',
    '..XWX.......w..',
    '...X...X.......',
    '.w.......XWX...',
    '..........X....',
]
SPARK_A = ['.X...', 'XwX..', '.X..w']
SPARK_B = ['w..X.', '..XwX', '...X.']

WDX, WDY = 2, 3
def layers():
    W = {p: shift(wing(p), WDX, WDY) for p in FORE}; WF = {p: shift(wing(p, True), 5 + WDX, -2 + WDY) for p in FORE}
    BODY = rows_of(body())
    return [
        dict(n='wingB', g='wingB', x=0, y=0, rows=WF['up'], alt={'idle1|idle3|walk1|walk3|atk2|atk1': WF['mid'], 'walk2': WF['down']}),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['up'], alt={'idle1|idle3|walk1|walk3|atk2': W['mid'], 'walk2': W['down']}),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='horn2', g='head', x=36, y=11, rows=HORN2),
        dict(n='claw', g='body', x=44, y=38, rows=CLAW),
        dict(n='head', g='head', x=0, y=0, rows=HEAD, alt=HEAD_EYES),
        dict(n='horn', g='head', x=31, y=8, rows=HORN),
        dict(n='spark', g='root', x=4, y=6, rows=outline(SPARK_A), alt={'idle1|idle3|walk1|walk3': outline(SPARK_B)}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='breath', g='root', x=61, y=19, rows=outline(BREATH), only='atk1'),
        dict(n='breath2', g='root', x=63, y=19, rows=outline(BREATH2), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'head': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'head': (-3, -2)},
    'atk1': {'root': (1, 0), 'head': (2, 1)},
    'atk2': {'root': (2, 0), 'head': (2, 1)},
    'hit': {'root': (-4, -1), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root'}
