# ワダツミ（みず・ドラゴン × 海竜）手打ち GBA風
META = dict(id='watatsumi', name='ワダツミ', types=['water', 'dragon'], base='海竜', size='L')
PAL = {
    'k': '#101018', 'l': '#123038',
    'A': '#62c4a8', 'B': '#2e8a7e', 'D': '#1a5054',
    'E': '#ece2b0', 'F': '#b09c68',
    'c': '#c4f0ff', 'C': '#4aa6e8', 'N': '#2a5cb0',
    'w': '#ffffff',
    'Y': '#ffd23c', 'O': '#c4741a',
    'r': '#a01c30',
}
LIGHT = set('AEcwY')
KEEP_BLACK = set('wYr')

# とぐろ：奥の 輪（尾へ つづく）
REAR = [
    '.....................kk....',
    '....................kAAk...',
    '...................kAAAAk..',
    '...................kABBAk..',
    '...................kABBBAk.',
    '...................kABBBAk.',
    '...................kABBBBk.',
    '...................kABBBBDk',
    '...................kBBBBBDk',
    '..................kABBBBBDk',
    '..................kABBBBBDk',
    '...............kkkABBBBBBDk',
    '............kkkAAAABBBBBDk.',
    '.........kkkAAAAAABBBBBBDk.',
    '......kkkAAAAAABBBBBBBBBDk.',
    '....kkAAAAAABBBBBBBBBBBDDk.',
    '...kAAAAABBBBBBBBBBBBDDDDk.',
    '...kAABBBBBBBBBBBBBBDDDDk..',
    '..kABBBBBBBBBBBBBBDDDDDk...',
    '..kABBBBBBBBBBBBDDDDDkk....',
    '.kABBBBBBBBBBDDDDDDDk......',
    '.kABBBBBBBBBDDDDDDkk.......',
    '.kABBBBBBBBDDDDDkk.........',
    'kABBBBBBBBBDDkkk...........',
    'kDBBBBBBBBDDk..............',
    'kDBBBBBBBBDk...............',
    'kDDDBBBBDDDk...............',
    '.kDDDDDDDDk................',
    '.kDDDDDDDDk................',
    '..kkDDDDkk.................',
    '....kkkk...................',
]
# とぐろ：手前の 輪（地面に ふせる。下がわは 腹の 板）
FRONT = [
    '..........................................kkkk....',
    '........................................kkAAADkk..',
    '.......................................kAAAAAAADk.',
    '.......................................kAABBBBADk.',
    '......................................kABBBBBDDDDk',
    '......................................kABBBBDDDDDk',
    '......................................kABBBBDDDDDk',
    '....kkkk.............................kABBBBDDFEEFk',
    '..kkAAAAkk..........................kkABBBDDEFEFk.',
    '.kAAAAAAADk........................kAABBBBDDEFEFk.',
    '.kAABBBBAADk.................kkkkkkAAABBBDDEEFEFk.',
    'kABBBBBBBBADkkkkkkkkkkkkkkkkkAAAAAAABBBDDDEEEFFk..',
    'kDBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAABBDDDDDEEEFFk..',
    'kDBBBBBBBBBBAAAAAAAAAAAAAAAAABBBBBBDDDDDDFEEEFFk..',
    'kDDDBBBBBBBBBBBBBBBBBBBBBBBBBDDDDDDDDDDEEFEEFFk...',
    '.kDDDBBBBDDDDDDDDDDDDDDDDDDDDDDDDDDDDFEEEFFFFFk...',
    '.kDDDDBBDDDDDDDDDDDDDDDDDDDDDDDDDDDEEFEEEFFFkk....',
    '..kkDDDBDDDDDDDDDDDDDDDDDDDDDFEEEFEEEFEFFFkk......',
    '....kDDDDFEEEFEEEFEEEFEEEFEEEFEEEFEEEFFFFk........',
    '.....kDDFFEEEFEEEFEEEFEEEFEEEFFFFFFFFFFkk.........',
    '......kDFFFFFFFFFFFFFFFFFFFFFFFFFFFFFkk...........',
    '.......kkFFFFFFFFFFFFFFFFFFFFkkkkkkkk.............',
    '.........kkkkkkkkkkkkkkkkkkkk.....................',
]
# 首：S字に 立ち上がる。前がわは 腹の 板
NECK = [
    '.........kkkkkk..',
    '........kAAAAADk.',
    '.......kAAAAADDDk',
    '......kAABBBDDDDk',
    '.....kAABBBDDDDDk',
    '....kAABBBDDDEFDk',
    '...kAABBBDDDEEEFk',
    '...kABBBDDDFFFFFk',
    '..kABBBBDDEEEFFk.',
    '..kABBBBDEEEFFk..',
    '.kABBBBDFFFFFk...',
    '.kABBBBDEEEFk....',
    'kABBBBDDEEFk.....',
    'kABBBBDFFFFk.....',
    'kABBBBDEEEk......',
    'kABBBBFEEEk......',
    'kABBBBFFFFk......',
    'kABBBBAEEEk......',
    'kBBBBBAEEEk......',
    'kBBBBBBFFFFk.....',
    'kBBBBBBEEEEk.....',
    'kDBBBBBEEEEk.....',
    'kDBBBBBFFFFFk....',
    'kDBBBBBFEEEEk....',
    '.kDBBBBAFEEEEk...',
    '.kDBBBBAFFFFFk...',
    '.kDDBBBBAFEEEk...',
    '..kDBBBBAFEEEFk..',
    '..kDBBBBBDFFFFk..',
    '...kBBBBBDEEEFk..',
    '...kBBBBBDEEEFk..',
    '...kBBBBBDFFFFk..',
    '...kBBBBBDEEEFk..',
    '..kABBBBDEEEFk...',
    '..kABBBBDFFFFk...',
    '..kABBBBDEEEFk...',
    '..kDBBBBDEEEFk...',
    '..kDBBBBDFFFFk...',
    '..kDDDBBDFFFFk...',
    '...kDDDDDDFFk....',
    '...kDDDDDDDDk....',
    '....kkDDDDkk.....',
    '......kkkk.......',
]
# 波の 背びれ：うしろへ 流れる 波頭。前の ふちが 白い しぶき
CREST = [
    '..kk.kk.....',
    '.kwk.kwk....',
    'kwwkkwwk....',
    'kcwwwwck....',
    '.kcCccwkk...',
    '.kcCCCCcwk..',
    '..kcCCCCCwk.',
    '..kcCCCCCcwk',
    '...kcCCCCCNk',
    '...kcCCCCNNk',
    '....kcCCNNNk',
    '....kcCNNNk.',
    '.....kNNNk..',
    '.....kkkk...',
]
CREST2 = [
    'w.k..k......',
    '.kwk.kwk....',
    'kwwkkwwk....',
    'kcwwwwck....',
    '.kcCccwkk...',
    '.kcCCCCcwk..',
    '..kcCCCCCwk.',
    '..kcCCCCCcwk',
    '...kcCCCCCNk',
    '...kcCCCCNNk',
    '....kcCCNNNk',
    '....kcCNNNk.',
    '.....kNNNk..',
    '.....kkkk...',
]
# 尾の 先の 大きな 波びれ（扇）
TAILFIN = [
    'kk.......kk....',
    'kwkk....kwk....',
    '.kwwk..kwck....',
    '.kcwwkkwcCk....',
    '..kcCwwcCCk..kk',
    '..kcCCcCCNkkkwk',
    '...kcCCCCNkwwck',
    '...kcCCCCNwcCk.',
    '....kcCCCCCNk..',
    '....kcCCCNNk...',
    '.....kCCNNk....',
    '......kkkk.....',
]
# ほおの ひれ（あごの つけ根）
FRILL = [
    'kk.......',
    'kwkkk....',
    '.kccCkk..',
    'kwcCCNNk.',
    '.kkcCNNNk',
    'kwccCNNk.',
    '.kkkkkk..',
]
# 角：うしろへ 反った 金の 角（手前・奥）
HORN = [
    'kkkk...........',
    'kYYYkkk........',
    '.kkYYYYkkk.....',
    '...kkOYYYYkkk..',
    '.....kkOOYYYYk.',
    '.......kkkOOOOk',
    '..........kkkk.',
]
HORN2 = [
    'kkk...........',
    'kOOkkk........',
    '.kkOOOkkk.....',
    '...kkOOOOkkk..',
    '.....kkkOOOOk.',
    '........kkkk..',
]
# 頭：ぶあつい まゆの 下に 金の つり目。長い 鼻先、上あごの 牙
HEAD = [
    '.........kkkkk..............',
    '.......kkAAAAAkk............',
    '.....kkAAAAAAAAAkkk.........',
    '....kAAAABBBBBBAAAAkkk......',
    '...kAABBBBBBBBBBBBBAAAkkk...',
    '..kAABkkkkkkBBBBBBBBBBAAAk..',
    '..kABBBBBBBkkkBBBBBBBBBBBAk.',
    '.kABBkYYYYkkBBBBBBBBBBBBBBAk',
    '.kABBkOOOkBBBBBBBBBBBBBBkBDk',
    'kABBBBkkkBBBBBBBBBBBBBBBBDDk',
    'kBBBBBBBBBBBBBBBBBBBBBBDDDk.',
    'kDBBBBBBBBBBBBBBBBBDDDDDkk..',
    'kDBBBBkkkkkkkkkkkkkkkkkkk...',
    'kDBBBkwkEEwkEEEEwkEEEwkEk...',
    'kDDBBkkEEEkEEEEEkEEEEkEEEk..',
    '.kDDkEEEEEEEEEEEEEEEEEEFk...',
    '..kDDFFFFFFFFFFFFFFFFkk.....',
    '...kkkkkkkkkkkkkkkkkk.......',
]
# 口を 開けた 頭（ブレス）：下あごを 落とし、口の 中は 暗い 赤
HEAD_OPEN = HEAD[:12] + [
    'kDBBBBkkkkkkkkkkkkkkkkkkk...',
    'kDBBBkrrrrwkrrrrrwkrrwkk....',
    'kDDBkrrrrrrrrrrrrrrrrrk.....',
    '.kDDkrrrrrrrrrrrrrrrrrrk....',
    '.kDDkkkkkkwkkkkwkkkkwkkEk...',
    '..kDDEEEEEEEEEEEEEEEEEEFk...',
    '...kkFFFFFFFFFFFFFFFFFkk....',
    '.....kkkkkkkkkkkkkkkkkk.....',
]
def _eye(h, a, b):
    h = list(h); h[7] = h[7][:6] + a + h[7][6 + len(a):]; h[8] = h[8][:6] + b + h[8][6 + len(b):]; return h
HEAD_ATK0 = _eye(HEAD, 'YYYYY', 'OOOO')
HEAD_OPEN = _eye(HEAD_OPEN, 'YYYYY', 'OOOO')
HEAD_BLINK = _eye(HEAD, 'kkkkk', 'BBBk')
HEAD_HIT = _eye(HEAD, 'kYkYk', 'BkBk')
HEAD_KO = _eye(HEAD, 'BkBkB', 'BBkBk')
# 水の ブレス（口から 右へ）
BEAM = [
    '...........c...c.',
    'cccccccccccCc.c..',
    'CCCCCCCCCCCCCc..c',
    'wwwwwwwwwwwwwwcC.',
    'wwwwwwwwwwwwwwwcC',
    'CCCCCCCCCCCCCcC..',
    'cccccccccccCc.c..',
    '...........c...c.',
]
BEAM2 = [
    '..........c...c.',
    'ccccccccccCc..c.',
    'wwwwwwwwwwwwcC..',
    'cccccccccccCc..c',
    '..........c.....',
]
def layers():
    return [
        dict(n='horn2', g='head', x=31, y=3, rows=HORN2),
        dict(n='tailfin', g='tail', x=11, y=16, rows=TAILFIN),
        dict(n='rear', g='tail', x=0, y=26, rows=REAR),
        dict(n='cr3', g='front', x=3, y=28, rows=CREST, alt={'idle1|idle3|walk1|walk3': CREST2}),
        dict(n='front', g='front', x=0, y=38, rows=FRONT),
        dict(n='cr2', g='neck2', x=26, y=22, rows=CREST, alt={'idle2|walk0|walk2': CREST2}, not_='ko'),
        dict(n='cr1', g='neck1', x=28, y=13, rows=CREST, alt={'idle1|idle3|walk1|walk3': CREST2}, not_='ko'),
        dict(n='neck', g='neck1', x=36, y=9, rows=NECK[:22], not_='ko'),
        dict(n='neckb', g='neck2', x=36, y=31, rows=NECK[22:], not_='ko'),
        dict(n='head', g='head', x=36, y=2, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN, 'atk0': HEAD_ATK0, 'blink': HEAD_BLINK, 'hit': HEAD_HIT, 'ko': HEAD_KO}),
        dict(n='horn', g='head', x=33, y=0, rows=HORN),
        dict(n='beam', g='head', x=61, y=14, rows=BEAM, only='atk1'),
        dict(n='beam2', g='head', x=61, y=15, rows=BEAM2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'neck1': (0, 1)}, 'idle2': {'neck1': (0, 1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1)},
    'blink': {},
    'walk0': {'neck1': (-1, 0), 'tail': (0, -1)}, 'walk1': {'neck1': (0, 0), 'neck2': (1, 0), 'front': (0, 0)},
    'walk2': {'neck1': (1, 0), 'tail': (0, 1)}, 'walk3': {'neck2': (-1, 0)},
    'atk0': {'neck1': (-2, 1), 'neck2': (-1, 0), 'head': (-1, 1)}, 'atk1': {'neck1': (2, 0), 'neck2': (1, 0), 'head': (1, 0)}, 'atk2': {'neck1': (2, 0), 'neck2': (1, 0)},
    'hit': {'neck1': (-2, 2), 'neck2': (-1, 0), 'head': (-1, 1)}, 'ko': {'head': (1, 38), 'tail': (0, 2)},
}
PARENT = {'head': 'neck1', 'neck1': 'neck2', 'neck2': 'root', 'tail': 'root', 'front': 'root'}
