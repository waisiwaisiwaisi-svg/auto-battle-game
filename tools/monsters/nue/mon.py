# ヌエ（ノーマル・あく × 妖怪ぬえ）手打ち GBA風
META = dict(id='nue', name='ヌエ', types=['normal', 'dark'], base='ぬえ（妖怪）', size='L')
PAL = {
    'k': '#101018', 'l': '#3e1e16',
    'Y': '#ffc858', 'O': '#d47e22', 'B': '#7e3c16',
    'W': '#fbf8ee', 'V': '#cfc5b2', 'D': '#7e706a',
    'R': '#d8382e',
    'P': '#8a6aa8', 'Q': '#4c3466', 'Z': '#261a34',
    'E': '#d4ff3a', 'w': '#ffffff',
}
LIGHT = set('YWPEw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, ramp='YOB', lit=1, dk=2):
    H = len(spans); m = [[a <= x <= b for x in range(W)] for (a, b) in spans]
    def ins(y, x): return 0 <= y < H and 0 <= x < W and m[y][x]
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            du = next(i for i in range(1, 9) if not ins(y - i, x) or i == 8)
            dl = next(i for i in range(1, 9) if not ins(y, x - i) or i == 8)
            dd = next(i for i in range(1, 9) if not ins(y + i, x) or i == 8)
            dr = next(i for i in range(1, 9) if not ins(y, x + i) or i == 8)
            c = ramp[1]
            if dd <= dk: c = ramp[2]
            elif du <= lit or dl <= 1: c = ramp[0]
            elif dr <= 1: c = ramp[2]
            g[y][x] = c
    return g

# ---- 胴：肩が 高く 腰が 低い 虎の 体。しまは 手で ----
SPAN = [(26, 34), (22, 36), (19, 37), (16, 38), (12, 38), (8, 39), (5, 39), (3, 39), (2, 39), (1, 39), (1, 39), (1, 39),
        (1, 39), (1, 39), (1, 39), (1, 38), (2, 38), (3, 37), (5, 36), (8, 35), (14, 34), (20, 33)]
STRIPES = [  # しま：上は 太く、下へ 細く（手で 1ドットずつ）
    [(9, 5), (10, 5), (11, 5), (9, 6), (10, 6), (10, 7), (11, 7), (11, 8), (11, 9)],
    [(14, 4), (15, 4), (16, 4), (14, 5), (15, 5), (15, 6), (16, 6), (15, 7), (16, 8), (16, 9), (16, 10)],
    [(19, 2), (20, 2), (21, 2), (19, 3), (20, 3), (20, 4), (21, 4), (20, 5), (21, 6), (21, 7), (21, 8)],
    [(24, 1), (25, 1), (26, 1), (24, 2), (25, 2), (25, 3), (26, 3), (25, 4), (26, 5), (26, 6)],
    [(5, 7), (6, 7), (5, 8), (6, 8), (5, 9), (6, 10), (6, 11)], [(2, 11), (3, 11), (3, 12), (4, 12), (4, 13), (5, 14)],
    [(11, 12), (12, 12), (12, 13), (12, 14), (13, 15), (13, 16)], [(18, 12), (19, 12), (19, 13), (19, 14), (20, 15)],
    [(25, 10), (26, 10), (26, 11), (26, 12), (27, 13), (27, 14)], [(30, 6), (31, 6), (31, 7), (31, 8), (32, 9)],
]
def body():
    g = shade(SPAN, 40, 'YOB', lit=2, dk=3)
    for s in STRIPES:
        for (x, y) in s:
            if g[y][x] != '.': g[y][x] = 'k'
    for (x, y) in ((8, 7), (13, 6), (18, 4), (23, 3), (7, 9)):
        if g[y][x] == 'O': g[y][x] = 'Y'
    return [''.join(r) for r in _ol(g)]

# ---- たてがみ（白い 毛の えり）：外がわへ のびる 毛たばを 手で ----
MANE = [
    '.......kk.k..........',
    '.....kkWWkWk.........',
    '...kkWWWWWVWkk.......',
    '..kWWWWVVVVVVVkk.....',
    '.kWWWWWWDWWVVVVVk....',
    'kWWWWWVDDWWVVVVVVk...',
    'kkWWWVDDVWVVDVVVVVk..',
    'kWWVVDVVVVVDDVVVVVk..',
    '.kWVVVVVVVDVVVVVVVVk.',
    'kWVVVVVVDDVVVVVVVVVk.',
    'kkVVVVVDVVVVVDVVVVDk.',
    'kWVVVVDVVVVVDDVVVVDk.',
    '.kVVVVVVVVVDVVVVVDDk.',
    'kWVVVVVVVVDVVVVVDDk..',
    '.kDVVVVVVDVVVVVDDDk..',
    'kDDVVVVVDVVVVDDDk....',
    '.kkDDVVDDVVDDDk......',
    '...kDDkDDkDDkk.......',
    '....kk.kk.kk.........',
]
# 顔：赤い 猿の 顔、太い まゆの でっぱり、長い 口に 牙
FACE = [
    '..kkkkkkk.....',
    '.kYYYRRRRkk...',
    'kYYRRRRRRRRk..',
    'kkkkkkkkRRRRk.',
    'kBBBBBkkkRRRRk',
    'kRRBRRRRRYYRRk',
    '.kRRRRRRRRRRBk',
    '.kBRRRRRRkkkk.',
    '..kBRRRkwkwkwk',
    '..kBRRkZZZZZk.',
    '...kBBkwkwkk..',
    '....kkkkkk....',
]
EYE = ['EEEk', 'kEk.']
EYE_ALT = {'blink': ['kkkk', 'RBB.'], 'atk0|atk1|atk2': ['wwEk', 'kwk.'], 'hit': ['EkEk', 'kEk.'], 'ko': ['kBkB', 'BkB.']}
FACE_OPEN = FACE[:7] + [
    '.kBRRRRRkkkkk.',
    '..kRRRRkwZwZwk',
    '..kRRRkZZZZZk.',
    '..kRRRkZZZZk..',
    '...kRBkwZwk...',
    '....kkkkkk....',
]

# ---- 蛇の しっぽ：中心の 道すじを 手で 決めた 太い 管（上左が 明）＋うろこ ----
PATH = [(9, 33), (7, 30), (5, 26), (4, 22), (5, 18), (7, 14), (10, 11), (14, 9), (18, 8)]
def snake(path, W=24, H=37, r=2.6):
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            best = None
            for (ax, ay), (bx, by) in zip(path, path[1:]):
                dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
                t = max(0, min(1, ((x + .5 - ax) * dx + (y + .5 - ay) * dy) / L2))
                px, py = ax + t * dx - (x + .5), ay + t * dy - (y + .5)
                d = (px * px + py * py) ** .5
                if best is None or d < best[0]:
                    L = L2 ** .5; nx, ny = -dy / L, dx / L
                    if nx + ny > 0: nx, ny = -nx, -ny
                    best = (d, -(px * nx + py * ny))
            if best[0] <= r:
                s = best[1] / r
                g[y][x] = 'P' if s > .35 else ('Q' if s > -.45 else 'Z')
                if s < -.75: g[y][x] = 'V'   # 腹の うろこ
    # うろこの もよう（手で）
    for (x, y) in ((5, 28), (4, 24), (4, 20), (6, 16), (9, 12), (12, 10), (16, 9), (7, 31)):
        if g[y][x] == 'Q': g[y][x] = 'Z'
        if g[y - 1][x - 1] == 'Q': g[y - 1][x - 1] = 'P'
    return [''.join(r) for r in _ol(g)]
SNAKE = snake(PATH)
PATH_B = [(9, 33), (7, 30), (5, 26), (4, 22), (5, 18), (6, 14), (8, 10), (11, 7), (14, 6)]
PATH_A = [(9, 33), (7, 30), (5, 26), (4, 22), (5, 18), (7, 14), (10, 11), (15, 9), (21, 9), (27, 11), (32, 14)]
SNAKE_B = snake(PATH_B)
SNAKE_A = snake(PATH_A, W=40)
SHEAD = [
    '..kkkkk.....',
    '.kPPPPQkk...',
    'kPPkkkkPQkk.',
    'kPkEEkkQQQQk',
    'kQQkkQQQQQkk',
    'kQQQQQkkkkk.',
    '.kZZkwkwk...',
    '..kkkk......',
]
SHEAD_OPEN = [
    '..kkkkk.....',
    '.kPPPPQkk...',
    'kPPkkkkPQkk.',
    'kPkwwkkQQQQk',
    'kQQkkQQQkkk.',
    'kQQQQkwkwk..',
    'kQQQkZZZZRR.',
    'kZZZkwkwk..R',
    '.kkkkkkk....',
]

FLEG = [
    '.kkkkkkk..',
    'kYYOOOOOBk',
    'kYOkkOOOBk',
    'kYOOOOOOBk',
    '.kYOOkkOBk',
    '.kOOOOOOBk',
    '..kYOOOBk.',
    '..kOkkOBk.',
    '..kOOOOBk.',
    '..kYOOOBk.',
    '.kYOOOOOBk',
    'kYOOOOOOBBk',
    'kOOOOOOOBBk',
    '.kBBBBBBBk.',
    '..kwkwkwk..',
]
# 前足を ふり上げた 形（攻撃）
FLEG_UP = [
    'kkkkkk...........',
    'kYYOOOkkkkkk.....',
    'kYOOOOOOOOOYkk...',
    'kOOkkOOkkOOOOYkwk',
    'kOOOOOOOOOkOOOOkw',
    'kOOOOOOOOOOOOBBk.',
    '.kBBOOOOOBBBBBkwk',
    '..kkkBBBBBkkkkkw.',
    '.......kkkk......',
]
HLEG = [
    '..kkkkkkk..',
    '.kYYOOOOOkk',
    'kYYOOkkOOBk',
    'kYOOOOOkOBk',
    'kYOOOOOOOBk',
    'kOkkOOOOBBk',
    '.kOOOOOOBk.',
    '..kOOOOBk..',
    '...kOOBk...',
    '...kOkBk...',
    '...kOOBk...',
    '..kYOOOBk..',
    '.kYOOOOOBk.',
    '.kOOOOOBBk.',
    '..kBBBBBk..',
    '..kwkwkwk..',
]
CLOUD = [
    '...kkk.......kkkk.......kkk.......',
    '..kPPQk..kkkkPPQQk...kkPPQk..kk...',
    '.kPQQQZkkPPQQQQQQZkkkPPQQQZkkPQk..',
    'kPQQZZZQQQQZZZZZZZZQQQQZZZZZQQZZk.',
    'kQZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZk',
    '.kkZZZZkkkZZZZZZkkkkZZZZZkkkZZZkk.',
    '...kkkk...kkkkkk....kkkkk...kkk...',
]
CLOUD2 = [
    '....kkk......kkk.......kkkk......',
    '..kkPPQk..kkkPPQk...kkPPQQk..kk..',
    '.kPPQQQZkkPPQQQQZkkkPQQQQQZkkPQk.',
    'kPQQZZZZQQQZZZZZZZQQQQZZZZZZQQZZk',
    'kQZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZk',
    '.kkZZZkkkZZZZZZZkkkZZZZZZkkkZZkk.',
    '...kkk...kkkkkkk...kkkkkk...kk...',
]
SLASH = [
    '.......E.....',
    '......E..E...',
    '.....E..E...E',
    '....E..E...E.',
    '...E..E...E..',
    '..E..E...E...',
    '.E..E...E....',
    'E.......E....',
]
DARK = {'Y': 'O', 'O': 'B', 'B': 'l', 'W': 'V', 'V': 'D'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    return [
        dict(n='snake', g='tail', x=-1, y=4, rows=SNAKE, alt={'atk0': SNAKE_B, 'atk1|atk2': SNAKE_A}),
        dict(n='shead', g='shead', x=16, y=7, rows=SHEAD, not_='atk0|atk1|atk2'),
        dict(n='sheadB', g='tail', x=12, y=5, rows=SHEAD, only='atk0'),
        dict(n='sheadA', g='tail', x=30, y=12, rows=SHEAD_OPEN, only='atk1|atk2'),
        dict(n='legHF', g='legB', x=13, y=45, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=30, y=45, rows=dark(FLEG)),
        dict(n='body', g='body', x=4, y=28, rows=BODY),
        dict(n='legH', g='legA', x=6, y=45, rows=HLEG),
        dict(n='mane', g='head', x=33, y=19, rows=MANE),
        dict(n='face', g='head', x=45, y=25, rows=FACE, alt={'atk1|atk2': FACE_OPEN}),
        dict(n='eye', g='head', x=46, y=29, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='legB', x=36, y=46, rows=FLEG, not_='atk1'),
        dict(n='legFup', g='body', x=38, y=42, rows=FLEG_UP, only='atk1'),
        dict(n='cloud', g='root', x=2, y=55, rows=CLOUD, alt={'idle1|idle3|walk1|walk3|atk1': CLOUD2}, not_='ko'),
        dict(n='slash', g='root', x=56, y=40, rows=SLASH, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'shead': (0, -1)},
    'idle2': {'body': (0, 1), 'tail': (0, 0), 'shead': (1, 0)},
    'idle3': {'shead': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 1), 'legB': (-1, 0)},
    'atk1': {'root': (5, 0), 'body': (0, -1), 'head': (1, -1)},
    'atk2': {'root': (7, 0), 'legB': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'tail': (0, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'shead': 'tail', 'body': 'root', 'legA': 'root', 'legB': 'root'}
