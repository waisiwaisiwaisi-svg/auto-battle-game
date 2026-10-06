# トンボギリ（かくとう・むし × トンボ）手打ち GBA風・デフォルメ（2〜3頭身：頭は ほぼ 大きな 複眼、胸は 小さく 太く、4枚の はね、長い 腹の 先が 薙刀の 刃）
META = dict(id='tonbogiri', name='トンボギリ', types=['fighting', 'bug'], base='トンボ', size='M')
EYE_BOX = (40, 17, 18, 15)
PAL = {
    'k': '#101018', 'l': '#3e1418',
    'A': '#ff7c5c', 'B': '#c63a30', 'D': '#6a1a22',      # 赤い 体
    'Y': '#ffe27a', 'O': '#c88a24',                      # 金の 輪（はばき）
    'g': '#a6f6c6', 'G': '#2a9a76', 'E': '#14503e',      # 複眼（明・中・暗）
    'S': '#f4f8ff', 'T': '#a6b2ca', 'U': '#566080',      # 鋼の 刃
    'c': '#dcf6ff', 'C': '#80bce4',                      # はね
    'w': '#ffffff',
}
LIGHT = set('AYgScw')
KEEP_BLACK = set('wgYSc')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角 / ('t',ch,r,[(x,y),...]) 太い 線。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
        elif s[0] == 't':
            r, pts = s[2], s[3]
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                n = int(max(abs(bx - ax), abs(by - ay)) * 2) + 1
                for i in range(n + 1):
                    t = i / n; pix.ellipse(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, r, s[1]) if False else _disc(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, s[1])
    return g
def _disc(g, cx, cy, r, ch):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= y < len(g) and 0 <= x < len(g[0]) and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: g[y][x] = ch
def shade(g, ramps, lw=2, dw=2):
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, c):
        n = 1
        while 0 <= y + dy * n < H and 0 <= x + dx * n < W and src[y + dy * n][x + dx * n] == c: n += 1
        return n
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c not in ramps: continue
            hi, mid, lo = ramps[c]
            if run(y, x, 1, 0, c) <= dw or run(y, x, 0, 1, c) <= dw: g[y][x] = lo
            elif run(y, x, -1, 0, c) <= lw or run(y, x, 0, -1, c) <= 1: g[y][x] = hi
            else: g[y][x] = mid
    return g
def P(g, ramps, over=(), lw=2, dw=2, ol=True):
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭（輪郭の ぶん 左上へ 1 ずれる）"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '........', '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
import math
RED = {'1': 'ABD'}; STEEL = {'1': 'STU'}; EYEC = {'1': 'gGE'}
DK = {'A': 'B', 'B': 'D', 'D': 'l', 'c': 'C', 'C': 'U', 'w': 'C', 'g': 'G', 'G': 'E'}

# ---- はね（4枚＝前ばね・後ろばねの 2組）：細長い だ円を 付け根から 後ろ上へ。すじと うすい 市松 ----
def wing(root, tip, w):
    (ax, ay), (bx, by) = root, tip; L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L; nx, ny = -uy, ux
    pts = []
    pts = [(ax + ux * (L / 2 + L / 2 * math.cos(t)) + nx * w * math.sin(t) * (0.6 + 0.4 * (1 + math.cos(t)) / 2), ay + uy * (L / 2 + L / 2 * math.cos(t)) + ny * w * math.sin(t) * (0.6 + 0.4 * (1 + math.cos(t)) / 2)) for t in [i / 24 * math.pi * 2 for i in range(24)]]
    g = M(64, 40, ('p', '1', pts))
    for y in range(40):
        for x in range(64):
            if g[y][x] == '1': g[y][x] = 'c' if (x + y) % 2 or (y > 0 and g[y - 1][x] == '.') else 'C'
    for i in range(3, int(L) - 1):                                         # 前の ふちの すじ（太い 脈）
        x, y = ax + ux * i - nx * (w * .45), ay + uy * i - ny * (w * .45)
        if g[int(y)][int(x)] != '.': g[int(y)][int(x)] = 'C'
    for i in range(3, int(L) - 3, 4):
        x, y = ax + ux * i, ay + uy * i
        if g[int(y)][int(x)] != '.': g[int(y)][int(x)] = 'C'
    x, y = ax + ux * (L - 3), ay + uy * (L - 3)
    g[int(y)][int(x)] = 'U'                                                # 縁紋（はねの 先の 点）
    return pix.outline(pix.rows_of(g))
def wings(up=0):
    """near=手前の 2枚、far=奥の 2枚（暗い）。up で はばたき"""
    near = [wing((30, 26), (13, 5 + up * 4), 4.2), wing((28, 28), (5, 17 + up * 3), 4.0)]
    far = [wing((34, 26), (37 - up * 2, 3 + up * 3), 3.4), wing((32, 26), (25, 2 + up * 4), 3.4)]
    return near, far
WN0, WF0 = wings(0); WN1, WF1 = wings(1)
def merge(*gs):
    g = pix.grid_of(gs[0])
    for h in gs[1:]:
        for y, r in enumerate(h):
            for x, c in enumerate(r):
                if c != '.': g[y][x] = c
    return pix.rows_of(g)
WING_N = merge(*WN0); WING_N1 = merge(*WN1); WING_F = dark(merge(*WF0), DK); WING_F1 = dark(merge(*WF1), DK)

# ---- 頭（大きい）：ほとんどが 複眼の ドーム。複眼の 中に 白い 光＋たての ひとみ＋まゆの ひさし。下に 白い 大あご ----
HEAD = P(M(19, 18, ('e', '1', 9.5, 9, 9.5, 9)), RED, [(['AAA', 'A'], 4, 12)], lw=2, dw=3)
# 複眼（D）：大きな 緑の ドーム。六角の あみ目（点の 並び）と 左上の 反射の 帯。ひとみは ない。上に 怒りの まゆの 線
def dome(mode='open'):
    g = M(16, 13, ('e', '1', 8.5, 7, 8, 6.5)); shade(g, EYEC, 2, 3)
    for y in range(13):
        for x in range(16):
            c = g[y][x]
            if c == '.': continue
            if x % 4 == (1 if y % 2 else 3):   # あみ目の 点
                g[y][x] = {'g': 'G', 'G': 'E', 'E': 'G'}[c] if mode != 'atk' else {'g': 'w', 'G': 'g', 'E': 'G'}[c]
            d = ((x + .5 - 8.5) / 8) ** 2 + ((y + .5 - 7) / 6.5) ** 2
            if .42 <= d <= .66 and x + .5 < 8.5 and y + .5 < 7.5 and x + y > 3:                                       # 反射の 帯（左上の 弧）
                if mode == 'hit' and (x + y) % 3 == 0: continue                                                         # 被弾：帯が 割れる
                g[y][x] = 'w' if (mode == 'atk' or (x + y) % 2) else 'g'
    return pix.outline(pix.rows_of(g))
DOME = dome(); DOME_ATK = dome('atk'); DOME_HIT = dome('hit')
# まゆの 線（ドームの 上を 前へ 下がる 太い 線）。まばたき＝まゆが 下がって ドームの 上を おおう
EYE = ['kk.........', 'kkkkk......', '..kkkkkk...', '.....kkkkk.', '.......kkkk', '.........kk']
EYE_ALT = {
    'blink': ['kk.........', 'kkkkk......', 'EEkkkkkk...', 'EEEEEkkkkk.', 'EEEEEEEkkkk', '..EEEEEEEkk', '.........kk'],
    'hit': ['...kkk.....', 'kkkk.kk....', '.......kk..', '.........kk', '...........', '...........'],
    'atk0|atk1|atk2': ['k..........', 'kkk........', '.kkkkkk....', '....kkkkk..', '.......kkkk', '.........kk', '..........k'],
    'ko': ['...........', '...kk...kk.', '....kk.kk..', '.....kkk...', '....kk.kk..', '...kk...kk.'],
}
JAW = ['kkkk.', '.kwwk', '..kwk', '...k.']
JAW_OPEN = ['kkkk.', '.kwwk', '..kwk', '.....', '..kwk', '.kwwk', 'kkkk.']

# ---- 胸（小さく 太い、前へ かたむく）：はねの 付け根 ----
THORAX = P(M(16, 16, ('e', '1', 8, 8, 8, 7.5)), RED, [(['..AA', '.A', 'A'], 3, 2), (['D', 'D', '.D', '..D'], 9, 5)], lw=2, dw=3)

# ---- 腹＝薙刀の 柄（節の 輪が 並ぶ）＋ 金の はばき ＋ 反った 鋼の 刃（見せ所）----
def bez(p0, p1, p2, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]
def naginata(p0, p1, p2, d):
    path = bez(p0, p1, p2); tip = p2
    n = math.hypot(*d); d = (d[0] / n, d[1] / n); nv = (d[1], -d[0])
    if nv[1] > 0: nv = (-nv[0], -nv[1])
    def Q(a, b): return (tip[0] + d[0] * a + nv[0] * b, tip[1] + d[1] * a + nv[1] * b)
    g = pix.grid(64, 64)
    for i, (x, y) in enumerate(path): _disc(g, x, y, 2.7 - 1.1 * i / len(path), '1')
    shade(g, RED, 1, 2)
    for i in range(2, len(path) - 1, 2):                                    # 節の 輪
        x, y = path[i]; dx, dy = path[i + 1][0] - x, path[i + 1][1] - y
        for k in (-2, -1, 0, 1, 2):
            X, Y = (round(x), round(y) + k) if abs(dx) > abs(dy) else (round(x) + k, round(y))
            if g[Y][X] in 'ABD': g[Y][X] = 'D'
    b = pix.grid(64, 64)
    pix.poly(b, [Q(1, 2.6), Q(6, 4), Q(11, 6), Q(16, 10), Q(12, 2.6), Q(6, -1.4), Q(1, -2.6)], '1'); shade(b, STEEL, 1, 2)
    for a in range(2, 14):
        x, y = Q(a, 2.0 + a * .3)
        if b[int(y)][int(x)] != '.': b[int(y)][int(x)] = 'S'
    for y in range(64):
        for x in range(64):
            if b[y][x] != '.': g[y][x] = b[y][x]
    for (x, y) in [Q(-1, k) for k in (-2, -1, 0, 1, 2)] + [Q(0, k) for k in (-2, -1, 0, 1, 2)] + [Q(.9, k) for k in (-2, -1, 0, 1, 2)]:   # はばき
        g[round(y)][round(x)] = 'Y' if x < tip[0] else 'O'
    return pix.outline(pix.rows_of(g))
NAG_REST = naginata((30, 38), (20, 42), (14, 41), (-1, -.4))
NAG_UP = naginata((30, 38), (21, 36), (15, 30), (-1, -1))
NAG_SWING = naginata((31, 40), (26, 54), (43, 51), (1, -.15))
NAG_THRUST = naginata((31, 40), (30, 52), (44, 47), (1, -.6))

# ---- 脚（6本 → 2本に まとめる）：胸から 前下へ、先は かぎ爪 ----
LEG = ['kkk...', 'kADk..', '.kADk.', '..kADk', '..kADk', '.kADk.', '.kwk..', 'kwk...']
LEG_F = dark(LEG, DK)
SLASH = ['......kkk.', '....kkcck.', '...kccCk..', '..kcCk....', '.kcCk.....', '.kcCk.....', 'kcCk......', 'kcck......', '.kcCk.....', '..kcck....', '...kkk....']
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='wingF', g='wing', x=0, y=0, rows=WING_F, alt={'idle1|idle3|walk1|walk3|atk0|hit': WING_F1}),
        dict(n='legF', g='body', x=38, y=40, rows=LEG_F),
        dict(n='nag', g='tail', x=-1, y=-1, rows=NAG_REST, alt={'atk0': NAG_UP, 'atk1': NAG_SWING, 'atk2': NAG_THRUST}),
        dict(n='thorax', g='body', x=26, y=26, rows=THORAX),
        dict(n='leg', g='body', x=34, y=40, rows=LEG),
        dict(n='head', g='head', x=37, y=19, rows=HEAD),
        dict(n='dome', g='head', x=40, y=17, rows=DOME, alt={'atk0|atk1|atk2': DOME_ATK, 'hit': DOME_HIT}),
        dict(n='eye', g='head', x=45, y=20, rows=EYE, alt=EYE_ALT),
        dict(n='jaw', g='head', x=52, y=33, rows=JAW, alt={NB: JAW_OPEN}),
        dict(n='wingN', g='wing', x=0, y=0, rows=WING_N, alt={'idle1|idle3|walk1|walk3|atk0|hit': WING_N1}),
        dict(n='slash', g='tail', x=55, y=40, rows=SLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -2)}, 'idle3': {'root': (0, -1)}, 'blink': {},
    'walk0': {'root': (1, -1)}, 'walk1': {'root': (2, -2)}, 'walk2': {'root': (1, -1)}, 'walk3': {'root': (0, 0)},
    'atk0': {'root': (-2, -2)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (3, 1)},
    'hit': {'root': (-4, -1), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'tail': 'body', 'body': 'root'}
