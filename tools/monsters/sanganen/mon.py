# サンガンエン（エスパー・かくとう × 三つ目の 猿）手打ち GBA風
from pix import outline
import math
META = dict(id='sanganen', name='サンガンエン', types=['psychic', 'fighting'], base='三つ目の 猿', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1c48',
    'A': '#b08ee6', 'B': '#6e50b0', 'C': '#3c2a6c',      # 毛（むらさき）
    'D': '#f4cc94', 'E': '#bc8650',                      # 顔・むね・手
    'S': '#f0b834', 'T': '#a8661e',                      # 帯（こがね）
    'P': '#ff74dc', 'Q': '#b42c9e',                      # 念力の 光
    'Y': '#ffe84a', 'w': '#ffffff', 'M': '#5a1430',      # 目・きば・口の 中
}
LIGHT = set('ADSPYw')
KEEP_BLACK = set('wYPM')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'S': 'T'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

# ---- 頭：前へ つき出した 顔。重い まゆの ひさし、うなる 口、額に 第三の 目 ----
HEAD = [
    "......................",
    "....AABBBBBBBA........",
    "..AABBBBBBBBBBBA......",
    ".ABBBBBBBBBBBBBBA.....",
    "ABBBBBBBBBBBBBBBBA....",
    "ABBBBBBBBBBBBBBBBBA...",
    "BBBBBBBBBDDDDDBBBBBB..",
    "BBBBBBBBDDDDDDDDDDDDD.",
    "BBBBBBBBDDDDDDDDDDDDDD",
    "BBBBBBBDDDDDDDDDDDDDDD",
    "BBBCBBBDDDDDDDDDDDDDDD",
    "BBBBCBBEDDDDDDDDDDDDDE",
    "BBBBBBBEDDDDDDDDDDDDDE",
    ".BBBBBBEEDDDDDDDDDDDE.",
    ".CBBBBBBEEDDDDDDDDDE..",
    "..CBBBBBBEEEEEEEEEE...",
    "...CCCBBBBCCCC........",
]
# 顔の 仕上げ（重い まゆ・つり目・鼻・うなる 口と きば）は 1ドットずつ
_B = "......................"
_BROW = ["........CCC...........", ".........CCCCC........", "..........kkCCCCCC...."]
_MOUTH = [".............kkkkkkkkk", "............kwkMMMMwkw", "............kMMMMMMMk.", ".............kwkkkkwk."]
_ROAR = ["............kkkkkkkkkk", "............kwkwkkwkwk", "............kMMMMMMMMk", "............kMMMMMMMk.", ".............kwkkkkwk."]
def _face(e1, e2, mouth=_MOUTH, under="............kkkk......"):
    return [_B] * 6 + _BROW + [e1, e2, under] + mouth
FACE = _face("..........kYYYwkkCC...", "...........kYYkYk...kk")
FACE_ALT = {
    'blink': _face("..........kkkkkkkCC...", "...........DDDDDD...kk", under=_B),
    'atk0|atk1|atk2': _face("..........kwwwwkkCC...", "...........kwwkwk...kk", _ROAR[:1] + _ROAR[1:], under=_B),
    'hit': _face("..........kYkYkkkCC...", "...........kkYkYk...kk"),
    'ko': _face("..........k.k...kCC...", "...........k.k.....kk", [_B, ".............kkkkkkkkk", "............kwkMMMMwk.", ".............kkkkkkk.."], under=".........k.k.........."),
}
# 額の 第三の 目（たての まぶた、光る）
EYE3 = ['.kk.', 'kPPk', 'PwYP', 'PYwP', 'kPQk', '.kk.']
EYE3_ALT = {'blink': ['....', '.kk.', 'kQQk', 'kkkk', '.kk.', '....'],
            'atk0|atk1|atk2': ['.PP.', 'PwwP', 'wwww', 'wwww', 'PwwP', '.PP.'],
            'ko': ['....', '.kk.', 'kkkk', 'kQQk', '.kk.', '....']}
# 逆立つ たてがみ（後ろへ なびく とげ）
MANE = [
    "AA..........",
    ".AAA........",
    "..ABBA......",
    "...ABBBB....",
    "AAAABBBBB...",
    ".AABBBBBBB..",
    "...AABBBBBB.",
    "AAAABBBBBBB.",
    ".AABBBBBBBB.",
    "...CBBBBBBB.",
    "AAACBBBBBBB.",
    ".CCBBBBBBB..",
    "...CCBBBB...",
]
# ---- 胴：広い 肩、しまった 腰。むねと 腹すじは 手で ----
BODY = [
    ".......AAAAAAAA.....",
    "....AAABBBBBBBBAA...",
    "..AABBBBBBBBBBBBBA..",
    ".ABBBBBBBBBBBBBBBBA.",
    "ABBBBBBBBBBBBBBDDDB.",
    "ABBBBBBBBBBBBBDDDDDE",
    "ABBBBBBBBBBBBBDDDDDE",
    ".ABBBBBBBBBBBBEEDDE.",
    ".ABBBBBBBBBBBBDDEDE.",
    "..ABBBBBBBBBBBEDDE..",
    "..ABBBBBBBBBBBEDDE..",
    "...ABBBBBBBBBBEDE...",
    "...ABBBBBBBBBBBEE...",
    "..SSSSSSSSSSSSSSST..",
    "..STSSSSTSSSSSSSTT..",
    "..TTTTTTTTTTTTTTTT..",
]
SASH = ['SS', 'ST', 'ST', 'TT', '.T']
# ---- 足：ひくい かまえ。前足は 前へ、後ろ足は 後ろへ ----
LEG_F = [
    "AAAAAAA.......",
    "ABBBBBBBA.....",
    "ABBBBBBBBBA...",
    ".BBBBBBBBBBA..",
    ".CBBBBBBBBBBA.",
    "..CCBBBBBBBBC.",
    "....CCBBBBBBC.",
    ".......ABBBBC.",
    ".......ABBBC..",
    "......ABBBBC..",
    "......ABBBC...",
    "......ABBBC...",
    ".....ABBBBC...",
    ".....ABBBC....",
    ".....ABBBC....",
    ".....ABBBBC...",
    "....ADDDDDDE..",
    "...ADDDDDDDDEw",
    "...EDEEDEEDEEw",
]
LEG_B = [
    ".....AAAAAAA",
    "....ABBBBBBB",
    "...ABBBBBBBC",
    "..ABBBBBBBC.",
    ".ABBBBBBBC..",
    "ABBBBBBCC...",
    "ABBBBBC.....",
    "ABBBBC......",
    ".ABBBC......",
    ".ABBBC......",
    "..ABBBC.....",
    "..ABBBC.....",
    "..ABBBC.....",
    "...ABBC.....",
    "...ABBC.....",
    "...ABBBC....",
    "..ADDDDDE...",
    ".ADDDDDDDEw.",
    ".EDEEDEEDEw.",
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
# ---- 腕：前の 腕は 掌底の かまえ（つめ つき）----
ARMF = [
    ".AAAA.............",
    "ABBBBA............",
    "ABBBBBA...........",
    "ABBBBBA...........",
    "ABBBBBBA..........",
    ".BBBBBBA......DD..",
    ".BBBBBBBA....DDDDw",
    ".CBBBBBBBAAAADDDDD",
    "..CBBBBBBBBBBDDDDE",
    "...CBBBBBBBBBDDDEw",
    "....CCCCCCCCCEEEE.",
]
ARMF_PUSH = [
    ".AAAA.....................",
    "ABBBBAAAAAAAAAAAAAAAAA.DD.",
    "ABBBBBBBBBBBBBBBBBBBBBDDDw",
    "ABBBBBBBBBBBBBBBBBBBBBDDDD",
    ".BBBBBBBBBBBBBBBBBBBBBDDDE",
    ".CCCCCCCCCCCCCCCCCCCCCDDEw",
    "......................EEE.",
]
# 後ろの 腕：あごの 前で かぎづめを かまえる
ARMB = [
    "..........DD..",
    ".........DDDDw",
    "........DDDDD.",
    "........DDDDEw",
    ".......ABEEE..",
    "......ABBC....",
    ".....ABBBC....",
    "....ABBBC.....",
    "AAAABBBBC.....",
    "BBBBBBBC......",
    "CCCCCCC.......",
]
BEAD = ['.kkk.', 'kwPPk', 'kPPQk', 'kPQQk', '.kkk.']
BEAD_S = ['.kk.', 'kwPk', 'kPQk', '.kk.']
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
def ring(cx, cy, r, a0, step, n):
    return [(round(cx + r * math.cos(math.radians(a0 + i * step))) - 2, round(cy + r * math.sin(math.radians(a0 + i * step))) - 2) for i in range(n)]
BEADS = {
    'a': ring(28, 26, 19, 150, 19, 9),
    'b': ring(28, 26, 19, 160, 19, 9),
    'atk0': ring(36, 16, 14, 140, 26, 9),
    'atk1': [(56 + i * 4, 20 + (2 if i % 2 else 0)) for i in range(5)],
}
def beads():
    L = []
    for key, frames in (('a', 'idle0|idle2|blink|walk0|walk2|hit'), ('b', 'idle1|idle3|walk1|walk3'), ('atk0', 'atk0'), ('atk1', 'atk1|atk2')):
        for i, (x, y) in enumerate(BEADS[key]):
            L.append(dict(n=f'bead{key}{i}', g='beads', x=x, y=y, rows=BEAD if (i % 3 == 1) else BEAD_S, only=frames))
    return L

def base():
    return [
        dict(n='tail', g='tail', x=3, y=24, rows=outline(TAIL)),
        dict(n='armB', g='armB', x=36, y=21, rows=outline(dk(ARMB))),
        dict(n='legB', g='legB', x=13, y=40, rows=outline(dk(LEG_B))),
        dict(n='mane', g='head', x=19, y=7, rows=outline(MANE)),
        dict(n='body', g='body', x=18, y=24, rows=outline(BODY)),
        dict(n='sash', g='body', x=19, y=40, rows=outline(SASH)),
        dict(n='legA', g='legA', x=25, y=40, rows=outline(LEG_F)),
        dict(n='head', g='head', x=29, y=6, rows=outline(HEAD)),
        dict(n='face', g='head', x=29, y=6, rows=FACE, alt=FACE_ALT),
        dict(n='eye3', g='head', x=40, y=7, rows=EYE3, alt=EYE3_ALT),
        dict(n='armF', g='armF', x=24, y=27, rows=outline(ARMF), not_='atk1|atk2'),
        dict(n='armFp', g='armF', x=24, y=27, rows=outline(ARMF_PUSH), only='atk1|atk2'),
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
    return beads() + [dict(l, not_=(l.get('not_', '') + '|ko').strip('|')) for l in base()] + [
        dict(n='wave', g='root', x=60, y=24, rows=WAVE, only='atk1'),
        dict(n='ko', g='root', x=4, y=61 - len(ko), rows=ko, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'beads': (0, -1)}, 'idle2': {'body': (0, 1), 'beads': (0, 0)}, 'idle3': {'beads': (0, 1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'armF': (-4, -1), 'armB': (-1, -2), 'tail': (1, 0)},
    'atk1': {'root': (4, 0), 'body': (1, 0), 'head': (1, 0)},
    'atk2': {'root': (5, 0), 'body': (1, 0), 'head': (1, 0), 'beads': (6, -2)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 1), 'armB': (-2, 1)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'beads': 'root'}
