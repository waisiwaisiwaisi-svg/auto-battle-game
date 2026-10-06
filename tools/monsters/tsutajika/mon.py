# ツタジカ（くさ・フェアリー × シカ）手打ち GBA風
import pix
META = dict(id='tsutajika', name='ツタジカ', types=['grass', 'fairy'], base='シカ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c2c52',
    'A': '#dccced', 'B': '#a08abf', 'C': '#5e4a82',
    'G': '#a6e45c', 'H': '#4c9c3c', 'I': '#245a30',
    'P': '#ffb8e4', 'Q': '#e64ca0',
    'R': '#efe2c4', 'S': '#a89272',
    'w': '#ffffff',
}
LIGHT = set('AGPRw')

def shade(rows, ramps, low=99):
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            hi, mid, lo = ramps[m]
            def e(dy, dx):
                yy, xx = y + dy, x + dx
                return not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m
            a = e(-1, 0) or e(-2, 0) or (e(0, -1) and y < low)
            b = e(1, 0) or e(0, 1) or e(1, 1) or e(0, 2)
            c = lo if y >= low else mid
            if a and not b: c = hi
            elif b and not a: c = lo
            o[y][x] = c
    return pix.rows_of(o)
def put(base, over, x=0, y=0):
    g = pix.grid_of(base); w = max(len(r) for r in over) + x; h = len(over) + y
    if w > len(g[0]): g = [r + ['.'] * (w - len(r)) for r in g]
    while len(g) < h: g.append(['.'] * len(g[0]))
    pix.stamp(g, over, x, y); return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'G': 'H', 'H': 'I', 'R': 'S', 'P': 'Q', 'w': 'P'}
def dark(rows): return pix.recolor(rows, DARK)
def notop(r): return ['.' * len(r[0])] + r[1:]

# ---- 胴：細く しまった 胴、背に 白い 斑（はん）----
BODY_M = [
    '.....####################.....',
    '..##########################..',
    '.############################.',
    '##############################',
    '##############################',
    '.#############################',
    '.############################.',
    '..##########################..',
    '...#######.........#######....',
    '....####............#####.....',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'ABC'}, low=7), [
    '',
    '.....A....A.....A',
    '..A....A....A.....A.....C',
    '......A....A...A.......C',
    '.......C..............C',
    '........C............C',
    '........C',
]))
# 背中を はう いばらの つた（葉と とげ）
VINE = [
    '..........kk..............kk.....',
    '.kk......kGGk......kk....kGHk....',
    'kGHk.kk.kGHk.kk...kGGk..kkHk.kk..',
    '.kkHkSkkkkkHkSkkkkkkGHkkSkkkkHkk.',
    '...kHHGGGHHkHHGGGGHHkkHHGGGHHkGHk',
    '....kkkkkkkkkkkkkkkkk.kkkkkkkkkkk',
]
NECK_M = [
    '.......#####',
    '......######',
    '.....#######',
    '.....######.',
    '.....######.',
    '....######..',
    '....######..',
    '...#######..',
    '..########..',
    '.#########..',
    '##########..',
    '###########.',
]
NECK = notop(pix.outline(put(shade(NECK_M, {'#': 'ABC'}), [
    '', '',
    '.....GG',
    '......HGG',
    '........HG',
    '', '',
    '...GG',
    '....HGG',
    '......HGG',
    '........H',
])))

# ---- 足：細く 長い。ひづめは 刃の ように とがる ----
HLEG_M = [
    '..######....',
    '.########...',
    '##########..',
    '##########..',
    '.#########..',
    '..########..',
    '...######...',
    '....####....',
    '.....###....',
    '....###.....',
    '...###......',
    '...##.......',
    '...##.......',
    '...##.......',
    '..%%%.......',
    '..%%%%......',
]
HLEG = notop(pix.outline(shade(HLEG_M, {'#': 'ABC', '%': 'BCC'})))
FLEG_M = [
    '.####..',
    '#####..',
    '#####..',
    '.####..',
    '.###...',
    '..##...',
    '..##...',
    '..##...',
    '..##...',
    '..##...',
    '..##...',
    '..##...',
    '.%%%...',
    '.%%%%..',
]
FLEG = notop(pix.outline(put(shade(FLEG_M, {'#': 'ABC', '%': 'BCC'}), [
    '', '', '', '', '',
    '..GG',
    '..HG',
    '', '',
    '..GG',
    '..HG',
])))

# ---- 頭（手打ち）：細い 鼻づら、つり上がった 桃色の 目 ----
HEAD = [
    '..kkkkkk...........',
    '.kAAAAAAkkk........',
    'kAABBBBBBBBkkk.....',
    'kABkkkkkkBBBBBkkk..',
    'kABBBBBkkkAAAAAABkk',
    'kBBBBBCBBkBBBBBBBCk',
    'kBCBBBBCBBBBBBBkkkk',
    'kCBCBBBBCBBBkkkk...',
    '.kCCBBBBBBCk.......',
    '..kkCCCCCCk........',
    '....kkkkkk.........',
]
HEAD_ATK = HEAD[:5] + [
    'kBBBBBCBBkBBBBBBBCk',
    'kBCBBBBCBBBBkkkkkk.',
    'kCBCBBBBCkwkwkk....',
    '.kCCBBBBBBkk.......',
    '..kkCCCCCCk........',
    '....kkkkkk.........',
]
EYE = ['kPPQk', '.kkk.']
EYE_ALT = {'blink': ['kkkkk', '.....'], 'hit': ['kBkBk', '.kBk.'], 'atk0|atk1|atk2': ['kPwPP', '.kkkk'], 'ko': ['kBkBk', '.kBk.']}
# 葉の 耳（後ろへ）
EAR = [
    'kk.......',
    'kGkk.....',
    'kGGHkk...',
    '.kGHHHk..',
    '.kGGHIHk.',
    '..kkGHIk.',
    '....kkk..',
]

# ---- いばらの 角：木の 枝角に つたが 巻きつき、先に 光る 花 ----
# 角の 骨組み：主幹は 後ろへ そり、枝は 上へ（点は 手で 決めた）
BEAMS = [((21, 21), (14, 14)), ((14, 14), (8, 9)), ((8, 9), (2, 4)), ((2, 4), (1, 1)),
         ((10, 11), (8, 1)), ((14, 14), (16, 6)), ((16, 6), (16, 2)), ((18, 18), (24, 13)), ((24, 13), (27, 12))]
def antler(glow=False):
    W, H = 30, 23; g = pix.grid(W, H)
    for (a, b) in BEAMS:
        pix.line(g, a[0], a[1], b[0], b[1], 'R')
    for y in range(H):
        for x in range(W - 1, 0, -1):
            if g[y][x - 1] == 'R' and g[y][x] == '.': g[y][x] = 'S'
    for (x, y) in ((19, 19), (15, 15), (12, 12), (9, 10), (5, 7), (16, 9), (9, 5), (22, 15)):
        if g[y][x] != '.': g[y][x] = 'G'
        if g[y][x + 1] != '.': g[y][x + 1] = 'H'
    for (x, y) in ((17, 21), (12, 15), (6, 9), (11, 6), (18, 7), (24, 16), (3, 2)):
        if g[y][x] == '.': g[y][x] = 'S'
    o = pix.grid_of(pix.outline(pix.rows_of(g)))
    for (x, y) in ((1, 1), (8, 1), (16, 2), (27, 12)):
        pix.stamp(o, ['.PP.', 'PwwP', 'PwPP', '.PP.'] if glow else ['.kk.', 'kPPk', 'kPQk', '.kk.'], x - 1, y - 1)
    return pix.rows_of(o)
ANT = antler(); ANT_GLOW = antler(True)
TAIL = [
    '.kk...',
    'kGHk..',
    'kGGHkk',
    '.kGHHk',
    '..kkk.',
]
# ---- いばらの むち（攻撃）：角から つたが 前へ のびる ----
def whip():
    import math
    W, H = 34, 12; g = pix.grid(W, H)
    for x in range(1, 29):
        y = int(round(6 + 2.4 * math.sin(x / 3.2) - x * .12))
        g[y][x] = 'G'; g[y + 1][x] = 'H'
        if x % 4 == 2: g[y - 1][x] = 'S'
        if x % 4 == 0: g[y + 2][x] = 'S'
    o = pix.grid_of(pix.outline(pix.rows_of(g)))
    pix.stamp(o, ['.kk.k', 'kPPkP', 'kPwPk', '.kPQk', '..kk.'], 28, 0)
    return pix.rows_of(o)
WHIP = whip()
PETALS = [
    '..kk.......kk......',
    '.kPQk.....kPk...kk.',
    '..kk...kk..k...kPQk',
    '......kPwk......kk.',
    '.kk....kk....kk....',
    'kPQk........kPQk...',
    '.kk..........kk....',
]

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='hlegF', g='legB', x=16, y=41, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=35, y=42, rows=dark(FLEG), not_='ko'),
        dict(n='tail', g='body', x=7, y=32, rows=TAIL),
        dict(n='body', g='body', x=9, y=34, rows=BODY),
        dict(n='vine', g='body', x=8, y=30, rows=VINE),
        dict(n='hleg', g='legA', x=10, y=41, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=30, y=42, rows=FLEG, not_='ko'),
        dict(n='neck', g='neck', x=33, y=24, rows=NECK),
        dict(n='ear', g='head', x=38, y=21, rows=EAR),
        dict(n='head', g='head', x=41, y=20, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=43, y=23, rows=EYE, alt=EYE_ALT),
        dict(n='ant', g='ant', x=24, y=1, rows=ANT, alt={'atk0|atk1|atk2|idle2|idle3': ANT_GLOW}),
        dict(n='whip', g='ant', x=50, y=12, rows=WHIP, only='atk1'),
        dict(n='petals', g='ant', x=48, y=6, rows=PETALS, only='atk2'),
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
