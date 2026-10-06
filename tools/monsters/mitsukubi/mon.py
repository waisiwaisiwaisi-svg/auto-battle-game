# ミツクビ（ドラゴン・どく × ヒドラ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='mitsukubi', name='ミツクビ', types=['dragon', 'poison'], base='ヒドラ', size='L')
PAL = {
    'k': '#101018', 'l': '#3c0e24',
    'H': '#f2808a', 'I': '#b63a56', 'J': '#681a38',      # うろこ（明・中・暗）
    'B': '#f4dea2', 'C': '#c29a5c',                      # 腹（明・暗）
    'V': '#e8ff5c', 'U': '#8ed028', 'T': '#3e7a24',      # 毒（明・中・暗）
    'P': '#a874e6', 'Q': '#5c2c8e',                      # 背の とげ
    'w': '#ffffff',
}
LIGHT = set('HBVPw')
KEEP_BLACK = set('wVU')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 首：あたりは 円を つなぐ → 陰影（左上＝明、前＝腹の 色）→ 腹の 段を 手の ルールで ----
def neck(pts, r=3.2, dark=False):
    W, H = 64, 64; g = grid(W, H)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) * 2))
        for i in range(n + 1):
            ellipse(g, x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, r, r, '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'I'
            if lf <= 2 or up <= 1: c = 'H'
            if rt <= 2: c = 'B' if y % 3 else 'C'
            elif rt == 3 or dn <= 1: c = 'J'
            out[y][x] = c
    if dark: out = [[{'H': 'I', 'I': 'J', 'J': 'l', 'B': 'C'}.get(c, c) for c in r] for r in out]
    return outline(rows_of(out))
def bend(pts, dx, dy):
    # 頭に 近い 点ほど 大きく 動かす（首が しなる）
    n = len(pts) - 1
    return [(x + dx * i / n, y + dy * i / n) for i, (x, y) in enumerate(pts)]
POSE = {'atk0': (-4, 0), 'atk1|atk2': (3, 0), 'hit': (-3, -2)}
def neck_layer(name, g, pts, dark=False, poses=POSE, extra=None):
    alt = {k: neck(bend(pts, *v), dark=dark) for k, v in poses.items()}
    if extra:
        for k, v in extra.items(): alt[k] = neck(bend(pts, *v), dark=dark)
    return dict(n=name, g=g, x=-1, y=-1, rows=neck(pts, dark=dark), alt=alt)

# ---- 胴 ----
def body():
    W, H = 40, 22; g = grid(W, H)
    ellipse(g, 21, 11, 18.5, 10, '#')
    poly(g, [(5, 6), (0, 16), (3, 17), (8, 15)], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'I'
            if dn <= 4: c = 'J'
            if dn == 5 and (x + y) % 2: c = 'J'
            if up <= 2 or lf <= 2: c = 'H'
            if dn <= 3 and 10 < x < 36: c = 'B' if dn >= 2 else 'C'
            out[y][x] = c
    # うろこの 列（ずらした 弧）
    for y in range(4, 14, 3):
        for x in range(6 + (y % 2) * 2, 36, 4):
            if out[y][x] == 'I': out[y][x] = 'J'; out[y][x + 1] = 'J'
            if out[y - 1][x] == 'I': out[y - 1][x] = 'H'
    # 腹の 段
    for x in range(12, 36, 3):
        for y in range(H):
            if out[y][x] == 'B': out[y][x] = 'C'
    return outline(rows_of(out))

HEAD = [
    '...kk............',
    '..kHHkkkkk.......',
    '.kHHHIIIIIkkk....',
    'kHHIIIIkkkIIIkk..',
    'kHIIIIIIIIkkIIIkk',
    'kIIIIIIIIIIIIIIHk',
    'kIIIIIIIIIIIIkkkk',
    'kJIIIIIIkkkkkkk..',
    'kJJIIIIkwJJwJwk..',
    '.kJJJJJJJJJJJk...',
    '..kkkkkkkkkkk....',
]
HEAD_OPEN = [
    '...kk............',
    '..kHHkkkkk.......',
    '.kHHHIIIIIkkk....',
    'kHHIIIIkkkIIIkk..',
    'kHIIIIIIIIkkIIIkk',
    'kIIIIIIIIIIIIIIHk',
    'kIIIIIIIIIkwkwkkk',
    'kJIIIIIIkUUUUUk..',
    'kJJIIIIkUUUUk....',
    'kJJJIIIIkwUUwk...',
    '.kJJJJJJJkkkkk...',
    '..kkkkkkkk.......',
]
EYE = ['kVVk', '.kV']
EYE_ALT = {'blink': ['kkkk', '.II'], 'hit': ['kIkI', '.kI'], 'atk0|atk1|atk2': ['kwVk', '.kV'], 'ko': ['kIkI', '.IkI']}
DKH = {'H': 'I', 'I': 'J', 'J': 'l'}
def dk(rows): return [''.join(DKH.get(c, c) for c in r) for r in rows]
SPINE = ['.kk', 'kPk', 'kPQk', 'kQQk']
LEG = [
    '.kkkkkkk.', 'kHIIIIIJk', 'kHIIIIJJk', '.kHIIIJJk', '.kIIIIJJk', '.kIIIJJk.',
    'kHIIIIJJk', 'kIIIIIJJJk', 'kJJJJJJJJk', 'kwkwkwkkk.',
]
DRIP = ['kVk', 'kUk', '.k.']
GLOB = ['.kkk.', 'kVVUk', 'kVUUk', '.kkk.']
SPLAT = ['..kk..kk..', '.kVUkkVUk.', 'kVUUUUUTk.', '.kUUTTTk..', 'kVk.kk.kUk', '.k......k.']

P1 = [(26, 41), (29, 33), (30, 26), (33, 19), (37, 14), (41, 11)]
P2 = [(31, 41), (35, 35), (38, 30), (42, 26), (48, 23)]
P3 = [(30, 45), (35, 45), (39, 42), (44, 40)]
BODY = body()

def layers():
    return [
        dict(n='legFF', g='legB', x=34, y=50, rows=dk(LEG)),
        dict(n='legHF', g='legA', x=12, y=50, rows=dk(LEG)),
        *[dict(n='sp%d' % i, g='body', x=x, y=y, rows=SPINE) for i, (x, y) in enumerate(((8, 32), (13, 30), (18, 29), (23, 29)))],
        neck_layer('neck1', 'n1', P1, True, {'atk0': (-4, 0), 'atk1|atk2': (3, 1), 'hit': (-3, -1)}),
        dict(n='head1', g='h1', x=40, y=4, rows=dk(HEAD), alt={'atk1|atk2': dk(HEAD_OPEN)}),
        dict(n='eye1', g='h1', x=47, y=7, rows=EYE, alt=EYE_ALT),
        dict(n='body', g='body', x=1, y=32, rows=BODY),
        dict(n='legH', g='legB', x=6, y=51, rows=LEG),
        neck_layer('neck3', 'n3', P3, False, {'atk0': (-3, 0), 'atk1|atk2': (3, 0), 'hit': (-2, -1)}),
        dict(n='head3', g='h3', x=42, y=34, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye3', g='h3', x=49, y=37, rows=EYE, alt=EYE_ALT),
        neck_layer('neck2', 'n2', P2, False, {'atk0': (-4, 0), 'atk1|atk2': (3, 0), 'hit': (-3, -2)}),
        dict(n='head2', g='h2', x=46, y=16, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye2', g='h2', x=53, y=19, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='legA', x=28, y=51, rows=LEG),
        dict(n='drip2', g='h2', x=56, y=24, rows=DRIP, only='idle1|idle2|walk1'),
        dict(n='drip3', g='h3', x=52, y=43, rows=DRIP, only='idle2|idle3|walk3'),
        dict(n='glob1', g='fx', x=58, y=8, rows=GLOB, only='atk1'),
        dict(n='glob2', g='fx', x=63, y=21, rows=GLOB, only='atk1'),
        dict(n='glob3', g='fx', x=60, y=38, rows=GLOB, only='atk1'),
        dict(n='splat', g='fx', x=62, y=18, rows=SPLAT, only='atk2'),
        dict(n='splat2', g='fx', x=60, y=36, rows=SPLAT, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'h1': (0, -1), 'h2': (0, 1), 'h3': (0, 0)},
    'idle2': {'body': (0, 1), 'h1': (-1, 0), 'h2': (0, 1), 'h3': (0, 1)},
    'idle3': {'body': (0, 0), 'h1': (0, 0), 'h2': (0, 0), 'h3': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1), 'h1': (0, -1)},
    'walk1': {'body': (0, -1), 'h2': (0, 1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1), 'h3': (0, -1)},
    'walk3': {'body': (0, -1), 'h1': (0, 1)},
    'atk0': {'body': (-1, 1), 'h1': (-4, 0), 'h2': (-4, 0), 'h3': (-3, 0)},
    'atk1': {'root': (2, 0), 'h1': (3, 1), 'h2': (3, 0), 'h3': (3, 0)},
    'atk2': {'root': (2, 0), 'h1': (3, 1), 'h2': (3, 0), 'h3': (3, 0)},
    'hit': {'root': (-3, 0), 'h1': (-3, -1), 'h2': (-3, -2), 'h3': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'n1': 'body', 'n2': 'body', 'n3': 'body', 'h1': 'body', 'h2': 'body', 'h3': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
