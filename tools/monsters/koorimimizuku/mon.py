# コオリミミズク（こおり・ひこう(風) × ミミズク）手打ち GBA風
import pix
META = dict(id='koorimimizuku', name='コオリミミズク', types=['ice', 'wind'], base='ミミズク', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2a4c',
    'W': '#f4f8ff', 'I': '#b4e2f8', 'J': '#6aa8d8', 'K': '#3a64a0',
    'N': '#5a6894', 'M': '#343e66',
    'E': '#a6fff2', 'G': '#cdbf9c', 'g': '#7a6a52',
}
LIGHT = set('WIEG')

HEAD = [
    'k.....................',
    'kWk................k..',
    'kIWkk.............kWk.',
    '.kJIWkk..........kWIk.',
    '..kJIWIkk......kkWIJk.',
    '...kkJIWNkkkkkkWIJkk..',
    '...kNNNNNNNNNNNNNkk...',
    '..kNNNNNNNNNNNNNNNk...',
    '.kNMMMMMMNNNNMMMMMNk..',
    '.kNMMkkkkkMMMMkkkMNk..',
    '.kNMkEEEEWkMMkEEWkNk..',
    'kNNkEEkEkWkgkEkkNNk...',
    'kNNWkkkkWkgGgkkWNk....',
    'kMNNWWWWWWgGgWWNNk....',
    '.kMNNWWWWWWgWWNNk.....',
    '..kMMNNWWWWWNMMk......',
    '...kkMMMMMMMMkk.......',
    '.....kkkkkkkk.........',
]
EYEN = ['WEEkk', 'EkEEk']
EYEN_ALT = {'blink': ['kkkkk', 'NNNNk'], 'atk0|atk1|atk2': ['WWWWk', 'WkWWk'], 'hit': ['kEkkk', 'EkEkk'], 'ko': ['EkEkk', 'kEkEk']}
EYEF = ['kE', 'Ek']
EYEF_ALT = {'blink': ['kk', 'WW'], 'atk0|atk1|atk2': ['WW', 'Ek'], 'hit|ko': ['kE', 'Ek']}
BODY = [
    '..............kkkkk.....',
    '...........kkkNNNNIk....',
    '.........kkNNNNNIWWIk...',
    '.......kkNNNNNNIWWWWk...',
    '.....kkNNNNNMNNIWJWWIk..',
    '....kNNNNMNNNNNIWWWJWk..',
    '...kNNNNNNNMNNNIJWWWWIk.',
    '..kNNMNNNNNNNNIWWJWWJIk.',
    '.kNNNNNNMNNNNNIWWWWJWIk.',
    '.kMNNNNNNNNNMNIJWWJWIJk.',
    'kMMNNNNNNNNNNNJIWWWIJk..',
    'kMMMNNNNNNNNNMJIIJIJk...',
    '.kMMMMNNNNNNMMJJJJk.....',
    '..kkMMMMMMMMMkkkkk......',
    '....kkkkkkkkk...........',
]
TALON = [
    '.kIJk..kIJk..',
    '.kJKk..kJKk..',
    'kMMMMk.kMMMMk',
    'kMkMkM.kMkMkM',
    'k.k.k..k.k.k.',
]
# 翼：紺の 雨覆いの 下に、つららの 刃の 羽が たれる（横に ひろげた 形を 手で）
WING_MID = [
    '.......................kkkkkkkkkkkkkkk...',
    '..................kkkkkNNNNNNNNNNNNNNNk..',
    '.............kkkkNNNNNNNNNNNNNNNNNNNNNNk.',
    '.........kkkkNNNNIJNNNNNIJNNNNNIJNNNNNNMk',
    '.....kkkkNNNNNNNNNNNIJNNNNNNNNNNNNIJNNMMk',
    '..kkkNNNNIJNNNNNIJNNNNNNNNNIJNNNNNNNNMMk.',
    '.kNNNNkkkkkkkkkkkkkkkkkkkkkkkkkkkkkMMMk..',
    'kWIJkWIJJkWIJJkWIJJkWIJJkWIJJkWIJJkMMk...',
    'kWIJkWIJJkWIJJkWIJJkWIJJkWIJJkWIJJkkk....',
    '.kWJkkWIJkkWIJkkWIJkkWIJkkWIJkkWIJk......',
    '.kWJk.kWJk.kWJk.kWJk.kWJk.kWJk.kWJk......',
    '..kJk..kJk..kJk..kJk..kJk..kJk..kJk......',
    '..kKk..kKk..kKk..kKk..kKk..kKk..kk.......',
    '...k....k....k....k....k....k............',
]
def shear(rows, k):
    """あたり：翼の 角度を 変える（左の 列ほど 上(k>0)／下(k<0)へ ずらす）"""
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); m = int((W - 1) * abs(k))
    out = pix.grid(W, H + m)
    for x in range(W):
        sft = int((W - 1 - x) * abs(k))
        for y in range(H):
            if g[y][x] != '.':
                ny = y + (m - sft if k > 0 else sft)
                out[ny][x] = g[y][x]
    return pix.rows_of(out)
WING_UP = shear(WING_MID, 0.45)
WING_DN = shear(WING_MID, -0.3)
def dark(rows): return pix.recolor(rows, {'W': 'I', 'I': 'J', 'J': 'K', 'N': 'M'})
MH = len(WING_UP) - len(WING_MID)

TAIL = [
    '.......kk',
    '.....kkIJk',
    '...kkWIJk.',
    '.kkWIJJk..',
    'kWIJJkk...',
    '.kkkk.....',
]
SHARD = ['kk..........', 'kWWkkk......', '.kWIIIJkkk..', '..kkIJJJKKk.', '....kkkJKk..', '.......kk...']
def volley(pts):
    g = pix.grid(34, 22)
    for (x, y) in pts: pix.stamp(g, SHARD, x, y)
    return pix.rows_of(g)
VOLLEY1 = volley([(0, 1), (9, 8), (1, 15)])
VOLLEY2 = volley([(10, 0), (20, 8), (12, 15)])
FROST = ['..k.....k..', '.kWk...kIk.', 'kWEWk.kIWIk', '.kWk...kIk.', '..k.....k..']
UP, MID, DN = 'idle0|blink|walk0|atk0', 'idle1|idle3|walk1|walk3|atk2|hit|ko', 'idle2|walk2|atk1'
def layers():
    # 肩（翼の 右上）を 体の 背中 (36, 29) あたりに あわせる
    return [
        dict(n='wingB_up', g='wingB', x=3, y=26 - MH, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=3, y=24, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=3, y=25, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='body', x=10, y=38, rows=TAIL),
        dict(n='body', g='body', x=18, y=28, rows=BODY),
        dict(n='talon', g='talon', x=31, y=42, rows=TALON),
        dict(n='wingF_up', g='wingF', x=-5, y=29 - MH, rows=WING_UP, only=UP),
        dict(n='wingF_mid', g='wingF', x=-5, y=28, rows=WING_MID, only=MID),
        dict(n='wingF_dn', g='wingF', x=-5, y=28, rows=WING_DN, only=DN),
        dict(n='head', g='head', x=26, y=12, rows=HEAD),
        dict(n='frost', g='head', x=24, y=6, rows=FROST, only='atk0'),
        dict(n='volley1', g='fx', x=46, y=19, rows=VOLLEY1, only='atk1'),
        dict(n='volley2', g='fx', x=42, y=19, rows=VOLLEY2, only='atk2'),
        dict(n='eyeN', g='head', x=30, y=22, rows=EYEN, alt=EYEN_ALT),
        dict(n='eyeF', g='head', x=39, y=22, rows=EYEF, alt=EYEF_ALT),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, 1)},
    'idle2': {'root': (0, 2), 'talon': (0, -1)},
    'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)},
    'walk1': {},
    'walk2': {'root': (0, 1), 'talon': (0, -1)},
    'walk3': {},
    'atk0': {'root': (-3, -3), 'head': (-1, 0)},
    'atk1': {'root': (2, 0), 'head': (2, 1), 'talon': (2, 0)},
    'atk2': {'root': (3, 0), 'head': (1, 1)},
    'hit': {'root': (-4, 0), 'head': (-2, -1), 'talon': (1, 0)},
    'ko': {'root': (-2, 10), 'head': (3, 3), 'talon': (0, -3)},
}
PARENT = {'head': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
