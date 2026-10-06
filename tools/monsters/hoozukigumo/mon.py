# ホオズキグモ（フェアリー・ゴースト × クモ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline, recolor

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


META = dict(id='hoozukigumo', name='ホオズキグモ', types=['fairy', 'ghost'], base='クモ', size='S')
PAL = {
    'k': '#101018', 'l': '#3a1a24',
    'A': '#ffc060', 'B': '#ec6c24', 'C': '#9a3018',      # ホオズキの 袋（紙の ような だいだい）
    'D': '#8a78a8', 'E': '#4c3e6a', 'F': '#261e3a',      # クモの 体（黒むらさき）
    'w': '#ffffff', 'c': '#9af0ff', 'b': '#3486c8',      # 霊火
    'r': '#ff2848', 'y': '#ffe070',                      # 目の 光
}
LIGHT = set('ADwcy')
KEEP_BLACK = set('wcbry')
RAMP = {'3': 'ABC', '1': 'DEF'}

# ---------- 腹：ホオズキの 袋（ちょうちん形）。すじが 先へ あつまり、網目の 窓から 霊火 ----------
TOP, TIP = (29, 21), (6, 41)
def lantern(glow=1):
    p = G()
    ell(p, 18, 28, 12, 11, '3')
    poly(p, [(10, 32), (5, 42), (15, 38)], '3')
    s = shade(p, RAMP, r=3, hi=.25, lo=-.22)
    # 袋の すじ（つけ根から 先へ 弧を えがく）
    for k in (-13, -6, 1, 8):
        mx, my = (TOP[0] + TIP[0]) / 2 - k * .55, (TOP[1] + TIP[1]) / 2 - k * .8
        for i in range(41):
            t = i / 40; x = (1 - t) ** 2 * TOP[0] + 2 * (1 - t) * t * mx + t * t * TIP[0]; y = (1 - t) ** 2 * TOP[1] + 2 * (1 - t) * t * my + t * t * TIP[1]
            X, Y = int(x), int(y)
            if s[Y][X] != '.':
                s[Y][X] = 'C'
                if s[Y][X - 1] in 'B' and k < 5: s[Y][X - 1] = 'A'
    # 網目の 窓（ホオズキの すけた 葉脈）＋ 中で 燃える 霊火
    WIN = [
        '...kkkkk...',
        '..kbbcbbkk.',
        '.kbccwcbbbk',
        'kbcwwwwcbbk',
        'kbcwwwwcbCk',
        'kbbcwwcbbCk',
        '.kbbccbbCk.',
        '..kCbbbCk..',
        '...kkkkk...',
    ]
    if glow == 2: WIN = [r.replace('b', 'c') for r in WIN]
    if glow == 0: WIN = [r.replace('w', 'c').replace('c', 'b') for r in WIN]
    put(s, WIN, 13, 27)
    for y in range(27, 36):           # 網の すじ
        for x in range(13, 24):
            if s[y][x] in 'bcw' and ((x + y) % 4 == 0 or (x - y) % 4 == 0): s[y][x] = 'C' if s[y][x] == 'b' else 'B' if s[y][x] == 'c' else s[y][x]
    return rows_of(ink(s))
# ---------- 脚：上へ 折れて から 地面へ（ひざが 高い）----------
def leg(pts, rad, dark=False):
    p = G(); tube(p, pts, rad, '1'); s = shade(p, RAMP, r=1, hi=.2, lo=-.2)
    if dark: s = swap(s, {'D': 'E', 'E': 'F'})
    # 先は するどい 爪
    x, y = int(pts[-1][0]), int(pts[-1][1]); s[y][x] = 'F'
    # ひざの ふし
    kx, ky = int(pts[1][0]), int(pts[1][1])
    if s[ky][kx] != '.': s[ky][kx] = 'C'
    return rows_of(ink(s))
LEGS = {   # 名前: (点, 太さ, 奥か, グループ)
    'f1': ([(36, 36), (42, 27), (47, 47)], [1.6, 1.4, .6], True, 'legB'),
    'f2': ([(32, 37), (34, 28), (37, 48)], [1.6, 1.4, .6], True, 'legA'),
    'n4': ([(29, 40), (21, 39), (14, 50)], [1.9, 1.6, .7], False, 'legB'),
    'n3': ([(31, 40), (27, 33), (25, 51)], [1.9, 1.6, .7], False, 'legA'),
    'n2': ([(34, 40), (39, 31), (42, 51)], [1.9, 1.6, .7], False, 'legB'),
    'n1': ([(37, 39), (46, 30), (52, 50)], [1.9, 1.7, .7], False, 'legA'),
}
RAISE = {'n1': [(37, 38), (45, 26), (53, 31)], 'n2': [(34, 39), (40, 28), (46, 36)]}
def thorax():
    p = G(); ell(p, 35, 37, 7, 5.5, '1'); ell(p, 41, 35, 4.5, 4, '1')
    s = shade(p, RAMP, r=2)
    return ink(s)
def head(eyes='norm'):
    g = thorax()
    # 4つの 赤い 目：まゆの ひさしの 下で つり上がる
    put(g, ['kkk....', '.Fkkk..', '.rrFkk.', '..rrrk.', '....F..'], 38, 31)
    if eyes == 'blink': put(g, ['kkk....', '.Fkkk..', '.kkFkk.', '..kkkk.', '....F..'], 38, 31)
    if eyes == 'glow': put(g, ['kkk....', '.ykkk..', '.yyrkk.', '..ryyk.', '....F..'], 38, 31)
    if eyes == 'hit': put(g, ['.......', '.kFkF..', '.FkFkF.', '..kFkF.', '....F..'], 38, 31)
    if eyes == 'ko': put(g, ['.......', '.kEk.k.', '.EkEEkE', '.kEk.kE', '.......'], 38, 31)
    # 牙（白い 大あご）
    put(g, ['kkk..', 'kwwk.', '.kwwk', '..kwk', '...k.'], 42, 38) if eyes != 'ko' else None
    return rows_of(g)
FANG_OPEN = ['kkk...', 'kwwkk.', '.kwwwk', '..kkwk', '..kwk.', '..kk..']
STEM = ['.kk..', 'kCBk.', 'kBDEk', '.kEEk', '..kk.']
WISP = ['..c.', '.cc.', 'cwc.', 'cwwc', '.cc.']
WISP2 = ['.c..', '.cc.', '.cwc', 'cwwc', '.cc.']
BALL = [
    '......cc....',
    '..c.ccwc....',
    '.cccwwwwcc..',
    'ccwwwwwwwcc.',
    '.cbwwwwwwwcc',
    'cbcwwwwwwcc.',
    '.bbccwwccb..',
    '..b.bccb....',
]
BALL2 = ['....c.c.....', '.c.ccwcc.c..', 'ccwwwwwwccc.', '.cbcwwwcbc..', '..b.bccb.b..']

def layers():
    L = []
    for n in ('f1', 'f2'):
        pts, rad, dark, gg = LEGS[n]; L.append(dict(n=n, g=gg, x=0, y=0, rows=leg(pts, rad, True)))
    L += [
        dict(n='wisp', g='wisp', x=6, y=12, rows=WISP, alt={'idle1|idle3|walk1|walk3': WISP2}, not_='ko'),
        dict(n='lantern', g='abd', x=0, y=0, rows=lantern(), alt={'idle1|idle3|atk0|atk1': lantern(2), 'ko': lantern(0)}),
        dict(n='stem', g='abd', x=27, y=18, rows=STEM),
    ]
    for n in ('n4', 'n3'):
        pts, rad, dark, gg = LEGS[n]; L.append(dict(n=n, g=gg, x=0, y=0, rows=leg(pts, rad)))
    L.append(dict(n='head', g='body', x=0, y=0, rows=head(), alt={'blink': head('blink'), 'atk0|atk1|atk2': head('glow'), 'hit': head('hit'), 'ko': head('ko')}))
    for n in ('n2', 'n1'):
        pts, rad, dark, gg = LEGS[n]
        L.append(dict(n=n, g=gg, x=0, y=0, rows=leg(pts, rad), alt={'atk0|atk1': leg(RAISE[n], rad)}))
    L += [
        dict(n='fang', g='body', x=42, y=38, rows=FANG_OPEN, only='atk1|atk2'),
        dict(n='ball', g='root', x=50, y=28, rows=BALL, only='atk1'),
        dict(n='ball2', g='root', x=56, y=30, rows=BALL2, only='atk2'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'abd': (0, 1)}, 'idle2': {'body': (0, 1), 'abd': (0, 2), 'wisp': (0, -1)}, 'idle3': {'body': (0, 0), 'abd': (0, 1), 'wisp': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'body': (0, -1)}, 'walk1': {'abd': (0, 1)}, 'walk2': {'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'abd': (0, 1)},
    'atk0': {'body': (-2, -2), 'abd': (-1, -1), 'legA': (-1, 0), 'legB': (-1, 0)}, 'atk1': {'root': (3, 0), 'body': (1, 0)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 1), 'abd': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'abd': 'root', 'wisp': 'abd', 'body': 'root', 'legA': 'root', 'legB': 'root'}
