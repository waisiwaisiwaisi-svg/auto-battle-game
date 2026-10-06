# ライデンウナギ（でんき・みず × ウナギ）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく、体の うねりは そのまま）
from pix import outline
EYE_BOX = (45, 22, 9, 5)
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
# ---- デフォルメの 体：太く 短い S字（あたりは 道すじ＋太さ、発電板と 模様は 手で 置く）----
PATH = [(5, 52), (10, 47), (17, 45), (24, 48), (31, 51), (37, 48), (41, 42), (43, 36)]
RAD = [2.2, 3.4, 4.6, 5.4, 6.0, 6.3, 6.5, 6.5]
def body(hot=False):
    W, H = 64, 64; g = [['.'] * W for _ in range(H)]
    for y in range(30, 62):
        for x in range(0, 54):
            best = None
            for i in range(len(PATH) - 1):
                (ax, ay), (bx, by) = PATH[i], PATH[i + 1]
                dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
                t = max(0, min(1, ((x + .5 - ax) * dx + (y + .5 - ay) * dy) / L2))
                px, py = ax + t * dx, ay + t * dy; d = ((x + .5 - px) ** 2 + (y + .5 - py) ** 2) ** .5
                L = L2 ** .5; nx, ny = -dy / L, dx / L
                if nx + 2 * ny > 0: nx, ny = -nx, -ny
                r = RAD[i] + (RAD[i + 1] - RAD[i]) * t
                if best is None or d - r < best[0]: best = (d - r, ((x + .5 - px) * nx + (y + .5 - py) * ny) / r, i, t)
            if best[0] <= 0:
                v = best[1]
                g[y][x] = 'A' if v > .62 else 'B' if v > .05 else 'D' if v > -.25 else 'E' if v > -.7 else 'F'
    # 発電板：わき腹（B と D の さかい）に 2ドットずつ 手で 置く
    for x in range(0, 54):
        col = [y for y in range(H) if g[y][x] == 'D']
        if not col or x % 4 > 1: continue
        y = col[0]
        g[y][x] = 'Y' if hot else 'y'
        if y + 1 < H and g[y + 1][x] == 'D': g[y + 1][x] = 'y' if hot else 'O'
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return [''.join(r) for r in out]
BODY, BODY_HOT = body(), body(True)
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]
SEG = [(0, 14), (14, 26), (26, 36), (36, 64)]   # うねり用に 4つに 切る
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
# 頭（大きく）：平たく 大きな 口、光る つり目（2段の 虹彩＋たての ひとみ）、ほおにも 発電板
HEAD_TOP = [
    ".......AAAAAAA............",
    "....AAAAAAAAAAAAA.........",
    "..AAABBBBBBBBBBBAAA.......",
    ".AABBBBBBBBBBBBBBBAAA.....",
    "AABBBBBBBBBBBBBBBBBBAAA...",
    "ABBBBBBBBBBBBBBBBBBBBBAA..",
    "ABBBBBBBBBBBBBBBBBBBBBBBA.",
    "ABBBBBBBBBBBBBBBBBBBBBBBBA",
    "BBBBBBBBBBBBBBBBBBBBBBBBBD",
    "BBBBBBBBBBBBBBBBBBBBBBBBDD",
    "BBBBBBBBBBBBBBBBBBBBBBBDD.",
]
HEAD_BOT = [
    "DDBBBBkEEEkEEEkEEEkEEk....",
    ".DDBBEEEEEEEEEEEEEEEEk....",
    "..DDEEEEEEEEEEEEEEEEk.....",
    "...DFFFFFFFFFFFFFFFk......",
    "....FFFFFFFFFFFFF.........",
]
# 目（E 光る目）：瞳なし。白い 芯→黄白→稲妻の 黄の 光が 前下へ とがる 逆三角形。ふちは 黒線の かわりに だいだいの にじみ、前の 角に 水色の 火花
EYES = {   # 前下へ ななめに 走る 稲妻の 切れ目の 形
    'open':  ['kk.......', '.kkkkk...', '.OYwwyOkk', '..OyYwYOk', '...OOyyOc', '.....OO..'],
    'hot':   ['kk.......', '.kkkkk...', '.YwwwwYkk', '.OYwwwwYc', '..OOYwYOc', '....OOO..'],
    'blink': ['kk.......', '.kkkkk...', '.kkkkkkkk', '..OOyyOOk', '.....OO..', '.........'],
    'hit':   ['kk.......', '.kkkkk...', '.OYkwyOkk', '..OkYOkOk', '...OkyO..', '.........'],
    'ko':    ['kk.......', '.kkkkk...', '..O...Okk', '...O.O...', '....O....', '...O.O...'],
}
def head(eye='open', gape=0):
    rows = list(HEAD_TOP) + ["DBBBBBBBkkkkkkkkkkkkkkkk..", "DBBBBBBkwkwkkwkkwkkwkkwk.."]
    rows += ["DBBBBBkrrrrrrrrrrrrrrrrk.." if i < gape - 1 else "DBBBBBkwkkwkkwkkwkkwkkk..." for i in range(gape)]
    rows += HEAD_BOT
    g = [list(r) for r in rows]
    for j, r in enumerate(EYES[eye]):
        for i, c in enumerate(r):
            if c != '.': g[3 + j][9 + i] = c
    for (x, y, c) in ((2, 8, 'k'), (3, 8, 'y'), (4, 8, 'y'), (5, 8, 'k'), (2, 9, 'k'), (3, 9, 'O'), (4, 9, 'O'), (5, 9, 'k')):   # ほおの 発電板
        g[y][x] = c
    for (x, y) in ((6, 2), (7, 2), (3, 4), (2, 5)): g[y][x] = 'A'
    for (x, y) in ((19, 6), (20, 7), (21, 7), (17, 9), (18, 10)): g[y][x] = 'D'
    return outline([''.join(r) for r in g])
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
        L.append(dict(n=f's{i}', g=f's{i}', x=a, y=0, rows=cut(BODY, a, b), alt={hot: cut(BODY_HOT, a, b)}))
    return [
        dict(n='tbolt', g='s0', x=0, y=50, rows=TAILBOLT),
        dict(n='bolt1', g='s0', x=8, y=37, rows=BOLT_S),
        dict(n='bolt2', g='s1', x=17, y=35, rows=BOLT),
        dict(n='bolt3', g='s2', x=27, y=39, rows=BOLT_S),
        dict(n='bolt4', g='s3', x=33, y=33, rows=BOLT),
    ] + L + [
        dict(n='hbolt', g='head', x=36, y=13, rows=HBOLT),
        dict(n='head', g='head', x=35, y=17, rows=head(), alt={'atk1|atk2': head('hot', 3), 'atk0': head('hot'), 'blink': head('blink'), 'hit': head('hit'), 'ko': head('ko')}),
        dict(n='spark', g='head', x=28, y=17, rows=SPARK, only='idle2'),
        dict(n='z1', g='s0', x=1, y=36, rows=ZIG, only='atk1'),
        dict(n='z2', g='s1', x=21, y=28, rows=ZIG2, only='atk1'),
        dict(n='z3', g='s1', x=14, y=53, rows=ZIG2, only='atk1'),
        dict(n='z4', g='s2', x=30, y=56, rows=ZIG, only='atk1'),
        dict(n='z5', g='s3', x=47, y=50, rows=ZIG2, only='atk1'),
        dict(n='z6', g='head', x=29, y=10, rows=ZIG, only='atk1|atk0'),
        dict(n='zap', g='head', x=60, y=30, rows=ZAP, only='atk1|atk2'),
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
