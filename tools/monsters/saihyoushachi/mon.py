# サイヒョウシャチ（みず・こおり × シャチ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭、胴は 短く まるく、背びれ＝砕氷船の 船首は 大きく）
META = dict(id='saihyoushachi', name='サイヒョウシャチ', types=['water', 'ice'], base='シャチ', size='L')
PAL = {
    'k': '#101018', 'l': '#1a2032',
    'B': '#56627e', 'C': '#2e354e', 'D': '#1c2032',                    # シャチの 黒
    'E': '#e2ecf2', 'F': '#9aaabe',                                    # シャチの 白
    'V': '#d0f6ff', 'W': '#74cdf2', 'X': '#2f7cbc',                    # 氷
    'R': '#d0343c',                                                    # 船の 赤い 帯
    'Y': '#ffe25e', 'O': '#e8701c',                                    # 目
    'w': '#ffffff',
}
LIGHT = set('BEVYw')
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
BLK = 'BCD'; WHT = 'wEF'; ICE = 'VWX'

# ---- 胴（短く まるい）＋ 尾びれ ----
def body():
    g = G(64, 64)
    ball(g, 26, 39, 15, 10.5, BLK)
    for y in range(40, 52):                                        # 腹の 白
        for x in range(10, 44):
            if g[y][x] != '.' and y > 44 - (x - 20) / 5: g[y][x] = 'E' if y < 47 else 'F'
    # 背中の 白い サドル（ぼかし）
    for (x, y) in ((18, 30), (19, 30), (20, 30), (17, 31), (18, 31)): g[y][x] = 'F'
    return ol(g)
def tail(sw=0):
    g = G(64, 64)
    tube(g, [(14, 40), (8, 38)], [5.5, 3.5], BLK)
    poly(g, [(9, 37), (1, 27 + sw), (5, 27 + sw), (12, 35)], 'C'); poly(g, [(9, 39), (1, 48 - sw), (5, 47 - sw), (12, 41)], 'C')
    edge(g, {'C': BLK}, 1, 1, 1, 1)
    return ol(g)
# ---- 胸びれ（短く 太い）----
def pec(up=0):
    g = G(64, 64)
    tube(g, [(36, 44), (38, 50 - up), (35, 54 - up)], [3.6, 3.4, 2.4], BLK)
    return ol(g)
# ---- 背びれ（見せ所）＝砕氷船の 船首：前へ つき出た 鋭い 板。氷の 鉄板、鋲の 列、赤い 喫水線、根もとに 氷の かけら ----
def fin(glow=0):
    g = G(64, 64)
    poly(g, [(20, 31), (24, 22), (31, 13), (41, 4), (43, 5), (40, 14), (38, 24), (37, 31)], 'W')
    edge(g, {'W': ICE}, 2, 2, 2, 2)
    # 前の ふち（船首の 刃）：白く 光る
    for (x, y) in ((41, 5), (41, 6), (40, 7), (40, 8), (40, 9), (39, 10), (39, 11), (39, 12), (39, 13), (38, 14), (38, 15), (38, 16), (38, 17), (37, 18), (37, 19), (37, 20), (37, 21), (37, 22), (36, 23), (36, 24), (36, 25)):
        if g[y][x] != '.': g[y][x] = 'w' if y < 14 or glow else 'V'
    for y0 in (13, 20):                                            # 鉄板の つぎ目
        for x in range(20, 39):
            if g[y0][x] == 'W' or g[y0][x] == 'X': g[y0][x] = 'X'
            if g[y0 - 1][x] == 'W': g[y0 - 1][x] = 'V'
    for (x, y) in ((33, 16), (35, 16), (30, 23), (32, 23), (34, 23), (28, 25), (31, 25), (34, 25)):  # 鋲
        if g[y][x] != '.': g[y][x] = 'X'
    for x in range(20, 39):                                        # 赤い 帯（喫水線）
        for y in (27, 28):
            if g[y][x] != '.': g[y][x] = 'R'
        if g[29][x] != '.': g[29][x] = 'C'
    g = ol(g)
    # 氷の かけら（根もと）
    for (x, y, h) in ((19, 31, 4), (24, 30, 3), (36, 30, 4)):
        for i in range(h):
            dots(g, 'V' if i < h - 1 else 'W', [(x, y - i)])
            dots(g, 'k', [(x - 1, y - i), (x + 1, y - i)])
        dots(g, 'k', [(x, y - h)])
    return g
# ---- 頭（大きく）：白い 目の 上の もよう、下あごは 白、するどい 歯 ----
def head(gape=0):
    g = G(64, 64)
    ball(g, 44, 36, 14, 12, BLK, hi=.5, lo=-.3)
    lo = G(64, 64); poly(lo, [(36, 42 + gape), (58, 40 + gape), (56, 45 + gape), (46, 49 + gape), (36, 48 + gape)], 'E'); edge(lo, {'E': WHT}, 1, 1, 2, 1)
    if gape:
        poly(g, [(38, 40), (58, 38), (58, 41 + gape), (38, 43 + gape)], 'l')
        hline(g, 'R', 42, 54, 42 + gape // 2)
    stamp(g, R(lo), 0, 0)
    for y in range(24, 49):
        for x in range(30, 59):
            if g[y][x] == 'D' and y > 44: g[y][x] = 'F'
    # 白い アイパッチ（目の 後ろ上）
    for (x0, x1, y) in ((38, 43, 30), (37, 45, 31), (37, 45, 32), (38, 44, 33)): hline(g, 'E', x0, x1, y)
    hline(g, 'F', 39, 43, 33)
    g = ol(g)
    # 歯（上は 下むき、下は 上むき）
    for x in range(42, 57, 3):
        y = 41 - (x - 42) // 8
        dots(g, 'k', [(x - 1, y), (x + 1, y), (x, y + 1)]); dots(g, 'w', [(x, y)])
        yy = y + 1 + gape
        dots(g, 'k', [(x, yy + 1)]); dots(g, 'w', [(x + 1, yy)])
    dots(g, 'k', [(58, 39), (59, 39)])
    return g
# 目（K：魚の 目）：シャチの 白い 斑を 前へ のばし、その 中に 小さく まぶたの ない 丸い 目。平たい 黒瞳＋細い 氷色の 輪（水色・青）＋白い 光
PATCH = ['...EEEEEE....', 'EEEEEEEEEEE..', 'EEEEEEEEEEEF.', 'EEEEEEEEEEF..', 'FEEEEEEEEEF..', '.FFFFFFFFF...', '...FFFFF.....']
def eyerows(cells):
    g = [list(r) for r in PATCH]
    for y, x, s in cells:
        for i, c in enumerate(s):
            if c != ' ': g[y][x + i] = c
    return [''.join(r) for r in g]
EYE = eyerows([(1, 5, 'kkkk'), (2, 4, 'kwWWXk'), (3, 4, 'kWkkXk'), (4, 4, 'kXXXXk'), (5, 5, 'kkkk')])
EYE_ALT = {'blink': eyerows([(2, 4, 'kkkkkk'), (3, 5, 'FFFF')]),
           'hit': eyerows([(1, 5, 'kk'), (2, 6, 'kk'), (3, 7, 'kk'), (4, 5, 'kk'), (4, 7, ' '), (3, 5, '  ')]),
           'atk0|atk1|atk2': eyerows([(1, 5, 'kkkk'), (2, 4, 'kwwWWk'), (3, 4, 'kwkkWk'), (4, 4, 'kWWXXk'), (5, 5, 'kkkk')]),
           'ko': eyerows([(1, 5, 'k  k'), (2, 6, 'kk'), (3, 6, 'kk'), (4, 5, 'k  k')])}
# 氷の いぶき（攻撃）
def breath(ph):
    g = G(90, 64)
    for (x, y, s_) in (((62, 41, 2), (66, 38, 3), (70, 43, 2)) if ph == 0 else ((64, 40, 3), (69, 36, 3), (73, 42, 4), (68, 46, 2))):
        poly(g, [(x - s_, y), (x, y - s_ - 1), (x + s_, y), (x, y + s_ + 1)], 'W')
        dots(g, 'V', [(x, y - 1), (x - 1, y)]); dots(g, 'w', [(x, y)])
    return ol(g)
NB = 'atk1|atk2'
def layers():
    return [
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(2)}),
        L('fin', 'fin', fin(), alt={'atk0|atk1|atk2': fin(1)}),
        L('body', 'body', body()),
        L('head', 'head', head(), alt={'atk0': head(1), NB: head(4)}),
        dict(n='eye', g='head', x=44, y=29, rows=EYE, alt=EYE_ALT),
        L('pec', 'pec', pec(), alt={'idle1|idle3|walk1|walk3': pec(1)}),
        L('breath', 'fx', breath(0), alt={'atk2': breath(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, 1)}, 'idle2': {'root': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 1)}, 'blink': {},
    'walk0': {'root': (0, -1), 'tail': (1, 0)}, 'walk1': {'root': (0, 0)}, 'walk2': {'root': (0, 1), 'tail': (-1, 0)}, 'walk3': {'root': (0, 0)},
    'atk0': {'root': (-3, 0), 'head': (-1, -1), 'fin': (0, -1)}, 'atk1': {'root': (5, 0), 'head': (1, 0)}, 'atk2': {'root': (6, 0), 'head': (1, 0), 'fx': (1, 0)},
    'hit': {'root': (-3, -1), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
EYE_BOX = (44, 29, 12, 7)
PARENT = {'head': 'body', 'fin': 'body', 'tail': 'body', 'pec': 'body', 'body': 'root', 'fx': 'root'}
