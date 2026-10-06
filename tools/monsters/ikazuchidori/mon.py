# イカヅチドリ（でんき・ひこう(風) × 雷鳥）手打ち GBA風
import pix
META = dict(id='ikazuchidori', name='イカヅチドリ', types=['elec', 'wind'], base='雷鳥（神話）', size='L')
PAL = {
    'k': '#101018', 'l': '#1a2a3e',
    'P': '#7ca6b8', 'Q': '#3e5f78', 'Z': '#1f2f48',
    'G': '#eaeef6', 'g': '#9ca6be',
    'Y': '#ffec3a', 'E': '#7af4ff', 'w': '#ffffff',
    'O': '#f4c64a', 'o': '#a6702a',
}
LIGHT = set('PGYEwO')

# 翼：上の ふちが 稲妻の ぎざぎざ、青い 羽に 電気の すじ
WING_UP = [
    '....k..........k..........k........',
    '...kYk........kYk........kYk.......',
    '...kPk.......kPPk.......kPPk.......',
    '..kPPQk.....kPPQk......kPPQQk......',
    '..kPPQQk...kPPPQQk....kPPPQQk......',
    '.kPPPQQQk.kPPPQQQQk..kPPPQQQQk.....',
    '.kPPQQQQQkPPPQQQQQQkkPPQQQQQQk.....',
    'kPPPQQQQQQPPQQQQQQQQPPQQQQQQQZk....',
    'kPPQQQQQQQPQQQQQQQQQPQQQQQQQZZk....',
    '.kPQQQQQQQQQQQQQQQQQQQQQQQQZZZk....',
    '..kQQQQQQQQQQQQQQQQQQQQQQQZZZZk....',
    '...kQQkQQQQQkQQQQQQQkQQQQZZZZk.....',
    '....kZkQQQQkQQQQQQkQQQQQZZZZZk.....',
    '.....kkZQQkQQQQQQkQQQQQZZZZZk......',
    '......kkZkZQQQQQkQQQQQZZZZZZk......',
    '.......kkkZZQQQkZQQQQZZZZZZk.......',
    '........kkkZZZkZZQQQZZZZZZk........',
    '.........kkkkkkZZZQQZZZZZk.........',
    '...........kkkkkZZZZZZZZk..........',
    '.............kkkkZZZZZZk...........',
    '...............kkkkZZZk............',
    '...................kkk.............',
]
def bolt(rows, pts):
    g = pix.grid_of(rows)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        pix.line(g, x0, y0, x1, y1, 'Y')
        pix.line(g, x0, y0 + 1, x1, y1 + 1, 'E')
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if c in 'YE' and rows[y][x] in '.k': g[y][x] = rows[y][x]
    return pix.rows_of(g)
WING_UP = [WING_UP[0]] + [r for r in WING_UP[1:6] for _ in (0, 1)] + WING_UP[6:]
WING_UP = bolt([r.replace('E', 'Q') for r in WING_UP], [(4, 11), (9, 15), (8, 17), (15, 19), (14, 21), (21, 23)])
def swept(rows):
    keep = [r for y, r in enumerate(rows) if y % 3 != 1]
    H = len(keep); out = []
    for y, r in enumerate(keep):
        sh = (H - 1 - y) * 2 // 3
        out.append(('.' * 12 + r)[sh:])
    w = max(len(r) for r in out); return [r.ljust(w, '.') for r in out]
WING_MID = swept(WING_UP)
WING_DN = pix.flip_v(WING_MID)
def dark(rows): return pix.recolor(rows, {'P': 'Q', 'Q': 'Z', 'E': 'Q', 'Y': 'E'})

BODY = [
    '..............kkkkk.....',
    '...........kkkPPPPGk....',
    '.........kkPPPPPGGGGk...',
    '.......kkPPPPPQGGGGGk...',
    '.....kkPPPPQQQQGGgGGk...',
    '....kPPPPQQQQQQGGGGgGk..',
    '...kPPPQQQQQQQQGgGGGgk..',
    '..kPPQQQQQQQQQQGGGgGgk..',
    '.kPQQQQQQQQQQQQgGGGggk..',
    '.kQQQQQQQQQQQQgGgGgggk..',
    'kQQQQQQQQQQQQQggGgggk...',
    'kZQQQQQQQQQQQZgggggk....',
    'kZZQQQQQQQQQZZggggk.....',
    '.kZZZQQQQQZZZZkkkk......',
    '..kkZZZZZZZZZk..........',
    '....kkkkkkkkk...........',
]
HEAD = [
    'k.........k.........',
    'kYk......kYk........',
    '.kYk....kYk.........',
    '..kEk..kEk..........',
    '..kPPkkPPk..........',
    '..kPPPPPPQkk........',
    '.kPPPPPPPPQQkk......',
    '.kPPkkkkkkkQQQk.....',
    'kPPkEEwkkkkkQQQk....',
    'kPQQkkkkOOOOkkQk....',
    'kQQQQQQkOOOOOOkk....',
    'kZQQQQQkOOooOOOOk...',
    'kZZQQQQkOoookkOOk...',
    '.kZZQQQkkooYk.kOk...',
    '..kkZZZk.kkkk.kok...',
    '....kkk........kk...',
]
EYE = ['EEw']
EYE_ALT = {'blink': ['kkk'], 'atk0|atk1|atk2': ['www'], 'hit': ['kEk'], 'ko': ['EkE']}
TAIL = [
    '..............kk..',
    '............kkPQk.',
    '..........kkPPQk..',
    '........kkPPQQk...',
    '..kk..kkPPQQQk....',
    '.kYPkkPPQQQQk.....',
    '..kkPPPQQQZk......',
    '....kkQQQZZk......',
    '...kPPQQZZkk......',
    '..kPPkkZZk.kk.....',
    '.kPPk..kZk.kQk....',
    'kYPk..kQZk..kQk...',
    '.kk..kQZk...kZk...',
    '....kQZk....kZQk..',
    '...kYQk......kZQk.',
    '...kYk.......kYk..',
    '....k.........k...',
]
TALON = [
    '.kkkkk...',
    'kPQQQZk..',
    'kQQQZZk..',
    'kQQZZZk..',
    '.kQZZk...',
    '.kOOok...',
    'kOkOkOk..',
    'kwkokwk..',
    'kw.kw.wk.',
    '.k..k..k.',
]

SPARK = [  # ため：冠の 避雷針に 放電
    '..k.....k..',
    '.kYk...kEk.',
    'kYwYk.kEwEk',
    '.kYk...kEk.',
    '..k..k..k..',
    '....kYk....',
    '...kYwYk...',
    '....kYk....',
    '.....k.....',
]
BOLT = [  # 決め：くちばしから 稲妻
    '..................kk......',
    '.................kYwk.....',
    'kkk.............kYwk......',
    'kwYkk.....kk...kYwk.......',
    '.kkwYkk..kYwk.kYwwkkkkk...',
    '...kkwYkkYwwkkYwwYYYYwwk..',
    '.....kkwwwwYYwwwkkkkkYwwk.',
    '.......kkYwwkkkk....kkYwwk',
    '.........kYwk.........kYwk',
    '..........kYk..........kYk',
    '...........k............k.',
]
BURST = [
    '...k...k...',
    '..kEk.kYk..',
    'k.kwEkwYk.k',
    'kEkkwwwkkYk',
    '.kEwwwwwYk.',
    'kkwwwwwwwkk',
    '.kYwwwwwEk.',
    'kYkkwwwkkEk',
    'k.kYkwkEk.k',
    '..kYk.kEk..',
    '...k...k...',
]
UP, MID, DN = 'idle0|blink|walk0|atk0', 'idle1|idle3|walk1|walk3|atk2|hit|ko', 'idle2|walk2|atk1'
MANE = [
    '....kkk..kkk....',
    '..kkGGGkkGGGkk..',
    '.kGGGGGGGGGGGgk.',
    'kGGGgGGGGgGGGggk',
    'kGGgggGGgggGgggk',
    '.kgggkggggkgggk.',
    '..kkk.kkkk.kkk..',
]

def layers():
    return [
        dict(n='wingB_up', g='wingB', x=18, y=1, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=10, y=13, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=9, y=31, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='tail', x=5, y=42, rows=TAIL),
        dict(n='talonB', g='talon', x=29, y=42, rows=pix.recolor(TALON, {'P': 'Q', 'Q': 'Z'})),
        dict(n='body', g='body', x=18, y=30, rows=BODY),
        dict(n='talon', g='talon', x=34, y=41, rows=TALON),
        dict(n='mane', g='head', x=35, y=24, rows=MANE),
        dict(n='head', g='head', x=40, y=10, rows=HEAD),
        dict(n='eye', g='head', x=44, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='spark', g='head', x=37, y=0, rows=SPARK, only='atk0'),
        dict(n='bolt', g='fx', x=51, y=13, rows=BOLT, only='atk1'),
        dict(n='burst', g='fx', x=60, y=12, rows=BURST, only='atk2'),
        dict(n='wingF_up', g='wingF', x=6, y=9, rows=WING_UP, only=UP),
        dict(n='wingF_mid', g='wingF', x=-3, y=18, rows=WING_MID, only=MID),
        dict(n='wingF_dn', g='wingF', x=-3, y=33, rows=WING_DN, only=DN),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, 1)},
    'idle2': {'root': (0, 2), 'talon': (0, -1)},
    'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)},
    'walk1': {},
    'walk2': {'root': (0, 1), 'talon': (-1, -1), 'tail': (0, -1)},
    'walk3': {},
    'atk0': {'root': (-3, -2), 'head': (-1, 0), 'talon': (1, 0)},
    'atk1': {'root': (2, 1), 'head': (2, 1), 'talon': (2, -1)},
    'atk2': {'root': (4, 1), 'head': (1, 1)},
    'hit': {'root': (-4, 0), 'head': (-1, -1), 'talon': (1, 0), 'tail': (1, 0)},
    'ko': {'root': (-2, 6), 'head': (3, 4), 'talon': (0, -2), 'tail': (0, -3)},
}
PARENT = {'head': 'body', 'tail': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
