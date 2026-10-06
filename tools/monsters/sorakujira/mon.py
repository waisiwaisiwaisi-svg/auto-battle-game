# ソラクジラ（かぜ・みず × クジラ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

META = dict(id='sorakujira', name='ソラクジラ', types=['wind', 'water'], base='クジラ', size='L')
PAL = {
    'k': '#101018', 'l': '#1c2848',
    'A': '#8cc0ec', 'B': '#4a7cc0', 'D': '#2a4682',      # 背（空色の 鯨）
    'E': '#eef2f4', 'F': '#a4b6ca',                      # 腹の うね
    'Y': '#ffd862', 'y': '#a8782c',                      # 真鍮の プロペラ・目
    'r': '#d0405a', 'm': '#5c1830',                      # 口の 中
    'w': '#ffffff',
    'W': '#f2fbff', 'V': '#90c8e8',                      # 雲・しぶき
}
LIGHT = set('AEYWw')
KEEP_BLACK = set('wYrm')
RAMP = {'1': 'ABD', '2': 'EEF', '3': 'YYy', '4': 'BDD', '5': 'WWV'}
DARK = {'A': 'B', 'B': 'D', 'D': 'l', 'E': 'F', 'Y': 'y'}

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
def dark(g): return [[DARK.get(c, c) for c in r] for r in g]
def shift(g, dx, dy):
    o = G()
    for y in range(64):
        for x in range(64):
            if g[y][x] != '.' and 0 <= x + dx < 64 and 0 <= y + dy < 64: o[y + dy][x + dx] = g[y][x]
    return o

# ---------- 胴：飛行船の ような 細長い だ円、前は 四角い 巨大な 頭 ----------
BODY = [(9, 30), (13, 27), (22, 23), (29, 19), (35, 13), (44, 9), (56, 8), (61, 10), (63, 15), (63, 31), (61, 37), (34, 38), (22, 36), (13, 34)]
def body():
    def f(p):
        poly(p, BODY, '1')
        # 腹がわ（下の 帯）は 白い うね
        for y in range(64):
            for x in range(64):
                if p[y][x] == '1' and y > 33 - (x - 30) * .05 and x < 34: p[y][x] = '2'
    g = part(f, r=3)
    # 飛行船の 縫い目（胴に そった 長い すじ）
    for pts in (((14, 28), (24, 24), (31, 20), (40, 15), (52, 13), (60, 14)), ((12, 31), (24, 29), (32, 27), (36, 25))):
        for i in range(len(pts) - 1): line(g, *pts[i], *pts[i + 1], 'l')
    # 帯の 金具（たての 帯＋びょう）
    for x in (24, 25):
        for y in range(19, 38):
            if g[y][x] in 'ABDEF': g[y][x] = 'y' if x == 25 else 'Y'
    # 頭の 古傷（白い ひっかき）
    for (x0, y0, x1, y1) in ((50, 18, 55, 23), (54, 17, 59, 22), (47, 22, 50, 25)):
        line(g, x0, y0, x1, y1, 'F')
    return g
# 口の 線と 目（目は 口の 角の 上、骨の ひさしの 下）
def face(g, eye='n'):
    line(g, 34, 37, 62, 37, 'k')
    E = {
        'n':     ['kkkk.....', '.kkkkkk..', '..kYYYkk.', '..kYkkk..', '...kk....'],
        'blink': ['kkkk.....', '.kkkkkk..', '..kkkkkk.', '...kkk...', '.........'],
        'atk':   ['kkkk.....', '.kkkkkkk.', '..kYYYYk.', '..kYYkk..', '...kk....'],
        'hit':   ['.k...k...', '..kkk....', '.kYkYk...', '..kYk....', '...k.....'],
        'ko':    ['.........', '.k.k.....', '..k......', '.k.k.....', '.........'],
    }[eye]
    stamp(g, E, 37, 27)
    # 骨の ひさし（目の 上に 張り出す 板）
    for x in range(35, 47): g[26][x] = 'l' if g[26][x] != '.' else '.'
    dots(g, 'A', [(x, 25) for x in range(36, 46)])
    return g
def teeth():
    g = G()
    for x in range(40, 62, 3):
        dots(g, 'w', [(x, 37), (x, 38)]); dots(g, 'k', [(x - 1, 38), (x + 1, 38), (x, 39)])
    return g
def head_body(eye='n'): return face(body(), eye)

# ---------- 下あご：長い あごに 牙の 列 ----------
def jaw(open_=0):
    if open_ == 0: pts = [(32, 37), (62, 37), (61, 40), (57, 43), (40, 43), (34, 41)]
    elif open_ == 1: pts = [(32, 37), (60, 42), (59, 46), (55, 48), (40, 45), (34, 41)]
    else: pts = [(32, 37), (58, 49), (56, 53), (52, 54), (39, 47), (33, 42)]
    g = part(lambda p: poly(p, pts, '2'), r=1)
    for (x0, y0, x1, y1) in ((38, 41, 54, 42 + open_ * 3),):
        line(g, x0, y0, x1, y1, 'F')
    # 牙（上向きの 白い 三角）
    if open_ == 0:
        for x in range(40, 61, 4): dots(g, 'w', [(x, 38)])
    else:
        x0, y0 = pts[0]; x1, y1 = pts[1]
        for i in range(2, 9):
            t = i / 9; x = round(x0 + (x1 - x0) * t); y = round(y0 + (y1 - y0) * t)
            dots(g, 'w', [(x, y - 1), (x, y - 2)]); dots(g, 'k', [(x - 1, y - 1), (x + 1, y - 1), (x, y - 3)])
    return g
def mouth(open_):
    """開いた 口の 中（赤）と 上の 牙"""
    pts = {1: [(33, 37), (62, 37), (60, 42), (34, 39)], 2: [(33, 37), (62, 37), (58, 49), (34, 41)]}[open_]
    p = G(); poly(p, pts, 'r')
    for y in range(64):
        for x in range(64):
            if p[y][x] == 'r' and (y > 38 + (x - 34) * .1 or x < 40): p[y][x] = 'm'
    g = ink(p)
    for x in range(44, 62, 4): stamp(g, ['w', 'w'] if open_ == 2 else ['w'], x, 38)
    return g

# ---------- 尾びれ：飛行船の 十字の 安定板 ----------
def tail():
    g = G()
    over(g, part(lambda p: poly(p, [(1, 12), (6, 13), (14, 24), (17, 28), (8, 28)], '1'), r=1))
    over(g, part(lambda p: poly(p, [(1, 46), (6, 45), (14, 34), (17, 31), (8, 31)], '4'), r=1))
    line(g, 4, 15, 12, 26, 'l'); line(g, 4, 43, 12, 33, 'l')
    return g
def tail_side():
    """手前の 横の 安定板"""
    return part(lambda p: poly(p, [(6, 29), (16, 28), (19, 31), (16, 33), (2, 35)], '1'), r=1)

# ---------- プロペラ（胸びれの かわり）----------
def prop(ph=0):
    g = G()
    over(g, part(lambda p: poly(p, [(30, 36), (37, 36), (35, 41), (31, 42)], '4'), r=1))   # びれの 根もと
    blades = {
        0: [[(32, 41), (30, 33), (32, 31), (34, 41)], [(32, 43), (31, 52), (33, 54), (34, 43)]],
        1: [[(32, 41), (25, 36), (24, 38), (31, 43)], [(33, 43), (39, 49), (40, 47), (34, 41)]],
        2: [[(31, 42), (23, 42), (23, 44), (31, 43)], [(34, 42), (41, 41), (41, 43), (34, 43)]],
    }[ph]
    for b in blades: over(g, part(lambda p: poly(p, b, '3'), r=1, hi=.1))
    over(g, part(lambda p: ellipse(p, 32.5, 42.5, 2.2, 2.2, '3'), r=1, hi=.2))
    dots(g, 'y', [(33, 43)])
    return g
# 回る 残像（雲の 色の 弧）
BLUR = ['..V..', '.V...', 'V....', '.....', 'V....', '.V...', '..V..']

# ---------- しぶき（潮吹き）と 雲 ----------
SPOUT0 = ['.W...W.', '..WVW..', '...V...', '...V...']
SPOUT1 = ['W.W.W.W', '.WVWVW.', '..WVW..', '...V...']
def cloud(ph=0):
    p = G()
    for (cx, cy, rx, ry) in ((10 + ph, 50, 6, 3.5), (18 + ph, 52, 6, 3.4), (25 + ph, 50, 4.5, 3), (4 + ph, 52, 3.6, 2.4)):
        ellipse(p, cx, cy, rx, ry, '5')
    s = shade(p, r=2, hi=.1, lo=-.15); g = G()
    for y in range(64):
        for x in range(64):
            if s[y][x] != '.': g[y][x] = s[y][x]
            elif any(at(s, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (0, 1))): g[y][x] = 'V'
    return g
BLAST = [
    '..........V..........',
    '....V..VWWWV...V.....',
    '..VWW.VWWWWWV.VWV..V.',
    '.VWWWVWWVVWWWVWWWV.W.',
    'VWWVWWWWV..VWWWVWWVWV',
    'WWVWWWW......WWWWVWW.',
    'VWWVWWWWV..VWWWVWWVWV',
    '.VWWWVWWVVWWWVWWWV.W.',
    '..VWW.VWWWWWV.VWV..V.',
    '....V..VWWWV...V.....',
    '..........V..........',
]

def layers():
    J0, J1, J2 = rows_of(jaw(0)), rows_of(jaw(1)), rows_of(jaw(2))
    P = [rows_of(prop(i)) for i in range(3)]
    HB = {e: rows_of(head_body(e)) for e in ('n', 'blink', 'atk', 'hit', 'ko')}
    return [
        dict(n='cloud', g='cloud', x=0, y=0, rows=rows_of(cloud(0)), alt={'idle2|idle3|walk2|walk3': rows_of(cloud(-1))}, not_='ko'),
        dict(n='tail', g='tail', x=0, y=0, rows=rows_of(tail())),
        dict(n='jaw', g='jaw', x=0, y=0, rows=J0, alt={'atk0|hit': J1, 'atk1': J2}),
        dict(n='mouth', g='jaw', x=0, y=0, rows=rows_of(mouth(1)), only='atk0|hit'),
        dict(n='mouth2', g='jaw', x=0, y=0, rows=rows_of(mouth(2)), only='atk1'),
        dict(n='body', g='body', x=0, y=0, rows=HB['n'], alt={'blink': HB['blink'], 'atk0|atk1|atk2': HB['atk'], 'hit': HB['hit'], 'ko': HB['ko']}),
        dict(n='teeth', g='body', x=0, y=0, rows=rows_of(teeth()), not_='atk0|atk1|hit|ko'),
        dict(n='tside', g='tail', x=0, y=0, rows=rows_of(tail_side())),
        dict(n='prop', g='prop', x=0, y=0, rows=P[0], alt={'idle1|idle3|walk1|walk3|atk1|hit': P[1], 'idle2|walk2|atk0|atk2': P[2]}),
        dict(n='blur', g='prop', x=25, y=36, rows=BLUR, only='idle1|idle3|walk1|walk3|atk1'),
        dict(n='spout', g='body', x=45, y=4, rows=SPOUT0, alt={'idle1|idle3|walk1|walk3': SPOUT1}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='blast', g='fx', x=61, y=37, rows=BLAST, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, -1)},
    'idle2': {'root': (0, -1), 'tail': (0, 1)},
    'idle3': {'root': (0, 0), 'tail': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1), 'tail': (0, 1)},
    'walk1': {'root': (1, -2)},
    'walk2': {'root': (0, -1), 'tail': (0, -1)},
    'walk3': {'root': (1, 0)},
    'atk0': {'root': (-3, -1), 'tail': (0, -1)},
    'atk1': {'root': (5, 0), 'tail': (1, 1)},
    'atk2': {'root': (6, 1)},
    'hit': {'root': (-3, -2), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'jaw': 'body', 'prop': 'body', 'tail': 'body', 'body': 'root', 'cloud': 'root', 'fx': 'root'}
