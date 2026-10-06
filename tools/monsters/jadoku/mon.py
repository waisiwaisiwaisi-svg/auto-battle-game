# ジャドク（どく・あく × コブラ）手打ち GBA風
META = dict(id='jadoku', name='ジャドク', types=['poison', 'dark'], base='コブラ', size='M')
PAL = {
    'k': '#101018', 'l': '#24162e',
    'A': '#84639e', 'B': '#4e366a', 'D': '#2c1d40',
    'E': '#d6e67c', 'F': '#86a034',
    'G': '#b4ff6c', 'g': '#36b838',
    'Y': '#ffe14a', 'w': '#ffffff', 'r': '#9a1838',
    'U': '#e8e0d0', 'V': '#9a8e80',
}
LIGHT = set('AEGYwU')
KEEP_BLACK = set('wGgYr')

# とぐろ：奥（尾の 先へ）
REAR = [
    '...............kkkkkkkkkkkkkkkkk........',
    '...........kkkkAAAAAAAAAAAAAAAAAkkkk....',
    '........kkkAAAAAAAAAAAAAAAAAAAAAAAAAkk..',
    '.....kkkAAAAAABBBBBBBBBBBBBBBBBAAAAAAAk.',
    '....kAAAAABBBBBBBBBBBBBBBBBBBBBBBBBAAAAk',
    '...kAABBBBBBBBBBBDDDDDDDDDDBBBBBBBBBBBBk',
    '..kAABBBBBBDDDDDDDDDDDDDDDDDDDDBBBBBBBBk',
    '.kAABBBDDDDDDDEEEEEEEEEEEEEEDDDDDDDBBBBk',
    'kAABBDDEEEEEEEEFFFFFFFFFEEEEEEEEDDDDDDDk',
    'kBBDDEEFFFFFkkkkkkkkkkkkkkFFFFEEEEEEDDDk',
    'kDDEFFkkkkkk..............kkkkFFFFEEEEk.',
    '.kkkkk........................kkkkkkkk..',
]
# とぐろ：手前（腹は 毒々しい 黄緑）
FRONT = [
    '............kkkkk................................',
    '........kkkkAAAAAk....................kkkkkk.....',
    '.....kkkAAAAAAAABBk..................kDBBBAAk....',
    '....kAAAAAAABBBBBBBk................kEDDBBBAAk...',
    '...kAAAABBBBBBBBBBDk................kEDDBBBAAk...',
    '...kABBBBBBBBBBDDDDk................kEDDBBBAAAk..',
    '..kAAABBBBBDDDDDDEEk................kEEDDBBBAAk..',
    '..kAABBBDDDDDDEEEEk.................kFEDDBBBAAAk.',
    '.kAAABBBDDDEEEEFFk..................kFEDDBBBBAAk.',
    '.kAABBBBDDEEFFkkkkkkkkkkkkkkkkkkkkkkAAAEDDBBBADDk',
    'kAAABBBDDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBDBBBDDDk',
    'kAABBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBDDDDEk',
    'kAABBBBBBBBBBBBBBBBAAAAAAAAAAAABBBBBBBBBBBDDDEEEk',
    'kABBBDDDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDDEEFk.',
    '.kBBBDDDDDDBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDEEEFFk.',
    '.kBBBEEEDDDDDBBBBBBBBBBBBBBBBBBBBBBBBDDDDEEFFkk..',
    '..kkFFEEEEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDEEEFFk....',
    '....kkFFFEEEDDDDDDDDDDDDDDDDDDDDDDDDDEEEFFkk.....',
    '......kkFFFEEEEEEEEEEEEEEEEEEEEEEEEEEEEFFk.......',
    '........kkkFFFFFFFFFFFFFFFFFFFFFFFFFFFFkk........',
    '...........kkkkkkkkkkkkkkkkkkkkkkkkkkkk..........',
]
# 首：まっすぐ 立てる。前がわは 腹の 板
NECK = [
    '.........kkkk...',
    '........kABBBk..',
    '.......kAABBBDk.',
    '......kAABBBDDEk',
    '......kAABBBDEEk',
    '.....kAABBBDDEFk',
    '.....kAABBBDEEFk',
    '....kAABBBDDEFk.',
    '....kAABBBDEEFk.',
    '...kAABBBDDEFk..',
    '...kAABBBDEEFk..',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBDDEFk...',
    '...kAABBBDEEFk..',
    '...kAABBBDDEFk..',
    '...kAABBBDDEEFk.',
    '....kAABBBDDEFk.',
    '....kAABBBDDEFk.',
    '....kAABBBBDEEFk',
    '.....kAABBBDDEFk',
    '.....kAABBBDDEEk',
    '.....kAABBBDDEEk',
    '.....kAABBBDDEEk',
    '.....kAABBBDDEFk',
    '.....kAABBBDDEFk',
    '.....kAABBBDDEFk',
    '....kAAABBBDDEFk',
    '....kAABBBBDDEFk',
    '...kAAABBBBDDEFk',
    '...kAABBBBDDEEFk',
    '..kAAABBBBDDEEFk',
    '.kAAABBBBDDEEFk.',
    '.kAABBBBDDDEFFk.',
    'kAAABBBBDDEEFk..',
    'kAABBBBDDEEFk...',
    'kABBBBDDDEFFk...',
    'kABBBBDDEEFk....',
    '.kBBBDDEEFk.....',
    '.kBBDDDEFFk.....',
    '..kkDDEEkk......',
    '....kkkk........',
]
# フード：大きく 広げた 首の 膜（うしろ 3/4 から 見る）
HOOD = [
    '............kkkkkkk.............',
    '..........kkAAAABBBkk...........',
    '.........kAAAAAAAABBBk..........',
    '........kAABBBBBBBBBBBk.........',
    '.......kAABBBBBBDBBBDDDk........',
    '......kAABBBBBBBDBBBBDDDk.......',
    '.....kAABBBBBBBBDBBBBBDDDk......',
    '....kAABBBBBBBBBDBBBBBBDDDk.....',
    '...kAABBBBBBBBBBDBBBBBBBDDDk....',
    '...kAABBBBBBBBBBDBBBBBBBDDDk....',
    '..kAABBBBBBBBBBBDBBBBBBBBDDDk...',
    '..kAABBBBBBBBBBBDBBBBBBBBDDDk...',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '.kAABBBBBBBBBBBBDBBBBBBBBBDDDk..',
    '..kAABBBBBBBBBBBDBBBBBBBBDDDk...',
    '..kAABBBBBBBBBBBDBBBBBBBBDDDk...',
    '...kAABBBBBBBBBBDBBBBBBBDDDk....',
    '...kAABBBBBBBBBBDBBBBBBBDDDk....',
    '....kAABBBBBBBBBDBBBBBBDDDk.....',
    '.....kAABBBBBBBBDBBBBBDDDk......',
    '......kAABBBBBBBDBBBBDDDk.......',
    '......kAABBBBBBBDBBBBDDDk.......',
    '.......kAABBBBBBDBBBDDDk........',
    '.......kAABBBBBBDBBBDDDk........',
    '........kAABBBBBDBBDDDk.........',
    '........kAABBBBBDBBDDDk.........',
    '.........kkkkkkkkkkkkkk.........',
]
# フードの 目玉もよう（光る 毒の 目、たての ひとみ）
OCELLUS = [
    'kkk......',
    'kGGkkk...',
    'kgGGGGkk.',
    '.kggGkGGk',
    '..kkgkGgk',
    '....kkggk',
    '......kk.',
]
OCELLUS_S = [
    '......kkk',
    '...kkkGGk',
    '.kkGGGGgk',
    'kGGkGggk.',
    'kgGkgkk..',
    'kggkk....',
    '.kk......',
]
# フードの ふちの 骨の とげ（うしろへ）
SPK = [
    'kk....',
    'kUkkk.',
    '.kUUVk',
    '..kkkk',
]
SPK2 = [
    '..kkkk',
    '.kUUVk',
    'kUkkk.',
    'kk....',
]
# 頭：細い つり目（黄色）、長い 毒の 牙
HEAD = [
    '....kkkkkkk.........',
    '..kkAAAAAAAkkk......',
    '.kAAABBBBBBAAAkkk...',
    'kAABBBBBBBBBBBAAAkk.',
    'kABBkkkkkBBBBBBBBAAk',
    'kABBBBYYYkkkBBBBBBBk',
    'kBBBBBkYkBBBBBBBBBDk',
    'kBBBBBBkBBBBBBBBBDDk',
    'kDBBBkkkkkkkkkkkkkk.',
    'kDDBkEEwkEEEEEEEwk..',
    '.kDDkEEwkEEEEEEEwk..',
    '..kDDFFkFFFFFFFFkk..',
    '...kkkkkkkkkkkkk....',
]
HEAD_OPEN = [
    '....kkkkkkk.........',
    '..kkAAAAAAAkkk......',
    '.kAAABBBBBBAAAkkk...',
    'kAABBBBBBBBBBBAAAkk.',
    'kABBkkkkkBBBBBBBBAAk',
    'kABBBBYYYYkkBBBBBBBk',
    'kBBBBBkYYkBBBBBBBBDk',
    'kBBBBBBkkBBBBBBBBDDk',
    'kDBBBkkkkkkkkkkkkkk.',
    'kDDBkrrwkrrrrrrrwk..',
    'kDDkrrrwkrrrrrrrwk..',
    '.kDkrrrrrrrrrrrrrrk.',
    '.kDkrrrrrrrrrrrrrrk.',
    '.kDDkkkwkkkkkkwkkkk.',
    '..kDEEEEEEEEEEEEk...',
    '...kkFFFFFFFFFkk....',
    '.....kkkkkkkkk......',
]
def _eye(h, a, b):
    h = list(h); h[5] = h[5][:5] + a + h[5][5 + len(a):]; h[6] = h[6][:6] + b + h[6][6 + len(b):]; return h
HEAD_BLINK = _eye(HEAD, 'BkkkkB', 'BBB')
HEAD_HIT = _eye(HEAD, 'BkYkYk', 'BkB')
HEAD_KO = _eye(HEAD, 'BkBkBk', 'BBk')
HEAD_ATK0 = _eye(HEAD, 'BYYYYk', 'kYY')
# 牙から たれる 毒
DRIP = ['G', 'g']
DRIP2 = ['.', 'G', 'g']
# 毒の 吐きかけ
SPIT = [
    '.........G..G......',
    '...GG..GGg.....G...',
    'GGGgGGGGgGG.GG..Gg.',
    'gGGGggGGGgGGgGG.G..',
    '..gg..GgG..g..g....',
    '.......g......g....',
]
SPIT2 = [
    '.......G...G..',
    '..G.GgG..G..g.',
    'GgGG.g..g.....',
    '.g.....g......',
]
# 尾の 先の 骨の とげ
TAILSPK = ['kk...', 'kUkk.', '.kUVk', '..kk.']

def layers():
    return [
        dict(n='tailspk', g='coil', x=3, y=43, rows=TAILSPK),
        dict(n='rear', g='coil', x=6, y=37, rows=REAR),
        dict(n='neck', g='neck', x=33, y=7, rows=NECK, not_='ko'),
        dict(n='spk1', g='hood', x=26, y=9, rows=SPK, not_='ko'),
        dict(n='spk2', g='hood', x=23, y=14, rows=SPK, not_='ko'),
        dict(n='spk3', g='hood', x=24, y=22, rows=SPK2, not_='ko'),
        dict(n='hood', g='hood', x=26, y=3, rows=HOOD, not_='ko'),
        dict(n='oc1', g='hood', x=29, y=17, rows=OCELLUS, not_='ko'),
        dict(n='oc2', g='hood', x=41, y=17, rows=OCELLUS_S, not_='ko'),
        dict(n='front', g='coil', x=4, y=40, rows=FRONT),
        dict(n='head', g='head', x=38, y=4, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN, 'atk0': HEAD_ATK0, 'blink': HEAD_BLINK, 'hit': HEAD_HIT, 'ko': HEAD_KO}),
        dict(n='drip', g='head', x=54, y=15, rows=DRIP, alt={'idle2|idle3|walk1|walk3': DRIP2}, not_='atk1|atk2|ko'),
        dict(n='spit', g='head', x=57, y=13, rows=SPIT, only='atk1'),
        dict(n='spit2', g='head', x=61, y=14, rows=SPIT2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'neck': (0, 1)}, 'idle2': {'neck': (0, 1), 'hood': (0, 0)}, 'idle3': {'neck': (0, 0), 'hood': (0, -1)},
    'blink': {},
    'walk0': {'neck': (-1, 0), 'coil': (0, 0)}, 'walk1': {'neck': (0, 1)}, 'walk2': {'neck': (1, 0)}, 'walk3': {'neck': (0, 1)},
    'atk0': {'neck': (-2, 1), 'hood': (0, -1), 'head': (-1, 0)}, 'atk1': {'neck': (2, -1), 'head': (2, 0)}, 'atk2': {'neck': (2, 0), 'head': (1, 0)},
    'hit': {'neck': (-2, 1), 'head': (-2, 1)}, 'ko': {'head': (2, 41), 'coil': (0, 0)},
}
PARENT = {'head': 'neck', 'hood': 'neck', 'neck': 'root', 'coil': 'root'}
