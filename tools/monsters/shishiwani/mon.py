# シシワニ（ノーマル・ほのお × ワニ）手打ち GBA風・デフォルメ（2〜3頭身：獅子舞の 大きな 頭、胴は 布に つつまれ 小さく まるく、足は 短く 太く）
META = dict(id='shishiwani', name='シシワニ', types=['normal', 'fire'], base='ワニ', size='M')
EYE_BOX = (32, 9, 13, 11)   # 目の 位置（idle0 の 64x64 座標）
PAL = {
    'k': '#101018', 'l': '#3c1418',
    'R': '#ff6e4a', 'S': '#c4262a', 'T': '#6c1222',          # 朱ぬりの 頭
    'Y': '#ffe46e', 'O': '#ec9420',                          # 金（歯・目・ほのお）
    'G': '#84d46a', 'H': '#2f8c4c', 'J': '#1a4a36',          # 唐草の 布
    'P': '#b4aa66', 'Q': '#727040', 'U': '#3e3e26',          # ワニの 皮
    'w': '#ffffff',
}
LIGHT = set('RYGPw')
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
RED = 'RST'; CLOTH = 'GHJ'; SKIN = 'PQU'

# ---- 胴（小さく まるい）＋ 腹 ----
def body():
    g = G(64, 64); ball(g, 26, 47, 13, 8, SKIN)
    for x in range(16, 37, 3): dots(g, 'U', [(x, 51)])
    return ol(g)
# ---- 足（短く 太い ワニの 足、白い 爪 3本）：付け根は 胴に 3ドット ----
LEG = ['.kkkkk..', 'kPPQQQk.', 'kPQQQUk.', 'kPQQQUk.', '.kQQQUk.', '.kQQQUUk', 'kPQQQQUk', 'kQQQQUUk', 'kwkwkwkk']
DARK = {'P': 'Q', 'Q': 'U', 'U': 'l', 'w': 'P'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
LEG_N = ['........'] + LEG[1:]       # 手前の 足：上の 輪郭を けして 胴に なじませる
# ---- しっぽ：うろこの 段、先に ほのお ----
def tail(sw=0):
    g = G(64, 64)
    tube(g, [(16, 47), (11, 50), (9 + sw, 47), (9 + sw, 42)], [4, 3, 2.2, 1.6], SKIN)
    for (x, y) in ((12, 46), (10, 47), (8 + sw, 44)): dots(g, 'U', [(x, y)]); dots(g, 'P', [(x, y - 1)])
    g = ol(g)
    fl = ['..k..', '.kOk.', 'kOYOk', 'kYwYk', '.kYk.'] if not sw else ['.k...', '.kOk.', 'kOYOk', 'kYwYk', '.kYk.']
    stamp(g, fl, 7 + sw, 36)
    return g
# ---- 唐草の 布（たてがみ）：頭の 後ろから 背中へ。すそは ほのお ----
def cloth(ph=0):
    g = G(64, 64)
    poly(g, [(30, 14), (38, 22), (40, 38), (35, 46), (24, 47), (13, 45), (11, 40), (17, 30), (24, 20)], 'H')
    edge(g, {'H': CLOTH}, 2, 2, 2, 2)
    # 白い 唐草（うずまき）を 手で 置く
    SW = ['.ww.', 'w..w', 'w.ww', '.w..']
    for (x, y) in ((19, 34), (27, 28), (29, 38), (21, 41)):
        for j, r in enumerate(SW):
            for i, c in enumerate(r):
                if c == 'w' and g[y + j][x + i] != '.': g[y + j][x + i] = 'w'
    # すその ひだ
    for (x, y) in ((16, 44), (22, 46), (29, 46), (35, 44)):
        dots(g, 'J', [(x, y), (x, y - 1), (x, y - 2)])
    g = ol(g)
    # 背の ほのお（布の 上で 燃える たてがみ）
    F1 = ['.....k.......k....', '....kRk.....kRk...', '.k..kOk..k..kOk...', 'kRk.kOYk.kRkkOYk..', 'kOk.kOYOkkOkROYk..',
          'kOYkROYOkROYOYOk.k', '.kOYOYYOkOYYYYOkkR', '.kOYYwYYOYYwYYOkRk', '..kOYYYYYYYYYOkOk.', '...kkOOOOOOOOkkk..']
    F2 = ['......k......k....', '.k..kRk.....kRk...', 'kRk.kOk..k..kOk...', 'kOk.kOYk.kRkkOYk.k', '.kOkkOYOkkOkROYkkR',
          '.kOYROYOkROYOYOkRk', '.kOYOYYOkOYYYYOkOk', '.kOYYwYYOYYwYYOkk.', '..kOYYYYYYYYYOkk..', '...kkOOOOOOOOkk...']
    stamp(g, F2 if ph else F1, 15, 10)
    return g

# ---- 獅子舞の 頭（見せ所）：朱ぬりの 長い 口、金の 歯、ぎょろりと した 金の 目、黒い まゆ ----
def head(gape=0):
    g = G(64, 64)
    ball(g, 36, 24, 9, 9, RED)                                        # 頭（あたま）
    up = G(64, 64); poly(up, [(37, 17), (55, 19), (59, 22), (59, 28), (37, 29)], 'S'); edge(up, {'S': RED}, 2, 1, 2, 1)
    stamp(g, R(up), 0, 0)
    ball(g, 56.5, 20.5, 3, 2.6, RED)                                   # はなの こぶ
    dots(g, 'l', [(57, 21), (58, 21)])                                 # はなの あな
    # 下あご（ひらく）
    lo = G(64, 64); poly(lo, [(34, 30 + gape), (56, 29 + gape), (55, 34 + gape), (42, 36 + gape), (33, 34 + gape)], 'S'); edge(lo, {'S': 'RST'}, 1, 1, 1, 1)
    # 口の 中（暗い）
    if gape:
        poly(g, [(38, 28), (57, 28), (56, 31 + gape), (37, 32 + gape)], 'T')
        for x in range(40, 56, 4): dots(g, 'l', [(x, 30 + gape // 2)])
    stamp(g, R(lo), 0, 0)
    g = ol(g)
    # 金の 歯（上は 下むき、下は 上むき）
    for x in range(39, 57, 3):
        dots(g, 'k', [(x - 1, 29), (x + 1, 29), (x - 1, 30), (x + 1, 30), (x, 31)]); dots(g, 'Y', [(x, 29)]); dots(g, 'O', [(x, 30)])
    for x in range(41, 55, 3):
        y = 29 + gape
        dots(g, 'k', [(x - 1, y), (x + 1, y), (x, y - 1)]); dots(g, 'Y', [(x, y)])
    # 金の ふち どり（口の 上の 線）
    for x in range(38, 55): 
        if g[27][x] in 'RST': g[27][x] = 'O'
    for x in range(38, 55, 2):
        if g[26][x] in 'RST': g[26][x] = 'Y'
    # ほおの 金の うずまき
    dots(g, 'Y', [(31, 26), (32, 25), (33, 26), (32, 27)]); dots(g, 'O', [(31, 27), (33, 25)])
    return g
# 目（T：出目）：頭の 上へ 飛び出た 大きな 金の 目玉。まわりを 朱〜こげ赤の まぶたの 輪が かこみ、瞳は 前へ 寄った 小さな たての 切れ目
EYE_TOP = ['....kkkkk....', '..kkRRRRSkk..']
EYE_BOT = ['.kTTkkkkkTTk.', '..kkTTTTTkk..', '....kkkkk....']
EYE = EYE_TOP + ['.kRRkkkkkSSk.', '.kRkwwYYYkSk.', 'kRkwYYYYkYkTk', 'kSkYYYYYkOkTk', 'kSkYYYYOkOkTk', '.kTkOYOOOkTk.'] + EYE_BOT
EYE_ALT = {'blink': EYE_TOP + ['.kRRRRRRRSSk.', '.kRRRRRRSSSk.', 'kRRRSSSSSSSTk', 'kSSSSSSSSSSTk', 'kkkkkkkkkkkkk', '.kTTTTTTTTTk.'] + EYE_BOT,
           'hit': EYE_TOP + ['.kRRRRRRRSSk.', '.kRRSSSSSSSk.', 'kRkkkkkkkkkTk', 'kSkYYYYkYOkTk', 'kSkOYYYOOOkTk', '.kTkOOOOOkTk.'] + EYE_BOT,
           'atk0|atk1|atk2': EYE_TOP + ['.kRRkkkkkSSk.', '.kRkwwwwYkSk.', 'kRkwwYYYkwkTk', 'kSkwYYYYkYkTk', 'kSkYYYYYkYkTk', '.kTkOYYYOkTk.'] + EYE_BOT,
           'ko': EYE_TOP + ['.kRRkkkkkSSk.', '.kRkkYYYkkSk.', 'kRkYYkYkYYkTk', 'kSkYYYkYYOkTk', 'kSkYYkOkOOkTk', '.kTkkOOOkkTk.'] + EYE_BOT}
# 火の 粉（攻撃）
def fire(ph):
    g = G(80, 64)
    pts = [(60, 24, 2), (62, 30, 3), (60, 35, 2)] if ph == 0 else [(63, 22, 3), (66, 29, 3), (62, 36, 2), (68, 33, 1)]
    for (x, y, r) in pts: ball(g, x, y, r, r, 'YOS')
    for (x, y, r) in pts: dots(g, 'w', [(x - 1, y - 1)])
    return ol(g)
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='legFF', g='legB', x=34, y=51, rows=dark(LEG)),
        dict(n='legFH', g='legA', x=12, y=51, rows=dark(LEG)),
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(1)}),
        L('body', 'body', body()),
        dict(n='legH', g='legA', x=17, y=51, rows=LEG_N),
        dict(n='legF', g='legB', x=37, y=51, rows=LEG_N),
        L('cloth', 'mane', cloth(), alt={'idle1|idle3|walk1|walk3|atk1': cloth(1)}),
        L('head', 'head', head(), alt={'atk0': head(1), NB: head(5)}),
        dict(n='eye', g='head', x=32, y=9, rows=EYE, alt=EYE_ALT),
        L('fire', 'fx', fire(0), alt={'atk2': fire(1)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'head': (0, 1), 'body': (0, 1), 'mane': (0, 1)}, 'idle3': {'mane': (0, 0)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1), 'mane': (0, -1), 'head': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1), 'mane': (0, -1)},
    'atk0': {'head': (-2, -1), 'mane': (-1, 0), 'body': (-1, 1)}, 'atk1': {'root': (4, 0), 'head': (2, -2)}, 'atk2': {'root': (6, 0), 'head': (2, 0), 'fx': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'root', 'mane': 'root', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
