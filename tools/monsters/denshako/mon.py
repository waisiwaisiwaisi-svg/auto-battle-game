# デンシャコ（でんき・かくとう × シャコ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp

# ---------- 下書きの 道具（あたりを とり、陰影は 光の 向きで 決めて から 手で 直す）----------
W = H = 64
def G(): return grid(W, H)
def at(g, x, y): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < H and 0 <= x < W: g[y][x] = ch
def ell(p, cx, cy, rx, ry, ch, only=None):
    for y in range(H):
        for x in range(W):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1 and (only is None or p[y][x] in only): p[y][x] = ch
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < W and 0 <= y < H and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(W)] for y in range(H)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < H and 0 <= xx < W else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(H) for x in range(W) if m[y][x]}
def shade(p, ramps, r=2, hi=.35, lo=-.3):
    """左上から 光：ramps = {下書きの 文字: '明中暗'}"""
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def ink(p, ch='k'):
    """1ドットの 黒い 輪郭で かこむ"""
    g = G()
    for y in range(H):
        for x in range(W):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = ch
            elif p[y][x] != '.': g[y][x] = p[y][x]
    return g
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g
def swap(g, mp, box=None):
    x0, y0, x1, y1 = box or (0, 0, W, H)
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            if g[y][x] in mp: g[y][x] = mp[g[y][x]]
    return g
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < W and 0 <= y + dy < H: g[y + dy][x + dx] = c
    return rows_of(g)


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
        tube(p, [(14, 53), (21, 54), (28, 52), (33, 49)], [4.2, 5.2, 5.8, 6.2])
    def post(s):
        for cx in (17, 22, 27): seg(s, cx, 53, 0, 1, 7)
        for y in range(58, 60):
            for x in range(64):
                if s[y][x] in 'AB': s[y][x] = 'D'
    return part(d, SH, r=2, post=post)
def tail_g():
    def d(p):
        tube(p, [(14, 51), (3, 44)], [3.2, 1], '2')
        tube(p, [(13, 53), (1, 52)], [3.4, 1], '2')
        tube(p, [(14, 55), (4, 60)], [3, 1], '2')
    def post(s):
        for (x0, y0, x1, y1) in ((12, 51, 5, 46), (11, 53, 3, 52)):
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
    return part(d, SH, r=2, post=post)
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
# ---- 目（柄の 先の 複眼。まんなかの 帯＝横の ひとみ、ひさしで つり目）----
def stalks_g():
    def d(p):
        tube(p, [(45, 22), (43, 14)], [1.6, 1.4])
        tube(p, [(49, 22), (50, 14)], [1.8, 1.6])
    return part(d, SH, r=1)
EYE_B = ['.kkkk.', 'kAkkkk', 'kkyyYk', 'kkkkkk', '.kkkk.']
EYE_F = ['.kkkkk.', 'kAAkkkk', 'kBkkYYk', 'kkyYYYk', 'kkkkkkk', '.kkkkk.']
EYE_F_ALT = {
    'blink': ['.kkkkk.', 'kAAkkkk', 'kBBBkkk', 'kkkkkkk', 'kBBBBBk', '.kkkkk.'],
    'atk0|atk1|atk2': ['.kkkkk.', 'kAAkkkk', 'kBkWWWk', 'kkWWWWk', 'kkkkkkk', '.kkkkk.'],
    'hit': ['.kkkkk.', 'kAAkkkk', 'kBkkkBk', 'kkBBkkk', 'kkkkkkk', '.kkkkk.'],
    'ko': ['.kkkkk.', 'kAkBkAk', 'kBBkBBk', 'kAkBkAk', 'kkkkkkk', '.kkkkk.'],
}
EYE_B_ALT = {
    'blink': ['.kkkk.', 'kAkkkk', 'kBBBBk', 'kkkkkk', '.kkkk.'],
    'atk0|atk1|atk2': ['.kkkk.', 'kAkkkk', 'kkWWWk', 'kkkkkk', '.kkkk.'],
    'hit': ['.kkkk.', 'kAkkkk', 'kkBkBk', 'kkkkkk', '.kkkk.'],
    'ko': ['.kkkk.', 'kkBkBk', 'kBkBkk', 'kkBkBk', '.kkkk.'],
}
# 触角の うろこ（だいだいの 小旗）と むち
def ant_g():
    def d(p):
        poly(p, [(54, 22), (58, 16), (61, 14), (60, 18), (56, 23)], '2')
    g = part(d, OR, r=1)
    line(g, 52, 20, 58, 9, 'k'); dots(g, 'k', [(59, 8), (60, 8)])
    return g
# ---- 見せ所：電気の こぶし（捕脚の こぶ ⇔ ボクシングの こぶし）----
def arm_g(cx=52, cy=41, r=8.2, mx=(41, 34), punch=False):
    def d(p):
        tube(p, [mx, (cx - r + 2, cy + 1)], [2.6, 2.8], '1')
    a = part(d, SH, r=1)
    def dc(p):
        ellipse(p, cx, cy, r, r * .95, '3')
    c = part(dc, CL, r=3, hi=.3, lo=-.25)
    def club_post(c):
        # こぶしの 指の 段（右がわに 3本の しわ）
        for i, yy in enumerate((-3, 0, 3)):
            for j in range(3):
                x, y = round(cx + r * .45 + j), round(cy + yy - j * .3)
                if at(c, x, y) in 'Yyg': c[y][x] = 'g'
        # 電気の すじ（手で：ジグザグ）
        over(c, 'W', [(round(cx - 4), round(cy - 4)), (round(cx - 3), round(cy - 5)), (round(cx - 2), round(cy - 4)), (round(cx - 1), round(cy - 5)), (round(cx - 5), round(cy - 2)), (round(cx - 5), round(cy - 1))], 'Yy')
        # 手首の テープ（かくとう）
        wx = round(cx - r + 1)
        for y in range(round(cy - 4), round(cy + 5)):
            for x in (wx, wx + 1):
                if at(c, x, y) in 'Yyg': c[y][x] = 't' if (y + x) % 3 else 'W'
    club_post(c)
    g = G(); stamp(g, R(a), 0, 0); stamp(g, R(c), 0, 0)
    return g
SPARK1 = ['..W....', '.WC..C.', 'C..W.W.', '...C...']
SPARK2 = ['.C...W.', 'W.W.C..', '..C..WC', '.W.....']
BOLT = [
    '.......W.....C.',
    '..C...WC...W...',
    'W..WWWCW..WCW..',
    '.WWCCWWWWWCCWWC',
    'C..WWCWWCWWW..W',
    '..W..WCW..CW.C.',
    '.C...W.C....W..',
    '.....C......C..',
]
# 脚（だいだい、細く 3本 → 2本に まとめる）
def leg_g(x0, y0, x1, y1):
    def d(p): tube(p, [(x0, y0), ((x0 + x1) / 2 + 1, (y0 + y1) / 2), (x1, y1)], [1.6, 1.4, 1.1], '2')
    return part(d, OR, r=1)

def layers():
    ARM = R(arm_g()); ARM_BACK = R(arm_g(cx=46, cy=30, mx=(40, 33))); ARM_PUNCH = R(arm_g(cx=56, cy=36, mx=(42, 33)))
    ARM2 = R(arm_g(cx=55, cy=38, mx=(42, 33)))
    return [
        L('legB2', 'legB', R(leg_g(29, 53, 30, 60))),
        L('tail', 'tail', R(tail_g())),
        L('abd', 'abd', R(abd_g())),
        L('legA', 'legA', R(leg_g(36, 51, 39, 60))),
        L('thorax', 'body', R(thorax_g())),
        L('legB', 'legB', R(leg_g(33, 54, 34, 60))),
        L('stalks', 'head', R(stalks_g())),
        dict(n='eyeB', g='head', x=40, y=9, rows=EYE_B, alt=EYE_B_ALT),
        L('ant', 'head', R(ant_g())),
        L('headc', 'head', R(head_g())),
        dict(n='eyeF', g='head', x=47, y=9, rows=EYE_F, alt=EYE_F_ALT),
        L('arm', 'arm', ARM, alt={'atk0': ARM_BACK, 'atk1': ARM_PUNCH, 'atk2': ARM2}),
        dict(n='spk', g='arm', x=56, y=31, rows=SPARK1, alt={'idle1|idle3|walk1|walk3': SPARK2}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='spk0', g='arm', x=44, y=19, rows=SPARK2, only='atk0'),
        dict(n='bolt', g='arm', x=63, y=31, rows=BOLT, only='atk1'),
        dict(n='bolt2', g='arm', x=62, y=33, rows=SPARK1, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, -1)}, 'idle3': {'arm': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'tail': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'tail': (0, -1)},
    'atk0': {'body': (-1, 1), 'tail': (0, -1)}, 'atk1': {'root': (3, 0)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 1), 'arm': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'arm': 'body', 'body': 'root', 'abd': 'root', 'tail': 'root', 'legA': 'root', 'legB': 'root'}
