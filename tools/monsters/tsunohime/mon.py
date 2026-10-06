# ツノヒメ（フェアリー・エスパー × ユニコーン）手打ち GBA風
META = dict(id='tsunohime', name='ツノヒメ', types=['fairy', 'psychic'], base='ユニコーン', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1e48',
    'F': '#7272c4', 'G': '#43428a', 'H': '#24224e',
    'C': '#fff0fa', 'P': '#ff7ad2', 'Q': '#a8389c',
    'S': '#ffe98e', 'T': '#d9a23c', 'U': '#8a5622',
    'E': '#6ef4ff', 'w': '#ffffff',
}
LIGHT = set('FCSEw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, lit=1, dk=2):
    H = len(spans); m = [[a <= x <= b for x in range(W)] for (a, b) in spans]
    def ins(y, x): return 0 <= y < H and 0 <= x < W and m[y][x]
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            du = next(i for i in range(1, 9) if not ins(y - i, x) or i == 8)
            dl = next(i for i in range(1, 9) if not ins(y, x - i) or i == 8)
            dd = next(i for i in range(1, 9) if not ins(y + i, x) or i == 8)
            dr = next(i for i in range(1, 9) if not ins(y, x + i) or i == 8)
            c = 'G'
            if dd <= dk: c = 'H'
            elif du <= lit or dl <= 1: c = 'F'
            elif dr <= 1: c = 'H'
            g[y][x] = c
    return g

# ---- 胴と 首（あたりの はばを 行ごとに）----
SPAN = [(36, 37), (33, 38), (32, 39), (31, 40), (31, 41), (30, 41), (30, 41), (30, 40), (29, 40), (29, 40), (28, 40), (28, 40),
        (10, 40), (8, 40), (6, 39), (4, 39), (3, 39), (3, 39), (2, 39), (2, 38), (2, 37), (2, 36), (3, 36), (3, 35), (4, 33),
        (6, 29), (8, 27), (10, 25)]
def body():
    g = shade(SPAN, 42, lit=2, dk=3)
    # 筋肉（肩・もも・首の すじ）を 手で
    for (x, y) in ((30, 14), (29, 15), (28, 16), (28, 17), (29, 18), (9, 15), (8, 16), (8, 17), (9, 18), (10, 19), (34, 6), (33, 8), (33, 10),
                   (16, 20), (17, 20), (18, 21), (22, 21), (23, 21), (36, 15), (36, 16)):
        if g[y][x] == 'G': g[y][x] = 'H'
    for (x, y) in ((31, 13), (30, 13), (31, 12), (10, 14), (11, 14), (6, 16), (5, 17), (35, 4), (34, 5), (20, 14), (21, 14), (22, 14)):
        if g[y][x] == 'G': g[y][x] = 'F'
    for x in range(13, 28):
        if g[14][x] == 'G' and 14 <= x <= 26: g[14][x] = 'F'
        if g[15][x] == 'G' and 17 <= x <= 23: g[15][x] = 'F'
        if g[21][x] == 'G' and 15 <= x <= 27: g[21][x] = 'H'
        if g[22][x] == 'G': g[22][x] = 'H'
    for (x, y) in ((8, 14), (7, 15), (6, 16), (6, 17), (32, 12), (33, 13), (34, 13), (35, 4), (36, 3), (34, 7), (33, 9)):
        if g[y][x] == 'G': g[y][x] = 'F'
    return [''.join(r) for r in _ol(g)]

# 頭：金の 面よろい（鼻すじ）、耳は 後ろへ
HEAD = [
    '...kk.............',
    '..kFGk............',
    '..kFGHk...........',
    '..kGGHkkkk........',
    '.kGGGkSSSTkk......',
    '.kGGkSSTTTTUk.....',
    'kGGkkkkkSTTTUk....',
    'kGGGGGGkkSTTUUk...',
    'kGGGGGGGGkSTTUUk..',
    'kFGGGGGGGGkSTTUUk.',
    '.kGGGGGGGGGkSTTUk.',
    '.kHGGGGGGGGGkTTUUk',
    '..kHGGGGGGGGGkUUUk',
    '...kHGGGGGGGGGkkHk',
    '....kHHGGGGGkkkkk.',
    '.....kHHHHkwkwkk..',
    '......kkHHHHHkk...',
    '........kkkkk.....',
]
EYE = ['wEEEk', 'kEEk.']
EYE_ALT = {'blink': ['kkkkk', 'GGGG.'], 'atk0|atk1|atk2': ['wwwEk', 'kwEk.'], 'hit': ['kEkkk', 'GkEk.'], 'ko': ['kGkGk', 'GkGk.']}
# 結晶の やり（ツノ）：ななめに 手で 打つ。らせんの きざみ つき
HORN = [
    '............kk',
    '...........kCk',
    '..........kCPk',
    '.........kCPQk',
    '........kCPQk.',
    '.......kCPQk..',
    '......kCCQk...',
    '.....kCPQk....',
    '....kCPQQk....',
    '...kCPPQk.....',
    '..kCCPQk......',
    '.kCPPQk.......',
    'kCPPQQk.......',
    'kkkkkk........',
]
HORN_HOT = [r.replace('P', 'C').replace('Q', 'P') for r in HORN]
# たてがみの かわりの 結晶の とげ
SHARD = [
    'k......',
    'kCk....',
    'kCPk...',
    'kCPPk..',
    'kCCPQk.',
    '.kCPQQk',
    '.kCPQQk',
    '..kPQk.',
    '...kk..',
]
SHARD_S = ['k...', 'kCk.', 'kPQk', '.kk.']
TAIL = [
    '......kkk.',
    '....kkCCPk',
    '...kCCPPQk',
    '..kCPPQQk.',
    '.kCPPQk...',
    'kCPPQk.kk.',
    'kCPQk.kCPk',
    'kPQk.kCPQk',
    'kPQk.kPQk.',
    '.kQk.kPQk.',
    '.kk..kQk..',
    '.....kk...',
]
PLATE = [
    '..kkkkk.....',
    '.kSSSSTkk...',
    'kSSTTTTUCk..',
    'kSTTTTUkCPk.',
    'kSTwETUkPQQk',
    'kSTEETUkCPk.',
    'kSTTTUUkPk..',
    '.kTTTUUkk...',
    '.kTTUUk.....',
    '..kUUk......',
    '...kk.......',
]
FLEG = [
    '.kkkkkk.',
    'kFFGGGHk',
    'kFGGGGHk',
    'kFGGGGHk',
    'kFGGGHHk',
    'kGGGGHHk',
    '.kGGGHHk',
    '.kGGGHk.',
    '.kFGGHk.',
    '..kGGHk.',
    '..kFGHk.',
    '..kGGHk.',
    '..kGHk..',
    '..kGHk..',
    '..kGHk..',
    '..kGHk..',
    '..kGHk..',
    '.kSSTUk.',
    '.kGGHHk.',
    '.kGGHHk.',
    '.kCPPQk.',
    'kCPPPQQk',
    'kkkkkkkk',
]
# 前足を 上げた 形（ため）
FLEG_UP = [
    '.kkkkk...',
    'kFGGGHk..',
    'kFGGGHHk.',
    'kFGGGHHk.',
    '.kGGGHHk.',
    '..kGGGHk.',
    '...kGGHk.',
    '...kGGHk.',
    '..kGGHk..',
    '.kGGHk...',
    'kSSTUk...',
    'kCPQk....',
    'kPQk.....',
    'kkk......',
]
HLEG = [
    '..kkkkkk...',
    '.kFFGGGGkk.',
    'kFFGGGGGGHk',
    'kFGGGGGGGHk',
    'kFGGGGGGGHk',
    'kGGGGGGGHHk',
    'kGGGGGGGHHk',
    '.kGGGGGHHk.',
    '.kGGGGHHk..',
    '.kGGGGHk...',
    'kGGGGHk....',
    'kFGGHk.....',
    '.kGGHk.....',
    '.kGGHk.....',
    '..kGHk.....',
    '..kGHk.....',
    '..kGHk.....',
    '..kGHk.....',
    '.kSSTUk....',
    '.kGGHHk....',
    '.kCPPQk....',
    'kCPPPQQk...',
    'kkkkkkkk...',
]
MOTE = ['.k.', 'kCk', 'kPk', '.k.']
BURST = [
    '......C......',
    '......C......',
    '..P...C...P..',
    '...P..P..P...',
    '....P.C.P....',
    '.....CwC.....',
    'CCPPCwwwCPPCC',
    '.....CwC.....',
    '....P.C.P....',
    '...P..P..P...',
    '..P...C...P..',
    '......C......',
    '......C......',
]
BURST2 = [
    '...P.....P...',
    '.............',
    'P....PCP....P',
    '....P...P....',
    '...P.....P...',
    '..C...w...C..',
    '..P..www..P..',
    '..C...w...C..',
    '...P.....P...',
    '....P...P....',
    'P....PCP....P',
    '.............',
    '...P.....P...',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'C': 'P', 'P': 'Q'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=27, rows=TAIL),
        dict(n='legHF', g='legB', x=16, y=37, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=33, y=38, rows=dark(FLEG)),
        dict(n='sh1', g='neck', x=33, y=8, rows=SHARD),
        dict(n='sh2', g='neck', x=31, y=13, rows=SHARD),
        dict(n='sh3', g='neck', x=30, y=18, rows=SHARD),
        dict(n='sh4', g='body', x=28, y=23, rows=SHARD),
        dict(n='body', g='body', x=7, y=15, rows=BODY),
        dict(n='plate', g='body', x=41, y=27, rows=PLATE),
        dict(n='legH', g='legA', x=9, y=38, rows=HLEG),
        dict(n='legF', g='legB', x=38, y=38, rows=FLEG, alt={'atk0': FLEG_UP}),
        dict(n='head', g='head', x=41, y=10, rows=HEAD),
        dict(n='eye', g='head', x=45, y=17, rows=EYE, alt=EYE_ALT),
        dict(n='horn', g='head', x=46, y=1, rows=HORN, alt={'atk0|atk1|atk2': HORN_HOT}),
        dict(n='m1', g='m1', x=24, y=6, rows=MOTE),
        dict(n='m2', g='m2', x=2, y=14, rows=MOTE),
        dict(n='m3', g='m3', x=58, y=30, rows=MOTE, not_='atk1|atk2'),
        dict(n='burst', g='head', x=53, y=-5, rows=BURST, alt={'atk2': BURST2}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'idle2': {'body': (0, 1), 'm1': (0, -2), 'm2': (0, 2), 'm3': (0, -2)},
    'idle3': {'body': (0, 1), 'head': (0, 0), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'm1': (0, -1)},
    'walk1': {'body': (0, -1), 'm2': (0, 1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'm1': (0, -1)},
    'walk3': {'body': (0, -1), 'm2': (0, 1)},
    'atk0': {'body': (-2, 0), 'head': (-1, 2), 'legB': (2, -2), 'm1': (8, 2), 'm2': (14, -2)},
    'atk1': {'root': (6, 0), 'head': (2, 3), 'legB': (3, 0), 'm1': (14, 4), 'm2': (30, 0)},
    'atk2': {'root': (8, 0), 'head': (2, 2), 'm1': (6, 0), 'm2': (10, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'm1': (-2, 2), 'm2': (1, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'neck', 'neck': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'm1': 'root', 'm2': 'root', 'm3': 'root'}
