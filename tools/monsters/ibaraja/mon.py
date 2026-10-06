# イバラジャ（フェアリー・どく × ヘビ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline, recolor

# ---------- 下書きの 道具（あたりを とり、陰影は 光の 向きで 決めて から 手で 直す）----------
W = H = 64
def G(): return grid(W, H)
def at(g, x, y): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < H and 0 <= x < W: g[y][x] = ch
def ell(p, cx, cy, rx, ry, ch, only=None):
    for y in range(H):
        for x in range(W):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1 and (only is None or p[y][x] in only): p[y][x] = ch
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < W and 0 <= y < H and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(W)] for y in range(H)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < H and 0 <= xx < W else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(H) for x in range(W) if m[y][x]}
def shade(p, ramps, r=2, hi=.35, lo=-.3):
    """左上から 光：ramps = {下書きの 文字: '明中暗'}"""
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def ink(p, ch='k'):
    """1ドットの 黒い 輪郭で かこむ"""
    g = G()
    for y in range(H):
        for x in range(W):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = ch
            elif p[y][x] != '.': g[y][x] = p[y][x]
    return g
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g
def swap(g, mp, box=None):
    x0, y0, x1, y1 = box or (0, 0, W, H)
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            if g[y][x] in mp: g[y][x] = mp[g[y][x]]
    return g
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < W and 0 <= y + dy < H: g[y + dy][x + dx] = c
    return rows_of(g)

META = dict(id='ibaraja', name='イバラジャ', types=['fairy', 'poison'], base='ヘビ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1432',
    'A': '#a8d858', 'B': '#4f8e30', 'C': '#245030',      # いばらの 茎＝うろこ（緑）
    'P': '#ff9ad2', 'Q': '#e0428e', 'R': '#8c1a58',      # バラの 花びら
    'T': '#f0e0b0',                                      # とげの 先（白っぽい 骨色）
    'V': '#d88cff', 'U': '#7a30b0',                      # 毒（むらさき）
    'Y': '#ffe040', 'w': '#ffffff', 'r': '#5a0c28',
}
LIGHT = set('APTVYw')
KEEP_BLACK = set('wYVr')

RAMP = {'1': 'ABC', '5': 'PQR'}
# ---------- 胴：S字に 立ちあがる いばらの 茎 ----------
LOW_PATH = [(7, 55.5), (10, 57), (18, 57.6), (28, 56.4), (36, 53.2), (40, 47.5), (37, 42), (29, 38.6), (22, 35)]
LOW_RAD = [1.2, 2.4, 3.3, 3.9, 4.3, 4.4, 4.3, 4.1, 4]
NECK_PATH = [(24, 36.5), (20.5, 32), (21.5, 27), (26, 24.5), (31, 23)]
NECK_RAD = [4, 3.9, 3.8, 3.6, 3.4]
def thorns(p, path, rad, every, side):
    """茎の 外がわに とげ（根もとは 濃い赤、先は 白）"""
    pts = []
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / every))
        for j in range(n):
            t = (j + .5) / n; cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t; r = rad[i] + (rad[i + 1] - rad[i]) * t
            dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L * side, dx / L * side
            pts.append((cx, cy, r, nx, ny))
    for cx, cy, r, nx, ny in pts:
        bx, by = cx + nx * (r - .5), cy + ny * (r - .5)
        # 後ろへ 少し そった 三角の とげ
        tx, ty = bx + nx * 3.2 - (ny * .0), by + ny * 3.2
        for k in range(4):
            x, y = int(bx + (tx - bx) * k / 3), int(by + (ty - by) * k / 3)
            if 0 <= x < W and 0 <= y < H: p[y][x] = '9' if k < 3 else 'T'
        x, y = int(bx + nx * 1 + ny), int(by + ny * 1 - nx)
        if 0 <= x < W and 0 <= y < H and p[y][x] == '.': p[y][x] = '9'
KO_PATH = [(3, 57), (10, 58), (18, 56.6), (26, 57.8), (34, 57), (40, 56)]
KO_RAD = [1.4, 2.6, 3.4, 3.8, 3.9, 3.8]
def stem(path, rad, side, every=7):
    p = G(); tube(p, path, rad, '1'); s = shade(p, RAMP, r=2)
    # うろこの ななめ帯（茎の ねじれ）
    for y in range(H):
        for x in range(W):
            if s[y][x] == 'B' and (x - y) % 6 == 0 and at(s, x - 1, y + 1) in 'BC': s[y][x] = 'C'
    thorns(s, path, rad, every, side)
    s = swap(s, {'9': 'R'})
    return ink(s)
def coil(): return rows_of(stem(LOW_PATH, LOW_RAD, -1))
def neck(): return rows_of(stem(NECK_PATH, NECK_RAD, -1, 6))

# ---------- バラの 頭（花びらが 頭の うしろを つつむ）----------
BC = (33.5, 16.5)
# 手打ちの バラ（3/4 前から。外の 花びらが 杯形に つつみ、中心は 巻いた うず）
ROSE = [
    '.......kkkk..kkkk.......',
    '.....kkPPPPkkPPPPkkk....',
    '....kPPQQQQPPkQQQQPPk...',
    '...kPQQQRRRRQPkRRQQQPk..',
    '..kPQQRRkkkkkRRPkRQQQQk.',
    '..kPQRkPPPPPPkkRPkRQQQk.',
    '.kPQRkPQQQQQQPPkRkRQQRk.',
    'kkPQRkPQRRRRRQQPkRkQQRk.',
    'kPQQRkPQRkPPkRQQkRkQQRRk',
    'kPQQRkPQRkPQRkQQkRkQQRRk',
    'kPQQRRkPQRRRkQQRkRQQRRRk',
    'kPQQQRkPQQQQQQRkRQQQRRRk',
    'kPQQQRRkkQQQQRkRRQQQRRRk',
    '.kPQQQRRRkkkkkRRQQQRRRk.',
    '.kPPQQQRRRRRRRQQQQRRRRk.',
    'kPPPQQQQQQQQQQQQQRRRRk..',
    'kRPPPQQQQQQQQQQQRRRRRk..',
    '.kRRPPPQQQQQQQRRRRRkk...',
    '..kkRRRRRRRRRRRRRRk.....',
    '....kkkkkkkkkkkkkk......',
]
def bloom(open_=0, wilt=False):
    g = G(); rows = ROSE
    if open_:      # 怒ると 外の 花びらが ひらく：ふちを 1ドット ふくらませる
        rows = outline(recolor(ROSE, {'k': 'R'}), 'k')
        rows = [r.replace('R', 'Q', 1) if i < 6 else r for i, r in enumerate(rows)]
    if wilt: rows = recolor(rows, {'P': 'Q', 'Q': 'R'})
    put(g, rows, int(BC[0]) - 12 - (1 if open_ else 0), int(BC[1]) - 10 - (1 if open_ else 0))
    return rows_of(g)
def sepals(wilt=False):
    """花の うしろから つき出る とがった がく（緑）"""
    p = G(); cx, cy = BC
    for ang, L in ((186, 20), (214, 18), (152, 19)):
        a = math.radians(ang); tx, ty = cx + math.cos(a) * L, cy + math.sin(a) * L + (5 if wilt else 0)
        nx, ny = -math.sin(a) * 3.2, math.cos(a) * 3.2
        poly(p, [(cx + nx, cy + ny), (tx, ty), (cx - nx, cy - ny)], '1')
    s = shade(p, RAMP, r=1)
    return rows_of(ink(s))

# 頭（へびの 口先）：花から 前へ つき出す。まゆの ひさし＋たての ひとみ
HEAD = [
    '....kkkkkk...........',
    '..kkAAAAAAkkkkk......',
    '.kAABBBBBBAAAAAkkk...',
    'kABBBkkkBBBBBBBBAAk..',
    'kBBBBYYkkkBBBBBBBBBk.',
    'kBBBBYkYYkBBBBBBBBkBk',
    'kBBBBBkkkBBBBBBBBBBBk',
    'kCBBBBBBBBBBBBBBBBBBk',
    'kCCBBBBkkkkkkkkkkkkkk',
    'kCCCBBkwCCCCwCCCCCk..',
    '.kCCCCkwCCCCCCCCCk...',
    '..kkCCCCCCCCCCCkk....',
    '....kkkkkkkkkkk......',
]
HEAD_OPEN = [
    '....kkkkkk...........',
    '..kkAAAAAAkkkkk......',
    '.kAABBBBBBAAAAAkkk...',
    'kABBBkkkBBBBBBBBAAk..',
    'kBBBBYYYkkBBBBBBBBBk.',
    'kBBBBYYkYkBBBBBBBBkBk',
    'kBBBBBkkkBBBBBBBBBBBk',
    'kCBBBkkkkkkkkkkkkkkkk',
    'kCCBkrwrrrrwrrrrrwk..',
    'kCCBkrwrrrrrrrrrrk...',
    'kCCCkrrrrrrrrrrrk....',
    'kCCCkrrrrrrrrrrrrk...',
    '.kCCkrrrwrrrrwrrrrk..',
    '.kCCkkkwkkkkwkkkkwkk.',
    '..kCCCCCCCCCCCCCCCk..',
    '...kkkkkkkkkkkkkkk...',
]
def _eye(h, a, b, c):
    h = list(h)
    for i, t in zip((4, 5, 6), (a, b, c)): h[i] = h[i][:5] + t + h[i][5 + len(t):]
    return h
HEAD_BLINK = _eye(HEAD, 'BBBkk', 'BkkkB', 'BBBBB')
HEAD_HIT = _eye(HEAD, 'kBBBk', 'BkBkB', 'kBBBk')
HEAD_KO = _eye(HEAD, 'kBkBB', 'BkBBB', 'kBkBB')
HEAD_ATK0 = _eye(HEAD, 'YYYkk', 'YYkYk', 'BkkkB')
DRIP = ['V', 'U']
DRIP2 = ['.', 'V', 'U']
SPRAY = [
    '..........V...V.....',
    '...VV...VVU.......V.',
    'VVVUVVVVVUVV.VV..VU.',
    'UVVVUUVVVVUVVUVV.V..',
    '..UU..VUV..U..U.....',
    '.......U......U.....',
]
SPRAY2 = ['......V...V...', '..V.VUV..V..U.', 'VUVV.U..U.....', '.U.....U......']
# 怒って ひらく 外がわの 花びら（とげの ついた がく）
SEPAL = ['kk....', 'kAkk..', '.kBBkk', '..kkBk', '....kk']

def layers():
    CO = coil(); NE = neck(); BL = bloom(); BL_O = bloom(1); BL_W = bloom(0, True)
    return [
        dict(n='coil', g='coil', x=0, y=0, rows=CO, not_='ko'),
        dict(n='neck', g='neck', x=0, y=0, rows=NE, not_='ko'),
        dict(n='sepal', g='bloom', x=0, y=0, rows=sepals(), not_='ko'),
        dict(n='bloom', g='bloom', x=0, y=0, rows=BL, alt={'atk0|atk1|atk2': BL_O}, not_='ko'),
        dict(n='head', g='head', x=40, y=10, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN, 'atk0': HEAD_ATK0, 'blink': HEAD_BLINK, 'hit': HEAD_HIT}, not_='ko'),
        dict(n='drip', g='head', x=47, y=21, rows=DRIP, alt={'idle2|idle3|walk1|walk3': DRIP2}, not_='atk1|atk2|ko'),
        dict(n='spray', g='head', x=60, y=18, rows=SPRAY, only='atk1'),
        dict(n='spray2', g='head', x=61, y=19, rows=SPRAY2, only='atk2'),
        # ダウン：花が しおれて 頭が 地面に 落ちる
        dict(n='bodyko', g='root', x=0, y=0, rows=rows_of(stem(KO_PATH, KO_RAD, -1)), only='ko'),
        dict(n='sepalko', g='root', x=4, y=31, rows=sepals(True), only='ko'),
        dict(n='bloomko', g='root', x=4, y=32, rows=BL_W, only='ko'),
        dict(n='headko', g='root', x=40, y=48, rows=HEAD_KO, only='ko'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'neck': (0, 1)}, 'idle2': {'neck': (0, 1)}, 'idle3': {'neck': (0, 0), 'bloom': (0, -1)},
    'blink': {},
    'walk0': {'neck': (-1, 0)}, 'walk1': {'neck': (0, 1), 'coil': (1, 0)}, 'walk2': {'neck': (1, 0)}, 'walk3': {'neck': (0, 1), 'coil': (-1, 0)},
    'atk0': {'neck': (-2, 1), 'head': (-1, 0)}, 'atk1': {'neck': (3, -1), 'head': (2, 0)}, 'atk2': {'neck': (3, 0), 'head': (1, 0)},
    'hit': {'neck': (-2, 1), 'head': (-2, 1), 'bloom': (0, 0)}, 'ko': {},
}
PARENT = {'head': 'neck', 'bloom': 'neck', 'neck': 'root', 'coil': 'root'}
