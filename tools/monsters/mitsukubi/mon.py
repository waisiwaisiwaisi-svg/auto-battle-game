# ミツクビ（ドラゴン・どく × ヒドラ）手打ち GBA風・デフォルメ（頭を 大きく、首を 短く、胴を 小さく 丸く、足を 短く）
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
EYE_BOX = (42, 20, 12, 28)
META = dict(id='mitsukubi', name='ミツクビ', types=['dragon', 'poison'], base='ヒドラ', size='L')
PAL = {
    'k': '#101018', 'l': '#3c0e24',
    'H': '#f2808a', 'I': '#b63a56', 'J': '#681a38',      # うろこ（明・中・暗）
    'B': '#f4dea2', 'C': '#c29a5c',                      # 腹（明・暗）
    'V': '#e8ff5c', 'U': '#8ed028', 'T': '#3e7a24',      # 毒（明・中・暗）
    'P': '#a874e6', 'Q': '#5c2c8e',                      # 背の とげ
    'w': '#ffffff',
    'Y': '#ffe04a', 'O': '#c8780e', 'R': '#ff5a2a',      # 首ごとの 目（黄・こがね・赤）
}
LIGHT = set('HBVPw')
KEEP_BLACK = set('wVUYOR')

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
    W, H = 34, 19; g = grid(W, H)
    ellipse(g, 18, 9.5, 15.5, 8.8, '#')
    poly(g, [(5, 5), (0, 13), (3, 14), (8, 12)], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'I'
            if dn <= 4: c = 'J'
            if dn == 5 and (x + y) % 2: c = 'J'
            if up <= 2 or lf <= 2: c = 'H'
            if dn <= 3 and 9 < x < 30: c = 'B' if dn >= 2 else 'C'
            out[y][x] = c
    # うろこの 列（ずらした 弧）
    for y in range(4, 12, 3):
        for x in range(6 + (y % 2) * 2, 30, 4):
            if out[y][x] == 'I': out[y][x] = 'J'; out[y][x + 1] = 'J'
            if out[y - 1][x] == 'I': out[y - 1][x] = 'H'
    # 腹の 段
    for x in range(11, 30, 3):
        for y in range(H):
            if out[y][x] == 'B': out[y][x] = 'C'
    return outline(rows_of(out))

# 頭（デフォルメで 大きく 17x11 → 20x14）：後ろに 2本の とげ、太い まゆの つり目、上あごの 牙
HEAD = [
    '..kk................',
    '.kHHk...kk..........',
    '.kHIkk.kHk..........',
    '..kHIIkkIkkkkk......',
    '..kHIIIIIIIIIIkkk...',
    '.kHHIIIIIIIIIIIIIkk.',
    'kHHkkkkkIIIIIIIIIIk.',
    'kHIk....kkkIIIIIIIHk',
    'kIIIk......kIIIIIIIk',
    'kIIIIkkkkkkkIIIIIIIk',
    'kJIIIIIIIIIIkkkkkkkk',
    'kJJIIIIIIIIkkwkkwkk.',
    '.kJJJJJJJJJkBBBBBk..',
    '..kkkkkkkkkkkkkkk...',
]
HEAD_OPEN = HEAD[:9] + [
    'kIIIIkkkkkkkIIIIkkkk',
    'kJIIIIIIIIIIkwkwkk..',
    'kJJIIIIIIIIkUUUUUk..',
    'kJJJIIIIIIkUUTTUUk..',
    '.kJJJJJJJJkwBBwBk...',
    '..kkkkkkkkkkkkkk....',
]
# A 爬虫類の つり目：白目なし。上は 明るい 虹彩、下は 暗い 虹彩、まん中を 2段の 細い たての スリット。上まぶたは 太い まゆ、
# 下は 細い 線。首ごとに 虹彩の 色を 変える（上の 首＝緑 V/U、まん中＝黄 Y/O、下の 首＝赤 R/J）
EYE = ['VVkV', 'kUkVUUk']
EYE_ALT = {'blink': ['IIII', 'kkkkkkk'], 'hit': ['kkVk', 'kVkkVkk'], 'atk0|atk1|atk2': ['wVkV', 'kVkwVVk'], 'ko': ['kIkI', 'IkIkIkI']}
def eye_of(col, dark=False):
    m = {'g': {}, 'y': {'V': 'Y', 'U': 'O'}, 'r': {'V': 'R', 'U': 'J'}}[col]
    if dark: m = dict(m, I='J')
    f = lambda rows: [''.join(m.get(c, c) for c in r) for r in rows]
    return f(EYE), {k: f(v) for k, v in EYE_ALT.items()}
DKH = {'H': 'I', 'I': 'J', 'J': 'l'}
def dk(rows): return [''.join(DKH.get(c, c) for c in r) for r in rows]
SPINE = ['.kk', 'kPk', 'kPQk', 'kQQk']
LEG = [
    '.kkkkkkk.', 'kHIIIIIJk', 'kHIIIIJJk', 'kHIIIIJJk', 'kIIIIIJJJk', 'kJJJJJJJJk', 'kwkwkwkkk.',
]
DRIP = ['kVk', 'kUk', '.k.']
GLOB = ['.kkk.', 'kVVUk', 'kVUUk', '.kkk.']
SPLAT = ['..kk..kk..', '.kVUkkVUk.', 'kVUUUUUTk.', '.kUUTTTk..', 'kVk.kk.kUk', '.k......k.']

P1 = [(27, 43), (29, 36), (32, 29), (36, 24), (41, 21)]
P2 = [(30, 44), (34, 39), (39, 35), (45, 33)]
P3 = [(30, 48), (36, 48), (42, 46)]
BODY = body()

def layers():
    return [
        dict(n='legFF', g='legB', x=29, y=53, rows=dk(LEG)),
        dict(n='legHF', g='legA', x=11, y=53, rows=dk(LEG)),
        *[dict(n='sp%d' % i, g='body', x=x, y=y, rows=SPINE) for i, (x, y) in enumerate(((9, 36), (14, 34), (19, 34), (24, 35)))],
        neck_layer('neck1', 'n1', P1, True, {'atk0': (-4, 0), 'atk1|atk2': (3, 1), 'hit': (-3, -1)}),
        dict(n='head1', g='h1', x=38, y=13, rows=dk(HEAD), alt={'atk1|atk2': dk(HEAD_OPEN)}),
        dict(n='eye1', g='h1', x=42, y=20, rows=eye_of('g', True)[0], alt=eye_of('g', True)[1]),
        dict(n='body', g='body', x=4, y=37, rows=BODY),
        dict(n='legH', g='legB', x=6, y=54, rows=LEG),
        neck_layer('neck3', 'n3', P3, False, {'atk0': (-3, 0), 'atk1|atk2': (3, 0), 'hit': (-2, -1)}),
        dict(n='head3', g='h3', x=40, y=39, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye3', g='h3', x=44, y=46, rows=eye_of('r')[0], alt=eye_of('r')[1]),
        neck_layer('neck2', 'n2', P2, False, {'atk0': (-4, 0), 'atk1|atk2': (3, 0), 'hit': (-3, -2)}),
        dict(n='head2', g='h2', x=43, y=26, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye2', g='h2', x=47, y=33, rows=eye_of('y')[0], alt=eye_of('y')[1]),
        dict(n='legF', g='legA', x=24, y=54, rows=LEG),
        dict(n='drip2', g='h2', x=57, y=38, rows=DRIP, only='idle1|idle2|walk1'),
        dict(n='drip3', g='h3', x=54, y=51, rows=DRIP, only='idle2|idle3|walk3'),
        dict(n='glob1', g='fx', x=61, y=22, rows=GLOB, only='atk1'),
        dict(n='glob2', g='fx', x=66, y=35, rows=GLOB, only='atk1'),
        dict(n='glob3', g='fx', x=63, y=48, rows=GLOB, only='atk1'),
        dict(n='splat', g='fx', x=64, y=32, rows=SPLAT, only='atk2'),
        dict(n='splat2', g='fx', x=62, y=45, rows=SPLAT, only='atk2'),
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
