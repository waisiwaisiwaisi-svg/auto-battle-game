# ドクエイ（どく・みず × エイ）手打ち GBA風・デフォルメ（2〜3頭身：ひし形の 平たい 体は そのまま、
# 前の 頭の ふくらみ・目・頭びれを 大きく、つばさは ひろく、毒針の 尾は 太く 大きく）
import math
from pix import grid, poly, outline, rows_of, ellipse
META = dict(id='dokuei', name='ドクエイ', types=['poison', 'water'], base='エイ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c1a2a',
    'A': '#6e9e8c', 'B': '#3e6a62', 'D': '#22403e',
    'E': '#c8d8c0',
    'P': '#ff7ae0', 'p': '#c03aa8', 'q': '#6a1a6a',
    'Y': '#ffe040', 'y': '#c08a10',
    'w': '#f4ecd8', 'n': '#b0a080',
    'c': '#a8f0ff',
}
LIGHT = set('AEPwYc')
KEEP_BLACK = set('wYyPp')
EYE_BOX = (41, 33, 12, 7)   # 両目（idle0 の 64x64 座標）

def _run(g, x, y, dx, dy, ch):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] == ch: n += 1; x += dx; y += dy
    return n
def P(g, pts, ch, only=None):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]) and (only is None or g[y][x] in only): g[y][x] = ch

# ---- 体：3/4 横から 見た ひし形の 平たい 体。奥の つばさ（上）・手前の つばさ（下、裏の 白い ふち）・
#      前に 盛り上がった 頭（目は 上）・頭の 前に 2本の 頭びれ（角の ように 前へ）。境めは 影の 線で、輪郭で 切らない ----
def body(flap=0):
    g = grid(70, 64)
    poly(g, [(9, 44), (20, 35), (32, 27 - flap), (37, 27 - flap), (44, 33), (49, 40), (9, 45)], '1')        # 奥の つばさ
    poly(g, [(9, 44), (49, 40), (48, 46), (40, 52), (30, 58 + flap), (25, 58 + flap), (17, 51)], '2')       # 手前の つばさ
    ellipse(g, 47, 39.5, 9.5, 7.5, '3')                                                                    # 頭の ふくらみ
    poly(g, [(50, 34), (57, 29), (61, 29), (59, 32), (55, 37), (52, 38)], '3')                              # 上の 頭びれ
    poly(g, [(53, 43), (59, 44), (62, 47), (58, 48), (52, 47)], '3')                                        # 下の 頭びれ
    out = [r[:] for r in g]
    for y in range(64):
        for x in range(70):
            c = g[y][x]
            if c == '.': continue
            up = _run(g, x, y, 0, -1, c); dn = _run(g, x, y, 0, 1, c); lf = _run(g, x, y, -1, 0, c); rt = _run(g, x, y, 1, 0, c)
            if c == '1': out[y][x] = 'A' if up <= 1 else 'D' if dn <= 1 else 'B'
            elif c == '2': out[y][x] = 'A' if up <= 1 else 'E' if dn <= 2 else 'D' if dn == 3 else 'B'
            else: out[y][x] = 'D' if (dn <= 2 or rt <= 1) else 'A' if (up <= 2 or lf <= 1) else 'B'
    # 背骨の 稜線（うしろの 先から 頭へ）：光の すじ
    for x in range(12, 39):
        y = round(44 - (x - 12) * 0.12)
        if out[y][x] in 'BD': out[y][x] = 'A'
        if out[y + 1][x] in 'AB': out[y + 1][x] = 'D'
    # つばさの ひれの 骨（光の すじ）
    P(out, [(24, 37), (25, 38), (26, 39), (31, 33), (32, 34), (33, 35), (34, 36), (22, 48), (23, 49), (29, 49), (30, 50), (31, 51)], 'A', 'B')
    # 頭と つばさの さかい：影の 線
    for y in range(64):
        for x in range(1, 70):
            if g[y][x] == '3' and g[y][x - 1] in '12': out[y][x - 1] = 'D'
    # まゆの ひさし（目の 上で つり上がる 骨の 線）
    P(out, [(41, 35), (42, 35), (43, 35), (44, 36), (45, 36), (46, 36), (47, 37)], 'k')
    P(out, [(49, 33), (50, 33), (51, 33), (52, 34)], 'k')
    # 口：頭びれの あいだに 大きく さけた 口と 牙
    for y in range(37, 46):
        for x in range(52, 62):
            if g[y][x] == '.' and (x - 52) > abs(y - 41.5) * 1.1 and x < 60: out[y][x] = 'q'
    P(out, [(53, 39), (54, 40), (55, 39), (57, 38), (56, 41)], 'k', 'q')
    P(out, [(54, 39), (56, 38), (58, 38), (55, 44), (57, 44)], 'w')
    P(out, [(54, 43), (56, 43)], 'w', 'q')
    # 毒の いぼ（頭の 上）
    P(out, [(44, 33), (48, 32)], 'p'); P(out, [(43, 34), (47, 33)], 'P')
    ys = [y for y in range(64) if any(c != '.' for c in out[y])]; xs = [x for x in range(70) if any(out[y][x] != '.' for y in range(64))]
    return xs[0] - 1, ys[0] - 1, outline(rows_of([r[xs[0]:xs[-1] + 1] for r in out[ys[0]:ys[-1] + 1]]))
DX, DY, DISC = body()

# ---- 尾：根もとは 太く 体の うしろの 先に 食いこみ、上へ 大きく 反り返る。外がわに 毒の とげ ----
def tail(strike=False):
    W, H = 46, 36; g = grid(W, H)
    if not strike:
        pts = [(8, 33), (2, 24), (3, 11), (10, 3), (18, 2), (22, 5)]
    else:
        pts = [(8, 33), (2, 22), (6, 8), (18, 1), (32, 2), (42, 9)]
    def bez(t):
        n = len(pts) - 1; x = y = 0
        for i, (px, py) in enumerate(pts):
            b = math.comb(n, i) * (1 - t) ** (n - i) * t ** i; x += b * px; y += b * py
        return x, y
    spine = []
    for i in range(200):
        t = i / 199; x, y = bez(t); r = 3.8 - 2.3 * t
        spine.append((x, y, t))
        for yy in range(H):
            for xx in range(W):
                if (xx + .5 - x) ** 2 + (yy + .5 - y) ** 2 <= r * r: g[yy][xx] = '#'
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] != '#': continue
            up = _run(g, x, y, 0, -1, '#'); lf = _run(g, x, y, -1, 0, '#'); dn = _run(g, x, y, 0, 1, '#'); rt = _run(g, x, y, 1, 0, '#')
            out[y][x] = 'A' if (lf <= 1 or up <= 1) else 'D' if (rt <= 1 or dn <= 1) else 'B'
    # 毒の とげ：尾の 外がわ（左・上）に 3つ
    for t0 in (.3, .5, .68):
        x, y, _ = spine[int(t0 * 199)]
        x2, y2, _ = spine[int(t0 * 199) + 4]
        nx, ny = (y2 - y), -(x2 - x); L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        nx, ny = -nx, -ny
        r = 3.8 - 2.3 * t0
        tx, ty = -(y2 - y) * 0 + (x2 - x), (y2 - y); T = math.hypot(tx, ty) or 1; tx, ty = tx / T, ty / T
        for k in range(0, 5):
            for side in ((0, 1) if k < 2 else (0,)):
                px = round(x - nx * (r + k - .5) - tx * (k * .6) + tx * side)
                py = round(y - ny * (r + k - .5) - ty * (k * .6) + ty * side)
                if 0 <= py < H and 0 <= px < W: out[py][px] = 'P' if k >= 3 else 'p'
    return outline(rows_of(out)), spine[-1]
TAIL, (TX, TY, _) = tail()
TAIL_S, (SX, SY, _) = tail(True)
# 尾の 先の 毒針：ぎざぎざの 返しの ついた 骨の 大きな 針（前を 向く）
BARB = [
    '.kk...........',
    'kwnkk.........',
    'kwwnnkkk......',
    '.kwwwwnnkkk...',
    '..kkwwwwwnnkk.',
    '...kPkkwwwwnnk',
    '....kpPkkkkkk.',
    '.....kkpPk....',
    '.......kpk....',
    '........k.....',
]
BARB_HOT = [r.replace('w', 'P').replace('n', 'p') for r in BARB]
# 毒の ふくろ（つばさに 光る）
GL = ['Pp', 'pq']
GL_HOT = ['PP', 'Pp']
# 目（M：重い まぶた・半目）：厚い まぶた（A／B）が 金の 虹彩の 上半分を おおい、黒い まぶたの 線が 瞳を 横に 切る。下に 残る 金（Y／y）と 黒瞳で 冷たく 見下す。手前は 大きく、奥は 小さく
EYE = ['kAAAAAk', 'kkkkkkk', 'kYYkkYk', '.kyyyk.']
EYE_ALT = {'blink': ['kAAAAAk', 'kBBBBBk', 'kkkkkkk', '.BBBBB.'], 'atk0|atk1|atk2': ['kkkkkkk', 'kYYkkYk', 'kYYkkyk', '.kyyyk.'],
           'hit': ['kAAAAAk', 'kkBBkkB', 'BBkkBBB', '.BBBBB.'], 'ko': ['kAAAAAk', 'BkBBkBB', 'BBkkBBB', 'BkBBkBB']}
EYE2 = ['kkkk', 'kYkk', '.kyk']
EYE2_ALT = {'blink': ['kkkk', 'AAAA', '.AA.'], 'atk0|atk1|atk2': ['kYkk', 'kYkk', '.kyk'], 'hit': ['kkAA', 'AAkk', '.AA.'], 'ko': ['kAkA', 'AkAk', '.AA.']}
# 毒しぶき
SPRAY = [
    '.P...p..',
    'p.Pp..P.',
    '..pP.p..',
    '.P..p..P',
    '...p..p.',
]
DRIP = ['P', 'p']
# 海底の 砂けむり（すべる）
DUST = [['c....c', '.c..c.'], ['.c..c.', 'c....c']]
# つばさの 波うち：体を 列で 3つに 分ける（前の 列は 頭と いっしょ）
SEG = [(0, 12), (12, 25), (25, 99)]
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]
TBX, TBY = 0, 13
def layers():
    L = [
        dict(n='tail', g='tail', x=TBX, y=TBY, rows=TAIL, not_='atk1|atk2'),
        dict(n='barb', g='tail', x=TBX + round(TX) - 1, y=TBY + round(TY) - 2, rows=BARB, alt={'atk0': BARB_HOT}, not_='atk1|atk2'),
        dict(n='drip', g='tail', x=TBX + round(TX) + 3, y=TBY + round(TY) + 6, rows=DRIP, only='idle2|idle3|walk1|walk3'),
        dict(n='strike', g='root', x=TBX, y=TBY, rows=TAIL_S, only='atk1|atk2'),
        dict(n='barbS', g='root', x=TBX + round(SX) - 2, y=TBY + round(SY) - 1, rows=[r for r in BARB_HOT], only='atk1|atk2'),
    ]
    for i, (a, b) in enumerate(SEG):
        L.append(dict(n=f'd{i}', g=f'w{i}', x=DX + a, y=DY, rows=cut(DISC, a, b)))
    L += [
        dict(n='g1', g='w0', x=18, y=40, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g2', g='w1', x=26, y=35, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g3', g='w1', x=32, y=31, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g4', g='w1', x=21, y=48, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g5', g='w1', x=28, y=52, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g6', g='w2', x=36, y=47, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='eye', g='w2', x=41, y=36, rows=EYE, alt=EYE_ALT),
        dict(n='eye2', g='w2', x=49, y=34, rows=EYE2, alt=EYE2_ALT),
        dict(n='spray', g='root', x=TBX + round(SX) + 6, y=TBY + round(SY) + 2, rows=SPRAY, only='atk1'),
        dict(n='dust', g='root', x=6, y=58, rows=DUST[0], alt={'walk1|walk3': DUST[1]}, only='walk0|walk1|walk2|walk3'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'w0': (0, -1), 'tail': (0, -1)}, 'idle2': {'w1': (0, -1), 'tail': (0, -1)}, 'idle3': {'w2': (0, -1)},
    'blink': {},
    'walk0': {'w0': (0, -1)}, 'walk1': {'w1': (0, -1), 'tail': (1, 0)}, 'walk2': {'w2': (0, -1)}, 'walk3': {'w1': (0, 1), 'tail': (-1, 0)},
    'atk0': {'tail': (-1, -2), 'root': (-2, 0), 'w2': (0, 1)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (3, 0), 'w2': (0, 1)},
    'hit': {'root': (-3, 0), 'w2': (0, -2), 'w1': (0, -1), 'tail': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'w0': 'root', 'w1': 'root', 'w2': 'root', 'tail': 'root'}
