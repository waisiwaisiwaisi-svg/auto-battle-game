# アンモレイ（いわ・ゴースト × アンモナイト）手打ち GBA風・デフォルメ（大きな 化石の 渦殻、殻口から 霊の 頭と 触手）
import math
META = dict(id='anmorei', name='アンモレイ', types=['rock', 'ghost'], base='アンモナイト', size='M')
EYE_BOX = (37, 24, 10, 8)
PAL = {
    'k': '#101018', 'l': '#2e2638',
    'S': '#e4d8bc', 'T': '#a8977a', 'U': '#5e5040',      # 化石の 石
    'P': '#f0dcff', 'Q': '#b07ce8', 'R': '#6236ac',      # 霊火・霊の 体
    'E': '#1c0e28',                                      # 殻の 中の 闇
    'Y': '#ff86f4', 'Z': '#8a14c8',                      # 目（光る 紫：明るい 光・暗い にじみ）
    'w': '#ffffff',
}
LIGHT = set('SPYw')
KEEP_BLACK = set('wPQRYZ')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
    return g
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
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def opentop(rows, n=1):
    """体に かさなる 付け根：上の 輪郭を 消して 体の 色と なじませる"""
    return ['.' * len(r) if i < n else r for i, r in enumerate(rows)]
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '..' + '.' * 6, '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
STONE = {'1': 'STU'}; GHOST = {'1': 'PQR'}
DK = {'P': 'Q', 'Q': 'R', 'R': 'l'}

# ---- 渦殻（見せ所）：石の 円盤に 渦の みぞ。みぞの 中を 霊火が めぐる（ph で 光の 位置が 回る）----
def shell(ph=0):
    N = 32; c = (N - 1) / 2; R = 15.6
    g = M(N, N, ('e', '1', N / 2, N / 2, R, R))
    shade(g, STONE, lw=3, dw=3)
    b = R / (2 * math.pi * 2.6)
    for y in range(N):
        for x in range(N):
            if g[y][x] == '.': continue
            dx, dy = x - c, y - c; r = math.hypot(dx, dy)
            th = math.atan2(-dy, dx) % (2 * math.pi)            # 右から 反時計まわり
            for n in range(4):
                d = r - b * (th + 2 * math.pi * n) - 1.0
                if abs(d) < .75:
                    lit = math.cos(th * 2 + ph * math.pi / 2) > .3
                    g[y][x] = 'P' if lit and abs(d) < .45 else 'Q'
                elif .75 <= d < 1.5 and g[y][x] in 'ST': g[y][x] = 'U'     # みぞの 影
            # 化石の 肋（ろく）：放射状の 短い すじ
            if r > 5 and int(math.degrees(th)) % 30 in (0, 1) and g[y][x] in 'ST': g[y][x] = 'U' if g[y][x] == 'T' else 'T'
    # 中心の へそ
    for (x, y) in ((15, 15), (16, 15), (15, 16), (16, 16)): g[y][x] = 'R'
    # 殻口（右の ふち）：中は からっぽの 闇
    # 殻口の ふち（厚い 石の くちびる）
    for y in range(8, 26):
        for x in range(27, N):
            if g[y][x] != '.' and (x == 29 or x == 30) and g[y][x] != 'P': g[y][x] = 'U' if x == 30 else 'S'
    for y in range(N):
        for x in range(N):
            if g[y][x] == 'E' and not (0 <= x < N) : pass
    return pix.outline(pix.rows_of(g))
SHELL, SHELL2 = shell(), shell(1)

# ---- 霊の 頭（殻口から 出る ずきん形）：つり目、牙の ある 口 ----
HOOD = P(M(18, 17, ('e', '1', 9, 8.5, 9, 8.5), ('p', '1', [(0, 3), (12, 2), (18, 8), (16, 15), (0, 15)])), GHOST, [
    (['..PPP', '.P', 'P'], 3, 1),
    (['RRRRRR', '......RR'], 1, 12),
    (['..RRRRRRR', 'RRQQQQQQ'], 6, 1),     # まゆの 骨
], lw=2, dw=3)
# 目（E 光る目）：ひとみの ない 紫の 霊光。白い 芯＋白紫（P）＋明るい 紫（Y）、まわりに 1ドットの こい 紫の にじみ（Z）。
# 上が 平らで 下が 丸い にらむ 形。後ろへ 霊火の 尾が ゆらぐ
EYE = ['Z.........', 'YZ........', 'ZYZZZZZZZ.', '.ZYYYYYYYZ', '..ZYPwwPYZ', '..ZYPwPPZ.', '...ZYYYZ..', '....ZZZ...']
EYE_ALT = {
    'blink': ['Z.........', 'YZ........', 'ZYZ.......', '.Z.ZZZZZZ.', '..ZYYYYYYZ', '...ZZZZZZ.', '..........', '..........'],
    'hit': ['..........', 'Z.........', 'YZ.ZZ..ZZ.', '.ZZYYZZYZ.', '..ZPwZYPZ.', '..ZYZ.ZYZ.', '...Z...Z..', '..........'],
    'atk0|atk1|atk2': ['YZ........', 'PYZ.......', 'ZPYZZZZZZZ', '.ZYPPPPYYZ', '.ZYPwwwPYZ', '..ZPwwwPYZ', '..ZYPPPYZ.', '...ZZZZZ..'],
    'ko': ['..........', '..........', '..EZ..ZE..', '...EZZE...', '....EE....', '...EZZE...', '..EZ..ZE..', '..........'],
}
MOUTH = ['kkkkkk', 'kwkwkw', 'kEEEEk', '.kwkwk', '..kkk.']

def flame(W, H, polys):
    """霊火の 触手：舌の 形を 重ね、ふち R → Q → 芯 P"""
    g = pix.grid(W, H)
    for pts in polys:
        m = pix.grid(W, H); pix.poly(m, pts, '#')
        for y in range(H):
            for x in range(W):
                if m[y][x] != '#': continue
                r = 3
                for d in (1, 2):
                    if any(not (0 <= y + dy < H and 0 <= x + dx < W) or m[y + dy][x + dx] != '#' for dy in (-d, 0, d) for dx in (-d, 0, d)):
                        r = d; break
                g[y][x] = 'R' if r == 1 else 'Q' if r == 2 else 'P'
    return pix.outline(pix.rows_of(g))
# ---- 霊の 触手：前下へ うねる 4本（付け根は ずきんの 下に もぐる）----
def tent(ph=0):
    s = 1 if ph else -1
    return flame(26, 19, [
        [(0, 0), (6, 0), (6, 8), (4, 14), (1 + s, 18), (0, 12), (1, 6)],
        [(5, 0), (11, 0), (12, 7), (11, 12), (8 - s, 18), (7, 11), (6, 5)],
        [(10, 0), (16, 0), (18, 6), (19, 10), (17 + s, 16), (15, 9), (12, 5)],
        [(14, 0), (19, 0), (23, 3), (25, 7 - s), (24, 11), (21, 5), (16, 3)],
    ])
TENT, TENT2 = tent(), tent(1)
TENT_ATK = flame(30, 14, [
    [(0, 0), (8, 0), (18, 2), (29, 5), (22, 7), (10, 6), (2, 7)],
    [(0, 4), (9, 5), (20, 8), (28, 12), (18, 12), (8, 11), (0, 10)],
])
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tent', g='tent', x=31, y=36, rows=TENT, alt={'idle1|idle3|walk1|walk3|hit': TENT2, NB: TENT_ATK}),
        dict(n='hood', g='head', x=30, y=22, rows=HOOD),
        dict(n='shell', g='shell', x=4, y=13, rows=SHELL, alt={'idle1|idle3|walk1|walk3|atk1': SHELL2}),
        dict(n='eye', g='head', x=37, y=24, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=43, y=33, rows=MOUTH),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -2), 'head': (1, 0)}, 'idle3': {'root': (0, -1)}, 'blink': {},
    'walk0': {'root': (1, 0)}, 'walk1': {'root': (1, -1), 'tent': (1, 0)}, 'walk2': {'root': (1, -2)}, 'walk3': {'root': (1, -1), 'tent': (-1, 0)},
    'atk0': {'root': (-3, -1), 'head': (-1, 0)}, 'atk1': {'root': (3, 0), 'head': (2, 0), 'tent': (3, -3)}, 'atk2': {'root': (5, 0), 'head': (2, 0), 'tent': (5, -3)},
    'hit': {'root': (-3, -1), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'shell', 'tent': 'head', 'shell': 'root'}
