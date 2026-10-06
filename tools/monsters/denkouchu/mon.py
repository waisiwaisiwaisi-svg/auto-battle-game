# デンコウチュウ（でんき・むし × カブトムシ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 角、羽の ドームは 小さく 丸く、足は 短く）
import pix
META = dict(id='denkouchu', name='デンコウチュウ', types=['elec', 'bug'], base='カブトムシ', size='M')
EYE_BOX = (39, 35, 10, 8)   # 複眼（idle0）
PAL = {
    'k': '#101018', 'l': '#1c1a40',
    'A': '#6c8ce8', 'B': '#30409a', 'C': '#18204e',      # 甲羅（つやの ある 紺）
    'Y': '#fff47a', 'G': '#f0b828', 'E': '#a8f4ff',      # 電気
    'H': '#f4e2b0', 'I': '#b88e44', 'J': '#5c3e22',      # 真ちゅうの 角
    'D': '#3a8ad0', 'F': '#123a7a',                      # 複眼の あみ目（明・暗）
    'w': '#ffffff',
}
LIGHT = set('AYEHw')
KEEP_BLACK = set('wYEDF')

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
def put(rows, det, x0=0, y0=0):
    g = pix.grid_of(rows)
    for j, r in enumerate(det):
        for i, c in enumerate(r):
            if c not in '. ' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c
    return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'H': 'I', 'I': 'J'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 前ばね（ドームは 楕円で あたり → 陰影 → つやと いなずまの すじは 手で）----
ZZ = [5, 4, 3, 2, 1, 3, 2, 1, 0, -1, 1, 0, -1, -2]
def elytra(n=3):
    g = pix.grid(29, 19); pix.ellipse(g, 14.5, 11.5, 14.7, 11.3, '#')
    rows = shade(pix.rows_of(g), 'A', 'B', 'C', t=3, lf=2, r=3, b=3)
    g = pix.grid_of(rows)
    for (x, y) in ((6, 3), (7, 2), (8, 2), (9, 2), (10, 2), (5, 4), (4, 5), (3, 7), (3, 8)):
        g[y][x] = 'w' if (x, y) in ((8, 2), (9, 2)) else 'A'
    # いなずま形の すじ 3本。n 本 光る（光らない すじは 暗い みぞ）
    for i, bx in enumerate((6, 13, 20)):
        lit = i < n
        for y, o in zip(range(3, 16), ZZ):
            x = bx + o
            if g[y][x] == '.' or g[y][x + 1] == '.': continue
            g[y][x] = ('Y' if 5 <= y <= 12 else 'G') if lit else 'l'
            if g[y][x + 1] in 'ABC': g[y][x + 1] = 'G' if lit else 'C'
    for x in range(3, 26):
        if g[16][x] != '.' and g[16][x] not in 'YG': g[16][x] = 'l'
    return pix.outline(pix.rows_of(g))

PRO = [
    '.....kkkkkk.......',
    '...kkAAAwAAkk.....',
    '..kAAAAAABBBBkk...',
    '.kAAABBBBBBBBBBk..',
    'kAABBBBBBBBBBBBBk.',
    'kABBBBBBBBBBBBBBBk',
    'kABBBBBBBBBBBBBBCk',
    'kBBBBBBBBBBBBBBCCk',
    'kBBBBBBBBBBBBBCCk.',
    'kBBBBBBBBBBBBCCCk.',
    'kCBBBBBBBBBBCCCk..',
    'kCCBBBBBBBCCCCk...',
    '.kCCCCCCCCCCkk....',
    '..kkkkkkkkkk......',
]
# 頭（大きく）：丸い かぶと、まゆの ひさしの 下に 電光色の つり目（2段の 虹彩＋たての ひとみ）、白い 大あご
HEAD_M = [
    "....##########.........",
    "..###############......",
    ".##################....",
    "#####################..",
    "######################.",
    "#######################",
    "#######################",
    "#######################",
    "#######################",
    "#######################",
    "######################.",
    "#####################..",
    ".##################....",
    "..###############......",
    "....###########........",
]
# 目：複眼（D）。大きな ドームに 六角の 点の あみ目（D/F の 市松）、左上に 反射の 帯（E・w）と 火花の 黄の 光（Y）。瞳なし。太い まゆの 線が 前へ 下がって 怒りを 出す
EYES = {
    'open':  ['kkk.......', '.kkkkk....', '.kEEkkkkk.', 'kEwwDEFDkk', 'kYEDDFDFDk', 'kEDDFDFDFk', '.kDFDFDFk.', '..kkkkkk..'],
    'glow':  ['kkk.......', '.kkkkk....', '.kwwkkkkk.', 'kwwwYEYGkk', 'kwYEYGYGYk', 'kYEYGYGYGk', '.kYGYGYGk.', '..kkkkkk..'],
    'blink': ['..........', 'kkk.......', '.kkkkkkk..', 'kkkkkkkkkk', 'kYEDDFDFDk', 'kEDDFDFDFk', '.kDFDFDFk.', '..kkkkkk..'],
    'hit':   ['.......kk.', '....kkkk..', '.kkkkkkkk.', 'kDFDkFDFkk', 'kFDFDkDFDk', 'kDFDkFDFDk', '.kFDFkFDk.', '..kkkkkk..'],
    'ko':    ['..........', '..........', '.kkkkkkkk.', 'kDkEDEkDEk', 'kEDkDkDEDk', 'kDEDkDEDFk', '.kEkDkFDk.', '..kkkkkk..'],
}
def head(eye='open'):
    rows = shade(HEAD_M, 'A', 'B', 'C', t=2, lf=1, r=2, b=2)
    g = pix.grid_of(rows)
    for j, r in enumerate(EYES[eye]):
        for i, c in enumerate(r):
            if c != '.': g[2 + j][7 + i] = c
    for x in range(9, 22): g[11][x] = 'k'                  # 口
    for x in range(10, 21): g[12][x] = 'w' if x % 2 else 'k'  # 白い 大あご
    for (x, y) in ((5, 1), (6, 1), (2, 3), (1, 4)): g[y][x] = 'w' if (x, y) == (5, 1) else 'A'
    for (x, y) in ((3, 9), (4, 10), (5, 11), (17, 9), (18, 9)): g[y][x] = 'C'
    return pix.outline(pix.rows_of(g))
# 角：避雷針。太い 銅の 角に 光る コイル、先は ふたまた
HORN = [
    '......kk..........',
    '.....kYEk.........',
    '....kHIIk.kk......',
    '....kHIIkkEk......',
    '....kHHIIHIk......',
    '....kHHIIIJk......',
    '.....kHHIIJk......',
    '.....kEEEEEEk.....',
    '......kHHIIJk.....',
    '......kHHIIJJk....',
    '......kHHHIIJk....',
    '......kEEEEEEEk...',
    '.......kHHHIIJJk..',
    '.......kHHHIIJJk..',
    '......kHHHIIIJJk..',
    '.....kEEEEEEEEEk..',
    '....kHHHHIIIJJk...',
    '...kHHHHIIIJJk....',
    '..kHHHHIIIJJk.....',
    '.kHHHHIIIJJk......',
    'kHHHHIIJJkk.......',
    'kkkkkkkkk.........',
]
PHORN = [
    'kk..........',
    'kHHkkk......',
    'kHHIIIkkk...',
    '.kIIIJJJIkk.',
    '..kkJJJJJJEk',
    '....kkkkkkk.',
]
SPARK = {'idle0|walk0|walk2': ['E....Y.', '.E..k..', '...Y...'],
         'idle1|walk1|walk3|blink': ['..E..Y.', '.Y.....', 'E....E.'],
         'idle2': ['Y.....E', '..E.Y..', '.......'],
         'idle3': ['.Y..E..', 'E......', '....Y..']}
BOLT = [
    '.......kk.........',
    '......kYYk........',
    '.....kYEYk...kk...',
    'kk..kYEYk...kYYk..',
    'kYkkYEYk...kYEYk..',
    'kYEEYYk...kYEYkk..',
    '.kkYEYk..kYEYEEYk.',
    '...kYEYkkYEYkkkYEk',
    '....kYEEYYk....kYk',
    '.....kkYYk......kk',
    '.......kk.........',
]
FLASH = ['...Y...', '.E.Y.E.', '..YYY..', 'YYYwYYY', '..YYY..', '.E.Y.E.', '...Y...']
AURA = ['E.......', '.Y....E.', '........', 'Y.....Y.', '.E......']
LEG = [
    '...kkk.',
    '..kABBk',
    '.kABCk.',
    'kABCk..',
    'kBCk...',
    'kBCkk..',
    '.kBCk..',
    '.kBCk..',
    'kkCCk..',
    '.kkkk..',
]
LEGF = pix.flip_h(LEG)
LEGM = ['.kkk..', 'kABBk.', 'kBBCk.', 'kBBCk.', '.kBCk.', '.kBCk.', '..kBCk', '..kBCk', '..kBCk', '..kBCk', '.kCCkk', '.kkk..']

def layers():
    A = 'atk1|atk2'
    return [
        dict(n='legF1', g='legB', x=9, y=49, rows=dark(LEG)),
        dict(n='legF2', g='legA', x=24, y=47, rows=dark(LEGM)),
        dict(n='legF3', g='legB', x=41, y=49, rows=dark(LEGF)),
        dict(n='ely', g='body', x=3, y=30, rows=elytra(1),
             alt={'idle1|walk1|walk3': elytra(2), 'idle2|idle3|blink|atk0|atk1|atk2': elytra(3), 'hit|ko': elytra(0)}),
        dict(n='leg1', g='legA', x=5, y=49, rows=LEG),
        dict(n='leg2', g='legB', x=19, y=48, rows=LEGM),
        dict(n='pro', g='body', x=22, y=32, rows=PRO),
        dict(n='phorn', g='body', x=27, y=28, rows=PHORN),
        dict(n='horn', g='horn', x=42, y=15, rows=HORN),
        dict(n='head', g='head', x=31, y=32, rows=head(), alt={'blink': head('blink'), 'hit': head('hit'), 'atk0|atk1|atk2': head('glow'), 'ko': head('ko')}),
        dict(n='leg3', g='legA', x=36, y=49, rows=LEGF),
        dict(n='spark', g='horn', x=44, y=12, rows=SPARK['idle0|walk0|walk2'], alt=SPARK, not_='hit|ko|atk0|' + A),
        dict(n='aura', g='body', x=8, y=22, rows=AURA, only='atk0'),
        dict(n='aura2', g='horn', x=42, y=12, rows=pix.flip_h(AURA), only='atk0'),
        dict(n='bolt', g='horn', x=55, y=14, rows=BOLT, only=A),
        dict(n='flash', g='horn', x=67, y=20, rows=FLASH, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1), 'head': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1), 'head': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 2)},
    'atk1': {'root': (5, 0), 'head': (1, 0)},
    'atk2': {'root': (6, 0), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'horn': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'horn': 'head', 'head': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root'}
