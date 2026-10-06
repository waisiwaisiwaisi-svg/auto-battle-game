# モリシシ（くさ・じめん × イノシシ）手打ち GBA風
import pix
META = dict(id='morishishi', name='モリシシ', types=['grass', 'ground'], base='イノシシ', size='L')
PAL = {
    'k': '#101018', 'l': '#33261a',
    'A': '#b4875a', 'B': '#7c5636', 'C': '#4a3120',
    'M': '#a8dc52', 'N': '#5ea434', 'O': '#2e6628',
    'R': '#f0dcaa', 'S': '#b49464',
    'E': '#ff4628', 'w': '#ffffff',
}
LIGHT = set('AMRw')

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
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'M': 'N', 'N': 'O', 'R': 'S', 'w': 'S'}
def dark(rows): return pix.recolor(rows, DARK)

# ---- 胴：肩の こぶに 苔の 毛布。苔の ふちは 手で 指定した たれ ----
SPAN = [(22, 30), (17, 34), (13, 36), (10, 38), (8, 39), (6, 40), (5, 40), (4, 40), (3, 40), (2, 40)] + [(1, 40)] * 9 + \
       [(2, 40), (2, 39), (3, 38), (4, 37), (6, 35), (8, 33)]
MOSS = [12, 11, 12, 10, 11, 13, 12, 10, 11, 12, 14, 12, 11, 10, 12, 13, 11, 12, 14, 13, 11, 10, 12, 14, 13, 12, 11, 13, 12, 10, 11, 13, 12, 11, 10, 9, 10, 8, 9, 8]
def body():
    H = len(SPAN); m = [['.'] * 40 for _ in range(H)]
    for y, (a, b) in enumerate(SPAN):
        for x in range(a, b): m[y][x] = '%' if y < MOSS[x] else '#'
    g = pix.grid_of(shade(pix.rows_of(m), {'#': 'ABC', '%': 'MNO'}, low=19))
    for x in range(40):
        y = MOSS[x]
        if y < H and g[y][x] != '.': g[y][x] = 'C'
        if y + 1 < H and g[y + 1][x] in 'AB' and x % 3: g[y + 1][x] = 'B'
    # 苔の かたまり（明るい 粒）と 影の くぼみ：手で 置く
    for (x, y) in ((8, 6), (12, 4), (15, 7), (19, 3), (23, 6), (27, 3), (31, 5), (34, 7), (20, 9), (11, 9), (28, 8), (6, 9)):
        if g[y][x] in 'NO': g[y][x] = 'M'
        if g[y + 1][x] in 'NM': g[y + 1][x] = 'O'
    # 剛毛の すじ
    for (x, y) in ((6, 15), (7, 16), (10, 14), (11, 15), (16, 16), (17, 17), (22, 15), (23, 16), (28, 16), (29, 17), (34, 14), (35, 15), (5, 19), (12, 19)):
        if g[y][x] in 'AB': g[y][x] = 'C'
    return pix.outline(pix.rows_of(g))
BODY = body()

# ---- 足（太く 短い、石の ひづめ）----
LEG_M = [
    '.#######.',
    '#########',
    '#########',
    '.#######.',
    '.######..',
    '.######..',
    '.######..',
    '..#####..',
    '..#####..',
    '.%%%%%%..',
    '.%%%%%%..',
]
LEG = pix.outline(put(shade(LEG_M, {'#': 'ABC', '%': 'SBC'}), [
    '', '', '', '', '', '', '', '', '',
    '....k',
    '....k',
]))
HLEG_M = [
    '..#######..',
    '.#########.',
    '###########',
    '###########',
    '.#########.',
    '..#######..',
    '...######..',
    '...#####...',
    '...#####...',
    '..%%%%%%...',
    '..%%%%%%...',
]
HLEG = pix.outline(put(shade(HLEG_M, {'#': 'ABC', '%': 'SBC'}), [
    '', '', '', '', '', '', '', '', '',
    '.....k',
    '.....k',
]))

# ---- 頭（手打ち）：長い 鼻と 平らな 鼻先、まゆの 下の 赤い 目 ----
HEAD = [
    '...kk.....................',
    '..kAAk....................',
    '..kABBk...................',
    '..kABBBkkkk...............',
    '.kAABBBBBBBkkk............',
    '.kAABBBBBBBBBBkkk.........',
    'kAABBkkkkkkBBBBBBkkk......',
    'kABBBBBBBkkkkAAAAAAAkkk...',
    'kABBBBBBBBBBkBBBBBBBBBBkk.',
    'kBBBBBBBBBBBBBBBBBBBBBBBkk',
    'kBBCBBBBBBBBBBBBBBBBBBBkRk',
    'kBCBBBBBBBBBBBBBBBBBBBBkSk',
    'kCBCBBBBBBBBBBBBBBBkkkkkkk',
    'kCCBBBBBBBkkkkkkkkkCBBk...',
    '.kCCBBBBkkCCCCCCCCCCk.....',
    '..kCCCBBBCCCCCCCCCk.......',
    '...kkCCCCCCCCCkkk.........',
    '.....kkkkkkkkk............',
]
HEAD_OPEN = HEAD[:12] + [
    'kCBCBBBBBBBBBBBBBkkkkkkkk.',
    'kCCBBBBBBBkkkkkkkwkwk.....',
    '.kCCBBBBBkllllllllk.......',
    '..kCCCBBBkkwkwkkCCk.......',
    '...kkCCCCCCCCCCCCk........',
    '.....kkkkkkkkkkkk.........',
]
EYE = ['EEEk', 'kEEk', '.kk.']
EYE_ALT = {'blink': ['BBBk', 'kkkk', '....'], 'hit': ['kBkB', 'BkBk', '....'], 'atk0|atk1|atk2': ['EEEE', 'kEEE', '.kkk'], 'ko': ['kBkB', 'BkBB', 'kBkB']}
# 根の きば（口の はしから 上へ、先は 後ろへ 曲がる）
TUSK = [
    '.kkk......',
    'kRRSk.....',
    '.kkRSk....',
    '...kRSk...',
    '....kRSk..',
    '....kRRSk.',
    '.....kRSk.',
    '.....kRSk.',
    '....kRRSk.',
    '...kRRSk..',
    '..kRRSk...',
    '..kRSk....',
    '..kSSk....',
    '...kk.....',
]
# 背すじの 根の とげ（イノシシの たてがみ）
SPK = ['k....', 'kRk..', '.kRk.', '.kRSk', '.kRSk', 'kRSSk', 'kRSSk']
def crest():
    g = pix.grid(40, 14)
    for (x, y) in ((0, 7), (6, 4), (12, 2), (19, 1), (26, 2), (32, 5)): pix.stamp(g, SPK, x, y)
    return pix.rows_of(g)
CREST = crest()
# ---- 背中の 若木 ----
TREE = [
    '....kkkk...kkk......',
    '..kkMMMNkkkMMNkk....',
    '.kMMMNNNNkMMNNNOk...',
    'kMMNNMNNNNNNMNNOOk..',
    'kMNNNNNNNOONNNOOOk..',
    '.kNNNOONOkkONOOOk...',
    '..kkOOkkBkkkOOkk....',
    '....kkkBBkkkkk......',
    '......kkBkkBk.......',
    '.......kBBBk........',
    '.......kBCk.........',
    '......kABCk.........',
    '......kABCk.........',
    '.....kABBCCk........',
]
TREE2 = [
    '...kkkk....kkk......',
    '.kkMMMNkk.kMMNkk....',
    'kMMMNNNNkkMMNNNOk...',
    'kMNNMNNNNNNNMNNOOk..',
    'kMNNNNNNNOONNNOOOk..',
    '.kNNNOONOkkONOOOk...',
    '..kkOOkkBkkkOOkk....',
    '....kkkBBkkkkk......',
    '......kkBkkBk.......',
    '.......kBBBk........',
    '.......kBCk.........',
    '......kABCk.........',
    '......kABCk.........',
    '.....kABBCCk........',
]
# ---- 土けむり（突進）と はね上げた 土くれ ----
DUST = [
    '......kk.......',
    '..kk.kSSk..kk..',
    '.kSSkkSRSkkSRk.',
    'kSRRSSRRRSSRRSk',
    'kSSRRRRSSRRSSSk',
    '.kkSSSSkkSSSkk.',
    '...kkkk..kkk...',
]
CLODS = [
    '....kk.....kk..',
    '...kBCk...kAk..',
    '....kk..kk.k...',
    '.kk....kNk.....',
    'kABk....k...kk.',
    '.kk........kBk.',
    '............k..',
]

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='hlegF', g='legB', x=14, y=47, rows=dark(HLEG)),
        dict(n='flegF', g='legB', x=40, y=47, rows=dark(LEG)),
        dict(n='crest', g='body', x=11, y=15, rows=CREST),
        dict(n='tree', g='tree', x=24, y=12, rows=TREE, alt={'idle1|idle2|walk1|walk3|atk1': TREE2}),
        dict(n='body', g='body', x=5, y=24, rows=BODY),
        dict(n='hleg', g='legA', x=7, y=47, rows=HLEG),
        dict(n='fleg', g='legA', x=33, y=47, rows=LEG),
        dict(n='head', g='head', x=37, y=29, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='eye', g='head', x=42, y=36, rows=EYE, alt=EYE_ALT),
        dict(n='tusk', g='head', x=54, y=28, rows=TUSK),
        dict(n='dust', g='fx', x=0, y=50, rows=DUST, only=NB),
        dict(n='clods', g='head', x=58, y=16, rows=CLODS, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 3), 'legA': (-1, 0), 'tree': (-1, 0)},
    'atk1': {'root': (6, 0), 'head': (1, 3), 'fx': (-6, 0)},
    'atk2': {'root': (8, 0), 'head': (1, -3), 'tree': (1, 0), 'fx': (-10, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'tree': (-1, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tree': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
