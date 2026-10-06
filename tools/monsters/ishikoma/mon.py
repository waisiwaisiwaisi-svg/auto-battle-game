# イシコマ（いわ・エスパー × 狛犬）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 阿の 大口、たてがみは 石灯籠の 笠の 段、胴は 小さく 丸く）
META = dict(id='ishikoma', name='イシコマ', types=['rock', 'psychic'], base='狛犬', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2c28',
    'S': '#e0e0cc', 'T': '#9c9c86', 'U': '#58594c',      # 石
    'J': '#ffb2f0', 'K': '#cc44b4',                      # 宝珠（念力）
    'R': '#d0344c', 'E': '#4a1020',                      # 口の 中
    'Y': '#ffd84a', 'O': '#c07a1a',                      # 目
    'w': '#ffffff',
}
LIGHT = set('SJYw')
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
STONE = {'1': 'STU', '2': 'STU', '3': 'STU'}; STONE2 = {'1': 'STU', '2': 'TTU', '3': 'STU'}
DK = {'S': 'T', 'T': 'U', 'U': 'l', 'w': 'T'}

# ---- たてがみ ＝ 石灯籠の 笠（3段、のきの 先が 巻き毛の ように 反りあがる）----
def mane():
    g = M(28, 32,
          ('p', '1', [(9, 1), (17, 1), (22, 6), (27, 2), (26, 10), (2, 10), (0, 2), (4, 6)]),
          ('p', '2', [(3, 10), (24, 10), (26, 15), (28, 11), (28, 20), (0, 20), (0, 11), (1, 15)]),
          ('p', '3', [(1, 20), (27, 20), (27, 26), (23, 31), (5, 31), (1, 26)]),
          ('e', '1', 13, 1.5, 3, 2))                                    # 笠の 上の 宝珠の つまみ
    CURL = ['.kkk.', 'kSSUk', 'kSkUk', 'kUUkk', '.kk..']                              # 巻き毛（石の 渦）
    return _mane(g, CURL)
def _mane(g, CURL):
    """笠の 段ごとに 明暗を 変え、のきの 先と すそに 石の 巻き毛を 打つ"""
    shade(g, STONE2, lw=2, dw=2)
    for rows, x, y in ((CURL, 0, 5), (CURL, 23, 5), (CURL, 0, 15), (CURL, 23, 15), (CURL, 3, 25), (CURL, 8, 26), (CURL, 13, 26), (CURL, 18, 25),
                       (['S', 'S', 'S'], 13, 3), (['SSSS'], 6, 11), (['SSSS'], 4, 21)):
        pix.stamp(g, rows, x, y)
    return pix.outline(pix.rows_of(g))
MANE = mane()

# ---- 頭（大きい）：阿の 大口（見せ所）は いつも 開いて 牙が 並ぶ ----
def head(wide=False):
    g = M(26, 22, ('e', '1', 12, 11, 12, 11), ('r', '1', 13, 5, 25, 21))
    shade(g, STONE, lw=2, dw=3)
    top = 9 if wide else 11
    pix.poly(g, [(12, 13), (26, top), (26, 20), (12, 15)], 'E')
    for y in range(22):
        for x in range(26):
            if g[y][x] != 'E': continue
            if y > 0 and g[y - 1][x] in 'STU' and x % 3 != 1: g[y][x] = 'w'           # 上の 牙
            elif y + 1 < 22 and g[y + 1][x] in 'STU' and x % 3 == 0: g[y][x] = 'w'   # 下の 牙
            elif y + 2 < 22 and g[y + 2][x] in 'STU' and x > 16: g[y][x] = 'R'       # 舌
    for (x, y) in ((24, top - 1), (25, top - 1)): g[y][x] = 'w'                     # 上の 大きな 牙
    for (x, y) in ((4, 2), (5, 2), (6, 1), (7, 1), (3, 3), (2, 4)):
        if g[y][x] == 'T': g[y][x] = 'S'
    for (x, y) in ((22, 4), (23, 4), (24, 4), (25, 5)): g[y][x] = 'U'             # 鼻の しわ
    for x in range(9, 20): g[3 + (x - 9) // 4][x] = 'U'; g[2 + (x - 9) // 4][x] = 'S'   # 太い 石の まゆ
    g[5][24] = 'k'; g[6][25] = 'k'                                               # 鼻の 穴
    return pix.outline(pix.rows_of(g))
HEAD, HEAD_WIDE = head(), head(True)
EYE, EYE_ALT = eye('Y', 'O', glow='J')
JEWEL = ['...k...', '..kJk..', '.kwJJk.', 'kwJJJKk', 'kJJJKKk', '.kJKKk.', '..kkk..']
JEWEL_GLOW = ['...k...', '..kwk..', '.kwwJk.', 'kwwwJJk', 'kJwJJKk', '.kJJKk.', '..kkk..']

# ---- 胴（小さく 丸い）・しっぽ（宝珠形に 巻く 石の 炎）----
BODY = P(M(22, 16, ('e', '1', 11, 8, 11, 8)), STONE, [(['..UUU', '.U...U', 'U'], 9, 7)], lw=2, dw=3)
TAIL = P(M(14, 21, ('p', '1', [(11, 21), (4, 17), (1, 11), (4, 5), (9, 0), (9, 6), (12, 10), (14, 16)])), STONE, [
    (['.UU', 'U..U', 'U.UU', '.U'], 5, 8)], lw=2, dw=2)
TAIL2 = P(M(14, 21, ('p', '1', [(11, 21), (4, 17), (1, 11), (3, 5), (7, 1), (8, 6), (12, 10), (14, 16)])), STONE, [
    (['.UU', 'U..U', 'U.UU', '.U'], 5, 8)], lw=2, dw=2)

# ---- 足：短く 太い 石の 足、白い 爪 ----
LEG = [
    '.kkkkkk..',
    'kSSTTTUk.',
    'kSTTTTUk.',
    'kSTTTUUk.',
    'kTTTTUUk.',
    'kSTTTUUUk',
    'kTTTTTUUk',
    'kTUTUTUUk',
    'kwkwkwkkk',
]
LEG_N = opentop(LEG); LEG_F = dark(LEG, DK)

# ---- 念力の ほえ声（攻撃の エフェクト：口から 広がる 輪）----
WAVE = [
    '..kkk.....kk.',
    '.kJJk....kKk.',
    'kJkk....kKk..',
    'kJk....kJk...',
    'kJk....kJk...',
    'kJk....kJk...',
    'kJkk....kKk..',
    '.kJJk....kKk.',
    '..kkk.....kk.',
]
WAVE2 = [
    '...kk.....kkk..',
    '..kKk....kJJk..',
    '.kKk....kJkk...',
    'kJk....kJk.....',
    'kJk....kJk.....',
    'kJk....kJk.....',
    '.kKk....kJkk...',
    '..kKk....kJJk..',
    '...kk.....kkk..',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='legHF', g='legB', x=15, y=51, rows=LEG_F),
        dict(n='legFF', g='legA', x=31, y=51, rows=LEG_F),
        dict(n='tail', g='tail', x=3, y=22, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='body', g='body', x=10, y=36, rows=BODY),
        dict(n='legH', g='legA', x=10, y=51, rows=LEG_N),
        dict(n='legF', g='legB', x=27, y=51, rows=LEG_N),
        dict(n='mane', g='mane', x=14, y=8, rows=MANE),
        dict(n='head', g='head', x=27, y=15, rows=HEAD, alt={NB: HEAD_WIDE}),
        dict(n='eye', g='head', x=38, y=21, rows=EYE, alt=EYE_ALT),
        dict(n='jewel', g='head', x=30, y=16, rows=JEWEL, alt={'atk0|atk1|atk2|idle2': JEWEL_GLOW}),
        dict(n='wave', g='fx', x=56, y=21, rows=WAVE, alt={'atk2': WAVE2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'mane': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'body': (0, -1)}, 'walk3': {},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'tail': (1, 0)}, 'atk1': {'root': (3, 0), 'head': (1, -1)}, 'atk2': {'root': (4, 0), 'head': (1, -1), 'fx': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'mane': (-1, 0)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'mane', 'mane': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
