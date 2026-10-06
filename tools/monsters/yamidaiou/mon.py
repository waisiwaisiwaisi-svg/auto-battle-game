# ヤミダイオウ（あく・みず × ダイオウイカ）手打ち GBA風・デフォルメ（2〜3頭身：胴（外とう）は 短く 丸く、頭と 目は 大きく、太い 触腕が 見せ所）
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

META = dict(id='yamidaiou', name='ヤミダイオウ', types=['dark', 'water'], base='ダイオウイカ', size='L')
PAL = {
    'k': '#101018', 'l': '#22122e',
    'A': '#8a64b0', 'B': '#563678', 'D': '#2a1a44',      # 体（闇の 紫）
    'E': '#b03a78',                                      # 色素の 斑点
    'S': '#efe4f4', 'R': '#e0283e',                      # 吸盤＝目玉（白目・赤い ひとみ）
    'Y': '#ffe24a', 'O': '#e66a1c',                      # 本当の 目
    'N': '#4c4672', 'C': '#7ae0f2',                      # 闇の 墨・水
    'w': '#ffffff',
}
LIGHT = set('ASYCw')
KEEP_BLACK = set('wSY')
SKIN = {'1': 'ABD'}
SKIN_BACK = {'1': 'BDD'}

# ---------- 外とう（胴）：短く 丸い 円すい、先に 三角の ひれ ----------
def mantle(fl=0):
    def f(p):
        tube(p, [(21, 20), (25, 26), (30, 32)], [6.5, 9.5, 10.5])
        poly(p, [(22, 21), (5 - fl, 14), (13, 29)], '1')               # ひれ（後ろ）
        poly(p, [(17, 20), (21, 3 + fl), (30, 18)], '1')               # ひれ（上）
    g = part(f, SKIN, r=3, tilt=.8)
    for x, y in ((19, 18), (23, 21), (18, 24), (25, 27), (21, 29), (28, 24), (15, 20)):      # 色素の 斑点
        if at(g, x, y) in 'AB': put(g, x, y, 'E'); put(g, x + 1, y, 'E')
    return g

# 目（G：よこ瞳）：大きな 金の 虹彩（黄・だいだい）の まん中に 横長の 四角い 黒瞳。白い 光、上まぶたの 線は 後ろが 上がる
BIGEYE = ['kk........', '.kkkkkkkk.', '.kwYYYYYOk', '.kYkkkkYOk', '.kYkkkkOOk', '..kOOOOOk.', '...kkkkk..']
BIGEYE_ATK = ['kk........', '.kkkkkkkk.', '.kwwYYYYYk', '.kYkkkkkOk', '.kYYYYYOOk', '..kOOOOOk.', '...kkkkk..']
OCTO_EYE = {
    'blink': ['kk........', '.kkkkkkkk.', '.kAAAAAAAk', '.kBBBBBBBk', '..kkkkkkk.', '..........', '..........'],
    'hit':   ['kk........', '.kkk...kk.', '...kk.kk..', '....kkk...', '...kk.kk..', '.kkk...kk.', '..........'],
    'ko':    ['..........', '..A....A..', '...A..A...', '....AA....', '...A..A...', '..A....A..', '..........'],
}
# ---------- 頭：大きな 丸い 頭に 闇の 中で 光る 目 ----------
def head(mode='idle'):
    def f(p): disc(p, 37, 38, 11.5, 9)
    g = part(f, SKIN, r=2, tilt=.5)
    if mode in ('idle', 'atk'):                        # 大きな 目（白い 光＋金と だいだいの 虹彩＋たての ひとみ）
        stamp(g, BIGEYE if mode == 'idle' else BIGEYE_ATK, 32, 31)
    else:
        stamp(g, OCTO_EYE[mode], 32, 31)
    for x, y in ((30, 41), (31, 42), (40, 43), (44, 40)): put(g, x, y, 'E')
    return g

# ---------- 触腕（見せ所）：太い 腕を 5本に 引いて 太く。吸盤は 目玉（白目＋赤い ひとみ）----------
ARMS = {
    'idle': [([(30, 43), (25, 51), (19, 57), (13, 58), (10, 55)], [3.6, 3, 2.4, 1.6, 1], 1),
             ([(34, 45), (33, 53), (30, 58), (25, 60)], [3.8, 3.2, 2.4, 1.4], 1),
             ([(38, 45), (40, 53), (44, 58), (49, 58), (51, 55)], [4, 3.4, 2.6, 1.8, 1.1], 0),
             ([(42, 43), (48, 49), (54, 51), (58, 48), (58, 44)], [4.2, 3.6, 2.8, 2, 1.2], 0),
             ([(44, 39), (51, 39), (56, 35), (58, 30), (55, 28)], [3.6, 3.1, 2.5, 1.8, 1.1], 0)],
    'b':    [([(30, 43), (27, 51), (22, 56), (17, 58), (15, 56)], [3.6, 3, 2.4, 1.6, 1], 1),
             ([(34, 45), (32, 53), (29, 58), (24, 59)], [3.8, 3.2, 2.4, 1.4], 1),
             ([(38, 45), (41, 53), (45, 57), (50, 57), (52, 54)], [4, 3.4, 2.6, 1.8, 1.1], 0),
             ([(42, 43), (48, 48), (54, 49), (58, 46), (57, 42)], [4.2, 3.6, 2.8, 2, 1.2], 0),
             ([(44, 39), (51, 38), (55, 33), (57, 28), (54, 27)], [3.6, 3.1, 2.5, 1.8, 1.1], 0)],
    'atk':  [([(30, 43), (26, 51), (21, 57), (16, 58), (14, 55)], [3.6, 3, 2.4, 1.6, 1], 1),
             ([(34, 45), (33, 53), (30, 58), (25, 60)], [3.8, 3.2, 2.4, 1.4], 1),
             ([(38, 45), (40, 53), (44, 58), (49, 58), (51, 55)], [4, 3.4, 2.6, 1.8, 1.1], 0),
             ([(42, 43), (50, 46), (56, 46), (60, 44), (62, 40)], [4.2, 3.6, 3, 2.4, 1.8], 0),
             ([(44, 39), (52, 36), (57, 33), (61, 32), (62, 35)], [3.6, 3.1, 2.8, 2.2, 1.6], 0)],
    'ko':   [([(30, 43), (25, 51), (19, 58), (12, 60), (8, 60)], [3.6, 3, 2.4, 1.6, 1], 1),
             ([(34, 45), (32, 53), (28, 59), (22, 61)], [3.8, 3.2, 2.4, 1.4], 1),
             ([(38, 45), (41, 53), (46, 59), (52, 61), (56, 61)], [4, 3.4, 2.6, 1.8, 1.1], 0),
             ([(42, 43), (49, 50), (55, 56), (60, 60), (63, 61)], [4.2, 3.6, 2.8, 2, 1.2], 0),
             ([(44, 39), (51, 44), (56, 50), (60, 54), (62, 57)], [3.6, 3.1, 2.5, 1.8, 1.1], 0)],
}
def arms(kind='idle', back=False):
    p = G(); spec = [a for a in ARMS[kind] if a[2] == (1 if back else 0)]
    for path, rad, _ in spec: tube(p, path, rad)
    s = shade(p, SKIN_BACK if back else SKIN, r=1, tilt=.3)
    g = ink(s)
    if not back:                                       # 吸盤＝目玉：腕の 内がわに 白目＋赤い ひとみ
        for path, rad, _ in spec:
            for i in range(len(path) - 1):
                (x0, y0), (x1, y1) = path[i], path[i + 1]
                for u in (.3, .8):
                    x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                    r = rad[i] + (rad[i + 1] - rad[i]) * u
                    if r < 1.8: continue
                    dx, dy = x1 - x0, y1 - y0; n = math.hypot(dx, dy); nx, ny = dy / n, -dx / n   # 腕の 内がわ（右回り）
                    sx, sy = round(x + nx * (r - 1.6) - .5), round(y + ny * (r - 1.6) - .5)
                    if all(at(g, sx + i, sy + j) in 'ABD' for i in (0, 1) for j in (0, 1)):
                        put(g, sx, sy, 'S'); put(g, sx + 1, sy, 'S'); put(g, sx, sy + 1, 'S'); put(g, sx + 1, sy + 1, 'R')
    return g

# ---------- 闇の 墨（攻撃の エフェクト：はなれていて よい）----------
def ink_cloud(big):
    p = G()
    for cx, cy, r in ((54, 22, 4), (59, 18, 3), (58, 26, 3.5), (62, 22, 2.5)) if big else ((52, 22, 3), (56, 20, 2.2), (55, 26, 2.4)):
        disc(p, cx, cy, r, r, '9')
    g = ink(p); swap(g, {'9': 'N'})
    for x, y in ((53, 20), (58, 16), (57, 24), (51, 21)):
        if at(g, x, y) == 'N': put(g, x, y, 'C' if (x + y) % 2 else 'w')
    return g
DROP = [['..k..', '.kCk.', 'kCwCk', '.kkk.'], ['..k..', '.kCk.', '.kwk.', '..k..']]

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    return [
        L('armsB', 'armB', arms('idle', True), alt={'idle2|idle3|walk1|walk3': rows_of(arms('b', True)), 'ko': rows_of(arms('ko', True))}),
        L('mantle', 'body', mantle(), alt={'idle1|idle3|walk1|walk3': rows_of(mantle(1))}),
        L('arms', 'arm', arms(), alt={'idle2|idle3|walk1|walk3': rows_of(arms('b')), 'atk1|atk2': rows_of(arms('atk')), 'ko': rows_of(arms('ko'))}),
        L('head', 'head', head(), alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        dict(n='drop', g='fx', x=6, y=27, rows=DROP[0], alt={'idle2|idle3|walk2|walk3': DROP[1]}, not_='atk1|atk2|hit|ko'),
        L('ink', 'fx2', ink_cloud(False), alt={'atk2': rows_of(ink_cloud(True))}, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'root': (0, -1)}, 'idle3': {'root': (0, -1), 'body': (0, -1)},
    'blink': {},
    'walk0': {'root': (1, 0)}, 'walk1': {'root': (1, -1), 'arm': (-1, 0)}, 'walk2': {'root': (0, -2)}, 'walk3': {'root': (0, -1), 'arm': (-1, 0)},
    'atk0': {'root': (-2, 1), 'body': (-1, -1), 'arm': (-1, 0)},
    'atk1': {'root': (2, 0)},
    'atk2': {'root': (1, 0), 'fx2': (2, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, -1), 'head': (-1, 0)},
    'ko': {'body': (-2, 9), 'head': (0, 6), 'armB': (0, 0)},
}
EYE_BOX = (32, 31, 10, 7)
PARENT = {'body': 'root', 'head': 'root', 'arm': 'root', 'armB': 'root', 'fx': 'root', 'fx2': 'root'}
