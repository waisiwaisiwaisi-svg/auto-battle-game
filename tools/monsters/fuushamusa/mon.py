# フウシャムサ（かぜ・ノーマル × ムササビ）手打ち GBA風・デフォルメ（2〜3頭身：右向き 3/4 で 滑空。大きな 頭に 房の 耳と 前歯、前足と 後ろ足の あいだの 飛膜が 風車の 帆）
EYE_BOX = (43, 19, 9, 7)
META = dict(id='fuushamusa', name='フウシャムサ', types=['wind', 'normal'], base='ムササビ', size='M')
PAL = {
    'k': '#101018', 'l': '#3e2a26',
    'A': '#f2d8a6', 'B': '#c48c58', 'C': '#7c4e32',      # 毛（明・中・暗）
    'D': '#f8f4e4', 'E': '#b4a07c',                      # 膜（帆布の 色：明・暗）
    'c': '#e0fff6', 'm': '#6ad6bc', 'T': '#23806e',      # 風（白・みどり・濃い みどり）＝目の 虹彩も
    'R': '#a02838',                                      # 口の 中
    'w': '#ffffff',
}
LIGHT = set('ADcw')
KEEP_BLACK = set('wcm')
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
FUR = {'1': 'ABC'}
DK = {'A': 'B', 'B': 'C', 'C': 'l', 'D': 'E', 'E': 'C', 'w': 'E'}

# ---- 飛膜 ＝ 風車の 帆（見せ所）：前足の 先・後ろ足の 先・胴を 角に した 帆。格子の すじ、まん中の 骨で 2枚に わかれる ----
def sail(pts, rib):
    g = M(64, 64, ('p', '1', pts))
    for y in range(64):
        for x in range(64):
            if g[y][x] == '1': g[y][x] = 'E' if (x % 4 == 0 or y % 4 == 0) else 'D'
    pix.line(g, *rib, 'C')                                        # 帆の 骨（膜を 2枚に 分ける）
    return pix.outline(pix.rows_of(g))
def limb(path, r=2.0):
    g = M(64, 64, ('t', '1', r, path))
    shade(g, FUR, 1, 1)
    x, y = path[-1]; g[int(y)][int(x)] = 'w'                        # かぎ爪
    return pix.outline(pix.rows_of(g))
def wingset(f=0):
    """f: はばたき（帆の 先が 上下に 1〜2ドット）"""
    near = sail([(36, 37), (52, 46 + f), (31, 50 + f), (7, 51 - f), (16, 40)], (25, 40, 29, 50 + f))
    far = dark(sail([(33, 29), (43, 7 - f), (24, 7 - f), (3, 12 + f), (16, 30)], (25, 29, 25, 8 - f)), DK)
    legs_n = [limb([(36, 37), (45, 41), (52, 46 + f)]), limb([(18, 39), (12, 45), (7, 51 - f)])]
    legs_f = [dark(limb([(34, 29), (39, 18), (43, 7 - f)]), DK), dark(limb([(17, 30), (10, 21), (3, 12 + f)]), DK)]
    return near, far, legs_n, legs_f
def merge(*gs):
    g = pix.grid_of(gs[0])
    for h in gs[1:]:
        for y, r in enumerate(h):
            for x, c in enumerate(r):
                if c != '.': g[y][x] = c
    return pix.rows_of(g)
def wings(f):
    n, fa, ln, lf = wingset(f)
    return merge(fa, *lf), merge(n, *ln)
FAR0, NEAR0 = wings(0); FAR1, NEAR1 = wings(2)

# ---- 胴（小さく 平たい、前が 少し 上がる）としっぽ（平たく 後ろへ）----
BODY = P(M(26, 14, ('e', '1', 13, 7, 13, 6.5)), FUR, [(['..AAAA', 'AA'], 5, 1), (['AAAAAAA'], 9, 10)], lw=2, dw=2)
TAIL = P(M(18, 9, ('p', '1', [(18, 2), (18, 7), (8, 8), (0, 6), (4, 3), (10, 1)])), FUR, [(['C.C.C'], 5, 4)], lw=1, dw=2)
TAIL2 = P(M(18, 9, ('p', '1', [(18, 2), (18, 7), (8, 6), (0, 3), (4, 1), (10, 0)])), FUR, [(['C.C.C'], 5, 2)], lw=1, dw=2)

# ---- 頭（大きい）：房の ある とがった 耳、ほおの 毛、鼻先、白い 前歯（牙）----
HEAD = P(M(23, 21, ('e', '1', 11, 10.5, 11, 9.5), ('e', '1', 17.5, 13, 5, 5.5)), FUR, [
    (['..AAAA', '.AA', 'A'], 3, 2),
    (['AAAA', 'AAAAA', '.AAAA'], 16, 13),                          # 口もと
    (['C.', 'CC', '.C', 'C'], 2, 13), (['CCC.', '...C'], 8, 8),                              # ほおの 毛
], lw=2, dw=3)
EAR = ['k..k.......', 'kk.kk......', '.kkAkk.....', '.kAAAkk....', '..kBAAAkk..', '..kBBAAAk..', '...kCBBBAk.', '...kCCBBk..', '....kkkk...']   # 先に 房毛
EAR_F = dark(EAR, DK)
# 目：三白眼（C）。白目が 広く、小さな 青緑の 虹彩が 上まぶたの 前に 寄る。下まぶたの 線は 濃く 2重（にらむ 目）
EYE = ['kkkk.....', '.kkkkkkkk', '.kwwwmkTk', 'kwwwwwTTk', 'kDwwwwwwk', '.kkkkkkkk', '..CCCCC..']
EYE_ALT = {
    'blink': ['kkkk.....', '.kkkkkkkk', '.kBBBBBBk', 'kBBBBBBBk', 'kkkkkkkkk', '..CCCCC..'],
    'hit':   ['kkkk.....', '.kkkkkkkk', '..kkkkk..', '.....kkk.', '..kkkkk..', '.kkkkkk..', '..CCCCC..'],
    'atk0|atk1|atk2': ['kkkk.....', '.kkkkkkkk', '.kwwwcmkk', 'kwwwwwcmk', 'kDwwwwwwk', '.kkkkkkkk', '..CCCCC..'],
    'ko':    ['kkkk.....', '.kkkkkkkk', '..k...k..', '...k.k...', '....k....', '...k.k...', '..k...k..'],
}
NOSE = ['kk', 'kk']
TEETH = ['kkkk', 'kwwk', 'kwwk', '.kk.']
MOUTH_OPEN = ['kkkkk', 'kRRRk', 'kwwRk', 'kwwk.', '.kk..']
GUST = ['....kkkk......', '..kkccmmkk....', '.kcmmkkkmmk...', 'kcmk....kmk.kk', 'kmk..kkk.kk.kck', '.k..kccmk...kmk', '...kcmkk...kmk.', '....kk....kk...']
WIND = ['.kk...kk..', 'kcmkkkcmk.', '.kk...kkmk', '.......kk.']
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='far', g='wing', x=0, y=0, rows=FAR0, alt={'idle1|idle3|walk1|walk3|atk0|hit': FAR1}),
        dict(n='earF', g='head', x=33, y=7, rows=EAR_F),
        dict(n='tail', g='tail', x=0, y=31, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='body', g='body', x=11, y=26, rows=BODY),
        dict(n='head', g='head', x=32, y=14, rows=HEAD),
        dict(n='ear', g='head', x=37, y=7, rows=EAR),
        dict(n='eye', g='head', x=43, y=19, rows=EYE, alt=EYE_ALT),
        dict(n='nose', g='head', x=55, y=26, rows=NOSE),
        dict(n='teeth', g='head', x=52, y=30, rows=TEETH, alt={NB: MOUTH_OPEN}),
        dict(n='near', g='wing', x=0, y=0, rows=NEAR0, alt={'idle1|idle3|walk1|walk3|atk0|hit': NEAR1}),
        dict(n='wind', g='fx', x=0, y=20, rows=WIND, only='idle1|idle3|walk0|walk2'),
        dict(n='gust', g='fx', x=55, y=29, rows=GUST, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'head': (0, 1)}, 'idle3': {'root': (0, 0)}, 'blink': {},
    'walk0': {'root': (1, -1)}, 'walk1': {'root': (2, -2)}, 'walk2': {'root': (1, -1)}, 'walk3': {'root': (0, 0)},
    'atk0': {'root': (-2, -1), 'head': (-1, 1)}, 'atk1': {'root': (3, 1)}, 'atk2': {'root': (4, 1), 'fx': (2, 0)},
    'hit': {'root': (-3, -1), 'head': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'wing': 'body', 'body': 'root', 'fx': 'root'}
