# カマダヌキ（ノーマル・はがね × タヌキ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭、胴は 鉄の 茶釜で まるく、手足は 短く 太く）
META = dict(id='kamadanuki', name='カマダヌキ', types=['normal', 'steel'], base='タヌキ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1c1c',
    'F': '#e6b674', 'G': '#a8703a', 'H': '#5c3820', 'D': '#352628',   # 毛（明・中・暗）＋ くまどり・手足
    'C': '#f6e8c8',                                                    # 口もと
    'S': '#9aa6ba', 'T': '#56607a', 'U': '#2a3044',                    # 鉄の 釜
    'Y': '#ffd660', 'O': '#c0761c',                                    # 金の ふち・目
    'w': '#ffffff',
}
LIGHT = set('FCSYw')
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
import math
def L(n, g, grid, **kw): d = dict(n=n, g=g, x=0, y=0, rows=R(grid)); d.update(kw); return d
FUR = 'FGH'; IRON = 'STU'; DFUR = 'HDl'

# ---- しっぽ：太い しまの しっぽ（後ろに 立てる）----
def tail(sw=0):
    g = G(64, 64)
    tube(g, [(24, 48), (15, 46), (10 + sw, 39), (11 + sw, 32)], [3, 5, 5.4, 3.6], FUR)
    for (x0, y0, x1, y1) in ((13, 49, 17, 43), (8, 43, 13, 39), (8 + sw, 36, 14 + sw, 35)):
        pix.line(g, x0, y0, x1, y1, 'D')
    for y in range(26, 34):
        for x in range(4, 20):
            if g[y][x] != '.' and y < 32 - (x - 6 - sw) // 3: g[y][x] = 'D'
    return ol(g)
# ---- 足・腕（短く 太く、白い 爪）----
LEG = ['kkkkkk.', 'kHDDDlk', 'kHDDDlk', 'kDDDDlk', 'kHDDDDlk', 'kDDDDllk', 'kwkwkwkk']
LEG_N = ['.......'] + LEG[1:]
ARM = ['..kkkk..', '.kHDDDk.', 'kHDDDDlk', 'kDDDDDlk', '.kDDDllk', '.kDDDlkw', '.kwkwkk.']
ARM_UP = ['..kkk...', '.kHDDk..', 'kHDDDlk.', 'kDDDDlkw', '.kDDDlkw', '..kwkwk.']
DARKF = {'H': 'D', 'D': 'l', 'w': 'S'}
def far(rows): return [''.join(DARKF.get(c, c) for c in r) for r in rows]

# ---- 鉄の 茶釜（見せ所の 胴）：あられ もようの いぼ、金の ふち、前に ふた ----
def kettle(lid=0):
    g = G(64, 64)
    ball(g, 32, 43, 12.5, 10.5, IRON, hi=.45, lo=-.3)
    for y in range(34, 54):                                     # あられ（いぼ）を 市松に
        for x in range(20, 45):
            if (x + (y // 3) * 2) % 4 == 0 and y % 3 == 0 and g[y][x] in 'ST':
                g[y][x] = 'S' if g[y][x] == 'T' else 'w'
                if g[y + 1][x] in 'ST': g[y + 1][x] = 'U'
    for x in range(20, 45):                                     # 金の ふち（口）
        if g[34][x] != '.': g[34][x] = 'O'
        if g[33][x] != '.': g[33][x] = 'Y'
    for x in range(21, 44):                                     # すその 帯
        if g[50][x] != '.': g[50][x] = 'U'
    g = ol(g)
    # 鐶（かん）：横の 鉄の 輪
    stamp(g, ['.kkk.', 'kOYOk', 'kY.Ok', 'kOOOk', '.kkk.'], 17, 37)
    # ふた
    if lid == 0:
        stamp(g, ['..kkkkkk..', '.kSSSSSTk.', 'kSSkYYkSTk', 'kSTkOOkTUk', '.kTTTTTUk.', '..kkkkkk..'], 31, 40)
    elif lid == 1:   # 熱く 光る
        stamp(g, ['..kkkkkk..', '.kYYYYYOk.', 'kYYkwwkYOk', 'kYOkYYkOOk', '.kOOOOOOk.', '..kkkkkk..'], 31, 40)
    else:            # ひらいた ふた（上へ）＋ 中は 赤く 光る 湯気口
        stamp(g, ['..kkkkkk..', '.kOOOOOOk.', 'kOYYwwYYOk', 'kOYwwwwYOk', '.kOYYYYOk.', '..kkkkkk..'], 31, 41)
        stamp(g, ['...kkkk..', '.kkSSSSk.', 'kSSkYkSTk', '.kkTTTTk.', '...kkkk..'], 32, 35)
    return g

# ---- 頭（大きく）：まるい 耳、くまどりの 中に つり目、とがった 口に 牙 ----
def head():
    g = G(64, 64)
    for (x, y, rmp) in ((29, 14, 'GHD'), (38, 13, FUR)):             # 耳
        ball(g, x, y, 4, 4, rmp)
    ball(g, 36, 23, 11.5, 9.5, FUR, hi=.5, lo=-.3)
    # ほおの 毛（ぎざぎざ）
    poly(g, [(25, 25), (22, 31), (27, 29), (26, 34), (31, 31), (33, 34), (35, 31)], 'G')
    for (x, y) in ((22, 31), (26, 34), (33, 34)): g[y][x] = 'H'
    ball(g, 47, 27, 5.5, 4, 'CCG')                                     # 口もと
    g = ol(g)
    for (x, y) in ((29, 14), (30, 13), (38, 13), (39, 12)): g[y][x] = 'D'   # 耳の 中
    dots(g, 'l', [(29, 15), (38, 14)])
    # くまどり（目の まわりの 黒い 毛）：前へ 下がる
    for (x0, x1, y) in ((33, 45, 21), (32, 46, 22), (32, 46, 23), (33, 45, 24), (34, 44, 25), (36, 41, 26)):
        hline(g, 'D', x0, x1, y)
    dots(g, 'F', [(46, 21), (45, 20), (44, 20), (34, 20), (35, 20)])
    # 鼻と 口
    dots(g, 'k', [(51, 25), (52, 25), (51, 26), (52, 26), (52, 27)]); dots(g, 'G', [(51, 24)])
    hline(g, 'k', 43, 51, 29); dots(g, 'k', [(42, 28)])
    dots(g, 'w', [(47, 30), (49, 30)]); dots(g, 'k', [(46, 30), (48, 30), (50, 30), (47, 31), (49, 31)])
    return g
# 目：白い 光＋金と だいだいの 虹彩＋たての ひとみ（くまどりの 中）。上に 太い まゆ
EYE = ['kkk.....', '.kkkkkk.', '.kwYYkOk', '..kOOkkk']
EYE_ALT = {'blink': ['kkk.....', '.kkkkkk.', '.DDDDDDk', '..kkkkk.'], 'hit': ['.kk...k.', '..kk.kk.', '.kk.kk..', '........'],
           'atk0|atk1|atk2': ['kkk.....', '.kkkkkkk', '.kwwYkYk', '..kYOkOk'], 'ko': ['........', '.kD.kD..', '..kD....', '.kD.kD..']}
# 湯気の 一撃
def steam(ph):
    g = G(80, 64)
    for (x, y, r) in (((46, 44, 3), (51, 42, 3.6), (57, 44, 4)) if ph == 0 else ((50, 43, 3.4), (56, 41, 4.2), (63, 44, 4.6), (59, 48, 3))):
        ball(g, x, y, r, r, 'wSS')
    return ol(g)
NB = 'atk1|atk2'
def layers():
    return [
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(1)}),
        dict(n='armB', g='armB', x=18, y=38, rows=far(ARM)),
        dict(n='legB', g='legB', x=34, y=53, rows=far(LEG)),
        L('kettle', 'body', kettle(), alt={'atk0': kettle(1), NB: kettle(2)}),
        dict(n='legA', g='legA', x=25, y=53, rows=LEG_N),
        L('head', 'head', head()),
        dict(n='eye', g='head', x=37, y=20, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='arm', x=42, y=38, rows=ARM, alt={NB: ARM_UP}),
        L('steam', 'fx', steam(0), alt={'atk2': steam(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'head': (0, 1), 'body': (0, 1), 'arm': (0, 1)}, 'idle3': {'body': (0, 1), 'head': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'armB': (1, 0), 'arm': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'armB': (-1, 0), 'arm': (1, 0)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (0, 1), 'arm': (-1, 0)}, 'atk1': {'root': (3, 0), 'arm': (1, -2)}, 'atk2': {'root': (4, 0), 'arm': (1, -2), 'fx': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'arm': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
