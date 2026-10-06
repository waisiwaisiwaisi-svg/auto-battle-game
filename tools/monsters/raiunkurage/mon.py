# ライウンクラゲ（でんき・ひこう(かぜ) × クラゲ）手打ち GBA風
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

META = dict(id='raiunkurage', name='ライウンクラゲ', types=['elec', 'wind'], base='クラゲ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c3050',
    'A': '#f6f8ff', 'B': '#bcc4dc', 'D': '#767ea0', 'E': '#40466a',   # 雲（白 → 嵐の 灰）
    'Y': '#fff480', 'y': '#f2b424', 'o': '#a8601a',                    # 稲妻の 触手
    'C': '#8af2ff', 'c': '#3c9ad0',                                    # 雲の 中の 放電
    'w': '#ffffff', 'm': '#b81c40',
}
LIGHT = set('AYCw')
KEEP_BLACK = set('wYCm')

# ---- 見せ所：積乱雲の かさ（もこもこの 半球 ⇔ クラゲの かさ）----
PUFFS = [  # 奥 → 手前（cx, cy, r）
    (31, 11, 10), (21, 15, 9), (42, 13, 9), (13, 22, 7), (50, 21, 7.5), (26, 22, 9), (39, 22, 9),
]
def bell_g(PF=PUFFS, base=31, squash=1.0, flash=False):
    p = G(); own = {}
    for i, (cx, cy, r) in enumerate(PF):
        for y in range(64):
            for x in range(64):
                if ((x + .5 - cx) ** 2 + ((y + .5 - cy) / squash) ** 2) <= r * r and y < base:
                    own[(x, y)] = i; p[y][x] = '1'
    for (x, y), i in own.items():
        cx, cy, r = PF[i]
        v = -(x + .5 - cx) / r * .55 - (y + .5 - cy) / (r * squash) * .85
        p[y][x] = 'A' if v > .45 else 'B' if v > -.15 else 'D'
        # 下の 帯は 嵐の 底（暗い）
        if y >= base - 5: p[y][x] = 'E' if y >= base - 3 else ('D' if p[y][x] != 'A' else 'B')
    # もこもこの さかいめ：手前の 玉の ふちに 暗い 線
    for (x, y), i in own.items():
        for dx, dy in ((-1, 0), (0, -1), (1, 0)):
            j = own.get((x + dx, y + dy))
            if j is not None and j < i and p[y][x] in 'AB' and ((x + dx + .5 - PF[i][0]) ** 2 + ((y + dy + .5 - PF[i][1]) / squash) ** 2) > PF[i][2] ** 2:
                p[y + dy][x + dx] = 'D' if p[y + dy][x + dx] != 'E' else 'E'
    if flash:  # 雲の 中で 光る 放電
        for (x, y) in ((22, 14), (23, 15), (22, 16), (23, 17), (33, 9), (34, 10), (33, 11), (34, 12), (35, 13), (16, 21), (17, 22)):
            if p[y][x] != '.': p[y][x] = 'C'
    g = G(); ink(g, p); return g
# 顔：底の 前がわ。つり目（光る）＋ ぎざぎざの きばの 口
EYES = [
    'kk.......kk..',
    'kYkk...kkYYk.',
    '.kwYk..kYYwk.',
    '..kkk...kkk..',
]
EYES_ALT = {
    'blink': ['kk.......kk..', 'kkkk...kkkkk.', '.kkkk..kkkkk.', '.............'],
    'atk0|atk1|atk2': ['kk.......kk..', 'kwkk...kkwwk.', '.kwwk..kwwwk.', '..kkk...kkk..'],
    'hit': ['.k.k.....k.k.', '..k.......k..', '.k.k.....k.k.', '.............'],
    'ko': ['k.k......k.k.', '.k........k..', 'k.k......k.k.', '.............'],
}
MOUTH = ['kkkkkkkkkk', 'kwkwkwkwkk', '.kmmmmmmk.', '..kkkkkk..']
MOUTH_OPEN = ['kkkkkkkkkkk', 'kwkwkwkwkwk', 'kmmmmmmmmmk', 'kmmmmmmmmmk', 'kwkwkwkwkwk', '.kkkkkkkkk.']
MOUTH_SHUT = ['kkkkkkkkkk', '.kkkkkkkk.']
# ---- 稲妻の 触手（ジグザグ）----
def zig(x0, y0, n, step=4, amp=3, flip=1):
    pts = [(x0, y0)]
    for i in range(n):
        x0 += amp * flip * (1 if i % 2 == 0 else -1) + (1 if i % 2 == 0 else 0); y0 += step
        pts.append((x0, y0))
    return pts
def tent_g(sw=0, limp=False):
    p = G()
    specs = [(17, 29, 6, 1, 1.6), (26, 30, 7, -1, 1.9), (36, 30, 7, 1, 1.9), (46, 28, 6, -1, 1.6)]
    for i, (x, y, n, f, w) in enumerate(specs):
        if limp:
            pts = [(x, y)] + [(x + (j + 1) * 3 * (1 if i > 1 else -1), min(57, y + 6 + j * 2) if j < 2 else 57) for j in range(4)]
        else:
            pts = zig(x + (sw if i % 2 else -sw), y, n, step=4 if n == 7 else 4, amp=2.6, flip=f * (1 if sw >= 0 else -1))
        tube(p, pts, [w] * (len(pts) - 1) + [.8], '2')
    s = shade(p, {'2': 'Yyo'}, r=1, hi=.2, lo=-.3)
    g = G(); ink(g, s); return g
def fx_g(paths):
    p = G()
    for pts in paths:
        for i in range(len(pts) - 1): line(p, *pts[i], *pts[i + 1], 'w')
    q = [r[:] for r in p]
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) == 'w' for dx, dy in ((1, 0), (0, 1), (-1, 0))): q[y][x] = 'C'
    g = G(); ink(g, q); return R(g)
STRIKE = fx_g([[(52, 30), (56, 36), (54, 38), (59, 46), (57, 48), (63, 58)], [(56, 36), (61, 38)], [(59, 46), (63, 45)]])
STRIKE2 = fx_g([[(55, 44), (58, 48), (57, 50), (61, 57)]])
CHARGE = fx_g([[(4, 10), (6, 13), (5, 15)], [(56, 6), (58, 9), (57, 11)], [(30, -1), (31, 1)]])
# ---- ダウン：しぼんだ 雲が 地面に つぶれる ----
KO_PUFFS = [(30, 46, 8), (20, 49, 7), (40, 48, 7), (13, 52, 5), (48, 52, 5.5), (27, 52, 7), (37, 52, 7)]

def layers():
    BELL = R(bell_g()); BELL_F = R(bell_g(flash=True)); BELL_KO = R(bell_g(KO_PUFFS, base=58, squash=.8))
    return [
        L('tent', 'tent', R(tent_g()), alt={'idle1|idle2|walk1|walk2': R(tent_g(1)), 'atk0': R(tent_g(-1)), 'ko': R(tent_g(limp=True))}),
        L('bell', 'bell', BELL, alt={'idle1|idle3|walk3|atk0': BELL_F, 'ko': BELL_KO}),
        dict(n='eyes', g='bell', x=38, y=21, rows=EYES, alt=EYES_ALT, not_='ko'),
        dict(n='eyesko', g='root', x=36, y=51, rows=EYES_ALT['ko'], only='ko'),
        dict(n='mouth', g='bell', x=42, y=26, rows=MOUTH, alt={'atk1|atk2': MOUTH_OPEN, 'blink': MOUTH, 'hit': MOUTH_SHUT}, not_='ko'),
        dict(n='mouthko', g='root', x=41, y=55, rows=MOUTH_SHUT, only='ko'),
        L('charge', 'bell', CHARGE, only='atk0'),
        L('strike', 'bell', STRIKE, only='atk1'),
        L('strike2', 'bell', STRIKE2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'bell': (0, -1), 'tent': (0, -1)}, 'idle2': {'bell': (0, -1)}, 'idle3': {'tent': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)}, 'walk1': {'root': (0, -2), 'tent': (0, 1)}, 'walk2': {'root': (0, -1)}, 'walk3': {'root': (0, 0), 'tent': (0, -1)},
    'atk0': {'root': (-2, -2), 'tent': (0, -2)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (1, 0)},
    'hit': {'root': (-3, -1), 'tent': (-1, 1)},
    'ko': {'tent': (0, 0)},
}
PARENT = {'bell': 'root', 'tent': 'bell'}
