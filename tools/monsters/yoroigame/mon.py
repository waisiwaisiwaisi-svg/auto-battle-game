# ヨロイガメ（いわ・みず × リクガメ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='yoroigame', name='ヨロイガメ', types=['rock', 'water'], base='リクガメ', size='L')
PAL = {
    'k': '#101018', 'l': '#22223c',
    'S': '#d8d2c6', 'T': '#9a929a', 'U': '#5c5664',      # 城壁の 石（明・中・暗）
    'A': '#94d6a2', 'B': '#409a78', 'C': '#22584e',      # 皮（明・中・暗）
    'W': '#e4f8ff', 'X': '#5cb6f2', 'Z': '#2a5cb6',      # 水（明・中・暗）
    'Y': '#ffd23a', 'M': '#9cc24a', 'w': '#ffffff',
}
LIGHT = set('SAWYMw')
KEEP_BLACK = set('wYXW')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, Lc, Mc, Dc, lt=2, dk=4):
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = Mc
            if dn <= dk or rt <= 3: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if up <= 1 and rt <= 2: c = Mc
            out[y][x] = c
    return out

# ---- 城壁の 甲羅：ドーム＋ 胸壁（凸凹）→ 石積みの 目地 → 矢狭間（光る 水）・苔・砲門を 手で ----
def shell(glow=False):
    W, H = 50, 44; g = grid(W, H)
    poly(g, [(1, 41), (0, 34), (3, 22), (6, 14), (38, 14), (41, 22), (44, 34), (43, 41)], '#')
    for x0 in range(5, 39, 6):                      # 胸壁（凸）
        for y in range(9, 14):
            for x in range(x0, x0 + 4): g[y][x] = '#'
    for y in range(4, 14):                          # まん中の 塔
        for x in range(15, 29): g[y][x] = '#'
    for x0 in (15, 20, 25):
        for y in range(0, 4):
            for x in range(x0, x0 + 4): g[y][x] = '#'
    out = shade(g, 'S', 'T', 'U', lt=1, dk=3)
    # 石積み：横の 目地 4行ごと、たての 目地は 段ごとに ずらす
    for y in range(4, 37):
        for x in range(W):
            if out[y][x] == '.': continue
            row = y // 4; yy = y % 4
            if yy == 3: out[y][x] = 'l'
            elif (x + (row % 2) * 3) % 6 == 0: out[y][x] = 'l'
            elif yy == 0 and out[y][x] == 'T' and x < 30: out[y][x] = 'S'
    # 塔と 壁の さかい（塔の 右の 影）
    for y in range(4, 15):
        if out[y][29] != '.': out[y][29] = 'l'
        if out[y][28] != '.': out[y][28] = 'U'
    # ふちの 板（甲羅の 縁の うろこ）
    for y in range(37, 42):
        for x in range(W):
            if out[y][x] == '.': continue
            k = x % 5
            out[y][x] = 'l' if k == 0 or y == 37 else ('T' if y == 38 and k < 3 else 'U' if y >= 40 else 'T' if k < 2 else 'U')
    # 矢狭間（たての すき間から 水の 光）
    c1, c2 = ('W', 'X') if glow else ('X', 'Z')
    for (x, y) in ((21, 5), (9, 17), (20, 17), (31, 17), (14, 25), (25, 25), (35, 25), (5, 29)):
        out[y][x] = 'k'; out[y + 1][x] = c1; out[y + 2][x] = c2
    # 苔
    for (x, y) in ((5, 14), (6, 14), (7, 15), (12, 15), (15, 4), (16, 4), (3, 23), (2, 24), (2, 25), (9, 37), (10, 37), (24, 37)):
        if out[y][x] != '.': out[y][x] = 'M'
    # 前の 砲門（まるい 穴）
    for (x, y, ch) in ((36, 18, 'k'), (37, 18, 'k'), (35, 19, 'k'), (38, 19, 'k'), (35, 20, 'k'), (38, 20, 'k'), (36, 21, 'k'), (37, 21, 'k'),
                       (36, 19, c2), (37, 19, c1), (36, 20, c2), (37, 20, c2), (34, 19, 'S'), (34, 20, 'S'), (39, 19, 'U'), (39, 20, 'U'), (35, 18, 'S'), (38, 21, 'U')):
        out[y][x] = ch
    return outline(rows_of(out))

HEAD = [
    '....kkkkkkkkk..........',
    '..kkAAAAAAAAAkkk.......',
    '.kAABBBBBBBBBBBBkk.....',
    'kAABBBBBkkkkkkBBBBkk...',
    'kABBBBBBBCCCCCkkkBBBk..',
    'kABBBBBBBBBBBBBBBkBBSk.',
    'kBBBBBBBBBBBBBBBBBBSSk.',
    'kBBBBBBBBBBBBBBBBBSSTTk',
    'kCBBBBBBBBBBBBBBBSTTTUk',
    'kCBBBBBBBkkkkkkkkkTTUUk',
    'kCCBBBBBkTTTTTTTkkkTUk.',
    '.kCCBBBBBkkkkkkkk..kk..',
    '..kCCCCBBBBBBBBCk......',
    '...kkCCCCCCCCCkk.......',
    '.....kkkkkkkkk.........',
]
HEAD_OPEN = HEAD[:9] + [
    'kCBBBBBBBkkkkkkkkkTTUUk',
    'kCCBBBBBkZZZZZZZkkkTUk.',
    '.kCCBBBkZZZZZZZk..kk...',
    '..kCCBBkkTTTTTk........',
    '...kkCCCCkkkkk.........',
    '.....kkkkkk............',
]
EYE = ['kYYYk', '.kYk']
EYE_ALT = {'blink': ['kkkkk', '.BBB'], 'hit': ['kBkBk', '.kBk'], 'atk0|atk1|atk2': ['kwYYk', '.kYk'], 'ko': ['kBkBk', '.BkB']}
NECK = [
    '..kkkkkkk..',
    '.kAABBBBCk.',
    'kAABBlBBBCk',
    'kABBBBlBBCk',
    'kABBBBBlBCk',
    'kBBBBBlBBCk',
    'kBBBBlBBCCk',
    'kCBBBBBCCk.',
    '.kCCCCCCk..',
    '..kkkkkk...',
]
LEG = [
    '.kkkkkkk..', 'kAABBBBCk.', 'kABBBBBBCk', 'kAlllBBBCk', 'kABBBlllCk', 'kBBBBBBBCk',
    'kBlllBBCCk', 'kCBBBlllCk', 'kCCCCCCCCk', 'kwkwkwkkk.',
]
TAIL = ['....kkk', '..kkABk', 'kkABBCk', 'kBBCCk.', '.kkkk..']
# 甲羅の うしろの 滝（樋口から 流れ落ちる）
def fall(phase):
    rows = ['kkkkk', 'kSTUk', 'kXWXk']
    for y in range(18):
        r = ''
        for x in range(3):
            v = (y + phase + x * 2) % 4
            r += 'W' if v == 0 else 'X' if v < 3 else 'Z'
        rows.append('k' + r + 'k')
    rows += ['kWXWXk', 'WXWWXWk', 'kkkkkkk']
    return rows
FALL = [fall(0), fall(1), fall(2), fall(3)]
DARK = {'A': 'B', 'B': 'C', 'C': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 砲門からの 水の 大砲
def jet(n, splash=False):
    rows = ['.' + 'k' * n, 'k' + 'X' * n, 'W' * (n + 1), 'w' * (n + 1), 'W' * (n + 1), 'k' + 'X' * n, '.' + 'Z' * (n - 1) + 'k', '.' + 'k' * n]
    rows[1] = 'k' + ''.join('W' if i % 5 == 0 else 'X' for i in range(n))
    if splash:
        S = ['..k.kk..', '.kWkWXk.', 'kWXWWXk.', 'XWwWXWXk', 'WwwWXXk.', 'XWWXWXk.', 'kXZXWk..', '.kkZkk..']
        rows = [r + s for r, s in zip(rows, S)]
    return rows
SHELL = shell(); SHELL_G = shell(True)

def layers():
    return [
        dict(n='legFF', g='legB', x=40, y=47, rows=dark(LEG)),
        dict(n='legHF', g='legA', x=16, y=47, rows=dark(LEG)),
        dict(n='tail', g='body', x=1, y=44, rows=TAIL),
        dict(n='fall', g='body', x=0, y=34, rows=FALL[0], alt={'idle1|walk1': FALL[1], 'idle2|walk2|atk0': FALL[2], 'idle3|walk3|atk1': FALL[3]}, not_='ko'),
        dict(n='neck', g='neck', x=37, y=37, rows=NECK),
        dict(n='shell', g='body', x=2, y=6, rows=SHELL, alt={'idle1|idle2|atk0|atk1|atk2': SHELL_G}),
        dict(n='legH', g='legA', x=8, y=48, rows=LEG),
        dict(n='legF', g='legB', x=33, y=48, rows=LEG),
        dict(n='head', g='head', x=41, y=31, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=50, y=35, rows=EYE, alt=EYE_ALT),
        dict(n='jet1', g='fx', x=42, y=22, rows=jet(16), only='atk1'),
        dict(n='jet2', g='fx', x=42, y=22, rows=jet(20, True), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 0), 'head': (0, 1)},
    'idle2': {'body': (0, 1), 'neck': (0, 0), 'head': (0, 1)},
    'idle3': {'body': (0, 1), 'neck': (0, 0), 'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (0, 2), 'neck': (-3, 1), 'head': (-2, 1)},
    'atk1': {'root': (-2, 0), 'body': (0, 1), 'neck': (-3, 1), 'head': (-1, 0)},
    'atk2': {'root': (-3, 0), 'body': (0, 1), 'neck': (-3, 1), 'head': (-1, 0)},
    'hit': {'root': (-3, 0), 'neck': (-2, -1), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'neck': 'body', 'head': 'neck', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'body'}
