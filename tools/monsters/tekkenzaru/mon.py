# テッケンザル（かくとう・はがね × 大猿）手打ち GBA風・デフォルメ（2〜3頭身：頭は 元の 大きさ、
# 胴は 肩の 高い 小さな ゴリラ型、足は 短く 曲げて 見せる。見せ所の 鉄の こてと こぶしは 大きく）
from pix import grid, rows_of, outline, poly, ellipse
META = dict(id='tekkenzaru', name='テッケンザル', types=['fighting', 'steel'], base='大猿（ゴリラ）', size='L')
PAL = {
    'k': '#101018', 'l': '#2e1a1c',
    'A': '#a8705a', 'B': '#6c4036', 'C': '#3c2224',      # 毛（赤黒）
    'D': '#b4a8a0', 'E': '#6e6260',                      # はだ（顔・手）
    'S': '#f2f6fa', 'T': '#a4b0c2', 'U': '#566276',      # はがね
    'R': '#ff3424', 'O': '#ffb22e', 'w': '#ffffff',
}
LIGHT = set('ADSOw')
KEEP_BLACK = set('wRO')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'S': 'T', 'T': 'U'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=44, H=44):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.' and 0 <= dy + j < H and 0 <= dx + i < W: g[dy + j][dx + i] = c
    return [''.join(r) for r in g]
def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, L='A', M='B', D='C', lt=2, dkn=3, rk=3):
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = M
            if dn <= dkn or rt <= rk: c = D
            if up <= lt or lf <= lt: c = L
            if (lf <= lt and dn <= dkn) or (up <= lt and rt <= rk): c = M
            out[y][x] = c
    return out

# ---- 胴：肩（右上）が 高く、背中が 丸く おしり（左下）へ 下がる ゴリラ型。毛の すじは 手で ----
def body():
    W, H = 31, 20; g = grid(W, H)
    poly(g, [(0, 13), (3, 7), (10, 2), (18, 0), (26, 1), (30, 5), (31, 13), (27, 19), (16, 20), (3, 20)], '#')
    out = shade(g)
    for (x, y) in ((10, 6), (11, 7), (16, 4), (17, 5), (22, 3), (23, 4), (7, 11), (8, 12), (14, 10), (15, 11), (21, 9), (22, 10), (27, 8), (28, 9),
                   (5, 15), (6, 16), (12, 14), (13, 15), (19, 13), (20, 14), (25, 12), (26, 13), (16, 17), (17, 18)):
        if out[y][x] == 'B': out[y][x] = 'C'
        elif out[y][x] == 'A': out[y][x] = 'B'
    return outline(rows_of(out))
BODY = body()
# 鎖（たすきがけ）：たて・よこの 輪を 交互に
LINK_V = ['.SS.', 'S..T', 'S..U', '.UU.']
LINK_H = ['.ST.', '.TU.']
CHAIN = place([(LINK_V if i % 2 == 0 else LINK_H, x, y) for i, (x, y) in enumerate(
    [(3, 15), (5, 13), (7, 11), (9, 9), (10, 7), (12, 5), (14, 3), (16, 1), (19, 0)])], W=34, H=26)

HEAD = [
    "....AAAAAA........",
    "..AABBBBBBAA......",
    ".ABBBBBBBBBBA.....",
    "ABBBBBBBBBBBBA....",
    "ABBBBSSSSSSSSTU...",
    "ABBBBTTkTTTTkTU...",
    "BBBBEDDDDDDDDDDE..",
    "BBBBEDDDDDDDDDDDE.",
    "BBBBEDDDDDDDEDEDE.",
    "BBBBEDDDDDDDDDDDE.",
    "BBBBEDkkkkkkkkkkk.",
    "BBBBEDkwkkkkkkwk..",
    ".BBBBEDwDDDDDDwE..",
    ".CBBBEEDDDDDDDE...",
    "..CCBBBEEEEEEE....",
    "....CCCCCC........",
]
HEAD_ROAR = HEAD[:9] + [
    "BBBBEDkkkkkkkkkkk.",
    "BBBBEkwkwkkkkwkwk.",
    "BBBBEkRRRRRRRRRk..",
    ".BBBEkwkkkkkkwwk..",
    ".CBBBEwDDDDDDwE...",
    "..CCBBBEEEEEEE....",
    "....CCCCCC........",
]
# 目：ハイライト w ＋ 虹彩 2色（O 明・R 暗）＋ たての ひとみ k、まゆと 下まぶたで かこむ
EYE = ['kkkkkk', 'kwOkOk', '.kRkRk', '..kkk.']
EYE_ALT = {'blink': ['kkkkkk', 'Ekkkkk', '.EEEEE', '..EEE.'], 'hit': ['.kk.kk', 'DDkkDD', '.kkDkk', '..DDD.'],
           'atk0|atk1|atk2': ['kkkkkk', 'kwwkOk', '.kOkRk', '..kkk.'], 'ko': ['.k.k..', '..k...', '.k.k..', '......']}

# ---- こぶし（見せ所）：下向き（地面に つく）。手の 甲は 上、指 4本が ならび、指先の 関節に 鉄の キャップ ----
def fist():
    """はがねの こぶし（右＝前 向き）：丸い かたまりに、前の はしだけ 指の みぞ 3本＋ つき出た 関節、手前に 親指"""
    W, H = 16, 13; g = grid(W, H)
    rows = [(3, 12), (1, 13), (0, 14), (0, 15), (0, 15), (0, 14), (0, 15), (0, 15), (0, 14), (0, 15), (0, 15), (1, 14), (3, 12)]
    for y, (a, b) in enumerate(rows):
        for x in range(a, b + 1): g[y][x] = '#'
    g = shade(g, 'S', 'T', 'U', lt=1, dkn=2, rk=1)
    for y in (2, 5, 8, 11):          # 関節の ハイライト（指ごとの 丸み）
        for x in range(10, 14):
            if g[y][x] == 'T': g[y][x] = 'S'
    for y in (4, 7, 10):             # 指の みぞ（前の はしだけ）
        for x in range(10, 16):
            if g[y][x] != '.': g[y][x] = 'k'
        g[y][9] = 'U'
    # 手の 甲の びょう
    g[3][3] = 'k'; g[3][7] = 'k'
    # 親指：手の 甲から 前へ、人差し指〜中指の 上に かぶさる
    for x in range(2, 11): g[6][x] = 'k'
    for x in range(1, 11): g[7][x] = 'S' if x < 10 else 'w'
    for x in range(1, 11): g[8][x] = 'T' if x < 10 else 'S'
    g[7][11] = 'k'; g[8][11] = 'k'
    for x in range(2, 11): g[9][x] = 'k'
    return outline(rows_of(g))
def transpose(rows):
    w = max(len(r) for r in rows); rows = [r.ljust(w, '.') for r in rows]
    return [''.join(rows[y][x] for y in range(len(rows))) for x in range(w)]
FIST = fist()
# 鉄の こて（前腕を 包む 筒）：ひじ側の ふちが ひろがり、びょう打ちと みぞ
GAUNT = [
    'kkkkkkkkkkkkk',
    'kSSSSSSSSSSUk',
    'kSTTkTTTkTTUk',
    'kSUUUUUUUUUUk',
    '.kSTTTTTTTUk.',
    '.kSTTTTTTTUk.',
    '.kSTkTTTkTUk.',
    '.kSTTTTTTTUk.',
    '.kSUUUUUUUUk.',
    '.kkkkkkkkkkk.',
]
UPPER = [
    '.kBBBBBBBk.',
    'kABBBBBBBCk',
    'kABBBBBBBCk',
    'kAABBBBBBCk',
    'kAABBCBBBCk',
    '.kABBBBBCCk',
    '.kABBBBBCk.',
    '.kABBBBBCk.',
]
# 腕：肩（上の 3行は 胴に 食いこむ）→ 上腕（毛）→ 鉄の こて → こぶし（こての 下に 2ドット 重ねる）
ARM = place([(UPPER, 1, 0), (GAUNT, 0, 7), (FIST, 0, 14)], W=18, H=29)
# 打ち出し：腕を 前へ 水平に、こぶしは 鎖ごと とぶ（横向きは 同じ 絵を 斜めに 写した もの：光は 左上の まま）
UPPER_H, GAUNT_H, FIST_H = transpose(UPPER), transpose(GAUNT), transpose(FIST)
def shot(n):
    parts = [(UPPER_H, 0, 1), (GAUNT_H, 7, 0)]
    for i in range(n): parts.append((outline(['SS', 'TU']) if i % 2 == 0 else outline(['ST']), 16 + i * 3, 4 + (i % 2)))
    parts.append((FIST, 16 + n * 3, 0))
    return place(parts, W=50, H=16)
ARM_SHOT, ARM_BACK = shot(3), shot(0)
# ため：こぶしを 肩の 上へ ふりかぶる（こぶし→こて→上腕 が 肩へ 下りる）
ARM_UP = place([(FIST[::-1], 0, 0), (GAUNT[::-1], 0, 13), (UPPER[::-1], 1, 21)], W=18, H=30)

# ---- 足：短く 太く ひざを 曲げる（上の 3行は おしりに 食いこむ）。足の 指は はだ色 ----
LEG = [
    '.kCCCCCCCk...',
    'kABBBBBBBCk..',
    'kABBBBBBBBCk.',
    'kAABBBBBBBCk.',
    '.kAABBBBBBCCk',
    '..kABBBBBBBCk',
    '..kABBBBBBCk.',
    '.kABBBBBBCk..',
    '.kABBBBBCk...',
    'kkDDDDDDDEk..',
    'kDDEEEEEEEEk.',
    'kDElEElEElEk.',
    'kkkkkkkkkkkk.',
]
BANG = [
    "...k....k...",
    "..kOk..kOk..",
    "k.kwOkkOwk.k",
    "kOkwwwwwwkOk",
    ".kwwwwwwwwk.",
    "kOOwwwwwwOOk",
    ".kkOwwwwOkk.",
    "..kOkkkkOk..",
    "...k....k...",
]
NB = 'atk0|atk1|atk2'
def layers():
    return [
        dict(n='armB', g='armB', x=44, y=31, rows=dk(ARM)),
        dict(n='legB', g='legB', x=22, y=46, rows=dk(LEG)),
        dict(n='body', g='body', x=12, y=28, rows=BODY),
        dict(n='chain', g='body', x=13, y=29, rows=CHAIN),
        dict(n='legA', g='legA', x=13, y=48, rows=LEG),
        dict(n='armUp', g='armF', x=24, y=10, rows=ARM_UP, only='atk0'),
        dict(n='head', g='head', x=32, y=15, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_ROAR)}),
        dict(n='eye', g='head', x=38, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=37, y=32, rows=ARM, not_=NB),
        dict(n='armShot', g='armF', x=37, y=34, rows=ARM_SHOT, alt={'atk2': ARM_BACK}, only='atk1|atk2'),
        dict(n='bang', g='fx', x=72, y=33, rows=BANG, only='atk1'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (0, -1), 'armB': (0, -1)}, 'idle2': {'body': (0, 1), 'armF': (0, -1), 'armB': (0, -1)}, 'idle3': {},
    'blink': {},
    'walk0': {'legA': (1, -1), 'armB': (-1, 0), 'armF': (1, -1)}, 'walk1': {'body': (0, -1), 'armF': (0, 0)},
    'walk2': {'legB': (1, -1), 'armF': (-1, 0), 'armB': (1, -1)}, 'walk3': {'body': (0, -1), 'armB': (0, 0)},
    'atk0': {'body': (-2, 1), 'head': (-1, -1), 'armB': (-1, 1)},
    'atk1': {'root': (2, 0), 'head': (1, 0)},
    'atk2': {'root': (3, 0), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'armF': (-2, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
