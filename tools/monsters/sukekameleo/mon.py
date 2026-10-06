# スケカメレオ（エスパー・ゴースト × カメレオン）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きめ、胴は 小さく 丸く、足は 短く）
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
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='sukekameleo', name='スケカメレオ', types=['psychic', 'ghost'], base='カメレオン', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1838',
    'A': '#a8eccc', 'B': '#52ae9c', 'D': '#2a6470',      # 皮（霊の 青みどり）
    'G': '#e2ecff', 'H': '#8e9cd2',                      # すけた 部分（霊体）
    'M': '#ff86dc', 'N': '#a42e9e',                      # 念の 渦（ピンク・紫）
    'Y': '#fff27a',                                      # 念の 光
    'w': '#ffffff', 'p': '#e0506e',                      # 光／舌・口の 中
}
LIGHT = set('AGMYw')
KEEP_BLACK = set('wY')
SKIN = {'1': 'ABD', '2': 'GHH'}

def ghostify(g, test):
    """霊体（すける ところ）：皮の 色を 青白く、市松に すかす"""
    for y in range(64):
        for x in range(64):
            if not test(x, y): continue
            c = g[y][x]
            if c in 'AB': g[y][x] = 'G' if (x + y) % 2 else 'H'
            elif c == 'D': g[y][x] = 'H' if (x + y) % 2 else '.'
            elif c in 'kl' and (x + y) % 2: g[y][x] = 'H'
    return g

# ---------- 尾＝催眠の 渦（見せ所）：くるりと 巻いた 尾に 念の しまが 走る ----------
SC = (12.5, 35.5)
def spiral_pts(ph=0):
    pts, rad = [(21, 47), (16, 46.5)], [3.2, 3.2]
    n = 22
    for i in range(n + 1):
        t = i / n; a = math.radians(95 + 520 * t); r = 10.2 - 7.4 * t
        pts.append((SC[0] + r * math.cos(a), SC[1] + r * math.sin(a))); rad.append(3.0 - 1.9 * t)
    return pts, rad
def tail(ph=0):
    pts, rad = spiral_pts()
    p = G(); tube(p, pts, rad, '1')
    s = shade(p, SKIN, r=2, tilt=.5)
    for i in range(2, len(pts) - 2):                 # 念の しま：線の まん中を 交互に ピンク／紫
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        c = 'M' if ((i + ph) // 3) % 2 == 0 else 'N'
        for u in range(4):
            x, y = x0 + (x1 - x0) * u / 4, y0 + (y1 - y0) * u / 4
            if at(s, round(x - .5), round(y - .5)) != '.': put(s, round(x - .5), round(y - .5), c)
    g = ink(s)
    ghostify(g, lambda x, y: x < 5 or y > 44 and x < 14)       # 尾の 外がわは すけている
    return g

# ---------- 胴：小さく 丸い、背に 小さな とさか。下半分が すける ----------
def body():
    def f(p):
        disc(p, 28, 46, 11, 7.5)
        for x in range(20, 36, 4): poly(p, [(x, 41), (x + 2, 37.5), (x + 4, 41)], '1')
    g = part(f, SKIN, r=2, tilt=.6)
    for x, y in ((24, 44), (25, 44), (29, 43), (30, 43), (33, 45), (34, 45)): put(g, x, y, 'N')     # 背の 念の もよう
    ghostify(g, lambda x, y: y > 50)
    return g

# ---------- 足：短く まがった 足に はさむ 指（2つに わかれた 足先）----------
def leg(x, back, dx=0, lift=0):
    def f(p):
        tube(p, [(x, 47), (x - 1, 53), (x + dx, 57 - lift)], [3, 2.6, 2.4])
        disc(p, x + dx - 1.5, 58.5 - lift, 2.4, 2); disc(p, x + dx + 2, 58.5 - lift, 2.4, 2)
    g = part(f, {'1': ('BDD' if back else 'ABD')}, r=1, tilt=.3, skip=lambda X, Y: Y < 48)
    put(g, round(x + dx), round(59 - lift), 'k')
    ghostify(g, lambda X, Y: Y > 54 and (X + Y) % 4 == 0)
    return g

# ---------- 頭：かぶとの 様な とさか、長い あご。目は 大きな 筒の 目（ぐるぐる 回る）----------
def head(mode='idle'):
    def f(p):
        disc(p, 42, 37, 10.5, 8); disc(p, 50.5, 39.5, 5.5, 3.6)
        poly(p, [(32.5, 35), (34.5, 22), (47, 31)], '1')          # かぶとの とさか
    g = part(f, SKIN, r=2, tilt=.5)
    for x, y in ((36, 26), (37, 28), (38, 30), (35, 29), (36, 31)): put(g, x, y, 'N')     # とさかの 念の もよう
    put(g, 36, 27, 'M'); put(g, 37, 29, 'M')
    if mode == 'atk':
        cut(g, (44, 41, 56, 44))
        stamp(g, ['kkkkkkkkkkkkk', 'kwpppppwpppk.', 'kppppppppk...', '.kkkkkkkk....'], 44, 40)
    else:
        for x, y in ((43, 40), (44, 41), (45, 42), (46, 42), (47, 42), (48, 42), (49, 42), (50, 42), (51, 41), (52, 41), (53, 41), (54, 40), (55, 40)): put(g, x, y, 'k')
        if mode != 'ko':                              # ぎざぎざの 歯
            dots(g, 'w', [(46, 43), (48, 43), (50, 43), (52, 42), (54, 41)]); dots(g, 'k', [(46, 44), (48, 44), (50, 44), (52, 43)])
    return g
# 筒の 目：皮の 筒（輪の すじ）＋まぶたの ひさし＋渦の 虹彩（M／N の 2色）＋ひとみ＋白い 光
TURRET = [
    '...kkkkk...',
    '..kAAAAAk..',
    '.kAkkkkkBk.',
    'kAk.....kDk',
    'kAk.....kDk',
    'kBk.....kDk',
    'kBk.....kDk',
    '.kBkkkkkDk.',
    '..kDDDDDk..',
    '...kkkkk...',
]
IRIS = {
    0: ['wNNNN', 'MMMMN', 'NNkMN', 'NMMMN', 'NNNNN'],
    1: ['wNNNN', 'NMMMN', 'NMkNN', 'NMMMM', 'NNNNN'],
    'blink': ['AAAAA', 'BBBBB', 'kkkkk', 'BBBBB', 'DDDDD'],
    'hit': ['kNNNk', 'NkNkN', 'NNkNN', 'NkNkN', 'kNNNk'],
    'ko': ['k...k', '.k.k.', '..k..', '.k.k.', 'k...k'],
    'atk': ['wwNNN', 'wMMMN', 'NNkMN', 'NMMMN', 'NNNNN'],
}
def turret(mode=0):
    t = [list(r) for r in TURRET]
    I = IRIS[mode]
    for j in range(5):
        for i in range(5):
            c = I[j][i]
            t[3 + j][3 + i] = {'.': 'G'}.get(c, c) if mode == 'ko' else c
    if mode == 'ko':
        for j in range(5):
            for i in range(5):
                if t[3 + j][3 + i] == 'G': t[3 + j][3 + i] = 'B'
    # 上の まぶた（するどい ひさし：前へ 下がる）
    for i, c in enumerate('kkkkkkkk'):
        if 2 + i < 11: t[2 + (i // 4)][1 + i] = 'k'
    return rows_of(t)

# ---------- 舌の 一撃（攻撃）：口から のびる 舌（つながっている）＋先に 念の 玉 ----------
def tongue(n):
    p = G()
    tube(p, [(52, 42.5), (52 + n, 42)], [1.4, 1.4], '5')
    disc(p, 53 + n, 42, 3, 3, '6')
    g = ink(p)
    swap(g, {'5': 'p', '6': 'M'})
    dots(g, 'w', [(52 + n, 41)]); dots(g, 'N', [(54 + n, 43), (55 + n, 42)])
    return g
RING = ['..kkkk..', '.kM..Mk.', 'kM....Mk', 'kM....Mk', '.kM..Mk.', '..kkkk..']

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    T = {m: turret(m) for m in (0, 1, 'blink', 'hit', 'ko', 'atk')}
    return [
        L('tail', 'tail', tail(0), alt={'idle1|idle3|walk1|walk3|atk1': rows_of(tail(1)), 'idle2|walk2|atk0': rows_of(tail(2)), 'atk2': rows_of(tail(3))}),
        L('hb', 'legB', leg(27, True)),
        L('fb', 'legA', leg(36, True)),
        L('body', 'body', body()),
        L('hf', 'legA', leg(22, False)),
        L('ff', 'legB', leg(39, False), alt={'atk1|atk2': rows_of(leg(39, False, 2, 1))}),
        L('head', 'head', head(), alt={'blink': H['blink'], 'atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        dict(n='eye', g='head', x=39, y=28, rows=T[0], alt={'idle1|idle3|walk1|walk3': T[1], 'blink': T['blink'], 'atk0|atk1|atk2': T['atk'], 'hit': T['hit'], 'ko': T['ko']}),
        L('tongue', 'head', tongue(7), alt={'atk2': rows_of(tongue(4))}, only='atk1|atk2'),
        dict(n='ring', g='root', x=55, y=27, rows=RING, only='atk0|atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1)}, 'idle3': {'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 0)},
    'atk1': {'root': (2, 0)},
    'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'tail': (1, 1)},
    'ko': {'body': (0, 5), 'head': (2, 6), 'tail': (-1, 0)},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
