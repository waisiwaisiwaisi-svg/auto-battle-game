# モリシシ（くさ・じめん × イノシシ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭、苔の こぶの 胴は 小さく 丸く、足は 短く 太く）
import pix
META = dict(id='morishishi', name='モリシシ', types=['grass', 'ground'], base='イノシシ', size='L')
PAL = {
    'k': '#101018', 'l': '#33261a',
    'A': '#b4875a', 'B': '#7c5636', 'C': '#4a3120',
    'M': '#a8dc52', 'N': '#5ea434', 'O': '#2e6628',
    'R': '#f0dcaa', 'S': '#b49464',
    'E': '#ff5a2a', 'F': '#a8201c', 'w': '#ffffff',     # 目：明・暗の 虹彩
}
KEEP_BLACK = set('wEF')
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
SPAN = [(12, 24), (8, 29), (5, 31), (3, 33), (2, 34), (1, 35), (1, 35)] + [(0, 36)] * 9 + [(1, 36), (1, 35), (2, 34), (4, 32)]
MOSS = [9, 9, 10, 9, 10, 11, 10, 9, 10, 11, 12, 10, 11, 10, 9, 11, 12, 11, 10, 9, 10, 11, 12, 10, 9, 10, 9, 8, 9, 8, 7, 8, 7, 6, 6, 6]
def body():
    H = len(SPAN); m = [['.'] * 36 for _ in range(H)]
    for y, (a, b) in enumerate(SPAN):
        for x in range(a, b): m[y][x] = '%' if y < MOSS[x] else '#'
    g = pix.grid_of(shade(pix.rows_of(m), {'#': 'ABC', '%': 'MNO'}, low=17))
    for x in range(36):
        y = MOSS[x]
        if y < H and g[y][x] != '.': g[y][x] = 'C'
        if y + 1 < H and g[y + 1][x] in 'AB' and x % 3: g[y + 1][x] = 'B'
    # 苔の かたまり（明るい 粒）と 影の くぼみ：手で 置く
    for (x, y) in ((6, 5), (10, 3), (13, 6), (17, 2), (21, 5), (25, 3), (8, 8), (19, 8), (28, 5)):
        if g[y][x] in 'NO': g[y][x] = 'M'
        if g[y + 1][x] in 'NM': g[y + 1][x] = 'O'
    # 剛毛の すじ
    for (x, y) in ((5, 13), (6, 14), (10, 13), (11, 14), (16, 14), (17, 15), (22, 13), (23, 14), (4, 16), (12, 17)):
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
    '..#####..',
    '.%%%%%%..',
    '.%%%%%%..',
]
LEG = pix.outline(put(shade(LEG_M, {'#': 'ABC', '%': 'SBC'}), [
    '', '', '', '', '', '',
    '....k',
    '....k',
]))
HLEG_M = [
    '..#######..',
    '.#########.',
    '###########',
    '###########',
    '.#########.',
    '...######..',
    '..%%%%%%...',
    '..%%%%%%...',
]
HLEG = pix.outline(put(shade(HLEG_M, {'#': 'ABC', '%': 'SBC'}), [
    '', '', '', '', '', '',
    '.....k',
    '.....k',
]))

# ---- 頭（大きく）：重い まゆ、2段の 赤い 目、長い 鼻と 平らな 鼻先 ----
HEAD_M = [
    "...#########.................",
    ".##############..............",
    "#################............",
    "###################..........",
    "####################.........",
    "######################.......",
    "########################.....",
    "##########################...",
    "##########################@@.",
    "##########################@@@",
    "##########################@@@",
    "##########################@@@",
    "##########################@@@",
    "##########################@@.",
    "##########&&&&&&&&&&&&&&&&...",
    ".#########&&&&&&&&&&&&&&.....",
    "..#######&&&&&&&&&&&&........",
    "....###&&&&&&&&&&............",
    ".......&&&&&&&...............",
]
EYES = {
    'open':  ['kk......', '.kkkkk..', '.kwEEkEk', 'kFFFFkFk', '.kkkkkk.'],
    'blink': ['kk......', '.kkkkk..', '.kBBBBBk', 'kkkkkkkk', '.kCCCCk.'],
    'hit':   ['kk......', '.kkkkk..', '.kEkkEkk', 'kkFkFkFk', '.kkkkkk.'],
    'glow':  ['kk......', '.kkkkk..', '.kwwEEEk', 'kEEEEkEk', '.kFFkFk.'],
    'ko':    ['........', '.kEFFEk.', '.kFkkFk.', '.kkFFkk.', '.kFkkFk.'],
}
def head(eye='open', mouth=False):
    g = pix.grid_of(shade(HEAD_M, {'#': 'ABC', '@': 'RSS', '&': 'BCC', '%': 'ABC'}, low=14))
    pix.stamp(g, EYES[eye], 8, 4)
    # 重い まゆの ひさし（前へ 下がる）と しわ
    for (x, y) in ((6, 3), (7, 3), (16, 6), (17, 6), (18, 7)): g[y][x] = 'k'
    for (x, y) in ((6, 2), (7, 2), (8, 2), (9, 2), (10, 3), (11, 3), (12, 3), (13, 4), (14, 4), (4, 1), (5, 1), (3, 2), (16, 3), (17, 4), (18, 4)): g[y][x] = 'A'
    for (x, y) in ((3, 6), (3, 7), (4, 8), (4, 9), (20, 9), (21, 10), (22, 9), (23, 10), (12, 10), (13, 11), (14, 10), (16, 11), (17, 12)): g[y][x] = 'C'
    for (x, y) in ((27, 10), (27, 11), (27, 12)): g[y][x] = 'k'            # 鼻の あな
    for (x, y) in ((26, 9), (26, 13)): g[y][x] = 'S'
    if mouth:   # 口を 大きく あける（歯を 見せる）
        for x in range(9, 27): g[14][x] = 'k'
        for x in range(10, 25): g[15][x] = 'l'
        for x in range(11, 22): g[16][x] = 'l' if x % 3 else 'w'
        for x in (13, 16, 19, 22, 25): g[14][x] = 'w'
    else:
        for x in range(11, 27): g[14 + (1 if x < 17 else 0)][x] = 'k'
        g[14][10] = 'k'; g[15][19] = 'w'; g[15][22] = 'w'; g[15][25] = 'w'
    return pix.outline(pix.rows_of(g))
HEAD = head()
# 首すじに かかる 苔の 毛布の はし（頭と 胴の つなぎ目）
NAPE = ['..kkkk....', '.kMMMNkk..', 'kMMNNNNNk.', 'kMNNNNOOk.', 'kNNNOONOk.', 'kNNOOkOk..', '.kOkkOk...', '.kk..k....']
EAR = pix.outline(['..AA', '.ABB', 'ABBC', 'ABCC', 'BBCC', 'BCC.'])
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
    g = pix.grid(36, 14)
    for (x, y) in ((0, 6), (5, 3), (19, 1), (25, 2), (30, 4)): pix.stamp(g, SPK, x, y)
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
        dict(n='hlegF', g='legB', x=10, y=50, rows=dark(HLEG)),
        dict(n='flegF', g='legB', x=33, y=50, rows=dark(LEG)),
        dict(n='crest', g='body', x=6, y=21, rows=CREST),
        dict(n='tree', g='tree', x=11, y=17, rows=TREE, alt={'idle1|idle2|walk1|walk3|atk1': TREE2}),
        dict(n='body', g='body', x=2, y=29, rows=BODY),
        dict(n='hleg', g='legA', x=4, y=50, rows=HLEG),
        dict(n='fleg', g='legA', x=28, y=50, rows=LEG),
        dict(n='ear', g='head', x=32, y=25, rows=EAR),
        dict(n='head', g='head', x=30, y=28, rows=HEAD, alt={'blink': head('blink'), 'hit': head('hit'), 'atk0': head('glow'), NB: head('glow', True), 'ko': head('ko')}),
        dict(n='nape', g='head', x=27, y=27, rows=NAPE),
        dict(n='tusk', g='head', x=49, y=29, rows=TUSK),
        dict(n='dust', g='fx', x=0, y=50, rows=DUST, only=NB),
        dict(n='clods', g='head', x=56, y=16, rows=CLODS, only='atk2'),
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
