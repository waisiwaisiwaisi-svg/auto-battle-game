# マグマジロ（ほのお・じめん × アルマジロ）手打ち GBA風
META = dict(id='magmajiro', name='マグマジロ', types=['fire', 'ground'], base='アルマジロ', size='M')
PAL = {
    'k': '#101018', 'l': '#4a2230',
    'R': '#a898b4', 'Q': '#62527a', 'P': '#382c48',
    'Y': '#ffe066', 'O': '#ff7a22',
    'F': '#e8b47c', 'G': '#b8743e', 'H': '#6e3a24',
    'w': '#ffffff', 'n': '#f08aa0',
}
LIGHT = set('RFYw')

# ---- 甲羅（ドームの はばは 行ごとに 手で 指定、板の すき間＝溶岩の みぞ）----
def shell(hot=False):
    W, H = 36, 26
    L = [12, 9, 7, 5, 4, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 4]
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(L[y], W - L[y]):
            d_left = x - L[y]; d_right = W - 1 - L[y] - x
            # 光は 左上：上の 3行と 左の 2列は 明、右の 4列と 下は 影
            c = 'Q'
            if y <= 2 or d_left <= 1 or (y <= 5 and d_left <= 4): c = 'R'
            if d_right <= 3 or y >= 18 or (y >= 16 and d_right <= 8): c = 'P'
            if d_right <= 3 and y <= 3: c = 'Q'
            g[y][x] = c
    # 帯の みぞ（ドームに そって 外へ ふくらむ 弧）を 行ごとに 手で 指定
    A = [None, None, None, 13, 12, 12, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11]
    B = [None, None, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18]
    C = [None, None, None, 23, 24, 24, 25, 25, 25, 26, 26, 26, 26, 26, 26, 26, 25, 25, 25, 25]
    for xs in (A, B, C):
        for y, x in enumerate(xs):
            if x is None: continue
            mid = 5 <= y <= 15
            g[y][x] = 'Y' if (mid and (hot or 7 <= y <= 13)) else 'O'
            if mid: g[y][x - 1] = 'O'; g[y][x + 1] = 'O'
            else: g[y][x + 1] = 'l'
            # みぞの 両わきに 板の あつみ（左＝影の ふち、右＝光の ふち）
            if g[y][x - 2] in 'RQP' and mid: g[y][x - 2] = 'l'
            if x + 2 < W and g[y][x + 2] in 'QP' and mid: g[y][x + 2] = 'R'
    # 冷えた あわ（つぶつぶ）：手で 置く
    for (x, y) in ((5, 8), (6, 13), (15, 5), (15, 11), (21, 7), (21, 13), (29, 7), (30, 12), (4, 4), (28, 3), (14, 16), (22, 16)):
        if g[y][x] in 'QP': g[y][x] = 'R'
        if y + 1 < H and g[y + 1][x] in 'QR': g[y + 1][x] = 'P'
    # ふちの 小さな うろこ（4ドットずつ）
    for y in range(20, H):
        for x in range(L[y], W - L[y]):
            k = (x - L[y]) % 4
            if y == 20: g[y][x] = 'l'
            elif y == H - 1: g[y][x] = 'P'
            else: g[y][x] = 'l' if k == 3 else ('R' if y == 21 and k < 2 else 'Q' if y < 24 else 'P')
    return [''.join(r) for r in g]

HEAD = [
    '......kkkkkkk...........',
    '....kkRRRRRQQkk.........',
    '...kRRRRQQQQQQPkk.......',
    '..kRRQQQQQQQQQQPPkk.....',
    '.kRQQQQQQQQQQQQQPPPkk...',
    '.kQQQQQQQQQQQQQQQQPPPkk.',
    'kPQQQQQQQPPPPPPPPPPPPPPk',
    'kPPQQQPPkkkkkkkkkkkkkkk.',
    '.kPPPPkHHHk.....kHHHHk..',
    '.kHkkkHGGGHkkkkkHGGGGGk.',
    '.kHGOOGGGGGGGGGGGGGGGGkk',
    '.kHGGOOGGGGGGGGGGGGGGGHk',
    '.kHGGGGGGGGGGGkkkkkkkkk.',
    '.kHGGGGGkkkkkkwGwGGwGk..',
    '..kHGGGGGGGGGGGGGGGHk...',
    '..kHHHGGGGGGGGGHHHk.....',
    '...kkHHHHHHHHHHHkk......',
    '.....kkkkkkkkkkk........',
]
# するどい 目：つり上がった まゆ＋溶岩色の 虹彩＋たての ひとみ
EYE = ['YYYkO']
EYE_ALT = {'blink': ['kkkkk'], 'hit': ['kOkOk'], 'atk0|atk1|atk2': ['YYYYk'], 'ko': ['HkHkH']}
NHORN = ['...kk', '..kRk', '.kRQk', 'kRQPk', 'kRPPk']
SPIKE = ['k.....', 'kYk...', '.kOkk.', '.kRQPk', '.kRQPk', 'kRQQPk', 'kRQPPk']
# 耳の かわりに 後ろへ 反った 岩の つの（先が 溶岩）
EAR = ['kk......', 'kOkk....', '.kRQkk..', '.kRQQPk.', '..kRQQPk', '..kRQPPk', '...kRPk.', '....kk..']
LEG = ['.kkkkk', 'kFGGGHk', 'kFGGGHk', 'kGGGGHk', 'kGGGHHk', 'kGGGHHHk', 'kHHHHHHk', '.kwkwkk']
BELLY = [
    '.kHHHHHHHHHHHHHHHHHHHHHHHHHHk',
    'kHGGGGGGGGGGGGGGGGGGGGGGGGGGHk',
    'kHGGGGGGGGGGGGGGGGGGGGGGGGGGHk',
    '.kHHHHHHHHHHHHHHHHHHHHHHHHHHk',
]
TAIL = [
    '.............kk',
    '...........kkQPk',
    '..........kRQlQPk',
    '........kkRQlRQPk',
    '.......kRQlRQlQPk',
    '......kRQlRQlQPPk',
    '.....kRQlRQlQPPk',
    '....kRQlRQlQPPk',
    '...kRQlRQPPPkk',
    '...kQlRQPPkk',
    '..kQlQPPkk',
    '..kOYOkk',
    '.kOYYYOk',
    '.kOYYOk',
    '..kOOk',
    '...kk',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'P', 'R': 'Q', 'Q': 'P'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- まるまった ボール（攻撃）：円と 溶岩の みぞを 手で 指定 ----
def ball(hot=True, phase=0.0):
    N = 30; c = (N - 1) / 2; g = [['.'] * N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            if d > 14.2: continue
            nx, ny = (x - c) / 14, (y - c) / 14
            l = -nx * .6 - ny * .8
            g[y][x] = 'R' if l > .55 and d > 10 else 'P' if l < -.35 else 'Q'
            # 甲羅の 帯の みぞ：球の 経線（u = 一定）。真ん中ほど 黄色く 光る
            u = (x - c) / max(.5, (14.2 ** 2 - (y - c) ** 2) ** .5)
            for u0 in [v + phase for v in (-1.1, -.55, 0, .55, 1.1)]:
                if abs(u - u0) < .075 and d < 13.6:
                    g[y][x] = 'Y' if hot and abs(y - c) < 6 else 'O'
                elif abs(u - u0) < .16 and d < 13.6 and g[y][x] in 'QR' and u > u0:
                    g[y][x] = 'R' if l > -.2 else g[y][x]
    # 頭の かぶと（右下に 少し）とつぶつぶ
    for (x, y) in ((8, 8), (11, 5), (6, 13), (20, 6), (9, 19)):
        if g[y][x] in 'QP': g[y][x] = 'R'
    out = [r[:] for r in g]
    for y in range(N):
        for x in range(N):
            if g[y][x] != '.': continue
            if any(0 <= y + dy < N and 0 <= x + dx < N and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return [''.join(r) for r in out]
def rot90(rows):
    h, w = len(rows), max(len(r) for r in rows); rows = [r.ljust(w, '.') for r in rows]
    return [''.join(rows[h - 1 - y][x] for y in range(h)) for x in range(w)]

SHELL = shell(); SHELL_HOT = shell(True)
NOT_BALL = 'atk1|atk2'
def layers():
    def outline_shell(rows):
        H, W = len(rows), len(rows[0]); g = [list('.' + r + '.') for r in rows]; g = [['.'] * (W + 2)] + g + [['.'] * (W + 2)]
        out = [r[:] for r in g]
        for y in range(len(g)):
            for x in range(len(g[0])):
                if g[y][x] != '.': continue
                if any(0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]) and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
        return [''.join(r) for r in out]
    return [
        dict(n='legFF', g='legB', x=37, y=41, rows=dark(LEG), not_=NOT_BALL),
        dict(n='legFH', g='legA', x=21, y=41, rows=dark(LEG), not_=NOT_BALL),
        dict(n='tail', g='tail', x=0, y=31, rows=TAIL, not_=NOT_BALL),
        dict(n='belly', g='body', x=12, y=39, rows=BELLY, not_=NOT_BALL),
        dict(n='legH', g='legB', x=14, y=42, rows=LEG, not_=NOT_BALL),
        dict(n='legF', g='legA', x=40, y=42, rows=LEG, not_=NOT_BALL),
        dict(n='shell', g='body', x=8, y=16, rows=outline_shell(SHELL), alt={'idle1|idle3|walk1|walk3': outline_shell(SHELL_HOT)}, not_=NOT_BALL),
        dict(n='sp1', g='body', x=10, y=15, rows=SPIKE, not_=NOT_BALL),
        dict(n='sp2', g='body', x=16, y=11, rows=SPIKE, not_=NOT_BALL),
        dict(n='sp3', g='body', x=23, y=9, rows=SPIKE, not_=NOT_BALL),
        dict(n='sp4', g='body', x=30, y=11, rows=SPIKE, not_=NOT_BALL),
                dict(n='head', g='head', x=40, y=28, rows=HEAD, not_=NOT_BALL),
        dict(n='ear', g='ear', x=36, y=23, rows=EAR, not_=NOT_BALL),
        dict(n='nhorn', g='head', x=59, y=30, rows=NHORN, not_=NOT_BALL),
        dict(n='eye', g='head', x=51, y=36, rows=EYE, alt=EYE_ALT, not_=NOT_BALL),
        dict(n='ball', g='root', x=14, y=20, rows=ball(), alt={'atk2': ball(True, .28)}, only=NOT_BALL),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 0), 'ear': (0, -1)},
    'idle2': {'body': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 2), 'head': (-2, 1), 'ear': (-1, 1), 'tail': (1, 1)},
    'atk1': {'root': (6, 0)},
    'atk2': {'root': (12, 0)},
    'hit': {'root': (-3, 0), 'head': (-3, 2), 'ear': (0, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'ear': 'head', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
