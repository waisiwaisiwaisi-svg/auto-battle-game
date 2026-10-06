# サンガンエン（エスパー・かくとう × 三つ目の 猿）手打ち GBA風
from pix import outline
META = dict(id='sanganen', name='サンガンエン', types=['psychic', 'fighting'], base='三つ目の 猿', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1c48',
    'A': '#b08ee6', 'B': '#6e50b0', 'C': '#3c2a6c',      # 毛（むらさき）
    'D': '#f4cc94', 'E': '#bc8650',                      # 顔・むね・手
    'S': '#f0b834', 'T': '#a8661e',                      # 帯（こがね）
    'P': '#ff74dc', 'Q': '#b42c9e',                      # 念力の 光
    'Y': '#ffe84a', 'w': '#ffffff',
}
LIGHT = set('ADSPYw')
KEEP_BLACK = set('wYP')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'S': 'T'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

HEAD = [
    "......A..A........",
    "....AAA.AAA.A.....",
    "...ABBAABBAAB.....",
    "..ABBBBBBBBBBA....",
    ".ABBBBBBBBBBBBA...",
    "ABBBBBBBDDDDDDBA..",
    "ABBBBBBDDDDDDDDDA.",
    "ABDDBBDDDDDDDDDDD.",
    "BDDEBBDDDDDDDDDDDE",
    "BDEEBBDDDDDDDDDDDE",
    "BBEBBBEDDDDDDDDDE.",
    "BBBBBBEDDkkkkkkkk.",
    ".BBBBBBEDkwDDwkE..",
    ".CBBBBBEEDDDDDE...",
    "..CCBBBBEEEEEE....",
    "....CCCCCC........",
]
HEAD_SHOUT = [
    "......A..A........",
    "....AAA.AAA.A.....",
    "...ABBAABBAAB.....",
    "..ABBBBBBBBBBA....",
    ".ABBBBBBBBBBBBA...",
    "ABBBBBBBDDDDDDBA..",
    "ABBBBBBDDDDDDDDDA.",
    "ABDDBBDDDDDDDDDDD.",
    "BDDEBBDDDDDDDDDDDE",
    "BDEEBBDDDDDDDDDDDE",
    "BBEBBBEDDkkkkkkkk.",
    "BBBBBBEDkwkkkkwk..",
    ".BBBBBBEkQQQQQk...",
    ".CBBBBBEkwkkwk....",
    "..CCBBBBEEEEEE....",
    "....CCCCCC........",
]
EYES = ['kkkk..kkk', 'wYYk.wYk.', '.kkk..kk.']
EYES_ALT = {'blink': ['kkkk..kkk', 'EEEk.EEk.', '.........'], 'hit': ['.kkk..kk.', 'kYkYk.kYk', '.kkk...k.'],
            'atk0|atk1|atk2': ['kkkk..kkk', 'wwwk.wwk.', '.kkk..kk.'], 'ko': ['k.k...k.k', '.k.....k.', 'k.k...k.k']}
EYE3 = ['.k.', 'kPk', 'kwk', 'kQk', '.k.']
EYE3_ALT = {'blink': ['...', 'kkk', 'kQk', 'kkk', '...'], 'atk0|atk1|atk2': ['kPk', 'Pwk', 'www', 'kwP', 'kPk'], 'ko': ['...', 'kkk', 'kQk', 'kkk', '...']}
BODY = [
    ".....AAAAAAA......",
    "...AABBBBBBBAA....",
    "..ABBBBBBBDDDBA...",
    ".ABBBBBBBDDDDDDB..",
    ".ABBBBBBDDDDDDDDC.",
    "ABBBBBBBDDDEDDDDC.",
    "ABBBBBBBDDDDDDDDC.",
    "ABBBBBBBDDDEEDDDC.",
    "ABBBBBBBDDDDDDDC..",
    "ABBBBBBBEDDEEDDC..",
    "ABBBBBBBEDDDDDEC..",
    "SSSSSSSSSSSSSSST..",
    "STSSSSTSSSSSSSTT..",
    "TTTTTTTTTTTTTTTT..",
    "ABBBBBBBBBBBBBCC..",
    "ABBBBBBBBBBBBCC...",
    ".CBBBBBBBBBBCC....",
    "..CCCCCCCCCC......",
]
SASH = ['SS', 'ST', 'ST', 'TT', '.T']
LEG = [
    "..AAAAA....",
    ".ABBBBBBA..",
    "ABBBBBBBBC.",
    "ABBBBBBBBC.",
    ".ABBBBBBBC.",
    "..ABBBBBCC.",
    "...ABBBBC..",
    "...ABBBBC..",
    "..ABBBBC...",
    "..ABBBC....",
    ".ABBBBC....",
    ".ABBBC.....",
    ".ABBBC.....",
    ".ABBBBC....",
    ".EDDDDDDE..",
    "EDDEDDEDDEw",
    "EEEEEEEEEE.",
]
TAIL = [
    "....AAAA........",
    "..AABBBBA.......",
    ".ABBC..CBA......",
    "ABC.....BB......",
    "AB......BB......",
    "AB.....ABC......",
    "ABA..AABC.......",
    ".BBBBBBC........",
    "..CCCBBA........",
    "......BBA.......",
    "......ABB.......",
    "......ABB.......",
    ".......ABB......",
    ".......ABBA.....",
    "........ABBA....",
    ".........ABBAA..",
    "..........ABBBBA",
    "............CBBB",
]
ARMF = [
    "..........D...",
    ".........DDD..",
    "AAAAA....DDDE.",
    "ABBBBBAA.DDDE.",
    "ABBBBBBBBDDDE.",
    "BBBBBBBBBDDEE.",
    ".CCCCCCCCEEE..",
]
ARMF_PUSH = [
    "..................DD..",
    ".................DDDD.",
    "AAAAAAAAAAAAAA...DDDE.",
    "ABBBBBBBBBBBBBBBBDDDE.",
    "BBBBBBBBBBBBBBBBBDDEE.",
    ".CCCCCCCCCCCCCCCCEEE..",
]
ARMB = ['..DD...', '.DDDE..', '.DDDE..', '.ABC...', '.ABC...', '.ABBC..', 'ABBBC..', 'ABBBBAA', '.CBBBBB', '..CCCCC']
BEAD = ['.kkk.', 'kwPPk', 'kPPQk', 'kPQQk', '.kkk.']
BEAD_S = ['.kk.', 'kwPk', 'kPQk', '.kk.']
BROW = ['.DDD.', 'DDDDD', 'DDDDE', '.DDE.']
WAVE = [
    "......kkk.......",
    "........kPk.....",
    "..kk.....kPk....",
    "....kPk...kPk...",
    "kk...kPk...kwk..",
    "..kk..kwk..kwk..",
    "..kPk.kwk..kwk..",
    "..kk..kwk..kwk..",
    "kk...kPk...kwk..",
    "....kPk...kPk...",
    "..kk.....kPk....",
    "........kPk.....",
    "......kkk.......",
]
# 数珠：念力で 体の まわりを 回る（コマごとに 位置を 手で 決める）
import math
def ring(cx, cy, r, a0, step, n):
    return [(round(cx + r * math.cos(math.radians(a0 + i * step))) - 2, round(cy + r * math.sin(math.radians(a0 + i * step))) - 2) for i in range(n)]
BEADS = {
    'a': ring(25, 27, 17, 160, 20, 9),
    'b': ring(25, 27, 17, 170, 20, 9),
    'atk0': ring(30, 22, 13, 150, 24, 9),
    'atk1': [(50 + i * 4, 22 + (2 if i % 2 else 0)) for i in range(5)],
}
def beads():
    L = []
    for key, frames in (('a', 'idle0|idle2|blink|walk0|walk2|hit'), ('b', 'idle1|idle3|walk1|walk3'), ('atk0', 'atk0'), ('atk1', 'atk1|atk2')):
        for i, (x, y) in enumerate(BEADS[key]):
            L.append(dict(n=f'bead{key}{i}', g='beads', x=x, y=y, rows=BEAD if (i % 3 == 1) else BEAD_S, only=frames))
    return L

def base():
    return [
        dict(n='armB', g='armB', x=20, y=14, rows=outline(dk(ARMB))),
        dict(n='tail', g='tail', x=5, y=22, rows=outline(TAIL)),
        dict(n='legB', g='legB', x=17, y=42, rows=outline(dk(LEG))),
        dict(n='body', g='body', x=20, y=25, rows=outline(BODY)),
        dict(n='sash', g='body', x=21, y=39, rows=outline(SASH)),
        dict(n='legA', g='legA', x=25, y=42, rows=outline(LEG)),
        dict(n='head', g='head', x=26, y=9, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_SHOUT)}),
        dict(n='eyes', g='head', x=35, y=16, rows=EYES, alt=EYES_ALT),
        dict(n='brow', g='head', x=35, y=11, rows=BROW),
        dict(n='eye3', g='head', x=36, y=11, rows=EYE3, alt=EYE3_ALT),
        dict(n='armF', g='armF', x=32, y=27, rows=outline(ARMF), alt={'atk1|atk2': outline(ARMF_PUSH)}),
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
    return beads() + [dict(l, not_='ko') for l in base()] + [
        dict(n='wave', g='root', x=60, y=16, rows=WAVE, only='atk1'),
        dict(n='ko', g='root', x=4, y=61 - len(ko), rows=ko, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'beads': (0, -1)}, 'idle2': {'body': (0, 1), 'beads': (0, 0)}, 'idle3': {'beads': (0, 1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'armF': (-4, -2), 'armB': (2, 0)},
    'atk1': {'root': (4, 0), 'body': (1, 0), 'head': (1, 0)},
    'atk2': {'root': (5, 0), 'body': (1, 0), 'head': (1, 0), 'beads': (6, -2)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 1)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'beads': 'root'}
