# イカリタガメ（むし・みず × タガメ）手打ち GBA風・デフォルメ（2〜3頭身：大きな くさび形の 頭、平たい 背は 小さく、前脚は 鉄の 錨）
META = dict(id='ikaritagame', name='イカリタガメ', types=['bug', 'water'], base='タガメ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2618',
    'B': '#c4b06c', 'C': '#7e6c38', 'D': '#40361e',      # 体（どろ色）
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

# ---- 背（平たい だ円の 羽）：小さく、羽の 重なりの すじ、ふちに 水の つや ----
BODY = P(M(26, 15, ('e', '1', 13, 7.5, 13, 7.5)), BUG, [
    (['..AAAA', '.A', 'A'], 3, 1),                           # 水に ぬれた つや
    (['......DD', '....DD', '..DD', 'DD'], 12, 2),            # 羽の 重なり
    (['DDDDDDDDDD'], 2, 9),
], lw=2, dw=3)

# ---- 頭（大きい くさび形）：前へ とがる、下に 針の くちばし ----
HEAD = P(M(21, 17, ('e', '1', 9, 9, 9, 8), ('p', '1', [(6, 1), (17, 4), (21, 9), (17, 14), (6, 17)])), BUG, [
    (['..BBB', '.B', 'B'], 3, 2),
    (['DDDDDDDDD'], 1, 12),                                    # 頭と むねの さかい
    (['D', 'D', 'D'], 14, 13),
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
ANCHOR_SWING = pix.rot90(pix.rot90(pix.rot90(ANCHOR)))   # 前へ ふり出す（90度）
FEMUR = P(M(15, 17, ('p', '1', [(1, 17), (0, 13), (10, 1), (13, 0), (15, 3), (5, 17)])), BUG, [(['B', 'B', 'B'], 9, 3)], lw=1, dw=2)
FEMUR_FWD = P(M(17, 9, ('p', '1', [(0, 9), (0, 4), (14, 0), (17, 3), (16, 6), (4, 9)])), BUG, [], lw=1, dw=2)

# ---- 泳ぐ 足（4本 → 2本に まとめる）：短く 太く、すその 毛は 水色 ----
LEG = [
    '.kkkkk...',
    'kBBCCCk..',
    'kBCCCDk..',
    '.kBCCk...',
    '.kBCDk...',
    '..kBCk...',
    '..kBCk...',
    '.kBCCDk..',
    '.kBCDDk..',
    'kACACACk.',
    '.kkkkkkk.',
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
        dict(n='anchorF', g='armF', x=40, y=22, rows=dark(ANCHOR, DK), not_=NB),
        dict(n='femurF', g='armF', x=35, y=24, rows=dark(FEMUR, DK), not_=NB),
        dict(n='legF', g='legB', x=12, y=47, rows=LEG_F),
        dict(n='body', g='body', x=4, y=33, rows=BODY),
        dict(n='legN', g='legA', x=22, y=47, rows=LEG_N),
        dict(n='head', g='head', x=24, y=21, rows=HEAD),
        dict(n='eye', g='head', x=34, y=25, rows=EYE, alt=EYE_ALT),
        dict(n='beak', g='head', x=42, y=35, rows=BEAK),
        dict(n='femur', g='arm', x=38, y=25, rows=FEMUR, alt={NB: FEMUR_FWD}),
        dict(n='anchor', g='arm', x=44, y=23, rows=ANCHOR, not_=NB),
        dict(n='anchorS', g='arm', x=53, y=22, rows=ANCHOR_SWING, only=NB),
        dict(n='splash', g='arm', x=62, y=36, rows=SPLASH, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, 1)}, 'idle3': {'arm': (0, 1)}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'arm': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'body': (0, -1)}, 'walk3': {'arm': (0, -1)},
    'atk0': {'body': (-2, 1), 'arm': (-2, -2), 'armF': (-2, -2)}, 'atk1': {'root': (3, 0), 'arm': (0, 8)}, 'atk2': {'root': (5, 0), 'arm': (0, 8)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'arm': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'arm': 'head', 'armF': 'head', 'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
