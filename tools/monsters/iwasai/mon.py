# イワサイ（いわ・じめん × サイ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
EYE_BOX = (43, 32, 5, 9)
META = dict(id='iwasai', name='イワサイ', types=['rock', 'ground'], base='サイ', size='L')
PAL = {
    'k': '#101018', 'l': '#28242e',
    'D': '#a8aab8', 'E': '#6c6e84', 'F': '#3e4052',      # 花こう岩の 皮（明・中・暗）
    'S': '#f2d496', 'T': '#c8924a', 'U': '#7c5428',      # 砂岩の 角・よろい（明・中・暗）
    'r': '#ff4a2a', 'q': '#9a1a24', 'w': '#ffffff',
    'p': '#e6a69c',                                      # 古傷（うす桃）
}
LIGHT = set('DSw')
KEEP_BLACK = set('wrq')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, Lc, Mc, Dc, lt=2, dk=4):
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = Mc
            if dn <= dk or rt <= 2: c = Dc
            if dn == dk + 1 and (x + y) % 2: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if up <= 1 and rt <= 2: c = Mc
            out[y][x] = c
    return out

# ---- 胴：肩が もり上がった くさび形 → 陰影 → 皮の ひだ・ひびを 手で ----
# デフォルメ：胴を 小さく 丸く（50x34 → 37x26）。手で 置いた 点も 同じ 比で ちぢめる
FX, FY = .74, .77
def P(pts): 
    out = []
    for (x, y) in pts:
        q = (round(x * FX), round(y * FY))
        if q not in out: out.append(q)
    return out
def body():
    W, H = 37, 26; g = grid(W, H)
    ellipse(g, 25, 11.5, 12, 11.5, '#'); ellipse(g, 11, 14.5, 10.5, 9.5, '#')
    poly(g, [(10, 5), (25, 0), (25, 15), (10, 15)], '#')
    for y in range(24, H):
        for x in range(W): g[y][x] = '.'
    out = shade(g, 'D', 'E', 'F', lt=2, dk=5)
    # 肩と ももの ひだ（サイの 皮の 境目）
    for pts in (((29, 4), (28, 5), (28, 6), (27, 7), (27, 8), (27, 9), (27, 10), (27, 11), (27, 12), (28, 13), (28, 14), (29, 15), (29, 16), (30, 17), (31, 18)),
                ((12, 9), (11, 10), (11, 11), (10, 12), (10, 13), (10, 14), (10, 15), (11, 16), (11, 17), (12, 18)),
                ((18, 23), (19, 24), (20, 24), (21, 24), (22, 24), (23, 24), (24, 24), (25, 23), (26, 23))):
        for (x, y) in P(pts):
            out[y][x] = 'l'
            if out[y][x - 1] == 'E': out[y][x - 1] = 'D'
    # 岩肌の ひび・こぶ
    for (x, y) in P(((20, 10), (21, 11), (21, 12), (38, 18), (39, 19), (39, 20), (6, 20), (7, 21))):
        out[y][x] = 'l'
    for (x, y) in P(((16, 6), (24, 4), (5, 15), (33, 8), (40, 12), (18, 16), (36, 24))):
        if out[y][x] in 'EF': out[y][x] = 'D'; out[y + 1][x] = 'F'
    # 肩の 砂岩の よろい（体の 一部を 砂岩に：ふちは 濃い 線、中に ひび）
    arm = grid(W, H)
    ellipse(arm, 24.5, 7, 9.6, 8, '#'); ellipse(arm, 12.5, 9, 6.7, 5.4, '#')
    M = {'D': 'S', 'E': 'T', 'F': 'U'}
    for y in range(H):
        for x in range(W):
            if arm[y][x] == '#' and out[y][x] in M and y < 13: out[y][x] = M[out[y][x]]
    for y in range(H):
        for x in range(W):
            if out[y][x] in 'STU' and y < 14:
                if any(0 <= y + dy < H and 0 <= x + dx < W and out[y + dy][x + dx] in 'DEF' for dy, dx in ((1, 0), (0, 1), (0, -1))): out[y][x] = 'l'
    for x in range(W):
        ys = [y for y in range(14) if out[y][x] in 'STU']
        if not ys: continue
        for y in ys:
            d = y - ys[0]
            if out[y][x] == 'T' and (d <= 2 or (d == 3 and (x + y) % 2)) and x < 30: out[y][x] = 'S'
            if out[y][x] == 'T' and y >= ys[-1] - 1: out[y][x] = 'U'
    for pts in (((26, 2), (26, 3), (25, 4), (25, 5), (26, 6), (26, 7)), ((36, 4), (37, 5), (37, 6), (38, 7)), ((30, 10), (31, 11), (32, 11), (33, 12)),
                ((17, 8), (18, 9), (18, 10))):
        for (x, y) in P(pts):
            if out[y][x] in 'STU': out[y][x] = 'l'
            if out[y][x + 1] == 'T': out[y][x + 1] = 'S'
    return outline(rows_of(out))

# 背の 砂岩の よろい板（重なる 盾）
CRAG_A = ['...kk.', '..kSk.', '.kSTkk', '.kSTUk', 'kSTTUk', 'kSTUUk']
CRAG_B = ['..kk', '.kSk', 'kSTk', 'kSUk', 'kTUk']
# デフォルメで 頭を ひと回り 大きく（23x17 → 27x18）：耳・砂岩の まゆ板・鼻の あな・口の 線
HEAD = [
    '...kk......................',
    '..kDDk.....................',
    '.kDDEFk....................',
    '.kDEEEFkkkkkk..............',
    'kDDEEEEDDDDDDkk............',
    'kDEEEEEEEEEEEEEkk..........',
    'kDEEEEEkkkkkkEEEEkk........',
    'kDEEEEkSSSSSSkkkkEEkk......',
    'kDEEEEkTTTTTUUkEEEEEEkk....',
    'kEEEEEEkk.....kDDDDEEEEkk..',
    'kEEEEEEEk.....kEEEEEEEEEEk.',
    'kEEEElEEEkkkkkEEEEEEEEEDDDk',
    'kFEEEElEEEEEEEEEEEEEEEkEEDk',
    'kFEEEEElEEEEllEEEEEEEEEEEFk',
    'kFFEEEEEEEEEEEkkkkkkkkkkkk.',
    '.kFFEEEEEEEEEFFFFFFFFFFk...',
    '..kFFFFFFFFFFFFFFFFFFFk....',
    '...kkkkkkkkkkkkkkkkkkk.....',
]
HEAD_ROAR = HEAD[:14] + [
    'kFFEEEEEEEEEEkkkkkkkkkkkkk.',
    '.kFFEEEEEEEEkUUUUUUUUUUk...',
    '..kFFEEEEEEEEkkkkkkkkkk....',
    '...kFFFFFFFFFFFk...........',
    '....kkkkkkkkkkk............',
]
# O 傷の 目：額から ほおへ たてに 走る 古傷（うす桃 p）。砂岩の まゆ板は 傷の ところで 欠け、まぶたも 切れて いる。
# 傷を またいで 暗い 赤の 虹彩（q）に 赤い 光（r）と 黒い ひとみ。見えて いる 片目に 傷（横向きなので もう片方は 見えない）
def _scar(e1, e2, lid='.'):
    return ['....p..', '....p..', '...k...', '...k...', '.' + e1 + '.', '.' + e2 + '.', '...' + ('p' if lid == '.' else lid) + '...', '..p....', '..p....']
EYE = _scar('rqpkq', 'qqpkq')
EYE_ALT = {'blink': _scar('kkpkk', 'EEpEE'), 'hit': _scar('kkpkk', 'EqpqE'), 'atk0|atk1|atk2': _scar('wrprr', 'rqpkq'),
           'ko': _scar('kEpEk', 'EkpkE')}
HORN = [
    '.......kk',
    '......kSk',
    '......kSTk',
    '.....kSSTk',
    '.....kSTTk',
    '....kSSTUk',
    '....kSTTUk',
    '...kSSTTUk',
    '...kSTTTUk',
    '..kSSTlTUk',
    '..kSTTTlUk',
    '.kSSTTTTUk',
    '.kSTTTTTUUk',
    'kSSTlTTTUUk',
    'kSTTTlTTUUk',
    'kSTTTTTUUUk',
    'kkkkkkkkkkk',
]
HORN2 = ['...kk', '..kSk', '.kSTk', '.kSUk', 'kSTUk', 'kSTUk', 'kkkkk']
LEG = [
    'kkkkkkkkk.', 'kDEEEEEFk.', '.kDElEEFk.', '.kDEEEFFk.',
    'kDEEEElFFk', 'kEEEEEEFFk', 'kFFFFFFFFk', 'kSkSkSkkk.',
]
DARK = {'D': 'E', 'E': 'F', 'F': 'l', 'S': 'T', 'T': 'U'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 突進の 土けむり（うしろに 残る）
DUST1 = [
    '.......kkk.....',
    '..kkk.kSSTk....',
    '.kSSTkSTTTUk.kk',
    'kSTTTTTTUUUkkTk',
    'kTTUUUUUUUkk.k.',
    '.kkkkkkkkk.....',
]
DUST2 = [
    '...........kkk.......',
    '....kkk...kSSTk......',
    '...kSSTk.kSTTTUk..kk.',
    '.kkSTTTUkSTTUUUkkkSTk',
    'kSSTTUUUTTUUUUkSSTTUk',
    'kTTUUUUUUUUUkkkTTUUk.',
    '.kkkkkkkkkkk...kkkk..',
]
SPEED = ['kkkkkkk.....', '............', '...kkkkkkkk.', '............', 'kkkkkk......']
ROCKS = ['..kk......kk..', '.kSTk....kTUk.', '..kUk.....kk..', '.......kk.....', '......kSTk....', '.......kk.....']
BODY = body()
def top(x, x0=4, y0=30):
    for j, r in enumerate(BODY):
        if 0 <= x - x0 < len(r) and r[x - x0] != '.': return y0 + j
    return 60
def on_back(x, rows, sink=2): return (x, top(x + len(rows[-1]) // 2) - len(rows) + sink, rows)

def layers():
    return [
        dict(n='dust1', g='dust', x=-6, y=52, rows=DUST1, only='atk0'),
        dict(n='dust2', g='dust', x=-8, y=50, rows=DUST2, only='atk1|atk2'),
        dict(n='speed', g='dust', x=-2, y=30, rows=SPEED, only='atk1'),
        dict(n='legFF', g='legB', x=34, y=52, rows=dark(LEG)),
        dict(n='legHF', g='legA', x=13, y=52, rows=dark(LEG)),
        *[dict(n='crag%d' % i, g='body', x=x, y=y, rows=r) for i, (x, y, r) in enumerate((on_back(9, CRAG_B), on_back(14, CRAG_A), on_back(20, CRAG_B), on_back(25, CRAG_A)))],
        dict(n='body', g='body', x=4, y=30, rows=BODY),
        dict(n='legH', g='legB', x=8, y=53, rows=LEG),
        dict(n='horn2', g='head', x=45, y=24, rows=HORN2),
        dict(n='head', g='head', x=34, y=27, rows=HEAD, alt={'atk2': HEAD_ROAR}),
        dict(n='horn', g='head', x=49, y=21, rows=HORN),
        dict(n='eye', g='head', x=42, y=32, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='legA', x=29, y=53, rows=LEG),
        dict(n='rocks', g='fx', x=52, y=8, rows=ROCKS, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 2), 'head': (0, 3), 'legB': (-1, 0), 'dust': (2, 0)},
    'atk1': {'root': (6, 0), 'body': (0, 1), 'head': (1, 3), 'legA': (2, -1), 'legB': (-2, 0), 'dust': (-6, 0)},
    'atk2': {'root': (8, 0), 'body': (0, -1), 'head': (1, -3), 'dust': (-8, 0)},
    'hit': {'root': (-3, 0), 'head': (-3, -2), 'body': (0, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'dust': 'root', 'fx': 'root'}
