# ヌケガラゼミ（むし・ゴースト × セミ）手打ち GBA風・デフォルメ（2〜3頭身：横に 広い 頭の 両はしに 目、こはく色の すけた 殻、節の ある 腹、かぎの 前足、割れた 背から 霊火）
META = dict(id='nukegarazemi', name='ヌケガラゼミ', types=['bug', 'ghost'], base='セミ', size='M')
PAL = {
    'k': '#101018', 'l': '#3e2414',
    'A': '#fff2c8', 'F': '#f6ca78', 'G': '#c47e36', 'H': '#6c3c1c',      # 抜け殻（すけた こはく色：つや・明・中・暗）
    'P': '#d4f6ff', 'Q': '#7cc6f4', 'U': '#5a58d0',      # 霊火（明・中・ふち）
    'E': '#24122e',                                      # 殻の 中の からっぽの 闇
    'R': '#ff6a7a', 'S': '#a81a48',                      # 目（明・暗）
    'w': '#ffffff',
}
LIGHT = set('AFPw')
KEEP_BLACK = set('wPQU')
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
AMBER = {'1': 'FGH'}
DK = {'A': 'F', 'F': 'G', 'G': 'H', 'H': 'l', 'w': 'G', 'R': 'S'}
def flame(W, H, polys):
    """霊火：舌の 形を 重ね、ふち U → Q → 芯 P"""
    g = pix.grid(W, H)
    for pts in polys:
        m = pix.grid(W, H); pix.poly(m, pts, '#')
        for y in range(H):
            for x in range(W):
                if m[y][x] != '#': continue
                r = 9
                for d in range(1, 4):
                    if any(not (0 <= y + dy < H and 0 <= x + dx < W) or m[y + dy][x + dx] != '#' for dy in range(-d, d + 1) for dx in range(-d, d + 1) if max(abs(dy), abs(dx)) == d):
                        r = d; break
                g[y][x] = 'U' if r == 1 else 'Q' if r == 2 else 'P'
    return pix.outline(pix.rows_of(g))

# ---- 割れた 背から 立ちのぼる 霊火（見せ所）：後ろ上へ なびく 3本の 舌 ----
def ghostfire(sw=0, tall=0):
    t = -tall
    return flame(32, 33, [
        [(12, 32), (25, 32), (25, 25), (22, 18), (17, 11 + t), (14 + sw, 4 + t), (10 + sw, 0 + t), (11, 6 + t), (9, 13), (11, 20), (10, 26)],
        [(8, 32), (15, 28), (13, 22), (8, 18 + t), (3 + sw, 16 + t), (0 + sw, 12 + t), (1, 19), (4, 24), (5, 29)],
        [(20, 32), (29, 31), (31, 25), (30, 18), (28, 13 + t), (30 + sw, 7 + t), (25, 11), (22, 17), (21, 24)],
    ])
WINGS = ghostfire(); WINGS2 = ghostfire(-2); WINGS_BIG = ghostfire(-1, 3)
# 裂け目の 手前に こぼれる 霊火（頭の 上に かさなる）
WISP = ['..k.....k..', '.kPk..kkQk.', '.kPQkkPQk..', 'kQPPQPPQk..', 'kQPPPPQk...', '.kkkkkk....']
WISP2 = ['.k.....k...', 'kQk..kkPk..', '.kPkkPQk...', 'kQPPQPPQk..', 'kQPPPPQk...', '.kkkkkk....']


# ---- 頭（横に 広い 棒の ような 頭）：顔に セミの 横すじ、上と 下に まぶたの 殻 ----
HEAD = P(M(26, 17, ('e', '1', 13, 8.5, 13, 8.5), ('e', '1', 16, 10, 9, 7)), AMBER, [
    (['..AAAA', '.A', 'A'], 3, 1),
    (['..FFFFF..', '.FAAFFFF.', 'HHHHHHHHH', 'FFFFFFFFF', 'HHHHHHHHH', '.FFFFFFF.', '.HHHHHHH.', '..GGGGG..'], 13, 5),   # 顔の ふくらみ（セミの 横すじ）
    (['..', 'w'], 14, 5),
], lw=2, dw=3)
def dome(w, h):
    return P(M(w, h, ('e', '1', w / 2, h / 2, w / 2, h / 2)), AMBER, [(['AA', 'A'], 1, 1)], lw=1, dw=1)
DOME = dome(12, 11); DOME_F = dark(dome(10, 9), DK)
EYE, EYE_ALT = eye('R', 'S')
EYE_F = ['kkkk.', 'kwRRk', 'kSSkk']; EYE_F_ALT = {'blink|hit|ko': ['.....', 'kkkkk', '.....']}
MOUTH = ['kk..', 'kGk.', '.kGk', '..kk']                        # 口の 針（ストロー）

# ---- 胸（背の こぶ）：まん中が たてに 割れて 中は からっぽの 闇 ----
THORAX = P(M(20, 21, ('e', '1', 10, 11, 10, 10), ('r', '1', 0, 12, 19, 17)), AMBER, [
    (['A', 'A', 'A'], 1, 7),
    (['AA.......AA', '.AEEEEEEEA', '.EEEEEEEEE', '..EEEEEEE', '...EEE.E', '....E'], 4, 0),   # 割れた 背（ふちが めくれ、中は からっぽの 闇）
    (['H', 'H', 'H', '.H', '..H'], 15, 10),
], lw=2, dw=3)
# ---- 腹（節の 輪が 5つ、後ろが すぼまる）----
ABD = P(M(24, 18, ('e', '1', 13, 9, 11, 8.5), ('p', '1', [(5, 4), (0, 11), (6, 15)])), AMBER, [
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 5, 5),
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 9, 3),
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 13, 2),
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 17, 2),
    (['A', 'A'], 10, 4), (['A', 'A'], 14, 3), (['A', 'A'], 18, 3),
], lw=2, dw=3)

# ---- 前足（見せ所 その2）：太い もも（下に とげ）→ ひじ → 上へ 反る かぎ爪。付け根は 胸に もぐる ----
CLAW = [
    '..............kk..',
    '.............kAFk.',
    '.............kFGk.',
    '.kkkkk.......kFGk.',
    'kFFFFFkkkk..kFGHk.',
    'kGFFFFFFFFkkkFGHk.',
    'kGGGFFFFFFFFFGGHk.',
    'kHGGGGGGGGGGGGHk..',
    '.kHHHHGGGGGGGHk...',
    '..kkwkkHHHHHHk....',
    '....k.kwkwkkk.....',
    '........k.k.......',
]
CLAW_UP = [
    '...........kk.',
    '..........kAFk',
    '..........kFGk',
    '.kkkkk...kFGHk',
    'kFFFFFkkkkFGHk',
    'kGFFFFFFFFGGHk',
    'kGGGFFFFFFGHk.',
    'kHGGGGGGGGHk..',
    '.kHHHHHHHHk...',
    '..kkwkwkkk....',
    '....k.k.......',
]
CLAW_N = CLAW; CLAW_F = dark(CLAW, DK)
LEG = ['.kGGk.', '.kFGHk', '..kFHk', '..kGHk', '.kGGHk', 'kGGHHk', 'kwkkwk']
LEG_F = dark(LEG, DK)
SLASH = ['..........kk', '........kkPk', '......kkPQk.', '....kkPQUk..', '..kkPQUkk...', 'kkPQUkk.....', 'kPUkk.......', 'kkk.........']
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='fire', g='fire', x=0, y=0, rows=WINGS, alt={'idle1|idle3|walk1|walk3|atk2': WINGS2, 'atk0|atk1': WINGS_BIG}, not_='ko'),
        dict(n='legF', g='legB', x=23, y=52, rows=LEG_F),
        dict(n='clawF', g='clawF', x=40, y=33, rows=CLAW_F, alt={'atk0': dark(CLAW_UP, DK)}),
        dict(n='abd', g='abd', x=2, y=40, rows=ABD),
        dict(n='thorax', g='body', x=15, y=29, rows=THORAX),
        dict(n='leg', g='legA', x=29, y=52, rows=LEG),
        dict(n='domeF', g='head', x=28, y=13, rows=DOME_F),
        dict(n='eyeF', g='head', x=30, y=16, rows=EYE_F, alt=EYE_F_ALT),
        dict(n='head', g='head', x=30, y=16, rows=HEAD),
        dict(n='dome', g='head', x=47, y=12, rows=DOME),
        dict(n='eye', g='head', x=49, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=47, y=33, rows=MOUTH),
        dict(n='clawN', g='clawN', x=35, y=38, rows=CLAW_N, alt={'atk0': CLAW_UP}),
        dict(n='slash', g='clawN', x=51, y=27, rows=SLASH, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'head': (0, 1)}, 'idle2': {'fire': (0, -1), 'clawN': (0, -1)}, 'idle3': {'body': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'root': (1, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'root': (1, 0)},
    'atk0': {'fire': (0, -2), 'root': (-2, 0), 'clawN': (0, -3), 'clawF': (0, -2)}, 'atk1': {'fire': (0, -2), 'root': (4, 0), 'clawN': (3, -1)}, 'atk2': {'root': (5, 0), 'clawN': (2, 1), 'clawF': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'clawN': (-1, 0)}, 'ko': {'_flip': True},
}
PARENT = {'abd': 'body', 'fire': 'body', 'head': 'body', 'clawN': 'body', 'clawF': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
