# ムシャボロ（ゴースト・はがね × 中身の ない よろい武者）手打ち GBA風
EYE_BOX = (40, 31, 12, 3)
META = dict(id='mushaboro', name='ムシャボロ', types=['ghost', 'steel'], base='空の よろい武者', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2440',
    'S': '#d6deee', 'T': '#8a94b4', 'U': '#4c5272',
    'R': '#e4505a', 'r': '#8e2638',
    'Y': '#f8d45a', 'y': '#a8722a',
    'W': '#effff6', 'C': '#6ef2d2', 'D': '#24a0a4',
    'w': '#ffffff',
}
LIGHT = set('SYWCRw')

# デフォルメ（2〜3頭身）：かぶとは そのまま、胴・草摺・すね当てを 短く
# ---- かぶと（右向き 3/4）：鉢・ひさし・しころ（3段）・吹き返し・面頬 ----
HEAD = [
    '.........kkkkkkkk...........',
    '.......kkSSSSSSTTkk.........',
    '......kSSSSSTTTTTTUk........',
    '.....kSSSTTTTTTTTTUUk.......',
    '....kSSTTTTTTTTTTTUUUk......',
    '....kSTTTTTTTTTTTTUUUk......',
    '...kSSTTTTTTTTTTTUUUUUk.....',
    '...kSTTTTTTTTTTTTUUUUUk.....',
    '..kkkkkkkkkkkkkkkkkkkkkkkk..',
    '.kSSSSSSkYYkSSSSSSSSSSSSSTTk',
    '.kTTTTTkYYykTTTTTTTTTTUUUUUk',
    'kSSSSSSSkYykkkkkkkkkkkkkkkk.',
    'kRrRrRrRkykkkkkkkkkkkkkkk...',
    'kSSSSSSSSkkkkkkkkkkkkkkkk...',
    'kTTTTTTTTkkkkkkkkkSSSSTTk...',
    'kRrRrRrRrRkkkkkkkSSTTTUUUk..',
    'kSSSSSSSSSkkkkkkkkwkwkwUUk..',
    'kTTTTTUUUUkkkkkkkkkkkkkUk...',
    'kRrRrRrRrrkkkkkkTTwkwkwk....',
    '.kkkkkkkkkk..kkkkkkkkkkk....',
]
# J バイザー／スリット：からっぽの かぶとの 闇に、横一文字の 霊火の 切れ目が 1本。後ろは 細く 高く、前へ 太く 下がる（怒りの かたむき）。
# 芯は 白（W）→ 水色（C）→ 青緑（D）の にじみ。ひとみは なし
EYE = ['DCCWWCD......', '..DCCWWWWCCD.', '.......DDDD..']
EYE_ALT = {
    'blink': ['DDDDDD.......', '...DDDDDDDD..', '.............'],
    'atk0|atk1|atk2': ['CWWWWWC......', 'DCWWWWWWWWWC.', '..DDCCCCCCD..'],
    'hit': ['D.C.W.D......', '..D.CW.C.D...', '.......D.D...'],
}
# 鍬形（くわがた）の 金の 角
CREST = [
    'kk.........kk',
    'kYk.......kYk',
    'kYk.......kYk',
    'kYyk.....kYyk',
    '.kYk.....kYk.',
    '.kYyk...kYyk.',
    '..kYyk.kYyk..',
    '...kYYkYyk...',
    '...kYRRryk...',
    '....kyyyk....',
]
# 胴：おどし糸（赤）＋鋼の 板。胸に やぶれ穴 → 中の 霊火が 見える
TORSO = [
    '.....kkkkkkkkkkkk.....',
    '...kkSSSSSSSTTTTTkk...',
    '..kSSSSTTTTTTTTTTUUk..',
    '..kSSSSSkkkTTTTTTUUk..',
    '..kSTTTkCWCkTTTTUUUk..',
    '..kRrRkCWWDkRrrrrrrk..',
    '..kSSSkCWDkTTTTTTUUk..',
    '..kSTTTkDkTTTTTTUUUk..',
    '..kRrRrRkRrRrRrrrrrk..',
    '..kkkkkkkkkkkkkkkkkk..',
    '..kYYYYYYYyyyyyyyyyk..',
    '..kkkkkkkkkkkkkkkkkk..',
]
# 草摺（すそ広がり、すそは ぼろぼろ）
SKIRT = [
    '...kkkkkkkkkkkkkkkkkkkkkk...',
    '..kSSTTkSSSTTkSSSTTkSTTUUk..',
    '..kRrRrkRrRrrkRrRrrkRrrrrk..',
    'kSSTTTkSSTTTUkSTTTUkTTTUUUUk',
    'kTTUUUkTTUUUkkTUUUkkkUUUUkk.',
    '.kkk.kk.kkkk...kkk....kkk...',
]
# 大袖（前）と 後ろの 袖
SODE = [
    'kkkkkkkkkk..',
    'kSSSSSTTUUk.',
    'kRrRrRrrrrk.',
    'kSSSSTTTTUUk',
    'kRrRrRrrrrlk',
    '.kSSTTTTTUUUk',
    '.kRrRrrrrrlk.',
    '.kTTTTUUUUUUk',
    '..kkkkkkkkkk.',
]
SODE_B = [
    '.kkkkkkk',
    'kTTTTTUk',
    'krrrrrlk',
    'kTTTUUUk',
    'krrrrrlk',
    'kUUUUUUk',
    '.kkkkkk.',
]
# 前の うで（袖の 下は 霊火、籠手が 刀を にぎる）
ARM = [
    '.kCCk.......',
    'kCWWCk......',
    'kCWCDkkkk...',
    '.kkkkSSTUkk.',
    '...kSSTTTUUk',
    '...kTTTUUUUk',
    '....kkkkkkk.',
]
# 刀（ふだんは 右上へ かまえる）
SWORD = [
    '......................kk',
    '.....................kwk',
    '....................kwSk',
    '...................kwSTk',
    '..................kwSTk.',
    '.................kwSTk..',
    '................kwSTk...',
    '...............kwSTk....',
    '..............kwSTk.....',
    '.............kwSTk......',
    '............kwSTk.......',
    '...........kwSTk........',
    '..........kwSTk.........',
    '.........kwSTk..........',
    '.......kkYSTk...........',
    '......kYYyYk............',
    '....kkkyykk.............',
    '...kSSTUk...............',
    '..kSSTTUUk..............',
    '..kSTTUUUk..............',
    '..kTkrkUk...............',
    '.kkrkrkk................',
    'krkrkk..................',
    'kkkk....................',
]
# ため：刀を 肩の 上、後ろへ（八双）
SWORD_UP = [
    '.........k...',
    '........kwk..',
    '.......kCwSk.',
    '......kCWwSk.',
    '.....kCWCwSTk',
    '.....kCWCwSTk',
    '....kCWCDwSTk',
    '....kCWCDwSTk',
    '.....kCDkwSTk',
    '....kCWCkwSTk',
    '....kCWDkwSTk',
    '.....kCDkwSTk',
    '......kkkwSTk',
    '........kwSTk',
    '........kwSTk',
    '........kwSTk',
    '........kwSTk',
    '........kwSTk',
    '.......kkYYYkk',
    '.......kYyyyYk',
    '.....kkSSTTTUk',
    '....kSSSTTUUUk',
    '....kSTTTUUUk.',
    '.....kkkrkrk..',
    '.........krk..',
    '.........kk...',
]
# 決め：刀を 前へ 水平に
SWORD_FWD = [
    '.........kkkkkkkkkkkkkkkkkkk.',
    '.kk...kkkYkwwwwwwwwwwwwwwwwwk',
    'krkkkkSSkYkSSSSSSSSSSSSSSSkk.',
    'kkrkrkSSTkYkTTTTTTTTTTTTkk...',
    '.kkkkkTTUkkkkkkkkkkkkkkk.....',
    '.....kkkk....................',
]
# ふりぬき：刀を 前下へ
SWORD_DN = [
    '...kkkk..............',
    '..kSSTUkk............',
    '.kSSTTUkYk...........',
    'kkSTTUUkYYk..........',
    'krkkkkkkYyYkk........',
    'kkrk.....kkSwkk......',
    '..kk.......kTSwkk....',
    '.............kTSwkk..',
    '...............kkTSwk',
    '.................kkTk',
    '...................kk',
]
# すね当て（短く 太く。後ろ足は 後ろへ、前足は 前へ。上は 霊火で 草摺と つながる）
LEG_B = [
    '....kCCk..',
    '...kCWCDk.',
    '...kkkkkk.',
    '..kSSTUk..',
    '..kSTTUUk.',
    '.kSTTUUUk.',
    'kkkkkkkkk.',
    'kSSTTUUUkk',
    'kTUUUUUUUk',
    '.kkkkkkkk.',
]
LEG_A = [
    '.kCCk.......',
    '.kCWCDk.....',
    '.kkkkkkk....',
    '..kSSTUk....',
    '..kSTTUUk...',
    '...kSTTUUk..',
    '..kkkkkkkkk.',
    '..kSSTTTUUkk',
    '..kTTUUUUUUk',
    '...kkkkkkkk.',
]
# 霊火の 吹き流し（かぶとの 後ろから）
PLUME0 = [
    '..k.................',
    '.kCk................',
    '.kCk.......k........',
    'kCWCk.....kCk.......',
    'kCWCk....kCWk.......',
    '.kCWCk...kCWCk..k...',
    '.kCWWCk.kCWWCk.kCk..',
    '..kCWWCkkCWWCDkCWk..',
    '..kCWWWCkCWWCDkCWCk.',
    '...kCWWWCWWWCDCWWCk.',
    '...kCWWWWWWWCDCWCDk.',
    '....kCWWWWWWWCWWCDk.',
    '....kCCWWWWWWWWCDDk.',
    '.....kCCWWWWWWCCDDk.',
    '......kDCCCCCCCDDk..',
    '.......kkDDDDDDkk...',
    '.........kkkkkk.....',
]
PLUME1 = [
    '....................',
    'k...................',
    'kCk.........k.......',
    'kCk........kCk......',
    '.kCk......kCWk...k..',
    '.kCWCk....kCWCk.kCk.',
    '..kCWCk..kCWWCkkCWk.',
    '..kCWWCkkCWWCDkCWCk.',
    '..kCWWWCkCWWCDkCWCk.',
    '...kCWWWCWWWCDCWWCk.',
    '...kCWWWWWWWCDCWCDk.',
    '....kCWWWWWWWCWWCDk.',
    '....kCCWWWWWWWWCDDk.',
    '.....kCCWWWWWWCCDDk.',
    '......kDCCCCCCCDDk..',
    '.......kkDDDDDDkk...',
    '.........kkkkkk.....',
]
# 霊火の 斬撃（三日月）
SLASH = [
    'kkkkk.................',
    'kWWCCkkk..............',
    '.kkWWWCCkk............',
    '...kkWWWCCk...........',
    '.....kkWWWCk..........',
    '.......kWWWCk.........',
    '........kWWCDk........',
    '.........kWWCDk.......',
    '..........kWWCk.......',
    '..........kWWCDk......',
    '...........kWWCk......',
    '...........kWWCDk.....',
    '............kWCDk.....',
    '............kWCDk.....',
    '............kWCDk.....',
    '............kWCDk.....',
    '...........kWCDk......',
    '...........kCDk.......',
    '..........kCDk........',
    '.........kDkk.........',
    '.........kk...........',
]

# ダウン：中身が 抜けて よろいが くずれ落ちる
KO = [
    '..........................kkkkkkkk..........',
    '........................kkSSSSSSTTkk........',
    '.......................kSSSTTTTTTTUUk.......',
    '......................kSSTTTTTTTTTUUUk......',
    '......................kSTTTTTTTTTTUUUUk.....',
    '.....................kkkkkkkkkkkkkkkkkkkk...',
    '....................kSSSSSkSSSSSSSSSSSSTTk..',
    '...........kkkkkkkkkRrRrkkkkkkkkkkkkkkkkk...',
    '.........kkSSSSSSSTkSSSSkkCkCkkkkCkCkkkk....',
    '........kSSTTTTTTTTkRrRrkkkCkkkkkkCkkSSTk...',
    '........kRrRrRrRrrrkSSSSkkCkCkkkkCkCkTTUUk..',
    '........kSSSSSTTTTUkTTUUkkkkkkkkkkkkwkwkUk..',
    '......kkkRrRrRrrrrrkkkkkkkkkkkkkkkkkkkkkk...',
    '.....kSSTTkSSSTTkSSSTTkSTTUUk...............',
    '.....kRrRrkRrRrrkRrRrrkRrrrrk..kk...........',
    '....kSSTTTkSSTTTkSSTTTkSTTUUUkkYk...........',
    '....kTTUUUkTTUUUkTTUUUkTUUUUUkYykk..........',
    'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkykkYk.kk......',
    'kSSSTTTTUUkkSSSTTTTUUUkkkkkkkkkkkkkkkkkkkkk.',
    'kTTTUUUUUUkkTTTUUUUUUUkYkwSSSSSSSSSSSSSSSSSk',
    '.kkkkkkkkk..kkkkkkkkkkkkkTTTTTTTTTTTTTTTTkk.',
    '.........................kkkkkkkkkkkkkkkk...',
]
KO_WISP = ['..k..', '.kCk.', 'kCDk.', '.kDk.', '..kDk', '...k.']

def layers():
    return [
        dict(n='ko', g='root', x=12, y=39, rows=KO, only='ko'),
        dict(n='wisp', g='root', x=40, y=32, rows=KO_WISP, only='ko'),
        dict(n='plume', g='plume', x=17, y=14, rows=PLUME0, alt={'idle1|idle3|walk1|walk3|atk1|atk2': PLUME1}, not_='ko'),
                dict(n='sodeB', g='body', x=17, y=36, rows=SODE_B, not_='ko'),
        dict(n='legB', g='legB', x=15, y=51, rows=LEG_B, not_='ko'),
        dict(n='legA', g='legA', x=35, y=51, rows=LEG_A, not_='ko'),
        dict(n='skirt', g='body', x=17, y=46, rows=SKIRT, not_='ko'),
        dict(n='torso', g='body', x=21, y=35, rows=TORSO, not_='ko'),
        dict(n='sword', g='arm', x=40, y=23, rows=SWORD, not_='ko|atk0|atk1|atk2'),
        dict(n='head', g='head', x=29, y=20, rows=HEAD, not_='ko'),
        dict(n='eye', g='head', x=40, y=31, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='crest', g='head', x=39, y=14, rows=CREST, not_='ko'),
        dict(n='swordV', g='arm', x=46, y=24, rows=SWORD_UP, only='atk0'),
        dict(n='swordF', g='arm', x=44, y=42, rows=SWORD_FWD, only='atk1'),
        dict(n='swordD', g='arm', x=46, y=43, rows=SWORD_DN, only='atk2'),
        dict(n='sode', g='body', x=35, y=35, rows=SODE, not_='ko'),
        dict(n='arm', g='arm', x=38, y=42, rows=ARM, not_='ko'),
        dict(n='slash', g='fx', x=52, y=20, rows=SLASH, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'legA': (0, 0)},
    'idle2': {'body': (0, 1), 'plume': (0, -1)},
    'idle3': {'body': (0, 0), 'plume': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'arm': (2, -1), 'legA': (-1, 0)},
    'atk1': {'root': (3, 0), 'body': (1, 1), 'arm': (2, 2), 'legA': (2, 0)},
    'atk2': {'root': (5, 1), 'arm': (2, 2)},
    'hit': {'root': (-3, 0), 'body': (-1, 1), 'head': (-2, 0), 'arm': (-3, 3), 'plume': (-2, 1), 'legA': (-1, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'plume': 'head', 'arm': 'body', 'sword': 'arm', 'swordUp': 'arm', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
