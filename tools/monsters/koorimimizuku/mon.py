# コオリミミズク（こおり・ひこう(風) × ミミズク）手打ち GBA風
# 直立して にらむ 夜の 狩人。大きな 頭・氷の 結晶の 羽角・つららの 刃の 翼
import pix
META = dict(id='koorimimizuku', name='コオリミミズク', types=['ice', 'wind'], base='ミミズク', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2a4c',
    'W': '#f4f8ff', 'I': '#b4e2f8', 'J': '#6aa8d8', 'K': '#3a64a0',
    'n': '#7c8cc0', 'N': '#4c5a8c', 'M': '#2c3560',
    'E': '#8ffff0', 'e': '#26a6b4', 'G': '#d8c48e', 'g': '#7a6a52',
}
LIGHT = set('WInEG')
KEEP_BLACK = set('Eew')   # 目の まわりの 黒は 濃い まま

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
    pix.ellipse(g, 34, 42.5, 10.5, 11.5, 'N')
    g = shade(g, 'N', 'n', 'N', 'M', 2)
    # 胸：白い 羽毛に 水色の 横じま（右前）
    c = canvas(); pix.ellipse(c, 38.5, 44, 6.5, 9.5, 'W')
    for y in range(S):
        for x in range(S):
            if c[y][x] == 'W' and g[y][x] != '.':
                g[y][x] = 'I' if (x >= 42 or y >= 51) else 'W'
    for j, y in enumerate(range(37, 55, 4)):   # 波うつ 横じま（とちゅうで 切れる）
        for x in range(30, 48):
            if (x + j * 2) % 6 in (0, 5): continue
            yy = y + (1 if (x + j * 2) % 6 in (2, 3) else 0)
            if g[yy][x] in 'WI': g[yy][x] = 'J' if g[yy][x] == 'W' else 'K'
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
CRYSTAL_B = [  # うしろの 羽角：氷の 結晶（3本の 刃が うしろへ 反る）
    'kk...........',
    'kWk..........',
    '.kWk.........',
    '.kWIk...k....',
    '..kWIk.kWk...',
    'k.kWIJkWIk...',
    'Wk.kWIJIJk...',
    'kWkkWIJJKk...',
    '.kWIIJJKKk...',
    '..kIJJJKKk...',
    '...kkJJKk....',
    '.....kKk.....',
]
CRYSTAL_F = [
    '.........kk',
    '........kWk',
    '.......kWIk',
    '...k..kWIJk',
    '..kWk.kWJKk',
    '..kWIkWIJKk',
    '.kWIIJIJKk.',
    '.kWIJJJKKk.',
    'kWIJJKKKk..',
    'kIJJKKKk...',
    '.kkJKKk....',
    '...kkk.....',
]
# 顔（手打ち）：重い まゆの ひさし、つり上がった 光る 目、白い 霜の 顔、かぎくちばし。'.'は 頭の 地のまま
FACE = [
    'MM.................',
    'MMMM............MM.',
    'lMMMMMM.......MMMM.',
    '.llMMMMMM...MMMMMl.',
    '.WWllMMMMM.MMMllWW.',
    'WWWWWllMMMMMlWWWWW.',
    'WWWWWWWlkMMklWWWWW.',
    'WWWWWWWWkllkWWWWIW.',
    'WIWWWWWWkGGkWWWIIW.',
    'WIIWWWWkGGGGkWWIII.',
    '.IIWWWWkGGGGgkWII..',
    '.JIIIIIkGGGggkIIJ..',
    '..JIIIIkGGGgkIIJ...',
    '...JJIIIkGgkIIJ....',
    '....JJJIkgkIJJ.....',
    '......JJJkJJ.......',
]
def head():
    g = canvas()
    pix.ellipse(g, 38.5, 20.5, 12.5, 10.5, 'N')
    g = shade(g, 'N', 'n', 'N', 'M', 2)
    pix.stamp(g, FACE, 29, 14)
    g = ol(g)
    pix.stamp(g, CRYSTAL_B, 22, 2)
    pix.stamp(g, CRYSTAL_F, 42, 2)
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
    for i in range(5):
        bx, by = wx + 2 + i * 4, wy + 2 + i * 4
        blade(g, (bx - 1, by), (bx + 4, by + 1), (bx - 7 + i, by + 24 - i * 2), .4)
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
    for i in range(3):
        bx, by = 22 + i * 3, 40 + i * 3 - lift
        blade(g, (bx, by), (bx + 5, by + 3), (13 + i * 5, 56 + i - lift), .55)
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
    blade(g, (27, 50), (31, 53), (20, 60), .5)
    return g
TALON = [  # 羽毛の 足（短いが 見える）と 金の かぎ爪
    '.knNk..knNk..',
    '.knNk..knNk..',
    '.knMk..knMk..',
    '.kNMk..kNMk..',
    'kGGGGk.kGGGGk',
    'kGkGkGkkGkGkG',
    'kgkgkgkkgkgkg',
    '.k.k.k..k.k.k',
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

# 目（手打ち）：外側が 高く、くちばし側へ 下がる つり目。黒い ふちで 光を きわだたせる
# 目：ハイライト W ＋ 虹彩 2色（E 明・e 暗）＋ たての ひとみ k
EYE = ['kkkk.....', 'kWWEkkk..', 'kWEEkEEkk', 'keEEkEEek', '.keekeek.', '..kkkkk..']
EYE_ALT = {'blink': ['kkkk.....', 'kMMMkkk..', 'kMMMMMMkk', 'kkkkkkkkk', '.WWWWWW..', '.........'],
           'atk0|atk1|atk2': ['kkkk.....', 'kWWWkkk..', 'kWWEkWEkk', 'kEWEkWEEk', '.keekeek.', '..kkkkk..'],
           'hit': ['kkkk.....', 'kMMMkkk..', 'kkkkkkkkk', 'kEkkkkEkk', '.kkEEkk..', '..kkkkk..']}
EYEF = ['...kk', '.kWEk', 'kEkEk', 'kekek', '.kkk.']
EYEF_ALT = {'blink': ['...kk', '.kkMk', 'kMMMk', 'kkkkk', '.....'], 'atk0|atk1|atk2': ['...kk', '.kWWk', 'kWkEk', 'kekek', '.kkk.'], 'hit': ['...kk', '.kkMk', 'kkkkk', 'kEkEk', '.kkk.']}

# ---------- ダウン：あおむけに たおれる。頭は 横に ころがり（羽角が 右、顔が 上）、目は ×、爪は 上を 向く ----------
EYE_KO = ['kEkkkEk', 'kkEkEkk', 'kkkEkkk', 'kkEkEkk', 'kEkkkEk']
EYEF_KO = ['EkE', 'kEk', 'EkE']
def crop(g):
    ys = [y for y in range(len(g)) if any(c != '.' for c in g[y])]; xs = [x for x in range(len(g[0])) if any(g[y][x] != '.' for y in ys)]
    return [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
def anti_t(g):
    """右上〜左下の 対角線で 折り返す（上 → 右、右 → 上）。90度 回転＋左右反転に あたる"""
    H, W = len(g), len(g[0])
    return [[g[H - 1 - x][W - 1 - y] for x in range(H)] for y in range(W)]
def ko_head():
    g = canvas()
    pix.ellipse(g, 38.5, 20.5, 12.5, 10.5, 'N')
    pix.stamp(g, FACE, 29, 14)
    pix.stamp(g, EYE_KO, 29, 17); pix.stamp(g, EYEF_KO, 42, 18)
    pix.stamp(g, recolor_dim(CRYSTAL_B), 22, 2); pix.stamp(g, recolor_dim(CRYSTAL_F), 42, 2)
    g = anti_t(crop(g))
    g = shade(g, 'N', 'n', 'N', 'M', 2)   # 光は 回したあとで つけ直す（左上から）
    return pix.grid_of(pix.outline(pix.rows_of(g)))
def recolor_dim(rows): return pix.recolor(rows, {'W': 'I', 'I': 'J', 'J': 'K'})   # 結晶の 光が 消える
def ko_pose():
    g = canvas()
    # 地面に 広がった 翼（刃が 左へ ねる）
    for i in range(5):
        bx, by = 26 - i * 2, 49 + i
        blade(g, (bx, by), (bx + 3, by + 4), (3 + i * 3, 58 + i // 2), .45)
    b = canvas(); pix.ellipse(b, 28, 52.5, 13, 7, 'N')
    b = shade(b, 'N', 'n', 'N', 'M', 1)
    c = canvas(); pix.ellipse(c, 30, 49, 9, 4, 'W')   # 白い 胸が 上を 向く
    for y in range(S):
        for x in range(S):
            if c[y][x] == 'W' and b[y][x] != '.': b[y][x] = 'W' if x < 33 else 'I'
    for x in range(22, 38, 3):
        if b[50][x] == 'W': b[50][x] = 'J'
        if b[50][x + 1] == 'W': b[51][x + 1] = 'J'
    b = ol(b)
    g = merge(g, b)
    pix.stamp(g, pix.flip_v(TALON), 18, 40)   # 爪は 上を 向いて 丸まる
    h = ko_head(); hh, hw = len(h), len(h[0])
    pix.stamp(g, pix.rows_of(h), 64 - hw - 1, 61 - hh)
    return g

UP_WING = {0: wing_raised(), 1: wing_raised(1), 2: wing_raised(2)}
def layers():
    WR, WR1, WR2 = UP_WING[0], UP_WING[1], UP_WING[2]
    WH = wing_raised(-3, 2)
    return [
        dict(n='wingB', g='wingB', x=0, y=2, rows=rows(WR), alt={'idle1|idle3|walk1|walk3': rows(WR1), 'idle2|walk2|atk2': rows(WR2), 'atk0|atk1': rows(WH), 'hit': rows(WR2)}, not_='ko'),
        dict(n='tail', g='body', x=0, y=0, rows=rows(tail()), not_='ko'),
        dict(n='talonB', g='talon', x=27, y=52, rows=pix.rows_of(dark(pix.grid_of(TALON))), not_='ko'),
        dict(n='body', g='body', x=0, y=0, rows=rows(body()), not_='ko'),
        dict(n='talon', g='talon', x=32, y=52, rows=TALON, not_='ko'),
        dict(n='wingF', g='wingF', x=0, y=0, rows=rows(wing_folded()), alt={'atk0': rows(wing_folded(3)), 'atk1|atk2': rows(wing_strike())}, not_='ko'),
        dict(n='head', g='head', x=0, y=4, rows=rows(head()), not_='ko'),
        dict(n='eye', g='head', x=28, y=21, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='eyeF', g='head', x=41, y=21, rows=EYEF, alt=EYEF_ALT, not_='ko'),
        dict(n='frost', g='head', x=22, y=2, rows=FROST, only='atk0'),
        dict(n='volley1', g='fx', x=50, y=24, rows=VOLLEY1, only='atk1'),
        dict(n='volley2', g='fx', x=46, y=24, rows=VOLLEY2, only='atk2'),
        dict(n='ko', g='root', x=-4, y=0, rows=rows(ko_pose()), only='ko'),
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
