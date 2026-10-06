# ヤドカザン（ほのお・いわ × ヤドカリ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭の こうらと 目、小さな 胴、短い 脚、巨大な はさみ）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり → 左上光の 陰影 → 輪郭）。仕上げの 目・牙・模様は 手で 打つ ----------
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < N and 0 <= x < N: g[y][x] = ch
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g
def tube(p, path, rad, ch):
    """太さの かわる 管（手足・首・尾の あたり）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < N and 0 <= y < N and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def ink(p, ch='k'):
    """まわりに 1ドットの 輪郭"""
    g = G()
    for y in range(N):
        for x in range(N):
            if p[y][x] != '.': g[y][x] = p[y][x]
            elif any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = ch
    return g
def shade(p, ramps, r=2, hi=.3, lo=-.28):
    """左上から 光：ふくらみの 向きで 明・中・暗、上と 左の ふちは 明（三日月）、下と 右の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(N)] for y in range(N)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1): n += 1; s += m[yy][xx] if 0 <= yy < N and 0 <= xx < N else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(N):
        for x in range(N):
            c = p[y][x]
            if c not in ramps: continue
            h, md, d = ramps[c]
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5
            out[y][x] = h if v > hi else d if v < lo else md
            if at(p, x, y - 1) == '.' or at(p, x - 1, y) == '.': out[y][x] = h
            if at(p, x, y + 1) == '.' or at(p, x + 1, y) == '.': out[y][x] = d
    return out
def recol(g, mp): return [[mp.get(c, c) for c in r] for r in g]
def make(draw, ramps, r=2, hi=.3, lo=-.28, post=None, post2=None, dk=None):
    """draw(p) で あたり → 陰影 → post(s) 手打ち → 輪郭 → post2(g) 手打ち"""
    p = G(); draw(p); s = shade(p, ramps, r, hi, lo)
    if post: post(s)
    if dk: s = recol(s, dk)
    g = ink(s)
    if post2: post2(g)
    return rows_of(g)
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < N and 0 <= y + dy < N: g[y + dy][x + dx] = c
    return rows_of(g)
def over(*rowsets):
    g = G()
    for rs in rowsets: stamp(g, rs, 0, 0)
    return rows_of(g)
EYE_BOX = (28, 13, 18, 9)
META = dict(id='yadokazan', name='ヤドカザン', types=['fire', 'rock'], base='ヤドカリ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1e22',
    'A': '#b4a494', 'B': '#76665e', 'C': '#42363a',      # 火山岩の 貝（明・中・暗）
    'Y': '#ffe45c', 'O': '#ff7a1e', 'R': '#b8281e',      # 溶岩（目の 虹彩も 兼ねる）
    'E': '#f09a64', 'F': '#d0583a', 'H': '#6a2028',      # カニの からだ（赤）
    'S': '#e4e0e8', 'T': '#9a94a6',                      # 噴煙
    'w': '#ffffff',
}
LIGHT = set('AYESw')
KEEP_BLACK = set('wYO')
RAMP = {'1': 'ABC', '2': 'EFH'}
DARK = {'A': 'B', 'B': 'C', 'E': 'F', 'F': 'H', 'Y': 'O', 'O': 'R'}

# ---------- 火山の 貝（円すい）----------
def volcano(erupt=False):
    def d(p): poly(p, [(4, 54), (9, 41), (13, 29), (16, 19), (27, 19), (30, 28), (33, 38), (36, 47), (35, 54), (8, 56)], '1')
    def post(s):
        # 巻き貝の 段（らせんの みぞ）：みぞの 上は 光、下は 影
        for y0 in (25, 33, 41, 48):
            for x in range(64):
                y = y0 + (x - 10) * 6 // 30
                if 0 <= y < 63 and s[y][x] in 'ABC' and at(s, x, y - 1) != '.' and at(s, x, y + 1) != '.':
                    s[y][x] = 'k'
                    if s[y + 1][x] in 'ABC': s[y + 1][x] = 'C' if x > 24 else 'B'
                    if s[y - 1][x] in 'BC': s[y - 1][x] = 'A'
        for x in range(16, 28): s[19][x] = 'k'
        for x in range(17, 27): s[20][x] = 'O' if erupt else 'R'
        for x in range(18, 26): s[21][x] = 'C'
        flows = [[(19, 21), (18, 25), (17, 29), (15, 33), (14, 37)],
                 [(24, 21), (25, 25), (27, 29), (28, 33), (30, 38), (31, 43)],
                 [(21, 22), (21, 26), (20, 31), (21, 35), (20, 40), (19, 46)]]
        for f in flows:
            for i in range(len(f) - 1): line(s, *f[i], *f[i + 1], 'O')
        for f in flows:
            for (x, y) in (f if erupt else f[:3]): s[y][x] = 'Y'
            for (x, y) in f:
                if s[y][x + 1] in 'ABC': s[y][x + 1] = 'R'
        # 貝の 口（カニが 出てくる 暗い 穴）
        poly(s, [(29, 44), (34, 40), (37, 47), (36, 54), (30, 55)], 'k')
    return make(d, RAMP, r=3, hi=.25, lo=-.22, post=post)

# ---------- 噴煙 ----------
def puffs(lst):
    g = G()
    for (cx, cy, rx, ry) in lst:
        stamp(g, make(lambda p: ellipse(p, cx, cy, rx, ry, '3'), {'3': 'SST'}, r=1, hi=.1, lo=-.05), 0, 0)
    return g
SM = [[(14, 7, 3, 2.6), (19, 10, 3.6, 3), (25, 11, 3.2, 2.8), (21, 15, 4, 3)],
      [(13, 6, 3.2, 2.6), (19, 9, 3.8, 3), (25, 10, 3.2, 2.8), (22, 15, 4, 3)],
      [(12, 6, 3, 2.4), (18, 9, 4, 3.2), (24, 11, 3.6, 2.8), (21, 15, 4.2, 3)],
      [(13, 7, 2.8, 2.4), (18, 10, 3.8, 3), (25, 10, 3.4, 3), (22, 15, 3.8, 3)]]
def smoke(ph): return rows_of(puffs(SM[ph]))
def eruption():
    g = puffs([(11, 5, 3, 2.4), (17, 7, 4, 3), (27, 8, 3.6, 3), (22, 12, 4.6, 3.4)])
    put(g, ['...Y....', '.Y.OY.O.', 'O.YOOY..', '.YORROY.', '..OYYO..', '...OO...'], 18, 12)
    dots(g, 'O', [(15, 13), (30, 11), (32, 14), (13, 11)]); dots(g, 'Y', [(31, 6), (15, 3)])
    return rows_of(g)

# ---------- カニ：胴（小さく 丸い）・頭の こうら（大きい）・目の 柄 ----------
def body(): return make(lambda p: ellipse(p, 38, 47, 6.5, 5, '2'), RAMP, lo=-.4)
def head(open_=False):
    def d(p):
        ellipse(p, 40, 33, 10, 7.5, '2')
        poly(p, [(32, 29), (46, 28), (50, 32), (50, 39), (31, 39)], '2')
    def post(s):
        # こうらの 段（ぎざぎざの ふち）と いぼ
        for x in range(32, 46, 2):
            if s[30][x] != '.' and at(s, x, 29) != '.': s[30][x] = 'k'
        dots(s, 'H', [(33, 34), (34, 35), (36, 37)]); dots(s, 'E', [(33, 33), (35, 36)])
        # 口：よこに さけた あご と 牙
        if open_:
            put(s, ['kkkkkkkkk', 'kwwkRwwkw', 'RRwRRRwRR', 'RRRRRRRRR', 'RRwRRRwRR', 'kwwkkwwkk'], 42, 34)
        else:
            put(s, ['kkkkkkkkk', 'kwwkFwwkw', 'FFwFFFwFF'], 42, 35)
    def post2(g):
        if open_:
            for y in range(34, 41): g[y][51] = 'k'
    return make(d, RAMP, lo=-.4, post=post, post2=post2)
# 目：柄の 先の 目（R）。頭から のびる 細い 柄の 先に 丸い 目玉。黄色い 目玉に よこ長の 黒い 瞳、怒った 上まぶた
def stalk(far=False):
    if far: return make(lambda p: tube(p, [(35, 29), (34, 22)], [1.4, 1.2], '2'), RAMP, r=1, dk=DARK)
    return make(lambda p: tube(p, [(45, 30), (45, 21)], [2, 1.7], '2'), RAMP, r=1)
EYE = ['..kkkkk..', '.kHFFFHkk', 'kwkkkkkkk', 'kwYYYYYYk', 'kYkkkkkYk', 'kOkkkkkOk', 'kROOYOORk', '.kRROORk.', '..kkkkk..']
EYE_ALT = {
    'blink': ['..kkkkk..', '.kHFFFHkk', 'kEFFFFFFk', 'kFFFFFFFk', 'kFFFFFFFk', 'kkkkkkkkk', 'kHFFFFFHk', '.kHHHHHk.', '..kkkkk..'],
    'hit':   ['..kkkkk..', '.kHFFFHkk', 'kFFFFFFFk', 'kFFFFFFFk', 'kkkkkkkkk', 'kYYYkkYYk', 'kROOOOORk', '.kRROORk.', '..kkkkk..'],
    'atk0|atk1|atk2': ['..kkkkk..', '.kHFFkkkk', 'kwkkkkkYk', 'kwwYYYYYk', 'kYYYYYYYk', 'kYkkkkkYk', 'kOYYYYYOk', '.kOOOORk.', '..kkkkk..'],
    'ko':    ['..kkkkk..', '.kHFFFHkk', 'kkkkkkkkk', 'kYkYYYkYk', 'kYYkYkYYk', 'kOOOkOOOk', 'kROkOkORk', '.kkROOkk.', '..kkkkk..'],
}
EYEF = ['.kkkk.', 'kHFFkk', 'kYkkYk', 'kOkkOk', '.kRRk.', '..kk..']
EYEF_ALT = {'blink|ko': ['.kkkk.', 'kHFFkk', 'kHHHHk', 'kkkkkk', '.kHHk.', '..kk..'], 'hit': ['.kkkk.', 'kHFFkk', 'kHHHHk', 'kYkkOk', '.kRRk.', '..kk..'],
            'atk0|atk1|atk2': ['.kkkk.', 'kHFFkk', 'kYYYYk', 'kOkkOk', '.kRRk.', '..kk..']}

def leg(path, far=False):
    def post2(g): x, y = path[1]; g[y][x] = 'k'
    return make(lambda p: tube(p, path, [2, 1.7, 1.1][:len(path)], '2'), RAMP, r=1, dk=DARK if far else None, post2=post2)

# 巨大な はさみ（見せ所）：火山岩の よろいの 掌（溶岩の さけめ）＋赤熱した 2本の 指
def claw(mode):
    def d(p):
        tube(p, [(40, 50), (46, 50)], [2.6, 3.2], '2')
        poly(p, [(43, 44), (46, 39), (53, 38), (57, 41), (57, 56), (52, 60), (45, 59), (42, 53)], '1')
        if mode == 'open':
            poly(p, [(52, 42), (56, 37), (60, 34), (63, 34), (63, 36), (60, 39), (57, 44), (55, 47)], '2')
            poly(p, [(55, 50), (59, 51), (62, 52), (63, 55), (59, 58), (54, 57)], '2')
        else:
            poly(p, [(52, 41), (57, 38), (62, 39), (64, 43), (64, 47), (60, 46), (57, 47), (55, 48)], '2')
            poly(p, [(55, 50), (58, 50), (62, 50), (64, 49), (63, 55), (58, 58), (54, 58)], '2')
    def post(s):
        # 岩の 板の すき間から 溶岩
        line(s, 46, 54, 52, 47, 'O'); line(s, 48, 44, 50, 48, 'O'); dots(s, 'Y', [(49, 51), (50, 50), (49, 46)])
        dots(s, 'R', [(47, 55), (50, 53), (53, 49), (50, 45)])
        dots(s, 'A', [(46, 46), (47, 45), (45, 48)])
    def post2(g):
        line(g, 54, 43, 55, 48, 'k'); line(g, 55, 50, 55, 56, 'k')
        if mode == 'open':
            dots(g, 'Y', [(62, 35), (61, 35), (62, 34)]); dots(g, 'O', [(60, 35), (60, 36), (61, 36)])
            dots(g, 'w', [(57, 42), (59, 40), (61, 38)])
            dots(g, 'Y', [(62, 54), (61, 54)]); dots(g, 'O', [(60, 54), (62, 53), (60, 55)])
            dots(g, 'w', [(57, 51), (59, 52), (61, 52)])
        else:
            dots(g, 'Y', [(62, 45), (62, 46)]); dots(g, 'O', [(61, 45), (62, 44), (61, 46)])
            dots(g, 'w', [(57, 48), (59, 48), (61, 47)])
            dots(g, 'Y', [(62, 50), (61, 51)]); dots(g, 'O', [(61, 50), (60, 51), (61, 52)])
            dots(g, 'w', [(57, 49), (59, 49)])
    return make(d, RAMP, hi=.2, lo=-.3, post=post, post2=post2)
def small_claw(): return make(lambda p: (tube(p, [(34, 47), (31, 50)], [2, 2.2], '2'), ellipse(p, 30, 51, 3, 2.6, '2')), RAMP, r=1, dk=DARK)
SPARK1 = ['..Y.....Y..', 'Y..O..O...Y', '.O..YY..O..', '...YwwY....', '.O..YY..O..', 'Y..O..O...Y', '..Y.....Y..']
SPARK2 = ['.O...O.', '..Y.Y..', 'O..Y..O', '..Y.Y..', '.O...O.']

def layers():
    V = volcano(); VE = volcano(True); CL = claw('closed'); CO = claw('open'); H = head(); HO = head(True)
    return [
        dict(n='smoke', g='smoke', x=-1, y=3, rows=smoke(0), alt={'idle1|walk1|blink': smoke(1), 'idle2|walk2': smoke(2), 'idle3|walk3|hit': smoke(3)}, not_='atk1|atk2|ko'),
        dict(n='erupt', g='shell', x=-1, y=3, rows=eruption(), only='atk1|atk2'),
        dict(n='legF1', g='legB', x=-3, y=0, rows=leg([(35, 50), (32, 56), (31, 60)], True)),
        dict(n='legF2', g='legA', x=-3, y=0, rows=leg([(41, 51), (41, 56), (42, 60)], True)),
        dict(n='shell', g='shell', x=-1, y=0, rows=V, alt={'idle1|idle3|walk1|walk3|atk1|atk2': VE}),
        dict(n='sclaw', g='body', x=-3, y=0, rows=small_claw()),
        dict(n='stalkF', g='head', x=-3, y=0, rows=stalk(True)),
        dict(n='eyeF', g='head', x=28, y=16, rows=EYEF, alt=EYEF_ALT),
        dict(n='body', g='body', x=-3, y=0, rows=body()),
        dict(n='legA1', g='legA', x=-3, y=0, rows=leg([(36, 51), (34, 56), (33, 60)])),
        dict(n='legB1', g='legB', x=-3, y=0, rows=leg([(41, 52), (44, 56), (45, 60)])),
        dict(n='stalk', g='head', x=-3, y=0, rows=stalk()),
        dict(n='head', g='head', x=-3, y=0, rows=H, alt={'atk1': HO}),
        dict(n='eye', g='head', x=37, y=13, rows=EYE, alt=EYE_ALT),
        dict(n='claw', g='claw', x=-1, y=0, rows=CL, alt={'atk1': CO}),
        dict(n='spark', g='claw', x=54, y=42, rows=SPARK1, only='atk2'),
        dict(n='spark0', g='claw', x=56, y=44, rows=SPARK2, only='atk0'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'claw': (-3, 1), 'body': (-1, 1), 'head': (0, 1)},
    'atk1': {'root': (2, 0), 'claw': (1, -3)},
    'atk2': {'root': (3, 0)},
    'hit': {'root': (-3, 0), 'claw': (-2, 2), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'claw': 'body', 'shell': 'body', 'smoke': 'shell', 'body': 'root', 'legA': 'root', 'legB': 'root'}
