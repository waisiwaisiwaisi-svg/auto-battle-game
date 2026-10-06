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

# ---- 胴（デフォルメ：小さく 丸い すわった もも＋ 立てた 胸）。陰影の あと、石の われ目と 念の 紋様を 手で ----
def body(glow=False):
    W, H = 34, 26; g = grid(W, H)
    ellipse(g, 11, 15, 10.5, 10.5, '#')
    poly(g, [(2, 16), (8, 8), (18, 6), (25, 0), (32, 2), (33, 20), (28, 25), (18, 26), (6, 26)], '#')
    out = shade(g, lt=2, dk=4)
    import math
    for t in range(-70, 75, 5):
        a = math.radians(t); x = round(11 + 10 * math.cos(a)); y = round(15 + 10 * math.sin(a))
        if 0 <= y < H and 0 <= x < W and out[y][x] in 'STU':
            out[y][x] = 'l'
            if x + 1 < W and out[y][x + 1] in 'TU': out[y][x + 1] = 'S' if t < 0 else 'T'
    # 石の われ目
    for pts in (((18, 7), (19, 8), (19, 9)), ((3, 20), (4, 21)), ((29, 17), (30, 18))):
        for (x, y) in pts: out[y][x] = 'l'
    # 胸の 筋肉の みぞ
    for (x, y) in ((26, 4), (25, 5), (24, 6), (24, 7), (24, 8), (25, 9), (26, 10)):
        out[y][x] = 'l'; out[y][x + 1] = 'S' if out[y][x + 1] == 'T' else out[y][x + 1]
    # もも の うず巻き（念力で 光る みぞ）
    c1, c2 = ('P', 'Q') if glow else ('Q', 'R')
    rune = [(9, 12), (10, 12), (11, 12), (12, 12), (13, 13), (14, 14), (14, 15), (14, 16), (13, 17), (12, 18), (11, 18), (10, 18),
            (9, 17), (8, 16), (8, 15), (9, 14), (10, 14), (11, 14), (12, 15), (11, 16)]
    for i, (x, y) in enumerate(rune): out[y][x] = c1 if i % 3 == 0 else c2
    # 胸の 三本の 紋様
    for (x, y) in ((28, 6), (28, 7), (28, 8), (30, 5), (30, 6), (30, 7), (30, 8), (30, 9)):
        out[y][x] = c1 if y in (6, 7) else c2
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
    N = 27; c = (N - 1) / 2; g = grid(N, N)
    star = []
    for i in range(20):
        a = math.pi * 2 * i / 20 + .1; r = 13.4 if i % 2 == 0 else 10.6
        star.append((N / 2 + r * math.cos(a), N / 2 + r * math.sin(a)))
    poly(g, star, '#')
    out = shade(g, 'A', 'B', 'C', lt=2, dk=3)
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            if 7.4 <= d < 8.4: out[y][x] = 'l'
            elif 8.4 <= d < 9.2 and out[y][x] == 'B' and x + y < 2 * c: out[y][x] = 'A'
    for (x, y) in ((4, 13), (5, 8), (8, 5), (13, 4), (6, 18), (9, 21)):
        out[y][x] = ('P' if glow else 'Q'); out[y + 1][x] = 'R'
    return outline(rows_of(out))
DISC = disc(); DISC_G = disc(True)

HEAD = [
    '....kkkkkkkkk.....',
    '..kkSSSSSSSSTkk...',
    '.kSSSTTTTTTTTTTk..',
    'kSSTTTTTTTTTTTTTk.',
    'kSTTTTTTTTTTTTTTk.',
    'kSTTTkkkkkkkkTTTTk',
    'kSTTTTkUUUUUUkkkTk',
    'kSTTTTkTTTTTTkTTTk',
    'kSTTTlTkkkkkkTTSSk',
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
# 目：白い 光＋ 虹彩 2色（P/Q）＋ たての ひとみ。上は まゆの ひさし、下は まぶたの 線
EYE = ['wPPkQ', 'QQRkR']
EYE_ALT = {'blink': ['kkkkk', 'TTTTT'], 'hit': ['kQTQk', 'TkQkT'], 'atk0|atk1|atk2': ['wwPkP', 'PQQkQ'],
           'ko': ['TkTkT', 'TTkTT', 'TkTkT']}
# 額の 第三の 目（たて長）
EYE3 = ['.kkk.', 'kwPQk', 'kPkQk', 'kQkRk', '.kkk.']
EYE3_ALT = {'blink|hit|ko': ['.....', '..k..', '.kTk.', '..k..', '.....'], 'atk0|atk1|atk2': ['.kkk.', 'kwwPk', 'kPkPk', 'kPkQk', '.kkk.'],
            'idle1|idle2': ['.kkk.', 'kwwQk', 'kPkQk', 'kQkRk', '.kkk.']}
# 前足（短く 太く、上は 胴に 食いこむ ので 上の 輪郭なし）
LEG_F = [
    'kSTTTUk', 'kSTTTUk', 'kSTTTUk', 'kSTTTUk', 'kSTTTUk', 'kSTTlUk', 'kSTTTUk', 'kSTTTUUk', 'kSTTTTUUk', 'kUUUUUUUk', 'kwkwkwkk.',
]
PAW_H = ['..kkkkk...', '.kSTTTUkk.', 'kSTTTTTUUk', 'kUUUUUUUUk', '.kwkwkkkk.']
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
HX, HY = 40, 13
def layers():
    return [
        dict(n='wingF', g='wing', x=18, y=3, rows=dark(wing()), alt={'atk0|atk1|atk2': dark(wing(2))}),
        dict(n='legFF', g='legB', x=42, y=49, rows=dark(LEG_F)),
        dict(n='tail', g='tail', x=1, y=41, rows=TAIL),
        dict(n='wing', g='wing', x=9, y=7, rows=wing(), alt={'atk0|atk1|atk2': wing(2)}),
        dict(n='body', g='body', x=6, y=28, rows=BODY, alt={'idle1|idle2|atk0|atk1|atk2': BODY_G}),
        dict(n='pawH', g='legA', x=13, y=55, rows=PAW_H),
        dict(n='legF', g='legA', x=35, y=49, rows=LEG_F),
        dict(n='disc', g='head', x=HX - 13, y=HY - 6, rows=DISC, alt={'idle1|idle2|atk0|atk1|atk2': DISC_G}),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD, alt={'atk1|atk2': HEAD_ROAR}),
        dict(n='eye', g='head', x=HX + 7, y=HY + 6, rows=EYE, alt=EYE_ALT),
        dict(n='eye3', g='head', x=HX + 7, y=HY + 1, rows=EYE3, alt=EYE3_ALT),
        dict(n='beam1', g='fx', x=HX + 13, y=HY - 1, rows=beam(8), only='atk1'),
        dict(n='beam2', g='fx', x=HX + 13, y=HY - 1, rows=beam(10, True), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'wing': (0, 0)},
    'idle3': {'body': (0, 1), 'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, -1), 'wing': (0, -2), 'tail': (0, -1)},
    'atk1': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -2)},
    'atk2': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, 2), 'wing': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'head'}
