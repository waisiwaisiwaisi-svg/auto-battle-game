# ユキオニ（こおり・かくとう × イエティ）手打ち GBA風
from pix import outline, flip_h
META = dict(id='yukioni', name='ユキオニ', types=['ice', 'fighting'], base='イエティ', size='L')
PAL = {
    'k': '#101018', 'l': '#26304e',
    'A': '#f4f8ff', 'B': '#aebfe0', 'C': '#5e6fa4',      # 毛皮
    'D': '#4c5896', 'E': '#2c3266',                      # 鬼の はだ（顔・むね）
    'I': '#e4ffff', 'J': '#86dcf2', 'K': '#3a8ec6',      # 氷
    'R': '#ff3c3c', 'O': '#ffc23a', 'w': '#ffffff',
}
LIGHT = set('AIw')
KEEP_BLACK = set('wRO')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'I': 'J', 'J': 'K'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=40, H=44):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

BODY = [
    ".....AAAAAAAAAAAAAAAAA.......",
    "...AAAAAABBBBAAAABBBBAAA.....",
    "..AAABBBBBBBBBBBBBBBBBBBBA...",
    ".AAABBBBACBBBBBBACBBBBBBBBC..",
    ".AABBBBBBCBBBBBBBCBBBBBBBBCC.",
    "AABBBACBBBBBBACBBBBBBBBBBBCC.",
    "AABBBBCBBBBBBBCBBBBBBBBBBCCC.",
    "ABBBBBBBBBACBBBBBBBACBBBBCCC.",
    "ABBBBBBBBBBCBBBBBBBBCBBBCCCC.",
    "ABBACBBBBBBBBBBBBBBBBBBBCCCC.",
    "ABBBCBBBBBBBACBBBBBBBBBCCCC..",
    ".ABBBBBBBBBBBCBBBBBBBBCCCCC..",
    ".ABBBBBACBBBBBBBBBBBBCCCCCC..",
    ".ABBBBBBCBBBBBBBBBBBCCCCCC...",
    "..ABBBBBBBBBBBBBBBBCCCCCCC...",
    "..ABBBBBBBBBBBCBBBCCCCCCC....",
    "..ABBBBBBBBBBBBCBCCCCCCCC....",
    "...BBBBBBBBBBBBBCCCCCCCC.....",
    "...BBBBBBBBBBBBCCCCCCCCC.....",
    "...CBBBBBBBBBCCCCCCCCCC......",
    "...CCBCBBCBCCCCCCCCCC........",
    "....C.CC.CC.CC.CC............",
]
HEAD = [
    ".....AAAAAAA..........",
    "...AAABBBBBBAAA.......",
    "..AABBBBBBBBBBBA......",
    ".AABBBBBBBBBBBBBA.....",
    "AABBBBBBBEEEEEEEEE....",
    "ABBBBBBBEEEEEEEEEEEE..",
    "ABBBBBBEDDDDDDDDDDDDE.",
    "ABBBBBEDDDDDDDDDDDDDDE",
    "BBBBBBEDDDDDDDDDDDDDDD",
    "BBBBBBEDDDDDDDDDDDDDEE",
    "BBBBBBEDDDDDDDDDDDDDE.",
    "BBBBBBEDDkkkkkkkkkkkk.",
    "BBBBBBEDkwDDDDDDDwDk..",
    ".BBBBBEDDwDDDDDDDwDE..",
    ".BBBBBBEDDDDDDDDDDDE..",
    "..CBBBBBEEEEEEEEEEE...",
    "...CCCCBBBBB..........",
]
HEAD_ROAR = [
    ".....AAAAAAA..........",
    "...AAABBBBBBAAA.......",
    "..AABBBBBBBBBBBA......",
    ".AABBBBBBBBBBBBBA.....",
    "AABBBBBBBEEEEEEEEE....",
    "ABBBBBBBEEEEEEEEEEEE..",
    "ABBBBBBEDDDDDDDDDDDDE.",
    "ABBBBBEDDDDDDDDDDDDDDE",
    "BBBBBBEDDDDDDDDDDDDDDD",
    "BBBBBBEDDDDDDDDDDDDDEE",
    "BBBBBBEDkkkkkkkkkkkkk.",
    "BBBBBBEkwkwkkkkkwkwk..",
    "BBBBBBEkRRRRRRRRRRk...",
    ".BBBBBEkwkkkkkkkwwk...",
    ".BBBBBBEwDDDDDDDwDE...",
    "..CBBBBBEEEEEEEEEEE...",
    "...CCCCBBBBB..........",
]
EYE = ['kkkk...', 'EkkkkkE', '.kRROwk', '..kkkk.']
EYE_ALT = {'blink': ['kkkk...', 'EkkkkkE', '.Ekkkkk', '..EEEE.'], 'hit': ['..kk...', 'EkRkkk.', '.kkkRRk', '..kkkk.'],
           'atk0|atk1|atk2': ['kkkk...', 'EkkkkkE', '.kOwwwk', '..kkkk.'], 'ko': ['.k...k.', '..k.k..', '...k...', '..k.k..']}
HORN = ['.I..', '.IJ.', 'IIJ.', 'IJJ.', 'IJK.', 'IJJK', 'IJJK', 'IJKK', 'IJKK']
HORN2 = ['I...', 'IJ..', 'IJJ.', 'IJK.', 'IJKK', 'IJKK']
ICEFIST = [
    "....I..I....I...",
    "...IJ.IJK..IJ...",
    "..IIJJIJJKIIJK..",
    ".IIJJJJJJJJJJJK.",
    "IIJJIIJJJJJJJKKK",
    "IJJIJJJJIJJJKKKK",
    "IJIJJJJIJJJJKKKK",
    "IJJJJJIJJJJKKKKK",
    ".JJJJIJJJJKKKKKK",
    ".KJJJJJJJKKKKKK.",
    "..KKJJJKKKKKKK..",
    "....KKKKKKKK....",
]
ARM = [
    "..AAAAAA....",
    ".AABBBBBAA..",
    "AABBBBBBBBC.",
    "ABBBBBBBBBCC",
    "ABBBCBBBBBCC",
    "ABBBBBBBBCCC",
    ".ABBBBBBBCCC",
    ".ABBBBCBBCCC",
    ".ABBBBBBBCCC",
    "..ABBBBBBCC.",
    "..ABBCBBBCC.",
    "..ABBBBBCCC.",
    "..ABBBBBCC..",
    ".AABBBBBCC..",
    "ABABBABBCBC.",
    ".B.C.B.C.C..",
]
ARMS = {
    'base': place([(outline(ARM), 0, 0), (outline(ICEFIST), 3, 15)]),
}
# 攻撃：こぶしを 頭の 上へ ふりあげ（ため）→ 前へ たたきつける
ARM_UP = [
    "...........AAAA",
    ".........AABBBB",
    ".......AABBBBBC",
    ".....AABBBBBBC.",
    "...AABBBBBBBC..",
    "..ABBBBBBBBC...",
    ".ABBBBBBBCC....",
    "ABBBBBBBCC.....",
    "ABBBBBCC.......",
    "ABBBCC.........",
    "BCCC...........",
]
ARM_SLAM = [
    "..AAAAAAAAA.......",
    ".AABBBBBBBBAAA....",
    "AABBBBBBBBBBBBAA..",
    "ABBBBBBBBBBBBBBBA.",
    "ABBBBBBBBBBBBBBBBC",
    ".ABBBBBBBBBBBBBBCC",
    "..CCBBBBBBBBBBBCC.",
    "....CCCCCCCCCCC...",
]
ARMS['atk0'] = place([(outline(ICEFIST), 8, 0), (outline(ARM_UP), 0, 11)])
ARMS['slam'] = place([(outline(ARM_SLAM), 0, 2), (outline(ICEFIST), 14, 4)])
LEG = [
    "AABBBBBBBBA..",
    "ABBBBBBBBBCC.",
    "ABBCBBBBBBCC.",
    "ABBBBBBBCBCC.",
    "ABBBBBBBBCCC.",
    ".ABBBBCBBCCC.",
    ".ABBBBBBBCC..",
    ".ABBCBBBBCC..",
    ".BCBBCBBCCC..",
    ".CEDDDDDDDE..",
    "..EDDDDDDDDEw",
    ".EDDEDDEDDDEw",
    ".EEEEEEEEEEE.",
]
SHARDS = [
    "....k.........k.....",
    "...kIk.......kIk....",
    "...kJk..k...kIJk....",
    "..kIJKkkIk..kJKk..k.",
    "..kJJKkIJk.kIJKk.kIk",
    ".kIJKKkJKk.kJKKkkIJk",
    "kkkkkkkkkkkkkkkkkkkk",
]
SNOW = ['.k.', 'kAk', '.k.']

def base():
    return [
        dict(n='legB', g='legB', x=13, y=46, rows=outline(dk(LEG))),
        dict(n='armB', g='armB', x=-19, y=22, rows=flip_h(dk(ARMS['base']))),
        dict(n='body', g='body', x=10, y=20, rows=outline(BODY)),
        dict(n='legA', g='legA', x=26, y=46, rows=outline(LEG)),
        dict(n='armUp', g='armF', x=38, y=22, rows=ARMS['atk0'], only='atk0'),
        dict(n='horn2', g='head', x=33, y=4, rows=outline(HORN2)),
        dict(n='head', g='head', x=29, y=9, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_ROAR)}),
        dict(n='horn', g='head', x=40, y=0, rows=outline(HORN)),
        dict(n='eye', g='head', x=37, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=38, y=22, rows=ARMS['base'], alt={'atk1|atk2': ARMS['slam']}, not_='atk0'),
    ]
def fx():
    return [
        dict(n='shards', g='root', x=50, y=54, rows=SHARDS, only='atk1|atk2'),
        dict(n='snow1', g='root', x=8, y=12, rows=SNOW, only='idle1|idle2'),
        dict(n='snow2', g='root', x=52, y=8, rows=SNOW, only='idle2|idle3'),
    ]
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        if l.get('only'): continue
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
    return [l if l.get('only') else dict(l, not_=(l.get('not_', '') + '|ko').strip('|')) for l in base()] + fx() + [dict(n='ko', g='root', x=0, y=61 - len(ko), rows=ko, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (0, 0)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (-7, -25), 'armB': (1, -2)},
    'atk1': {'root': (4, 0), 'body': (1, 3), 'armF': (0, 14), 'armB': (2, 1), 'head': (1, 1)},
    'atk2': {'root': (5, 0), 'body': (1, 4), 'armF': (0, 15), 'armB': (2, 2), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'armF': (-2, -1)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
