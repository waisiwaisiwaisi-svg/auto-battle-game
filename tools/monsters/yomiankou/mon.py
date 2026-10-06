# ヨミアンコウ（ゴースト・みず × チョウチンアンコウ）手打ち GBA風
import pix
EYE_BOX = (34, 26, 8, 8)
META = dict(id='yomiankou', name='ヨミアンコウ', types=['ghost', 'water'], base='チョウチンアンコウ', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2238',
    'A': '#bccbe2', 'B': '#7a8ab2', 'D': '#4a5282',
    'r': '#2a0e2c', 'w': '#ffffff',
    'c': '#c8fff4', 'C': '#4ce0d0', 'N': '#2a8a9a',
    'P': '#8a5ab8',
}
LIGHT = set('Acw')
KEEP_BLACK = set('wcCNr')

# 体：まるい 頭と 胴（青白い 亡霊の 色）
BODY = [
    '.................kkkkkkkkkk.............',
    '..............kkkAAAAAAAAAAkkk..........',
    '............kkAAAAAAABBBBBAAAAkk........',
    '...........kAAAAAAABBBBBBBBBAABBk.......',
    '..........kAAAAAAABBBBBBBBBBBBBBDk......',
    '........kkAAAAAABBBBBBBBBBBBBBBBBDkk....',
    '.......kAAAAAABBBBBBBBBBBBBBBBBBBBDDk...',
    '.......kAAAAABBBBBBBBBBBBBBBBBBBBBDDk...',
    '......kAAAABBBBBBBBBBBBBBBBBBBBBBBBDDk..',
    '.....kAAAABBBBBBBBBBBBBBBBBBBBBBBBBDDDk.',
    '..kkkAAABBBBBBBBBBBBBBBBBBBBBBBBBDDDDDk.',
    '.kAAAAABBBBBBBBBBBBBBBBBBBBBBBBBDDDDDDk.',
    'kAAAAABBBBBBBBBBBBBBBBBBBBBBBBDDDDDDDDDk',
    'kAAAAABBBBBBBBBBBBBBBBBBBBBBBDDDDDDDDDDk',
    'kAAAAABBBBBBBBBBBBBBBBBBBBBDDDDDDDDDDDk.',
    'kAAAAAABBBBBBBBBBBBBBBBBBBDDDDDDDDDDkk..',
    'kAAAAAABBBBBBBBBBBBBBBBBDDDDDDDDDDkk....',
    'kAAAAAABBBBBBBBBBBBBBBDDDDDDDDDkkk......',
    'kAAAAAABBBBBBBBBBBBBBDDDDDDDDkk.........',
    '.kAAABBBBBBBBBBBBBBDDDDDDDDkk...........',
    '..kkkBBBBBBBBBBBBBDDDDDDDkk.............',
    '.....kkDBBBBBBBBDDDDDDDkk...............',
    '.......kDBBBBBDDDDDDDDDk................',
    '.......kDDDBBDDDDDDDDDDk................',
    '........kkDDDDDDDDDDDDDk................',
    '..........kDDDDDDDDDDDDk................',
    '...........kDDDDDDDDDDDk................',
    '............kkDDDDDDDDDk................',
    '..............kkkDDDDDDk................',
    '.................kkkkkk.................',
]
# 下あご：前へ つき出た 受け口
JAW = [
    '............................k..',
    '..........................kkDk.',
    '.........................kDDDk.',
    '.......................kkDDDDDk',
    '....................kkkBBDDDDDk',
    '..................kkBBBDDDDDDk.',
    '...............kkkBBBDDDDDDDDk.',
    '.............kkBBBBDDDDDDDDDk..',
    '..........kkkBBBBDDDDDDDDDDk...',
    '.......kkkBBBBBDDDDDDDDDDDDk...',
    '....kkkBBBBBBDDDDDDDDDDDDDk....',
    '...kBBBBBBBDDDDDDDDDDDDDDk.....',
    '..kBBBBBBDDDDDDDDDDDDDDDk......',
    '.kBBBBBDDDDDDDDDDDDDDDDk.......',
    '.kBBBDDDDDDDDDDDDDDDDkk........',
    '.kBDDDDDDDDDDDDDDDDDk..........',
    'kDDDDDDDDDDDDDDDDDDk...........',
    'kDDDDDDDDDDDDDDDkkk............',
    '.kkDDDDDDDDDDkkk...............',
    '...kkkDDDDkkk..................',
    '......kkkk.....................',
]
# 尾びれ：ぼろぼろに やぶれた 亡霊の ひれ
TAIL = [
    'kk..........',
    'kAkk........',
    '.kABkk......',
    '..kABBDkk...',
    '.kAkABBBDk..',
    'kAAABABBBDk.',
    '.kkABBBBBDk.',
    '...kABBBBDk.',
    '..kABBBBBDk.',
    '.kABBkBBBDk.',
    'kABkkBBBDk..',
    'kkk.kBBDDk..',
    '...kBDDkk...',
    '..kDDk......',
    '.kkk........',
]
# 背びれ・胸びれ（やぶれた 膜）
DFIN = [
    '.k...k....',
    'kAk.kAk...',
    'kABkABk.k.',
    '.kABBBkkAk',
    '.kBBBBBBBk',
    '..kBBBBBDk',
]
PFIN = [
    '....kkkk',
    '..kkABBk',
    '.kABBBDk',
    'kABkBDk.',
    'kBkkDDk.',
    'kk.kDk..',
    '...kk...',
]
# K 魚の 目：まぶたの ない まん丸の 目。白く にごった 目玉（A・左上に 白 w）、細い 青緑の 輪（N）の 中に 平たい 大きな ひとみが
# 霊火で 光る（C・芯は c）。まわりは 骨の ふち（D）
EYE = ['..DDDD..', '.DkkkkD.', 'DkwAAAkD', 'kwANNAAk', 'kANcCNAk', 'kANCCNDk', '.kANNDk.', '..kkkk..']
EYE_ALT = {
    'blink': ['..DDDD..', '.DkkkkD.', 'DkwAAAkD', 'kwAAAAAk', 'kAANNAAk', 'kAANNADk', '.kAAADk.', '..kkkk..'],
    'atk0|atk1|atk2': ['..DDDD..', '.DkkkkD.', 'DkwCCAkD', 'kwCccCAk', 'kCcwwcCk', 'kCcccCDk', '.kCccDk.', '..kkkk..'],
    'hit': ['..DDDD..', '.DkkkkD.', 'DkwAAAkD', 'kwAAAAAk', 'kAAAAANk', 'kAAAANDk', '.kAAADk.', '..kkkk..'],
    'ko': ['..DDDD..', '.DkkkkD.', 'DkwAAAkD', 'kAkAkAAk', 'kAAkAAAk', 'kAkAkADk', '.kAAADk.', '..kkkk..'],
}
# 口の 中（暗い 紫）
def _maw():
    g = pix.grid(26, 18)
    pix.poly(g, [(0, 11), (22, 1), (25, 2), (25, 12), (16, 16), (2, 17)], 'r')
    return pix.outline(pix.rows_of(g))
MAW = _maw()
# 牙：上あごから 下へ、下あごから 上へ のびる 針の 牙（x, 上, 下）
def teeth(spec, W, H):
    g = pix.grid(W, H)
    for x, y0, y1 in spec:
        for y in range(y0, y1 + 1):
            g[y][x] = 'w'; g[y][x + 1] = 'k' if g[y][x + 1] != 'w' else 'w'
        # つけ根は 太く（先ほど 細い 針）
        yb = y1 if y0 < 3 or W == 19 else y0
        if W == 19: g[y1][x - 1] = 'w'; g[y1 - 1][x - 1] = 'w' if y1 - 1 > y0 else g[y1 - 1][x - 1]
        else: g[y0][x - 1] = 'w' if x > 0 else g[y0][x - 1]
    return pix.rows_of(g)
UTEETH = teeth([(2, 0, 2), (6, 0, 2), (10, 0, 3), (14, 0, 2)], 17, 4)          # 体の 口の ふちから
LTEETH = teeth([(2, 8, 10), (6, 6, 9), (10, 4, 7), (14, 2, 6), (17, 0, 4)], 19, 11)  # 下あごの ふちから
# 頭の ちょうちん：茎と 魂の 火
LURE = [
    '.....kkkkk....',
    '...kkBBBBBkk..',
    '..kBkkkkkkBBk.',
    '.kBk......kBk.',
    '.kBk.......kBk',
    'kBk........kBk',
    'kBk.........kk',
    'kBk...........',
    'kBk...........',
    'kBk...........',
    '.kBk..........',
    '.kBk..........',
    '.kBk..........',
    '..kk..........',
]
FLAME = [
    '...k...',
    '..kck..',
    '..kcCk.',
    '.kcwcCk',
    'kcwwcCk',
    'kCcwcNk',
    '.kCCNk.',
    '..kkk..',
]
FLAME2 = [
    '.......',
    '..kk...',
    '.kcCk..',
    '.kcwCk.',
    'kcwwcCk',
    'kCcwcNk',
    '.kCCNk.',
    '..kkk..',
]
FLAME_BIG = [
    '....k....',
    '...kck...',
    '..kcwck..',
    '.kcwwcCk.',
    'kcwwwwcCk',
    'kcwwwwcNk',
    'kCcwwcCNk',
    '.kCCCCNk.',
    '..kkkkk..',
]
# 側線の 霊火の 点（亡霊の しるし）
DOTS = ['C...C...C...C', '.............']
# 泡と 霊気
BUB = [['..c.', '.c.c', '..c.', '....', '.N..'], ['....', '..c.', '.c.c', '..c.', '....']]
WISP = [
    '..N....C..',
    '.CcN..CcN.',
    'NcwcNNcwcN',
    '.CcN..CcN.',
    '..N....C..',
]
# まわりを ただよう 人魂（ひとだま）
SOUL = ['..k..', '.kck.', 'kcwCk', 'kCcNk', '.kNk.', '..kk.', '...k.']
SOUL2 = ['.k...', 'kck..', 'kcwCk', 'kCcNk', '.kNk.', '.kk..', '.k...']
def layers():
    return [
        dict(n='tail', g='tail', x=4, y=28, rows=TAIL),
        dict(n='dfin', g='body', x=17, y=22, rows=DFIN),
        dict(n='lure', g='lure', x=34, y=12, rows=LURE),
        dict(n='maw', g='body', x=29, y=34, rows=MAW),
        dict(n='body', g='body', x=9, y=24, rows=BODY),
        dict(n='dots', g='body', x=15, y=36, rows=DOTS),
        dict(n='eye', g='body', x=34, y=26, rows=EYE, alt=EYE_ALT),
        dict(n='ut', g='body', x=32, y=41, rows=UTEETH),
        dict(n='jaw', g='jaw', x=27, y=34, rows=JAW),
        dict(n='lt', g='jaw', x=35, y=30, rows=LTEETH),
        dict(n='pfin', g='fin', x=21, y=41, rows=PFIN),
        dict(n='flame', g='lure', x=44, y=18, rows=FLAME, alt={'idle1|idle3|walk1|walk3': FLAME2, 'atk0|atk1': FLAME_BIG}),
        dict(n='bub', g='root', x=10, y=17, rows=BUB[0], alt={'idle2|idle3|walk2|walk3': BUB[1]}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='soul', g='tail', x=6, y=47, rows=SOUL, alt={'idle1|idle3|walk1|walk3': SOUL2}, not_='ko|atk1'),
        dict(n='wisp', g='jaw', x=52, y=40, rows=WISP, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'jaw': (0, 1), 'tail': (0, 1)}, 'idle3': {'lure': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1), 'fin': (0, 1)}, 'walk1': {'root': (0, -1)}, 'walk2': {'tail': (0, 1), 'fin': (-1, 0)}, 'walk3': {'root': (0, -1), 'lure': (0, 1)},
    'atk0': {'root': (-3, 0), 'lure': (0, -1), 'tail': (0, -1)}, 'atk1': {'root': (5, 0), 'jaw': (0, 6), 'lure': (1, -1)}, 'atk2': {'root': (7, 0), 'jaw': (0, 2)},
    'hit': {'root': (-3, -1), 'jaw': (0, 1), 'lure': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'jaw': 'body', 'lure': 'body', 'fin': 'body', 'tail': 'body', 'body': 'root'}
