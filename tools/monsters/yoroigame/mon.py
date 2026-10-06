# ヨロイガメ（いわ・みず × リクガメ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='yoroigame', name='ヨロイガメ', types=['rock', 'water'], base='リクガメ', size='L')
PAL = {
    'k': '#101018', 'l': '#22223c',
    'S': '#d8d2c6', 'T': '#9a929a', 'U': '#5c5664',      # 城壁の 石（明・中・暗）
    'A': '#94d6a2', 'B': '#409a78', 'C': '#22584e',      # 皮（明・中・暗）
    'W': '#e4f8ff', 'X': '#5cb6f2', 'Z': '#2a5cb6',      # 水（明・中・暗）
    'Y': '#ffd23a', 'O': '#d8781c', 'M': '#9cc24a', 'w': '#ffffff',
}
LIGHT = set('SAWYMw')
KEEP_BLACK = set('wYXW')

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
            if dn <= dk or rt <= 3: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if up <= 1 and rt <= 2: c = Mc
            out[y][x] = c
    return out

# ---- 城壁の 甲羅：ドーム → 石の 甲板（背甲・肋甲・縁甲）を 角度で 分ける → 板ごとに 面取りの 光と 影
#      上に 胸壁の 凸凹と 小さな 見張り塔、前に 砲門、矢狭間から 水の 光（手で 置く）----
import math
# デフォルメ：甲羅を 小さく（42x36 → 36x30）。見せ所の 城壁の 形は そのまま
SW, SH, SCX, SCY = 36, 30, 17.5, 30.0
def shell(glow=False):
    W, H = SW, SH; idg = [[None] * W for _ in range(H)]
    for y in range(5, H):
        for x in range(W):
            dx, dy = (x + .5 - SCX) / 18, (SCY - (y + .5)) / 25
            if dx * dx + dy * dy > 1: continue
            if y >= 21 and ((x + .5 - SCX) / 18) ** 2 + ((y + .5 - 20.5) / 9.5) ** 2 > 1: continue
            if y >= 25: idg[y][x] = ('m', (x + (1 if y % 2 else 0)) // 5)       # 縁甲
            else:
                th = math.degrees(math.atan2(SCY - (y + .5), x + .5 - SCX))
                inner = ((x + .5 - SCX) / 11) ** 2 + ((SCY - (y + .5)) / 17.5) ** 2 > 1
                if inner: idg[y][x] = ('v', 0 if th > 128 else 1 if th > 90 else 2 if th > 52 else 3)
                else: idg[y][x] = ('c', 0 if th > 140 else 1 if th > 105 else 2 if th > 72 else 3 if th > 40 else 4)
    # 胸壁（凸）と 見張り塔：甲羅の 上の 弧に 乗せる
    def top(x): return next((y for y in range(H) if idg[y][x] is not None), H)
    for i, x0 in enumerate((3, 8, 24, 29)):
        t = min(top(x) for x in range(x0, x0 + 4))
        for y in range(t - 3, t + 1):
            for x in range(x0, x0 + 4): idg[y][x] = ('b', i)
    for y in range(0, 7):
        for x in range(13, 23):
            if y < 2 and x in (15, 16, 19, 20): continue
            idg[y][x] = ('t', 0)
    g = grid(W, H)
    for y in range(H):
        for x in range(W):
            p = idg[y][x]
            if p is None: continue
            def same(yy, xx): return 0 <= yy < H and 0 <= xx < W and idg[yy][xx] == p
            def solid(yy, xx): return 0 <= yy < H and 0 <= xx < W and idg[yy][xx] is not None
            # 板の さかい目（右と 下が ちがう 板なら 目地）
            if (solid(y, x + 1) and not same(y, x + 1)) or (solid(y + 1, x) and not same(y + 1, x)):
                g[y][x] = 'l'; continue
            nx, ny = (x + .5 - SCX) / 18, (y + .5 - 12) / 20
            lt = -nx * .7 - ny * .7
            c = 'S' if lt > .55 else 'U' if lt < -.45 else 'T'
            if not same(y - 1, x) or not same(y, x - 1): c = 'S' if lt > -.6 else 'T'      # 面取りの 光（上と 左）
            elif not same(y + 1, x) or not same(y, x + 1) or not same(y + 2, x): c = 'U'   # 下と 右は 影
            if p[0] == 'm': c = 'S' if (not same(y - 1, x) and lt > -.2) else 'T' if y < 28 and lt > -.3 else 'U'
            g[y][x] = c
    # 塔の 右の 影・入り口
    for y in range(0, 7): g[y][21] = 'U' if g[y][21] != '.' else '.'
    for (x, y) in ((17, 3), (18, 3), (17, 4), (18, 4), (17, 5), (18, 5)): g[y][x] = 'k'
    c1, c2 = ('W', 'X') if glow else ('X', 'Z')
    g[4][17] = c1; g[5][17] = c2; g[4][18] = c2
    # 矢狭間（たての すき間）
    for (x, y) in ((9, 14), (16, 11), (23, 13), (5, 20), (12, 19), (20, 20)):
        g[y][x] = 'k'; g[y + 1][x] = c1; g[y + 2][x] = c2
    # ひび
    for (x, y) in ((11, 16), (12, 17), (19, 15), (25, 18), (26, 19), (4, 24), (30, 23)):
        if g[y][x] in 'ST': g[y][x] = 'U'
    # 苔（光の 側の 目地に）
    for (x, y) in ((4, 17), (5, 17), (8, 10), (9, 10), (13, 7), (14, 7), (2, 24), (3, 24), (11, 25), (12, 25), (22, 8), (11, 9)):
        if 0 <= y < H and g[y][x] != '.': g[y][x] = 'M'
    # 前の 砲門（まるい 穴）
    for (dx, dy, ch) in ((1, 0, 'k'), (2, 0, 'k'), (0, 1, 'k'), (3, 1, 'k'), (0, 2, 'k'), (3, 2, 'k'), (1, 3, 'k'), (2, 3, 'k'),
                       (1, 1, c1), (2, 1, c2), (1, 2, c2), (2, 2, 'Z'), (0, 0, 'S'), (-1, 1, 'S'), (-1, 2, 'T'), (4, 1, 'U'), (4, 2, 'U'), (3, 3, 'U'), (3, 0, 'T')):
        g[15 + dy][28 + dx] = ch
    return outline(rows_of(g))

# ワニガメの 頭：重い まゆの ひさし・かぎ形の 石の くちばし
HEAD = [
    '.....kkkkkkkkkk.......',
    '...kkSSTkSSTTkSkk.....',
    '..kASTUkSTTUkBBBkk....',
    '.kAABBBBBBBBkkkkkBkk..',
    'kAABBBBBBBkkCCCCCkkBk.',
    'kABBBBBBBkC......kBSk.',
    'kABBBBBBBkC......kBSk.',
    'kABBBBBBBBkkkkkkkBSSTk',
    'kBBBBBBBBBBBBBBBkSSTTk',
    'kBBlBBBBlBBBBBBkSTTTUk',
    'kBBBlBBBBlBBBBkSTTTUUk',
    'kCBBBBBBBBBBkkkkkkkTUk',
    'kCBBlBBBBBBkTTTTTTkkUk',
    '.kCBBBlBBBBkkTTTTTUUk.',
    '..kCCBBBBBBBkkkkkkkk..',
    '...kkCCCCCCCCk........',
    '.....kkkkkkkk.........',
]
HEAD_OPEN = HEAD[:10] + [
    'kBBBlBBBBlBBBBkSTTTUUk',
    'kCBBBBBBBBBkkkkkkkkTUk',
    'kCBBlBBBBBkZZZZZZZkkUk',
    '.kCBBBlBBkZWZZZZZk.kk.',
    '..kCCBBBBkkTTTTTUk....',
    '...kkCCCCCkkkkkkk.....',
    '.....kkkkkk...........',
]
# 目：2段（ハイライト＋黄と だいだいの 虹彩＋たての ひとみ）。前は まゆで 切れて つり目
EYE = ['wYYkYk', 'OOOkOk']
EYE_ALT = {'blink': ['CCCCCC', 'kkkkkk'], 'hit': ['kkCCkk', 'CYkkYC'], 'atk0|atk1|atk2': ['wwYkYY', 'YOOkOk'], 'ko': ['kCkCkC', 'CkCkCk']}
# 太い 首（しわの 帯と 背の 小さな とげ）
NECK = [
    '......kk.kk...',
    '.....kSkkSk...',
    '...kkkUkkUkk..',
    '..kAABBBBBBBk.',
    '.kAABlBBBlBBCk',
    'kAABBlBBBlBBCk',
    'kABBBBlBBBlBCk',
    'kABBBBlBBBlBCk',
    'kBBBBBlBBBlCCk',
    'kBBBBlBBBlBCCk',
    'kCBBBlBBBlBCCk',
    '.kCCBBBBBBCCk.',
    '..kkkkkkkkkk..',
]
# 太い 足（デフォルメで 短く）：石の うろこ、白い かぎ爪
LEG = [
    '.kkkkkkkkkk.',
    'kAABBBBBBBCk',
    'kSTBBBCBBCCk',
    'kTUBBBBBBCCk',
    'kABBBBBCBCCk',
    'kABBBBBBBCCCk',
    'kCCCCCCCCCCCk',
    'kwkkwkkwkkwk.',
]
TAIL = ['....kkk', '..kkABk', 'kkABBCk', 'kBBCCk.', '.kkkk..']
# 腹（甲羅の 下に 見える 皮）
BELLY = [
    '.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.',
    'kBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBk',
    'kCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCk',
    '.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.',
]
# 甲羅の うしろの 滝（樋口から 流れ落ちる）
def fall(phase):
    rows = ['kkkkk', 'kSTUk', 'kXWXk']
    for y in range(14):
        r = ''
        for x in range(3):
            v = (y + phase + x * 2) % 4
            r += 'W' if v == 0 else 'X' if v < 3 else 'Z'
        rows.append('k' + r + 'k')
    rows += ['kWXWXk', 'WXWWXWk', 'kkkkkkk']
    return rows
FALL = [fall(0), fall(1), fall(2), fall(3)]
DARK = {'A': 'B', 'B': 'C', 'C': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 砲門からの 水の 大砲
def jet(n, splash=False):
    rows = ['.' + 'k' * n, 'k' + 'X' * n, 'W' * (n + 1), 'w' * (n + 1), 'W' * (n + 1), 'k' + 'X' * n, '.' + 'Z' * (n - 1) + 'k', '.' + 'k' * n]
    rows[1] = 'k' + ''.join('W' if i % 5 == 0 else 'X' for i in range(n))
    if splash:
        S = ['..k.kk..', '.kWkWXk.', 'kWXWWXk.', 'XWwWXWXk', 'WwwWXXk.', 'XWWXWXk.', 'kXZXWk..', '.kkZkk..']
        rows = [r + s for r, s in zip(rows, S)]
    return rows
SHELL = shell(); SHELL_G = shell(True)

def layers():
    return [
        dict(n='legFF', g='legB', x=36, y=51, rows=dark(LEG)),
        dict(n='legHF', g='legA', x=15, y=51, rows=dark(LEG)),
        dict(n='tail', g='body', x=2, y=50, rows=TAIL),
        dict(n='fall', g='body', x=6, y=36, rows=FALL[0], alt={'idle1|walk1': FALL[1], 'idle2|walk2|atk0': FALL[2], 'idle3|walk3|atk1': FALL[3]}, not_='ko'),
        dict(n='neck', g='neck', x=38, y=30, rows=NECK),
        dict(n='legH', g='legA', x=10, y=53, rows=LEG),
        dict(n='legF', g='legB', x=30, y=53, rows=LEG),
        dict(n='shell', g='body', x=8, y=23, rows=SHELL, alt={'idle1|idle2|atk0|atk1|atk2': SHELL_G}),
        dict(n='head', g='head', x=40, y=22, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=51, y=27, rows=EYE, alt=EYE_ALT),
        dict(n='jet1', g='fx', x=40, y=35, rows=jet(16), only='atk1'),
        dict(n='jet2', g='fx', x=40, y=35, rows=jet(18, True), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {'body': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (0, 2), 'neck': (-2, 1), 'head': (-1, 0)},
    'atk1': {'root': (-2, 0), 'body': (0, 1), 'neck': (0, -2), 'head': (0, -1)},
    'atk2': {'root': (-3, 0), 'body': (0, 1), 'neck': (0, -2), 'head': (0, -1)},
    'hit': {'root': (-3, 0), 'neck': (-1, -1), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'neck': 'body', 'head': 'neck', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'body'}
