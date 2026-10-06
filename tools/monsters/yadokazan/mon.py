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
    poly(p, [(5, 52), (10, 38), (15, 24), (18, 16), (31, 16), (34, 24), (39, 36), (42, 46), (40, 53), (10, 55)], '1')
    s = shade(p, RAMP, r=3, hi=.25, lo=-.22)
    # 岩の 段（横の 割れ目）：手で 打つ
    for y, xs in ((24, range(17, 24)), (31, range(14, 21)), (38, range(10, 17)), (45, range(8, 14)), (27, range(28, 33)), (35, range(31, 37)), (43, range(34, 40))):
        for x in xs:
            if s[y][x] in 'ABC': s[y][x] = 'C'
            if s[y - 1][x] in 'BC' and x < 26: s[y - 1][x] = 'A'
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
    poly(s, [(33, 44), (39, 40), (43, 47), (40, 53), (34, 54)], 'k')
    poly(s, [(35, 45), (39, 42), (41, 47), (39, 52), (35, 52)], 'H')
    return rows_of(ink(s))

# ---------- 噴煙（idle で 形が かわる）----------
def smoke(ph):
    p = G()
    puffs = [[(24, 13, 4, 3), (21, 9, 4, 3.2), (17, 6, 3.5, 2.8), (12, 4, 2.5, 2)],
             [(25, 13, 4, 3), (22, 9, 4.2, 3), (18, 6, 3.4, 3), (13, 3, 3, 2.2)],
             [(24, 13, 4.4, 3), (21, 10, 3.6, 3), (17, 6, 4, 2.8), (12, 3, 2.6, 2.2)],
             [(25, 13, 4, 3.2), (21, 9, 3.8, 3.2), (16, 6, 3.6, 2.6), (11, 4, 2.4, 2)]][ph]
    for (cx, cy, rx, ry) in puffs: ellipse(p, cx, cy, rx, ry, '3')
    s = shade(p, {'3': 'STT'}, r=2, hi=.15, lo=-.1)
    return rows_of(ink(s))
def eruption():
    p = G()
    for (cx, cy, rx, ry) in ((25, 11, 5, 4), (20, 6, 4.4, 3.4), (14, 3, 3.4, 2.4)): ellipse(p, cx, cy, rx, ry, '3')
    s = shade(p, {'3': 'STT'}, r=2, hi=.15, lo=-.1)
    g = ink(s)
    # 噴き上がる 溶岩の しぶき
    put(g, ['..Y...', '.YOY.O', 'YOROYO', '.OYO..', '..O...'], 22, 9)
    dots(g, 'O', [(18, 12), (31, 8), (33, 11), (16, 9)]); dots(g, 'Y', [(30, 6), (19, 4)])
    return rows_of(g)

# ---------- カニの からだ・目・脚 ----------
def body():
    p = G()
    ellipse(p, 42.5, 44, 7, 6, '2')
    s = shade(p, RAMP, r=2)
    # 頭の 甲（かたい ふち）とげ
    dots(s, 'k', [(38, 42), (39, 41), (40, 41), (41, 41), (42, 41), (43, 41)])
    dots(s, 'E', [(39, 40), (41, 40), (43, 40)])
    # 口もと：小さい 牙
    put(s, ['kkk', 'wkw'], 46, 47)
    return rows_of(ink(s))
def stalks():
    p = G()
    tube(p, [(41, 40), (40, 34), (41, 30)], [1, 1, 1], '2')
    tube(p, [(45, 40), (46, 35), (48, 31)], [1.1, 1.1, 1.1], '2')
    s = shade(p, RAMP, r=1)
    s = [[DARK.get(c, c) if x < 43 and y < 41 else c for x, c in enumerate(r)] for y, r in enumerate(s)]
    return rows_of(ink(s))
# するどい 目：上が 平らな つり目＋たての ひとみ（まゆの とげ つき）
EYE_N = ['kkk....', 'kHkkkk.', '.kYYYkk', '.kYYkYk', '..kkkk.']
EYE_F = ['kkkk..', '.kOOkk', '.kOkOk', '..kkk.']
EYE_ATK = ['kkk....', 'kHkkkk.', '.kwYYkk', '.kYYYYk', '..kkkk.']
EYE_BL = ['kkk....', 'kHkkkk.', '.kFFFkk', '.kkkkkk', '..kkkk.']
EYE_HIT = ['kkk....', 'kHkkkk.', '.kYkYkk', '.kkYkkk', '..kkkk.']
EYE_KO = ['kkk....', 'kHkkkk.', '.kkFkkk', '.kFkFkk', '..kkkk.']
EYE_FKO = ['kkkk..', '.kkHkk', '.kHkHk', '..kkk.']

def leg(path, far=False):
    p = G(); tube(p, path, [1.6, 1.4, 1.0, .6][:len(path)], '2')
    s = shade(p, RAMP, r=1)
    if far: s = recol(s, DARK)
    g = ink(s)
    # 関節の 線
    x, y = path[1]; g[y][x] = 'k'
    return rows_of(g)

# 巨大な はさみ（見せ所）：ごつい 岩の こぶ＋赤熱した 刃先
def claw(mode):
    p = G()
    ellipse(p, 49, 45, 7.5, 6.5, '2')             # 掌（てのひら）
    tube(p, [(42, 47), (45, 46)], [3, 3.4], '2')    # うで
    if mode == 'open':
        poly(p, [(51, 39), (56, 34), (61, 33), (63, 35), (59, 37), (55, 41)], '2')    # 上の 指（大きく 開く）
        poly(p, [(53, 48), (59, 49), (63, 50), (60, 53), (54, 53)], '2')              # 下の 指
    else:
        poly(p, [(51, 39), (57, 38), (62, 41), (63, 44), (58, 43), (54, 44)], '2')    # 上の 指（とじる）
        poly(p, [(53, 48), (59, 47), (63, 45), (61, 49), (56, 51), (52, 51)], '2')   # 下の 指
    s = shade(p, RAMP, r=2, hi=.22, lo=-.25)
    # 岩の こぶ（掌の 上に 火山岩の よろい）
    for (x, y) in ((45, 41), (48, 40), (51, 41), (44, 44), (47, 43)):
        dots(s, 'B', [(x, y), (x + 1, y)]); dots(s, 'A', [(x, y - 1)]) if at(s, x, y - 1) != '.' else None
        dots(s, 'C', [(x + 1, y + 1)])
    # 赤熱した 刃先と 内がわの 歯
    g = ink(s)
    if mode == 'open':
        dots(g, 'Y', [(61, 34), (62, 34), (60, 35)]); dots(g, 'O', [(59, 36), (58, 37), (61, 35), (59, 34)])
        dots(g, 'w', [(56, 40), (58, 38), (60, 37)])
        dots(g, 'Y', [(62, 51), (61, 52)]); dots(g, 'O', [(60, 51), (59, 50), (62, 50), (60, 52)])
        dots(g, 'w', [(56, 48), (58, 48), (60, 48)])
    else:
        dots(g, 'Y', [(62, 43), (61, 42)]); dots(g, 'O', [(60, 42), (59, 41), (62, 42), (60, 43)])
        dots(g, 'w', [(56, 44), (58, 44), (60, 44)])
        dots(g, 'Y', [(62, 46), (61, 47)]); dots(g, 'O', [(60, 47), (59, 48), (62, 47)])
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
        dict(n='legF1', g='legB', x=0, y=0, rows=leg([(40, 48), (36, 53), (34, 59)], True), not_='ko'),
        dict(n='legF2', g='legA', x=0, y=0, rows=leg([(44, 49), (42, 54), (43, 60)], True)),
        dict(n='shell', g='shell', x=0, y=0, rows=V, alt={'idle1|idle3|walk1|walk3|atk1|atk2': VE}),
        dict(n='sclaw', g='body', x=0, y=0, rows=small_claw()),
        dict(n='stalks', g='head', x=0, y=0, rows=stalks()),
        dict(n='eyeF', g='head', x=38, y=28, rows=EYE_F, alt={'blink': ['kkkk..', '.kkkkk', '.kHHHk', '..kkk.'], 'ko': EYE_FKO, 'atk0|atk1|atk2': ['kkkk..', '.kYYkk', '.kYYYk', '..kkk.']}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legA1', g='legA', x=0, y=0, rows=leg([(39, 49), (33, 54), (30, 59)])),
        dict(n='legB1', g='legB', x=0, y=0, rows=leg([(44, 50), (46, 55), (49, 60)])),
        dict(n='eyeN', g='head', x=45, y=28, rows=EYE_N, alt={'blink': EYE_BL, 'atk0|atk1|atk2': EYE_ATK, 'hit': EYE_HIT, 'ko': EYE_KO}),
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
