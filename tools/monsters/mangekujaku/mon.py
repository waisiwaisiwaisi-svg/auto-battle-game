# マンゲクジャク（フェアリー・エスパー × クジャク）手打ち GBA風・デフォルメ（2〜3頭身）
META = dict(id='mangekujaku', name='マンゲクジャク', types=['fairy', 'psychic'], base='クジャク', size='L')
PAL = {
    'k': '#101018', 'l': '#1c1a3c',
    'B': '#6eaaff', 'N': '#3262c8', 'M': '#1e2c78',
    'G': '#84e2a4', 'H': '#2ea07a', 'J': '#15605a',
    'P': '#ff8edc', 'Q': '#b23aa8',
    'C': '#8af4ff', 'Y': '#fff07a',
    'O': '#f0a030',
    'w': '#ffffff',
}
LIGHT = set('BGPCYw')
import pix
from pix import grid, rows_of, outline, ellipse, poly, line, recolor


# ---- 下書きの 道具（あたりは 図形で、仕上げは 手で 打つ）----
def G(w, h): return grid(w, h)
def ell(g, cx, cy, rx, ry, ch): ellipse(g, cx, cy, rx, ry, ch); return g
def pl(g, pts, ch): poly(g, pts, ch); return g
def thick(g, pts, ch, w=2):
    """太い 線（尾・首などの あたり）"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for dx in range(w):
            for dy in range(w): line(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, ch)
    return g
def edge(g, mats, ch='k'):
    """素材の さかい目に 内側の 線（あとで エンジンが 濃い色に する）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if src[y][x] not in mats: continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and src[yy][xx] not in mats and src[yy][xx] not in '.k': g[y][x] = ch; break
    return g
def shade(g, ramps, hl=1, dk=2, dr=1):
    """光は 左上：上・左の ふち hl ドットは 明、下の ふち dk・右の ふち dr ドットは 暗"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, m):
        n = 0
        while n < 9 and 0 <= y + dy * (n + 1) < H and 0 <= x + dx * (n + 1) < W and src[y + dy * (n + 1)][x + dx * (n + 1)] == m: n += 1
        return n
    for y in range(H):
        for x in range(W):
            m = src[y][x]
            if m not in ramps: continue
            L, M, D = ramps[m]
            u, l, d, r = run(y, x, -1, 0, m), run(y, x, 0, -1, m), run(y, x, 1, 0, m), run(y, x, 0, 1, m)
            c = M
            if d < dk or r < dr: c = D
            elif u < hl or l < hl: c = L
            g[y][x] = c
    return g
def at(g, x, y, *rows):
    """手打ち：( x, y ) から 文字を 置く（空白と '.' は そのまま）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c not in ' .' and 0 <= y + j < len(g) and 0 <= x + i < len(g[y + j]): g[y + j][x + i] = c
    return g
def done(g, open_top=0, open_left=0):
    """輪郭を つける。付け根側の 輪郭を 開けて 体に なじませる"""
    rows = [list(r) for r in outline(rows_of(g))]
    for y in range(open_top): rows[y] = ['.' if c == 'k' else c for c in rows[y]]
    for r in rows:
        for x in range(open_left):
            if r[x] == 'k': r[x] = '.'
    return [''.join(r) for r in rows]
import math
RAMP = {'b': 'BNM', 'g': 'GHJ', 'o': 'OOl', 'n': 'NMM'}
DARKER = {'B': 'N', 'N': 'M', 'O': 'l'}
def dark(rows): return recolor(rows, DARKER)

# 万華鏡の レンズ（羽の 目玉もよう）：まわりは 黒い 枠、中は 左右対称の かけら
LENS = [['..kkkk..', '.kCPPCk.', 'kCwYYPCk', 'kPYQQYPk', 'kPYQQYPk', 'kCPYYPCk', '.kCPPCk.', '..kkkk..'],
        ['..kkkk..', '.kPCCPk.', 'kPwQQCPk', 'kCQYYQCk', 'kCQYYQCk', 'kPCQQCPk', '.kPCCPk.', '..kkkk..']]
LENS_GLOW = ['..kkkk..', '.kCYYCk.', 'kCwwwwCk', 'kYwwwwYk', 'kYwwwwYk', 'kCwwwwCk', '.kCYYCk.', '..kkkk..']

# ---- 尾羽の 扇（見せ所）：大きく 広がり、目玉もようが 万華鏡の レンズ ----
def fan(ph=0, glow=False, spread=1.0):
    W, H = 60, 40; g = G(W, H); cx, cy = 29.5, 39
    for i in range(15):                                             # ふちの 羽先（丸い 波）
        a = math.pi * (i / 14)
        ell(g, cx - 28 * spread * math.cos(a), cy - 36 * math.sin(a) * spread, 3.5, 3.5, 'g')
    ell(g, cx, cy, 28 * spread, 36 * spread, 'g')
    for y in range(H):
        for x in range(W):
            if y > 37: g[y][x] = '.'
    shade(g, RAMP, hl=2, dk=2, dr=2)
    for i in range(1, 14):                                          # 羽の じく（中心から 放射）
        a = math.pi * (i / 14)
        line(g, int(cx), int(cy), int(cx - 27 * spread * math.cos(a)), int(cy - 35 * spread * math.sin(a)), 'H')
    for i in range(1, 14, 2):                                       # 羽の 間の 暗い みぞ
        a = math.pi * (i / 14) + .02
        line(g, int(cx) + 1, int(cy), int(cx - 26 * spread * math.cos(a)) + 1, int(cy - 34 * spread * math.sin(a)), 'J')
    for n, (rx, ry, k0) in enumerate(((22, 28, 7), (12.5, 16.5, 5))):  # 外の 輪 7こ、内の 輪 5こ
        for i in range(k0):
            a = math.pi * (.08 + .84 * i / (k0 - 1))
            x = int(round(cx - rx * spread * math.cos(a))) - 4; y = int(round(cy - ry * spread * math.sin(a))) - 4
            at(g, x, y, *(LENS_GLOW if glow else LENS[(i + n + ph) % 2]))
    return done(g)

# ---- 胴と 首：小さく 丸い 胴、太く 短い 首 ----
def body():
    g = G(25, 27)
    thick(g, [(12, 14), (15, 9)], 'b', 8)                  # 首
    ell(g, 11, 18, 10, 8.5, 'b')
    shade(g, RAMP, hl=1, dk=3, dr=2)
    # たたんだ 翼（濃い 青、羽の すじ）
    w = G(25, 27); pl(w, [(3, 14), (12, 12), (17, 17), (13, 23), (2, 22)], 'n')
    for y in range(27):
        for x in range(25):
            if w[y][x] == 'n': g[y][x] = 'N' if (x + y) % 5 else 'M'
    line(g, 3, 14, 12, 12, 'B'); line(g, 4, 18, 13, 17, 'M'); line(g, 4, 20, 12, 20, 'M')
    at(g, 14, 9, 'C'); at(g, 15, 7, 'C'); at(g, 13, 11, 'C')        # 首の 光る うろこ
    return done(g)

# ---- 頭：大きく 丸い、かぎ形の くちばし、レンズの 冠 ----
def head(eye=None, ko=False, mouth=0):
    g = G(27, 27)
    ell(g, 11, 16, 10.5, 10, 'b')
    thick(g, [(6, 8), (4, 3)], 'o', 1); thick(g, [(9, 7), (9, 2)], 'o', 1); thick(g, [(12, 8), (14, 3)], 'o', 1)   # 冠の じく
    shade(g, RAMP, hl=1, dk=3, dr=1)
    at(g, 3, 1, 'PC', 'CP'); at(g, 8, 0, 'CP', 'PC'); at(g, 14, 1, 'PC', 'CP')   # 冠の 先の 小さな レンズ
    at(g, 2, 17, 'C'); at(g, 3, 19, 'CC'); at(g, 5, 21, 'N')          # ほおの もよう
    # くちばし：するどく 下へ 曲がる
    if mouth: at(g, 17, 12, 'kkkkkk..', 'kOOOOOkk', 'kOOOOOOk', 'kkkkkkkk', 'kQQQQk..', 'kOOOOk..', '.kkkk...')
    else: at(g, 17, 13, 'kkkkkk..', 'kOOOOOkk', 'kOOOOOOk', '.kkkkkOk', '..kOOkk.', '...kk...')
    if ko: e = ['k...k', '.k.k.', '..k..', '.k.k.', 'k...k']
    else: e = eye or ['kkkkkk...', '.kkkkkkk.', 'kwPPPkQk.', 'kPPQQkQk.', '.kkkkkk..', '.CCCCC...']
    at(g, 8, 11, *e)
    at(g, 7, 10, 'kk')
    return done(g)
EYE_BLINK = ['kkkkkk...', '.kkkkkkk.', 'kNNNNNNk.', 'kkkkkkkk.', '.NNNNNN..', '.CCCCC...']
EYE_HIT = ['k........', '.kkkkk...', 'kPPPPkkk.', '.kkkkkPk.', '.NNNNNN..', '.CCCCC...']
EYE_ATK = ['kkkkkk...', '.kkkkkkk.', 'kwwPPkPk.', 'kwPPQkQk.', '.kkkkkk..', '.CCCCC...']

LEG = ['..kkk...', '..kOk...', '..kOk...', '..kOk...', '.kOOOk..', 'kOOkOOk.', 'kwk.kwk.']
def legs(): return ['........'] + LEG

# ---- 念力の 万華鏡（エフェクト：はなれて いるのは 意図的）----
def burst(big=False):
    r = 7 if big else 5; n = 2 * r + 1; g = G(n, n)
    for i in range(12):
        a = i * math.pi / 6; rr = r if i % 2 == 0 else r * .55
        line(g, r, r, int(round(r + rr * math.cos(a))), int(round(r + rr * math.sin(a))), 'P' if i % 4 == 0 else 'C')
    ell(g, r + .5, r + .5, 2, 2, 'w'); g[r][r] = 'Y'
    return done(g)

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='fan', g='fan', x=0, y=3, rows=fan(), alt={'idle1|idle3|walk1|walk3': fan(1), 'atk0': fan(0, True), NB: fan(1, True), 'hit': fan(0, False, .92)}),
        dict(n='legF', g='legB', x=22, y=51, rows=dark(legs())),
        dict(n='body', g='body', x=20, y=27, rows=body()),
        dict(n='leg', g='legA', x=29, y=51, rows=legs()),
        dict(n='head', g='head', x=32, y=10, rows=head(),
             alt={'blink': head(EYE_BLINK), 'hit': head(EYE_HIT), 'atk0': head(EYE_ATK), NB: head(EYE_ATK, mouth=1), 'ko': head(ko=True)}),
        dict(n='burst', g='fx', x=58, y=24, rows=burst(), alt={'atk2': burst(True)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1), 'fan': (0, 1)}, 'idle3': {'body': (0, 1), 'fan': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'head': (0, -1), 'fan': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'fan': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 0), 'fan': (-1, -1)}, 'atk1': {'root': (2, 0), 'head': (1, 0)}, 'atk2': {'root': (3, 0), 'head': (1, 0), 'fx': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 0), 'fan': (1, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'fan': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
