# イカリタガメ（むし・みず × タガメ）手打ち GBA風・デフォルメ（2〜3頭身：大きな くさび形の 頭、平たい 背は 小さく、前脚は 鉄の 錨）
META = dict(id='ikaritagame', name='イカリタガメ', types=['bug', 'water'], base='タガメ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2618',
    'B': '#dcc47c', 'C': '#96793e', 'D': '#4e3a1e',      # 体（どろ色）
    'I': '#d4dce8', 'J': '#828ca0', 'K': '#40465c',      # 鉄の 錨
    'A': '#a8eaff', 'W': '#3e94d4',                      # 水
    'Y': '#ffe24c', 'O': '#c4741a',                      # 目
    'w': '#ffffff',
}
LIGHT = set('BIAYw')
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
BUG = {'1': 'BCD'}
DK = {'B': 'C', 'C': 'D', 'D': 'l', 'I': 'J', 'J': 'K', 'K': 'l', 'A': 'W', 'w': 'J'}

# ---- 背（平たい だ円の 羽）：小さく、カメムシの なかまの X字の 羽の 重なり、おしりに 呼吸管 ----
BODY = P(M(22, 14, ('e', '1', 12, 7, 10, 7), ('p', '1', [(4, 4), (0, 8), (4, 11)])), BUG, [
    (['..AAAA', '.A', 'A'], 4, 1),                           # 水に ぬれた つや
    (['DDDD.......', '....DDD....', '.......DDDD'], 8, 3),     # 羽の 重なり（X字）
    (['.......DDDD', '....DDD....', 'DDDD.......'], 8, 8),
], lw=2, dw=3)
SIPHON = ['kkkkk.', 'kCCDDk', '.kkkkk']

# ---- 頭（大きい くさび形）：前へ とがる、下に 針の くちばし ----
HEAD = P(M(19, 16, ('e', '1', 7, 9, 7, 7), ('p', '1', [(3, 2), (11, 0), (19, 8), (14, 14), (3, 16)])), BUG, [
    (['..BBB', '.B', 'B'], 3, 2),
    (['DDDDDDDD'], 1, 12),                                    # 頭と むねの さかい
], lw=2, dw=3)
EYE, EYE_ALT = eye('Y', 'O')
BEAK = ['kkk...', 'kCCkk.', '.kCDDk', '..kDwk', '...kwk', '....kk']

# ---- 前脚 ＝ 錨（見せ所）：もも（虫）→ 錨の 輪が ひざ → 柄 → かぎの 2本爪 ----
ANCHOR = [
    '.....kkkk.......',
    '....kIIJJk......',
    '....kIkkJk......',
    '....kIIJJk......',
    '.kkkkkIJkkkkk...',
    'kIIIIIIJJJJJKk..',
    '.kkkkkIJKkkkk...',
    '.....kIJKk......',
    '.....kIJKk......',
    '.....kIJKk......',
    '.....kIJKk......',
    '.....kIJKk......',
    '.....kIJKk......',
    '.....kIJKk......',
    'kk...kIJKk...kk.',
    'kwk..kIJKk..kwk.',
    'kIJk.kIJKk.kJKk.',
    'kIJKkkIJKkkJKKk.',
    'kIJJKkIJKkJJKKk.',
    '.kIJJJIJKJJJKk..',
    '..kkIJJJJJKkk...',
    '....kkkkkkk.....',
]
def grow(rows, keep=3):
    """3ドットごとに 1ドット ふやして 大きく（内側の 線は はずして 輪郭を つけ直す）"""
    g = [r.replace('k', '.') for r in rows]
    g = [''.join(c * (2 if i % keep == 1 else 1) for i, c in enumerate(r)) for r in g]
    out = []
    for j, r in enumerate(g): out += [r] * (2 if j % keep == 1 else 1)
    w = max(len(r) for r in out)
    return pix.outline([r.ljust(w, '.') for r in out])
ANCHOR = grow(ANCHOR)
ANCHOR_SWING = pix.rot90(pix.rot90(pix.rot90(ANCHOR)))   # 前へ ふり出す（90度）
FEMUR = P(M(15, 10, ('p', '1', [(0, 9), (0, 4), (11, 0), (15, 2), (13, 6), (3, 10)])), BUG, [(['BBB'], 5, 3)], lw=1, dw=2)
FEMUR_FWD = P(M(14, 9, ('p', '1', [(0, 9), (0, 4), (11, 0), (14, 3), (13, 6), (4, 9)])), BUG, [], lw=1, dw=2)

# ---- 泳ぐ 足（4本 → 2本に まとめる）：短く 太く、すその 毛は 水色 ----
LEG = [
    '.kkkk.....',
    'kBCCCk....',
    'kBCCDk....',
    '.kBCDk....',
    '..kBCDk...',
    '...kBCDkk.',
    '...kBBCCDk',
    '....kkBCDk',
    '.....kBCk.',
    '....kBCk..',
    '...kACAk..',
    '..kAkAkAk.',
    '..kkkkkkk.',
]
LEG_N = opentop(LEG); LEG_F = dark(LEG, DK)
SPLASH = [
    '....k.....k...',
    '...kAk...kAk..',
    '.k..kAk.kAk..k',
    'kAkk.kAkAk.kAk',
    '.kAAkkWAWkkAk.',
    '..kAWWwWWWAk..',
    '...kkkkkkkk...',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='anchorF', g='armF', x=34, y=28, rows=dark(ANCHOR, DK), not_=NB),
        dict(n='femurF', g='armF', x=30, y=31, rows=dark(FEMUR, DK), not_=NB),
        dict(n='legF', g='legB', x=10, y=48, rows=LEG_F),
        dict(n='siphon', g='body', x=4, y=40, rows=SIPHON),
        dict(n='body', g='body', x=6, y=34, rows=BODY),
        dict(n='legN', g='legA', x=19, y=48, rows=LEG_N),
        dict(n='head', g='head', x=24, y=22, rows=HEAD),
        dict(n='eye', g='head', x=33, y=26, rows=EYE, alt=EYE_ALT),
        dict(n='beak', g='head', x=40, y=35, rows=BEAK),
        dict(n='femur', g='arm', x=34, y=33, rows=FEMUR, alt={NB: FEMUR_FWD}, ),
        dict(n='anchor', g='arm', x=39, y=31, rows=ANCHOR, not_=NB),
        dict(n='anchorS', g='arm', x=46, y=24, rows=ANCHOR_SWING, only=NB),
        dict(n='splash', g='arm', x=56, y=40, rows=SPLASH, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, 1)}, 'idle3': {'arm': (0, 1)}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'arm': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'body': (0, -1)}, 'walk3': {'arm': (0, -1)},
    'atk0': {'body': (-2, 1), 'arm': (-2, -2), 'armF': (-2, -2)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (2, 0), 'arm': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'arm': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'arm': 'head', 'armF': 'head', 'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
