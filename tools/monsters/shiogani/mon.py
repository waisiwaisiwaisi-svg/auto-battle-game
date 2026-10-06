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
# 顔：甲羅の 前の 面。目の 柄（2本）の 先に 岩の まぶた＋黄色い つり目（たての ひとみ）
STALK = [
    '..kkkk.',
    '.kRRRRk',
    'kRQQQPk',
    'kkkkkkk',
    'kYYYkYk',
    '.kkkkk.',
    '..kBNk.',
    '..kBNk.',
    '..kNMk.',
    '..kNMk.',
    '..kNMk.',
]
EYEL = ['YYYkY']
EYEL_ALT = {'blink': ['kkkkk'], 'atk0|atk1|atk2': ['wYYkY'], 'hit': ['kYkkk'], 'ko': ['YkYkY']}
# 口：岩の 口板と 左右に ひらく 大あご（白い 牙）
MOUTH = [
    'kkkkkk..',
    'kQQQPPk.',
    'kkkkkkkk',
    'kwkPkwk.',
    'kNkkkNk.',
    'kBNkkBNk',
    '.kk..kk.',
]
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
# ---- 大ばさみ（ふりあげて 前へ むける）：手のひらは まるく、上下の 指の あいだに すき間、内がわに 岩の こぶ ----
CLAW = [
    '...............kk.......',
    '..............kREk......',
    '....kk.......kRQEk......',
    '...kEk.......kRQQEk.....',
    '...kRk......kRQQQPk.....',
    '...kRPk.....kRQQQQPk....',
    '...kRQPk....kRQQQQPk....',
    '...kRQRk...kRRQQQQPk....',
    '...kRQQPk..kRQQQQQQPk...',
    '...kRQQRk..kRQQQQQQPk...',
    '...kRQQQPkkRRQQQQQQPk...',
    '...kRQQQRkRRQQQQQQQPPk..',
    '..kRRQQQQRRQQQQQQQQPPk..',
    '.kRRQQQQQQQQQQQQQQQPPk..',
    'kRRQQQQQQQQQQQQQQQQPPk..',
    'kRQQkRQQQQQQQQQQQQPPPk..',
    'kRQQRPQQlQQQQQQkRQPPPk..',
    'kRQQQQQQQlQQQQQRPQPPk...',
    'kQQQQQQQQQlQQQQQQPPPk...',
    'kQQQQQQQQQQQQQQQQPPPk...',
    '.kPQQQQQQQQQQQQPPPPk....',
    '..kPPQQQQQQQQPPPPkk.....',
    '...kkPPPPPPPPPPkk.......',
    '.....kkkkkkkkkk.........',
]
CLAW_SLAM = pix.rot90(CLAW)
# 腕：甲羅の 前から ななめ上へ（関節で 2本に わかれる）
ARM = [
    '........kkkk',
    '.......kBBNk',
    '......kBBNMk',
    '.....kBBNMk.',
    '.....kNNMMk.',
    '....kkkkkkk.',
    '....kBBNNk..',
    '...kBBNMMk..',
    '...kBNNMk...',
    '..kBNNMk....',
    '..kNNMMk....',
    '.kBNNMk.....',
    '.kNMMk......',
    'kkkkk.......',
]
ARM_FWD = [
    '.......kkkkkk',
    '..kkkkkBBBNNk',
    '.kBBBNNkNNMMk',
    'kBNNNMMk.kkkk',
    'kNMMMMk......',
    '.kkkkk.......',
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
    NA = 'atk1|atk2'
    return [
        dict(n='stalkF', g='head', x=27, y=15, rows=dark(STALK)),
        dict(n='legF2', g='legB', x=15, y=40, rows=dark(LEG)),
        dict(n='coral1', g='body', x=6, y=20, rows=CORAL),
        dict(n='coral2', g='body', x=16, y=18, rows=CORAL2),
        dict(n='coral3', g='body', x=23, y=21, rows=dark(CORAL2)),
        dict(n='stalk', g='head', x=31, y=14, rows=STALK),
        dict(n='eyeF', g='head', x=28, y=19, rows=['YYkY'], alt={'blink': ['kkkk'], 'hit': ['kYkk'], 'ko': ['YkYk']}),
        dict(n='eye', g='head', x=32, y=18, rows=EYEL, alt=EYEL_ALT),
        dict(n='arm', g='body', x=37, y=22, rows=ARM[:10] + ['.kkkk.......'], not_=NA),
        dict(n='armF', g='body', x=35, y=34, rows=ARM_FWD, only=NA),
        dict(n='shell', g='body', x=5, y=24, rows=shell()),
        dict(n='mouth', g='head', x=37, y=31, rows=MOUTH),
        dict(n='belly', g='body', x=9, y=40, rows=BELLY),
        dict(n='leg1', g='legA', x=0, y=42, rows=LEG),
        dict(n='leg2', g='legB', x=11, y=42, rows=LEG),
        dict(n='leg3', g='legA', x=21, y=42, rows=LEGF),
        dict(n='claw', g='claw', x=38, y=0, rows=CLAW, not_=NA),
        dict(n='clawS', g='claw', x=46, y=26, rows=CLAW_SLAM, only=NA),
        dict(n='bub', g='head', x=46, y=30, rows=BUB['idle0|blink|walk0|walk2'], alt=BUB, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='splash', g='fx', x=46, y=48, rows=SPLASH, only=NA),
        dict(n='shards', g='fx', x=56, y=38, rows=SHARDS, only='atk2'),
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
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'claw': (-1, -1)},
    'atk1': {'root': (2, 0)},
    'atk2': {'root': (3, 0), 'claw': (1, 0)},
    'hit': {'root': (-3, 0), 'body': (0, 1), 'claw': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'claw': 'root', 'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
