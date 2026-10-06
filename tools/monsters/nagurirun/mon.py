# ナグリルー（かくとう × カンガルー）手打ち GBA風
from pix import outline
META = dict(id='nagurirun', name='ナグリルー', types=['fighting'], base='カンガルー', size='M')
PAL = {
    'k': '#101018', 'l': '#40201a',
    'A': '#f2ac62', 'B': '#c46a32', 'C': '#7c3820',      # 毛（赤茶）
    'E': '#f6e0b4', 'F': '#cca474',                      # はら・耳の 内がわ
    'R': '#f44a44', 'S': '#a4243a',                      # 拳闘の グローブ
    'G': '#c4c4d4', 'H': '#6c6c80',                      # 鉄の びょう・石
    'Y': '#ffe23a', 'w': '#ffffff',
}
LIGHT = set('AERGYw')
KEEP_BLACK = set('wY')
DK = {'A': 'B', 'B': 'C', 'E': 'F', 'R': 'S', 'G': 'H'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=40, H=30):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

HEAD = [
    "....AAAAAA..........",
    "..AABBBBBBAA........",
    ".ABBBBBBBBBBAA......",
    "ABBBBBBBBBBBBBAAA...",
    "ABBBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBkk",
    "ABBBBBBBBBBBBBBBBkkk",
    "BBBBBBBBBBBBBBBBBBC.",
    "BBBBBBBEEEEEEkkkkkk.",
    "CBBBBBEEEEEkwkwEEC..",
    ".CBBBBEEEEEEEEEEC...",
    "..CBBBBEEEEEEEFC....",
    "...CCBBBFFFFFCC.....",
    ".....CCCCCCC........",
]
HEAD_YELL = [
    "....AAAAAA..........",
    "..AABBBBBBAA........",
    ".ABBBBBBBBBBAA......",
    "ABBBBBBBBBBBBBAAA...",
    "ABBBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBkk",
    "ABBBBBBBBBBBBBBBBkkk",
    "BBBBBBBBBBBBBBBBBBC.",
    "BBBBBBBEEEkkkkkkkkk.",
    "CBBBBBEEEkwkkkkwkk..",
    ".CBBBBEEEkSSSSSSk...",
    "..CBBBBEEEkwkkwk....",
    "...CCBBBFFFkkkC.....",
    ".....CCCCCCC........",
]
EYE = ['kkE....', 'kkkEk..', 'kYYEYk.', '.kkkE..']
EYE_ALT = {'blink': ['kk.....', 'kkkkk..', 'BkkkkkB', '.BBBB..'], 'hit': ['..k....', '.kkkk..', 'kYkkYk.', '.kkkk..'],
           'atk0|atk1|atk2': ['kkE....', 'kkkEk..', 'kwYEwk.', '.kkkE..'], 'ko': ['.......', 'k...k..', '.k.k...', '..k....']}
EAR = [
    "A.......",
    "AA......",
    "ABA.....",
    "ABFA....",
    ".BFFA...",
    ".BFFFB..",
    ".CBFFBC.",
    "..CBFFBC",
    "...CBBBC",
    "....CCC.",
]
BODY = [
    "......AAAAAAAA........",
    "....AABBBBBBBBAA......",
    "...ABBBBBBBBBBBBA.....",
    "..ABBBBBBBBBBBEEEA....",
    "..ABBBBBBBBBBEEEEEB...",
    ".ABBBBBBBBBBEEEEEEEB..",
    ".ABBBBBBBBBBEEFFEEEEC.",
    ".ABBBBBBBBBBEEEEEEEEC.",
    "ABBBBBBBBBBEEEFFEEEEC.",
    "ABBBBBBBBBBEEEEEEEEEC.",
    "ABBBBBBBBBBEEEEEEEEEC.",
    "ABBBBBBBBBBEEEEGGEEEFC",
    "ABBBBBBBBBEEEEGGGHEEFC",
    "ABBBBBBBBBEFFFHHHFFFFC",
    "ABBBBBBBBBEEEEEEEEEEFC",
    "ABBBBBBBBBEEFEEEEEEFFC",
    "ABBBBBBBBBEEEEEEEEFFC.",
    "BBBBBBBBBBEEEEEEEFFC..",
    "BBBBBBBBBCFEEEEEFFCC..",
    "CBBBBBBBCCFFFFFFFCC...",
    ".CCBBBBCCCCCCCCCC.....",
    "...CCCCCC.............",
]
LEG = [
    "...AAAAAA...............",
    ".AABBBBBBAA.............",
    "ABBBBBBBBBBA............",
    "ABBBBBBBBBBBA...........",
    "ABBBBBBBBBBBC...........",
    "ABBBBBBBBBBBC...........",
    "ABBBBBBBBBBCC...........",
    ".ABBBBBBBBCC............",
    ".ABBBBBBBCC.............",
    "..ABBBBBCC..............",
    "...ABBBBC...............",
    "...ABBBC................",
    "....ABBC................",
    "....ABBC................",
    "....ABBBC...............",
    "....ABBBBAAAAAAAAAA.....",
    "....ABBBBBBBBBBBBBBBBA..",
    "....CBBBBBBBBBBBBBBBBBBw",
    ".....CCCCCCCCCCCCCCCCCCw",
]
TUFT = ['A..A..', 'AA.AA.', 'ABAABA', 'BBBBBC']
TAIL = [
    "..................ABBB",
    "................ABBBBB",
    "..............ABBBBBBC",
    "............ABBBBBBBC.",
    "..........ABBBBBBBCC..",
    "........ABBBBBBBCC....",
    "......ABBBBBBBCC......",
    ".....ABBBBBBCC........",
    "....ABBBBBCC..........",
    "...ABBBBCC............",
    "..ABBBCC..............",
    ".ABBCC................",
    "ABCC..................",
]
GLOVE = [
    "..RRRRR...",
    ".RwRRRRRS.",
    "RRRRRRRRSS",
    "RRRRRRRRSS",
    "RRRRRRRSSS",
    "SRRRRRSSSS",
    ".SSSSSSSS.",
    "..GHGHG...",
]
ARM = [
    "AAB.........",
    "ABBC........",
    "ABBBC.......",
    ".ABBBC......",
    "..ABBBC.....",
    "...ABBBAAAA.",
    "....ABBBBBBC",
    ".....CCCCCC.",
]
ARM_PUNCH = [
    "AAAAAAAAAAAAAAA",
    "ABBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBBC",
    "CCCCCCCCCCCCCC.",
]
ARMS = {
    'base': place([(outline(ARM), 0, 4), (outline(GLOVE), 11, 0)]),
    'punch': place([(outline(ARM_PUNCH), 0, 8), (outline(GLOVE), 15, 5)]),
}
IMPACT = [
    "....k.....",
    "...kYk..k.",
    "k.kYwYkkYk",
    "kYkwwwYYk.",
    ".kYwwwwYk.",
    "kYYwwwYkk.",
    ".kkYwYkYk.",
    "..kYk.k.k.",
    "...k......",
]
SWEAT = ['.k.', 'kwk', 'kGk', '.k.']

def base():
    return [
        dict(n='armB', g='armB', x=35, y=15, rows=dk(ARMS['base']), alt={'atk2': dk(ARMS['punch'])}),
        dict(n='earB', g='head', x=29, y=2, rows=outline(dk(EAR))),
        dict(n='tail', g='tail', x=2, y=46, rows=outline(TAIL)),
        dict(n='legB', g='legB', x=12, y=40, rows=outline(dk(LEG))),
        dict(n='body', g='body', x=18, y=20, rows=outline(BODY)),
        dict(n='legA', g='legA', x=16, y=40, rows=outline(LEG)),
        dict(n='tuft', g='head', x=31, y=6, rows=outline(TUFT)),
        dict(n='ear', g='head', x=26, y=3, rows=outline(EAR)),
        dict(n='head', g='head', x=28, y=8, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_YELL)}),
        dict(n='eye', g='head', x=37, y=10, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=32, y=22, rows=ARMS['base'], alt={'atk1': ARMS['punch']}),
    ]
def fx():
    return [dict(n='impact', g='root', x=61, y=24, rows=IMPACT, only='atk1')]
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        rows = l['rows']
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.' and 0 <= l['y'] + j < 70: g[l['y'] + j][l['x'] + i] = c
    ys = [y for y in range(70) if any(c != '.' for c in g[y])]; xs = [x for x in range(80) if any(g[y][x] != '.' for y in range(70))]
    g = [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
    h, w = len(g), len(g[0])
    return [''.join(g[y][w - 1 - x] for y in range(h)) for x in range(w)]
def layers():
    ko = knocked()
    return [dict(l, not_='ko') for l in base()] + fx() + [dict(n='ko', g='root', x=0, y=61 - len(ko), rows=ko, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (1, 0)}, 'idle2': {'body': (0, 1), 'armB': (0, 1)}, 'idle3': {'armF': (1, 0)},
    'blink': {},
    'walk0': {'legA': (2, -2), 'legB': (0, 0), 'body': (1, -1)}, 'walk1': {'body': (0, -2), 'legA': (0, -1), 'legB': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'armF': (-7, 1), 'armB': (-2, 0), 'tail': (1, 1), 'head': (-1, 0)},
    'atk1': {'root': (4, 0), 'body': (2, 0), 'armF': (0, 0), 'armB': (-3, 1)},
    'atk2': {'root': (5, 0), 'body': (2, 0), 'armF': (-6, 2), 'armB': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-3, 2)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
