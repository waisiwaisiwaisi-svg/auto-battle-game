# イバラジャ（フェアリー・どく × ヘビ）手打ち GBA風・デフォルメ（2〜3頭身：大きな バラの 頭、胴は 短く まるく とぐろ）
META = dict(id='ibaraja', name='イバラジャ', types=['fairy', 'poison'], base='ヘビ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1630',
    'F': '#b6e25e', 'G': '#5ea23e', 'H': '#2a5c30',          # いばらの 茎（胴）
    'P': '#ffa6cf', 'Q': '#e2457f', 'R': '#8e1c4e',          # バラの 花びら
    'V': '#d48af4', 'U': '#7a34a8',                          # 毒
    'Y': '#fff27a', 'O': '#e88a1c',                          # 目（虹彩 明・暗）
    'w': '#ffffff',
}
LIGHT = set('FPVYw')
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

STEM = 'FGH'; PET = 'PQR'
# ---- とぐろ（胴）：小さく まるく 2段。外がわに いばらの とげ ----
def coil(dy=0, dx=0):
    g = G(64, 64)
    ball(g, 30 + dx, 53 + dy, 17, 7, STEM)                 # 下の 段
    ball(g, 31 + dx, 45 + dy, 12, 5.5, STEM)               # 上の 段
    # 段の かさなり：上の 段の 下に 影の 線
    for x in range(20 + dx, 43 + dx):
        y = int(45 + dy + 5.5 * (1 - ((x + .5 - 31 - dx) / 12) ** 2) ** .5) if abs(x + .5 - 31 - dx) < 12 else None
        if y and g[y][x] != '.': g[y][x] = 'H'
        if y and g[y + 1][x] != '.': g[y + 1][x] = 'l'
    # 茎の ふし（たての すじ）
    for x, y in ((16, 52), (24, 55), (36, 56), (44, 52), (24, 45), (37, 46)):
        x += dx; y += dy
        if g[y][x] != '.': g[y][x] = 'H'; g[y + 1][x] = 'H'
    g = ol(g)
    # とげ（赤むらさきの 三角）を 外へ
    for (x, y, d) in ((13, 49, 'l'), (18, 46, 'u'), (24, 40, 'u'), (38, 40, 'u'), (44, 45, 'u'), (47, 50, 'r'), (11, 55, 'l')):
        x += dx; y += dy
        if d == 'u': dots(g, 'k', [(x - 2, y), (x + 2, y), (x - 2, y - 1), (x + 2, y - 1), (x - 1, y - 2), (x + 1, y - 2), (x - 1, y - 3), (x + 1, y - 3), (x, y - 4)]); dots(g, 'R', [(x - 1, y), (x - 1, y - 1), (x, y), (x + 1, y), (x + 1, y - 1)]); dots(g, 'Q', [(x, y - 1), (x, y - 2)]); dots(g, 'P', [(x, y - 3)])
        if d == 'l': dots(g, 'k', [(x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x - 3, y), (x - 2, y - 1), (x - 2, y + 1)]); dots(g, 'Q', [(x, y), (x - 1, y)]); dots(g, 'P', [(x - 2, y)])
        if d == 'r': dots(g, 'k', [(x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y + 1), (x + 3, y), (x + 2, y - 1), (x + 2, y + 1)]); dots(g, 'R', [(x, y), (x + 1, y)]); dots(g, 'Q', [(x + 2, y)])
    return g

# ---- しっぽ：後ろへ はね上がり、先に バラの つぼみ ----
def tail(sw=0):
    g = G(64, 64)
    tube(g, [(16, 54), (9, 52), (6 + sw, 46), (8 + sw, 41)], [3.2, 2.6, 2, 1.6], STEM)
    ball(g, 8.5 + sw, 38, 3, 3.6, PET)
    dots(g, 'R', [(8 + sw, 37), (9 + sw, 38)]); dots(g, 'P', [(7 + sw, 36)])
    dots(g, 'F', [(5 + sw, 41), (11 + sw, 41)])       # がく
    return ol(g)

# ---- 首：とぐろから 頭へ（ポーズごとに 道すじを かえる）----
def neck(hx=0, hy=0):
    g = G(64, 64)
    tube(g, [(31, 46), (32, 40), (34 + hx * .5, 34 + hy * .5), (37 + hx, 29 + hy)], [4.6, 4.2, 4, 4], STEM)
    for (x, y) in ((33, 42), (33, 38)): g[y][x] = 'H'
    g = ol(g)
    # 首の うしろの とげ
    for (x, y) in ((27, 40), (28 + int(hx * .3), 35 + int(hy * .3))):
        dots(g, 'k', [(x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x - 3, y), (x - 2, y - 1), (x - 2, y + 1)]); dots(g, 'Q', [(x, y), (x - 1, y)]); dots(g, 'P', [(x - 2, y)])
    return g

# ---- バラの 頭巾（見せ所）：まるい 花の 形に、花びらの ふち（濃い 線＋反った 明るい ふち）を 弧で 重ねる ----
import math
ARCS = [(.86, 195, 300), (.86, 315, 400), (.86, 60, 170), (.62, 150, 260), (.62, 280, 380), (.62, 20, 120),
        (.40, 230, 340), (.40, 0, 150), (.22, 120, 300)]
def bloom(open_=0, cx=27, cy=20, sx=1, sy=1, ramp=PET):
    g = G(64, 64); rx, ry = (12 + open_) * sx, (11 + open_) * sy
    L_, M_, D_ = ramp
    for i in range(7):                                   # 外の 花びらの こぶ（花の 形）
        t = math.radians(-90 + i * 360 / 7)
        ball(g, cx + math.cos(t) * rx * .82, cy + math.sin(t) * ry * .82, 5 * sx, 5 * sy, ramp, hi=.5, lo=-.2)
    ball(g, cx, cy, rx * .86, ry * .86, ramp, only=None, hi=.55, lo=-.25)
    for (r, a0, a1) in ARCS:
        for a in range(a0, a1, 2):
            t = math.radians(a); x, y = int(cx + .5 + math.cos(t) * rx * r), int(cy + .5 + math.sin(t) * ry * r)
            if g[y][x] == '.': continue
            g[y][x] = D_
            ox, oy = int(cx + .5 + math.cos(t) * (rx * r + 1.2)), int(cy + .5 + math.sin(t) * (ry * r + 1.2))
            if g[oy][ox] == M_ and math.sin(t) + math.cos(t) < .6: g[oy][ox] = L_
    dots(g, D_, [(cx, cy), (cx + 1, cy), (cx, cy - 1)]); dots(g, 'l', [(cx + 1, cy + 1)])
    return ol(g)

# ---- がく（首の まわりの 葉の えり）----
def sepal():
    g = G(64, 64)
    for pts in (((26, 29), (31, 28), (24, 36)), ((31, 29), (36, 28), (38, 36)), ((20, 26), (27, 29), (16, 33))):
        poly(g, pts, 'G')
    edge(g, {'G': STEM}, 1, 1, 1, 1)
    return ol(g)

# ---- ヘビの 頭（横向き、つり目、毒牙）----
HEAD = [
    '.........kkkk.............',
    '......kkkFFFFkkk..........',
    '....kkFFFGGGGGGGkkkk......',
    '...kFFGGGGGGGGGGGGGGkkk...',
    '..kFGGGGGGGGGGGGGGGGGGGkk.',
    '.kFGGGGGGGGGGGGGGGGGGGGGGk',
    'kFGGGGGGGGGGGGGGGGGGGGkGGk',
    'kGGGGGGGGGGGGGGGGGGGGGGGHk',
    'kGGGGGGGGGGGGGGGGGGGGGGHHk',
    'kGGGGGGGGGGkkkkkkkkkkkkkkk',
    'kHGGGGGGGkkwkkkkkkkkkwk.k.',
    'kHGGGGGGkFFwFFFFFFFFFwk...',
    '.kHGGGGGGkFFFFFFFFFFFk....',
    '..kHHGGGGGkkHHHHHHHkk.....',
    '...kkkHHHHHHkkkkkkk.......',
    '......kkkkkk..............',
]
HEAD_OPEN = HEAD[:8] + [
    'kGGGGGGGGGGGGGGGGGGGGGGHHk',
    'kGGGGGGGGGkkkkkkkkkkkkkkkk',
    'kHGGGGGGkkwkkkkkkkkkwkkkk.',
    'kHGGGGGkRRwRRRRRRRRRwRk...',
    'kHGGGGGkRRUURRRRRRRRRk....',
    '.kHGGGGGkRRRRRRRRRRRk.....',
    '.kHHGGGGkwkkkkkkkwkk......',
    '..kkHHHGGFFFFFFFFFk.......',
    '....kkkkHHHHHHHHHkk.......',
    '........kkkkkkkkk.........',
]
# うろこの すじ（手打ち）
def head(open_=False):
    rows = [list(r) for r in (HEAD_OPEN if open_ else HEAD)]
    for (x, y) in ((5, 6), (8, 4), (4, 9), (7, 8), (11, 7), (6, 11)):
        if rows[y][x] == 'G': rows[y][x] = 'H'
    return [''.join(r) for r in rows]
# 頭の 上の いばらの つの（後ろへ 反る）
HORN = ['kk.....', 'kQkk...', '.kQQkk.', '..kRQQk', '...kRRk', '....kk.']
# 目：白い 光＋金と だいだいの 虹彩＋たての ひとみ。まゆは 前へ 下がる（怒り）
EYE = ['kkk.....', '.kkkkkkk', '.kwYYkOk', '..kOOkkk']
EYE_ALT = {'blink': ['kkk.....', '.kkkkkkk', '.GGGGGGk', '..kkkkk.'], 'hit': ['..kk..k.', '.kGGkkG.', '.GkkGGkG', '..GGGGG.'],
           'atk0|atk1|atk2': ['kkk.....', '.kkkkkkk', '.kwwYkYk', '..kYOkOk']}
# 毒の しずく・毒の 霧（攻撃）
DRIP = ['kVk', 'kUk', '.k.']
def spray(ph):
    g = G(80, 64)
    pts = [(58, 25), (61, 23), (63, 26), (60, 28), (66, 24), (65, 29)] if ph == 0 else [(62, 22), (67, 26), (64, 30), (70, 23), (69, 29), (72, 26)]
    for (x, y) in pts:
        dots(g, 'V', [(x, y), (x + 1, y), (x, y + 1)]); dots(g, 'U', [(x + 1, y + 1)])
    return ol(g)
SPARK = ['.P.', 'PwP', '.P.']

NB = 'atk1|atk2'
def layers():
    hx, hy = 0, 0
    return [
        L('tail', 'tail', tail(), alt={'idle1|idle3|walk1|walk3': tail(1)}),
        L('coil', 'body', coil()),
        L('neck', 'neck', neck(), alt={'atk0': neck(-3, 1), NB: neck(6, 2), 'hit': neck(-3, -1)}, not_='ko'),
        L('bloom', 'head', bloom(), alt={'atk0|atk1|atk2': bloom(1)}, not_='ko'),
        L('sepal', 'head', sepal(), not_='ko'),
        dict(n='horn', g='head', x=30, y=10, rows=HORN, not_='ko'),
        dict(n='head', g='head', x=33, y=13, rows=head(), alt={NB: head(True)}, not_='ko'),
        dict(n='eye', g='head', x=41, y=15, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='drip', g='head', x=53, y=26, rows=DRIP, only='idle0|idle1|idle2|idle3|blink|walk0|walk1|walk2|walk3'),
        L('spray', 'fx', spray(0), alt={'atk2': spray(1)}, only=NB),
        dict(n='sp1', g='fx', x=14, y=7, rows=SPARK, only='idle1|idle3|walk1'),
        dict(n='sp2', g='fx', x=40, y=4, rows=SPARK, only='idle0|idle2|walk3'),
        # ダウン：花が しおれて 地面に 落ちた 頭
        L('koneck', 'body', neck_ko(), only='ko'),
        L('kobloom', 'body', bloom_ko(), only='ko'),
        dict(n='kohead', g='body', x=36, y=45, rows=head(), only='ko'),
        dict(n='koeye', g='body', x=46, y=49, rows=['kGk', 'GkG', 'kGk'], only='ko'),
    ]
def neck_ko():
    g = G(64, 64); tube(g, [(31, 46), (34, 48), (38, 52)], [4.6, 4.2, 4], STEM); return ol(g)
def bloom_ko(): return bloom(0, 33, 51, 1, .62, 'QQR')
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'neck': (0, 0)}, 'idle2': {'head': (0, 1), 'body': (0, 0)}, 'idle3': {'head': (0, 0)}, 'blink': {},
    'walk0': {'body': (1, 0), 'head': (0, -1)}, 'walk1': {'head': (0, 0), 'tail': (-1, 0)},
    'walk2': {'body': (-1, 0), 'head': (0, -1)}, 'walk3': {'tail': (1, 0)},
    'atk0': {'head': (-3, 1)}, 'atk1': {'head': (6, 2), 'fx': (0, 0)}, 'atk2': {'head': (6, 2), 'fx': (2, 0)},
    'hit': {'head': (-3, -1), 'root': (-2, 0)}, 'ko': {},
}
PARENT = {'head': 'root', 'neck': 'body', 'tail': 'body', 'body': 'root', 'fx': 'root'}
