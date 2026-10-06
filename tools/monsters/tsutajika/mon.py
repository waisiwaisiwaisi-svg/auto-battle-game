# ツタジカ（くさ・フェアリー × シカ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline, ellipse

META = dict(id='tsutajika', name='ツタジカ', types=['grass', 'fairy'], base='シカ', size='L')
PAL = {
    'k': '#101018', 'l': '#36264c',
    'A': '#e4d6f2', 'B': '#a68ccc', 'C': '#5c4488',      # 毛皮（うす紫）
    'G': '#aaea5c', 'H': '#4a9e3a', 'I': '#22562c',      # 葉と つた
    'P': '#ffbce6', 'Q': '#ea4ca4',                      # 光る 花
    'R': '#f2e6c8', 'S': '#b49a74', 'T': '#6c5638',      # 白木の 角
    'w': '#ffffff',
}
LIGHT = set('AGPRw')

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
def tube(p, path, rad, ch='1'):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64: p[y][x] = ch
FUR = {'1': 'ABC'}
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'G': 'H', 'H': 'I', 'R': 'S', 'S': 'T', 'P': 'Q', 'w': 'P'}
def dark(g): return [[DARK.get(c, c) for c in r] for r in g]
def part(build, ramps=FUR, r=2, far=False, hi=.32, lo=-.28):
    p = G(); build(p); s = shade(p, ramps, r, hi, lo)
    if far: s = dark(s)
    g = G(); ink(g, s); return g

# ---------- 足：太く たくましい。ひづめは 刃の ように とがる ----------
def hind(p):
    ellipse(p, 17, 38, 6.5, 7, '1')                                  # 太い もも
    tube(p, [(19, 42), (13, 50), (14, 57)], [3, 2.1, 1.8])         # かかとは 後ろへ 折れる
def fore(p):
    ellipse(p, 40, 38, 5, 6.5, '1')                                  # 肩の 筋肉
    tube(p, [(40, 42), (41, 50), (40, 57)], [2.7, 2.1, 1.8])
HOOF = ['.kkkkk..', 'kSSSTTk.', 'kSTTTTTk', 'kkkkkkkk']
def leg(build, hx, far=False, shift=0):
    def b(p):
        q = G(); build(q)
        for y in range(64):
            for x in range(64):
                if q[y][x] != '.' and 0 <= x + shift < 64: p[y][x + shift] = q[y][x]
    g = part(b, far=far)
    # ひざの つた（手で 巻く）
    for (x, y, c) in ((hx - 1, 52, 'G'), (hx, 53, 'H'), (hx + 1, 54, 'H'), (hx - 1, 55, 'G')):
        if g[y][x + shift] not in '.k': g[y][x + shift] = DARK.get(c, c) if far else c
    h = HOOF if not far else [r.replace('S', 'T') for r in HOOF]
    stamp(g, h, hx - 3 + shift, 57)
    return g

# ---------- 胴：厚い 胸と 盛り上がった 肩。背に 白い 斑 ----------
def body():
    def b(p):
        ellipse(p, 16, 36, 8, 7.5, '1')     # しり
        ellipse(p, 27, 36.5, 13, 7.2, '1')  # どう
        ellipse(p, 38, 36, 8.5, 8.8, '1')   # 厚い 胸
    g = part(b, r=3)
    # 筋肉の すじ（肩・もも・あばら）を 手で
    dots(g, 'C', [(35, 33), (34, 34), (34, 35), (34, 36), (35, 38), (22, 35), (23, 36), (23, 37), (23, 38), (27, 41), (29, 42), (31, 42)])
    dots(g, 'A', [(36, 32), (35, 33), (24, 34), (24, 35), (28, 40), (30, 41)])
    # 白い 斑（フェアリーの しるし）
    dots(g, 'w', [(14, 32), (19, 31), (25, 32), (30, 31), (17, 34), (22, 33), (28, 34)])
    return g

# ---------- 首：太く 前へ のびる。いばらの つたが 巻く ----------
def neck():
    def b(p):
        poly(p, [(35, 32), (39, 25), (43, 20), (49, 17), (53, 19), (52, 25), (49, 31), (47, 38), (42, 40), (37, 38)], '1')
    g = part(b, r=2)
    # 首の 下の 毛（明るい えりまき）
    for (x, y) in ((50, 27), (49, 29), (48, 31), (47, 33), (46, 35), (51, 25), (49, 28), (48, 30), (47, 32)):
        if g[y][x] in 'BC': g[y][x] = 'A' if (x + y) % 2 else 'B'
    # つたの 帯（ななめに 2本）
    for (x0, y0) in ((38, 31), (41, 24)):
        for i in range(10):
            x, y = x0 + i, y0 + 3 - round(i * .45)
            if g[y][x] not in '.k': g[y][x] = 'H' if i % 3 else 'G'
            if g[y + 1][x] not in '.k': g[y + 1][x] = 'I'
    return g
# 首の うしろの 葉の たてがみ（手で 置く 葉）
LEAF = ['.kk..', 'kGGk.', 'kGHHk', '.kHIk', '..kk.']
LEAF_S = ['.kk.', 'kGHk', 'kHIk', '.kk.']

# ---------- 頭（手打ち）：大きな くさび形、深い まゆの ひさし ----------
HEAD = [
    '....kkkkkkk...........',
    '..kkAAAAAAAkkk........',
    '.kAABBBBBBBAAAkkk.....',
    'kAABBBBBBBBBBBBAAkkk..',
    'kABBBBBBBBBBBBBBBBAAk.',
    'kBBBBBBBBBBBBBBBBBBBBk',
    'kBBBBBBBBBBBBBBBBBBkkk',
    'kCBBBBBBBBBBBBBBBBBBk.',
    'kCBBBCBBBBBBBBBBBBBk..',
    'kCCBBBCBBBBBkkkkkkkk..',
    '.kCCBBBBBCCBBBBBBBk...',
    '..kCCBBBCCCCCCCCkk....',
    '...kkCCCCCCCkkkk......',
    '.....kkkkkkk..........',
]
HEAD_ATK = HEAD[:8] + [
    'kCBBBCBBBBBBkkkkkkkkk.',
    'kCCBBBCBBBkwkwkwkk....',
    '.kCCBBBBBkkkkkkkkk....',
    '..kCCBBBCCCCCCCCCk....',
    '...kkCCCCCCCCkkkk.....',
    '.....kkkkkkkk.........',
]
# するどい 目：重い まゆの ひさしの 下で 桃色に 光る（たての ひとみ）
EYE = ['kkkk.....', '.CCkkkkk.', '..kPwPQkk', '...kkkkk.']
EYE_ALT = {
    'blink': ['kkkk.....', '.CCkkkkk.', '..kkkkkkk', '.........'],
    'atk0|atk1|atk2': ['kkkk.....', '.CCkkkkk.', '..kwwwPkk', '...kkkkk.'],
    'hit': ['kkkk.....', '.C.k...k.', '....kkk..', '...k...k.'],
    'ko': ['.........', '...k...k.', '....kkk..', '...k...k.'],
}
EAR = ['kk........', 'kGkk......', '.kGGHkk...', '.kGGHHHk..', '..kGHHIIk.', '...kkHIk..', '.....kk...']

# ---------- いばらの 角：太い 白木の 枝角に つたが 巻き、とげと 光る 花 ----------
NEAR = [((46, 14), (41, 9), (34, 5), (27, 3)), ((41, 9), (42, 4), (41, 1)), ((34, 5), (32, 0)), ((47, 13), (53, 9))]
FARA = [((50, 13), (54, 8), (58, 5), (61, 4)), ((54, 8), (53, 2)), ((58, 5), (59, 0))]
TIPS_N = [(27, 3), (41, 1), (32, 0), (53, 9)]
TIPS_F = [(61, 4), (53, 2), (59, 0)]
def antler(beams, tips, far=False, glow=False):
    p = G()
    for b in beams:
        n = len(b); tube(p, list(b), [2.3 - 1.2 * i / max(1, n - 1) for i in range(n)])
    s = shade(p, {'1': 'RST'}, r=1, hi=.2, lo=-.2)
    # つたが 巻きつく（ななめの 緑の すじ）＋とげ
    for b in beams:
        for (x0, y0), (x1, y1) in zip(b, b[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0))
            for i in range(1, n, 3):
                x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
                if s[y][x] in 'RST': s[y][x] = 'G'
                if at(s, x + 1, y + 1) in 'RST': s[y + 1][x + 1] = 'H'
    if far: s = dark(s)
    g = G(); ink(g, s)
    # とげ（つたの 外へ 1ドット）
    for (x, y) in ((38, 5), (30, 2), (44, 6), (45, 10), (57, 3), (51, 6), (37, 9), (29, 6)):
        if g[y][x] == 'k' or g[y][x] == '.':
            g[y][x] = 'S' if not far else 'T'
    # 光る 花
    for (x, y) in tips:
        f = ['.PP.', 'PwwP', 'PwPQ', '.PQ.'] if glow else ['.kk.', 'kPPk', 'kPQk', '.kk.']
        if far and not glow: f = ['.kk.', 'kQQk', 'kQlk', '.kk.']
        stamp(g, outline(f) if glow else f, x - (2 if glow else 1), y - (2 if glow else 1))
    return g

TAIL = ['.kk...', 'kGHk..', 'kGGHkk', '.kGHHk', '..kIIk', '...kk.']
# 背を はう いばらの つた
VINE = [
    '..........kk.............kk......',
    '.kk......kGGk......kk...kGHk.....',
    'kGHk.kk.kGHk.kk...kGGk..kHHk.kk..',
    '.kkHkSkkkkkHkSkkkkkkGHkkSkkkkHkk.',
    '...kHHGGGHHkHHGGGGHHkkHHGGGHHkGHk',
    '....kkkkkkkkkkkkkkkkk.kkkkkkkkkkk',
]
def whip():
    W, H = 30, 12; g = grid(W, H)
    for x in range(1, 25):
        y = int(round(6 + 2.4 * math.sin(x / 3.2) - x * .12))
        g[y][x] = 'G'; g[y + 1][x] = 'H'
        if x % 4 == 2: g[y - 1][x] = 'S'
        if x % 4 == 0: g[y + 2][x] = 'S'
    o = [list(r) for r in outline(rows_of(g))]
    stamp(o, ['.kk.k', 'kPPkP', 'kPwPk', '.kPQk', '..kk.'], 24, 0)
    return rows_of(o)
PETALS = [
    '..kk.......kk......',
    '.kPQk.....kPk...kk.',
    '..kk...kk..k...kPQk',
    '......kPwk......kk.',
    '.kk....kk....kk....',
    'kPQk........kPQk...',
    '.kk..........kk....',
]

def layers():
    NA = rows_of(antler(NEAR, TIPS_N)); NAG = rows_of(antler(NEAR, TIPS_N, glow=True))
    FA = rows_of(antler(FARA, TIPS_F, far=True)); FAG = rows_of(antler(FARA, TIPS_F, far=True, glow=True))
    GLOW = 'atk0|atk1|atk2|idle2|idle3'
    mane = []
    for i, (x, y) in enumerate(((41, 19), (38, 23), (35, 27), (44, 16))):
        mane.append(dict(n=f'mane{i}', g='neck', x=x, y=y, rows=LEAF if i % 2 == 0 else LEAF_S))
    return [
        dict(n='farA', g='ant', x=0, y=0, rows=FA, alt={GLOW: FAG}),
        dict(n='hlegF', g='legB', x=0, y=0, rows=rows_of(leg(hind, 14, far=True, shift=6)), not_='ko'),
        dict(n='flegF', g='legB', x=0, y=0, rows=rows_of(leg(fore, 40, far=True, shift=-5)), not_='ko'),
        dict(n='tail', g='body', x=5, y=30, rows=TAIL),
        dict(n='body', g='body', x=0, y=0, rows=rows_of(body())),
        dict(n='vine', g='body', x=9, y=25, rows=VINE),
        dict(n='hleg', g='legA', x=0, y=0, rows=rows_of(leg(hind, 14)), not_='ko'),
        dict(n='fleg', g='legA', x=0, y=0, rows=rows_of(leg(fore, 40)), not_='ko'),
        dict(n='neck', g='neck', x=0, y=0, rows=rows_of(neck())),
    ] + mane + [
        dict(n='ear', g='head', x=35, y=12, rows=EAR),
        dict(n='head', g='head', x=42, y=12, rows=HEAD, alt={'atk1|atk2': HEAD_ATK}),
        dict(n='eye', g='head', x=44, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='nearA', g='ant', x=0, y=0, rows=NA, alt={GLOW: NAG}),
        dict(n='whip', g='ant', x=56, y=12, rows=whip(), only='atk1'),
        dict(n='petals', g='ant', x=50, y=4, rows=PETALS, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'neck': (0, 0)},
    'idle2': {'body': (0, 1)},
    'idle3': {'body': (0, 0), 'head': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'neck': (0, 2), 'head': (0, 1), 'legA': (-1, 0)},
    'atk1': {'root': (4, 0), 'neck': (1, 3), 'head': (1, 1)},
    'atk2': {'root': (5, 0), 'neck': (1, 2)},
    'hit': {'root': (-3, 0), 'neck': (-1, -1), 'head': (-2, -1)},
    'ko': {'body': (-2, 12), 'neck': (0, 4), 'head': (2, 2)},
}
PARENT = {'ant': 'head', 'head': 'neck', 'neck': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
