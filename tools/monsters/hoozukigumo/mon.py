# ホオズキグモ（フェアリー・ゴースト × クモ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭胸部、足は 短く 太く、ホオズキの 腹は 大きく）
META = dict(id='hoozukigumo', name='ホオズキグモ', types=['fairy', 'ghost'], base='クモ', size='S')
PAL = {
    'k': '#101018', 'l': '#2a1838',
    'D': '#9a82c8', 'E': '#5c4888', 'F': '#33264e',          # 甲（むらさき）
    'A': '#ffd47a', 'B': '#f48a2a', 'C': '#a8401c',          # ホオズキの 袋
    'S': '#c8fcff', 'T': '#46c4e6',                          # 霊火（目も 同じ 色）
    'M': '#f06aa4',                                          # フェアリーの もよう
    'w': '#ffffff',
}
LIGHT = set('DASw')
KEEP_BLACK = set('wST')
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
import math
def L(n, g, grid, **kw): d = dict(n=n, g=g, x=0, y=0, rows=R(grid)); d.update(kw); return d
CARA = 'DEF'; FAR = 'EFl'

# ---- 足（短く 太く、ひざが 上に 出る）：付け根は 頭胸部の 中へ 3ドット ----
def leg(path, ramp=CARA):
    g = G(64, 64)
    tube(g, path[:2], [2.4, 1.9], ramp); tube(g, path[1:], [1.9, 1.2], ramp)
    kx, ky = path[1]; ball(g, kx, ky, 2.3, 2.3, ramp)              # ひざの 関節
    dots(g, 'D', [(int(kx) - 1, int(ky) - 1)]); dots(g, 'M', [(int(kx), int(ky) + 2)])   # ひざの 光・フェアリーの 輪
    fx, fy = path[2]; dots(g, 'l', [(int(fx), int(fy) - 1)])
    g = ol(g)
    return g
LEGS = {
    'n1': [(44, 45), (53, 38), (55, 59)], 'n2': [(42, 48), (48, 48), (49, 59)],
    'n3': [(36, 48), (30, 48), (29, 59)], 'n4': [(34, 45), (24, 40), (19, 59)],
}

# ---- ホオズキの 腹（見せ所）：つけ根が 広く、先が 後ろ上へ とがる ちょうちん形。すじの 間の やぶれ目から 霊火 ----
TIP = (8, 19); STEM = (33, 36)
def lantern(glow=0):
    g = G(64, 64)
    m = G(64, 64); pix.ellipse(m, 21, 31, 12, 11, '#'); poly(m, [(12, 25), (TIP[0], TIP[1]), (10, 19), (18, 21)], '#')
    for y in range(64):
        for x in range(64):
            if m[y][x] == '#':
                nx, ny = (x + .5 - 21) / 12, (y + .5 - 31) / 11; l = -nx * .6 - ny * .8
                g[y][x] = 'A' if l > .45 else ('C' if l < -.4 else 'B')
    # すじ（つけ根 → 先へ）：濃い 線＋上がわに 明るい ふち
    for (cx, cy) in ((16, 14), (24, 30), (20, 44), (34, 22)):
        for i in range(70):
            t = i / 69; x = (1 - t) ** 2 * STEM[0] + 2 * (1 - t) * t * cx + t * t * TIP[0]; y = (1 - t) ** 2 * STEM[1] + 2 * (1 - t) * t * cy + t * t * TIP[1]
            X, Y = int(x), int(y)
            if g[Y][X] != '.': g[Y][X] = 'C'
            if g[Y - 1][X] == 'B': g[Y - 1][X] = 'A'
    # やぶれ目（網の すけた 窓）と 霊火
    for y in range(64):
        for x in range(64):
            d = ((x + .5 - 21) / (6 + glow)) ** 2 + ((y + .5 - 32) / (5.5 + glow)) ** 2
            if d <= 1 and g[y][x] != '.':
                g[y][x] = 'C' if d > .7 else 'T'
    fl = ['..S...', '.SS.S.', '.SwSS.', 'SSwwS.', '.SwwS.', '..SS..'] if not glow else ['.S..S..', '.SS.SS.', 'SSwSSS.', 'SwwwwS.', 'SwwwwSS', '.SwwS..', '..SS...']
    stamp(g, fl, 18 - glow, 29 - glow)
    for (x, y) in ((16, 31), (17, 32), (24, 30), (25, 31), (20, 35), (21, 36)):   # 網の すじ
        if g[y][x] in 'T': g[y][x] = 'B'
    return ol(g)

# ---- 頭胸部（大きく）：甲の 上に フェアリーの もよう ----
def head(gape=0):
    g = G(64, 64)
    ball(g, 42, 37, 9, 8.5, CARA, hi=.5, lo=-.35)
    for (x, y) in ((38, 30), (39, 31), (40, 32), (41, 31), (42, 30)): g[y][x] = 'M'     # V字の もよう
    dots(g, 'l', [(35, 34), (35, 35), (36, 37), (36, 38), (37, 40)]); dots(g, 'D', [(36, 34), (36, 35), (37, 37)])   # 甲の ふち
    for y in range(36, 47):                                                         # 顔の 面（目の 下は 一段 暗い）
        for x in range(42, 52):
            if g[y][x] == 'D' and y > 38: g[y][x] = 'E'
            if g[y][x] == 'E' and y > 41 and x > 45: g[y][x] = 'F'
    g = ol(g)
    # 上あご（2本）：太い 根もと＋白く 内へ 曲がる きば
    FANG = ['kkkk.', 'kDEk.', 'kEFk.', 'kwwk.', '.kwwk', '.kwk.', '..k..']
    FANG_O = ['kkkk.', 'kDEk.', 'kEFk.', 'kwwk.', 'kwk..', 'kwk..', '.k...']
    for ox in (0, 4):
        stamp(g, FANG_O if gape else FANG, 45 + ox + gape, 41)
    return g
# 目：白い 光＋霊火色の 虹彩 2色＋たての ひとみ。まゆの ひさしは 前へ 下がる。上に 小さな 副眼 2つ
EYE = ['kkkk.....', '.kkkkkk..', '..kwSSkSk', '..kTTTkTk', '...kkkkk.']
EYE_ALT = {'blink': ['kkkk.....', '.kkkkkk..', '.........', '..kkkkkkk', '.........'],
           'hit': ['.........', '..kk...k.', '...kk.kk.', '..kk...kk', '.........'],
           'atk0|atk1|atk2': ['kkkk.....', '.kkkkkk..', '..kwwSkSk', '..kSSTkTk', '...kkkkk.'],
           'ko': ['.........', '..k..k...', '...kk....', '...kk....', '..k..k...']}
SUB = ['kSk.kSk', '.k...k.']
WISP = [['..k..', '.kSk.', '.kSSk', 'kSwSk', 'kSwSk', '.kkk.'], ['.k...', '.kSk.', 'kSSk.', 'kSwSk', 'kSwSk', '.kkk.']]
BITE = [['....kk', '..kkSk', '.kSSk.', 'kSwk..', 'kSk...', '.k....'], ['..k...', '.kSk..', 'kSwSkk', '.kSSSk', '..kkk.']]
def pedicel():
    g = G(64, 64); tube(g, [(31, 36), (36, 37)], [3, 3], CARA); return ol(g)
NB = 'atk1|atk2'
def layers():
    LG = {k: leg(v) for k, v in LEGS.items() if k[0] == 'n'}
    return [
        L('lantern', 'abd', lantern(), alt={'atk0|atk1|idle1|idle3': lantern(1)}, x=-1, y=3),
        L('ped', 'abd', pedicel(), x=-1, y=3),
        L('n4', 'legA', LG['n4']), L('n3', 'legB', LG['n3']), L('n2', 'legA', LG['n2']), L('n1', 'legB', LG['n1']),
        L('head', 'head', head(), alt={NB: head(1)}, x=-1, y=4),
        dict(n='eye', g='head', x=40, y=34, rows=EYE, alt=EYE_ALT),
        dict(n='sub', g='head', x=40, y=32, rows=SUB, not_='blink|ko|hit'),
        dict(n='wisp', g='fx', x=13, y=13, rows=WISP[0], alt={'idle1|idle3|walk1|walk3': WISP[1]}, not_='ko'),
        dict(n='bite', g='fx2', x=52, y=41, rows=BITE[0], alt={'atk2': BITE[1]}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'fx': (0, -1)}, 'idle2': {'head': (0, 1), 'abd': (0, 1)}, 'idle3': {'abd': (0, 1), 'fx': (0, -1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'fx': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'body': (0, 0), 'fx': (0, -1)},
    'atk0': {'body': (-2, 1), 'legA': (-1, 0), 'legB': (-1, 0)}, 'atk1': {'root': (5, 0), 'head': (1, 1)}, 'atk2': {'root': (7, 0), 'head': (1, 1), 'fx2': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'abd': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'abd', 'fx2': 'root'}
