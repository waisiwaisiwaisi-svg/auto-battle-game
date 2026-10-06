# カジキツルギ（はがね・みず × カジキ）手打ち GBA風
META = dict(id='kajikitsurugi', name='カジキツルギ', types=['steel', 'water'], base='カジキ', size='M')
PAL = {
    'k': '#101018', 'l': '#1a2440',
    'A': '#5e8edc', 'B': '#2c58a8', 'D': '#1a3470',
    'S': '#f0f4fa', 'T': '#a8b4c8', 'U': '#66728c',
    'c': '#a8f0ff', 'C': '#48a8e8',
    'Y': '#ffd040',
}
LIGHT = set('ASc')
KEEP_BLACK = set('YS')

# 体：背は 深い 青、腹は 鋼の うろこ（山形の 板）。えらぶたの 線
BODY = [
    '..............kkkkkkkkk............',
    '.............kAAAAAAAAAkkk.........',
    '..........kkkAAAAAAAAAAAAAkkk......',
    '.......kkkAAAABBBBBBBBBBAAAAAk.....',
    '.....kkAAAAABBBBBBBBBBBBBkBAAAkk...',
    '....kAAAABBBBBBBBBBBBBBBBkBBBBAAk..',
    '..kkAABBBBBBBBBBBBBBBBBBBBkBBBBBAk.',
    '.kAABBDDDDDDDDDDDDDDDDDDDDkDDDDDDBk',
    'kAADSSSSSSSSSSSSSSSSSSSSSSkSSSSSSTk',
    'kTTTTTUTTTTUTTTTUTTTTUTTTkTTTTTTUk.',
    '.kTTTUTUTTUTUTTUTUTTUTUTTkTTTTTUk..',
    '..kkTTTTUTTTTUTTTTUTTTTUkTTTTUUk...',
    '....kkkUUTTTTUTTTTUTTTUkTTUUkkk....',
    '.......kkkUUUUUTTTTUUUkUUkkk.......',
    '..........kkkkUUUUkkkkkk...........',
    '..............kkkk.................',
]
# 剣の くちばし：刀の ように 上の ふちが 光る
BILL = [
    'kkkkkkkkk...',
    'SSSSSSSSSkk.',
    'TTTTTTTTTSSk',
    'UUUUUUUUkkk.',
    'kTkkTkkTk...',
    '.k..k..k....',
]
# 頭の 鋼の かぶと（目の 上に ひさし）
HELM = [
    '...kkkkk...',
    '.kkSSSSTkk.',
    'kSSTTTTTTUk',
    'kkkkkkTTUUk',
    '......kkkk.',
]
# 帆の 背びれ：前が 高い 刃。鋼の すじが 通る
SAIL = [
    '..............kk...',
    '.............kASk..',
    '............kABTk..',
    '..........kkABBTk..',
    '........kkAABTBTk..',
    '......kkAABBTBBTk..',
    '....kkAABBTBBTBTUk.',
    '..kkAABBTBBTBBBTUk.',
    'kkAABBTBBTBBTBBBTUk',
    'kABBBTBBTBBTBBBBTUk',
    'kBBBTBBTBBTBBBBBBUk',
]
SAIL_UP = [  # 帆を 立てた（攻撃の ため）
    '...............kk..',
    '..............kASk.',
    '.............kABTk.',
    '...........kkABBTk.',
    '.........kkAABTBTk.',
    '.......kkAABBTBBTk.',
    '.....kkAABBTBBTBTUk',
    '...kkAABBTBBTBBBTUk',
    '.kkAABBTBBTBBTBBBTU',
    'kABBBTBBTBBTBBBBBTU',
    'kBBBTBBTBBTBBBBBBUk',
]
# 尾びれ：上は 青、下は 鋼。ふちが 刃
TAIL = [
    'kk........',
    'kSkk......',
    '.kSAkk....',
    '.kSABBkk..',
    '..kSABBDk.',
    '..kkSABBDk',
    '....kkABBk',
    '......kBBk',
    '......kBBk',
    '....kkTTUk',
    '..kkSTTUk.',
    '..kSTTUk..',
    '.kSTTUk...',
    '.kSTUk....',
    'kSUk......',
    'kk........',
]
# 胸びれ（鋼の 小刀）
PEC = [
    'kkkkk..',
    'kSTTUkk',
    '.kkTTUk',
    '...kkUk',
    '.....kk',
]
# 目：鋼の ひさしの 下で 光る 金の つり目
EYE = ['kkkk..', '.kYYkk', '..kkk.']
EYE_ALT = {'blink': ['kkkk..', '.kkkkk', '......'], 'atk0|atk1|atk2': ['kkkkk.', 'kYYYYk', '.kkkk.'], 'hit': ['kkkk..', '.kYkYk', '..kk..'], 'ko': ['kk.kk.', '..k...', 'kk.kk.']}
# 刃の きらめき（ため）
GLINT = ['...C...', '...S...', '..CSC..', 'CSSSSSC', '..CSC..', '...S...', '...C...']
# 突進の 水の すじ
SPEED = [
    'cCCCCCC.....',
    '............',
    '...cCCCCCCCC',
    '............',
    '.cCCCCC.....',
    '............',
    '....cCCCCCC.',
]
SPLASH = [
    '.c..c.',
    'c.cC..',
    '......',
    '......',
    '......',
    'c.cC..',
    '.c..c.',
]
def layers():
    return [
        dict(n='sail', g='sail', x=21, y=30, rows=SAIL, alt={'atk0|atk1|atk2': SAIL_UP}),
        dict(n='tail', g='tail', x=3, y=38, rows=TAIL),
        dict(n='body', g='body', x=12, y=39, rows=BODY),
        dict(n='bill', g='head', x=45, y=44, rows=BILL),
        dict(n='helm', g='head', x=37, y=39, rows=HELM),
        dict(n='eye', g='head', x=40, y=42, rows=EYE, alt=EYE_ALT),
        dict(n='pec', g='fin', x=33, y=51, rows=PEC),
        dict(n='glint', g='head', x=52, y=40, rows=GLINT, only='atk0'),
        dict(n='speed', g='root', x=-6, y=40, rows=SPEED, only='atk1|atk2'),
        dict(n='splash', g='head', x=56, y=42, rows=SPLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1), 'sail': (0, 0)},
    'blink': {},
    'walk0': {'tail': (0, -1), 'fin': (0, 1)}, 'walk1': {'root': (0, -1), 'sail': (-1, 0)}, 'walk2': {'tail': (0, 1), 'fin': (-1, 0)}, 'walk3': {'root': (0, -1)},
    'atk0': {'root': (-4, 0), 'tail': (0, -1), 'head': (0, 1)}, 'atk1': {'root': (8, 0)}, 'atk2': {'root': (11, 0), 'tail': (0, 1)},
    'hit': {'root': (-3, 1), 'head': (0, 1), 'tail': (0, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'sail': 'body', 'fin': 'body', 'tail': 'body', 'body': 'root'}
