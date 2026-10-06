# カザミドリ（かぜ・はがね × ニワトリ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

META = dict(id='kazamidori', name='カザミドリ', types=['wind', 'steel'], base='ニワトリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2a2c40',
    'S': '#e2e8f2', 'T': '#8e9ab2', 'U': '#4c5470',      # 鋼の 羽
    'C': '#ffb27a', 'c': '#d0623a', 'd': '#7a3024',      # 銅の とさか（風見の 矢）
    'Y': '#ffe066', 'y': '#c08a28',                      # くちばし・足
    'R': '#ff4a3a',                                      # 目
    'W': '#effcff', 'V': '#86d4ea',                      # 風
    'w': '#ffffff',
}
LIGHT = set('SCYWw')
KEEP_BLACK = set('wRY')

# ---------- 下書きの 道具 ----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def ink(p, g=None):
    g = g or G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
    return g
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(64) for x in range(64) if m[y][x]}
RAMP = {'1': 'STU', '2': 'Ccd', '3': 'YYy', '4': 'TUU'}
def shade(p, r=2, hi=.35, lo=-.3):
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in RAMP:
            h, m, d = RAMP[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def tube(p, path, rad, ch='1'):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64: p[y][x] = ch
def part(fn, r=2, hi=.35, lo=-.3):
    """下書き → 陰影 → 輪郭 の ひとまとまり"""
    p = G(); fn(p); return ink(shade(p, r, hi, lo))
def over(g, h):
    for y in range(64):
        for x in range(64):
            if h[y][x] != '.': g[y][x] = h[y][x]
    return g
DARK = {'S': 'T', 'T': 'U', 'U': 'l', 'Y': 'y', 'y': 'd', 'C': 'c', 'c': 'd'}
def dark(g): return [[DARK.get(c, c) for c in r] for r in g]
def shift(g, dx, dy):
    o = G()
    for y in range(64):
        for x in range(64):
            if g[y][x] != '.' and 0 <= x + dx < 64 and 0 <= y + dy < 64: o[y + dy][x + dx] = g[y][x]
    return o

# ---------- 尾：鋼の 鎌の 羽（3枚）----------
def tail():
    g = G()
    for path, rad in (
        ([(19, 37), (12, 37), (6, 35), (2, 37)], [2.6, 2.2, 1.6, .9]),
        ([(19, 35), (12, 29), (6, 24), (2, 25)], [2.8, 2.4, 1.8, 1]),
        ([(20, 33), (15, 24), (11, 15), (7, 10), (3, 11)], [3, 2.8, 2.3, 1.7, 1]),
    ):
        h = part(lambda p: tube(p, path, rad), r=1)
        # 羽の 軸（中央の 暗い 線）
        for i in range(len(path) - 1):
            (x0, y0), (x1, y1) = path[i], path[i + 1]
            line(h, round(x0), round(y0), round(x1), round(y1), 'U')
        over(g, h)
    return g
WIND0 = ['..WWV....', '.W...V...', 'W..VV.V..', 'V.W..V...', '.V..V....']
WIND1 = ['...WWV...', '..W...V..', '.W..VV.V.', '.V.W..V..', '..V..V...']

# ---------- 胴：鋼の 板の 胸 ----------
BODY_PTS = [(15, 31), (20, 26), (28, 24), (35, 24), (41, 28), (44, 34), (42, 41), (36, 46), (27, 48), (19, 45), (14, 38)]
def body():
    g = part(lambda p: poly(p, BODY_PTS, '1'), r=3)
    # 胸の 鋼板の つなぎ目（弧）とびょう
    for (x0, y0, x1, y1) in ((38, 27, 41, 33), (41, 33, 40, 40), (34, 30, 36, 37), (36, 37, 33, 43)):
        line(g, x0, y0, x1, y1, 'l')
    dots(g, 'S', [(39, 30), (40, 37), (35, 33)])
    return g

# ---------- 首と 頭 ----------
def head(eye='n'):
    def neck(p):
        tube(p, [(32, 31), (36, 23), (40, 17)], [6, 5.2, 4.5])
        ellipse(p, 43, 13.5, 5.6, 5.2, '1')
    g = part(neck, r=2)
    # 首の 羽（後ろへ 垂れる とがった 羽先）
    for (x, y) in ((31, 24), (30, 28), (30, 32), (33, 20)):
        stamp(g, ['kk..', 'kTk.', '.kTk', '..kk'], x - 3, y)
    for (x0, y0, x1, y1) in ((35, 22, 33, 27), (38, 20, 35, 30), (40, 22, 38, 31)):
        line(g, x0, y0, x1, y1, 'l')
    # くちばし（かぎ形）
    b = part(lambda p: poly(p, [(46, 10.5), (51, 11), (55, 13), (55, 16), (53, 15), (47, 16)], '3'), r=1, hi=.2)
    line(b, 48, 14, 53, 14, 'k'); dots(b, 'y', [(54, 15), (54, 14)])
    over(g, b)
    # 肉垂（銅）
    over(g, part(lambda p: poly(p, [(45, 16), (49, 16), (49.5, 21), (47, 23), (45, 20)], '2'), r=1))
    # するどい 目：つり上がった まゆ＋赤い 目、たての ひとみ
    E = {
        'n': ['kkk.....', '.kkkkk..', '..kRRRkk', '..kRRkk.', '...kk...'],
        'blink': ['kkk.....', '.kkkkk..', '..kkkkk.', '...kkk..', '........'],
        'atk': ['kkk.....', '.kkkkkk.', '..kRRRRk', '..kRRRk.', '...kk...'],
        'hit': ['.k......', '..kkkk..', '.kRkRk..', '..kRk...', '...k....'],
        'ko': ['........', '..k.k...', '...k....', '..k.k...', '........'],
    }[eye]
    stamp(g, E, 39, 9)
    if eye == 'ko':
        for (x, y) in ((40, 10), (41, 10), (41, 11), (42, 11), (40, 12)): pass
    return g
def head_open():
    """攻撃：くちばしを 大きく 開いて さけぶ"""
    g = head('atk')
    for y in range(9, 20):
        for x in range(46, 58):
            if g[y][x] in 'YyCcdk': g[y][x] = '.'
    over(g, part(lambda p: poly(p, [(46, 10.5), (51, 10), (57, 11), (57, 13), (52, 12.5), (47, 13.5)], '3'), r=1, hi=.2))
    over(g, part(lambda p: poly(p, [(47, 14), (52, 15), (55, 18), (52, 18), (47, 17)], '3'), r=1, hi=.2))
    over(g, part(lambda p: poly(p, [(45, 17), (48, 17), (49, 22), (47, 24), (45, 21)], '2'), r=1))
    return g

# ---------- とさか：風見の 矢（矢羽根が とさか、先に 矢じり）----------
def comb(spin=0):
    def f(p):
        # 矢羽根（ぎざぎざの 平たい 板）
        poly(p, [(30, 10), (27, 1), (31, 3.5), (33, 0), (36, 3.5), (39, 0.5), (42, 4), (44, 1.5), (46, 8), (45, 10)], '2')
        # 矢の 軸
        for x in range(38, 54): p[6][x] = '2'; p[7][x] = '2'
        # 矢じり
        poly(p, [(52, 2.5), (60, 7), (52, 11.5), (54, 7)], '2')
    g = part(f, r=1, hi=.25)
    # 矢羽根の すじ
    for x0 in (32, 35, 38, 41):
        line(g, x0, 4, x0 + 1, 9, 'd')
    line(g, 38, 7, 52, 7, 'd')
    return g

# ---------- 翼（たたんだ 鋼の 刃の 羽）----------
def wing(up=False):
    if not up:
        pts = [(21, 31), (32, 29), (38, 33), (34, 39), (25, 43), (13, 45), (11, 42), (15, 37)]
    else:
        pts = [(23, 32), (31, 30), (33, 25), (28, 17), (21, 12), (14, 11), (15, 16), (12, 19), (16, 23), (13, 26), (18, 30)]
    g = part(lambda p: poly(p, pts, '1'), r=2)
    if not up:
        for (x0, y0, x1, y1) in ((33, 34, 14, 42), (31, 37, 17, 44), (34, 31, 18, 37)):
            line(g, x0, y0, x1, y1, 'l')
    else:
        for (x0, y0, x1, y1) in ((29, 28, 15, 13), (27, 30, 14, 19), (25, 31, 15, 25)):
            line(g, x0, y0, x1, y1, 'l')
    return g

# ---------- 足：太もも（鋼）＋すね（金）＋巨大な 蹴爪 ----------
def leg(hip, knee, ankle, toes, spur, back=False):
    def f(p):
        tube(p, [hip, knee], [4.2, 3], '1')
    g = part(f, r=2)
    def s(p):
        tube(p, [knee, ankle], [1.6, 1.4], '3')
        for t in toes: tube(p, [ankle, t], [1.2, .8], '3')
    over(g, part(s, r=1, hi=.1))
    # 蹴爪：後ろへ 反る 大きな 刃
    over(g, part(lambda p: poly(p, spur, '1'), r=1, hi=.1))
    for t in toes: dots(g, 'w', [t])
    return dark(g) if back else g
LEG_A = dict(hip=(33, 45), knee=(35, 50), ankle=(34, 58), toes=[(40, 60), (38, 61), (30, 60)], spur=[(34, 52), (29, 52.5), (24, 50), (21, 46), (25, 51.5), (29, 55.5), (34, 56)])
LEG_B = dict(hip=(24, 45), knee=(25, 50), ankle=(23, 58), toes=[(29, 60), (27, 61), (19, 60)], spur=[(23, 52), (18, 52.5), (13, 50), (10, 46), (14, 51.5), (18, 55.5), (23, 56)])
# 飛びげり：両足を 前へ つき出し、蹴爪が 先頭
KICK_A = dict(hip=(33, 45), knee=(39, 48), ankle=(45, 54), toes=[(50, 55), (49, 57), (43, 58)], spur=[(44, 52), (48, 49), (53, 48), (56, 49), (52, 51), (48, 54), (45, 55)])
KICK_B = dict(hip=(26, 45), knee=(31, 50), ankle=(36, 56), toes=[(41, 57), (40, 59), (34, 60)], spur=[(35, 54), (39, 51), (44, 50), (47, 51), (43, 53), (39, 56), (36, 57)])

# ---------- 風の 斬撃 ----------
SLASH = [
    '......kkkk.......',
    '....kkWWWVkk.....',
    '...kWWVVkkVVk....',
    '..kWVkk...kkVk...',
    '..kWk.......kVk..',
    '.kWVk........kk..',
    '.kWk.............',
    'kWVk.............',
    'kWVk.............',
    'kWVk.............',
    '.kWVk............',
    '.kWVk.....kk.....',
    '..kWVkk..kVk.....',
    '...kWWVkkVk......',
    '....kkWWVVk......',
    '......kkkk.......',
]
GUST = ['W..V....W.', '.WW.VV.W..', '..V..WWV.V', 'W..V...W..']

def layers():
    T = rows_of(tail()); B = rows_of(body()); H = rows_of(head())
    W = rows_of(wing()); WU = rows_of(wing(True)); CB = rows_of(comb())
    LA = rows_of(leg(**LEG_A)); LB = rows_of(leg(**LEG_B, back=True))
    KA = rows_of(leg(**KICK_A)); KB = rows_of(leg(**KICK_B, back=True))
    ATK = 'atk1|atk2'
    return [
        dict(n='legB', g='legB', x=0, y=0, rows=LB, alt={ATK: KB}),
        dict(n='tail', g='tail', x=0, y=0, rows=T),
        dict(n='wind', g='tail', x=0, y=2, rows=WIND0, alt={'idle1|idle3|walk1|walk3': WIND1}, not_='ko|hit'),
        dict(n='body', g='body', x=0, y=0, rows=B),
        dict(n='legA', g='legA', x=0, y=0, rows=LA, alt={ATK: KA}),
        dict(n='comb', g='comb', x=0, y=0, rows=CB),
        dict(n='head', g='head', x=0, y=0, rows=H, alt={
            'blink': rows_of(head('blink')), 'atk0': rows_of(head('atk')), ATK: rows_of(head_open()),
            'hit': rows_of(head('hit')), 'ko': rows_of(head('ko'))}),
        dict(n='wing', g='wing', x=0, y=0, rows=W, alt={'atk0|atk1': WU}),
        dict(n='slash', g='fx', x=46, y=36, rows=SLASH, only='atk1'),
        dict(n='gust', g='fx', x=52, y=40, rows=GUST, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'comb': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, -1)},
    'idle3': {'body': (0, 0), 'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (-1, 0)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 0), 'legA': (-1, 0), 'legB': (-1, 0)},
    'atk1': {'root': (4, -5), 'head': (0, 1)},
    'atk2': {'root': (6, -2), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'body': (-1, 1), 'head': (-3, 1), 'comb': (-1, 0), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'comb': 'head', 'wing': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
