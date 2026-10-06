# キバザメ（みず・あく × サメ）手打ち GBA風
EYE_BOX = (41, 24, 8, 7)
META = dict(id='kibazame', name='キバザメ', types=['water', 'dark'], base='サメ', size='L')
PAL = {
    'k': '#101018', 'l': '#1c1d3a',
    'A': '#7a86ba', 'B': '#474e84', 'D': '#282b52',
    'E': '#d6dce6', 'F': '#8e97b2',
    'U': '#f0e6c8', 'V': '#b6a47e', 'X': '#6c5a44',
    'w': '#ffffff',
    'R': '#ff4a3a', 'r': '#a0142c',
    'c': '#a8f2ff', 'C': '#3a96d8',
}
LIGHT = set('AEUwc')
KEEP_BLACK = set('wRr')

# 尾びれ：上が 長い 三日月。上の ふちに 刃の 光（U）
TAIL = [
    'kk..................',
    'kUkk................',
    '.kUAkk..............',
    '.kUAABkk............',
    '..kUABBBkk..........',
    '..kUAABBBDk.........',
    '...kUABBBBDk........',
    '...kkUABBBBDk.......',
    '....kUAABBBBDk......',
    '....kkUABBBBBDk.....',
    '.....kUAABBBBDk.....',
    '.....kkUABBBBBDk....',
    '......kUAABBBBDk....',
    '.......kUABBBBBDk...',
    '........kAABBBBDk...',
    '.........kABBBBDDk..',
    '..........kABBBDDk..',
    '..........kBBBBDDk..',
    '.........kABBBDDk...',
    '........kABBBBDk....',
    '.......kABBBDDk.....',
    '......kABBBDDk......',
    '.....kABBDDk........',
    '....kABBDDk.........',
    '...kABDDk...........',
    '..kADDk.............',
    '.kDDk...............',
    '.kkk................',
]
# 背びれ：うしろへ 反った 大鎌。前の ふちが 骨の 刃（U）、うしろの ふちは ぎざぎざ
DFIN = [
    'kk..........',
    'kUkk........',
    '.kUUkk......',
    '.kDAUUk.....',
    '..kDBAUk....',
    '..kkDBAUk...',
    '...kDBBAUk..',
    '...kkDBBAUk.',
    '....kDBBBAUk',
    '....kkDBBBAU',
    '.....kDBBBBA',
    '.....kDDBBBB',
]
BODY = [
    '..............kkkkkkkkkkkkkkkkkkk.........',
    '...........kkkAAAAAAAAAAAAAAAAAAAkkk......',
    '.........kkAAAAAAAAABBBBBBBBBBBBAAAAkk....',
    '.......kkAAAABBBBBBBDBBBBBBDBBBBBBBBAAk...',
    '.....kkAAABBBBBBBBBDDBBBBBDDBBBBBDBBBBDk..',
    '....kAAABBBBBBBBBBDDBBBBBDDBBBBBDDBBBBDDk.',
    '..kkAABBBBBBBBBBBDDBBBBBDDBBBBBDDBBBBBDDk.',
    '.kAABBBBBBBBBBBBDDBBBBBDDBBBBBBDBBBBBBBDDk',
    'kAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDk',
    'kABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDk',
    'kDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDk',
    'kDDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDk',
    'kDDDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDk.',
    '.kDDDDBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDDDDk.',
    '..kDDDDDDDBBBBBBBBBBBBBBBBBBBDDDDDDDDDDk..',
    '...kkDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDk...',
    '.....kkFEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEk...',
    '.......kFEEEEEEEEEEEEEEEEEEEEEEEEEEEFk....',
    '........kkFFEEEEEEEEEEEEEEEEEEEEEFFFk.....',
    '..........kkFFFFFEEEEEEEEEEEFFFFFFk.......',
    '............kkkkFFFFFFFFFFFFFFkkkk........',
    '................kkkkkkkkkkkkkk............',
]
# 腹びれ（小さな 刃）
VFIN = [
    '....kkkk',
    '...kUBDk',
    '..kUBDk.',
    '.kUBDk..',
    'kUDDk...',
    'kkkk....',
]
# 胸びれ：下うしろへ のびる 刃
PEC = [
    '.....kkkkkkk',
    '....kUUAABDk',
    '....kUABBDk.',
    '...kUABBDk..',
    '...kUABDDk..',
    '..kUABBDk...',
    '..kUABDk....',
    '.kUABDDk....',
    '.kUBDDk.....',
    'kUBDDk......',
    'kUDDk.......',
    'kkkk........',
]
# 頭：とがった 鼻先。骨の ひさし（まゆ）が 目に かぶさり、ほおに えらの すじ
HEAD = [
    'kkkkkkk.................',
    'AAAAAAAkkk..............',
    'BBBAAAAAAAkkk...........',
    'BBBBBBBAAAAAAkkk........',
    'BBBBBBBBBBBBAAAAkkk.....',
    'BBBBBBBBBBBBBBBAAAAkk...',
    'BkBBBBBBBBBBBBBBBBBAAk..',
    'BkBkBBBBBBBBBBBBBBBBBAk.',
    'BBkBkBBBBBBBBBBBBBBBBBAk',
    'BBkBkBBBBBBBBBBBBBBBBDDk',
    'BBBkBkBBBBBBBBBBBBDDDkk.',
    'DBBkBBkBBBBBBBBDDDkkk...',
    'DDBBBBBBBBBBDDDkkk......',
    'DDDBBBBBDDDkkk..........',
    'DDDDDDkkkk..............',
]
# 目と 骨の ひさし（つり上がって 前へ 下がる）。虹彩は 赤、ひとみは 黒い たて線
EYE = [
    '.kkkkk.....',
    'kUUUUUkkk..',
    '.kkkVVUUVkk',
    '...kRRkkVVk',
    '...krRRkkk.',
    '....kkk....',
]
def _eye(a, b): return EYE[:3] + [a, b, '....kkk....']
EYE_ALT = {
    'blink': _eye('...kkkkkVVk', '...kkkkkkk.'),
    'atk0|atk1|atk2': _eye('...kRRRkVVk', '...kRRRRkk.'),
    'hit': _eye('...kkrkkVVk', '...krkrkkk.'),
    'ko': _eye('...kXkXkVVk', '....kXkkkk.'),
}
# 上の 牙（あごの 上に かさなる）
UTEETH = [
    '..........wk',
    '.......wk.wk',
    '....wk.wk...',
    '.wk.wk......',
    '.wk.........',
]
# 下あご：骨の よろい。ぎざぎざの 刃が 上を 向き、先は 上へ 反った かぎ
JAW = [
    '...................k.',
    '..................kUk',
    '...............k.kUXk',
    '............k.kwkUVXk',
    '.........k.kwkUUVVVXk',
    '......k.kwkUUVVVVVVXk',
    '...k.kwkUUVVVVVVVVXXk',
    '..kwkUUVVVVkVVVVVVXXk',
    '.kUUUVVVVVkVVVVVVXXk.',
    'kUVVVVVVVkVVVVVVXXk..',
    'kXVVVVVVkVVVVVXXXk...',
    'kXXVVVVkVVVVXXXk.....',
    '.kkXXXXXXXXXXkk......',
    '...kkkkkkkkkk........',
]
# 大口（攻撃）：口の 中は 暗い 赤
MAW = [
    '..............kkkk',
    '..........kkkkrrrk',
    '......kkkkrrrrrrrk',
    '...kkkkrrrrrrrrrrk',
    'kkkkrrrrrrrrrrrrrk',
    'kkkrrrrrrrrrrrrrrk',
    'kkkrrrrrrrrrrrrrk.',
    '.kkrrrrrrrrrrrrk..',
    '..kkkkkkkkkkkkk...',
]
# 水の うず（待機・泳ぎで 尾の うしろに 出る）
WAKE = [['..cc..', '.c..C.', 'C....c', '.C..c.', '..CC..'], ['......', '..cC..', '.c..c.', '..Cc..', '......']]
# 攻撃の 水しぶき（開いた 口の 前へ 円すいに 飛ぶ）
SPLASH = [
    '....c..c.',
    '..cC.cC..',
    'cCc......',
    '.........',
    '.........',
    '.........',
    '.........',
    '.........',
    '.........',
    '.........',
    '.........',
    'cCc......',
    '..cC.cC..',
    '....c..c.',
]
# ---- デフォルメ：胴を 短く（まん中を 16列 ぬく）、頭と あごを 大きく 描き直す ----
BODY = [r[:9] + r[25:] for r in BODY]
import pix
def head_big():
    W, H = 32, 19; m = pix.grid(W, H)
    pix.poly(m, [(0, 4), (5, 2), (10, 0.3), (20, 2), (27, 6), (32, 10), (31.5, 13), (24, 15.5), (12, 18), (0, 19)], '#')
    g = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            if m[y][x] != '#': continue
            up = y == 0 or m[y - 1][x] != '#' or (y > 1 and m[y - 2][x] != '#')
            dn = y + 1 >= H or m[y + 1][x] != '#' or (y + 2 < H and m[y + 2][x] != '#') or (y + 3 < H and m[y + 3][x] != '#')
            g[y][x] = 'A' if up and not dn else 'D' if dn else 'B'
    # 背の しま（あく）と えらの すじ（手打ち）
    for (x, y) in ((8, 3), (9, 4), (10, 5), (14, 4), (15, 5), (16, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (6, 7), (6, 8), (7, 9), (7, 10), (8, 11)):
        if g[y][x] != '.': g[y][x] = 'D' if (x, y) in ((8, 3), (9, 4), (10, 5), (14, 4), (15, 5), (16, 6)) else 'k'
    g[9][28] = 'k'; g[10][28] = 'k'                        # 鼻の あな
    for x in range(10, 30, 3):                              # 上の 牙（下の ふちに 白い 三角）
        y = max(yy for yy in range(H) if g[yy][x] != '.')
        g[y][x] = 'w'
        if y + 1 < H: g[y + 1][x] = 'w'
    rows = pix.outline(pix.rows_of(g))
    return [r[1:] for r in rows]                            # 首の 側（左）は 胴に うめるので 輪郭を けずる
HEAD = head_big()
def jaw_big():
    W, H = 28, 14; m = pix.grid(W, H)
    pix.poly(m, [(0, 6), (10, 4), (20, 2), (26.5, 0), (28, 2), (24, 8), (16, 12), (6, 14), (0, 13)], '#')
    g = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            if m[y][x] != '#': continue
            up = y == 0 or m[y - 1][x] != '#'
            dn = y + 1 >= H or m[y + 1][x] != '#' or (y + 2 < H and m[y + 2][x] != '#')
            g[y][x] = 'U' if up else 'X' if dn else 'V'
    for x in range(2, 27, 3):                               # ぎざぎざの 刃（上の ふち）
        ys = [y for y in range(H) if g[y][x] != '.']
        if ys and ys[0] > 0: g[ys[0] - 1][x] = 'w'
    for (x, y) in ((9, 7), (8, 8), (7, 9), (16, 5), (15, 6), (14, 7)): g[y][x] = 'k'   # 骨の ひび
    return pix.outline(pix.rows_of(g))
JAW = jaw_big()
MAW = [
    '.................kkk',
    '............kkkkkrrk',
    '.......kkkkkrrrrrrrk',
    '...kkkkrrrrrrrrrrrrk',
    'kkkrrrrrrrrrrrrrrrk.',
    'kkrrrrrrrrrrrrrrrk..',
    'kkrrrrrrrrrrrrrkk...',
    '.kkkkkkkkkkkkkk.....',
]
# 目（K 魚の 目）：まぶたの ない 丸い 目。灰白の 細い 虹彩の 輪に 平たく 大きな 黒い 瞳、まわりを 骨の ふち（U・V・X）が かこむ
def _fish(inner):
    return ['BVUUUUUVB',
            'VUkkkkUUV',
            'Uk' + inner[0] + 'kVB',
            'Uk' + inner[1] + 'kVB',
            'Uk' + inner[2] + 'kVB',
            'VVk' + inner[3] + 'kVBB',
            'BXVVVVXBB']
EYE = _fish(['EEkk', 'Ewkk', 'Ekkk', 'FF'])
EYE_ALT = {
    'blink': _fish(['EEEE', 'EEEF', 'Ekkk', 'FF']),        # まぶたは なく、白い 膜が 上から かぶさる
    'atk0|atk1|atk2': _fish(['kkkk', 'kwkk', 'kkkk', 'kk']),   # 瞳が 開ききって 黒い 穴に
    'hit': _fish(['EEFF', 'EEkF', 'EFFF', 'FF']),           # 瞳が 点に ちぢむ
    'ko': _fish(['kEEk', 'EkkE', 'EkkE', 'kk']),
}
def layers():
    return [
        dict(n='wake', g='tail', x=1, y=29, rows=WAKE[0], alt={'idle1|idle2|walk1|walk2': WAKE[1]}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='tail', g='tail', x=0, y=13, rows=TAIL),
        dict(n='dfin', g='body', x=18, y=15, rows=DFIN),
        dict(n='body', g='body', x=12, y=24, rows=BODY),
        dict(n='vfin', g='body', x=17, y=43, rows=VFIN),
        dict(n='maw', g='head', x=34, y=36, rows=MAW, only='atk1|atk2'),
        dict(n='jaw', g='jaw', x=33, y=34, rows=JAW),
        dict(n='head', g='head', x=31, y=21, rows=HEAD),
        dict(n='eye', g='head', x=41, y=24, rows=EYE, alt=EYE_ALT),
        dict(n='pec', g='fin', x=29, y=41, rows=PEC),
        dict(n='splash', g='head', x=60, y=28, rows=SPLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'body': (0, -1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1)}, 'walk1': {'body': (0, -1)}, 'walk2': {'tail': (0, 1)}, 'walk3': {'body': (0, 1)},
    'atk0': {'root': (-3, 1), 'head': (0, -1), 'tail': (0, -1)}, 'atk1': {'root': (6, 0), 'head': (0, -1), 'jaw': (0, 5)}, 'atk2': {'root': (9, 1), 'head': (0, -1), 'jaw': (0, 2)},
    'hit': {'root': (-3, -1), 'head': (0, 1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'jaw': 'head', 'fin': 'body', 'tail': 'body', 'body': 'root'}
