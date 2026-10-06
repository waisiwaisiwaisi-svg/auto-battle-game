# ツチザメ（みず・かくとう × シュモクザメ）手打ち GBA風・デフォルメ（2〜3頭身：木槌の 頭を 大きく、胴は 短く まるく、ひれは 短く 太く）
META = dict(id='tsuchizame', name='ツチザメ', types=['water', 'fighting'], base='シュモクザメ', size='L')
PAL = {
    'k': '#101018', 'l': '#1c2436',
    'P': '#a2bcd2', 'Q': '#5c7a9a', 'R': '#34485e',                    # サメの はだ
    'E': '#eaf0f2',                                                    # 腹・さらし
    'A': '#eec68c', 'B': '#b27a44', 'C': '#6a4224',                    # 木槌
    'V': '#a0e8ff', 'W': '#2e8cd8',                                    # 水
    'Y': '#ffd84a', 'O': '#e0661c',                                    # 目
    'w': '#ffffff',
}
LIGHT = set('PEAVYw')
KEEP_BLACK = set('wYO')
# ---------- 下書きの 道具（あたり → 光の 向きで 3段階 → 仕上げは 手打ち）----------
import pix
def G(w, h): return pix.grid(w, h)
def R(g): return pix.rows_of(g)
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def hline(g, ch, x0, x1, y): dots(g, ch, [(x, y) for x in range(x0, x1 + 1)])
def ball(g, cx, cy, rx, ry, ramp, only=None, hi=.45, lo=-.35):
    """だ円を 左上の 光で 3段階に ぬる"""
    L, M, D = ramp
    for y in range(len(g)):
        for x in range(len(g[0])):
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if nx * nx + ny * ny > 1 or (only and g[y][x] not in only): continue
            l = -nx * .6 - ny * .8
            g[y][x] = L if l > hi else (D if l < lo else M)
def tube(g, path, rad, ramp):
    """太さの ある 線（ヘビの 胴・首・しっぽ）。光は 左上"""
    L, M, D = ramp; H, W = len(g), len(g[0])
    for y in range(H):
        for x in range(W):
            best = None
            for i in range(len(path) - 1):
                (ax, ay), (bx, by) = path[i], path[i + 1]; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1
                t = max(0, min(1, ((x + .5 - ax) * dx + (y + .5 - ay) * dy) / L2))
                r = rad[i] + (rad[i + 1] - rad[i]) * t
                px, py = x + .5 - (ax + t * dx), y + .5 - (ay + t * dy); d = (px * px + py * py) ** .5
                if d <= r and (best is None or d / r < best[0]): best = (d / r, px / r, py / r)
            if best:
                l = -best[1] * .6 - best[2] * .8
                g[y][x] = L if l > .4 else (D if l < -.3 else M)
def poly(g, pts, ch): pix.poly(g, pts, ch)
def edge(g, ramps, up=1, left=1, down=1, right=1):
    """ぬった 面の ふちに 光（上・左）と 影（下・右）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = src[y][x]
            if m not in ramps: continue
            Lc, Mc, Dc = ramps[m]
            def run(dx, dy, n):
                for i in range(1, n + 1):
                    yy, xx = y + dy * i, x + dx * i
                    if not (0 <= yy < H and 0 <= xx < W) or src[yy][xx] != m: return True
                return False
            if run(0, 1, down) or run(1, 0, right): g[y][x] = Dc
            elif run(0, -1, up) or run(-1, 0, left): g[y][x] = Lc
            else: g[y][x] = Mc
def ol(g, ch='k'):
    """同じ 大きさの まま まわりに 輪郭（余白が いる）"""
    H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): o[y][x] = ch
    return o
def inner(g, ch, a, b):
    """面 a と 面 b の さかい目に 線（a 側）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if src[y][x] in a and any(0 <= y + dy < H and 0 <= x + dx < W and src[y + dy][x + dx] in b for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0))): g[y][x] = ch
def stamp(g, rows, x, y): pix.stamp(g, rows, x, y)
def crop(g):
    """余白を けずって (rows, x0, y0)"""
    ys = [y for y in range(len(g)) if any(c != '.' for c in g[y])]; xs = [x for x in range(len(g[0])) if any(g[y][x] != '.' for y in range(len(g)))]
    return [''.join(g[y][xs[0]:xs[-1] + 1]) for y in range(ys[0], ys[-1] + 1)], xs[0], ys[0]
def part(fn, n, g, **kw):
    """64x64 の 下書き → 層（余白を けずり、位置を おぼえる）"""
    rows, x0, y0 = crop(g); d = dict(n=n, g=fn, x=x0, y=y0, rows=rows); d.update(kw); return d
def L(n, g, grid, **kw): d = dict(n=n, g=g, x=0, y=0, rows=R(grid)); d.update(kw); return d
SK = 'PQR'; WOOD = 'ABC'

# ---- 胴（短く まるい）：上は 青灰、腹は 白 ----
def body():
    g = G(64, 64)
    ball(g, 27, 36, 14, 10.5, SK)
    for y in range(36, 48):
        for x in range(10, 50):
            if g[y][x] != '.' and y > 39 - (x - 27) / 6: g[y][x] = 'E' if y < 44 else 'P'
    for (x, y) in ((33, 31), (35, 32), (37, 33)): dots(g, 'R', [(x, y), (x, y + 1)])   # えら
    return ol(g)
# ---- 尾びれ（ふたまた）----
def tail(sw=0):
    g = G(64, 64)
    tube(g, [(16, 36), (9, 35)], [6, 4], SK)
    poly(g, [(11, 34), (2, 20 + sw), (6, 20 + sw), (14, 32)], 'Q'); poly(g, [(11, 36), (2, 49 - sw), (6, 48 - sw), (14, 38)], 'Q')
    edge(g, {'Q': SK}, 1, 1, 1, 1)
    return ol(g)
# ---- 背びれ ----
def dorsal():
    g = G(64, 64); poly(g, [(19, 28), (25, 13), (28, 13), (31, 27)], 'Q'); edge(g, {'Q': SK}, 1, 2, 1, 1)
    return ol(g)
# ---- 胸びれの うで：先に さらしを まいた こぶし ----
def fin(punch=0):
    g = G(80, 64)
    if not punch:
        tube(g, [(31, 42), (35, 47), (37, 50)], [3.6, 3.2, 3], SK)
        ball(g, 38, 51, 4.2, 3.8, 'wEE')
        for x in range(34, 43):
            if g[50][x] != '.': g[50][x] = 'B'
    else:
        tube(g, [(31, 42), (40, 44), (49, 45)], [3.6, 3.2, 3], SK)
        ball(g, 51, 45, 4.2, 3.8, 'wEE')
        for y in range(41, 50):
            if g[y][50] != '.': g[y][50] = 'B'
    return ol(g)
# ---- 木槌の 頭（見せ所）：たての 円柱の 頭（両はしが ふくらんだ 槌の 形）。前は 平らな 打つ 面、さらしの 帯、両はしに 目 ----
def hammer():
    g = G(64, 64)
    poly(g, [(46, 15), (49, 10), (57, 10), (61, 14), (61, 45), (57, 49), (49, 49), (46, 44), (48, 40), (48, 19)], 'Q')
    edge(g, {'Q': SK}, 2, 2, 2, 2)
    for y in range(11, 49):                                       # 前の 平らな 打つ 面
        if g[y][58] != '.': g[y][58] = 'R'
        for x in (59, 60):
            if g[y][x] != '.': g[y][x] = 'P' if y < 40 else 'Q'
    for y0 in (20, 36):                                           # さらしの 帯（かくとう）
        for x in range(47, 61):
            for dy, c in ((0, 'w'), (1, 'E'), (2, 'E')):
                if g[y0 + dy][x] != '.': g[y0 + dy][x] = c if x < 57 else 'P'
            if g[y0 + 3][x] != '.': g[y0 + 3][x] = 'R'
        dots(g, 'B', [(52, y0 + 1), (53, y0 + 2)])
    for (x, y) in ((52, 26), (53, 27), (53, 30), (54, 31), (52, 33)):
        if g[y][x] != '.': g[y][x] = 'R'                          # きずあと
    return ol(g)
def snout():
    g = G(64, 64); ball(g, 43, 34, 8, 9, SK)
    for y in range(33, 42):
        for x in range(35, 51):
            if g[y][x] != '.' and y > 35: g[y][x] = 'E'
    return ol(g)
# 口：するどい 三角の 歯
MOUTH = ['kkkkkkkkkk', 'kwwkwwkwwk', '.kwkwkwkk.', '..kkkkkk..']
MOUTH_O = ['kkkkkkkkkk', 'kwwkwwkwwk', 'kRRRRRRRRk', 'kRRllllRRk', 'kwkwwkwwkk', '.kkkkkkkk.']
# 目（木槌の 上の はし）：白い 光＋金と だいだいの 虹彩＋たての ひとみ、まゆの 線
EYE = ['kkkk....', '.kkkkkkk', '.kwYYYkY', '.kYYOOkO', '..kOOOkk', '...kkkk.']
EYE_ALT = {'blink': ['kkkk....', '.kkkkkkk', '........', '.kkkkkkk', '........', '........'], 'hit': ['........', '.kk...kk', '..kk.kk.', '...kkk..', '..kk.kk.', '........'],
           'atk0|atk1|atk2': ['kkkk....', '.kkkkkkk', '.kwwYYkY', '.kwYYYkY', '..kOOOkk', '...kkkk.'], 'ko': ['........', '..k...k.', '...k.k..', '....k...', '...k.k..', '..k...k.']}
EYE2 = ['kkkkk', 'kwYOk', '.kkkk']                                  # 下の はしの 目（小さく）
# 水の しぶき（頭突きの 決め）
def burst(ph):
    g = G(80, 64)
    for (x, y, r) in (((63, 22, 2.4), (65, 30, 3), (63, 38, 2.4)) if ph == 0 else ((66, 20, 2.6), (69, 30, 3.4), (66, 40, 2.6), (71, 25, 1.6), (71, 36, 1.6))):
        ball(g, x, y, r, r, 'VVW')
    return ol(g)
NB = 'atk1|atk2'
def layers():
    return [
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(2)}),
        L('dorsal', 'body', dorsal()),
        dict(n='finB', g='body', x=-4, y=-2, rows=R(fin()), not_=NB),
        L('body', 'body', body()),
        L('snout', 'head', snout()),
        dict(n='mouth', g='head', x=37, y=39, rows=MOUTH, alt={'atk0|' + NB: MOUTH_O}),
        L('hammer', 'hammer', hammer()),
        dict(n='eye', g='hammer', x=50, y=11, rows=EYE, alt=EYE_ALT),
        dict(n='eye2', g='hammer', x=53, y=43, rows=EYE2, not_='blink|hit|ko'),
        L('fin', 'fin', fin(), alt={NB: fin(1)}),
        L('burst', 'fx', burst(0), alt={'atk2': burst(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, 1)}, 'idle2': {'root': (0, 1), 'hammer': (0, 1)}, 'idle3': {'hammer': (0, 1)}, 'blink': {},
    'walk0': {'root': (0, -1), 'tail': (1, 0), 'fin': (-1, 0)}, 'walk1': {'root': (0, 0)},
    'walk2': {'root': (0, 1), 'tail': (-1, 0), 'fin': (1, 0)}, 'walk3': {'root': (0, 0)},
    'atk0': {'root': (-3, 0), 'head': (-1, 0), 'hammer': (-1, -1), 'fin': (-1, 0)}, 'atk1': {'root': (5, 0), 'hammer': (1, 0)}, 'atk2': {'root': (6, 0), 'hammer': (1, 0), 'fx': (1, 0)},
    'hit': {'root': (-3, -1), 'hammer': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'hammer': 'head', 'head': 'body', 'tail': 'body', 'fin': 'body', 'body': 'root', 'fx': 'root'}
