# イカヅチドリ（でんき・ひこう(風) × 雷鳥）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭、胴は 小さく、翼は 大きい まま）
import pix
META = dict(id='ikazuchidori', name='イカヅチドリ', types=['elec', 'wind'], base='雷鳥（神話）', size='L')
PAL = {
    'k': '#101018', 'l': '#1a2a3e',
    'P': '#7ca6b8', 'Q': '#3e5f78', 'Z': '#1f2f48',
    'G': '#eaeef6', 'g': '#9ca6be',
    'Y': '#ffec3a', 'E': '#7af4ff', 'w': '#ffffff',
    'O': '#f4c64a', 'o': '#a6702a', 'c': '#2a8cb8',   # c：目の 暗い 虹彩
}
KEEP_BLACK = set('wEcY')
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
# 頭（大きく）：丸い 頭、重い まゆ、かぎ形の くちばし
HEAD_C = [
    "......PPPPPP............",
    "....PPPPPPPPPP..........",
    "...PPPQQQQQQQQQ.........",
    "..PPQQQQQQQQQQQQQ.......",
    ".PPQQQQQQQQQQQQQQQ......",
    ".PQQQQQQQQQQQQQQQQQ.....",
    "PPQQQQQQQQQQQQQQQQQQ....",
    "PQQQQQQQQQQQQQQQQkOOOO..",
    "PQQQQQQQQQQQQQQQkOOOOOOO",
    "QQQQQQQQQQQQQQQkOOOOOOOO",
    "QQQQQQQQQQQQQQQkOOOOoooO",
    "ZQQQQQQQQQQQQQkOOoookkoO",
    "ZQQQQQQQQQQQQQkooook.koO",
    ".ZQQQQQQQQQQQQkkokk..kOo",
    ".ZZQQQQQQQQQQZ.kk....ko.",
    "..ZZZQQQQQQZZZ.......k..",
    "....ZZZZZZZZ............",
]
HEAD_OPEN_BEAK = {   # 口を あけた くちばし（上と 下が ひらく）
    10: "QQQQQQQQQQQQQQQkOOOOoooO",
    11: "ZQQQQQQQQQQQQQkOOkkkkkoO",
    12: "ZQQQQQQQQQQQQQkk.....kOo",
    13: ".ZQQQQQQQQQQQQkooOk...ko.",
    14: ".ZZQQQQQQQQQQZ.kooOOk.k..",
    15: "..ZZZQQQQQQZZZ..kkkkk....",
}
EYES = {
    'open':  ['kk........', '.kkkkkkkk.', '..kwEEEkEk', '.kEccccckc', '..kkkkkkk.'],
    'glow':  ['kk........', '.kkkkkkkk.', '..kwwwEEEk', '.kEEwEEkEk', '..kccckck.'],
    'blink': ['kk........', '.kkkkkkkk.', '..kQQQQQQk', '.kkkkkkkkk', '..ZZZZZZ..'],
    'hit':   ['kk........', '.kkkkkkkk.', '..kEkkkEkk', '.kkkckkkck', '..kkkkkkk.'],
    'ko':    ['..........', '..kEccEk..', '..kckkck..', '..kkcckk..', '..kckkck..'],
}
def head(eye='open', beak=False):
    rows = list(HEAD_C)
    if beak:
        for y, r in HEAD_OPEN_BEAK.items(): rows[y] = r
    g = [list(r) for r in rows]
    for j, r in enumerate(EYES[eye]):
        for i, c in enumerate(r):
            if c != '.': g[4 + j][7 + i] = c
    for (x, y) in ((5, 1), (6, 1), (3, 3), (2, 4), (9, 2), (10, 2)): g[y][x] = 'P'
    for (x, y) in ((3, 10), (4, 11), (5, 12), (10, 12), (11, 13)): g[y][x] = 'Z'
    return pix.outline([''.join(r) for r in g])
CREST = ['kk.......', 'kPkk.....', '.kPQQkk..', '..kQQQQZk', '...kkQQZk', 'kk...kkk.', 'kPkkk....', '.kPQQkk..', '..kkQQZk.', '....kkk..']
HORN = ['kk....', 'kYYk..', '.kYEk.', '..kEPk', '..kPPk', '..kPPk']
HORN_KO = pix.recolor(HORN, {'Y': 'g', 'E': 'Q'})
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

def lying_body(W, H):
    """あたり：たおれた 胴（横長の だ円）。光は 左上、右下は 影"""
    g = pix.grid(W, H); cx, cy, rx, ry = W / 2, H / 2, W / 2 - .2, H / 2 - .2
    for y in range(H):
        for x in range(W):
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if nx * nx + ny * ny > 1: continue
            l = -nx * .5 - ny * .85
            g[y][x] = 'P' if l > .55 else 'Z' if l < -.35 else 'Q'
    return pix.outline(pix.rows_of(g))
# ダウン：力なく 地面に たれた 翼（手打ち）。上の ふちの ぎざぎざは 残し、稲妻の 帯は 消えて 灰色
WING_KO = [
    '...................kkkk.........',
    '.............kk..kkPPPPkk.......',
    '..........kkkPPkkPPPPQQQQkk.....',
    '.......kkkPPPPPPPPQQQQQQQQQk....',
    '.....kkPPPQQQQQQQQQQQgQQQQZk....',
    '....kPPQQQkQQQQkQQQgQQQQZZZk....',
    '...kPQQkkPQQQkkPQgQkQQQZZZk.....',
    '..kPQkkkPQQkkkPQQkkkPQZZkk......',
    '.kPQk.kPQQk.kPQQk.kPQZZk........',
    'kPQZk.kPQZk.kPQZk.kPZk..........',
    'kQZk..kQZk..kQZk..kZk...........',
    '.kk....kk....kk....k............',
]
TAIL_KO = [
    '..........kk......',
    '..kk....kkPQk.....',
    '.kPQkkkkPQQZk.....',
    'kPQQQQPQQZZkkkk...',
    '.kkZZZQQZZkkQQZk..',
    '...kkkkkkk..kkkk..',
]
SMOKE = [  # 角から 立ちのぼる 消えた 電気の けむり
    '..kk...kk.',
    '.kggk.kgGk',
    '.kgk..kgk.',
    'kgk..kgk..',
    '.kk...kk..',
]
def ko_layers():
    return [
        dict(n='ko_tail', g='root', x=-6, y=54, rows=TAIL_KO),
        dict(n='ko_body', g='root', x=11, y=46, rows=lying_body(30, 13)),
        dict(n='ko_talon', g='root', x=31, y=51, rows=pix.flip_v(TALON)),
        dict(n='ko_mane', g='root', x=32, y=49, rows=MANE),
        dict(n='ko_horn', g='root', x=44, y=38, rows=HORN_KO),
        dict(n='ko_horn2', g='root', x=49, y=37, rows=HORN_KO),
        dict(n='ko_head', g='root', x=39, y=42, rows=head('ko', True)),
        dict(n='ko_wingF', g='root', x=2, y=49, rows=WING_KO),
        dict(n='ko_smoke', g='root', x=46, y=31, rows=SMOKE),
    ]

def layers():
    L = base_layers()
    for l in L: l['not_'] = (l['not_'] + '|ko') if l.get('not_') else 'ko'
    return L + [dict(l, only='ko') for l in ko_layers()]
def base_layers():
    return [
        dict(n='wingB_up', g='wingB', x=18, y=1, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=10, y=13, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=9, y=31, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='tail', x=5, y=42, rows=TAIL),
        dict(n='talonB', g='talon', x=29, y=42, rows=pix.recolor(TALON, {'P': 'Q', 'Q': 'Z'})),
        dict(n='body', g='body', x=18, y=30, rows=BODY),
        dict(n='talon', g='talon', x=34, y=41, rows=TALON),
        dict(n='crest', g='head', x=29, y=13, rows=CREST),
        dict(n='horn1', g='head', x=39, y=6, rows=HORN),
        dict(n='horn2', g='head', x=45, y=5, rows=HORN),
        dict(n='mane', g='head', x=33, y=26, rows=MANE),
        dict(n='head', g='head', x=36, y=10, rows=head(), alt={'blink': head('blink'), 'hit': head('hit'), 'atk0': head('glow'), 'atk1|atk2': head('glow', True)}),
        dict(n='spark', g='head', x=38, y=-3, rows=SPARK, only='atk0'),
        dict(n='bolt', g='fx', x=58, y=16, rows=BOLT, only='atk1'),
        dict(n='burst', g='fx', x=63, y=14, rows=BURST, only='atk2'),
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
    'ko': {},
}
PARENT = {'head': 'body', 'tail': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
