# ヌエ（ノーマル・あく × 妖怪ぬえ）手打ち GBA風・デフォルメ（2〜3頭身：猿の 顔と たてがみを 大きく、虎の 胴と 足は 短く 太く）
META = dict(id='nue', name='ヌエ', types=['normal', 'dark'], base='ぬえ（妖怪）', size='L')
EYE_BOX = (45, 30, 7, 4)   # 目（idle0 の 64x64 座標）
PAL = {
    'k': '#101018', 'l': '#3e1e16',
    'Y': '#ffc858', 'O': '#d47e22', 'B': '#7e3c16',
    'W': '#fbf8ee', 'V': '#cfc5b2', 'D': '#7e706a',
    'R': '#d8382e',
    'P': '#8a6aa8', 'Q': '#4c3466', 'Z': '#261a34',
    'E': '#d4ff3a', 'e': '#6a9a10', 'w': '#ffffff',
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

# ---- 胴（デフォルメ：短く 丸く）：肩が 高い 虎の 体。しまは 手で ----
SPAN = [(20, 27), (14, 29), (9, 30), (5, 30), (3, 30), (2, 30), (1, 30), (1, 30), (1, 30), (1, 30), (1, 30), (1, 30),
        (1, 30), (2, 29), (3, 28), (5, 27), (8, 25)]
STRIPES = [  # しま：上は 太く、下へ 細く（手で 1ドットずつ）
    [(8, 3), (9, 3), (8, 4), (9, 4), (9, 5), (9, 6), (10, 7)],
    [(14, 1), (15, 1), (14, 2), (15, 2), (15, 3), (15, 4), (16, 5), (16, 6), (16, 7)],
    [(20, 0), (21, 0), (20, 1), (21, 1), (21, 2), (21, 3), (22, 4), (22, 5)],
    [(25, 0), (26, 0), (25, 1), (26, 2), (26, 3), (27, 4)],
    [(4, 6), (5, 6), (4, 7), (5, 8), (5, 9)],
    [(10, 11), (11, 11), (11, 12), (12, 13)], [(17, 10), (18, 10), (18, 11), (18, 12), (19, 13)], [(24, 9), (25, 9), (25, 10), (25, 11), (26, 12)],
]
def body():
    g = shade(SPAN, 31, 'YOB', lit=2, dk=3)
    for s in STRIPES:
        for (x, y) in s:
            if g[y][x] != '.': g[y][x] = 'k'
    for (x, y) in ((7, 5), (13, 3), (19, 2), (24, 2), (3, 8)):
        if g[y][x] == 'O': g[y][x] = 'Y'
    return [''.join(r) for r in _ol(g)]

# ---- たてがみ（白い 毛の えり）：大きく 丸く、後ろへ 毛たばが なびく ----
import math
def mane():
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
    from pix import poly, ellipse
    W, H = 32, 30; cx, cy = 18, 14.5; g = [['.'] * W for _ in range(H)]
    ellipse(g, cx, cy, 10.5, 11, "#")
    # 毛たば：まわりから 外へ、後ろ（左）へ なびく 三角
    for deg in (-70, -100, -130, -160, 170, 140, 110, 80):
        a = math.radians(deg); ex, ey = cx + 9.5 * math.cos(a), cy + 10 * math.sin(a)
        tx, ty = cx + 14.5 * math.cos(a) - 3.5, cy + 14 * math.sin(a)
        nx, ny = -math.sin(a) * 3, math.cos(a) * 3
        poly(g, [(ex + nx, ey + ny), (ex - nx, ey - ny), (tx, ty)], '#')
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '#': continue
            up = next(i for i in range(1, 9) if y - i < 0 or g[y - i][x] == '.' or i == 8)
            lf = next(i for i in range(1, 9) if x - i < 0 or g[y][x - i] == '.' or i == 8)
            dn = next(i for i in range(1, 9) if y + i >= H or g[y + i][x] == '.' or i == 8)
            v = (x - cx) * .5 + (y - cy) * .8
            out[y][x] = 'D' if (dn <= 2 or v > 8) else 'W' if (up <= 2 or lf <= 1 or v < -6) else 'V'
    # 毛の すじ（たばの 中心線を 濃く）
    for deg in (-70, -100, -130, -160, 170, 140, 110, 80):
        a = math.radians(deg)
        for t in (.62, .72, .82):
            x, y = round(cx + 15 * t * math.cos(a) - 3.5 * t), round(cy + 15 * t * math.sin(a))
            if 0 <= y < H and 0 <= x < W and out[y][x] in 'WV': out[y][x] = 'D' if out[y][x] == 'V' else 'V'
    return [''.join(r) for r in _ol(out)]
MANE = mane()
# 顔（大きく）：赤い 猿の 顔、太い まゆの でっぱり、長い 口に 上下の 牙
FACE = [
    '...kkkkkkkk.......',
    '..kYYYRRRRRkk.....',
    '.kYYRRRRRRRRRkk...',
    'kYRRRRRRRRRRRRRk..',
    'kkkkkkkkkkRRRRRRk.',
    'kBBBBBBBBkkRRRRRk.',
    'kRRRRRRRRRkRRRRRRk',
    'kRRRRRRRRRRRRRYYRk',
    '.kBRRRRRRRRRRRRkRk',
    '.kBRRRRRRRRRkkkkk.',
    '..kBRRRRRkwkwkwkwk',
    '..kBRRRRkZZZZZZZk.',
    '...kBRRRkwkwkwkk..',
    '...kBBBBBBBBBk....',
    '....kkkkkkkkk.....',
]
FACE_OPEN = FACE[:9] + [
    '.kBRRRRRRRkkkkkkk.',
    '..kBRRRRkwZwZwZwk.',
    '..kBRRRkZZZZZZZk..',
    '..kBRRkZZZZZZZk...',
    '...kBRkwZwZwZk....',
    '...kBBBBBBBBk.....',
    '....kkkkkkkk......',
]
# 目（C：三白眼）：まゆの でっぱりの 下、白目（w／影 V）が 大きく、黄緑の 小さな 虹彩（E）と 黒い 点の 瞳が 上の 前すみに 押しつけられる。下まぶたは 太い 黒線＋赤茶の 影
EYE = ['kwwEkEk', 'kVwwEwk', '.kkkkkk', '..BBBB.']
EYE_ALT = {'blink': ['BBBBBBB', 'kkkkkkk', '.RRRRRR', '.......'], 'atk0|atk1|atk2': ['kwwEkEk', 'kwwwEwk', 'kVwwwwk', '.kkkkkk'],
           'hit': ['RkkRRRR', 'RRRkkkk', 'RkkRRRR', '.......'], 'ko': ['RkRRkRR', 'RRkkRRR', 'RkRRkRR', '.......']}

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
    'kPkwEkkQQQQk',
    'kQkeekQQQQkk',
    'kQQQQQkkkkk.',
    '.kZZkwkwk...',
    '..kkkk......',
]
SHEAD_OPEN = [
    '..kkkkk.....',
    '.kPPPPQkk...',
    'kPPkkkkPQkk.',
    'kPkwEkkQQQQk',
    'kQkeekQQkkk.',
    'kQQQQkwkwk..',
    'kQQQkZZZZRR.',
    'kZZZkwkwk..R',
    '.kkkkkkk....',
]

# 足（デフォルメ：短く 太く）。上の 3行は 胴に 食いこむ もも
FLEG = [
    'kYYOOOOOBk.',
    'kYOOOOOOBk.',
    'kYOOOOOOBk.',
    '.kYOOkkOBk.',
    '.kYOOOOOBk.',
    '.kYOOOOBBk.',
    'kYOOOOOOBBk',
    'kOOOOOOOBBk',
    '.kBBBBBBBk.',
    '..kwkwkwk..',
]
# 前足を ふり上げた 形（攻撃）
FLEG_UP = [
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
    'kYYOOOOOOBk',
    'kYYOOkkOOBk',
    'kYOOOOOOOBk',
    '.kOOOOOOBk.',
    '..kOOOOBk..',
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
SX, SY = 7, 3   # 蛇の しっぽの ずらし（付け根は 腰に 食いこむ）
def layers():
    return [
        dict(n='snake', g='tail', x=-1 + SX, y=4 + SY, rows=SNAKE, alt={'atk0': SNAKE_B, 'atk1|atk2': SNAKE_A}),
        dict(n='shead', g='shead', x=16 + SX, y=7 + SY, rows=SHEAD, not_='atk0|atk1|atk2'),
        dict(n='sheadB', g='tail', x=12 + SX, y=5 + SY, rows=SHEAD, only='atk0'),
        dict(n='sheadA', g='tail', x=30 + SX, y=12 + SY, rows=SHEAD_OPEN, only='atk1|atk2'),
        dict(n='legHF', g='legB', x=19, y=48, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=37, y=47, rows=dark(FLEG)),
        dict(n='body', g='body', x=10, y=33, rows=BODY),
        dict(n='legH', g='legA', x=12, y=48, rows=HLEG),
        dict(n='legF', g='legB', x=31, y=48, rows=FLEG, not_='atk1'),
        dict(n='legFup', g='body', x=33, y=45, rows=FLEG_UP, only='atk1'),
        dict(n='mane', g='head', x=27, y=18, rows=MANE),
        dict(n='face', g='head', x=44, y=25, rows=FACE, alt={'atk1|atk2': FACE_OPEN}),
        dict(n='eye', g='head', x=45, y=30, rows=EYE, alt=EYE_ALT),
        dict(n='cloud', g='root', x=7, y=55, rows=CLOUD, alt={'idle1|idle3|walk1|walk3|atk1': CLOUD2}, not_='ko'),
        dict(n='slash', g='root', x=58, y=38, rows=SLASH, only='atk2'),
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
