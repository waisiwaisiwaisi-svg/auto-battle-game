# オニビギツネ（ゴースト・ほのお × キツネ）手打ち GBA風
import pix
META = dict(id='onibigitsune', name='オニビギツネ', types=['ghost', 'fire'], base='キツネ', size='M')
PAL = {
    'k': '#101018', 'l': '#30295c',
    'A': '#fbfaff', 'B': '#cecce9', 'C': '#7c7ab0',
    'R': '#e82c4c',
    'V': '#e8fcff', 'X': '#78d4ff', 'Z': '#4a5cf0', 'D': '#28288c',
    'Y': '#ffd84a',
}
LIGHT = set('AVY')

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

# ---- 胴 ----
BODY_M = [
    '.......###############...',
    '....####################.',
    '..#######################',
    '.########################',
    '#########################',
    '#########################',
    '.########################',
    '..######################.',
    '...#######.......#####...',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'ABC'}, low=6), [
    '', '',
    '..........R.....R',
    '.........R.....R',
    '........R.....R',
]))
# 胸の 白い 毛（ぎざぎざ）
CHEST = [
    '..kkk...',
    '.kAAAk..',
    'kAAAABk.',
    'kAAAABk.',
    '.kAABBk.',
    'kAABBk..',
    '.kABk...',
    'kAkk....',
    '.k......',
]
# ---- 足：先が 青い 鬼火に ほどける ----
FLEG_M = [
    '.####.',
    '#####.',
    '.####.',
    '.###..',
    '..##..',
    '..##..',
    '..##..',
    '..##..',
    '..##..',
    '..##..',
    '..%%..',
    '.%%%%.',
    '%%%%%%',
]
FLEG = notop(pix.outline(shade(FLEG_M, {'#': 'ABC', '%': 'VXZ'})))
HLEG_M = [
    '.######.',
    '########',
    '########',
    '########',
    '.######.',
    '..####..',
    '...###..',
    '...##...',
    '..##....',
    '..##....',
    '..##....',
    '..%%....',
    '.%%%%...',
    '%%%%%%..',
]
HLEG = notop(pix.outline(shade(HLEG_M, {'#': 'ABC', '%': 'VXZ'})))
NECK_M = [
    '...######',
    '..#######',
    '..######.',
    '.#######.',
    '.######..',
    '#######..',
    '#######..',
    '########.',
]
NECK = notop(pix.outline(shade(NECK_M, {'#': 'ABC'})))
# ---- 頭（手打ち）：赤い くまどり、細い 金の 目 ----
HEAD = [
    '....kkkkkk..........',
    '..kkAAAAAAkk........',
    '.kAAAAABBBBBkk......',
    'kAAABBBBBBBBBBkk....',
    'kAABkkkkkkBBBBBBkk..',
    'kABRRRBBkkkAAAAAABkk',
    'kABBBRRBBBkBBBBBBBkk',
    'kBBBBBBRBBBBBBBBkkkk',
    'kBBBBBBBBBBBBkkkk...',
    'kCBBBBBBBkkAAk......',
    'kkCBBBBBBBAAk.......',
    'kAkCBBBBBCk.........',
    '.kAkkCCCCk..........',
    '..k..kkkk...........',
]
HEAD_OPEN = HEAD[:7] + [
    'kBBBBBBRBBBBBBkkkk..',
    'kBBBBBBBBBkkkAkAk...',
    'kCBBBBBBkZXXXXk.....',
    'kkCBBBBBkkAkAkk.....',
    'kAkCBBBBBCkk........',
    '.kAkkCCCCk..........',
    '..k..kkkk...........',
]
EYE = ['YYYk']
EYE_ALT = {'blink': ['kkkk'], 'hit': ['kBkB'], 'atk0|atk1|atk2': ['VYYY'], 'ko': ['BkBk']}
EAR = [
    '....k.',
    '...kk.',
    '..kAk.',
    '..kRk.',
    '.kARBk',
    '.kARBk',
    'kAARBk',
    'kABBBk',
    'kABBCk',
]

# ---- 三本の しっぽ：根もとは 毛、先は 鬼火 ----
def tails(ph=0):
    W, H = 30, 38; out = pix.grid(W + 2, H + 2)
    T = [((26, 33), (25, 16), (15, 3)), ((25, 33), (13, 28), (4, 14)), ((25, 34), (10, 38), (1, 28))]
    FUR = [((21, 21), (21, 22), (20, 15), (20, 16)), ((12, 27), (13, 27), (9, 23), (10, 23)), ((9, 33), (10, 33), (13, 35), (14, 35))]
    for (p0, p1, p2), fur in zip(T, FUR):   # 奥（上）から 手前（下）へ 1本ずつ 輪郭つきで 重ねる
        g = pix.grid(W, H)
        for i in range(80):
            t = i / 79
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            w = 2.4 + 2.8 * (1 - abs(t - .6) / .6) if t < .92 else 2.8
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
        dict(n='earF', g='head', x=39, y=13, rows=dark(EAR)),
        dict(n='tails', g='tail', x=0, y=6, rows=TAILS),
        dict(n='oni1', g='tail', x=11, y=1, rows=ONI, alt={'idle1|idle3|walk1|walk3|atk0': ONI2}),
        dict(n='oni2', g='tail', x=0, y=12, rows=ONI2, alt={'idle1|idle3|walk1|walk3|atk0': ONI}),
        dict(n='oni3', g='tail', x=-3, y=26, rows=ONI, alt={'idle1|idle3|walk1|walk3|atk0': ONI2}),
        dict(n='hlegF', g='legB', x=21, y=45, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=40, y=46, rows=dark(FLEG), not_='ko'),
        dict(n='body', g='body', x=17, y=36, rows=BODY),
        dict(n='hleg', g='legA', x=15, y=45, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=35, y=46, rows=FLEG, not_='ko'),
        dict(n='neck', g='body', x=35, y=29, rows=NECK),
        dict(n='chest', g='body', x=38, y=33, rows=CHEST),
        dict(n='head', g='head', x=37, y=21, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='ear', g='head', x=43, y=13, rows=EAR),
        dict(n='eye', g='head', x=44, y=26, rows=EYE, alt=EYE_ALT),
        dict(n='orb', g='fx', x=53, y=39, rows=ORB, not_=NB + '|ko'),
        dict(n='fireball', g='fx', x=55, y=21, rows=FIREBALL, only='atk1'),
        dict(n='wisps', g='fx', x=56, y=18, rows=WISPS, only='atk2'),
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
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 2), 'tail': (1, -1)},
    'atk1': {'root': (3, 0), 'head': (1, 1)},
    'atk2': {'root': (4, 0), 'fx': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'tail': (1, 0)},
    'ko': {'body': (0, 11), 'head': (2, 4), 'tail': (3, 3)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
