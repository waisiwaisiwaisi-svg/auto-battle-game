# ヒムカデ（むし・ほのお × ムカデ）手打ち GBA風
META = dict(id='himukade', name='ヒムカデ', types=['bug', 'fire'], base='ムカデ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1014',
    'A': '#b8484a', 'B': '#74242c', 'D': '#3e121c',
    'E': '#d09450', 'e': '#7e4a28',
    'Y': '#fff27a', 'O': '#ffa424', 'F': '#e0441a',
    'w': '#fff6e4',
}
LIGHT = set('AEYw')
KEEP_BLACK = set('wYO')

# 体：黒赤の 甲の 節。節の すき間から 溶けた 火が のぞく
BODY = [
    '......................................kk.....',
    '....................................kkAAkk...',
    '...................................kAAABBBk..',
    '.................................kkAAABBBBDk.',
    '................................kAOAABBBBDDk.',
    '..............................kkAAAOABBBDDDEk',
    '.............................kAAAABOFADDDEEEk',
    '............................kAOAABBBFDDDEEEk.',
    '...kk....................kkkAAAOABBBDFDEEEEk.',
    '..kOOkkkkkkkkkkkkkkkkkkkkAAOAABOFADDDEeeEEk..',
    '.kOOOAAAAOAAAAOAAAAOAAAAAAAOABBBFDDDEEEeek...',
    'kFFFFABBBOAAAAOAAAAOAAAAAABBOBBBDFDEEEEek....',
    'keeFFDBBBOABBBOABBBOBBBBABBBFABDDDeeEEkk.....',
    '.keeeDDDBFBBBBFABBBOBBBBABBBFFDDDEEeek.......',
    '..keeEEDFDDDDDFBBBBFBBBBABDDDFDEEEEek........',
    '...kkEEEeDDDDFDDDDDFDDDDFDDDDeeeEEEk.........',
    '.....kEeeeEEEeeDDDDeDDDDeDEEEeeeeEk..........',
    '......kkeeEEEeeEEEEeEEEEeeEEEEeekk...........',
    '........kkkEEeEEEEEeEEEEeeeEEkkk.............',
    '...........kkkkEEEEeEEEEeekkk................',
    '...............kkkkkkkkkkk...................',
]
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]
# 足：一本ずつ 先が 熾火（おきび）
LEG = [
    'kk...',
    'kDkk.',
    '.kDDk',
    '..kFk',
    '..kOk',
    '.kOk.',
    '.kYk.',
    '..k..',
]
LEG2 = [
    '...kk',
    '.kkDk',
    'kDDk.',
    'kFk..',
    'kOk..',
    '.kOk.',
    '.kYk.',
    '..k..',
]
LEGF = [  # 浮いた 前足（ぶら下がる）
    'kDk..',
    '.kFk.',
    '..kOk',
    '..kYk',
    '...k.',
]
# 頭：光る 目の むれ、甲の かぶと
HEAD = [
    '...kkkkkkkk.....',
    '.kkAAAAAAAAkkk..',
    'kAABBBBBBBBBAAk.',
    'kABkkkkBBBBBBBAk',
    'kBBBkYYkkBBBBBBk',
    'kBBkYYkBBBBBBBDk',
    'kDBBkkBBBBBBBDDk',
    '.kDDBBBBBBBDDkk.',
    '..kkkkkkkkkkk...',
]
def _eye(a, b):
    h = list(HEAD); h[4] = h[4][:4] + a + h[4][4 + len(a):]; h[5] = h[5][:3] + b + h[5][3 + len(b):]; return h
HEAD_ATK = _eye('kYYYk', 'kYYYk')
HEAD_BLINK = _eye('kBBkk', 'kkkBB')
HEAD_HIT = _eye('kYkYk', 'kkYkB')
HEAD_KO = _eye('kBkBk', 'BkBkB')
# 毒あご（顎肢）：前へ 曲がった 二本の 牙
FANG = [
    '.kkkkkkk......',
    'kDBBBBBAkkk...',
    '.kkkkDBBBBAk..',
    '.....kkkDBAk..',
    '........kDAk..',
    '.......kOYk...',
    '......kYk.....',
    '.......k......',
]
FANG_OPEN = [
    '.kkkkkkkk......',
    'kDBBBBBBAkkk...',
    '.kkkkkDBBBBAk..',
    '......kkkDBBAk.',
    '.........kDBAk.',
    '..........kDAk.',
    '.........kOYk..',
    '.........kYk...',
    '..........k....',
]
FANG_FAR = [r.replace('B', 'D').replace('A', 'B').replace('Y', 'O').replace('O', 'F') for r in FANG]
# 触角：うしろへ のびて 先が 炎
ANT = [
    '.........kk.',
    '.......kkYOk',
    '......kDkkk.',
    '.....kDk....',
    '....kDk.....',
    '...kDk......',
    '..kDk.......',
    '.kDk........',
    'kDk.........',
]
ANT_FAR = [
    '....kk..',
    '...kYOk.',
    '...kFk..',
    '...kDk..',
    '..kDk...',
    '..kDk...',
    '.kDk....',
    '.kDk....',
    'kDk.....',
    'kk......',
]
ANT2 = [
    '........kk..',
    '......kkYOk.',
    '.....kDkkk..',
    '.....kDk....',
    '....kDk.....',
    '...kDk......',
    '..kDk.......',
    '.kDk........',
    'kDk.........',
]
# 尾の 二本の 尾脚（先が 炎）
TAIL = [
    'kk.....',
    'kYkk...',
    '.kOFkk.',
    '..kkFDk',
    '....kDk',
]
# 攻撃：牙から ふき出す 炎
FIRE = [
    '.......kk.....',
    '....kkkOOkk...',
    '..kkFOOYYOOk..',
    'kkFOYYYwwYYOk.',
    'kOYYwwwwwwYYOk',
    'kkFOYYYwwYYOk.',
    '..kkFOOYYOOk..',
    '....kkkOOkk...',
    '.......kk.....',
]
FIRE2 = [
    '....kkk...',
    '..kkOOOk..',
    'kkFOYYYOk.',
    'kOYYwwYYOk',
    'kkFOYYYOk.',
    '..kkOOOk..',
    '....kkk...',
]
EMBER = [['.O...Y', '......', '..Y...'], ['..Y...', '.O..O.', '......']]

def layers():
    L = [
        dict(n='tail', g='body', x=0, y=37, rows=TAIL),
        dict(n='antf', g='head', x=42, y=21, rows=ANT_FAR),
    ]
    # 奥の 足（体の うしろ）
    for i, x in enumerate((8, 13, 18, 23, 28)):
        L.append(dict(n=f'bl{i}', g='legB' if i % 2 else 'legA', x=x, y=50, rows=LEG2 if i % 2 else LEG))
    L += [
        dict(n='fangfar', g='head', x=44, y=36, rows=FANG_FAR, alt={'atk0': FANG_OPEN}),
        dict(n='body', g='body', x=0, y=32, rows=cut(BODY, 0, 28)),
        dict(n='front', g='front', x=24, y=32, rows=cut(BODY, 24, 51)),
    ]
    # 手前の 足
    for i, x in enumerate((4, 9, 14, 19, 24)):
        L.append(dict(n=f'fl{i}', g='legA' if i % 2 else 'legB', x=x, y=52, rows=LEG if i % 2 else LEG2))
    L += [
        dict(n='ff1', g='front', x=31, y=48, rows=LEGF),
        dict(n='head', g='head', x=36, y=31, rows=HEAD, alt={'atk0|atk1|atk2': HEAD_ATK, 'blink': HEAD_BLINK, 'hit': HEAD_HIT, 'ko': HEAD_KO}),
        dict(n='ant', g='head', x=44, y=23, rows=ANT, alt={'idle1|idle3|walk1|walk3': ANT2}),
        dict(n='fang', g='head', x=41, y=37, rows=FANG, alt={'atk0': FANG_OPEN}),
        dict(n='ember', g='body', x=12, y=36, rows=EMBER[0], alt={'idle2|idle3|walk2|walk3': EMBER[1]}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='fire', g='head', x=54, y=34, rows=FIRE, only='atk1'),
        dict(n='fire2', g='head', x=55, y=36, rows=FIRE2, only='atk2'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'front': (0, -1)}, 'idle2': {'front': (0, -1), 'body': (0, 0)}, 'idle3': {'front': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'front': (0, -1), 'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'front': (0, -1), 'body': (0, -1)},
    'atk0': {'front': (-1, -2), 'head': (-1, -1), 'body': (0, -1)}, 'atk1': {'root': (4, 0), 'front': (2, 1), 'head': (1, 0)}, 'atk2': {'root': (5, 0), 'front': (1, 1), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'front': (-1, -2), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'front', 'front': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
