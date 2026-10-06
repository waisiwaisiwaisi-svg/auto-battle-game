# カゲヒョウ（あく × ヒョウ）手打ち GBA風
import math
import pix
META = dict(id='kagehyo', name='カゲヒョウ', types=['dark'], base='ヒョウ', size='M')
PAL = {
    'k': '#101018', 'l': '#22163a',
    'A': '#8a7abc', 'B': '#54478a', 'C': '#2e2556',
    'D': '#120a20', 'P': '#c86cff',
    'Y': '#d8ff3a', 'R': '#a8184c', 'w': '#ffffff',
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

# ---- 胴：肩が 高く 盛り上がり、腰は 低い。影の 斑点 ----
BODY_M = [
    '.....................######.......',
    '..........##################......',
    '......########################....',
    '...#############################..',
    '..###############################.',
    '.################################.',
    '##################################',
    '##################################',
    '##################################',
    '.#################################',
    '..###############################.',
    '...############################...',
    '....#######..........#########....',
    '.....####.............#######.....',
]
BODY = pix.outline(spots(shade(BODY_M, {'#': 'ABC'}, low=10),
                         [(5, 4, 0), (12, 2, 1), (17, 4, 2), (23, 2, 0), (29, 4, 3), (9, 8, 3), (15, 8, 0), (22, 7, 1), (27, 9, 2), (2, 7, 1)]))

# ---- 足：太い 前足、大きな 爪 ----
FLEG_M = [
    '.######..',
    '########.',
    '########.',
    '########.',
    '.######..',
    '.#####...',
    '..####...',
    '..###....',
    '..###....',
    '..###....',
    '..###....',
    '..###....',
    '..####...',
    '.######..',
    '#######..',
]
FLEG = notop(pix.outline(put(shade(FLEG_M, {'#': 'ABC'}), ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '.k.k.kw'])))
HLEG_M = [
    '...######...',
    '.#########..',
    '###########.',
    '###########.',
    '###########.',
    '.#########..',
    '..#######...',
    '...#####....',
    '....####....',
    '....###.....',
    '...###......',
    '..###.......',
    '..###.......',
    '..###.......',
    '..####......',
    '.######.....',
    '#######.....',
]
HLEG = notop(pix.outline(put(spots(shade(HLEG_M, {'#': 'ABC'}), [(4, 2, 2)]), ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '.k.k.kw'])))
# とびかかる 前足（攻撃）：前へ のばし、爪を 全部 出す
REACH = [
    '..................kk...',
    '..kkkkkkkkkkkkkk.kwwk..',
    '.kAAAAAAAABBBBBBkkwk...',
    'kAABBBBBBBBBBBBBBkk.kk.',
    'kBBBBBBBBBBBBBBBBBkkwwk',
    '.kCCCCCCCCCCCCBBBkkk...',
    '..kkkkkkkkkkkkkkkkwwk..',
    '..................kk...',
]

# ---- 頭（手打ち）：低い 頭、まゆの 下で 光る 黄緑の 目、牙 ----
HEAD = [
    '.kk.kkkkk.........',
    'kAAkAAAAAkk.......',
    'kABAAABBBBBkk.....',
    '.kABBBBBBBBBBkk...',
    'kABBkkkkkkBBBBBk..',
    'kABBBBBBkkkAAAAABk',
    'kBBDBBBkkBBBBBBBBk',
    'kBCBDBBBBBBBBBBkkk',
    'kCBCBBBBBBBkkkkkk.',
    'kCCBBBBBkkwkwkwk..',
    '.kCCBBBkRRRRRk....',
    '..kCCBBBkkwkwk....',
    '...kkCCCCCCk......',
    '.....kkkkkk.......',
]
HEAD_OPEN = HEAD[:8] + [
    'kCBCBBBBBkkkkkkkk.',
    'kCCBBBBkwkwkwkwk..',
    '.kCCBBkRRRRRRRk...',
    '.kCCBBkRRRRRRk....',
    '..kCCBBkwkwkwk....',
    '...kkCCCCCCCk.....',
    '.....kkkkkkk......',
]
EYE = ['YYk', 'kk.']
EYE_ALT = {'blink': ['kkk', '...'], 'hit': ['kBk', 'BkB'], 'atk0|atk1|atk2': ['YYY', 'kkk'], 'ko': ['kBk', 'BkB']}

# ---- しっぽ：長く 後ろへ のび、先が くるりと 上へ ----
def tail():
    W, H = 24, 22; g = pix.grid(W, H)
    def bez(p0, p1, p2, w0, w1):
        for i in range(80):
            t = i / 79
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            w = w0 + (w1 - w0) * t
            for yy in range(H):
                for xx in range(W):
                    if (xx + .5 - x) ** 2 + (yy + .5 - y) ** 2 <= w * w: g[yy][xx] = '#'
    bez((22, 3), (13, 21), (5, 12), 2.6, 2.2)      # 下へ たれて
    bez((5, 12), (1, 5), (6, 2), 2.2, 1.8)          # 先が 上へ くるり
    s = pix.grid_of(shade(pix.rows_of(g), {'#': 'ABC'}))
    for (x, y) in ((16, 12), (17, 13), (11, 15), (12, 15), (6, 12), (6, 13), (3, 7), (4, 7)):
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
        dict(n='tail', g='tail', x=1, y=26, rows=TAIL),
        dict(n='hlegF', g='legB', x=17, y=42, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=40, y=44, rows=dark(FLEG), not_='ko|atk1'),
        dict(n='body', g='body', x=9, y=28, rows=BODY),
        dict(n='hleg', g='legA', x=10, y=42, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=34, y=44, rows=FLEG, not_='ko|atk1'),
        dict(n='reach', g='legA', x=40, y=40, rows=REACH, only='atk1'),
        dict(n='head', g='head', x=42, y=29, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='eye', g='head', x=49, y=34, rows=EYE, alt=EYE_ALT),
        dict(n='mist', g='head', x=54, y=37, rows=MIST, alt={'idle1|idle3|walk1|walk3': MIST2}, not_=NB + '|ko'),
        dict(n='claw', g='fx', x=52, y=24, rows=CLAW, only='atk2'),
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
    'atk0': {'root': (-2, 0), 'body': (0, 3), 'head': (0, 1), 'tail': (0, -1)},
    'atk1': {'root': (6, -5), 'legB': (2, 2), 'head': (1, -1)},
    'atk2': {'root': (8, 0), 'fx': (0, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2)},
    'ko': {'body': (0, 15), 'head': (1, 2), 'tail': (0, 2)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
