# チョウリュウ（フェアリー・ドラゴン × 蝶の 竜）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline

META = dict(id='choryu', name='チョウリュウ', types=['fairy', 'dragon'], base='蝶の 竜', size='L')
PAL = {
    'k': '#101018', 'l': '#2c1030',
    'A': '#e278b4', 'B': '#a03c80', 'D': '#5a1c52',      # うろこ（こい 赤むらさき）
    'E': '#f2d6dc', 'F': '#b88ca4',                      # 腹の 板（うすい 骨色）
    'X': '#a6ecff', 'W': '#3c8ee6', 'Z': '#1c3784',      # 蝶の 翅（青の ステンドグラス）
    'Y': '#ffd23a', 'r': '#e8304a',                      # 目・翅の 目玉もよう
    'w': '#ffffff', 'U': '#efe4d2', 'V': '#a49280',      # 牙・つの（骨）
}
LIGHT = set('AEXYwU')
KEEP_BLACK = set('Yr')

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

# ---------- 体：S字に くねる ヘビの ような 竜。腹は 細い 骨色の 板 ----------
PATH = [(47, 19), (45, 25), (42, 31), (37, 37), (30, 41), (22, 43), (15, 45), (10, 50), (9, 55), (13, 58)]
RAD = [3.8, 4.3, 5.0, 5.3, 5.0, 4.4, 3.5, 2.6, 1.8, 1.0]
def body():
    p = G(); tube(p, PATH, RAD, belly=.45)
    s = shade(p, {'1': 'ABD', '2': 'EEF'}, r=2)
    # 腹の 板の 区切り（手で）
    for (x, y) in [(46, 24), (44, 29), (41, 34), (37, 39), (32, 43), (27, 45), (21, 46), (16, 48)]:
        for dy in range(-2, 3):
            for dx in range(-1, 2):
                if s[y + dy][x + dx] == 'E' and (dx + dy) == 0: s[y + dy][x + dx] = 'F'
    # 背の うろこの 光と 暗い うろこ（山形）
    dots(s, 'A', [(34, 36), (27, 39), (20, 41), (14, 43)])
    dots(s, 'D', [(31, 39), (24, 41), (17, 43), (38, 34), (12, 47)])
    g = G(); ink(g, s)
    # 背の とげ（骨色、後ろへ 向く）
    for (x, y) in [(41, 27), (36, 32), (30, 36), (23, 38), (16, 40)]:
        stamp(g, ['kk..', 'kUkk', '.kVk', '..k.'], x - 2, y - 2)
    # 尾の 先：花びらの 刃（ひれ）
    stamp(g, ['..kk.....', '.kXXkk...', 'kXXWWZkk.', '.kXWWZZZk', '..kWZZkk.', '...kkk...'], 12, 55)
    return g

# ---------- 頭（手打ち）：長い 鼻づら、骨の つの、牙 ----------
HEAD = [
    '.....kkkkk..........',
    '...kkAAAAAkkk.......',
    '..kAABBBBBAAAkkk....',
    '.kABBBBBBBBBBBAAkk..',
    'kABBBBBBBBBBBBBBBAk.',
    'kBBBBBBBBBBBBBBBBBBk',
    'kBBBBBBBBBBBBBBBBkBk',
    'kDBBBBBBBBBkkkkkkkkk',
    'kDDBBBBBkwkwkkkwkk..',
    '.kDDBBBEEEEEEEEEk...',
    '..kDDDEFFFFFFFkk....',
    '...kkkkkkkkkkkk.....',
]
HEAD_OPEN = [
    '.....kkkkk..........',
    '...kkAAAAAkkk.......',
    '..kAABBBBBAAAkkk....',
    '.kABBBBBBBBBBBAAkk..',
    'kABBBBBBBBBBBBBBBAk.',
    'kBBBBBBBBBBBBBBBBBBk',
    'kBBBBBBBBBBBBBBBBkBk',
    'kDBBBBBBkkkkkkkkkkkk',
    'kDDBBBkrrwrrrwrrwk..',
    'kDDBBkrrrrrrrrrrk...',
    '.kDDBkrrrrrrrrrrrk..',
    '.kDDBkkkwkkkwkkwkk..',
    '..kDDEEEEEEEEEEk....',
    '...kkFFFFFFFFkk.....',
    '.....kkkkkkkkk......',
]
HORN = [   # 骨の つの：額から 後ろへ 大きく そる
    'kk.........',
    'kUkk.......',
    '.kUUkk.....',
    '..kUUVkk...',
    '...kUUVVkk.',
    '....kkUVVVk',
    '......kkkk.',
]
HORN2 = ['kk.....', 'kVkk...', '.kVVkk.', '..kkVVk', '....kk.']
ANTENNA = ['..kk', '.kYk', '.kk.', 'k...', 'k...', '.k..']
# 目：黒い まゆの 下で 金に 光る つり目、赤い たての ひとみ
EYE = ['kkkkk..', '.kkkkkk', '.kYYrk.', '..kkk..']
EYE_ALT = {
    'blink': ['kkkkk..', '.kkkkkk', '.kkkkk.', '.......'],
    'atk0|atk1|atk2': ['kkkkk..', '.kkkkkk', '.kYYYk.', '..kkk..'],
    'hit': ['.......', '.kk.kk.', '...k...', '.kk.kk.'],
    'ko': ['.......', '..k.k..', '...k...', '..k.k..'],
}
CLAW = ['.kkk.', 'kBBDk', 'kBDDk', '.kUkU', '..k.k']

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

def layers():
    W = {p: wing(p) for p in FORE}; WF = {p: shift(wing(p, True), 5, -2) for p in FORE}
    BODY = rows_of(body())
    return [
        dict(n='wingB', g='wingB', x=0, y=0, rows=WF['up'], alt={'idle1|idle3|walk1|walk3|atk2|atk1': WF['mid'], 'walk2': WF['down']}),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['up'], alt={'idle1|idle3|walk1|walk3|atk2': W['mid'], 'walk2': W['down']}),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='claw', g='body', x=40, y=37, rows=CLAW),
        dict(n='horn2', g='head', x=41, y=10, rows=HORN2),
        dict(n='head', g='head', x=44, y=10, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='horn', g='head', x=38, y=5, rows=HORN),
        dict(n='eye', g='head', x=49, y=12, rows=EYE, alt=EYE_ALT),
        dict(n='spark', g='root', x=4, y=6, rows=outline(SPARK_A), alt={'idle1|idle3|walk1|walk3': outline(SPARK_B)}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='breath', g='root', x=63, y=14, rows=outline(BREATH), only='atk1'),
        dict(n='breath2', g='root', x=65, y=12, rows=outline(BREATH2), only='atk2'),
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
