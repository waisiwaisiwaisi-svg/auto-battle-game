# ジャドク（どく・あく × コブラ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp

META = dict(id='jadoku', name='ジャドク', types=['poison', 'dark'], base='コブラ', size='M')
PAL = {
    'k': '#101018', 'l': '#24162e',
    'A': '#9a74b8', 'B': '#5a3c7c', 'D': '#30204a',      # うろこ（黒紫）
    'E': '#dcec80', 'F': '#8ca234',                      # 腹の 板（黄緑）
    'G': '#b8ff6c', 'g': '#30b03a',                      # 毒の 光
    'Y': '#ffe14a', 'w': '#ffffff', 'r': '#9a1838',
    'U': '#ece4d4', 'V': '#9a8e80',                      # 骨の とげ
}
LIGHT = set('AEGYwU')
KEEP_BLACK = set('wGgYr')

# ---------- 下書きの 道具 ----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
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
def tube(p, path, rad, belly=None):
    """道すじに そって 丸い 管を ぬる。belly：下がわ（dy > rad*belly）を 腹の 板に"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64:
                        b = belly is not None and (y + .5 - cy) > r * belly
                        if p[y][x] == '.' or (p[y][x] == '2' and not b): p[y][x] = '2' if b else '1'
def ell(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
RAMP = {'1': 'ABD', '2': 'EEF'}
def scutes(s, step=3):
    """腹の 板：上の ふちは 光、区切りは 暗い 線（手で 間を 決める）"""
    for y in range(64):
        for x in range(64):
            if s[y][x] in 'EF':
                if at(s, x, y - 1) in 'ABD': s[y][x] = 'E'
                elif x % step == 0: s[y][x] = 'F'
                elif at(s, x, y + 1) in 'k.': s[y][x] = 'F'
    return s

# ---------- とぐろ：なめらかな 2段の 輪 ----------
def coil_low():
    p = G(); path = ell(29, 53, 21, 5.5, 0, 360, 40); tube(p, path, [4.4] * len(path), belly=.3)
    s = scutes(shade(p, RAMP, r=2))
    g = G(); ink(g, s); return g
def coil_up_back():
    p = G(); path = ell(31, 46, 15, 4.6, 180, 360, 20); tube(p, path, [4.2] * len(path))
    s = shade(p, RAMP, r=2); g = G(); ink(g, s); return g
def coil_up_front():
    p = G(); path = ell(31, 46, 15, 4.6, -10, 190, 24); tube(p, path, [4.2] * len(path), belly=.35)
    s = scutes(shade(p, RAMP, r=2)); g = G(); ink(g, s)
    return g
def tail_g():
    p = G(); path = [(10, 54), (6, 51), (3, 49)]; tube(p, path, [3, 2, 1.2])
    s = shade(p, RAMP, r=1); g = G(); ink(g, s)
    stamp(g, ['kk...', 'kUkk.', '.kUVk', '..kk.'], 0, 46)
    return g
def dorsal_marks(g, pts):
    """背の 山形もよう（手で）：暗い くの字"""
    for (x, y) in pts:
        for (dx, dy) in ((0, 0), (1, -1), (2, 0)):
            if g[y + dy][x + dx] in 'AB': g[y + dy][x + dx] = 'D'

# ---------- 首（腹の 板が 前がわ）----------
NECK_PATH = [(39, 46), (41, 41), (41, 34), (39, 27), (38, 20), (41, 15)]
def neck():
    p = G()
    tube(p, NECK_PATH, [4.6, 4.4, 4.2, 4.2, 4, 3.6])
    # 前がわ（右）は 腹の 板
    for y in range(64):
        xs = [x for x in range(64) if p[y][x] != '.']
        if xs:
            for x in xs[-3:]: p[y][x] = '2'
    s = shade(p, RAMP, r=1)
    for y in range(15, 48, 3):     # 腹の 板の 区切り
        xs = [x for x in range(64) if s[y][x] in 'EF']
        for x in xs: s[y][x] = 'F'
    g = G(); ink(g, s); return g

# ---------- フード：大きく 弧を えがいて 広がる 膜（背中がわ）----------
HOOD_TOP, HOOD_BOT = 4, 40
# 行ごとの 半はば（手で 決める）：上は 丸く、肩で いちばん 広がり、下は えぐれて 首へ しぼむ
HW = [4, 8, 10.5, 12, 13.5, 14.5, 15.2, 15.8, 16.3, 16.6, 16.8, 16.8, 16.8, 16.6, 16.4, 16, 15.5, 14.8, 14, 13, 11.8, 10.4, 9, 7.6, 6.5, 5.6, 5, 4.6, 4.4, 4.2, 4.2, 4.2, 4.2, 4.2, 4.2, 4.2, 4.2]
def hood_w(y): return HW[y - HOOD_TOP]
def hood_c(y): return 34.5 + (y - 22) * .1
def hood(flare=0):
    p = G()
    for y in range(HOOD_TOP, HOOD_BOT + 1):
        w = hood_w(y) + (flare if 10 < y < 34 else 0); c = hood_c(y)
        for x in range(64):
            if abs(x + .5 - c) <= w: p[y][x] = '1'
    s = shade(p, {'1': 'ABD'}, r=3, hi=.3, lo=-.28)
    # 膜の 肋（ろっ骨）：首から 放射する 暗い すじ、となりに 光
    for ang in (-52, -22, 22, 52):
        a = math.radians(ang - 90)
        for i in range(6, 30):
            x, y = round(hood_c(36) + math.cos(a) * i * .62), round(36 + math.sin(a) * i)
            if 0 <= y < 64 and s[y][x] in 'AB':
                s[y][x] = 'D' if s[y][x] == 'B' else s[y][x]
    # ふちの 内がわは うすい 膜（明るく）
    for y in range(64):
        for x in range(64):
            if s[y][x] != '.' and y < 34 and (at(s, x - 2, y) == '.' or at(s, x, y - 2) == '.') and s[y][x] in 'BD': s[y][x] = 'A'
    g = G(); ink(g, s)
    # 目玉もよう：めがねの ように つながった 2つの 毒の 目（つり上がる）
    stamp(g, OCELLUS_L, 23, 13); stamp(g, OCELLUS_R, 36, 13)
    # 目玉の 下の 暗い くまどり（にらむ 形）
    for (x, y) in ((25, 21), (26, 22), (27, 22), (28, 23), (42, 21), (41, 22), (40, 22), (39, 23)):
        if g[y][x] in 'ABD': g[y][x] = 'D'
    return g
OCELLUS_L = [
    'kk.........',
    'kGkk.......',
    'kgGGkkk....',
    '.kgGGGGkkk.',
    '.kggGGkGGGk',
    '..kggGkGgk.',
    '...kkggkk..',
    '.....kk....',
]
OCELLUS_R = [r[::-1] for r in OCELLUS_L]
SPK = ['kk....', 'kUkkk.', '.kUUVk', '..kkkk']
SPK2 = ['..kkkk', '.kUUVk', 'kUkkk.', 'kk....']

# ---------- 頭：平たい くさび形、たての ひとみの つり目、長い 毒牙 ----------
HEAD = [
    '......kkkkkk..........',
    '....kkAAAAAAkkkk......',
    '..kkAAABBBBBAAAAkkk...',
    '.kAABBBBBBBBBBBBAAAkk.',
    'kAABBBkkkkkBBBBBBBBAAk',
    'kABBBBBYYkYkkBBBBBBBBk',
    'kBBBBBBYYkYYkBBBBBBBBk',
    'kBBBBBBBkkkkBBBBBBBkBk',
    'kDBBBBBBBBBBBBBBBBBBDk',
    'kDDBBBBBBBBBkkkkkkkkkk',
    '.kDDBkkkkkkkkkkwkkwk..',
    '..kDDkEEEEEEEEEwkkwk..',
    '...kkDFFFFFFFFFkkkk...',
    '.....kkkkkkkkkkk......',
]
HEAD_OPEN = [
    '......kkkkkk..........',
    '....kkAAAAAAkkkk......',
    '..kkAAABBBBBAAAAkkk...',
    '.kAABBBBBBBBBBBBAAAkk.',
    'kAABBBkkkkkBBBBBBBBAAk',
    'kABBBBBYYYYkkBBBBBBBBk',
    'kBBBBBBYkYYYkBBBBBBBBk',
    'kBBBBBBBkkkkBBBBBBBkBk',
    'kDBBBBBkkkkkkkkkkkkkkk',
    'kDDBBkrrrrrrrrrwkkwk..',
    'kDDBkrrrrrrrrrrwkkwk..',
    '.kDBkrrrrrrrrrrrrrrrk.',
    '.kDDkrrrrrrrrrrrrrrrk.',
    '.kDDkkkkkkkkwkkkkwkkk.',
    '..kDDEEEEEEEEEEEEEk...',
    '...kkFFFFFFFFFFFkk....',
    '.....kkkkkkkkkkk......',
]
def _eye(h, a, b, c='BkkkkB'):
    h = list(h)
    h[5] = h[5][:6] + a + h[5][6 + len(a):]; h[6] = h[6][:6] + b + h[6][6 + len(b):]; h[7] = h[7][:6] + c + h[7][6 + len(c):]
    return h
HEAD_BLINK = _eye(HEAD, 'BBBBBkk', 'BkkkkkB', 'BBBBBB')
HEAD_HIT = _eye(HEAD, 'BkBBkBk', 'BBkkBBk', 'BkBBkB')
HEAD_KO = _eye(HEAD, 'BkBkBBk', 'BBkBBBk', 'BkBkBB')
HEAD_ATK0 = _eye(HEAD, 'BYYYYkk', 'BYYkYYk', 'BBkkkk')
DRIP = ['G', 'g']
DRIP2 = ['.', 'G', 'g']
SPIT = [
    '.........G..G......',
    '...GG..GGg.....G...',
    'GGGgGGGGgGG.GG..Gg.',
    'gGGGggGGGgGGgGG.G..',
    '..gg..GgG..g..g....',
    '.......g......g....',
]
SPIT2 = ['.......G...G..', '..G.GgG..G..g.', 'GgGG.g..g.....', '.g.....g......']

def layers():
    LOW = rows_of(coil_low()); UB = rows_of(coil_up_back()); UF = coil_up_front()
    UF = rows_of(UF)
    HOOD = rows_of(hood()); HOOD_F = rows_of(hood(1)); NECK = rows_of(neck()); TAIL = rows_of(tail_g())
    return [
        dict(n='tail', g='coil', x=0, y=0, rows=TAIL),
        dict(n='low', g='coil', x=0, y=0, rows=LOW),
        dict(n='upb', g='coil', x=0, y=0, rows=UB),
        dict(n='neck', g='neck', x=0, y=0, rows=NECK, not_='ko'),
        dict(n='spk0', g='hood', x=14, y=4, rows=SPK, not_='ko'),
        dict(n='spk1', g='hood', x=13, y=10, rows=SPK, not_='ko'),
        dict(n='spk2', g='hood', x=13, y=17, rows=SPK, not_='ko'),
        dict(n='spk3', g='hood', x=16, y=25, rows=SPK2, not_='ko'),
        dict(n='hood', g='hood', x=0, y=0, rows=HOOD, alt={'atk0|atk1|atk2': HOOD_F}, not_='ko'),
        dict(n='upf', g='coil', x=0, y=0, rows=UF),
        dict(n='head', g='head', x=39, y=7, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN, 'atk0': HEAD_ATK0, 'blink': HEAD_BLINK, 'hit': HEAD_HIT, 'ko': HEAD_KO}),
        dict(n='drip', g='head', x=57, y=20, rows=DRIP, alt={'idle2|idle3|walk1|walk3': DRIP2}, not_='atk1|atk2|ko'),
        dict(n='spit', g='head', x=61, y=15, rows=SPIT, only='atk1'),
        dict(n='spit2', g='head', x=63, y=16, rows=SPIT2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'neck': (0, 1)}, 'idle2': {'neck': (0, 1), 'hood': (0, 0)}, 'idle3': {'neck': (0, 0), 'hood': (0, -1)},
    'blink': {},
    'walk0': {'neck': (-1, 0)}, 'walk1': {'neck': (0, 1)}, 'walk2': {'neck': (1, 0)}, 'walk3': {'neck': (0, 1)},
    'atk0': {'neck': (-2, 1), 'hood': (0, -1), 'head': (-1, 0)}, 'atk1': {'neck': (2, -1), 'head': (2, 0)}, 'atk2': {'neck': (2, 0), 'head': (1, 0)},
    'hit': {'neck': (-2, 1), 'head': (-2, 1)}, 'ko': {'head': (2, 38)},
}
PARENT = {'head': 'neck', 'hood': 'neck', 'neck': 'root', 'coil': 'root'}
