# ヨドグモ（どく・むし × クモ）手打ち GBA風
import pix
META = dict(id='yodogumo', name='ヨドグモ', types=['poison', 'bug'], base='クモ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1640',
    'A': '#9a7ac4', 'B': '#563e7e', 'C': '#2e2048',      # 体（よどんだ 紫）
    'G': '#e2ff70', 'H': '#82d43c', 'I': '#2e7a40',      # 毒の ふくろ
    'R': '#ff4648', 'F': '#f2e8c8', 'Q': '#a89070',      # 目（赤）・牙（骨色）
    'w': '#ffffff',
}
LIGHT = set('AGFw')
KEEP_BLACK = set('wRG')

def shade(mask, lt, md, dk, t=2, lf=1, r=2, b=2):
    g = pix.grid_of(mask); H, W = len(g), len(g[0])
    on = lambda y, x: 0 <= y < H and 0 <= x < W and g[y][x] != '.'
    out = [r_[:] for r_ in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '#': continue
            dt = 0
            while on(y - dt - 1, x): dt += 1
            db = 0
            while on(y + db + 1, x): db += 1
            dl = 0
            while on(y, x - dl - 1): dl += 1
            dr = 0
            while on(y, x + dr + 1): dr += 1
            c = md
            if dt < t or dl < lf: c = lt
            if dr < r or db < b: c = dk
            if dt < t and dr < r: c = md
            out[y][x] = c
    return [''.join(r_) for r_ in out]
def put(rows, det, x0=0, y0=0):
    g = pix.grid_of(rows)
    for j, r in enumerate(det):
        for i, c in enumerate(r):
            if c not in '. ' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c
    return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'F': 'Q'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 足：関節の 位置を 手で 決め、線で あたり → 2段の 陰影＋ひざの つや ----
def leg(pts, far=False):
    g = pix.grid(72, 64)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        pix.line(g, x0, y0, x1, y1, 'B')
    for (x, y) in pts[1:-1]:                       # ひざ：ふくらみと つや
        g[y][x] = 'A'; g[y - 1][x] = 'A'; g[y][x + 1] = 'C'; g[y - 1][x + 1] = 'B'
    for (x0, y0), (x1, y1) in zip(pts[1:], pts[2:]):   # すねの 下半分は 影
        n = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(n // 2, n + 1):
            x, y = x0 + round((x1 - x0) * t / n), y0 + round((y1 - y0) * t / n)
            if g[y][x] == 'B': g[y][x] = 'C'
    rows = pix.outline(pix.rows_of(g))[1:]
    rows = [r[1:] for r in rows]
    gg = pix.grid_of(rows)
    for (x, y) in pts[1:-1]:                       # ひざの 上の とげ毛
        if gg[y - 3][x] == '.': gg[y - 3][x] = 'k'
        if gg[y - 2][x - 2] == '.': gg[y - 2][x - 2] = 'k'
    rows = pix.rows_of(gg)
    return dark(rows) if far else rows

L1 = [(41, 41), (51, 29), (58, 37), (61, 58)]
L1_UP = [(41, 40), (49, 22), (56, 17), (61, 21)]
L2 = [(39, 42), (45, 22), (49, 39), (53, 58)]
L3 = [(35, 42), (28, 23), (22, 39), (17, 58)]
L4 = [(34, 43), (17, 27), (10, 41), (5, 58)]
F1 = [(41, 40), (47, 25), (53, 40), (56, 57)]
F2 = [(38, 40), (40, 33), (44, 44), (47, 57)]
F3 = [(35, 40), (23, 30), (18, 43), (11, 57)]
F4 = [(33, 41), (13, 33), (7, 45), (4, 51)]

# ---- 腹：毒の ふくろが すけて 光る ----
def abdomen(hot=False):
    g = pix.grid(28, 24); pix.ellipse(g, 14, 12, 14, 12, '#')
    rows = shade(pix.rows_of(g), 'A', 'B', 'C', t=3, lf=2, r=3, b=4)
    g = pix.grid_of(rows)
    sacs = [(9, 6, 3), (17, 7, 3), (12, 13, 3), (20, 14, 2), (5, 12, 2)]
    for (cx, cy, r) in sacs:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
                if d > r + .3 or g[y][x] == '.': continue
                if d > r - .7: g[y][x] = 'k' if (x - cx) + (y - cy) > 0 else 'I'
                elif (x - cx) + (y - cy) < -r * .5 or (hot and d < r * .6): g[y][x] = 'G'
                elif (x - cx) + (y - cy) > r * .6: g[y][x] = 'I'
                else: g[y][x] = 'H'
    # 毛（ひかえめな 点）と つや
    for (x, y) in ((4, 5), (6, 3), (14, 3), (22, 8), (24, 13), (8, 19), (16, 20), (3, 8)):
        if g[y][x] in 'ABC': g[y][x] = 'A' if y < 10 else 'l'
    # 糸いぼ
    g[16][0] = 'C'; g[17][0] = 'C'
    return pix.outline(pix.rows_of(g))

CEPH = [
    '......kkkkkk........',
    '....kkAAAAAkRkk.....',
    '...kAAAABBkRRkRk....',
    '..kAABBBBBBkkkkkk...',
    '.kAABBBBBBBk.....k..',
    'kAABBBBBBBBBk.....k.',
    'kABBBBBBBBBBBkkkkkBk',
    'kBBBBBBBBBBBBBBBBBBk',
    'kBBBBBBBBBBBBBBBBBCk',
    'kCBBBBBBBBBBBBBBBCCk',
    '.kCCBBBBBBBBBBBCCCk.',
    '..kkCCCCCCCCCCCCkk..',
    '....kkkkkkkkkkkkk...',
]
# 目：大きな 赤い つり目（後ろへ 上がる）＋ 小さな 目が 6つ
EYE = ['RRRwkRRw', 'kRRkkkRR']
EYE_ALT = {'blink': ['kkkkkkkk', 'BBkkkkkk'], 'atk0|atk1|atk2': ['RRRRkRRw', 'kRRRRkRR'],
           'hit': ['kRkkkRkk', 'kkRRkkRk'], 'ko': ['RkRkRkRk', 'kRkkkRkk']}
FANG = [
    '.kkkk...',
    'kABBCk..',
    'kBBCCk..',
    '.kBCCkk.',
    '.kFFFQk.',
    '..kFFQk.',
    '..kFQk..',
    '.kFQk...',
    '.kQk....',
    '..k.....',
]
FANG_OPEN = [
    '.kkkk.....',
    'kABBCk....',
    'kBBCCkk...',
    '.kBCCCFkk.',
    '..kkkFFQk.',
    '.....kFQk.',
    '......kQk.',
    '......kk..',
]
DROP = {'idle0|walk0|walk2': ['.k.', 'kGk', 'kHk', '.k.'], 'idle1|walk1|walk3|blink': ['...', '.k.', 'kGk', 'kHk'],
        'idle2': ['...', '...', '...', '.G.'], 'idle3': ['.k.', 'kGk', '.k.', '...']}
GLOB = [
    '...kkk....',
    '.kkGGGk...',
    'kGGGHHHkk.',
    'kGHHHHIIHk',
    '.kHHIIIkk.',
    '..kkkkk...',
]
SPLAT = [
    '.H...G..H.',
    '...kGGk...',
    'G.kGHHHk.G',
    '.kGHHIHHk.',
    'H.kHIIIk.H',
    '...kkkk...',
    '.G..H...G.',
]

def layers():
    A = 'atk0|atk1|atk2'
    return [
        dict(n='f4', g='legB', x=0, y=0, rows=leg(F4, True)),
        dict(n='f3', g='legA', x=0, y=0, rows=leg(F3, True)),

        dict(n='f1', g='legA', x=0, y=0, rows=leg(F1, True)),
        dict(n='abd', g='body', x=4, y=19, rows=abdomen(), alt={'idle1|idle3|walk1|walk3|' + A: abdomen(True)}),
        dict(n='l4', g='legA', x=0, y=0, rows=leg(L4)),
        dict(n='l3', g='legB', x=0, y=0, rows=leg(L3)),
        dict(n='l2', g='legA', x=0, y=0, rows=leg(L2)),
        dict(n='l1', g='legF', x=0, y=0, rows=leg(L1), alt={'atk0': leg(L1_UP)}),
        dict(n='fangF', g='head', x=45, y=40, rows=dark(FANG), alt={'atk0': dark(FANG_OPEN)}),
        dict(n='ceph', g='head', x=27, y=31, rows=CEPH),
        dict(n='eye', g='head', x=39, y=35, rows=EYE, alt=EYE_ALT),
        dict(n='fang', g='head', x=42, y=41, rows=FANG, alt={'atk0': FANG_OPEN}),
        dict(n='drop', g='head', x=43, y=50, rows=DROP['idle0|walk0|walk2'], alt=DROP, not_=A + '|hit|ko'),
        dict(n='glob', g='head', x=52, y=40, rows=GLOB, only='atk1'),
        dict(n='splat', g='head', x=60, y=40, rows=SPLAT, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'legF': (1, -1)},
    'walk1': {'body': (0, -1), 'head': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'legF': (-1, 0)},
    'walk3': {'body': (0, -1), 'head': (0, -1)},
    'atk0': {'root': (-3, 0), 'body': (0, -1), 'head': (0, -3)},
    'atk1': {'root': (5, 0), 'head': (1, 1)},
    'atk2': {'root': (5, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, 2), 'body': (0, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root', 'legF': 'root'}
