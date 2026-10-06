# イカノボリ（ドラゴン・ひこう × 竜）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きめ、胴は 小さく 丸く、手足は 短く。凧の 翼は 大きい まま）
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
# 目（L：隈取り）：凧絵の 赤い 隈。目の 上を 赤い 線が 走り、後ろの 目じりから 上へ はね上がる。目は クリーム色の 白目に 黄緑の 虹彩（明・暗）＋黒い 瞳＋白い 光、下にも 赤い 隈が 後ろへ 流れる
def kuma(mid, under=True):
    top = ['............', '.rR.........', '..RRRRRRRr..', '...R' + mid[0][4:]]
    rows = top + mid[1:]
    if under: rows = rows + ['....rRRRR...', '...r........']
    return rows
KUMA_EYE = {
    'idle':  kuma(['....kkkkkkkk', '....kFwGkGFk', '.....kFHkHkk', '......kkkkk.']),
    'atk':   kuma(['....kkkkkkkk', '....kwwGkGGk', '.....kGGkHkk', '......kkkkk.']),
    'blink': kuma(['....kkkkkkkk', '............', '.....kkkkkkk', '............']),
    'hit':   kuma(['....kkkkkkkk', '.....kk..kk.', '.......kk...', '.....kk..kk.']),
    'ko':    kuma(['....kkkkkkkk', '.....F...F..', '......F.F...', '.......F....', '......F.F...'], under=False),
}
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='ikanobori', name='イカノボリ', types=['dragon', 'wind'], base='竜', size='L')
PAL = {
    'k': '#101018', 'l': '#1c3a32',
    'A': '#86dca0', 'B': '#3c9c6c', 'D': '#1e5a4a',      # うろこ（ひすい色）
    'F': '#f6e8bc',                                      # 腹・角・凧の 紙
    'R': '#e8463a', 'r': '#8e2030',                      # 凧の 絵（赤）
    'W': '#9a6430',                                      # 凧の 骨（竹）
    'Y': '#ffe25a', 'O': '#e8861c',                      # 目
    'C': '#c4f2ff',                                      # 風
    'w': '#ffffff', 'p': '#c83c5a',                      # 光／口の 中
    'G': '#b4f040', 'H': '#3e7c16',                      # 目（黄緑の 虹彩）
}
LIGHT = set('AFYCw')
KEEP_BLACK = set('wFGH')
SKIN = {'1': 'ABD'}
SKIN_BACK = {'1': 'BDD'}

# ---------- 翼＝凧（見せ所）：肩から 放射状に のびる 竹の 骨に 紙の 膜を 張る。ふちは 赤、骨の あいだに 赤い 帯の 絵 ----------
WING = {'up': [(26, 1), (6, 12), (16, 31), (34, 31)], 'mid': [(22, 4), (3, 20), (17, 35), (34, 31)], 'down': [(16, 14), (2, 33), (22, 42), (34, 32)]}
def wing(pose='up', back=False):
    T, Lf, Bt, Rt = WING[pose]
    if back: T, Lf, Bt = (T[0] + 9, T[1] + 4), (Lf[0] + 11, Lf[1] + 2), (Bt[0] + 7, Bt[1] - 2)
    p = G(); poly(p, [Rt, T, Lf, Bt], '1')
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] != '1': continue
            edge = any(at(p, x + dx, y + dy) != '1' for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            d = math.hypot(x - Rt[0], y - Rt[1])
            if back: g[y][x] = 'r' if edge else ('B' if (x + y) % 2 else 'D')
            else:
                band = 15 < d < 19                                  # 凧の 絵：弧を えがく 赤い 帯
                c = 'R' if edge or band else 'F'
                if not edge and not band and y > Rt[1] - 6 and (x + y) % 2: c = 'R' if d > 19 else 'F'
                g[y][x] = c
    g = ink(g)
    for tip in (T, Lf, Bt):                                         # 骨：肩から 放射状に
        line(g, Rt[0] - 1, Rt[1] - 1, round(tip[0] + (Rt[0] - tip[0]) * .03), round(tip[1] + (Rt[1] - tip[1]) * .03), 'W')
    stamp(g, ['.kk.', 'kWWk', 'kWDk', '.kk.'], Rt[0] - 3, Rt[1] - 3)  # 肩の 関節（骨の 根もと）
    return g

# ---------- 胴：小さく 丸い。腹は 板の うろこ ----------
def body():
    def f(p):
        disc(p, 27, 38, 8.5, 7.5)
        tube(p, [(31, 34), (36, 29)], [4.5, 4])                       # 首（頭の 中まで 食いこむ）
    g = part(f, SKIN, r=2, tilt=.6)
    for y in range(37, 46):
        for x in range(28, 36):
            if at(g, x, y) in 'ABD' and ((x - 33) / 3.5) ** 2 + ((y - 41) / 5) ** 2 <= 1: put(g, x, y, 'F' if y % 2 else 'W')
    for x, y in ((22, 33), (25, 31), (28, 30)): stamp(g, ['.k', 'kF'], x, y - 1)       # 背の とげ
    return g

# ---------- 尾：凧の 糸の ように 長く 細く、とちゅうに 赤い 房（凧の 尾）----------
def tail(ph=0):
    s = 1 if ph else -1
    pts = [(21, 41), (15, 46), (11, 51), (8, 55 + s), (4, 57 + s), (1, 56 - s)]
    p = G(); tube(p, pts[:3], [3, 2.2, 1.4]);
    g = ink(shade(p, SKIN, r=1, tilt=.3))
    for a, b in zip(pts[2:], pts[3:]): line(g, round(a[0]), round(a[1]), round(b[0]), round(b[1]), 'D')
    for (x, y) in (pts[2], pts[4]):      # 房（ちょうむすびの 赤い 布）
        stamp(g, ['kk.kk', 'kRkRk', 'kk.kk'], round(x) - 2, round(y) - 1)
    return g

# ---------- 手足：短く 太く、大きめの かぎ爪 ----------
def limb(kind, back=False):
    if kind == 'arm': path, rad, claw = [(31, 40), (35, 44), (37, 46)], [2.6, 2.2, 2], (37, 47)
    else: path, rad, claw = [(23, 42), (23, 47), (25, 49)], [3.2, 2.6, 2.2], (25, 50)
    g = part(lambda p: tube(p, path, rad), SKIN_BACK if back else SKIN, r=1, tilt=.3, skip=lambda X, Y: Y < 42 if kind == 'leg' else X < 33)
    dots(g, 'w', [(claw[0] + 1, claw[1]), (claw[0] - 1, claw[1] + 1)]); dots(g, 'k', [(claw[0] + 1, claw[1] + 1), (claw[0], claw[1])])
    return g

# ---------- 頭：大きめ。後ろへ のびる 角、長い ひげ（凧糸の よう）、きばの 口 ----------
def head(mode='idle'):
    def f(p):
        disc(p, 41, 25, 9, 7.5); disc(p, 49.5, 27.5, 5.5, 3.6)
    g = part(f, SKIN, r=2, tilt=.5)
    for y in range(64):          # あごの 下は 腹の 色
        for x in range(64):
            if at(g, x, y) in 'BD' and y >= 29 and x >= 41 and at(g, x, y + 1) in 'k.': put(g, x, y, 'F')
    for j, r in enumerate(KUMA_EYE[mode]):
        for i, c in enumerate(r):
            if c != '.': put(g, 36 + i, 17 + j, c)
    if mode == 'atk':
        cut(g, (45, 29, 56, 32))
        stamp(g, ['kkkkkkkkkkkk', 'kwkwkpppkwkk', 'kppppppppk..', 'kwkwkppkk...', '.kkkkkk.....'], 44, 28)
    else:
        for x, y in ((44, 29), (45, 29), (46, 30), (47, 30), (48, 30), (49, 30), (50, 30), (51, 30), (52, 29), (53, 29), (54, 29)): put(g, x, y, 'k')
        if mode not in ('ko', 'hit'): dots(g, 'w', [(47, 31), (50, 31)]); dots(g, 'k', [(47, 32), (50, 32)])
    stamp(g, ['kk', 'kD'], 53, 25)            # 鼻の あな
    return g
HORN = ['kk........', 'kFkk......', '.kFFkk....', '..kFFFkk..', '...kkFFFkk', '.....kkFFk', '.......kk.']
HORN2 = ['..kk......', '.kFk......', '.kFFk.....', '..kFFkk...', '...kkFFkk.', '.....kkFFk', '.......kk.']
WHISKER = [['..........kk', '.......kkk..', '...kkkk.....', 'kkk.........'], ['............', '.......kkkkk', '...kkkk.....', 'kkk.........']]
GUST = [
    '.....kkkk...',
    '...kkCCCCk..',
    '..kCCwwwkk..',
    '.kCwkkkk....',
    'kCwk.kkkkk..',
    'kCwkkCCCCCk.',
    '.kCCCwwwCCk.',
    '..kkkkkkkk..',
]
GUST2 = ['...kkk.....k', '..kCCCk...kC', '.kCwkkk...kC', 'kCwk.kkkkkCk', 'kCk.kCCCCCk.', '.kCkkwwwkk..', '..kkkkkk....']

def layers():
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    WB = {p: rows_of(wing(p, True)) for p in WING}; WF = {p: rows_of(wing(p)) for p in WING}
    return [
        L('wingB', 'wingB', WB['up'], alt={'idle1|idle3|walk1|walk3': WB['mid'], 'idle2|walk2|atk1': WB['down'], 'ko': WB['down']}),
        L('tail', 'tail', tail(0), alt={'idle1|idle3|walk1|walk3|atk1': rows_of(tail(1))}),
        L('legB', 'body', limb('leg', True), x=4, y=-1),
        L('body', 'body', body()),
        L('leg', 'leg', limb('leg')),
        dict(n='whisker', g='head', x=36, y=28, rows=WHISKER[0], alt={'idle1|idle3|walk1|walk3': WHISKER[1]}, not_='ko'),
        L('head', 'head', head(), alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit'], 'ko': H['ko']}),
        L('wing', 'wing', WF['up'], alt={'idle1|idle3|walk1|walk3': WF['mid'], 'idle2|walk2|atk1': WF['down'], 'ko': WF['down']}),
        L('arm', 'arm', limb('arm')),
        dict(n='horn', g='head', x=27, y=15, rows=HORN, alt={'atk0|atk1|atk2': HORN2}),
        dict(n='gust', g='fx', x=55, y=22, rows=GUST, alt={'atk2': GUST2}, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, 1)}, 'idle2': {'root': (0, 2)}, 'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (1, 0)}, 'walk1': {'root': (1, 1)}, 'walk2': {'root': (0, 2)}, 'walk3': {'root': (0, 1)},
    'atk0': {'root': (-2, 0), 'head': (-1, 0)},
    'atk1': {'root': (3, 1)},
    'atk2': {'root': (2, 0), 'fx': (2, 0)},
    'hit': {'root': (-3, -1), 'head': (-1, -1)},
    'ko': {'_flip': True},
}
EYE_BOX = (36, 18, 12, 8)
PARENT = {'head': 'body', 'wing': 'body', 'wingB': 'body', 'tail': 'body', 'leg': 'body', 'arm': 'body', 'body': 'root', 'fx': 'root'}
