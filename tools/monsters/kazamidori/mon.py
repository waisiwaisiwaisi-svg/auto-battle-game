# カザミドリ（かぜ・はがね × ニワトリ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 鉄の 頭に 風見の 矢の とさか、胴は 小さく 丸く、足は 短く 太く）
META = dict(id='kazamidori', name='カザミドリ', types=['wind', 'steel'], base='ニワトリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2e48',
    'S': '#eef2fa', 'T': '#9ea8c4', 'U': '#565c7e',      # 鋼
    'C': '#ffb878', 'D': '#d4622c', 'E': '#7a2a1e',      # 銅（矢の とさか・肉垂れ・目）
    'Y': '#ffe466', 'O': '#d08a1c',                      # くちばし・足
    'A': '#a4ecff', 'w': '#ffffff',                      # 風
}
LIGHT = set('SCYAw')
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
STEEL = {'1': 'STU'}; COPPER = {'1': 'CDE'}
DK = {'S': 'T', 'T': 'U', 'U': 'l', 'Y': 'O', 'O': 'E', 'w': 'T'}

# ---- 風見の 矢の とさか（見せ所）：前に 矢じり、後ろの 矢羽根は とさかの ぎざぎざ ----
def comb(ph=0):
    s = -1 if ph else 0
    g = M(50, 15,
          ('r', '1', 8, 6, 41, 9),
          ('p', '1', [(38, 0), (49, 7.5), (38, 15)]),
          ('p', '1', [(0, 2 + s), (3, 6), (5, 1 + s), (8, 5), (10, 0 + s), (13, 5), (16, 1), (20, 6), (20, 10), (16, 14), (2, 14), (6, 9)]))
    return P(g, COPPER, [(['E', 'E', 'E'], 37, 6), (['C'], 39, 3), (['.', '.'], 0, 0)], lw=2, dw=2)
COMB, COMB2 = comb(), comb(1)

# ---- 頭（大きく 丸い 鉄の かぶと）：目の まわりは 銅の 顔（ニワトリの 赤い 顔）----
FACE = ['...DDDDD..', '.DDDDDDDDD', 'DDDDDDDDDD', 'DDDDDDDDDD', 'EDDDDDDDDD', '.EDDDDDDD.', '..EEEDDE..']
HEAD = P(M(24, 21, ('e', '1', 12, 10, 12, 10), ('r', '1', 13, 9, 23, 19), ('e', '1', 9, 15, 9, 6)), STEEL, [
    (FACE, 12, 4),
    (['..SSSS', '.S', 'S'], 4, 1),             # 光の 三日月
    (['UUUUUUUUU', '.TTTTTTTTTT'], 12, 3),       # まゆの ひさし（鉄の 板）
    (['UU', '..UU', '...UUU'], 3, 13),          # ほおの 板の すじ
], lw=2, dw=3)
# ---- 首の 蓑毛（みのげ）：とがった 鉄の 羽が 胴に かぶさる（頭と 胴を つなぐ）----
HACKLE = P(M(18, 14, ('p', '1', [(4, 0), (17, 0), (17, 8), (14, 13), (12, 8), (9, 13), (7, 8), (3, 11), (3, 5)])), STEEL, [
    (['....U..U', '...U..U', '..U..U'], 6, 5)], lw=1, dw=2)
BEAK = [
    'kkkkkk......',
    'YYYYYYkkk...',
    'YYYYYYYYYkk.',
    'OOOOOOOOOOOk',
    'kkkkkkkkkOOk',
    'OOOOOOkk.kOk',
    'kkkkkkk...k.',
]
BEAK_OPEN = [
    'kkkkkk......',
    'YYYYYYkkk...',
    'YYYYYYYYYkk.',
    'OOOOOOOOOOOk',
    'kkkkkkkkkOOk',
    'EEEEk..kk.',
    'EEEEk.....',
    'OOOOOk....',
    'kkkkkk....',
]
WATTLE = ['kkkkk', 'kCCDk', 'kCDDk', 'kDDEk', '.kDEk', '..kk.']
EYE, EYE_ALT = eye('Y', 'O')

# ---- 胴（小さく 丸い）と 翼の 板 ----
BODY = P(M(20, 18, ('e', '1', 10, 9, 10, 9)), STEEL, [
    (['T.T.T', '.U.U.U', 'T.T.T'], 13, 9),   # 胸の うろこ板
], lw=2, dw=3)
WING = opentop(P(M(14, 10, ('p', '1', [(0, 1), (9, 0), (14, 4), (12, 9), (3, 10)])), STEEL, [
    (['UUUUU', '', 'UUUU'], 5, 4)], lw=1, dw=2))
WING_UP = P(M(14, 12, ('p', '1', [(0, 11), (3, 3), (10, 0), (8, 5), (14, 3), (11, 9), (6, 12)])), STEEL, [], lw=1, dw=2)

# ---- しっぽ：鉄の 鎌の 羽 3枚（後ろ上へ）----
def tail(ph=0):
    d = ph
    g = M(18, 24,
          ('p', '1', [(17, 23), (11, 13), (6, 5 - d), (0, 0 - d), (3, 7), (6, 15), (10, 23)]),
          ('p', '1', [(17, 23), (9, 16), (2, 12 - d), (5, 18), (11, 23)]),
          ('p', '1', [(17, 18), (13, 8), (12, 1 - d), (11, 9), (12, 20)]))
    return P(g, STEEL, [], lw=1, dw=2)
TAIL, TAIL2 = tail(), tail(1)

# ---- 足：短く 太い。すねは 黄色、うしろに 蹴爪（けづめ）----
LEG = [
    '.kkkkkk...',
    'kSSTTTUk..',
    'kTTTTTUk..',
    'kTTTTUUk..',
    '.kTTUUk...',
    '..kYOOk...',
    '..kYOOk...',
    'kkkYOOk...',
    'kwkYOOk...',
    '.kkYYOkkk.',
    'kYYYYYYYOk',
    'kwkkwkkwkk',
]
LEG_N = opentop(LEG)
LEG_F = dark(LEG, DK)

GUST = [
    '....kkkkk...',
    '..kkAAAAAkk.',
    '.kAwkkkkkAAk',
    'kAwk.....kkk',
    'kAk.........',
    'kAk.......k.',
    'kAwk....kkAk',
    '.kAwkkkkAAk.',
    '..kkAAAAkk..',
    '....kkkk....',
]
GUST2 = [
    '..kkkkkk......',
    '.kAAAAAAkkk...',
    'kAwkkkkkAAAk..',
    '.kk.....kkAAk.',
    '..........kAk.',
    'kkk.......kAk.',
    'kAAkk...kkAk..',
    '.kkAAkkkAAk...',
    '...kkAAAkk....',
    '.....kkk......',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='legF', g='legB', x=16, y=48, rows=LEG_F),
        dict(n='tail', g='tail', x=6, y=21, rows=TAIL, alt={'idle1|idle2|walk1|walk3': TAIL2}),
        dict(n='body', g='body', x=13, y=30, rows=BODY),
        dict(n='legN', g='legA', x=24, y=48, rows=LEG_N),
        dict(n='comb', g='comb', x=6, y=5, rows=COMB, alt={'idle1|idle2|walk1|walk3|atk1': COMB2}),
        dict(n='hackle', g='body', x=22, y=26, rows=HACKLE),
        dict(n='wing', g='wing', x=14, y=37, rows=WING, alt={'atk0|hit': WING_UP}),
        dict(n='head', g='head', x=27, y=12, rows=HEAD),
        dict(n='wattle', g='head', x=46, y=29, rows=WATTLE),
        dict(n='beak', g='head', x=49, y=21, rows=BEAK, alt={NB: BEAK_OPEN}),
        dict(n='eye', g='head', x=41, y=19, rows=EYE, alt=EYE_ALT),
        dict(n='gust', g='fx', x=58, y=16, rows=GUST, alt={'atk2': GUST2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'comb': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'body': (0, -1)}, 'walk3': {},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'tail': (1, 0)},
    'atk1': {'root': (4, 0), 'head': (2, 1), 'fx': (0, 0)}, 'atk2': {'root': (6, 0), 'head': (1, 0), 'fx': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'comb': 'head', 'head': 'body', 'tail': 'body', 'wing': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
