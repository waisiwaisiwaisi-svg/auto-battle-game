# コオリミミズク（こおり・ひこう(風) × ミミズク）手打ち GBA風
# 直立して にらむ 夜の 狩人。大きな 頭・氷の 結晶の 羽角・つららの 刃の 翼
import pix
META = dict(id='koorimimizuku', name='コオリミミズク', types=['ice', 'wind'], base='ミミズク', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2a4c',
    'W': '#f4f8ff', 'I': '#b4e2f8', 'J': '#6aa8d8', 'K': '#3a64a0',
    'n': '#7c8cc0', 'N': '#4c5a8c', 'M': '#2c3560',
    'E': '#8ffff0', 'G': '#d8c48e', 'g': '#7a6a52',
}
LIGHT = set('WInEG')
KEEP_BLACK = set('Ew')   # 目の まわりの 黒は 濃い まま

S = 64
def canvas(): return pix.grid(S, S)
def shade(g, chars, L, M, D, deep=1):
    """面の 陰影（あたり）：上と 左の ふち＝明、右と 下の ふち＝暗。仕上げは 手で 上書き"""
    H, W = len(g), len(g[0])
    def run(x, y, dx, dy):
        n = 0
        while 0 <= x < W and 0 <= y < H and g[y][x] in chars: x += dx; y += dy; n += 1
        return n
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] not in chars: continue
            u, lf, rt, dn = run(x, y, 0, -1), run(x, y, -1, 0), run(x, y, 1, 0), run(x, y, 0, 1)
            c = M
            if rt <= deep + 1 or dn <= deep + 1: c = D
            elif u <= deep or lf <= deep: c = L
            out[y][x] = c
    return out
def ol(g):
    """1ドットの 黒い 輪郭（同じ 大きさの まま）"""
    o = pix.grid_of(pix.outline(pix.rows_of(g)))
    return [r[1:-1] for r in o[1:-1]]
def put(g, pts):
    for (x, y, c) in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = c
def merge(*gs):
    out = canvas()
    for g in gs:
        for y in range(S):
            for x in range(S):
                if g[y][x] != '.': out[y][x] = g[y][x]
    return out

# ---------- 体（たまご形・直立）----------
def body():
    g = canvas()
    pix.ellipse(g, 34, 42, 10.5, 13.5, 'N')
    g = shade(g, 'N', 'n', 'N', 'M', 2)
    # 胸：白い 羽毛に 水色の 横じま（右前）
    c = canvas(); pix.ellipse(c, 38.5, 44, 6.5, 11, 'W')
    for y in range(S):
        for x in range(S):
            if c[y][x] == 'W' and g[y][x] != '.':
                g[y][x] = 'I' if (x >= 42 or y >= 51) else 'W'
    for y in range(36, 55, 3):   # 横じま（V字の 羽の もよう）
        for x in range(34, 45, 4):
            for (dx, dy) in ((0, 0), (1, 1), (2, 0)):
                if g[y + dy][x + dx] in 'WI': g[y + dy][x + dx] = 'J'
    return ol(g)

# ---------- 頭（大きく、まゆの ひさしが 重い）----------
BROW = [  # くちばしの 根もとへ 下がる V字の まゆ（紺の 羽の ひさし）
    'MM.................',
    'NMMM...............',
    '.NMMMMM........MMMM',
    '..lMMMMMMM...MMMMMl',
    '....llMMMMM.MMMMll.',
    '......lllMMMMMll...',
]
BEAK = [
    '.kGGk.',
    'kGGGgk',
    'kGGGgk',
    'kGGggk',
    '.kGggk',
    '.kGgk.',
    '..kgk.',
    '...k..',
]
CRYSTAL_B = [  # うしろの 羽角：氷の 結晶（2本の 刃）
    'k.........',
    'Wk........',
    'WIk.......',
    'kWIk...k..',
    '.kWIk.kWk.',
    '.kWIJkWIk.',
    '..kWIJIJk.',
    '..kIJJJKk.',
    '...kJJKk..',
    '...kJKk...',
]
CRYSTAL_F = [
    '.......k.',
    '......kW.',
    '.....kWI.',
    '..k.kWIJk',
    '.kWkWIJKk',
    '.kWIIJKk.',
    'kWIJJKKk.',
    'kIJJKKk..',
    '.kJKKk...',
    '..kKk....',
]
def head():
    g = canvas()
    pix.ellipse(g, 38.5, 20.5, 11, 9.5, 'N')
    g = shade(g, 'N', 'n', 'N', 'M', 2)
    # 顔の 皿：目の 下〜くちばしの まわりは 白い 霜の 羽
    f = canvas(); pix.ellipse(f, 41.5, 23.5, 7.5, 6.5, 'I')
    for y in range(S):
        for x in range(S):
            if f[y][x] == 'I' and g[y][x] != '.': g[y][x] = 'W' if (x < 41 and y < 25) else 'I' if y < 28 else 'J'
    pix.stamp(g, BROW, 30, 14)
    # 目：つり上がった 水色の 光、たての ひとみ
    put(g, [(34, 19, 'E'), (35, 19, 'E'), (36, 19, 'E'), (37, 19, 'W'), (38, 20, 'k'),
            (33, 20, 'k'), (34, 20, 'E'), (35, 20, 'k'), (36, 20, 'E'), (37, 20, 'E'), (38, 21, 'k'),
            (34, 21, 'k'), (35, 21, 'k'), (36, 21, 'k'), (37, 21, 'k'),
            (45, 19, 'E'), (46, 19, 'E'), (47, 19, 'k'), (45, 20, 'k'), (46, 20, 'k')])
    pix.stamp(g, BEAK, 39, 21)
    g = ol(g)
    pix.stamp(g, CRYSTAL_B, 26, 3)
    pix.stamp(g, CRYSTAL_F, 42, 3)
    return g

# ---------- 翼：つららの 刃の 羽（羽の 根もと＝紺、先へ いくほど 氷）----------
def blade(g, base0, base1, tip, cut=.45):
    """1枚の 羽（多角形）。先の 部分を 氷の 色に。黒で ふちどって から 上に 重ねる"""
    t = canvas(); pix.poly(t, [base0, base1, tip], 'N')
    t = shade(t, 'N', 'n', 'N', 'M', 0)
    ys = [y for y in range(S) if 'n' in t[y] or 'N' in t[y] or 'M' in t[y]]
    if not ys: return
    y0, y1 = ys[0], ys[-1]; xs = [x for y in ys for x in range(S) if t[y][x] != '.']
    x0, x1 = min(xs), max(xs)
    for y in range(S):
        for x in range(S):
            c = t[y][x]
            if c == '.': continue
            # 先の 方（tip に 近い 側）は 氷
            d0 = ((x - tip[0]) ** 2 + (y - tip[1]) ** 2) ** .5
            L = ((base0[0] - tip[0]) ** 2 + (base0[1] - tip[1]) ** 2) ** .5
            if d0 < L * (1 - cut): t[y][x] = {'n': 'W', 'N': 'I', 'M': 'J'}[c]
    t = ol(t)
    for y in range(S):
        for x in range(S):
            if t[y][x] != '.': g[y][x] = t[y][x]
def wing_raised(dy=0, spread=0):
    """半分 上げた 翼（うしろ）。前ふち：肩 → 手首（左上）。手首と 腕から つららの 刃が たれる"""
    g = canvas()
    wx, wy = 9 - spread, 9 + dy - spread       # 手首
    # 刃（奥 → 手前）
    for i in range(6):
        bx, by = wx + 3 + i * 3, wy + 2 + i * 3 - (0 if i < 3 else (i - 2))
        blade(g, (bx - 1, by), (bx + 4, by + 1), (bx - 5 + i, by + 20 - i * 1), .55)
    c = canvas(); pix.poly(c, [(31, 31), (wx + 3, wy - 1), (wx - 1, wy + 2), (wx + 5, wy + 7), (22, 22), (30, 37)], 'N')
    c = shade(c, 'N', 'n', 'N', 'M', 1)
    # 雨覆いの 氷の うろこ（手で）
    for (x, y) in ((16, 13), (19, 15), (22, 18), (25, 21), (15, 16), (18, 19), (21, 22)):
        if c[y][x] in 'nNM': c[y][x] = 'I'
    c = ol(c)
    for y in range(S):
        for x in range(S):
            if c[y][x] != '.': g[y][x] = c[y][x]
    return g
def wing_folded(lift=0):
    """たたんだ 翼（手前）：体の 横に そい、下の ふちから つららの 刃が うしろへ"""
    g = canvas()
    for i in range(4):
        bx, by = 22 + i * 2, 38 + i * 3 - lift
        blade(g, (bx, by), (bx + 5, by + 2), (12 + i * 3, 52 + i * 2 - lift), .5)
    c = canvas(); pix.poly(c, [(31, 28 - lift), (24, 32 - lift), (21, 42 - lift), (25, 49 - lift), (33, 44 - lift), (35, 34 - lift)], 'N')
    c = shade(c, 'N', 'n', 'N', 'M', 1)
    for (x, y) in ((27, 35), (30, 37), (25, 40), (28, 42)):
        if c[y - lift][x] in 'nNM': c[y - lift][x] = 'I'
    c = ol(c)
    for y in range(S):
        for x in range(S):
            if c[y][x] != '.': g[y][x] = c[y][x]
    return g
def wing_strike():
    """攻撃の 決め：手前の 翼を 前へ 打ちだす（刃が 右を 向く）"""
    g = canvas()
    for i in range(4):
        bx, by = 32 + i * 2, 30 + i * 3
        blade(g, (bx, by), (bx + 2, by + 5), (54 + i * 2, 32 + i * 4), .5)
    c = canvas(); pix.poly(c, [(28, 29), (36, 27), (42, 33), (38, 42), (30, 42), (26, 36)], 'N')
    c = shade(c, 'N', 'n', 'N', 'M', 1)
    c = ol(c)
    for y in range(S):
        for x in range(S):
            if c[y][x] != '.': g[y][x] = c[y][x]
    return g

def tail():
    g = canvas()
    blade(g, (26, 49), (30, 52), (13, 59), .5)
    blade(g, (27, 51), (31, 54), (17, 61), .5)
    return g
TALON = [
    '.kNNk.kNNk.',
    '.kMMk.kMMk.',
    'kGgGkkGgGk.',
    'kgkgkkgkgk.',
    'k.k.kk.k.k.',
]
def dark(g): return [[{'W': 'I', 'I': 'J', 'J': 'K', 'n': 'N', 'N': 'M', 'M': 'l'}.get(c, c) for c in r] for r in g]
def rows(g): return pix.rows_of(g)

SHARD = ['kk..........', 'kWWkkk......', '.kWIIIJkkk..', '..kkIJJJKKk.', '....kkkJKk..', '.......kk...']
def volley(pts):
    g = pix.grid(34, 22)
    for (x, y) in pts: pix.stamp(g, SHARD, x, y)
    return pix.rows_of(g)
VOLLEY1 = volley([(0, 1), (9, 8), (1, 15)])
VOLLEY2 = volley([(10, 0), (20, 8), (12, 15)])
FROST = ['..k.....k..', '.kWk...kIk.', 'kWEWk.kIWIk', '.kWk...kIk.', '..k.....k..']

EYE = ['EEEW', 'kEkE']                   # 手前の 目（頭の 中の 目を 上書き）
EYE_ALT = {'blink': ['MMMM', 'kkkk'], 'atk0|atk1|atk2': ['WWWW', 'kWkW'], 'hit': ['kkEk', 'EkkE'], 'ko': ['EkkE', 'kEEk']}
EYEF = ['EE']
EYEF_ALT = {'blink': ['MM'], 'atk0|atk1|atk2': ['WW'], 'hit': ['kE'], 'ko': ['kk']}

# ---------- ダウン：あおむけ ではなく 横だおし。翼は 地面に 広がり、目は × ----------
def ko_pose():
    g = canvas()
    # 地面に 広がった 翼（刃が 左へ ねる）
    for i in range(5):
        bx, by = 26 - i * 2, 47 + i
        blade(g, (bx, by), (bx + 3, by + 4), (4 + i * 3, 56 + i), .55)
    b = canvas(); pix.ellipse(b, 33, 52, 13, 7.5, 'N')
    b = shade(b, 'N', 'n', 'N', 'M', 1)
    c = canvas(); pix.ellipse(c, 36, 56, 9, 4, 'W')   # 白い 胸が 下に 見える
    for y in range(S):
        for x in range(S):
            if c[y][x] == 'W' and b[y][x] != '.': b[y][x] = 'I' if y >= 57 else 'W'
    b = ol(b)
    g = merge(g, b)
    # 頭：地面に 横たわる（羽角は ななめに たおれる）
    h = canvas()
    pix.ellipse(h, 49, 51, 9.5, 8.5, 'N')
    h = shade(h, 'N', 'n', 'N', 'M', 2)
    f = canvas(); pix.ellipse(f, 51.5, 54, 6.5, 5.5, 'I')
    for y in range(S):
        for x in range(S):
            if f[y][x] == 'I' and h[y][x] != '.': h[y][x] = 'W' if y < 55 else 'I'
    pix.stamp(h, ['MMM......', 'NMMMM..MM', '.lMMMMMMl', '...llMll.'], 42, 46)
    put(h, [(45, 50, 'E'), (47, 50, 'E'), (46, 51, 'E'), (45, 52, 'E'), (47, 52, 'E'),
            (46, 50, 'k'), (45, 51, 'k'), (47, 51, 'k'), (46, 52, 'k'), (48, 51, 'k'), (44, 51, 'k'),
            (53, 51, 'k'), (54, 51, 'E'), (53, 52, 'E'), (54, 52, 'k')])
    pix.stamp(h, BEAK, 50, 53)
    h = ol(h)
    pix.stamp(h, pix.rot90(CRYSTAL_B)[::-1], 37, 37)
    g = merge(g, h)
    # 爪：力なく 上を 向く
    pix.stamp(g, pix.flip_v(TALON), 24, 40)
    return g

UP_WING = {0: wing_raised(), 1: wing_raised(1), 2: wing_raised(2)}
def layers():
    WR, WR1, WR2 = UP_WING[0], UP_WING[1], UP_WING[2]
    WH = wing_raised(-3, 2)
    return [
        dict(n='wingB', g='wingB', x=0, y=0, rows=rows(WR), alt={'idle1|idle3|walk1|walk3': rows(WR1), 'idle2|walk2|atk2': rows(WR2), 'atk0|atk1': rows(WH), 'hit': rows(WR2)}, not_='ko'),
        dict(n='tail', g='body', x=0, y=0, rows=rows(tail()), not_='ko'),
        dict(n='talonB', g='talon', x=29, y=55, rows=pix.rows_of(dark(pix.grid_of(TALON))), not_='ko'),
        dict(n='body', g='body', x=0, y=0, rows=rows(body()), not_='ko'),
        dict(n='talon', g='talon', x=33, y=55, rows=TALON, not_='ko'),
        dict(n='wingF', g='wingF', x=0, y=0, rows=rows(wing_folded()), alt={'atk0': rows(wing_folded(3)), 'atk1|atk2': rows(wing_strike())}, not_='ko'),
        dict(n='head', g='head', x=0, y=0, rows=rows(head()), not_='ko'),
        dict(n='eye', g='head', x=34, y=19, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='eyeF', g='head', x=45, y=19, rows=EYEF, alt=EYEF_ALT, not_='ko'),
        dict(n='frost', g='head', x=24, y=0, rows=FROST, only='atk0'),
        dict(n='volley1', g='fx', x=50, y=24, rows=VOLLEY1, only='atk1'),
        dict(n='volley2', g='fx', x=46, y=24, rows=VOLLEY2, only='atk2'),
        dict(n='ko', g='root', x=0, y=0, rows=rows(ko_pose()), only='ko'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'talon': (0, -1)},
    'idle2': {'body': (0, 1), 'head': (0, 0), 'talon': (0, -1)},
    'idle3': {'body': (0, 1), 'talon': (0, -1)},
    'blink': {},
    'walk0': {'root': (0, -1), 'talon': (1, 0)},
    'walk1': {'root': (0, -2), 'talon': (0, 1)},
    'walk2': {'root': (0, -1), 'talon': (-1, 0)},
    'walk3': {},
    'atk0': {'root': (-2, 1), 'head': (-1, 1)},
    'atk1': {'root': (3, -1), 'head': (1, 0)},
    'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-4, 0), 'head': (-2, -1), 'talon': (2, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'talon': 'root', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
