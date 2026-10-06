# キバザメ（みず・あく × サメ）手打ち GBA風
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
# 攻撃の 水しぶき（かみつきの まわり）
SPLASH = [
    '...c.....c......',
    'c...C...cC...c..',
    '.C.......c..C...',
    '..............cC',
    '................',
    '................',
    '................',
    '................',
    '................',
    '................',
    '................',
    '................',
    '..............Cc',
    '.c.......C..c...',
    'C...cC..c....C..',
    '...C.....c......',
]
def layers():
    return [
        dict(n='wake', g='tail', x=3, y=33, rows=WAKE[0], alt={'idle1|idle2|walk1|walk2': WAKE[1]}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='tail', g='tail', x=2, y=17, rows=TAIL),
        dict(n='dfin', g='body', x=22, y=16, rows=DFIN),
        dict(n='body', g='body', x=14, y=27, rows=BODY),
        dict(n='vfin', g='body', x=22, y=46, rows=VFIN),
        dict(n='maw', g='head', x=46, y=36, rows=MAW, only='atk1|atk2'),
        dict(n='head', g='head', x=40, y=27, rows=HEAD),
        dict(n='eye', g='head', x=48, y=28, rows=EYE, alt=EYE_ALT),
        dict(n='jaw', g='jaw', x=43, y=35, rows=JAW),
        dict(n='uteeth', g='head', x=49, y=38, rows=UTEETH),
        dict(n='pec', g='fin', x=33, y=43, rows=PEC),
        dict(n='splash', g='head', x=62, y=32, rows=SPLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'body': (0, -1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1)}, 'walk1': {'body': (0, -1)}, 'walk2': {'tail': (0, 1)}, 'walk3': {'body': (0, 1)},
    'atk0': {'root': (-3, 1), 'head': (0, -1), 'tail': (0, -1)}, 'atk1': {'root': (6, 0), 'head': (0, -1), 'jaw': (0, 5)}, 'atk2': {'root': (9, 1), 'head': (0, -1), 'jaw': (0, 2)},
    'hit': {'root': (-3, -1), 'head': (0, 1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'jaw': 'head', 'fin': 'body', 'tail': 'body', 'body': 'root'}
