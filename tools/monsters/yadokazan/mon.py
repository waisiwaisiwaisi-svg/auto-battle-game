# ヤドカザン（ほのお・いわ × ヤドカリ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

META = dict(id='yadokazan', name='ヤドカザン', types=['fire', 'rock'], base='ヤドカリ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1e22',
    'A': '#b4a494', 'B': '#76665e', 'C': '#42363a',      # 火山岩の 貝（明・中・暗）
    'Y': '#ffe45c', 'O': '#ff7a1e', 'R': '#b8281e',      # 溶岩
    'E': '#f09a64', 'F': '#c04a30', 'H': '#6a2028',      # カニの からだ（赤）
    'S': '#e4e0e8', 'T': '#9a94a6',                      # 噴煙
    'w': '#ffffff',
}
LIGHT = set('AYESw')
KEEP_BLACK = set('wY')

# ---------- 下書きの 道具（形の あたり → 左上光の 陰影 → 輪郭）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def ink(p):
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
            elif p[y][x] != '.': g[y][x] = p[y][x]
    return g
def shade(p, ramps, r=2, hi=.3, lo=-.28):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1): n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(64):
        for x in range(64):
            c = p[y][x]
            if c not in ramps: continue
            h, md, d = ramps[c]
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5
            out[y][x] = h if v > hi else d if v < lo else md
            if at(p, x, y - 1) == '.' or at(p, x - 1, y) == '.': out[y][x] = h
            if at(p, x, y + 1) == '.' or at(p, x + 1, y) == '.': out[y][x] = d
    return out
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < 64 and 0 <= y < 64 and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def recol(g, mp): return [[mp.get(c, c) for c in r] for r in g]
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g

RAMP = {'1': 'ABC', '2': 'EFH'}
DARK = {'A': 'B', 'B': 'C', 'E': 'F', 'F': 'H', 'Y': 'O', 'O': 'R'}

# ---------- 火山の 貝（円すい）：火口・溶岩の すじ・岩の 段 ----------
def volcano(erupt=False):
    p = G()
    poly(p, [(7, 52), (11, 38), (16, 24), (19, 16), (30, 16), (33, 24), (37, 36), (40, 46), (38, 53), (11, 55)], '1')
    s = shade(p, RAMP, r=3, hi=.25, lo=-.22)
    # 巻き貝の 段（らせんの みぞ）：左上から 右下へ 下がる すじ。みぞの 上は 光、下は 影
    xs = [x for x in range(64)]
    for y0 in (21, 29, 37, 45):
        for x in range(64):
            y = y0 + (x - 10) * 7 // 30
            if 0 <= y < 63 and s[y][x] in 'ABC' and at(s, x, y - 1) != '.':
                s[y][x] = 'k'
                if s[y + 1][x] in 'ABC': s[y + 1][x] = 'C' if x > 22 else 'B'
                if s[y - 1][x] in 'BC': s[y - 1][x] = 'A'
    # 火口（上の ふちの くぼみ）
    for x in range(19, 31): s[16][x] = 'k'
    for x in range(20, 30): s[17][x] = 'R' if not erupt else 'O'
    for x in range(21, 29): s[18][x] = 'C'
    s[17][19] = 'C'; s[17][30] = 'C'
    # 溶岩の すじ（火口から 流れ落ちる）
    flows = [[(22, 18), (21, 21), (21, 24), (19, 27), (19, 30), (17, 33), (16, 37)],
             [(26, 18), (27, 22), (27, 26), (29, 30), (30, 34), (31, 39), (33, 43), (33, 47)],
             [(24, 19), (24, 23), (23, 28), (24, 32), (23, 37), (22, 42), (22, 48)]]
    for f in flows:
        for i in range(len(f) - 1):
            line(s, *f[i], *f[i + 1], 'O')
    for f in flows:
        for (x, y) in f[:4] if not erupt else f:
            s[y][x] = 'Y'
    for f in flows:
        for (x, y) in f:
            if s[y][x + 1] in 'ABC': s[y][x + 1] = 'R'
    # 貝の 口（右下の 開いた ところ）：暗い 穴
    poly(s, [(31, 44), (36, 40), (40, 46), (38, 53), (32, 54)], 'k')
    poly(s, [(33, 45), (36, 42), (38, 47), (37, 52), (33, 52)], 'H')
    return rows_of(ink(s))

# ---------- 噴煙（もくもくの 玉を 奥から 1つずつ 重ねる）----------
def puffs(lst, g=None):
    g = g or G()
    for (cx, cy, rx, ry) in lst:
        p = G(); ellipse(p, cx, cy, rx, ry, '3')
        s = shade(p, {'3': 'SST'}, r=1, hi=.1, lo=-.05)
        stamp(g, rows_of(ink(s)), 0, 0)
    return g
SM = [[(14, 5, 3, 2.6), (19, 8, 3.6, 3), (26, 10, 3.4, 2.8), (23, 13, 4, 3)],
      [(13, 4, 3.2, 2.6), (19, 7, 3.8, 3), (26, 9, 3.2, 2.8), (24, 13, 4, 3)],
      [(12, 4, 3, 2.4), (18, 7, 4, 3.2), (25, 10, 3.6, 2.8), (23, 13, 4.2, 3)],
      [(13, 5, 2.8, 2.4), (18, 8, 3.8, 3), (26, 9, 3.4, 3), (24, 13, 3.8, 3)]]
def smoke(ph): return rows_of(puffs(SM[ph]))
def eruption():
    g = puffs([(12, 3, 3, 2.4), (18, 5, 4, 3), (28, 6, 3.6, 3), (24, 10, 4.6, 3.4)])
    put(g, ['...Y....', '.Y.OY.O.', 'O.YOOY..', '.YORROY.', '..OYYO..', '...OO...'], 20, 9)
    dots(g, 'O', [(17, 11), (31, 9), (33, 12), (15, 9)]); dots(g, 'Y', [(32, 5), (16, 2)])
    return rows_of(g)

# ---------- カニの からだ・目・脚 ----------
def body():
    p = G()
    ellipse(p, 41, 42, 6.5, 5.5, '2')
    s = shade(p, RAMP, r=2)
    # 頭の 甲の ふち（ぎざぎざ）
    for x in range(36, 46): s[39][x] = 'k' if x % 2 else s[39][x]
    dots(s, 'E', [(37, 38), (39, 38), (41, 38), (43, 38)])
    # 口もと：小さい 牙
    put(s, ['kkk.', 'wkwk'], 44, 44)
    return rows_of(ink(s))
def stalks():
    p = G()
    tube(p, [(41, 39), (40, 34), (40, 31)], [1.2, 1.2, 1.3], '2')
    tube(p, [(44, 39), (45, 34), (46, 30)], [1.5, 1.3, 1.5], '2')
    s = shade(p, RAMP, r=1)
    s = [[DARK.get(c, c) if x < 42 and y < 40 else c for x, c in enumerate(r)] for y, r in enumerate(s)]
    return rows_of(ink(s))
# するどい 目：上が 平らな つり目＋たての ひとみ（まゆの とげ つき）
EYE_N = ['kk..........', 'kHkk........', '.kHHkkkk....', '..kHHHHHkkk.', '.kOYYYYkkHHk', '.kOYYYkYYkHk', '.kOOYYkYYYOk', '..kkOOOOOOk.', '....kkkkkk..']
EYE_F = ['kkkk..', '.kOOkk', '.kOkOk', '..kkk.']
EYE_ATK = ['kk..........', 'kHkk........', '.kHHkkkk....', '..kHHHHHkkk.', '.kYwYYYYkHHk', '.kYYYYYYYYHk', '.kOYYYYYYYOk', '..kkOOOOOOk.', '....kkkkkk..']
EYE_BL = ['kk..........', 'kHkk........', '.kHHkkkk....', '..kHHHHHkkk.', '.kHHHHHHkHHk', '.kkkkkkkkkHk', '.kFFFFFFFFFk', '..kkFFFFFFk.', '....kkkkkk..']
EYE_HIT = ['kk..........', 'kHkk........', '.kHHkkkk....', '..kHHHHHkkk.', '.kFkkFFFkHHk', '.kFFFkkFFkHk', '.kFFFFFkkFFk', '..kkFFFFFFk.', '....kkkkkk..']
EYE_KO = ['kk..........', 'kHkk........', '.kHHkkkk....', '..kHHHHHkkk.', '.kFkFFkFkHHk', '.kFFkFFkFkHk', '.kFkFkkFkFFk', '..kkFFFFFFk.', '....kkkkkk..']
EYE_FKO = ['kkkk..', '.kkHkk', '.kHkHk', '..kkk.']

def leg(path, far=False):
    p = G(); tube(p, path, [1.6, 1.4, 1.0, .6][:len(path)], '2')
    s = shade(p, RAMP, r=1)
    if far: s = recol(s, DARK)
    g = ink(s)
    # 関節の 線
    x, y = path[1]; g[y][x] = 'k'
    return rows_of(g)

# 巨大な はさみ（見せ所）：箱形の 掌＋長い 2本の 指。岩の こぶ と 赤熱した 刃先
def claw(mode):
    p = G()
    tube(p, [(40, 49), (44, 47)], [2.6, 3.2], '2')    # うで
    poly(p, [(43, 41), (46, 37), (51, 36), (53, 38), (53, 51), (49, 54), (44, 53), (42, 49)], '2')   # 掌
    if mode == 'open':
        UP = [(50, 37), (54, 33), (58, 31), (62, 31), (62, 33), (58, 35), (55, 39), (53, 42)]
        LO = [(52, 45), (57, 46), (61, 47), (62, 50), (58, 52), (52, 52)]
    else:
        UP = [(50, 37), (55, 36), (59, 37), (62, 39), (62, 42), (59, 41), (55, 42), (52, 43)]
        LO = [(52, 45), (56, 45), (60, 45), (62, 44), (61, 48), (57, 51), (52, 52)]
    poly(p, UP, '2'); poly(p, LO, '2')
    s = shade(p, RAMP, r=2, hi=.2, lo=-.25)
    # 指の つけ根の 線
    if mode == 'open': line(s, 51, 38, 53, 42, 'k')
    else: line(s, 51, 38, 52, 42, 'k')
    line(s, 52, 45, 52, 51, 'k')
    # 岩の よろい：火山岩の こぶ と 溶岩の さけめ
    for (x, y) in ((44, 40), (47, 38), (45, 44)):
        dots(s, 'B', [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]); dots(s, 'A', [(x, y)]); dots(s, 'C', [(x + 1, y + 1), (x + 2, y + 1)])
    line(s, 45, 50, 50, 46, 'O'); dots(s, 'Y', [(47, 48), (48, 47)]); dots(s, 'R', [(46, 51), (49, 49), (51, 47)])
    g = ink(s)
    if mode == 'open':
        dots(g, 'Y', [(61, 32), (60, 32), (61, 31)]); dots(g, 'O', [(59, 32), (59, 33), (60, 33)])
        dots(g, 'w', [(55, 38), (57, 36), (59, 35)])
        dots(g, 'Y', [(61, 49), (60, 49)]); dots(g, 'O', [(59, 49), (61, 48), (59, 50)])
        dots(g, 'w', [(55, 45), (57, 46), (59, 47)])
        dots(g, 'k', [(54, 44), (55, 43)])
    else:
        dots(g, 'Y', [(61, 40), (61, 41)]); dots(g, 'O', [(60, 40), (61, 39), (60, 41)])
        dots(g, 'w', [(54, 43), (56, 43), (58, 42)])
        dots(g, 'Y', [(61, 45), (60, 46)]); dots(g, 'O', [(60, 45), (59, 46), (60, 47)])
        dots(g, 'w', [(55, 44), (57, 44)])
        for x in range(53, 61): 
            if g[44][x] in 'EFH': g[44][x] = 'k'
    return rows_of(g)
def small_claw():
    p = G(); ellipse(p, 46, 50, 3, 2.4, '2'); poly(p, [(47, 48), (51, 49), (50, 51), (47, 52)], '2')
    s = recol(shade(p, RAMP, r=1), DARK); return rows_of(ink(s))
SPARK1 = ['..Y.....Y..', 'Y..O..O...Y', '.O..YY..O..', '...YwwY....', '.O..YY..O..', 'Y..O..O...Y', '..Y.....Y..']
SPARK2 = ['.O...O.', '..Y.Y..', 'O..Y..O', '..Y.Y..', '.O...O.']
KO_SMOKE = ['..TT.', '.TSST', 'TSST.', '.TT..']

def layers():
    V = volcano(); VE = volcano(True)
    CL = claw('closed'); CO = claw('open')
    return [
        dict(n='smoke', g='smoke', x=0, y=0, rows=smoke(0), alt={'idle1|walk1|blink': smoke(1), 'idle2|walk2': smoke(2), 'idle3|walk3|hit': smoke(3), 'atk1|atk2': eruption()}, not_='atk1|atk2|ko'),
        dict(n='erupt', g='shell', x=0, y=0, rows=eruption(), only='atk1|atk2'),
        dict(n='legF1', g='legB', x=0, y=0, rows=leg([(39, 46), (36, 53), (35, 59)], True), not_='ko'),
        dict(n='legF2', g='legA', x=0, y=0, rows=leg([(43, 47), (42, 54), (43, 60)], True)),
        dict(n='shell', g='shell', x=0, y=0, rows=V, alt={'idle1|idle3|walk1|walk3|atk1|atk2': VE}),
        dict(n='stalks', g='head', x=0, y=0, rows=stalks()),
        dict(n='eyeF', g='head', x=37, y=28, rows=EYE_F, alt={'blink': ['kkkk..', '.kkkkk', '.kHHHk', '..kkk.'], 'ko': EYE_FKO, 'atk0|atk1|atk2': ['kkkk..', '.kYYkk', '.kYYYk', '..kkk.']}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legA1', g='legA', x=0, y=0, rows=leg([(37, 47), (32, 53), (30, 59)])),
        dict(n='legB1', g='legB', x=0, y=0, rows=leg([(42, 49), (46, 55), (49, 60)])),
        dict(n='eyeN', g='head', x=40, y=22, rows=EYE_N, alt={'blink': EYE_BL, 'atk0|atk1|atk2': EYE_ATK, 'hit': EYE_HIT, 'ko': EYE_KO}),
        dict(n='claw', g='claw', x=0, y=0, rows=CL, alt={'atk1': CO}),
        dict(n='spark', g='claw', x=55, y=36, rows=SPARK1, only='atk2'),
        dict(n='spark0', g='claw', x=58, y=38, rows=SPARK2, only='atk0'),
        dict(n='kosmoke', g='root', x=20, y=50, rows=KO_SMOKE, only='ko'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'claw': (0, 1)},
    'idle2': {'body': (0, 1), 'claw': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 0), 'claw': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1), 'shell': (0, -1), 'claw': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1), 'shell': (0, -1), 'claw': (0, -1)},
    'atk0': {'claw': (-3, 1), 'body': (-1, 1), 'shell': (-1, 1), 'smoke': (-1, 1)},
    'atk1': {'root': (2, 0), 'claw': (1, -3)},
    'atk2': {'root': (3, 0), 'claw': (0, 0)},
    'hit': {'root': (-3, 0), 'claw': (-2, 2), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'claw': 'body', 'body': 'root', 'shell': 'root', 'smoke': 'shell', 'legA': 'root', 'legB': 'root'}
