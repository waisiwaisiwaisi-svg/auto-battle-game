# カゲヒョウ（あく × ヒョウ）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく、胴は 短く 丸く、足は 短く 太く）
import math
import pix
META = dict(id='kagehyo', name='カゲヒョウ', types=['dark'], base='ヒョウ', size='M')
PAL = {
    'k': '#101018', 'l': '#22163a',
    'A': '#8a7abc', 'B': '#54478a', 'C': '#2e2556',
    'D': '#120a20', 'P': '#c86cff',
    'Y': '#d8ff3a', 'G': '#6f9a10', 'R': '#a8184c', 'w': '#ffffff',
}
LIGHT = set('APYw')

def shade(rows, ramps, low=99):
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            hi, mid, lo = ramps[m]
            def e(dy, dx):
                yy, xx = y + dy, x + dx
                return not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m
            a = e(-1, 0) or e(-2, 0) or (e(0, -1) and y < low)
            b = e(1, 0) or e(0, 1) or e(1, 1) or e(0, 2)
            c = lo if y >= low else mid
            if a and not b: c = hi
            elif b and not a: c = lo
            o[y][x] = c
    return pix.rows_of(o)
def put(base, over, x=0, y=0):
    g = pix.grid_of(base); w = max(len(r) for r in over) + x; h = len(over) + y
    if w > len(g[0]): g = [r + ['.'] * (w - len(r)) for r in g]
    while len(g) < h: g.append(['.'] * len(g[0]))
    pix.stamp(g, over, x, y); return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'P': 'B', 'w': 'A'}
def dark(rows): return pix.recolor(rows, DARK)
def notop(r): return ['.' * len(r[0])] + r[1:]
# 影の 斑点：形は 3種、ふちの 下側だけ 紫に 光る
BLOT = [['.DDD.', 'DDDDP', '.DDP.'], ['DD.', 'DDP', '.P.'], ['.DD', 'DDP'], ['DDD', '.DP']]
def spots(g, pts):
    g = pix.grid_of(g)
    for (x, y, n) in pts:
        for j, r in enumerate(BLOT[n]):
            for i, c in enumerate(r):
                if c != '.' and g[y + j][x + i] in 'ABC': g[y + j][x + i] = c
    return pix.rows_of(g)

# ---- 胴：短く 丸く、肩（右）が 盛り上がる。影の 斑点 ----
BODY_M = [
    '............#####...',
    '.......###########..',
    '....###############.',
    '..#################.',
    '.###################',
    '####################',
    '####################',
    '####################',
    '####################',
    '.###################',
    '..#################.',
    '...###############..',
    '.....###########....',
]
BODY = pix.outline(spots(shade(BODY_M, {'#': 'ABC'}, low=10),
                         [(4, 4, 0), (9, 2, 1), (14, 3, 2), (7, 7, 3), (12, 7, 0), (2, 7, 1), (16, 6, 1)]))

# ---- 足：短く 太い。上の 4行は 胴の 中に 食いこむ ----
FLEG_M = [
    '.######.',
    '########',
    '########',
    '.######.',
    '.#####..',
    '..####..',
    '..####..',
    '..####..',
    '..####..',
    '.######.',
    '#######.',
]
FLEG = notop(pix.outline(put(shade(FLEG_M, {'#': 'ABC'}), ['', '', '', '', '', '', '', '', '', '', '.k.k.kw'])))
HLEG_M = [
    '..#######.',
    '.#########',
    '##########',
    '##########',
    '.########.',
    '..######..',
    '...####...',
    '...####...',
    '...####...',
    '..######..',
    '.#######..',
]
HLEG = notop(pix.outline(put(spots(shade(HLEG_M, {'#': 'ABC'}), [(4, 1, 2)]), ['', '', '', '', '', '', '', '', '', '', '.k.k.kw'])))
# とびかかる 前足（攻撃）：前へ のばし、爪を 全部 出す
REACH = [
    '..............kk...',
    '..kkkkkkkkkk.kwwk..',
    '.kAAAAAABBBBkkkwk..',
    'kAABBBBBBBBBBkk.kk.',
    'kBBBBBBBBBBBBBkkwwk',
    '.kCCCCCCCCCBBBkkk..',
    '..kkkkkkkkkkkkkwwk.',
    '...............kk..',
]

# ---- 頭（大きく：たて 17 × よこ 23）：低い まゆ、光る 目、牙 ----
HEAD_M = [
    '...##...............',
    '..####..............',
    '.#####.#####........',
    '.###############....',
    '#################...',
    '##################..',
    '##################..',
    '###################.',
    '####################',
    '####################',
    '####################',
    '###################.',
    '.#################..',
    '..###############...',
    '....###########.....',
]
def head(open_=False):
    g = pix.grid_of(shade(HEAD_M, {'#': 'ABC'}))
    def at(x, y, c):
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = c
    for (x, y) in ((3, 1), (3, 2), (2, 2)): at(x, y, 'C')            # 耳の 内
    for (x, y) in ((2, 5), (3, 5), (2, 6), (3, 9), (4, 9), (4, 10), (1, 11), (2, 11)): at(x, y, 'D')   # ほほの 斑点
    for (x, y) in ((8, 3), (9, 3)): at(x, y, 'D')
    at(19, 8, 'k'); at(18, 8, 'k'); at(19, 7, 'C')                    # 鼻
    if not open_:
        for x in range(8, 20): at(x, 10, 'k')                         # 口の 線
        for x in (10, 15, 18): at(x, 11, 'w')                         # 上の 牙
        at(10, 12, 'w')
        for x in range(9, 18): at(x, 11, 'R') if g[11][x] != 'w' else None
        for x in range(9, 18): at(x, 12, 'k') if x != 10 else None
        for x in (12, 14, 16): at(x, 12, 'w')
    else:
        for x in range(8, 20): at(x, 9, 'k')
        for y in (10, 11, 12):
            for x in range(8, 20 - (y - 10) * 2): at(x, y, 'R')
        for x in (10, 13, 16, 18): at(x, 10, 'w')
        at(10, 11, 'w')
        for x in range(8, 19): at(x, 13, 'k')
        for x in (11, 14, 17): at(x, 12, 'w')
    return pix.outline(pix.rows_of(g))
HEAD = head(); HEAD_OPEN = head(True)
# 目：まゆの ひさし＋光 w＋虹彩 2色（Y／G）＋たての ひとみ＋下まぶた
EYE = ['kkkk.....', '.kkkkkkk.', '.kwwYYkYk', '.kwYYYkYk', '..kGGGkGk', '...kkkkk.']
EYE_ALT = {
    'blink': ['kkkk.....', '.kkkkkkk.', '.kBBBBBBk', '.kkkkkkkk', '..BBBBBB.', '.........'],
    'hit': ['.........', 'kkkkkkkk.', '.Akk.kkA.', '..AkkkA..', '.kkA.Akk.', '.........'],
    'atk0|atk1|atk2': ['kkkk.....', '.kkkkkkk.', '.kwwYYkYk', '.kwYYYkYk', '..kYYYkYk', '...kkkkk.'],
    'ko': ['.........', '.kA..kA..', '..kAkA...', '...kA....', '..kAkA...', '.kA..kA..'],
}

# ---- しっぽ：後ろへ たれて、先が くるりと 上へ（根もとは 胴に 食いこむ）----
def tail():
    W, H = 18, 20; g = pix.grid(W, H)
    def bez(p0, p1, p2, w0, w1):
        for i in range(80):
            t = i / 79
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            w = w0 + (w1 - w0) * t
            for yy in range(H):
                for xx in range(W):
                    if (xx + .5 - x) ** 2 + (yy + .5 - y) ** 2 <= w * w: g[yy][xx] = '#'
    bez((17, 6), (9, 18), (5, 11), 2.0, 1.6)
    bez((5, 11), (2, 5), (6, 3), 1.6, 1.3)
    s = pix.grid_of(shade(pix.rows_of(g), {'#': 'ABC'}))
    for (x, y) in ((12, 12), (13, 12), (8, 14), (5, 11), (3, 6)):
        if s[y][x] in 'AB': s[y][x] = 'D'
    return pix.outline(pix.rows_of(s))
TAIL = tail()

# ---- 口から あふれる 黒い もや ----
MIST = [
    '...kk.....',
    '..kCCk.kk.',
    '.kCBCCkCCk',
    'kCBCDCCBCk',
    '.kCCkkCCk.',
    '..kk..kk..',
]
MIST2 = [
    '....kk....',
    '.kk.kCk...',
    'kCCkkCCkk.',
    'kCBCCDCBCk',
    '.kkCCkCCk.',
    '...kk.kk..',
]
# ---- 影の 爪あと（攻撃）----
CLAW = [
    '.........kk..kk..',
    '........kPk.kPk..',
    '.......kPwkkPwk.k',
    '......kPwkkPwk.kP',
    '.....kPwkkPwk.kPw',
    '....kPwkkPwk.kPwk',
    '...kPwkkPwk.kPwk.',
    '..kPwkkPwk.kPwk..',
    '.kPPkkPPk.kPwk...',
    '.kPk.kPk.kPPk....',
    '.kk..kk..kPk.....',
    '.........kk......',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=-1, y=30, rows=TAIL),
        dict(n='hlegF', g='legB', x=18, y=46, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=34, y=47, rows=dark(FLEG), not_='ko|atk1'),
        dict(n='body', g='body', x=14, y=34, rows=BODY),
        dict(n='hleg', g='legA', x=13, y=46, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=29, y=47, rows=FLEG, not_='ko|atk1'),
        dict(n='reach', g='legA', x=34, y=42, rows=REACH, only='atk1'),
        dict(n='head', g='head', x=32, y=24, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='eye', g='head', x=40, y=28, rows=EYE, alt=EYE_ALT),
        dict(n='mist', g='head', x=48, y=38, rows=MIST, alt={'idle1|idle3|walk1|walk3': MIST2}, not_=NB + '|ko'),
        dict(n='claw', g='fx', x=50, y=20, rows=CLAW, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 2), 'head': (0, 1), 'tail': (0, -1)},
    'atk1': {'root': (6, -4), 'legB': (2, 2), 'head': (1, -1)},
    'atk2': {'root': (8, 0), 'fx': (0, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -2)},
    'ko': {'body': (0, 11), 'head': (1, 1), 'tail': (0, 1)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
