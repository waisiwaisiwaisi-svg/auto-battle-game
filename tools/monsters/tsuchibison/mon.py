# ツチバイソン（ノーマル・じめん × バイソン）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 角、胴は 小さく まるく、足は 短く 太く。肩の 大槌こぶは 大きく）
META = dict(id='tsuchibison', name='ツチバイソン', types=['normal', 'ground'], base='バイソン', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1810',
    'F': '#c08a52', 'G': '#84522e', 'H': '#4a2c1a', 'D': '#2e2020',   # 毛（明・中・暗）＋ こい たてがみ
    'A': '#d2c29e', 'B': '#8e7c60', 'C': '#4c4034',                    # 岩の 大槌
    'P': '#f4ecd6', 'Q': '#ae9e80',                                    # 角・ひづめ
    'Y': '#ffd648', 'O': '#d8601c',                                    # 目
    'R': '#c42c34', 'X': '#5c0c1a',                                    # 目（黒っぽい 赤）
    'w': '#ffffff',
}
LIGHT = set('FAPYw')
KEEP_BLACK = set('wYORX')
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
FUR = 'FGH'; ROCK = 'ABC'; HORN = 'PQC'

# ---- 胴（小さく まるい）----
def body():
    g = G(64, 64); ball(g, 27, 45, 16, 9, FUR)
    for (x, y) in ((16, 44), (20, 47), (25, 49), (31, 48)): dots(g, 'H', [(x, y), (x + 1, y + 1)])
    return ol(g)
# ---- しっぽ（ふさ）----
def tail(sw=0):
    g = G(64, 64); tube(g, [(13, 42), (7, 45), (5, 50 + sw)], [1.6, 1.3, 1.2], FUR)
    ball(g, 4.5, 51 + sw, 2.4, 3, 'HDl'); return ol(g)
# ---- 足（短く 太く、ひづめ）----
LEG = ['kkkkkkk.', 'kFGGGGHk', 'kGGGGGHk', 'kGGGGHHk', '.kGGGHk.', '.kGGGHk.', 'kHHHHHHk', 'kPPQkQQk', 'kkkkkkkk']
LEG_N = ['........'] + LEG[1:]
DK = {'F': 'G', 'G': 'H', 'H': 'D', 'P': 'Q', 'Q': 'C'}
def dark(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

# ---- 肩の 大槌こぶ（見せ所）：横だおしの 大槌の 頭（角を 落とした 岩の 角柱）。両はしに 地層の 輪、前の 打つ 面は 平ら ----
def hammer(hot=False):
    g = G(64, 64)
    poly(g, [(12, 18), (16, 13), (40, 11), (45, 15), (46, 28), (42, 32), (17, 33), (12, 29)], 'B')
    edge(g, {'B': ROCK}, 2, 2, 3, 2)
    for y in range(10, 34):                                    # 前の 打つ 面（はしの 面）
        for x in range(41, 47):
            if g[y][x] != '.' and x >= 42: g[y][x] = 'A' if y < 22 else ('B' if y < 29 else 'C')
        if g[y][41] != '.': g[y][41] = 'C'
    for x0 in (18, 35):                                        # 地層の 輪
        for y in range(10, 34):
            if g[y][x0] != '.': g[y][x0] = 'C'
            if g[y][x0 + 1] != '.': g[y][x0 + 1] = 'C'
            if g[y][x0 + 2] != '.': g[y][x0 + 2] = 'A' if y < 28 else 'B'
    for (x, y) in ((25, 16), (26, 17), (26, 18), (27, 19), (30, 24), (31, 25), (23, 26), (24, 27), (44, 18), (44, 19), (43, 25)):   # ひび
        if g[y][x] != '.': g[y][x] = 'C'
    for (x, y) in ((24, 15), (31, 23), (22, 25), (14, 22), (14, 23)): 
        if g[y][x] != '.': g[y][x] = 'A'
    if hot:
        for (x, y) in ((26, 18), (31, 25), (24, 27), (44, 19)): g[y][x] = 'Y'
    return ol(g)
# ---- こい たてがみ（体の 前半分を おおう 毛。こぶを 胴に つなぐ）----
def mane():
    g = G(64, 64)
    poly(g, [(16, 36), (18, 30), (21, 32), (24, 27), (27, 31), (30, 26), (33, 30), (36, 25), (39, 29), (42, 24), (45, 28), (48, 40), (46, 50), (43, 47), (41, 51), (38, 47), (35, 50), (33, 45), (29, 47), (27, 42), (22, 43)], 'H')
    edge(g, {'H': 'GHD'}, 2, 1, 2, 2)
    for (x, y) in ((22, 34), (28, 33), (34, 32), (40, 31), (36, 38), (30, 39), (42, 40), (25, 39)): dots(g, 'G', [(x, y), (x - 1, y + 1)]); dots(g, 'D', [(x + 1, y + 1), (x + 1, y + 2)])
    g = ol(g)
    return g
# ---- 頭（大きく 低い）：太い 角、あごひげ、するどい 目 ----
def head():
    g = G(64, 64)
    tube(g, [(44, 31), (41, 25), (44, 19)], [2.6, 1.8, 1], 'QCl')              # 奥の 角
    ball(g, 48, 38, 9.5, 10, FUR, hi=.5, lo=-.3)
    ball(g, 55, 43, 5, 4.6, FUR, hi=.4, lo=-.2)                                # 鼻づら
    poly(g, [(43, 45), (56, 47), (53, 53), (50, 51), (48, 54), (45, 50)], 'D')  # あごひげ
    g = ol(g)
    # 前がみ（頭の 上の こい 毛）
    for (x0, x1, y) in ((42, 51, 29), (41, 52, 30), (41, 50, 31), (41, 46, 32), (41, 44, 33)): hline(g, 'D', x0, x1, y)
    dots(g, 'H', [(43, 30), (47, 30), (50, 29)])
    dots(g, 'k', [(58, 41), (59, 41), (58, 42)]); dots(g, 'l', [(53, 47), (54, 47), (55, 47), (56, 47)])   # 鼻・口
    dots(g, 'H', [(57, 39)])
    # 手前の 角：横へ 出て 上へ 反る
    h = G(64, 64); tube(h, [(49, 32), (55, 29), (59, 24), (58, 19)], [2.8, 2.3, 1.7, .9], HORN); h = ol(h)
    stamp(g, R(h), 0, 0)
    return g
# 目（M：重い まぶた）：毛の 色の 厚い 上まぶたが 虹彩の 上半分を おおい、太い まぶたの 線の 下に 黒っぽい 赤の 虹彩と 半分 かくれた 黒瞳。冷たく 見下す
LID = ['..kkkkkk..', '.kFFFFGHk.', 'kHkkkkkkkk']
EYE = LID + ['.kwRkkRRk.', '.kRXRRXXk.', '..kkkkkk..']
EYE_ALT = {'blink': ['..kkkkkk..', '.kFFFFGHk.', '.kGGGGGHHk', '.kGGGGHHk.', '..kkkkkk..'],
           'hit': ['..kkkkkk..', '.kFFFFGHk.', 'kHkkkkkkkk', '..kkHHkk..', '.kk....kk.'],
           'atk0|atk1|atk2': LID + ['.kwwRkkRk.', '.kRRRXXRk.', '..kkkkkk..'],
           'ko': ['..kkkkkk..', '.kFFFFGHk.', '.kkGGGkkk.', '..kkGkk...', '..kkGkk...', '.kk...kk..']}
# 地割れの 岩くず（攻撃）
def rocks(ph):
    g = G(80, 64)
    for (x, y, r) in (((61, 55, 2.5), (65, 51, 2), (63, 46, 1.6)) if ph == 0 else ((63, 54, 3), (68, 49, 2.4), (66, 43, 2), (70, 56, 2))):
        ball(g, x, y, r, r, ROCK)
    return ol(g)
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='legFF', g='legB', x=36, y=51, rows=dark(LEG)),
        dict(n='legFH', g='legA', x=11, y=51, rows=dark(LEG)),
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(1)}),
        L('body', 'body', body()),
        L('hammer', 'hump', hammer(), alt={'atk0|atk1|atk2': hammer(True)}),
        L('mane', 'body', mane()),
        dict(n='legH', g='legA', x=16, y=51, rows=LEG_N),
        dict(n='legF', g='legB', x=40, y=51, rows=LEG_N),
        L('head', 'head', head()),
        dict(n='eye', g='head', x=45, y=33, rows=EYE, alt=EYE_ALT),
        L('rocks', 'fx', rocks(0), alt={'atk2': rocks(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'hump': (0, 1)}, 'idle2': {'hump': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, 1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, 1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 0), 'head': (-1, -2), 'hump': (0, -1)}, 'atk1': {'root': (4, 0), 'head': (1, 2), 'hump': (1, 1)}, 'atk2': {'root': (6, 0), 'head': (1, 2), 'hump': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -2)}, 'ko': {'_flip': True},
}
EYE_BOX = (45, 33, 10, 6)
PARENT = {'head': 'body', 'hump': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
