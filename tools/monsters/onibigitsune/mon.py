# オニビギツネ（ゴースト・ほのお × キツネ）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく、胴を 小さく 丸く、足を 短く。しっぽは 大きい まま）
import pix
META = dict(id='onibigitsune', name='オニビギツネ', types=['ghost', 'fire'], base='キツネ', size='M')
PAL = {
    'k': '#101018', 'l': '#30295c',
    'A': '#fbfaff', 'B': '#cecce9', 'C': '#7c7ab0',
    'R': '#e82c4c',
    'V': '#e8fcff', 'X': '#78d4ff', 'Z': '#4a5cf0', 'D': '#28288c',
    'Y': '#ffd84a', 'y': '#d0861c', 'w': '#ffffff',
}
LIGHT = set('AVYw')

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
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'V': 'X', 'X': 'Z', 'Z': 'D', 'R': 'C'}
def dark(rows): return pix.recolor(rows, DARK)
def notop(r): return ['.' * len(r[0])] + r[1:]

# ---- 胴（小さく 丸く）----
BODY_M = [
    '....##########...',
    '..##############.',
    '.################',
    '#################',
    '#################',
    '.################',
    '..##############.',
    '...#####...#####.',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'ABC'}, low=6), [
    '', '',
    '.......R....R',
    '......R....R',
    '.....R....R',
]))
# 胸の 白い 毛（ぎざぎざ）
CHEST = [
    '..kkk..',
    '.kAAAk.',
    'kAAAABk',
    '.kAABBk',
    'kAABBk.',
    '.kABk..',
    'kAkk...',
    '.k.....',
]
# ---- 足（短く 太く）：先が 青い 鬼火に ほどける ----
FLEG_M = [
    '.####.',
    '######',
    '.####.',
    '.####.',
    '..###.',
    '..##..',
    '.%%%%.',
    '%%%%%%',
]
FLEG = notop(pix.outline(shade(FLEG_M, {'#': 'ABC', '%': 'VXZ'})))
HLEG_M = [
    '.######.',
    '########',
    '########',
    '.######.',
    '..####..',
    '...###..',
    '..###...',
    '.%%%%...',
    '%%%%%%..',
]
HLEG = notop(pix.outline(shade(HLEG_M, {'#': 'ABC', '%': 'VXZ'})))
# ---- 頭（手打ち・大きく）：赤い くまどり、するどい 金の つり目 ----
HEAD = [
    '.....kkkkkkk.............',
    '...kkAAAAAAAkk...........',
    '..kAAAAAABBBBBkk.........',
    'kAAAABBBBBBBBBBBkk.......',
    'kAABBBBBBBBBBBBBBBkk.....',
    'kABBRkkkkkkkkBBBBBBBkk...',
    'kABRRk.......kBBBBBBBBkk.',
    'kABBRRk......kBBBBBBBBBkk',
    'kBBBBRRkkkkkkBBBBBBBBBBCk',
    'kBBBBBBRBBBBBAAAAAAAAkkkk',
    'kBBBBBBBBBBAAAAAAAkkkk...',
    'kCBBBBBBBBBBBBkkkkAk.....',
    'kCBBBBBBBBBBBkAAAAk......',
    'kkCBBBBBBBBBBBkkkk.......',
    'kAkCBBBBBBBBCCk..........',
    '.kAkkCCCCCCCCk...........',
    '..kAkkkkkkkkk............',
    '...k.....................',
]
HEAD_OPEN = HEAD[:9] + [
    'kBBBBBBRBBBBBBBBBBBkkkkk.',
    'kBBBBBBBBBBBBBBkkAkAkk...',
    'kCBBBBBBBBBBBkZXXXXXk....',
    'kCBBBBBBBBBBkkAkAkkk.....',
    'kkCBBBBBBBBBBkkkk........',
    'kAkCBBBBBBBBCCk..........',
    '.kAkkCCCCCCCCk...........',
    '..kAkkkkkkkkk............',
    '...k.....................',
]
# 目：白い 光＋金と こがね色の 2色＋たての ひとみ。うしろの 目じりが 上がる つり目
EYE = ['wYYYkYy', '.yyyky']
EYE_ALT = {'blink': ['kkkkkkk', '.BBBBB'], 'hit': ['kkYkkkk', '.kykYk'], 'atk0|atk1|atk2': ['wwYYkYY', '.YyykY'], 'ko': ['BkBBkBk', '.BkkBB']}
EAR = [
    '.....k.',
    '....kk.',
    '...kAk.',
    '...kRk.',
    '..kARBk',
    '..kARBk',
    '.kAARBk',
    '.kARRBk',
    'kAABRBk',
    'kABBBBk',
    'kABBBCk',
]

# ---- 三本の しっぽ：根もとは 毛、先は 鬼火 ----
def tails(ph=0):
    W, H = 26, 30; out = pix.grid(W + 2, H + 2)
    T = [((22, 26), (21, 12), (13, 2)), ((21, 26), (11, 22), (4, 11)), ((21, 27), (9, 31), (2, 22))]
    FUR = [((18, 17), (18, 18), (17, 12), (17, 13)), ((10, 21), (11, 21), (8, 18), (9, 18)), ((8, 27), (9, 27), (11, 28), (12, 28))]
    for (p0, p1, p2), fur in zip(T, FUR):   # 奥（上）から 手前（下）へ 1本ずつ 輪郭つきで 重ねる
        g = pix.grid(W, H)
        for i in range(80):
            t = i / 79
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            w = 2.0 + 2.4 * (1 - abs(t - .6) / .6) if t < .92 else 2.4
            for yy in range(H):
                for xx in range(W):
                    if (xx + .5 - x) ** 2 + (yy + .5 - y) ** 2 <= w * w and g[yy][xx] == '.':
                        g[yy][xx] = '%' if t > .84 else '#'
        s = pix.grid_of(shade(pix.rows_of(g), {'#': 'ABC', '%': 'XXZ'}))
        for (x, y) in fur:
            if s[y][x] == 'B': s[y][x] = 'C'
        pix.stamp(out, pix.outline(pix.rows_of(s)), 0, 0)
    return pix.rows_of(out)
TAILS = tails()
# しっぽの 先で もえる 鬼火
ONI = [
    '....k.....',
    '...kVk..k.',
    '...kVk.kXk',
    '..kXVkkXk.',
    '.kXVVXXVk.',
    '.kXVVVVXk.',
    'kZXVVVVVXk',
    'kZXVVVVVXk',
    'kZXXVVVXZk',
    '.kZXXXXZk.',
    '..kkkkkk..',
]
ONI2 = [
    '......k...',
    '.k...kVk..',
    'kXk..kVk..',
    '.kXkkVXk..',
    '.kVXXVVXk.',
    '.kXVVVVXk.',
    'kZXVVVVVXk',
    'kZXVVVVVXk',
    'kZXXVVVXZk',
    '.kZXXXXZk.',
    '..kkkkkk..',
]
ORB = ['..kk..', '.kVXk.', 'kVVVXk', 'kXVXZk', '.kZZk.', '..kk..']
# ---- 鬼火の 玉（攻撃）----
BIG = [
    '.....k.......',
    '....kVk...k..',
    '....kVk..kXk.',
    '...kXVk.kXk..',
    '..kXVVXkXVk..',
    '..kXVVVXVVk..',
    '.kXVVVVVVVXk.',
    '.kXVVVVVVVXk.',
    'kZXVVVVVVVVXk',
    'kZXVVVVVVVVXk',
    'kZXXVVVVVVXZk',
    '.kZXXVVVVXZk.',
    '..kZZXXXXZk..',
    '...kkZZZZk...',
    '.....kkkk....',
]
FIREBALL = pix.rot90(pix.rot90(pix.rot90(BIG)))
WISPS = [
    '.kk.......kk....',
    'kXVk.....kVXk...',
    '.kk...kk..kk..kk',
    '.....kVXk....kXk',
    '..kk..kk......k.',
    '.kVXk.....kk....',
    '..kk.....kXk....',
    '..........k.....',
]

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='earF', g='head', x=37, y=21, rows=dark(EAR)),
        dict(n='tails', g='tail', x=2, y=22, rows=TAILS),
        dict(n='oni1', g='tail', x=10, y=16, rows=ONI, alt={'idle1|idle3|walk1|walk3|atk0': ONI2}),
        dict(n='oni2', g='tail', x=1, y=25, rows=ONI2, alt={'idle1|idle3|walk1|walk3|atk0': ONI}),
        dict(n='oni3', g='tail', x=0, y=36, rows=ONI, alt={'idle1|idle3|walk1|walk3|atk0': ONI2}),
        dict(n='hlegF', g='legB', x=25, y=50, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=39, y=51, rows=dark(FLEG), not_='ko'),
        dict(n='body', g='body', x=20, y=43, rows=BODY),
        dict(n='hleg', g='legA', x=19, y=50, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=33, y=51, rows=FLEG, not_='ko'),
        dict(n='chest', g='body', x=35, y=43, rows=CHEST),
        dict(n='head', g='head', x=32, y=29, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='ear', g='head', x=40, y=21, rows=EAR),
        dict(n='eye', g='head', x=38, y=35, rows=EYE, alt=EYE_ALT),
        dict(n='orb', g='fx', x=56, y=47, rows=ORB, not_=NB + '|ko'),
        dict(n='fireball', g='fx', x=57, y=30, rows=FIREBALL, only='atk1'),
        dict(n='wisps', g='fx', x=56, y=28, rows=WISPS, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'fx': (0, -1)},
    'idle2': {'body': (0, 1), 'fx': (0, -2)},
    'idle3': {'body': (0, 0), 'fx': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 1), 'tail': (1, -1)},
    'atk1': {'root': (3, 0), 'head': (1, 1)},
    'atk2': {'root': (4, 0), 'fx': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'tail': (1, 0)},
    'ko': {'body': (0, 8), 'head': (2, 3), 'tail': (2, 3)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
