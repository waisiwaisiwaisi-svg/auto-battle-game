# ズツキヒツジ（かくとう・いわ × ヒツジ）手打ち GBA風
import math
import pix
META = dict(id='zutsukihitsuji', name='ズツキヒツジ', types=['fighting', 'rock'], base='ヒツジ', size='M')
EYE_BOX = (44, 32, 8, 6)   # よこ瞳（idle0）
PAL = {
    'k': '#101018', 'l': '#3c3028',
    'A': '#f6f0e0', 'B': '#d0c4a6', 'C': '#8e8066',
    'D': '#76708a', 'E': '#4a4560', 'F': '#2c283a',
    'R': '#dcc8a4', 'S': '#a08868', 'T': '#5e4a38',
    'Y': '#ffd030', 'y': '#b07818', 'X': '#d83a3a', 'w': '#ffffff',
}
LIGHT = set('ADRYw')
KEEP_BLACK = set('wYy')

def shade(rows, ramps, low=99):
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            hi, mid, lo = ramps[m]
            def e(dy, dx):
                yy, xx = y + dy, x + dx
                return not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m
            a = e(-1, 0) or e(-2, 0) or (e(0, -1) and y < low)
            b = e(1, 0) or e(0, 1) or e(1, 1) or e(0, 2)
            c = lo if y >= low else mid
            if a and not b: c = hi
            elif b and not a: c = lo
            o[y][x] = c
    return pix.rows_of(o)
def put(base, over, x=0, y=0):
    g = pix.grid_of(base); w = max(len(r) for r in over) + x; h = len(over) + y
    if w > len(g[0]): g = [r + ['.'] * (w - len(r)) for r in g]
    while len(g) < h: g.append(['.'] * len(g[0]))
    pix.stamp(g, over, x, y); return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'D': 'E', 'E': 'F', 'R': 'S', 'S': 'T', 'X': 'l', 'w': 'C'}
def dark(rows): return pix.recolor(rows, DARK)
def notop(r): return ['.' * len(r[0])] + r[1:]

# ---- 羊毛の 胴：ふちは もこもこ、中は 巻き毛の 粒 ----
# もこもこの 玉（中心と 半径は 手で 置いた）
PUFFS = [(6, 7, 4.5), (12, 4, 4.5), (19, 3, 4.5), (26, 4, 4.5), (32, 8, 4.2), (3, 13, 4), (34, 14, 3.6),
         (5, 19, 4), (12, 21, 4), (20, 21, 4), (28, 20, 4), (33, 18, 3.4),
         (11, 11, 3.6), (19, 10, 3.6), (26, 11, 3.6), (15, 16, 3.4), (23, 15, 3.4), (8, 15, 3)]
# デフォルメ：玉の 位置を 横 .76・たて .82 に ちぢめ、小さく 丸い 胴に
SX, SY, SR = .76, .82, .8
PUFFS = [(round(cx * SX + 1, 1), round(cy * SY + 1, 1), round(r * SR + .3, 1)) for (cx, cy, r) in PUFFS]
def body():
    W, H = 31, 23; g = pix.grid(W, H)
    pix.ellipse(g, 15, 11.5, 12, 8, 'B')
    for (cx, cy, r) in PUFFS: pix.ellipse(g, cx, cy, r, r, 'B')
    # 玉ごとに 左上が 明るく 右下が 暗い（手前の 玉が 上書き）
    for (cx, cy, r) in PUFFS:
        for y in range(H):
            for x in range(W):
                dx, dy = x + .5 - cx, y + .5 - cy; d = (dx * dx + dy * dy) ** .5
                if d > r: continue
                if d > r - 1.3 and dx + dy > 1.5: g[y][x] = 'C'
                elif d > r - 1.6 and dx + dy < -1.5: g[y][x] = 'A'
                elif g[y][x] not in 'AC': g[y][x] = 'B'
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.' and y > 18 and g[y][x] == 'B': g[y][x] = 'C'
    return pix.outline(pix.rows_of(g))
BODY = body()
# 背中から つき出る 岩の とげ
SPIKE = [
    '...k.....',
    '..kRk....',
    '..kRSk...',
    '.kRRSk...',
    '.kRSSTk..',
    'kRRSSTk..',
    'kRSSTTTk.',
    'kRSSTTTk.',
    'kSSTTTTk.',
]
# 羊毛に うまった 岩（未使用）
ROCK = [
    '...kkk....',
    '..kRRSkk..',
    '.kRRSSSTk.',
    'kRRSSSSTk.',
    'kRSSSTTTTk',
    '.kTTTTTkk.',
    '..kkkkk...',
]
ROCK2 = [
    '.kkk..',
    'kRRSk.',
    'kRSTk.',
    '.kkk..',
]
# ---- 足：こげた 灰色、前足に 赤い 布、石の ひづめ ----
# デフォルメ：短く 太く（付け根は 羊毛の 中へ 3ドット 食いこむ）
FLEG_M = [
    '.#####.',
    '######.',
    '######.',
    '.XXXX..',
    '.XXXX..',
    '.####..',
    '.XXXX..',
    '.####..',
    '.%%%%..',
    '%%%%%%.',
]
FLEG = notop(pix.outline(put(shade(FLEG_M, {'#': 'DEF', '%': 'RST', 'X': 'XXl'}), [
    '', '', '', '', '.X..l', '', '.X..l', '', '', '...k',
])))
HLEG_M = [
    '..######.',
    '.########',
    '..######.',
    '...####..',
    '...###...',
    '...###...',
    '...###...',
    '...###...',
    '..%%%%...',
    '.%%%%%%..',
]
HLEG = notop(pix.outline(put(shade(HLEG_M, {'#': 'DEF', '%': 'RST'}), [
    '', '', '', '', '', '', '', '', '', '....k',
])))

# ---- 頭（手打ち）：ローマ鼻の 黒い 顔、横長の ひとみ ----
HEAD = [
    '......kkkkkkkk......',
    '....kkRRRRRRRSkk....',
    '...kRRRSSSSSSSTTk...',
    '..kRRSSSTSSSSSSTTk..',
    '.kRSSSSSSSSkkkkkkTk.',
    'kDDEEEEEEEEkEEEEkTk.',
    'kDEEEEEEEEEEkkkkDkTk',
    'kEEEEEEEEEEEDDDDDDkk',
    'kFEEEEEEEEEEEEEEEEDk',
    '.kFEEEFEEEEEEEEEEEDk',
    '.kFFEEFFEEEEEEEEEEEk',
    '..kFFEEEEEEEEEEEkkEk',
    '...kFFFEEEEEEEEkFFk.',
    '....kkFFFFFFFFFFkk..',
    '......kkkkkkkkkk....',
]
HEAD_OPEN = HEAD[:11] + [
    '..kFFEEEEEEEEEkkkkk.',
    '...kFFFEEEEEEkXXk...',
    '....kkFFFFFFFFkk....',
    '......kkkkkkkk......',
]
# 目：よこ瞳（G）。大きく 広い 金の 虹彩（Y 明・y 暗）の まん中に 横長の 四角い ひとみ（k、4×2）。白い ハイライト 1点。上まぶたは 前へ 下がる
EYE = ['.kkkkkkk', 'kwYYYkkk', 'kYkkkkyk', 'kykkkkyk', '.kyyyyk.', '..kkkk..']
EYE_ALT = {'blink': ['.kkkkkkk', 'kEEEEEkk', 'kEEEEEEk', 'kkkkkkkk', '.EEEEEE.', '........'],
           'hit': ['.kkkkkkk', 'kkkkkkkk', 'kEEEEEkk', 'kYkkkkyk', '.kkkkkk.', '........'],
           'atk0|atk1|atk2': ['.kkkkkkk', 'kwwwYkkk', 'kYYYYYYk', 'kYkkkkyk', '.kyyyyk.', '..kkkk..'],
           'ko': ['.kkkkkkk', '.EkEEkE.', '..EkkE..', '..EkkE..', '.EkEEkE.', '........']}
FLUFF = [
    '..kk.kk..',
    '.kAAkAAk.',
    'kAABAABBk',
    'kBBCBBCk.',
    '.kkkkkk..',
]

# ---- 岩の ねじれ角：らせんを 太い 筆で なぞり、段の すじを 入れる ----
def horn():
    N = 19; g = pix.grid(N, N); band = [[0] * N for _ in range(N)]
    cx, cy = 9.5, 9.5; steps = 260
    for i in range(steps):
        t = i / steps
        th = -math.pi / 2 - t * 2.1 * math.pi
        r = 7.6 - 5.4 * t; w = 3.2 - 1.7 * t
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        for y in range(N):
            for x in range(N):
                if (x + .5 - px) ** 2 + (y + .5 - py) ** 2 <= w * w:
                    if g[y][x] == '.': g[y][x] = '#'; band[y][x] = int(t * 13)
    s = pix.grid_of(shade(pix.rows_of(g), {'#': 'RST'}))
    for y in range(N):
        for x in range(N):
            if g[y][x] == '#' and band[y][x] % 2 == 1 and s[y][x] == 'S':
                if (x + y) % 2 == 0: s[y][x] = 'T'
    return pix.outline(pix.rows_of(s))
HORN = horn()

# ---- 頭突きの 衝撃（攻撃）----
IMPACT = [
    '........kk..........',
    '..kk...kYk....kk....',
    '.kRSk..kYk...kRSk...',
    '..kkk.kYYk..kSTk....',
    '....kkYwYk.kkk......',
    '.kkk.kYwwYkkk.kkk...',
    'kYYYkYwwwwYYYkYYYk..',
    'kYwwwwwwwwwwwwwwYYk.',
    'kYYYkYwwwwYYYkYYYk..',
    '.kkk.kYwwYkkk.kkk...',
    '....kkYwYk.kkk......',
    '..kkk.kYYk..kRSk....',
    '.kRSk..kYk...kSTk...',
    '..kk...kYk....kk....',
    '........kk..........',
]
IMPACT2 = [
    '.kk.........kk...',
    'kRSk..kk...kRSk..',
    '.kk..kSTk...kk...',
    '......kk.....kk..',
    '..kk........kSTk.',
    '.kSTk..kk....kk..',
    '..kk..kRSk.......',
    '.......kk...kk...',
    '...kk......kRk...',
    '..kRSk......k....',
    '...kk............',
]
TAIL = [
    '.kk..',
    'kAAk.',
    'kABBk',
    '.kCk.',
    '..k..',
]

NB = 'atk1|atk2'
HX, HY = 34, 28     # 頭の 位置（頭は 元の 大きさ）
def layers():
    return [
        dict(n='hlegF', g='legB', x=17, y=50, rows=dark(HLEG)),
        dict(n='flegF', g='legB', x=25, y=50, rows=dark(FLEG)),
        dict(n='tail', g='body', x=8, y=35, rows=TAIL),
        dict(n='sp1', g='body', x=13, y=25, rows=SPIKE),
        dict(n='sp2', g='body', x=20, y=23, rows=SPIKE),
        dict(n='sp3', g='body', x=27, y=24, rows=SPIKE),
        dict(n='body', g='body', x=10, y=31, rows=BODY),
        dict(n='hleg', g='legA', x=12, y=50, rows=HLEG),
        dict(n='fleg', g='legA', x=31, y=50, rows=FLEG),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='horn', g='head', x=HX - 8, y=HY - 3, rows=HORN),
        dict(n='eye', g='head', x=HX + 10, y=HY + 4, rows=EYE, alt=EYE_ALT),
        dict(n='impact', g='head', x=HX + 17, y=HY - 2, rows=IMPACT, alt={'atk2': IMPACT2}, only=NB),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-3, 0), 'body': (0, 1), 'head': (-1, 3)},
    'atk1': {'root': (7, 0), 'head': (2, 2)},
    'atk2': {'root': (5, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -2)},
    'ko': {'_flip': True, 'head': (0, 2)},
}
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
