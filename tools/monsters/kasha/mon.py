# カシャ（ほのお・あく × 猫）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きめ、胴は 小さく 丸く、足は 短く 太く）
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
    E = GLOW[mode] if big == 'glow' else (EYES_BIG if big else EYES)[mode]
    for j, r in enumerate(E):
        for i, c in enumerate(r):
            if c == '.': continue
            put(g, x + i, y + j, {'A': A, 'B': B}.get(c, c))
    return g
# 目（E：光る目・瞳なし）：炎の 黄と だいだいの 発光＋白い 芯。黒い 輪郭は なく、まわりに 1ドットの 赤い にじみ（光の ふち）。後ろ上へ 火の 粉の 尾
GLOW_XY = (41, 28)
GLOW = {
    'idle':  ['R.........', 'RORR......', '.ROYORRR..', '.RYwwYYOR.', '..RYYYOR..', '...RRRR...'],
    'atk':   ['RR........', 'ROORRR....', 'RYYYYOORR.', '.RYwwwYYOR', '.RYwwYYOR.', '..RRYYRR..', '....RR....'],
    'blink': ['R.........', 'R.........', '.RRRRRR...', '.ROOOOORR.', '..RRRRRR..', '..........'],
    'hit':   ['R.........', 'RRR.......', '.ROR.RRR..', '.RwR.ROR..', '..RR..RR..', '..........'],
    'ko':    ['..........', '.r...r....', '..r.r.....', '...r......', '..r.r.....', '.r...r....'],
}
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='kasha', name='カシャ', types=['fire', 'dark'], base='猫', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1630',
    'A': '#9886b0', 'B': '#5c4a78', 'D': '#2e2244',      # 毛（闇の 黒紫）
    'Y': '#ffe65a', 'O': '#ff8a1e', 'R': '#d8341c', 'r': '#6e1420',   # 炎・熾火
    'S': '#c8c0cc', 's': '#6c6274',                      # 車輪の 鉄
    'w': '#ffffff', 'p': '#e86a8a',                      # 牙・爪／口の 中
}
LIGHT = set('AYOSw')
KEEP_BLACK = set('wYO')
FUR = {'1': 'ABD'}
FUR_BACK = {'1': 'BDD'}

RC = (16.5, 33.5); RO, RI = 10.5, 5.5      # 尾の 輪（車輪）＝見せ所

# ---------- 尾：丸めて 輪に した 燃える 車輪。輪の 中に 鉄の 輻（や）、外へ 炎 ----------
def flames(phase):
    p = G()
    for i in range(10):
        a = i * 36 + phase * 18 + 10
        if 230 < a % 360 < 320: continue                       # 下（胴の 後ろ）は 炎を 引く
        ln = 4 + (2 if i % 2 else 0)
        pts, rad = [], []
        for j in range(5):
            t = j / 4; rr = RO - 1.5 + ln * t; aa = math.radians(a + 34 * t)    # 回る 向きと 逆へ なびく
            pts.append((RC[0] + rr * math.cos(aa), RC[1] - rr * math.sin(aa))); rad.append(2.4 * (1 - t) + .4)
        tube(p, pts, rad, 'F')
    for y in range(64):
        for x in range(64):
            if p[y][x] == 'F':
                d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
                p[y][x] = 'Y' if d < RO + 1.3 else 'O' if d < RO + 3.3 else 'R'
    g = ink(p); swap(g, {'k': 'r'})
    return g
def wheel(spin):
    p = G(); disc(p, RC[0], RC[1], RO, RO, '1')
    tube(p, [(24, 50), (17, 51), (11, 48), (8, 42)], [3.2, 3, 2.8, 2.8], '1')       # 尾の つけね（胴の 中から）→ 輪へ
    s = shade(p, FUR, r=2, tilt=.5)
    for y in range(64):
        for x in range(64):
            if math.hypot(x + .5 - RC[0], y + .5 - RC[1]) < RI: s[y][x] = '.'
    g = ink(s)
    for y in range(64):                                         # 輪の 中：燃える 芯
        for x in range(64):
            d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
            if d < RI - .6: g[y][x] = 'Y' if d < RI - 3.2 else 'O' if d < RI - 1.8 else 'R'
    cx, cy = RC[0] - .5, RC[1] - .5
    for a in ((0, 90, 180, 270) if spin == 0 else (45, 135, 225, 315)):       # 鉄の 輻（4本）
        line(g, round(cx), round(cy), round(cx + 4.6 * math.cos(math.radians(a))), round(cy - 4.6 * math.sin(math.radians(a))), 'S')
    hx, hy = round(cx), round(cy)
    for (x, y, c) in ((0, 0, 'w'), (-1, 0, 's'), (1, 0, 's'), (0, -1, 's'), (0, 1, 's')): put(g, hx + x, hy + y, c)
    for y in range(64):                                         # 輪の ふち：鉄の たが＋毛の すじ
        for x in range(64):
            d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
            if RI <= d < RI + 1.3 and g[y][x] in 'ABDk': g[y][x] = 'S' if (x < RC[0] and y < RC[1] + 1) else 's'
            if RO - 1.2 <= d < RO and g[y][x] in 'ABD' and (x + y) % 4 == 0: g[y][x] = 'S' if x + 3 < RC[0] + (RC[1] - y) else 's'
    for a in range(15, 360, 30):
        x, y = round(RC[0] + 8 * math.cos(math.radians(a)) - .5), round(RC[1] - 8 * math.sin(math.radians(a)) - .5)
        if g[y][x] in 'AB': g[y][x] = 'D' if g[y][x] == 'B' else 'B'
    return g

# ---------- 胴：小さく 丸い。背の 毛が 逆立つ ----------
def body(arch=0):
    p = G(); disc(p, 30, 47.5 - arch, 11, 6.8)
    s = shade(p, FUR, r=3, tilt=.6); g = ink(s)
    for (x, y) in ((20, 40 - arch), (24, 38 - arch), (28, 38 - arch)):            # 逆立つ 毛
        stamp(g, ['..k', '.kA', 'kAB', 'kBB'], x, y)
    dots(g, 'r', [(25, 45 - arch), (26, 46 - arch), (27, 46 - arch), (23, 49 - arch), (24, 50 - arch)])   # 熾火の しま
    dots(g, 'R', [(26, 45 - arch), (24, 49 - arch)])
    return g

# ---------- 足：短く 太く、大きな 前足に 爪 ----------
def leg(x, back, dx=0, lift=0, claws=True):
    def f(p):
        tube(p, [(x, 48), (x + dx * .5, 55 - lift), (x + dx, 58 - lift)], [3.6, 3.2, 3.0])
        disc(p, x + dx + 1.2, 58.6 - lift, 4.2, 2.6)
        if x < 30: disc(p, x - .5, 50, 4.6, 4.2)                     # 後ろ足の もも                  # 足先
    g = part(f, FUR_BACK if back else FUR, r=1, tilt=.3, skip=lambda X, Y: Y < 46)
    fx, fy = round(x + dx + 1.2), round(58.6 - lift)
    if claws:
        dots(g, 'w', [(fx + 4, fy + 1), (fx + 2, fy + 2)] if not back else [(fx + 4, fy + 1)])
        dots(g, 'k', [(fx + 1, fy), (fx + 3, fy)])
    return g

# ---------- 頭：大きな だ円＋口先・耳・ほおの 毛の 房。目・口・牙は 手で ----------
def head(mode='idle'):
    def f(p):
        disc(p, 42.5, 33, 10.5, 8.5); disc(p, 50.5, 36.5, 5, 3.6)
        poly(p, [(34, 29), (35.5, 19), (42, 26)], '1')      # 奥の 耳
        poly(p, [(42, 26), (47.5, 18.5), (51, 29)], '1')    # 手前の 耳
        poly(p, [(34, 36), (29, 39), (33, 40), (31, 43), (37, 42)], '1')   # ほおの 毛の 房
    g = part(f, FUR, r=2, tilt=.5)
    dots(g, 'r', [(36, 23), (36, 24), (37, 24), (37, 25), (38, 25), (36, 25)]); dots(g, 'R', [(36, 22), (37, 23)])          # 耳の 中（熾火）
    dots(g, 'r', [(47, 22), (47, 23), (48, 23), (47, 24), (48, 24), (48, 25), (46, 25)]); dots(g, 'R', [(47, 21), (46, 24)])
    dots(g, 'R', [(36, 30), (37, 31), (35, 33), (36, 34), (37, 34)]); dots(g, 'O', [(36, 31), (35, 34)])   # くまどり
    eye(g, GLOW_XY[0], GLOW_XY[1], mode, big='glow')
    stamp(g, ['kk', 'kD'], 55, 34)                     # 鼻
    if mode == 'atk':                                  # シャーッ：大きく 開いた 口と 上下の 牙
        cut(g, (46, 40, 56, 43))
        stamp(g, ['kkkkkkkkkk', 'kwkpppkwkk', 'kwppppppwk', 'kppppppppk', 'kwkpppkwk.', '.kkkkkkkk.'], 46, 38)
    elif mode in ('ko', 'hit'):
        for x, y in ((47, 39), (48, 39), (49, 40), (50, 40), (51, 39), (52, 40), (53, 40), (54, 39)): put(g, x, y, 'k')
    else:                                              # とじた 口から 牙が のぞく
        for x, y in ((46, 38), (47, 39), (48, 39), (49, 39), (50, 39), (51, 39), (52, 39), (53, 38), (54, 38)): put(g, x, y, 'k')
        dots(g, 'w', [(49, 40), (49, 41), (52, 40), (52, 41)]); dots(g, 'k', [(48, 40), (48, 41), (50, 41), (49, 42), (51, 40), (53, 41), (52, 42)])
    return g

# ---------- 爪の ひと振り（炎の 3本の 弧）：エフェクトなので はなれていて よい ----------
SLASH = [
    '.......kkk..',
    '....kkkRYk..',
    '..kkROYYk...',
    '.kROYYkk.kk.',
    'kROYkk.kkRYk',
    'kRYk.kkROYk.',
    'kRk.kROYkk..',
    'kk.kROYk....',
    '...kRYk.....',
    '...kRk......',
    '...kk.......',
]

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    return [
        L('fl', 'tail', flames(0), alt={'idle1|idle3|walk1|walk3|atk1': rows_of(flames(1))}, not_='ko'),
        L('wheel', 'tail', wheel(0), alt={'idle2|idle3|walk1|walk3|atk1': rows_of(wheel(1))}),
        L('hb', 'legB', leg(29, True)),
        L('fb', 'legA', leg(37, True)),
        L('body', 'body', body(), alt={'atk0': rows_of(body(1))}),
        L('hf', 'legA', leg(23, False)),
        L('ff', 'legB', leg(40, False), alt={'atk1|atk2': rows_of(leg(40, False, 4, 3))}),
        L('head', 'head', head(), y=2, alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        dict(n='slash', g='root', x=51, y=40, rows=SLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 0), 'tail': (0, -1), 'legA': (-1, 0), 'legB': (-1, 0)},
    'atk1': {'root': (4, -1)},
    'atk2': {'root': (3, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'tail': (1, 1)},
    'ko': {'body': (0, 6), 'head': (3, 7), 'tail': (-2, 2)},
}
EYE_BOX = (41, 30, 10, 6)
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
