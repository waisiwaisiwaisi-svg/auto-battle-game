# ライジュウ（でんき・ノーマル × ハクビシン）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きめ、胴は 小さく 丸く、足は 短く 太く）
# ===KIT=== 下書きの 道具（あたりを とって 3段の 陰影 → 目・牙・模様は 手で 打つ）
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def put(g, x, y, ch):
    if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def dots(g, ch, pts):
    for x, y in pts: put(g, x, y, ch)
def disc(p, cx, cy, rx, ry=None, ch='1'):
    ry = ry or rx
    for y in range(64):
        for x in range(64):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: p[y][x] = ch
def tube(p, path, rad, ch='1'):
    """道すじに そって 丸い 管を ぬる（太さは 点ごとに 指定）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: put(p, x, y, ch)
def shade(p, ramps, r=2, hi=.3, lo=-.3, tilt=.35, rim=True):
    """光は 左上：ふくらみ＋全体の 斜めの かたむき → 明・中・暗。上と 左の ふちは 明、右下の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    pts = [(x, y) for y in range(64) for x in range(64) if p[y][x] in ramps]
    if not pts: return [row[:] for row in p]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    cx, cy, w, h = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(4, max(xs) - min(xs)), max(4, max(ys) - min(ys))
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for x, y in pts:
        c = p[y][x]; hc, mc, dc = ramps[c]
        v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 - tilt * ((x - cx) / w * 1.2 + (y - cy) / h * 1.6)
        t = hc if v > hi else dc if v < lo else mc
        if rim:
            ul = at(p, x - 1, y) == '.' or at(p, x, y - 1) == '.'
            dr = at(p, x + 1, y) == '.' or at(p, x, y + 1) == '.'
            if ul and not dr and v > lo: t = hc
            elif dr and not ul: t = dc
        out[y][x] = t
    return out
def ink(p, g=None, skip=None):
    """まわりに 黒の 輪郭。skip(x, y) が 真の ところは 線を 引かない（付け根を 胴に なじませる）"""
    g = g or G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                if not (skip and skip(x, y)): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
    return g
def swap(g, mapping, box=None):
    x0, y0, x1, y1 = box or (0, 0, 63, 63)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if g[y][x] in mapping: g[y][x] = mapping[g[y][x]]
    return g
def cut(g, box):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): put(g, x, y, '.')
    return g
def L(n, grp, g, x=0, y=0, **kw): return dict(n=n, g=grp, x=x, y=y, rows=rows_of(g) if isinstance(g[0], list) else g, **kw)
def part(paint_fn, ramps, r=2, tilt=.4, skip=None, **kw):
    p = G(); paint_fn(p); return ink(shade(p, ramps, r=r, tilt=tilt, **kw), skip=skip)
def stack(*gs):
    g = G()
    for h in gs:
        for y in range(64):
            for x in range(64):
                if h[y][x] != '.': g[y][x] = h[y][x]
    return g
def fallen(g, cw=True, ground=61, cx=32):
    """ダウン用：全身を 90度 たおして 地面に のせる（90度 回転は 可）"""
    r = G()
    for y in range(64):
        for x in range(64): r[y][x] = g[63 - x][y] if cw else g[x][63 - y]
    pts = [(x, y) for y in range(64) for x in range(64) if r[y][x] != '.']
    x0, x1, y1 = min(p[0] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)
    out = G(); dx, dy = cx - (x0 + x1) // 2, ground - y1
    for x, y in pts: put(out, x + dx, y + dy, r[y][x])
    return out
# ---- するどい 目（右向き）：まゆ／上まぶたの 線＋白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ＋下まぶた ----
EYES = {
    'idle':  ['kk.....', '.kkkkk.', '.kwAkkk', '.kABkBk', '..kkkk.'],
    'atk':   ['kk.....', '.kkkkkk', '.kwwAkA', '.kAABkk', '..kkkk.'],
    'blink': ['kk.....', '.kkkkk.', '.......', '.kkkkkk', '.......'],
    'hit':   ['k......', '.kkk...', '....kkk', '.kkk...', '.......'],
    'ko':    ['.......', '.k...k.', '..k.k..', '...k...', '..k.k..', '.k...k.'],
}
EYES_BIG = {
    'idle':  ['kkk.....', '.kkkkkk.', '.kwAAkkk', '.kAABkBk', '..kBBkk.', '...kkk..'],
    'atk':   ['kkk.....', '.kkkkkkk', '.kwwAAkA', '.kwAABkk', '..kABkk.', '...kkk..'],
    'blink': ['kkk.....', '.kkkkkk.', '........', '.kkkkkkk', '........', '........'],
    'hit':   ['kk......', '.kkkk...', '.....kkk', '..kkkk..', '........', '........'],
    'ko':    ['........', '.k....k.', '..k..k..', '...kk...', '..k..k..', '.k....k.'],
}
def eye(g, x, y, mode='idle', A='Y', B='O', big=False):
    E = (EYES_BIG if big else EYES)[mode]
    for j, r in enumerate(E):
        for i, c in enumerate(r):
            if c == '.': continue
            put(g, x + i, y + j, {'A': A, 'B': B}.get(c, c))
    return g
# 目（L）の 差しかえ：とじ・被弾・ダウンは 黒い 仮面の 上でも 見える 明るい 毛の 色で かく
RAI_EYE = {
    'idle':  ['kk.........', '.kkkkkkkk..', '..kwYYYkOk.', '..kYYOOkOk.', '...kkkkkk..'],
    'atk':   ['kk.........', '.kkkkkkkk..', '..kwwYYkYk.', '..kwYYOkOk.', '...kkkkkk..'],
    'blink': ['kk.........', '.kkkkkkkk..', '...BBBBBB..', '...........', '...........'],
    'hit':   ['...........', '...AA......', '.....AA....', '.......AA..', '.....AA....', '...AA......'],
    'ko':    ['...........', '...A...A...', '....A.A....', '.....A.....', '....A.A....', '...A...A...'],
}
def put_rows(g, x, y, rows):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.': put(g, x + i, y + j, c)
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='raijuu', name='ライジュウ', types=['elec', 'normal'], base='ハクビシン', size='M')
EYE_BOX = (35, 31, 15, 7)   # 目の 位置（idle0 の 64x64 座標）
PAL = {
    'k': '#101018', 'l': '#3a2c2a',
    'A': '#cbbca4', 'B': '#8e7c68', 'D': '#54463e',      # 毛（灰茶）
    'M': '#2c2428',                                      # 顔の 黒い 隈どり
    'Y': '#fff27a', 'O': '#f2b21c', 'E': '#a0600e',      # 稲妻
    'C': '#a8f4ff',                                      # 電光の 青白い 芯
    'w': '#ffffff', 'p': '#d84e66',                      # 牙・爪・白い すじ／口の 中
}
LIGHT = set('AYCw')
KEEP_BLACK = set('wYC')
FUR = {'1': 'ABD'}
FUR_BACK = {'1': 'BDD'}

# ---------- 尾＝稲妻（ぎざぎざの 太い 帯）：見せ所 ----------
BOLT = [(23, 47), (12, 41), (19, 35), (6, 27), (14, 23), (3, 9)]
BW = [3.2, 3.4, 3.4, 3.0, 2.6, 0.4]
def bolt(ph=0):
    p = G()
    pts = [(x + (ph if i >= 2 else 0), y) for i, (x, y) in enumerate(BOLT)]
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]; dx, dy = x1 - x0, y1 - y0; n = math.hypot(dx, dy); nx, ny = -dy / n, dx / n
        w0, w1 = BW[i], BW[i + 1]
        poly(p, [(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)], '2')
        if i + 1 < len(pts) - 1: disc(p, x1, y1, w1 + .3, w1 + .3, '2')
    tube(p, [(25, 47), (18, 45)], [3.4, 3.2], '1')               # 毛の 付け根（胴の 中から）
    s = shade(p, {'1': 'ABD', '2': 'YOE'}, r=1, tilt=.6, hi=.15, lo=-.25)
    for i in range(1, len(pts) - 2):                              # 帯の 中心に 青白い 芯
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        for t in range(0, 11):
            x, y = round(x0 + (x1 - x0) * t / 10 - .5), round(y0 + (y1 - y0) * t / 10 - .5)
            if at(s, x, y) in 'YOE': put(s, x, y, 'C' if (t + ph) % 3 else 'w')
    g = ink(s)
    return g
SPARK = [['..k..', '.kYk.', 'kYwYk', '.kYk.', '..k..'], ['k...k', '.kYk.', '.YwY.', '.kYk.', 'k...k']]

# ---------- 胴：小さく 丸い。全身の 毛が 逆立つ ----------
def body(arch=0):
    p = G(); disc(p, 30, 47.5 - arch, 11, 6.8)
    for i, x in enumerate((21, 25, 29, 33)):                     # 背の 逆立つ 毛（ぎざぎざ）
        poly(p, [(x - 2, 43 - arch), (x - 1.5 - i * .3, 36.5 - arch), (x + 2.5, 42 - arch)], '1')
    s = shade(p, FUR, r=2, tilt=.6); g = ink(s)
    dots(g, 'D', [(34, 50), (35, 49), (36, 50), (24, 50), (25, 51)])
    return g

# ---------- 足：短く 太く、黄色く 光る 爪 ----------
def leg(x, back, dx=0, lift=0):
    def f(p):
        tube(p, [(x, 48), (x + dx * .5, 55 - lift), (x + dx, 58 - lift)], [3.6, 3.2, 3.0])
        disc(p, x + dx + 1.2, 58.6 - lift, 4.2, 2.6)
        if x < 30: disc(p, x - .5, 50, 4.6, 4.2)                     # 後ろ足の もも
    g = part(f, FUR_BACK if back else FUR, r=1, tilt=.3, skip=lambda X, Y: Y < 46)
    fx, fy = round(x + dx + 1.2), round(58.6 - lift)
    dots(g, 'k', [(fx + 1, fy), (fx + 3, fy)])
    dots(g, 'Y', [(fx + 4, fy + 1), (fx + 4, fy)]); dots(g, 'k', [(fx + 5, fy + 1)])
    if not back: dots(g, 'Y', [(fx + 2, fy + 2)])
    return g

# ---------- 頭：だ円＋長めの 口先・小さな 丸耳・逆立つ 頭の 毛。白い すじと 黒い 隈どりは 手で ----------
def head(mode='idle'):
    def f(p):
        disc(p, 41.5, 33, 10.5, 8.5); disc(p, 51.5, 36.8, 6.5, 3.6)
        disc(p, 36, 25.5, 3.4, 3.4)                              # 耳（丸く 小さい）
        for (x0, x1, tx, ty) in ((37, 42, 38, 19), (41, 46, 44, 19.5), (45, 49.5, 49, 22)):   # 逆立つ 頭の 毛
            poly(p, [(x0, 27), (tx, ty), (x1, 27)], '1')
        poly(p, [(33, 35), (27, 37), (32, 39), (28, 42), (35, 42)], '1')    # ほおの 毛の 房（ぎざぎざ）
    g = part(f, FUR, r=2, tilt=.5)
    dots(g, 'D', [(35, 24), (36, 24), (35, 25), (36, 25), (35, 26)]); dots(g, 'p', [(36, 25)])   # 耳の 中
    for x, y in ((40, 26), (41, 26), (42, 27), (43, 27), (44, 28), (45, 28), (46, 29), (47, 29), (48, 30), (49, 30), (50, 31),
                 (51, 31), (52, 32), (53, 32), (54, 33), (55, 33)):  # 額から 鼻への 白い すじ（ハクビシン）
        if at(g, x, y) in 'ABD': put(g, x, y, 'w')
    for x, y in ((40, 25), (41, 25), (42, 26), (43, 26), (44, 27), (45, 27)):
        if at(g, x, y) in 'ABD': put(g, x, y, 'A')
    # 目（L：隈取り）：ハクビシンの 黒い 仮面。後ろから 前へ 下がる 帯で 目を つつみ、下に 明るい 毛の ふち。中に 後ろが 上がった 細い つり目（黄）
    for x in range(35, 50):
        t = 29.6 + (x - 35) * .12 + max(0, 38 - x) * .7; bt = 34.4 + (x - 35) * .05 - max(0, x - 46) * .9
        for y in range(28, 39):
            if t <= y <= bt and at(g, x, y) in 'ABD': put(g, x, y, 'M')
        yb = int(bt) + 1
        if at(g, x, yb) in 'BD' and x < 47: put(g, x, yb, 'A')
    put_rows(g, 39, 29, RAI_EYE[mode])
    stamp(g, ['kk', 'kM'], 57, 35)                     # 鼻
    dots(g, 'C', [(32, 38), (30, 41)])                 # ほおの 電気
    if mode == 'atk':
        cut(g, (47, 40, 58, 43))
        stamp(g, ['kkkkkkkkkkk', 'kwkpppkwkwk', 'kwppppppppk', 'kppppppppk.', 'kwkpppkwk..', '.kkkkkkkk..'], 47, 38)
    elif mode in ('ko', 'hit'):
        for x, y in ((47, 39), (48, 39), (49, 40), (50, 40), (51, 39), (52, 40), (53, 40), (54, 39), (55, 39)): put(g, x, y, 'k')
    else:
        for x, y in ((46, 38), (47, 39), (48, 39), (49, 39), (50, 39), (51, 39), (52, 39), (53, 39), (54, 38), (55, 38), (56, 38)): put(g, x, y, 'k')
        dots(g, 'w', [(48, 40), (48, 41), (53, 40), (53, 41)]); dots(g, 'k', [(47, 40), (47, 41), (49, 41), (48, 42), (52, 40), (54, 41), (53, 42)])
    return g

# ---------- 稲妻の 爪（攻撃の エフェクト：はなれていて よい）----------
CLAW = [
    '....kk..kk..',
    '...kYk.kYk..',
    '..kYOkkYOk..',
    '.kYOk.kYOk.k',
    'kYCk.kYCkkYk',
    '.kYOkkYOk.kO',
    '..kYOkkYOkYk',
    '...kYk.kYkYk',
    '..kYk.kYk.k.',
    '..kk..kk....',
]
CLAW2 = [
    '..k.....k...',
    '.kYk...kYk..',
    '..kYk...kYk.',
    '...k.....k..',
    'k.....k.....',
    '.k...kYk....',
    '..k...k....k',
]

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    B1 = rows_of(bolt(1))
    return [
        L('bolt', 'tail', bolt(0), alt={'idle1|idle3|walk1|walk3|atk1': B1, 'ko': swap(bolt(0), {'Y': 'O', 'O': 'E', 'C': 'O', 'w': 'Y'})}),
        dict(n='spark', g='tail', x=1, y=12, rows=SPARK[0], alt={'idle1|idle3|walk1|walk3|atk1': SPARK[1]}, not_='ko|hit'),
        L('hb', 'legB', leg(29, True)),
        L('fb', 'legA', leg(37, True)),
        L('body', 'body', body(), alt={'atk0': rows_of(body(1))}),
        L('hf', 'legA', leg(23, False)),
        L('ff', 'legB', leg(40, False), alt={'atk1|atk2': rows_of(leg(40, False, 4, 3))}),
        L('head', 'head', head(), y=2, alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        dict(n='claw', g='root', x=52, y=42, rows=CLAW, alt={'atk2': CLAW2}, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1)}, 'idle3': {'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 0), 'tail': (-1, -1), 'legA': (-1, 0), 'legB': (-1, 0)},
    'atk1': {'root': (4, -1)},
    'atk2': {'root': (3, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'tail': (1, 1)},
    'ko': {'body': (0, 6), 'head': (3, 7), 'tail': (-2, 2)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
