# ハガマ（くさ・むし × カマキリ）手打ち GBA風
from pix import outline
META = dict(id='hagama', name='ハガマ', types=['grass', 'bug'], base='カマキリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2e2014',
    'A': '#d2a874', 'B': '#8c6038', 'C': '#4e3220',      # 樹皮の よろい
    'G': '#c4ee6a', 'H': '#5cb444', 'J': '#246a3a',      # 葉の 鎌
    'O': '#ff9a3c', 'R': '#d02c2c', 'Y': '#fff07a',      # 複眼
    'w': '#ffffff',
}
LIGHT = set('AGYw')
KEEP_BLACK = set('wOY')
DK = {'A': 'B', 'B': 'C', 'G': 'H', 'H': 'J'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=40, H=40):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

THORAX = [
    ".......ABBC",
    "......ABBCC",
    "......ABBC.",
    ".....ABBCC.",
    ".....ABBC..",
    "....AABBCC.",
    "...ABBBBBBC",
    "...ABCCCBBC",
    "..ABBBBBBBC",
    "..ABBBBBBCC",
    "..ACCCCBBC.",
    "..ABBBBBBC.",
    ".ABBBBBBBCC",
    ".ACCCCBBBC.",
    ".ABBBBBBBC.",
    "ABBBBBBBBCC",
    "ABBBBBBBBBC",
    ".CBBBBBBCC.",
    "..CCCCCCC..",
]
# 背中の とげ（手で 置く）
THORNS = ['k....', 'Ak...', '.....', '.....', '.....', 'k....', 'Ak...']
ABD = [
    "..........GGGGGGHH....",
    ".......GGGHHHHHHHHHH..",
    ".....GGHHHHJHHHHHHHHHH",
    "...GGHHHHJHHHHJHHHHHHJ",
    ".GGHHJJJJJJJJJJJJJJJJJ",
    "GHHHHHHHJHHHHHJHHHHHJJ",
    ".HHHHHHJHHHHHJHHHHHJJ.",
    "..JHHHHHHHHHHHHHHJJJ..",
    "....JJHHHHHHHHJJJJ....",
    "......JJJJJJJJJ.......",
]
HEAD = [
    "...AAAAAA.....",
    "..ABBBBBBAA...",
    ".ABBBBBBBBBA..",
    "ABBBBBBBBBBBB.",
    "ABBBBBBBBBBBBC",
    ".ABBBBBBBBBBC.",
    "..CBBBBBBBBC..",
    "...CBBBBBBBC..",
    "....CBBBBBCw..",
    ".....CBBBkw...",
    "......Ckw.....",
]
EYE = ['kkkk....', 'kOOOkkk.', 'kOYOOROk', 'kOOkRRRk', '.kRRRRk.', '..kkkk..']
EYE_ALT = {'blink': ['kkkk....', 'kCCCkkk.', 'kkkkkkkk', '.kCCCCk.', '..kkkk..', '........'],
           'hit': ['.kkk....', 'kOkOkk..', 'kkOkROk.', 'kOkRkRk.', '.kkkkk..', '........'],
           'atk0|atk1|atk2': ['kkkk....', 'kYYYkkk.', 'kYwYYOYk', 'kYYkOOOk', '.kOOOOk.', '..kkkk..'],
           'ko': ['........', '.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..']}
CREST = ['GG........', 'GHHG......', '.JHHHG....', '..JHHHHG..', '...JJHHHHG', '.....JJJHH']
ANT = ['.........kkk', '......kkk...', '....kk......', '..kk........', 'kk..........']
ARM = [
    ".....AAk..............",
    "....ABBCGGGGG.........",
    "...ABBCGGGHHHHHG......",
    "...ABCGGHHHHHHHHHG....",
    "..ABBCHHHJJJJHHHHHH...",
    "..ABCCJJJ....JJHHHHH..",
    ".ABBC..........JHHHHH.",
    ".ABCC.........wJHHHHH.",
    "ABBC...........JHHHHJ.",
    "ABCC..........wJHHHHJ.",
    "CCC............JHHHJ..",
    "..............wJHHHJ..",
    "...............JHHJ...",
    "..............wJHJ....",
    "...............JHJ....",
    "...............JJ.....",
    "...............J......",
]
ARM_SWING = [
    "............AAk.......",
    "AAAAAAAAAAABBBCGGGG...",
    "BBBBBBBBBBBBBCCHHHHHG.",
    "CCCCCCCCCCCCCJJJHHHHHH",
    "...............JHHHHHH",
    "..............wJHHHHH.",
    "...............JHHHHJ.",
    "..............wJHHHJ..",
    "...............JHHHJ..",
    "..............wJHHJ...",
    "...............JHJ....",
    "...............JJ.....",
    "...............J......",
]
LEG = [
    "ABBC......",
    "ABBCC.....",
    ".ABBC.....",
    ".ABBCC....",
    "..ABBC....",
    "..ABBC....",
    "...ABBC...",
    "...ABBCk..",
    "...ABBC...",
    "..ABBC....",
    "..ABC.....",
    "..ABC.....",
    ".ABBC.....",
    ".ABC......",
    ".ABC......",
    "ABBC......",
    "ABC.......",
    "ABC.......",
    "ABC.......",
    "ABBBBBCw..",
    "CCCCCCC...",
]
# 葉の 斬撃（三日月）と 舞う 葉
SLASH = [
    ".....kkkk.........",
    "...kkGGGGkk.......",
    "..kGGkkkGGGk......",
    ".kGk.....kHGk.....",
    ".kk.......kHGk....",
    "...........kHGk...",
    "............kHHk..",
    "............kHHk..",
    "...........kHHJk..",
    "..........kHJJk...",
    "........kkJJk.....",
    "......kkkkk.......",
]
LEAF1 = ['.kk.', 'kGHk', 'kHJk', '.kk.']
LEAF2 = ['..kk', '.kGk', 'kHJk', 'kk..']

def base():
    return [
        dict(n='armB', g='armB', x=20, y=15, rows=outline(dk(ARM)), alt={'atk1|atk2': outline(dk(ARM_SWING))}),
        dict(n='abd', g='tail', x=1, y=31, rows=outline(ABD)),
        dict(n='legB', g='legB', x=12, y=36, rows=outline(dk(LEG))),
        dict(n='thorax', g='body', x=19, y=17, rows=outline(THORAX)),
        dict(n='thorns', g='body', x=22, y=22, rows=THORNS),
        dict(n='legA', g='legA', x=23, y=37, rows=outline(LEG)),
        dict(n='crest', g='head', x=20, y=3, rows=outline(CREST)),
        dict(n='ant', g='head', x=39, y=5, rows=ANT),
        dict(n='head', g='head', x=27, y=8, rows=outline(HEAD)),
        dict(n='eye', g='head', x=33, y=9, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=24, y=18, rows=outline(ARM), alt={'atk1': outline(ARM_SWING), 'atk2': outline(ARM_SWING)}),
    ]
def fx():
    return [
        dict(n='slash', g='root', x=43, y=13, rows=SLASH, only='atk1'),
        dict(n='leaf1', g='root', x=56, y=30, rows=LEAF1, only='atk1|atk2'),
        dict(n='leaf2', g='root', x=62, y=20, rows=LEAF2, only='atk2'),
        dict(n='leaf3', g='root', x=52, y=40, rows=LEAF2, only='atk2'),
    ]
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if 'ko' in k.split('|'): rows = v
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[l['y'] + j][l['x'] + i] = c
    ys = [y for y in range(70) if any(c != '.' for c in g[y])]; xs = [x for x in range(80) if any(g[y][x] != '.' for y in range(70))]
    g = [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
    h, w = len(g), len(g[0])
    return [''.join(g[y][w - 1 - x] for y in range(h)) for x in range(w)]
def layers():
    ko = knocked()
    return [dict(l, not_='ko') for l in base()] + fx() + [dict(n='ko', g='root', x=4, y=61 - len(ko), rows=ko, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'tail': (0, -1)}, 'idle2': {'body': (0, 1), 'tail': (-1, -1), 'armF': (0, -1)}, 'idle3': {'armF': (0, -1), 'tail': (-1, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (-5, -2), 'armB': (-5, -3)},
    'atk1': {'root': (5, 0), 'body': (1, 1), 'armF': (1, 6), 'armB': (4, 6)},
    'atk2': {'root': (6, 0), 'body': (1, 2), 'armF': (1, 11), 'armB': (4, 10)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 1)},
    'ko': {},
}
PARENT = {'tail': 'body', 'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
