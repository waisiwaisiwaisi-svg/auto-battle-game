# ナゾジシ（エスパー・いわ × スフィンクス）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='nazojishi', name='ナゾジシ', types=['psychic', 'rock'], base='スフィンクス', size='L')
PAL = {
    'k': '#101018', 'l': '#40283c',
    'S': '#efdcaa', 'T': '#b89a6a', 'U': '#76603e',      # 砂岩（明・中・暗）
    'A': '#7ad6cc', 'B': '#2c8a96', 'C': '#1c4660',      # 頭かざりの 青石（明・中・暗）
    'P': '#ffc8ff', 'Q': '#ee4ad2', 'R': '#8a2498',      # 念力の 光（明・中・暗）
    'w': '#ffffff',
}
LIGHT = set('SAPw')
KEEP_BLACK = set('wPQ')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, Lc='S', Mc='T', Dc='U', lt=2, dk=4):
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = Mc
            if dn <= dk or rt <= 2: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if up <= 1 and rt <= 2: c = Mc
            out[y][x] = c
    return out

# ---- 胴：すわった もも＋ 立てた 胸（守り獣の かまえ）。陰影の あと、石の われ目と 念の 紋様を 手で ----
def body(glow=False):
    W, H = 50, 44; g = grid(W, H)
    ellipse(g, 14, 31, 12.5, 12, '#')
    poly(g, [(4, 32), (12, 20), (24, 16), (32, 6), (40, 2), (47, 6), (48, 30), (42, 36), (30, 43), (10, 43)], '#')
    out = shade(g, lt=3, dk=5)
    for y in range(H):
        for x in range(W):
            if out[y][x] == 'T' and run(g, x, y, 0, 1) == 6 and (x + y) % 2: out[y][x] = 'U'
            if out[y][x] == 'T' and (run(g, x, y, 0, -1) == 4 or run(g, x, y, -1, 0) == 4) and (x + y) % 2: out[y][x] = 'S'
    # もも の ふち（弧）：前側に 濃い 線、その 外に 光
    import math
    for t in range(-70, 75, 4):
        a = math.radians(t); x = round(14 + 12 * math.cos(a)); y = round(31 + 12 * math.sin(a))
        if 0 <= y < H and out[y][x] in 'STU':
            out[y][x] = 'l'
            if x + 1 < W and out[y][x + 1] in 'TU': out[y][x + 1] = 'S' if t < 0 else 'T'
    # 石の われ目（ブロックの 継ぎ目）
    for pts in (((24, 17), (25, 18), (25, 19), (26, 20)), ((38, 14), (38, 15), (39, 16), (39, 17), (39, 18)),
                ((4, 36), (5, 37), (6, 37)), ((44, 26), (45, 27), (45, 28)), ((30, 30), (31, 31), (31, 32))):
        for (x, y) in pts: out[y][x] = 'l'
    # 胸と もものの 筋肉の みぞ
    for (x, y) in ((33, 10), (32, 11), (31, 12), (31, 13), (31, 14), (32, 15), (33, 16), (34, 17)):
        out[y][x] = 'l'; out[y][x + 1] = 'S' if out[y][x + 1] == 'T' else out[y][x + 1]
    # もも に うず巻きの 紋様（念力で 光る みぞ）
    c1, c2 = ('P', 'Q') if glow else ('Q', 'R')
    cx, cy = 9, 13
    rune = [(12, 26), (13, 26), (14, 26), (15, 26), (16, 26), (17, 27), (18, 28), (18, 29), (18, 30), (18, 31), (17, 32), (16, 33), (15, 33),
            (14, 33), (13, 33), (12, 32), (11, 31), (11, 30), (12, 29), (13, 29), (14, 29), (15, 30), (14, 31)]
    for i, (x, y) in enumerate(rune): out[y][x] = c1 if i % 3 == 0 else c2
    # 胸の 三本の 紋様
    for (x, y) in ((40, 9), (40, 10), (40, 11), (43, 8), (43, 9), (43, 10), (43, 11), (43, 12), (46, 9), (46, 10), (46, 11)):
        out[y][x] = c1 if y in (9, 10) else c2
    return outline(rows_of(out))

# ---- 石の 翼（たたんで 上へ）：板の 羽を 1枚ずつ ----
def wing(up=0):
    W, H = 24, 26; g = grid(W, H)
    poly(g, [(23, 25), (22, 16), (12, 4 - up), (5, 0 - up), (2, 4 - up), (3, 12), (9, 20), (14, 25)], '#')
    out = shade(g, lt=1, dk=3)
    for k in range(4):
        x0 = 4 + k * 4
        line(out, x0, 4 + k * 3, x0 + 7, 22, 'l')
    for y in range(H):
        for x in range(W):
            if out[y][x] in 'TU' and x > 0 and out[y][x - 1] == 'l': out[y][x] = 'S'
    return outline(rows_of(out))

# ---- 頭の 後ろの 石の 円盤（たてがみ）：青石に 念の 文字が 光る ----
def disc(glow=False):
    import math
    N = 33; c = (N - 1) / 2; g = grid(N, N)
    star = []
    for i in range(24):
        a = math.pi * 2 * i / 24 + .1; r = 16.2 if i % 2 == 0 else 12.6
        star.append((N / 2 + r * math.cos(a), N / 2 + r * math.sin(a)))
    poly(g, star, '#')
    out = shade(g, 'A', 'B', 'C', lt=2, dk=4)
    # 内側の みぞ（輪）と 放射の 刻み
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            if 8.6 <= d < 9.6: out[y][x] = 'l'
            elif 9.6 <= d < 10.4 and out[y][x] == 'B' and x + y < 2 * c: out[y][x] = 'A'
    dots = [(5, 16), (6, 10), (10, 6), (16, 5), (7, 22), (11, 25), (16, 27)]
    for i, (x, y) in enumerate(dots):
        out[y][x] = ('P' if glow else 'Q'); out[y + 1][x] = 'R'
    # ふちの とげ（光の 方向に 4本）
    return outline(rows_of(out))
DISC = disc(); DISC_G = disc(True)

HEAD = [
    '....kkkkkkkkk.....',
    '..kkSSSSSSSSTkk...',
    '.kSSSTTTTTTTTTTk..',
    'kSSTTTTTTTTTTTTTk.',
    'kSTTTTTTTTTTTTTTk.',
    'kSTTTTkkkkkkkTTTTk',
    'kSTTTTTUUUUUUkkkTk',
    'kSTTTTTTTTTTTTTTTk',
    'kSTTTlTTTTTTTTTSSk',
    'kTTTTTlTTTTTTTSSSUk',
    'kTTTTTTTTTTTTTTkkkk',
    'kTTTTTTTTTkkkkkkkk.',
    'kUTTTTTTkwUUUwUwk..',
    'kUUTTTTTTkkkkkkk...',
    '.kUUTTTTTTTTTUk....',
    '..kUUUUUUUUUUk.....',
    '...kkkkkkkkkk......',
]
HEAD_ROAR = HEAD[:11] + [
    'kTTTTTTTTkkkkkkkkk',
    'kUTTTTTTkwRRRRRwk.',
    'kUUTTTTkRRRRRRRk..',
    'kUUUTTTkwRRRwkk...',
    '.kUUUTTTkkkkTk....',
    '..kUUUUUUUUUUk....',
    '...kkkkkkkkkk.....',
]
EYE = ['kPPQk', '.kQQk']
EYE_ALT = {'blink': ['kkkkk', '.TTTT'], 'hit': ['kQkQk', '.kTkT'], 'atk0|atk1|atk2': ['kwwPk', '.kPPk'], 'ko': ['kTkTk', '.TkTk']}
EYE3 = ['.k.', 'kQk', 'kPk', 'kQk', '.k.']
EYE3_ALT = {'blink|hit|ko': ['...', '.k.', 'kTk', '.k.', '...'], 'atk0|atk1|atk2': ['kPk', 'PwP', 'PwP', 'PwP', 'kPk'],
            'idle1|idle2': ['.k.', 'kPk', 'kwk', 'kPk', '.k.']}
LEG_F = [
    'kkkkkkk.', 'kSSTTTUk', 'kSTTTTUk', 'kSTTTTUk', 'kSTTTTUk', 'kSTTTlUk', 'kSTTTTUk', 'kSTTTTUk',
    'kSTTTTUk', 'kSTTTlUk', 'kSTTTTUk', 'kSTTTTUUk', 'kSSTTTTUk', 'kSTTTTTUUk', 'kUUUUUUUUk', 'kwkwkwkkk.',
]
PAW_H = ['....kkkkk.....', '..kkSTTTUkk...', '.kSSTTTTTUUkk.', 'kSTTTTTTTTUUUk', 'kUUUUUUUUUUUUk', '.kwkwkwkkkkkk.']
TAIL = [
    '....kk...', '...kSk...', '..kSTUk..', '..kSUk...', '.kkTk....', 'kQQk.....', 'kPQk.....',
    'kQRk.....', '.kkSkk...', '..kSTTkk.', '...kUTTTk', '....kkUUk', '......kk.',
]
DARK = {'S': 'T', 'T': 'U', 'U': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 念力の 光線（第三の 目から）と 先の 輪
def beam(n, ring=False):
    core = ['k' * n, 'R' * n, 'Q' * n, 'P' * n, 'w' * n, 'P' * n, 'Q' * n, 'R' * n, 'k' * n]
    for j in (0, 8):
        core[j] = ''.join('k' if (i % 4) else '.' for i in range(n))
    if ring:
        R = ['...kkk..', '..kQRQk.', '.kQkkkQk', 'kQk...kQk', 'kQk...kQk', 'kQk...kQk', '.kQkkkQk', '..kQRQk.', '...kkk..']
        core = [c + r for c, r in zip(core, R)]
    return core
BODY = body(); BODY_G = body(True)

def layers():
    return [
        dict(n='wingF', g='wing', x=22, y=4, rows=dark(wing()), alt={'atk0|atk1|atk2': dark(wing(2))}),
        dict(n='legFF', g='legB', x=48, y=45, rows=dark(LEG_F)),
        dict(n='tail', g='tail', x=0, y=47, rows=TAIL),
        dict(n='wing', g='wing', x=12, y=8, rows=wing(), alt={'atk0|atk1|atk2': wing(2)}),
        dict(n='body', g='body', x=3, y=16, rows=BODY, alt={'idle1|idle2|atk0|atk1|atk2': BODY_G}),
        dict(n='pawH', g='legA', x=20, y=55, rows=PAW_H),
        dict(n='legF', g='legA', x=41, y=45, rows=LEG_F),
        dict(n='disc', g='head', x=28, y=-2, rows=DISC, alt={'idle1|idle2|atk0|atk1|atk2': DISC_G}),
        dict(n='head', g='head', x=44, y=8, rows=HEAD, alt={'atk1|atk2': HEAD_ROAR}),
        dict(n='eye', g='head', x=51, y=14, rows=EYE, alt=EYE_ALT),
        dict(n='eye3', g='head', x=53, y=9, rows=EYE3, alt=EYE3_ALT),
        dict(n='beam1', g='fx', x=57, y=8, rows=beam(8), only='atk1'),
        dict(n='beam2', g='fx', x=57, y=8, rows=beam(10, True), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 0), 'head': (0, 1), 'wing': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'wing': (0, 1)},
    'idle3': {'body': (0, 1), 'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, -1), 'wing': (0, -2), 'tail': (0, -1)},
    'atk1': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -2)},
    'atk2': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -1)},
    'hit': {'root': (-3, 0), 'head': (-3, 2), 'wing': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'head'}
