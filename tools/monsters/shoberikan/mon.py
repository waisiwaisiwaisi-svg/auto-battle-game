# ショベリカン（ノーマル・みず × ペリカン）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と バケットの くちばし、胴は 小さく まるく、足は 短く）
META = dict(id='shoberikan', name='ショベリカン', types=['normal', 'water'], base='ペリカン', size='M')
PAL = {
    'k': '#101018', 'l': '#2a2c3e',
    'A': '#eef0f6', 'B': '#b2bacc', 'C': '#687088',                    # 羽（白〜灰青）
    'Y': '#ffd04c', 'O': '#e0761e',                                    # くちばし・足・目
    'S': '#a8b2c4', 'T': '#5e6680', 'U': '#2e3448',                    # 鉄の バケット
    'V': '#9ce6ff', 'W': '#2c8ad8',                                    # 水
    'w': '#ffffff',
}
LIGHT = set('AYSVw')
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
FEA = 'wAB'; WNG = 'ABC'; IRON = 'STU'; BEAK = 'YYO'

# ---- 胴（小さく まるい）と 首 ----
def body():
    g = G(64, 64)
    ball(g, 25, 46, 12, 9, FEA)
    tube(g, [(27, 41), (30, 35), (33, 29)], [5.5, 5, 5], FEA)
    for (x, y) in ((31, 35), (30, 37)): g[y][x] = 'B'
    return ol(g)
# ---- 翼（たたんで 少し 立てる）：先は 灰青の 風切り ----
def wing(up=0):
    g = G(64, 64)
    poly(g, [(17, 39 - up), (27, 38), (33, 42), (30, 48), (21, 51), (12, 50), (10, 46 - up)], 'B')
    edge(g, {'B': WNG}, 2, 1, 2, 1)
    # 風切り羽（3枚、後ろへ とがる）
    for i, (y0) in enumerate((43, 46, 49)):
        y0 -= up if i == 0 else 0
        poly(g, [(16, y0 - 2), (7 - i, y0 - 1 + i), (16, y0 + 2)], 'C')
        hline(g, 'T', 9, 15, y0 + 1)
    for (x0, y0, x1, y1) in ((17, 44, 28, 42), (17, 47, 27, 46)):
        pix.line(g, x0, y0, x1, y1, 'C')
    return ol(g)
# ---- 足（短く、水かき）----
LEG = ['.kkkk...', '.kOOOk..', '.kOOOk..', 'kYYOOkk.', 'kYOkOOOk', 'kkkkkkkk']
LEG_N = ['........'] + LEG[1:]
def dark(rows): return [r.replace('Y', 'O').replace('O', 'O') for r in rows]
# ---- 尾羽 ----
TAIL = ['kk.....', 'kBkk...', '.kBBkk.', 'kCBBBBk', 'kCCBBk.', '.kkkk..']

# ---- 頭（大きく）：とげの 冠羽、つり目 ----
def head():
    g = G(64, 64)
    ball(g, 36, 21, 10, 9, FEA, hi=.5, lo=-.3)
    for pts in (((28, 16), (21, 10), (31, 14)), ((30, 14), (26, 6), (34, 13)), ((34, 13), (34, 6), (38, 13))):   # 冠羽
        poly(g, pts, 'B')
    for (x, y) in ((22, 11), (27, 7), (34, 7)): dots(g, 'A', [(x, y)])
    for (x, y) in ((29, 26), (31, 28), (34, 29), (28, 23)): dots(g, 'B', [(x, y)])
    return ol(g)
# ---- バケットの くちばし（見せ所）：上は 黄色い くちばし、下の 袋は 鉄の ショベル。前に 鉄の 歯 ----
def bucket(gape=0):
    g = G(80, 64)
    # ショベルの バケット：後ろは まるく、上は 平らに ひらき、前の ふちに 歯
    poly(g, [(41, 26 + gape), (59, 26 + gape), (60, 32 + gape), (57, 37 + gape), (49, 40 + gape), (43, 38 + gape), (40, 32 + gape)], 'T')
    edge(g, {'T': IRON}, 2, 2, 2, 2)
    for y in range(26 + gape, 41 + gape):                        # 補強の 帯（2本）
        for x0 in (46, 53):
            if g[y][x0] != '.': g[y][x0] = 'U'
            if g[y][x0 + 1] != '.': g[y][x0 + 1] = 'S'
    for (x, y) in ((44, 29), (51, 29), (49, 37)): dots(g, 'w', [(x, y + gape)])
    if gape:                                                      # 中の 水
        poly(g, [(41, 26), (59, 26), (59, 26 + gape), (41, 26 + gape)], 'W'); hline(g, 'V', 41, 58, 26); dots(g, 'w', [(45, 27), (52, 27)])
    g = ol(g)
    # 鉄の 歯（前の ふちから 前へ つき出す）
    for y in (27, 31, 35):
        yy = y + gape - (1 if y == 35 else 0); x = 60 if y < 35 else 58
        dots(g, 'k', [(x, yy - 1), (x + 1, yy - 1), (x + 2, yy - 1), (x + 3, yy), (x, yy + 2), (x + 1, yy + 2), (x + 2, yy + 1)]); dots(g, 'S', [(x, yy), (x + 1, yy), (x + 2, yy)]); dots(g, 'T', [(x, yy + 1), (x + 1, yy + 1)]); dots(g, 'w', [(x + 1, yy)])
    return g
def bill(up=0):
    g = G(80, 64)
    poly(g, [(42, 19 - up), (60, 21 - up), (64, 23 - up), (63, 27 - up), (61, 25 - up), (42, 26 - up)], 'Y')
    edge(g, {'Y': BEAK}, 1, 1, 1, 1)
    for x in range(44, 61):
        if g[23 - up][x] != '.' and x % 4 == 0: g[23 - up][x] = 'O'
    dots(g, 'O', [(62, 25 - up), (62, 26 - up)])
    return ol(g)
# 目：白い 光＋金と だいだいの 虹彩＋たての ひとみ。黒い まゆが 前へ 下がる
EYE = ['kkkk....', '.kkkkkkk', '.kwYYkYk', '.kYOOkOk', '..kkkkk.']
EYE_ALT = {'blink': ['kkkk....', '.kkkkkkk', '........', '.kkkkkkk', '........'], 'hit': ['........', '.kk...kk', '..kk.kk.', '.kk...kk', '........'],
           'atk0|atk1|atk2': ['kkkk....', '.kkkkkkk', '.kwwYkYk', '.kYYOkOk', '..kkkkk.'], 'ko': ['........', '.k..k...', '..kk....', '..kk....', '.k..k...']}
# 水の 一撃
def splash(ph):
    g = G(80, 64)
    for (x, y, r) in (((65, 30, 2.6), (68, 25, 2), (69, 34, 2.2)) if ph == 0 else ((69, 29, 3.2), (73, 23, 2.4), (74, 35, 2.6), (77, 29, 1.6))):
        ball(g, x, y, r, r, 'VVW')
    g = ol(g)
    return g
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='legB', g='legB', x=30, y=54, rows=dark(LEG)),
        dict(n='tail', g='body', x=6, y=45, rows=TAIL),
        L('body', 'body', body()),
        dict(n='legA', g='legA', x=21, y=54, rows=LEG_N),
        L('wing', 'wing', wing(), alt={'idle1|idle3|walk1|walk3|atk0': wing(2)}),
        L('head', 'head', head()),
        L('bucket', 'head', bucket(), alt={'atk0': bucket(1), NB: bucket(4)}),
        L('bill', 'head', bill(), alt={'atk0': bill(1), NB: bill(3)}),
        dict(n='eye', g='head', x=34, y=15, rows=EYE, alt=EYE_ALT),
        L('splash', 'fx', splash(0), alt={'atk2': splash(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'head': (0, 1), 'body': (0, 1), 'wing': (0, 1)}, 'idle3': {'body': (0, 1), 'wing': (0, 0)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1), 'head': (0, -1), 'wing': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1), 'wing': (0, -1)},
    'atk0': {'head': (-2, -1), 'body': (-1, 0)}, 'atk1': {'root': (4, 0), 'head': (1, 2)}, 'atk2': {'root': (5, 0), 'head': (1, 2), 'fx': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'root', 'wing': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
