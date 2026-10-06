# デンシャコ（でんき・かくとう × シャコ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり → 左上光の 陰影 → 輪郭。仕上げは 手で 打つ）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def over(g, ch, pts, on):
    """on の 色の 上だけに 打つ"""
    for x, y in pts:
        if at(g, x, y) in on: g[y][x] = ch
def ink(g, p):
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(64) for x in range(64) if m[y][x]}
def shade(p, ramps, r=2, hi=.35, lo=-.3):
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
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
def ell(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
def part(draw, ramps, r=2, hi=.35, lo=-.3, post=None):
    p = G(); draw(p); s = shade(p, ramps, r, hi, lo)
    if post: post(s)
    g = G(); ink(g, s); return g
def R(g): return rows_of(g)
def L(n, g, rows, **kw): return dict(n=n, g=g, x=0, y=0, rows=rows, **kw)

META = dict(id='denshako', name='デンシャコ', types=['elec', 'fighting'], base='シャコ', size='M')
PAL = {
    'k': '#101018', 'l': '#16304a',
    'A': '#86dcea', 'B': '#3c90b0', 'D': '#1e4e72',      # 甲羅（青緑）
    'O': '#ffb048', 'P': '#d8602c', 'o': '#86301e',      # 脚・尾扇（だいだい）
    'Y': '#fff48a', 'y': '#f0b424', 'g': '#9a5a14',      # 電気の こぶし（金）
    'W': '#ffffff', 'C': '#7cf0ff',                      # 火花
    't': '#b4b4c8', 'r': '#c8203c',                      # テープ・口
}
LIGHT = set('AOYWCt')
KEEP_BLACK = set('WYCr')
SH = {'1': 'ABD'}; OR = {'2': 'OPo'}; CL = {'3': 'Yyg'}

def seg(s, cx, cy, px, py, n, a='D', b='A', on='ABD'):
    """甲羅の ふしの 区切り：暗い 線と その 前に 光の 線"""
    for i in range(-n, n + 1):
        x, y = round(cx + px * i), round(cy + py * i)
        if at(s, x, y) in on: s[y][x] = a
        if at(s, x + 1, y) in on and b and i < 0: s[y][x + 1] = b

# ---- 腹（地面に ねる 節の 胴）と 尾扇 ----
def abd_g():
    def d(p):
        tube(p, [(17, 53), (23, 54), (29, 52), (33, 49)], [4.4, 5.4, 6, 6.4])
    def post(s):
        for cx in (20, 25, 30): seg(s, cx, 53, 0, 1, 7)
        over(s, 'y', [(22, 48), (23, 47), (27, 47), (28, 46), (32, 44)], 'AB')
        for y in range(58, 60):
            for x in range(64):
                if s[y][x] in 'AB': s[y][x] = 'D'
    return part(d, SH, r=2, post=post)
def tail_g():
    def d(p):
        tube(p, [(17, 51), (8, 45)], [3.2, 1], '2')
        tube(p, [(16, 53), (6, 52)], [3.4, 1], '2')
        tube(p, [(17, 55), (9, 60)], [3, 1], '2')
    def post(s):
        for (x0, y0, x1, y1) in ((15, 51, 10, 47), (14, 53, 8, 52)):
            g2 = G(); line(g2, x0, y0, x1, y1, 'o')
            for y in range(64):
                for x in range(64):
                    if g2[y][x] == 'o' and s[y][x] in 'OP': s[y][x] = 'o'
    return part(d, OR, r=1, post=post)
# ---- 胸（起きあがる）＋ 頭の 甲羅 ----
def thorax_g():
    def d(p):
        tube(p, [(32, 50), (37, 42), (41, 33)], [6.4, 6.6, 6])
    def post(s):
        for t in (0.35, 0.7):
            cx, cy = 32 + 9 * t, 50 - 17 * t
            seg(s, cx, cy, .87, .48, 7)
    return part(d, SH, r=2, hi=.5, post=post)
def head_g():
    def d(p):
        poly(p, [(35, 31), (39, 24), (46, 20), (53, 21), (58, 24), (62, 26), (57, 28), (52, 31), (44, 34), (37, 35)], '1')
    def post(s):
        # 甲羅の ふちの 線と 光の 三日月（手で）
        for x in range(38, 57):
            y = 33 - (x - 38) * 0.28
            if at(s, x, round(y)) in 'ABD': s[round(y)][x] = 'D'
        over(s, 'A', [(41, 24), (42, 23), (43, 23), (44, 22), (45, 22), (46, 21), (47, 21), (48, 21), (38, 27), (39, 26), (40, 25)], 'BD')
        over(s, 'l', [(50, 25), (51, 25), (52, 26), (53, 26), (54, 26)], 'ABD')
    g = part(d, SH, r=2, post=post)
    # 口の きば（下向き）
    dots(g, 'k', [(50, 30), (51, 31), (52, 30), (53, 31), (54, 30), (49, 31), (55, 30)])
    dots(g, 'W', [(50, 31), (53, 32), (54, 31)]); dots(g, 'k', [(50, 32), (53, 33), (54, 32), (49, 32), (51, 32), (52, 33), (55, 31)])
    return g
# ---- 目（太く 短い 柄の 先の 複眼。上まぶたが 前へ 下がる つり目、たての ひとみ）----
def stalks_g():
    def d(p):
        tube(p, [(43, 24), (40, 18)], [2, 1.6])
        tube(p, [(49, 23), (51, 17)], [2.2, 1.8])
    return part(d, SH, r=1)
EYE_B = [
    '.kkkkk.',
    'kAABBDk',
    'kBkkkkk',
    'kYYkkkk',
    'kYkYYyk',
    'kykYyyk',
    '.kkkkk.',
]
EYE_F = [
    '..kkkkkk.',
    '.kAAABBDk',
    'kABBBkkkk',
    'kYYYkkkkk',
    'kWYYkYYyk',
    'kYYYkYyyk',
    'kyyykyygk',
    '.kkkkkkk.',
]
def _e(rows, *sub):
    rows = list(rows)
    for i, r in sub: rows[i] = r
    return rows
EYE_F_ALT = {
    'blink': _e(EYE_F, (3, 'kBBBkkkkk'), (4, 'kBBBBBBkk'), (5, 'kkkkkkkkk'), (6, 'kBBBBBBDk')),
    'atk0|atk1|atk2': _e(EYE_F, (3, 'kWWWkkkkk'), (4, 'kWWWkWWYk'), (5, 'kWWWkWYYk'), (6, 'kYYYkYYyk')),
    'hit': _e(EYE_F, (3, 'kBBkkkkBk'), (4, 'kBBBkkkBk'), (5, 'kBkkkBBBk'), (6, 'kkBBBBBDk')),
    'ko': _e(EYE_F, (3, 'kBkBBBkBk'), (4, 'kBBkBkBBk'), (5, 'kBBBkBBBk'), (6, 'kBBkBkBDk')),
}
EYE_B_ALT = {
    'blink': _e(EYE_B, (3, 'kBBkkkk'), (4, 'kkkkkkk'), (5, 'kBBBBDk')),
    'atk0|atk1|atk2': _e(EYE_B, (3, 'kWWkkkk'), (4, 'kWkWWYk'), (5, 'kYkWYyk')),
    'hit': _e(EYE_B, (3, 'kBkkkBk'), (4, 'kBBkBBk'), (5, 'kkBBBDk')),
    'ko': _e(EYE_B, (3, 'kBkBkBk'), (4, 'kBBkBBk'), (5, 'kBkBkBk')),
}
# 触角の うろこ（だいだいの 小旗）と むち
def ant_g():
    def d(p):
        poly(p, [(54, 23), (57, 17), (60, 14), (60, 19), (57, 24)], '2')
    g = part(d, OR, r=1)
    line(g, 52, 21, 56, 10, 'k'); dots(g, 'k', [(57, 9), (58, 9)])
    return g
# ---- 見せ所：電気の こぶし（捕脚の こぶ ⇔ ボクシングの こぶし）----
def arm_g(cx=52, cy=40, r=9.6, mx=(40, 34)):
    ix, iy = round(cx), round(cy)
    wx = ix - 9
    def d(p):
        tube(p, [mx, (wx - 1, iy + 1)], [2.6, 3], '1')
    a = part(d, SH, r=1)
    def dc(p):
        ellipse(p, cx, cy, r, r * .93, '3')
        # 指の あいだの くぼみ（右の ふちを 1ドット けずる）
        for yy in (-3, 2):
            for x in range(64):
                if p[iy + yy][63 - x] == '3': p[iy + yy][63 - x] = '.'; break
    c = part(dc, CL, r=3, hi=.3, lo=-.25)
    # 指の みぞ（右から 左へ）と 指の 上の 光
    for yy in (-3, 2):
        xs = [x for x in range(64) if c[iy + yy][x] in 'Yyg']
        for x in xs[-6:]: c[iy + yy][x] = 'g'
        for x in xs[-5:-1]:
            if at(c, x, iy + yy + 1) in 'yg': c[iy + yy + 1][x] = 'Y' if x < ix + 4 else 'y'
    # 親指（下を 横切る）
    for (x, y) in ((ix - 3, iy + 6), (ix - 2, iy + 5), (ix - 1, iy + 5), (ix, iy + 5), (ix + 1, iy + 5), (ix + 2, iy + 6)):
        if at(c, x, y) in 'Yyg': c[y][x] = 'g'
        if at(c, x, y - 1) in 'yg': c[y - 1][x] = 'Y'
    # 電気の すじ（ジグザグ）
    over(c, 'W', [(ix - 5, iy - 5), (ix - 4, iy - 6), (ix - 3, iy - 5), (ix - 2, iy - 6), (ix - 6, iy - 3), (ix - 6, iy - 2), (ix - 5, iy - 1)], 'Yy')
    # 手首の テープ（かくとう）
    def dt(p):
        for y in range(iy - 5, iy + 6):
            for x in range(wx - 1, wx + 3): p[y][x] = '4'
    t = part(dt, {'4': 'Wtt'}, r=1)
    for y in range(iy - 5, iy + 6, 3):
        for x in range(wx - 1, wx + 3):
            if t[y][x] in 'Wt': t[y][x] = 'l'
    g = G(); stamp(g, R(a), 0, 0); stamp(g, R(c), 0, 0); stamp(g, R(t), 0, 0)
    return g
def bolt(paths, w=0):
    """稲妻：W の しん＋C の ふち＋黒の 輪郭"""
    p = G()
    for pts in paths:
        for i in range(len(pts) - 1): line(p, *pts[i], *pts[i + 1], 'W')
    if w:
        q = [r[:] for r in p]
        for y in range(64):
            for x in range(64):
                if p[y][x] == '.' and any(at(p, x + dx, y + dy) == 'W' for dx, dy in ((1, 0), (0, 1))): q[y][x] = 'C'
        p = q
    g = G(); ink(g, p); return R(g)
SPARK1 = bolt([[(0, 4), (2, 2), (3, 4), (5, 0)], [(2, 7), (5, 6), (6, 9)]])
SPARK2 = bolt([[(0, 1), (3, 2), (4, 0), (6, 2)], [(1, 6), (3, 5), (4, 8), (6, 7)]])
BOLT = bolt([[(0, 6), (4, 3), (6, 7), (10, 2), (12, 6), (16, 0)], [(0, 8), (5, 10), (8, 8), (11, 13), (15, 11)], [(1, 4), (3, 0)]], 1)
BOLT2 = bolt([[(0, 4), (3, 2), (5, 5), (8, 1)], [(1, 7), (4, 9), (7, 8)]], 1)
CHG = bolt([[(0, 0), (2, 3), (1, 5), (3, 8)], [(9, 0), (8, 3), (10, 5)], [(4, 12), (6, 14), (9, 13)]], 1)
# 脚（だいだい、細く 3本 → 2本に まとめる）
def leg_g(x0, y0, x1, y1):
    def d(p): tube(p, [(x0, y0), ((x0 + x1) / 2 + 1, (y0 + y1) / 2), (x1, y1)], [1.6, 1.4, 1.1], '2')
    return part(d, OR, r=1)

# ---- ダウン：横だおれ（脚が 上を 向く）----
def ko_g():
    def d(p):
        tube(p, [(11, 56), (19, 57), (28, 56), (37, 54)], [4.2, 5, 5.6, 5.8])
        poly(p, [(35, 49), (42, 48), (49, 50), (53, 54), (48, 57), (39, 58), (35, 58)], '1')
    def post(s):
        for cx in (16, 22, 28, 33): seg(s, cx, 56, 0, 1, 7)
    b = part(d, SH, r=2, hi=.5, post=post)
    def dt(p):
        tube(p, [(11, 54), (2, 50)], [3, 1], '2'); tube(p, [(10, 57), (1, 58)], [3, 1], '2')
        for (x0, x1) in ((22, 25), (27, 31), (31, 37)): tube(p, [(x0, 51), (x1 - 1, 46), (x1 + 1, 44)], [1.5, 1.2, 1], '2')
    t = part(dt, OR, r=1)
    def ds(p): tube(p, [(45, 50), (50, 45)], [1.8, 1.6]); tube(p, [(40, 49), (41, 45)], [1.6, 1.4])
    st = part(ds, SH, r=1)
    c = arm_g(cx=56, cy=55, r=5.6, mx=(47, 57))
    g = G()
    for q in (t, b, st, c): stamp(g, R(q), 0, 0)
    stamp(g, ['.kkkkkk.', 'kBBBBBDk', 'kykyykyk', 'kyykkyyk', 'kykyykyk', '.kkkkkk.'], 47, 40)
    return R(g)
def layers():
    ARM = R(arm_g()); ARM_BACK = R(arm_g(cx=47, cy=45, mx=(37, 36))); ARM_PUNCH = R(arm_g(cx=57, cy=36, mx=(41, 32)))
    ARM2 = R(arm_g(cx=55, cy=39, mx=(41, 33)))
    return [
        L('legB2', 'legB', R(leg_g(29, 53, 30, 60)), not_='ko'),
        L('tail', 'tail', R(tail_g()), not_='ko'),
        L('abd', 'abd', R(abd_g()), not_='ko'),
        L('legA', 'legA', R(leg_g(36, 51, 39, 60)), not_='ko'),
        L('thorax', 'body', R(thorax_g()), not_='ko'),
        L('legB', 'legB', R(leg_g(33, 54, 34, 60)), not_='ko'),
        L('stalks', 'head', R(stalks_g()), not_='ko'),
        dict(n='eyeB', g='head', x=35, y=12, rows=EYE_B, alt=EYE_B_ALT, not_='ko'),
        L('ant', 'head', R(ant_g()), not_='ko'),
        L('headc', 'head', R(head_g()), not_='ko'),
        dict(n='eyeF', g='head', x=47, y=10, rows=EYE_F, alt=EYE_F_ALT, not_='ko'),
        L('ko', 'root', ko_g(), only='ko'),
        L('arm', 'arm', ARM, alt={'atk0': ARM_BACK, 'atk1': ARM_PUNCH, 'atk2': ARM2}, not_='ko'),
        dict(n='spk', g='arm', x=55, y=26, rows=SPARK1, alt={'idle1|idle3|walk1|walk3': SPARK2}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='spk0', g='arm', x=38, y=34, rows=CHG, only='atk0'),
        dict(n='bolt', g='arm', x=64, y=31, rows=BOLT, only='atk1'),
        dict(n='bolt2', g='arm', x=63, y=34, rows=BOLT2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, -1)}, 'idle3': {'arm': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'tail': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'tail': (0, -1)},
    'atk0': {'body': (-1, 1), 'tail': (0, -1)}, 'atk1': {'root': (4, 0)}, 'atk2': {'root': (3, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 1), 'arm': (-1, 1)},
    'ko': {},
}
PARENT = {'head': 'body', 'arm': 'body', 'body': 'root', 'abd': 'root', 'tail': 'root', 'legA': 'root', 'legB': 'root'}
