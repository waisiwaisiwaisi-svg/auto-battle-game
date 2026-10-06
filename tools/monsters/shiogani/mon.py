# シオガニ（みず・いわ × カニ）手打ち GBA風
import pix
META = dict(id='shiogani', name='シオガニ', types=['water', 'rock'], base='カニ', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2a48',
    'R': '#d2cab8', 'Q': '#8e857c', 'P': '#4e4652',      # 岩 明・中・暗
    'C': '#ffa48e', 'D': '#e05a72', 'E': '#8c2a50',      # サンゴ
    'B': '#74c0f0', 'N': '#2f72b8', 'M': '#1c3c74',      # 体（深い 海の 青）
    'W': '#d8f8ff', 'Y': '#ffe45c', 'w': '#ffffff',
}
LIGHT = set('RCBWYw')
KEEP_BLACK = set('wY')

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
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'B': 'N', 'N': 'M', 'M': 'l', 'C': 'D', 'D': 'E'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 甲羅：ごつごつの 岩の ドーム。前の 面に 顔（岩の まゆ・つり目・牙）----
SHELL_M = [
    '..........#....#.....#.........',
    '.........###..###...###.#......',
    '.......##########.######.#.....',
    '.....#######################...',
    '...##########################..',
    '..############################.',
    '.#############################.',
    '###############################',
    '###############################',
    '###############################',
    '###############################',
    '###############################',
    '###############################',
    '.#############################.',
    '..###########################..',
    '....#######################....',
]
SHELL_D = [
    '...............................',
    '..........R....R.....R.........',
    '...............................',
    '...............................',
    '............Pl.......R.........',
    '.....R.......P.....RPl.........',
    '...........llP.....Pl..........',
    '...kRk......P..................',
    '...RPR.....lP..................',
    '....P......P...................',
    '..........lP...................',
    '........ll.....................',
    '...............................',
    '..lllllllllllllllllllllllllll..',
    '...PPPPPPPPPPPPPPPPPPPPPPPPPP..',
]
# 顔：岩の まゆが 前へ 下がり、その 下で 黄色い つり目が 光る
FACE = [
    '........kk..',
    '.....kkkRRk.',
    '...kkRRRQQPk',
    '.kkRRQQQQPPk',
    'kRQQPPkkkkkk',
    'kkkkk.......',
    '............',
    '............',
    '.....k...k..',
    '.....kw.kwk.',
    '......k..k..',
]
EYE = ['kkYYYYYkYk', 'QkkYYYYkk.', 'QQkkkkk...']
EYE_ALT = {'blink': ['kkkkkkkkkk', 'QQkkkkkk..', 'QQQQQ.....'], 'atk0|atk1|atk2': ['kYYYYYYYYk', 'QkYYYYYYk.', 'QQkkkk....'],
           'hit': ['kkYkkkkYkk', 'QkkYYYYkk.', 'QQkkkkk...'], 'ko': ['kkYkYkkkkk', 'QkkYkkk...', 'QQkYkYk...']}
def shell():
    rows = put(shade(SHELL_M, 'R', 'Q', 'P', t=3, lf=2, r=3, b=3), SHELL_D)
    return pix.outline(rows)
BELLY = [
    '.kkkkkkkkkkkkkkkkkkkkkkk.',
    'kBNNNNNNNNNNNNNNNNNNNNNMk',
    '.kMMMMMMMMMMMMMMMMMMMMMk.',
    '..kkkkkkkkkkkkkkkkkkkkk..',
]
CORAL = [
    '.k...k..',
    'kCk.kCk.',
    'kCk.kDk.',
    '.kCkDk..',
    '.kCDDk.k',
    '..kDEkCk',
    '..kDEDk.',
    '..kDEk..',
]
CORAL2 = [
    '..k...',
    '.kCk.k',
    '.kCkCk',
    'k.kDDk',
    'CkCDEk',
    'kCDEk.',
    '.kDEk.',
]
# ---- 大ばさみ：岩の 粉砕ばさみ。上の 指は 太く 長く、先が 下へ 曲がる ----
CLAW = [
    '...kkkkkkkk.............',
    '..kRRRRRRRRkkkkkk.......',
    '.kRRQQQQQQQRRRRRRkkkk...',
    'kRRQQQQQQQQQQQQQQRRRRkk.',
    'kRQQQQlQQQQQQQQQQQQQQPPk',
    'kRQQQlQQQQQQkRkQQQQQPPPk',
    'kRQQQQQQQQQQRPRkkkkkkPPk',
    'kRQQQQQQQQQkkPkwkwkwkkPk',
    'kQQQQQQQQQk.........kPk.',
    'kQQQQQQQQQk..........k..',
    'kQQQQQQQQQQk.....kk.....',
    'kQQQRkQQQQQkwkwkwRk.....',
    'kQQRPRQQQQQQkkkkRPk.....',
    'kPQQPQQQQQQQQQQQQRPk....',
    '.kPQQQQQQQQQQQQPPPPk....',
    '.kPPPQQQQQQPPPPPkkk.....',
    '..kkkPPPPPPPkkkk........',
    '.....kkkkkkk............',
]
ARM = [
    '...kkk..',
    '..kBBNk.',
    '.kBNNMk.',
    'kBNNMk..',
    'kNMMk...',
    '.kkk....',
]
ARM_UP = [
    '...kk...',
    '..kBNk..',
    '..kNMk..',
    '..kBNk..',
    '..kNMk..',
    '.kBNMk..',
    '.kNMk...',
    'kBNMk...',
    'kNMk....',
    'kNMk....',
    'kNMk....',
    '.kk.....',
]
ARM_FWD = [
    '.kkkkkkkk.',
    'kBBBNNNNNk',
    'kNNNNMMMMk',
    '.kkkkkkkk.',
]
# 足：つけ根から ひざを 立て、先の とがった 足先で 立つ
LEG = [
    '......kkkk.......',
    '.....kBBBNkkk....',
    '....kBNNNNNNNkkk.',
    '....kNNkkkkMMNNNk',
    '...kBNk....kkMMMk',
    '...kNMk......kkk.',
    '...kNMk..........',
    '...kNMk..........',
    '..kBNk...........',
    '..kNMk...........',
    '..kNMk...........',
    '.kBNk............',
    '.kNMk............',
    '.kNMk............',
    'kBNk.............',
    'kNMk.............',
    'kMk..............',
    'kk...............',
]
LEGF = pix.flip_h(LEG)
BUB = {'idle0|blink|walk0|walk2': ['.kk.', 'kWWk', 'kWBk', '.kk.'], 'idle1|walk1|walk3': ['..kk.', '.kWk.', '..k..', 'W....'],
       'idle2': ['...W', '.kk.', 'kWBk', '.kk.'], 'idle3': ['.kk.', 'kWWk', '.kk.', '....']}
SPLASH = [
    '...W.......W......',
    '.W.kW...W.kW...W..',
    '..kWBk.kWWBk.kWk..',
    '.kWBBNkWBBNNkWBNk.',
    'kWBNNNkBNNNMkBNNMk',
    '.kkkkkkkkkkkkkkkk.',
]
SHARDS = ['.kk.....', 'kRQk..kk', '.kk..kRk', '......k.', '..kk....', '.kRQk...', '..kk....']

def layers():
    NA = 'atk0|atk1|atk2'
    return [
        dict(n='legF1', g='legB', x=5, y=39, rows=dark(LEG)),
        dict(n='legF2', g='legA', x=13, y=39, rows=dark(LEG)),
        dict(n='legF3', g='legA', x=26, y=39, rows=dark(LEGF)),
        dict(n='coral1', g='body', x=7, y=19, rows=CORAL),
        dict(n='coral2', g='body', x=18, y=17, rows=CORAL2),
        dict(n='coral3', g='body', x=27, y=21, rows=dark(CORAL2)),
        dict(n='shell', g='body', x=5, y=23, rows=shell()),
        dict(n='face', g='body', x=25, y=26, rows=FACE),
        dict(n='eye', g='body', x=26, y=31, rows=EYE, alt=EYE_ALT),
        dict(n='belly', g='body', x=10, y=39, rows=BELLY),
        dict(n='leg1', g='legA', x=0, y=41, rows=LEG),
        dict(n='leg2', g='legB', x=7, y=41, rows=LEG),
        dict(n='leg3', g='legA', x=14, y=41, rows=LEG),
        dict(n='leg4', g='legB', x=22, y=41, rows=LEGF),
        dict(n='arm', g='body', x=31, y=40, rows=ARM, not_=NA),
        dict(n='armU', g='body', x=34, y=30, rows=ARM_UP, only='atk0'),
        dict(n='armF', g='body', x=31, y=41, rows=ARM_FWD, only='atk1|atk2'),
        dict(n='claw', g='claw', x=34, y=37, rows=CLAW),
        dict(n='ctuft', g='claw', x=37, y=34, rows=CORAL2),
        dict(n='bub', g='body', x=40, y=31, rows=BUB['idle0|blink|walk0|walk2'], alt=BUB, not_=NA + '|hit|ko'),
        dict(n='splash', g='claw', x=36, y=52, rows=SPLASH, only='atk1|atk2'),
        dict(n='shards', g='claw', x=56, y=40, rows=SHARDS, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'claw': (0, 1)},
    'idle3': {'claw': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1), 'claw': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1), 'claw': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'claw': (3, -17)},
    'atk1': {'root': (3, 0), 'body': (1, 0), 'claw': (6, 0)},
    'atk2': {'root': (3, 0), 'body': (1, 0), 'claw': (6, 0)},
    'hit': {'root': (-3, 0), 'body': (0, 1), 'claw': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'claw': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root'}
