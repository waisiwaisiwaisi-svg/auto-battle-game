# ヤイバクワ（むし・はがね × クワガタ）手打ち GBA風
import pix
META = dict(id='yaibakuwa', name='ヤイバクワ', types=['bug', 'steel'], base='クワガタ', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2434',
    'A': '#e2eaf2', 'B': '#8e9cb6', 'C': '#4a5470',      # 鋼 明・中・暗
    'P': '#d8323e', 'Q': '#701824',                      # 赤い おどし（よろいの ひも）
    'G': '#f2cc64', 'H': '#a07226',                      # 金の つば
    'R': '#ff3a3a', 'E': '#c8f2ff', 'w': '#ffffff',
}
LIGHT = set('AGEw')
KEEP_BLACK = set('wRE')

def shade(mask, lt, md, dk, t=2, lf=1, r=2, b=2):
    g = pix.grid_of(mask); H, W = len(g), len(g[0])
    on = lambda y, x: 0 <= y < H and 0 <= x < W and g[y][x] != '.'
    out = [r_[:] for r_ in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '#': continue
            dt = 0
            while on(y - dt - 1, x): dt += 1
            db = 0
            while on(y + db + 1, x): db += 1
            dl = 0
            while on(y, x - dl - 1): dl += 1
            dr = 0
            while on(y, x + dr + 1): dr += 1
            c = md
            if dt < t or dl < lf: c = lt
            if dr < r or db < b: c = dk
            if dt < t and dr < r: c = md
            out[y][x] = c
    return [''.join(r_) for r_ in out]
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'w': 'A', 'G': 'H', 'P': 'Q'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 前ばね：ひらたく 長い 鋼の 板。赤い おどしで つづる（手で 置く）----
def elytra():
    g = pix.grid(28, 17); pix.ellipse(g, 14, 10, 14.3, 10.5, '#')
    rows = shade(pix.rows_of(g), 'A', 'B', 'C', t=3, lf=2, r=3, b=3)
    g = pix.grid_of(rows)
    for y in (6, 11):                                  # 板の さかい目
        for x in range(1, 27):
            if g[y][x] != '.' and g[y][x - 1] != '.' and g[y][x + 1] != '.': g[y][x] = 'l'
        for x in range(28):
            if g[y + 1][x] in 'BC' and g[y][x] == 'l' and x < 20: g[y + 1][x] = 'A' if x < 12 else 'B'
    for y in (6, 11):                                  # おどし：さかい目を またぐ 赤い ひも
        for x in range(4, 26, 4):
            if g[y][x] != 'l' or g[y - 1][x] == '.' or g[y + 2][x] == '.': continue
            g[y - 1][x] = 'P'; g[y][x] = 'P'; g[y + 1][x] = 'Q'
    for (x, y) in ((8, 1), (9, 1), (10, 1), (5, 3)):
        if g[y][x] in 'AB': g[y][x] = 'w' if y == 1 else 'A'
    return pix.outline(pix.rows_of(g))

PRO = [
    '...kkkkkkk....',
    '.kkAAAAAABkk..',
    'kAAABBBBBBBBk.',
    'kABBBBBBBBBBBk',
    'kABPBBBPBBBPBk',
    'kAlPllllPllllk',
    'kBBQBBBBQBBCCk',
    'kBBBBBBBBBCCk.',
    'kCBBBBBBBCCCk.',
    '.kCCCCCCCCkk..',
    '..kkkkkkkk....',
]
HEAD = [
    '...kkkkkkk.....',
    '.kkAAAAAABkkk..',
    'kAAABBBBBBBBBk.',
    'kABBBBBBBBBBBBk',
    'kABkkkkkkkBBBBk',
    'kBk.......kkBBk',
    'kBBkk......kBBk',
    'kCBBBkkkkkkBBCk',
    'kCCBBBBBBBBBCCk',
    '.kCCCBBBBBCCCk.',
    '..kkkkkkkkkkk..',
]
EYE = ['RRRRRRwk', 'kkkRRRkk']
EYE_ALT = {'blink': ['kkkkkkkk', 'BBkkkkkk'], 'atk0|atk1|atk2': ['RRRRRRRw', 'kkRRRRRk'],
           'hit': ['kRkkkkRk', 'kkRRRRkk'], 'ko': ['RkRkRkRk', 'kRkkkRkk']}
# ---- 刀の あご：金の つば ＋ 反った 刃。刃先（内がわ）は 白く 光る ----
BLADE = [
    '................kk',
    '..............kkwk',
    '............kkwwAk',
    'kkkk.....kkkwwABk.',
    'kGHk..kkkwwwAABk..',
    'kGHkkkwwAAAABBk...',
    'kHHkAAAABBBBCk....',
    'kGHkBBBBCCCkk.....',
    'kkkkkkkkkk........',
]
BLADE_U = dark(pix.flip_v(BLADE))
# ひらいた あご（ため）：つばは そのまま、刃が ななめ 下へ
OPEN = [
    'kkkk.............',
    'kGHkkk...........',
    'kGHkwwkk.........',
    'kHHkAwwwkk.......',
    'kGHkBAAwwwkk.....',
    'kkkkkBBAAwwwk....',
    '.....kkBBAAwwk...',
    '.......kkBBAwwk..',
    '.........kkBAwwk.',
    '...........kBAwk.',
    '............kBwwk',
    '.............kkwk',
    '...............k.',
]
OPEN_U = dark(pix.flip_v(OPEN))
CREST = ['.....kk', '...kkAk', '.kkABBk', 'kABBBk.', 'kBBCk..']
SLASH = [
    'kk.....',
    '.Ewk...',
    '..Ewk..',
    '...Ewk.',
    '...Ewk.',
    '....Ewk',
    '....Ewk',
    '....Ewk',
    '....Ewk',
    '...Ewk.',
    '...Ewk.',
    '..Ewk..',
    '.Ewk...',
    'kk.....',
]
SPARK = ['E.w.', '.w..', 'w.E.', '....']
LEG = [
    '.....kkkk',
    '....kABBk',
    '...kABCk.',
    '..kABCk..',
    '.kBBCk...',
    '.kBCkk...',
    'kkBCk....',
    '.kBCk....',
    'kkBCk....',
    '.kBCk....',
    '.kCCk....',
    'kCCk.....',
    'kkk......',
]
LEGF = pix.flip_h(LEG)
LEGM = [
    '.kkk..',
    'kABBk.',
    'kBBCk.',
    '.kBCk.',
    '.kBCkk',
    'kkBCk.',
    '.kBCk.',
    '.kBCkk',
    '..kBCk',
    '..kCCk',
    '.kCCkk',
    '.kkk..',
]

def layers():
    return [
        dict(n='legF1', g='legB', x=9, y=46, rows=dark(LEG)),
        dict(n='legF2', g='legA', x=21, y=47, rows=dark(LEGM)),
        dict(n='legF3', g='legB', x=34, y=46, rows=dark(LEGF)),
        dict(n='jawU', g='jawU', x=45, y=26, rows=BLADE_U, not_='atk0'),
        dict(n='jawUo', g='jawU', x=45, y=21, rows=OPEN_U, only='atk0'),
        dict(n='ely', g='body', x=4, y=31, rows=elytra()),
        dict(n='leg1', g='legA', x=5, y=47, rows=LEG),
        dict(n='leg2', g='legB', x=17, y=48, rows=LEGM),
        dict(n='pro', g='body', x=26, y=33, rows=PRO),
        dict(n='crest', g='head', x=39, y=27, rows=CREST),
        dict(n='head', g='head', x=34, y=31, rows=HEAD),
        dict(n='eye', g='head', x=36, y=35, rows=EYE, alt=EYE_ALT),
        dict(n='leg3', g='legA', x=33, y=47, rows=LEGF),
        dict(n='jawL', g='jawL', x=45, y=35, rows=BLADE, not_='atk0'),
        dict(n='jawLo', g='jawL', x=45, y=36, rows=OPEN, only='atk0'),
        dict(n='spark', g='jawL', x=60, y=30, rows=SPARK, only='idle1|idle3'),
        dict(n='slash', g='root', x=62, y=26, rows=SLASH, only='atk1'),
        dict(n='slash2', g='root', x=60, y=26, rows=dark(SLASH), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'jawU': (0, -1)},
    'idle3': {'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1), 'head': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1), 'head': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 0)},
    'atk1': {'root': (6, 0), 'jawU': (1, 4), 'jawL': (1, -4)},
    'atk2': {'root': (5, 0), 'jawU': (1, 4), 'jawL': (1, -4)},
    'hit': {'root': (-3, 0), 'head': (-1, 1), 'jawU': (0, -1), 'jawL': (0, 1)},
    'ko': {'_flip': True},
}
PARENT = {'jawU': 'head', 'jawL': 'head', 'head': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root'}
