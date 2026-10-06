# エンジャク（ほのお・ひこう(風) × 炎の 猛禽）手打ち GBA風
import pix
META = dict(id='enjaku', name='エンジャク', types=['fire', 'wind'], base='不死鳥', size='L')
PAL = {
    'k': '#101018', 'l': '#3c1620',
    'A': '#86728a', 'B': '#4c3e56', 'C': '#2a2234',
    'Y': '#fff2a0', 'O': '#ffb030', 'R': '#f05020', 'r': '#a01e24',
    'W': '#f2e2c4', 'V': '#b49a7c',
    'w': '#ffffff',
}
LIGHT = set('AYOWw')

HEAD = [
    'kkkk..................',
    'kWWWkkk...............',
    '.kVWWWWkkk............',
    '..kkVVWWWWkk..........',
    '....kkBAAAAAkk........',
    '....kBBAAAAAAAkk......',
    '...kBBAAkkkkkAABk.....',
    '...kBAkkYYYOkkAABk....',
    '..kBBBAkkkkkRkkkkkk...',
    '..kBBBBAAAkWWWWWWWWkk.',
    '.kBBBBBAAkWWWWWWWWWWWk',
    '.kCBBBBBkWWVVVVWWWWVWk',
    '.kCCBBBBkWkkkkkkVVVkVk',
    '..kCCBBBkVkWkWkWkkkkk.',
    '...kkCCBBkkkkkkkk.....',
    '.....kkkkk............',
]
BODY = [
    '......................kkkk......',
    '...................kkkBAAAk.....',
    '.................kkBBAAAAABk....',
    '...............kkBBBAAAAAABk....',
    '.............kkBBBBBAAAAABBk....',
    '...........kkBBBBBBBBAAAABBBk...',
    '.........kkBBBBBRBBBBBBAABBBk...',
    '........kBBBBBBBORBBBBBBBBBBCk..',
    '.......kBBBBBBBBBORBBBBBBBBBCk..',
    '......kBBBBBBBBBBBOBBBBBBBBCCk..',
    '.....kBBBBBBBBBBBBBBBBBRBBBCCk..',
    '....kBBBBBBBBBBBBBBBBBROBBCCCk..',
    '...kBBBBBBBBBBBBBBBBBBBOBCCCk...',
    '..kCBBBBBBBBBBBBBBBBBBBBCCCk....',
    '.kCCBBBBBBBBBBBBBBBBBBCCCCk.....',
    'kCCCBBBBBBBBBBBBBBBBCCCCkk......',
    'kCCCCBBBBBBBBBBBBCCCCCkk........',
    '.kkCCCCCCBBBBCCCCCCkk...........',
    '...kkkCCCCCCCCCCkkk.............',
    '......kkkkkkkkkk................',
]
TAIL0 = [
    '.....................kk.',
    '..................kkkRRk',
    '................kkROOOk.',
    '..............kkROYYOk..',
    '............kkROYYwOk...',
    '..........kkROYYYOkk....',
    '........kkROOYYOkk......',
    '.......kROOOOkkk........',
    '......kROOkk............',
    '.....kROk...............',
    '....kROk................',
    '....kROk................',
    '....kROOk...............',
    '.....kROOk..............',
    '......kROOkk............',
    '.......kRROOkk..........',
    '..k.....kkRROk..........',
    '.kRk......kROk..........',
    '..kRk....kROk...........',
    '...kRkkkROOk............',
    '....kRROOkk.............',
    '.....kkkk...............',
]
WING_UP = [
    '.......kk...kk..............',
    '......kYk..kYk..kk..........',
    '.....kYOk.kYOk.kYk...kk.....',
    '....kOOk.kOOk.kYOk..kYk.....',
    '...kROk.kROk.kOOk.kYOk......',
    '..kRRk.kRAk.kROk.kOOk.......',
    '.kRkAk.kAAkkRAk.kROk........',
    '.kkAAk.kABkkAAkkRAk.........',
    '..kABk.kABkkABkkAAkkkk......',
    '..kABBkkABBkABkkABkkAAk.....',
    '..kABBkkABBkABBkABBkRAAk....',
    '...kABBkkABBkABkkABkAAAk....',
    '...kABBBkABBkABBkABkAARBk...',
    '....kABBkkABBkABkABkAABOk...',
    '...kRkBBBkABBkABkABkAARBk...',
    '..kROkkBBkkABBkABkBkAABBk...',
    '..kOOOkkBBkABBkBBkBkAABBBk..',
    '..kYOOk.kBBkBBkBBkBkAABRBk..',
    '...kYOOkkkBkBBkBBkBkABBBOk..',
    '....kYOOOkkkBBkBBkkAABBRBk..',
    '.....kROOOOkkkkkkkkAABBBBk..',
    '......kRROOOOkCCCCkAABBBBBk.',
    '.......kkRROOkCCCkAABBBBBBk.',
    '.........kkRRkCCkAABBRBBBBk.',
    '...........kkkCkAABBBBORBCk.',
    '.............kkAABBBBBBBCCk.',
    '..............kABBBBBBBCCk..',
    '...............kkBBBBBCCk...',
    '.................kkkkkkk....',
]
TALON = [
    '..kBBk...',
    '..kBCCk..',
    '.kBCCCk..',
    'kWkkWkWk.',
    'kWVkWkWVk',
    '.kVkkVkkVk',
    '..k...k..k',
]

TAIL1 = pix.recolor([r[1:] + '.' for r in TAIL0], {})
def swept(rows):
    """あたり：上げた 翼を 45度ほど 後ろへ 倒した 形（行を 間引いて 上ほど 左へ ずらす）"""
    keep = [r for y, r in enumerate(rows) if y % 3 != 1]
    H = len(keep); out = []
    for y, r in enumerate(keep):
        sh = (H - 1 - y) * 2 // 3
        out.append('.' * 12 + r)
        out[-1] = out[-1][sh:] if sh else out[-1]
    w = max(len(r) for r in out); return [r.ljust(w, '.') for r in out]
WING_MID = swept(WING_UP)
WING_DN = pix.flip_v(WING_MID)
EYE = ['YYYO']
EYE_ALT = {'blink': ['kkkk'], 'atk0|atk1|atk2': ['wYYY'], 'hit': ['kYkk'], 'ko': ['OkOk']}
def dark(rows): return pix.recolor(rows, {'A': 'B', 'B': 'C', 'Y': 'O', 'O': 'R', 'R': 'r'})

GUST = [  # 攻撃：炎の つむじ風
    '........kkkk........',
    '.....kkkYYYOkk......',
    '...kkYYwwwYYOOkk....',
    '..kYwwkkkkkkYYOOk...',
    '.kYwkk......kkYORk..',
    '.kYk..........kYORk.',
    'kYOk...kkk.....kORk.',
    'kOOk..kYYOk....kORk.',
    'kOk..kYwOOk....kRk..',
    'kORk.kYOk.....kRRk..',
    '.kORk.kk....kkRRk...',
    '.kROOkk...kkROOk....',
    '..kRROOkkkROOkk.....',
    '...kkRRROOOkk.......',
    '.....kkkkkk.........',
]
UP, MID, DN = 'idle0|blink|walk0|atk0', 'idle1|idle3|walk1|walk3|atk2|hit|ko', 'idle2|walk2|atk1'

def layers():
    return [
        dict(n='wingB_up', g='wingB', x=18, y=0, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=9, y=8, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=9, y=24, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='tail', x=1, y=33, rows=TAIL0, alt={'idle1|idle3|walk1|walk3|atk1': TAIL1}),
        dict(n='body', g='body', x=17, y=22, rows=BODY),
        dict(n='talon', g='talon', x=31, y=40, rows=TALON),
        dict(n='head', g='head', x=40, y=8, rows=HEAD),
        dict(n='eye', g='head', x=48, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='wingF_up', g='wingF', x=9, y=2, rows=WING_UP, only=UP),
        dict(n='wingF_mid', g='wingF', x=0, y=10, rows=WING_MID, only=MID),
        dict(n='wingF_dn', g='wingF', x=0, y=26, rows=WING_DN, only=DN),
        dict(n='gust', g='fx', x=57, y=17, rows=GUST, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, 1)},
    'idle2': {'root': (0, 2), 'head': (0, -1), 'talon': (0, -1)},
    'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)},
    'walk1': {'root': (0, 0)},
    'walk2': {'root': (0, 1), 'talon': (-1, -1)},
    'walk3': {'root': (0, 0)},
    'atk0': {'root': (-3, -2), 'head': (-2, -1), 'talon': (1, 0)},
    'atk1': {'root': (3, 2), 'head': (2, 1), 'talon': (2, -1)},
    'atk2': {'root': (5, 2), 'head': (1, 1)},
    'hit': {'root': (-4, 0), 'head': (-1, -1), 'talon': (1, 0)},
    'ko': {'root': (-2, 9), 'head': (3, 6), 'talon': (0, -2)},
}
PARENT = {'head': 'body', 'tail': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
