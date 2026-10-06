# ライデンウナギ（でんき・みず × ウナギ）手打ち GBA風
META = dict(id='raidenunagi', name='ライデンウナギ', types=['elec', 'water'], base='ウナギ', size='M')
PAL = {
    'k': '#101018', 'l': '#181c36',
    'A': '#6474a6', 'B': '#38406c', 'D': '#1f2446',
    'E': '#a2bece', 'F': '#5e7a94',
    'Y': '#fffbc4', 'y': '#ffd83a', 'O': '#d0880e',
    'w': '#ffffff', 'c': '#9ef4ff',
    'r': '#a01c30',
}
LIGHT = set('AEYwc')
KEEP_BLACK = set('wYyr')

# 体：S字に うねる。わき腹に 発電板（黄色い 板）が 一列に 並ぶ
BODY = [
    '....................................kkkkkk...',
    '........kkkkkkkk...................kAAByOOk..',
    '.......kAAAAAAAAkk................kAAAyyODDk.',
    '......kABBBAAAABAAk..............kAAAByOODDEk',
    '.....kAABBBByyyBAAAk.............kAAAyyODDEEk',
    '....kAAByODDOOOBBAAAk...........kAAAByOODDEEk',
    '...kAAByDDDDDDDBByAAAk..........kAAAyyODDEEFk',
    '..kAABBDDEEEEEDDOyBAAAk........kAAAByOODDEEFk',
    '..kABBDEEFkFFEEDDOyBAAAk.......kAAABBODDEEFFk',
    '.kABBDEFkk.kkFEEDDBBBAAAk.....kAAABBBBDDEEFk.',
    '.kABDEFk.....kFEDDBByBAAAk...kAAAByyODDEEFFk.',
    '.kABDEk......kFEEDDOyyBAAAkkkAAABByOODDEEFk..',
    'kABDEk........kFEEDDOyBBAAAAAAABBBBODDEEFFk..',
    'kABDFk.........kFEEDDBBBBAAAAAByyBBDDDEEFk...',
    'kBDEk..........kFEEEDDByyBBBBByyOODDDEEFFk...',
    'kBEk............kFEEEDDOyyByyyBOODDDEEFFk....',
    '.kk..............kFEEDDDOBBOOOBBDDDEEFFk.....',
    '..................kFEEDDDDDDDDDDDDEEFFk......',
    '...................kFEEDDDDDDDDDDEEFFk.......',
    '....................kFEEEEEEEEEDEEFFk........',
    '....................kEEEEEEEEEEEEFFk.........',
    '.....................kkFFFFFFFFEFFk..........',
    '.......................kkkkkkkkkkk...........',
]
# 放電中：発電板が 白く 光る
BODY_HOT = [
    '....................................kkkkkk...',
    '........kkkkkkkk...................kAABYyyk..',
    '.......kAAAAAAAAkk................kAAAYYyDDk.',
    '......kABBBAAAABAAk..............kAAABYyyDDEk',
    '.....kAABBBBYYYBAAAk.............kAAAYYyDDEEk',
    '....kAABYyDDyyyBBAAAk...........kAAABYyyDDEEk',
    '...kAABYDDDDDDDBBYAAAk..........kAAAYYyDDEEFk',
    '..kAABBDDEEEEEDDyYBAAAk........kAAABYyyDDEEFk',
    '..kABBDEEFkFFEEDDyYBAAAk.......kAAABByDDEEFFk',
    '.kABBDEFkk.kkFEEDDBBBAAAk.....kAAABBBBDDEEFk.',
    '.kABDEFk.....kFEDDBBYBAAAk...kAAABYYyDDEEFFk.',
    '.kABDEk......kFEEDDyYYBAAAkkkAAABBYyyDDEEFk..',
    'kABDEk........kFEEDDyYBBAAAAAAABBBByDDEEFFk..',
    'kABDFk.........kFEEDDBBBBAAAAABYYBBDDDEEFk...',
    'kBDEk..........kFEEEDDBYYBBBBBYYyyDDDEEFFk...',
    'kBEk............kFEEEDDyYYBYYYByyDDDEEFFk....',
    '.kk..............kFEEDDDyBByyyBBDDDEEFFk.....',
    '..................kFEEDDDDDDDDDDDDEEFFk......',
    '...................kFEEDDDDDDDDDDEEFFk.......',
    '....................kFEEEEEEEEEDEEFFk........',
    '....................kEEEEEEEEEEEEFFk.........',
    '.....................kkFFFFFFFFEFFk..........',
    '.......................kkkkkkkkkkk...........',
]
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]
SEG = [(0, 12), (12, 24), (24, 35), (35, 45)]   # うねり用に 4つに 切る

# 稲妻形の 背びれ（先が うしろ上へ）
BOLT = [
    'kk.....',
    'kYkk...',
    '.kYYk..',
    '..kYyk.',
    '.kYYyk.',
    'kYyyyk.',
    '.kkYyyk',
    '..kYyyk',
    '.kYyyOk',
]
BOLT_S = [
    'kk....',
    'kYk...',
    '.kYk..',
    '.kYyk.',
    'kYyyk.',
    '.kYyyk',
    '.kyyOk',
]
# 尾の 先の 稲妻
TAILBOLT = [
    '..kkk.',
    '.kyyOk',
    'kYyOk.',
    '.kYyk.',
    '..kYk.',
    '.kYk..',
    'kYk...',
    'kk....',
]
# 頭：平たく 大きな 口、光る つり目、ほおにも 発電板
HEAD = [
    '.....kkkkk...........',
    '...kkAAAAAkkk........',
    '..kAAAAAAAAAAkk......',
    '.kAABBBBBBBAAAAkk....',
    '.kABBBBBBBBBBBAAAkk..',
    'kAABBkkkkkBBBBBBBAAk.',
    'kABBBBkYYwkkkBBBBBBAk',
    'kABBBBkyyYkBBBBBBBBBk',
    'kByykBBkkkBBBBBBBBBDk',
    'kBOOkBBBBBBBBBBBBBDDk',
    'kDBBBBkkkkkkkkkkkkkk.',
    'kDBBBkwkwkkwkkwkkwk..',
    'kDDBkEEEkEEEkEEEkEk..',
    '.kDDEEEEEEEEEEEEEEk..',
    '..kDFFFFFFFFFFFFFk...',
    '...kkkkkkkkkkkkkk....',
]
def _eye(h, a, b):
    h = list(h); h[6] = h[6][:6] + a + h[6][6 + len(a):]; h[7] = h[7][:6] + b + h[7][6 + len(b):]; return h
HEAD_OPEN = HEAD[:10] + [
    'kDBBBBkkkkkkkkkkkkkk.',
    'kDBBBkwkwkrrrrrrrrrk.',
    'kDDBkrrrrrrrrrrrrrk..',
    '.kDDkrrrrrrrrrrrrrrk.',
    '.kDDkwkkwkkwkkwkkwkk.',
    '..kDEEEEEEEEEEEEEEk..',
    '...kFFFFFFFFFFFFFk...',
    '....kkkkkkkkkkkkk....',
]
HEAD_OPEN = _eye(HEAD_OPEN, 'kYYYwk', 'kYYYYk')
HEAD_HOT = _eye(HEAD, 'kYYYwk', 'kYYYYk')
HEAD_BLINK = _eye(HEAD, 'kkkkkk', 'kBBBBk')
HEAD_HIT = _eye(HEAD, 'kYkYkk', 'kkykBk')
HEAD_KO = _eye(HEAD, 'kykykk', 'kBkBkk')
# 頭の 稲妻の つの
HBOLT = [
    'kkk.....',
    'kYYkk...',
    '.kkYYk..',
    '..kYyyk.',
    '.kYyyOk.',
    'kYyyyOk.',
]
# 放電（攻撃）：体の まわりに 稲妻が 走る
ZIG = [
    '...kk..',
    '..kYk..',
    '.kYwk..',
    'kYwYkk.',
    'kkYwYk.',
    '..kYk..',
    '.kYk...',
    '.kk....',
]
ZIG2 = [r[::-1] for r in ZIG]
# 前へ とぶ 電撃の 帯
ZAP = [
    '.....k......k......',
    '...kkYk...kkYk..c..',
    'kkkYwwYkkkYwwYkkYk.',
    'YwwwYYwwYwwYYwwwwYc',
    'kkkkkkYkkkkkkYkkkk.',
    '......k......k.....',
]
# ため：小さな 火花
SPARK = ['.c...c.', 'cYc.cYc', '.c...c.']

def layers():
    L = []
    hot = 'atk0|atk1'
    for i, (a, b) in enumerate(SEG):
        L.append(dict(n=f's{i}', g=f's{i}', x=2 + a, y=33, rows=cut(BODY, a, b), alt={hot: cut(BODY_HOT, a, b)}))
    return [
        dict(n='tbolt', g='s0', x=2, y=49, rows=TAILBOLT),
        dict(n='bolt1', g='s0', x=6, y=27, rows=BOLT_S),
        dict(n='bolt2', g='s1', x=12, y=26, rows=BOLT),
        dict(n='bolt3', g='s2', x=29, y=36, rows=BOLT_S),
        dict(n='bolt4', g='s3', x=34, y=31, rows=BOLT),
    ] + L + [
        dict(n='hbolt', g='head', x=35, y=19, rows=HBOLT),
        dict(n='head', g='head', x=37, y=24, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN, 'atk0': HEAD_HOT, 'blink': HEAD_BLINK, 'hit': HEAD_HIT, 'ko': HEAD_KO}),
        dict(n='spark', g='head', x=29, y=22, rows=SPARK, only='idle2'),
        dict(n='z1', g='s0', x=1, y=21, rows=ZIG, only='atk1'),
        dict(n='z2', g='s1', x=17, y=19, rows=ZIG2, only='atk1'),
        dict(n='z3', g='s1', x=12, y=47, rows=ZIG2, only='atk1'),
        dict(n='z4', g='s2', x=28, y=54, rows=ZIG, only='atk1'),
        dict(n='z5', g='s3', x=45, y=48, rows=ZIG2, only='atk1'),
        dict(n='z6', g='head', x=31, y=15, rows=ZIG, only='atk1|atk0'),
        dict(n='zap', g='head', x=58, y=34, rows=ZAP, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'s1': (0, -1), 'head': (0, 0)}, 'idle2': {'s1': (0, -1), 's2': (0, -1), 'head': (0, -1)}, 'idle3': {'s2': (0, -1)},
    'blink': {},
    'walk0': {'s0': (0, -1), 's2': (0, 1)}, 'walk1': {'s1': (0, -1), 's3': (0, 1), 'head': (0, 1)},
    'walk2': {'s0': (0, 1), 's2': (0, -1)}, 'walk3': {'s1': (0, 1), 's3': (0, -1), 'head': (0, -1)},
    'atk0': {'root': (-2, 0), 's1': (0, -1), 'head': (-1, 1)}, 'atk1': {'root': (3, -1), 'head': (1, 0)}, 'atk2': {'root': (5, 0), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -2), 's3': (0, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 's3', 's0': 'root', 's1': 'root', 's2': 'root', 's3': 'root'}
