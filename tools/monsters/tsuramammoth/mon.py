# ツラマンモス（こおり・いわ × マンモス）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きく、胴は 小さく 丸く、足は 短い 柱）
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
# 目（M：重い まぶた）：小さく 暗い 青の 目。毛の 色の 厚い 上まぶたが 前へ 垂れて 虹彩の 上半分を かくし、下に 小さく 白い 光＋青・こい 紺の 虹彩＋黒い 瞳が のぞく
LID_EYE = {
    'idle':  ['.kkkkk..', 'kAABBBk.', 'kkkkkkkk', '.kwKkNk.', '..kkkk..'],
    'atk':   ['.kkkkk..', 'kAABBBk.', 'kkkkkkkk', '.kwJkKk.', '.kKNkNk.', '..kkkk..'],
    'blink': ['.kkkkk..', 'kAABBBk.', 'kABBBBBk', '.kkkkkk.', '........'],
    'hit':   ['.kkkkk..', 'kAABBBk.', 'kkkkkkkk', '..k..k..', '.k....k.'],
    'ko':    ['.kkkkk..', 'kAABBBk.', 'kkABBkkk', '..kkk...', '..kkk...', '.k...k..'],
}
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='tsuramammoth', name='ツラマンモス', types=['ice', 'rock'], base='マンモス', size='L')
PAL = {
    'k': '#101018', 'l': '#2e1e1a',
    'A': '#b88452', 'B': '#7c4c2e', 'D': '#462a1e',      # 毛（こげ茶）
    'R': '#b4b0c0', 'Q': '#716c82', 'P': '#403c50',      # 氷河の 岩
    'I': '#eafcff', 'J': '#8edcf4', 'K': '#3a86bc',      # つらら・氷
    'w': '#ffffff', 'p': '#c04a5a', 'Y': '#ffe27a',      # 光／口の 中／目の 光
    'N': '#1a2c5c',                                      # 目（こい 紺）
}
LIGHT = set('ARIwY')
KEEP_BLACK = set('wIN')
FUR = {'1': 'ABD'}
FUR_BACK = {'1': 'BDD'}

# ---------- 背の 氷河の 岩（岩の 山＋氷の 面）----------
def glacier(ph=0):
    p = G()
    poly(p, [(9, 39), (11, 30), (15, 27), (17, 21), (22, 26), (26, 19), (31, 25), (34, 29), (37, 38)], '3')
    for poly_pts in ([(17, 21), (22, 26), (19, 31), (15, 28)], [(26, 19), (31, 25), (28, 30), (24, 26)], [(11, 30), (15, 27), (14, 33)]):
        poly(p, poly_pts, '4')
    s = shade(p, {'3': 'RQP', '4': 'IJK'}, r=2, tilt=.9, hi=.1, lo=-.2)
    g = ink(s, skip=lambda X, Y: Y > 36)
    for x, y in ((18, 23), (27, 21), (12, 31)): put(g, x, y, 'w')
    for x, y in ((20, 33), (21, 34), (25, 33), (29, 32), (30, 33)): put(g, x, y, 'P')     # 岩の ひび
    if ph: dots(g, 'w', [(23, 27), (29, 26)])
    return g

# ---------- 胴：小さく 丸い、すその 毛が ぼさぼさ ----------
def body():
    def f(p):
        disc(p, 24, 45, 15, 10.5)
        for x in range(11, 38, 4): poly(p, [(x, 52), (x + 2, 57.5), (x + 4, 52)], '1')
        tube(p, [(10, 42), (6, 46), (5, 49)], [2, 1.6, 1.2])          # 短い 尾
    g = part(f, FUR, r=3, tilt=.7)
    for x, y in ((14, 41), (15, 42), (19, 40), (20, 41), (27, 47), (28, 48), (22, 50)): put(g, x, y, 'B')
    dots(g, 'D', [(4, 49), (5, 50), (4, 50)])
    return g

# ---------- 足：太く 短い 柱、ひづめの つめ ----------
def leg(x, back, lift=0):
    def f(p):
        tube(p, [(x, 49), (x, 57 - lift)], [4.2, 4.2]); disc(p, x + .5, 59 - lift, 4.6, 2.4)
    g = part(f, FUR_BACK if back else FUR, r=1, tilt=.3, skip=lambda X, Y: Y < 47)
    fx, fy = round(x + .5), round(59 - lift)
    dots(g, 'R' if not back else 'Q', [(fx - 2, fy + 1), (fx, fy + 1), (fx + 2, fy + 1)])
    dots(g, 'k', [(fx - 1, fy + 1), (fx + 1, fy + 1)])
    return g

# ---------- 頭：大きな 丸い 頭、もり上がった 額、小さな 耳、短く 太い 鼻 ----------
def head(mode='idle'):
    def f(p):
        disc(p, 41, 35, 12.5, 11.5); disc(p, 38, 27, 8, 5.5)
        disc(p, 30, 33, 4, 5)                                         # 耳
        tube(p, {'atk': [(49, 39), (55, 43), (60, 42), (62, 39)], 'ko': [(49, 39), (54, 44), (59, 46), (63, 46)]}.get(mode, [(49, 39), (53, 47), (52, 54), (55, 57)]), [4, 3.2, 2.4, 1.8])
    g = part(f, FUR, r=2, tilt=.5)
    for x, y in ((29, 31), (30, 32), (29, 33), (30, 34)): put(g, x, y, 'D')
    if mode == 'atk': dots(g, 'B', [(56, 42), (58, 42)])
    else: dots(g, 'B', [(52, 45), (53, 48), (52, 51)])
    for x in range(36, 46): put(g, x, 22 + (x - 36) // 3, 'B')      # 額の 毛の すじ
    for x in range(39, 47): put(g, x, 26 + (x - 39) // 4, 'D')       # 太い まゆ
    for j, r in enumerate(LID_EYE[mode]):
        for i, c in enumerate(r):
            if c != '.': put(g, 41 + i, 28 + j, c)
    if mode == 'atk':
        stamp(g, ['kkkkk', 'kpppk', '.kkk.'], 44, 41)
    return g
# ---------- きば＝つらら（見せ所）：口の わきから 前へ 大きく 曲がる 氷の 牙 ----------
def tusk(back=False, mode='idle'):
    p = G()
    path = [(45, 43), (52, 49), (59, 47), (62, 40), (61, 32)] if mode != 'atk' else [(45, 43), (53, 48), (60, 47), (63, 42), (64, 36)]
    if back: path = [(x - 3, y - 1) for x, y in path]
    tube(p, path, [3.4, 3.2, 2.6, 1.6, .5], '4')
    s = shade(p, {'4': ('JKK' if back else 'IJK')}, r=1, tilt=.9, hi=.1, lo=-.25)
    g = ink(s)
    if not back:
        for t in range(1, 12):                           # 氷の 光の すじと 節（つららの 段）
            i = min(int(t / 3), 3); u = t / 3 - i
            (x0, y0), (x1, y1) = path[i], path[i + 1]
            x, y = round(x0 + (x1 - x0) * u - 1), round(y0 + (y1 - y0) * u - 1)
            if at(g, x, y) in 'IJK': put(g, x, y, 'w' if t % 3 else 'J')
    return g
SHARD = [
    '.....kk..',
    '...kkIk..',
    '.kkIJJkk.',
    'kIIJJKKJk',
    '.kkJKkkk.',
    '...kk....',
]
SHARD2 = ['..k...k..', '.kIk.kJk.', '..kJkk.k.', '...k.....', '.k....k..', 'kIk..kJk.', '.k....k..']

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    TA, TB = rows_of(tusk(False, 'atk')), rows_of(tusk(True, 'atk'))
    return [
        L('tuskB', 'head', tusk(True), alt={'atk1|atk2': TB}),
        L('legHB', 'legB', leg(16, True)),
        L('legFB', 'legA', leg(33, True)),
        L('glacier', 'body', glacier(), alt={'idle1|idle3|walk1|walk3': rows_of(glacier(1))}),
        L('body', 'body', body()),
        L('legH', 'legA', leg(12, False)),
        L('legF', 'legB', leg(28, False)),
        L('head', 'head', head(), alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        L('tusk', 'head', tusk(), alt={'atk1|atk2': TA}),
        dict(n='shard', g='root', x=55, y=28, rows=SHARD, alt={'atk2': SHARD2}, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, -2)},
    'atk1': {'root': (3, 0), 'head': (0, 1)},
    'atk2': {'root': (2, 0), 'head': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1)},
    'ko': {'body': (0, 5), 'head': (1, 2)},
}
EYE_BOX = (41, 28, 8, 5)
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
