# カシャ（ほのお・あく × 猫）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp

# ---------- 下書きの 道具（あたりを とって 自動で 3段の 陰影 → 仕上げは 手で 打つ）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def put(g, x, y, ch):
    if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def dots(g, ch, pts):
    for x, y in pts: put(g, x, y, ch)
def disc(p, cx, cy, rx, ry=None, ch='1'):
    ry = ry or rx
    for y in range(64):
        for x in range(64):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: p[y][x] = ch
def tube(p, path, rad, ch='1'):
    """道すじに そって 丸い 管を ぬる（太さは 点ごとに 指定）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: put(p, x, y, ch)
def shade(p, ramps, r=2, hi=.3, lo=-.3, tilt=.35, rim=True):
    """光は 左上：ふくらみ（まわりの 量の かたむき）＋ 全体の 斜めの かたむき → 明・中・暗。上と 左の ふちは 明、右下の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    pts = [(x, y) for y in range(64) for x in range(64) if p[y][x] in ramps]
    if not pts: return [row[:] for row in p]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    cx, cy, w, h = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(4, max(xs) - min(xs)), max(4, max(ys) - min(ys))
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for x, y in pts:
        c = p[y][x]; hc, mc, dc = ramps[c]
        v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 - tilt * ((x - cx) / w * 1.2 + (y - cy) / h * 1.6)
        t = hc if v > hi else dc if v < lo else mc
        if rim:
            ul = at(p, x - 1, y) == '.' or at(p, x, y - 1) == '.'
            dr = at(p, x + 1, y) == '.' or at(p, x, y + 1) == '.'
            if ul and not dr and v > lo: t = hc
            elif dr and not ul: t = dc
        out[y][x] = t
    return out
def ink(p, g=None):
    """まわりに 黒の 輪郭（エンジンが 内側の 線と 光側を 濃い色に する）"""
    g = g or G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
    return g
def swap(g, mapping, box=None):
    x0, y0, x1, y1 = box or (0, 0, 63, 63)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if g[y][x] in mapping: g[y][x] = mapping[g[y][x]]
    return g
def L(n, grp, g, **kw): return dict(n=n, g=grp, x=0, y=0, rows=rows_of(g) if isinstance(g[0], list) else g, **kw)

META = dict(id='kasha', name='カシャ', types=['fire', 'dark'], base='猫', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1630',
    'A': '#7e6c96', 'B': '#4a3a62', 'D': '#261c38',      # 毛（闇の 黒紫）
    'Y': '#ffe65a', 'O': '#ff8a1e', 'R': '#d8341c', 'r': '#6e1420',   # 炎
    'S': '#c8c0cc', 's': '#6c6274',                      # 車輪の 鉄
    'w': '#ffffff', 'p': '#e86a8a',                      # 牙・爪／口の 中
}
LIGHT = set('AYOSw')
KEEP_BLACK = set('wYO')
FUR = {'1': 'ABD'}
FUR_BACK = {'1': 'BDD'}

RC = (16, 22); RO, RI = 11.5, 6.5      # 尾の 輪（車輪）

# ---------- 尾：丸めて 輪に した 車輪。輪の 中に 鉄の 輻（や）、外へ 炎 ----------
def flames(phase):
    p = G()
    for i in range(11):
        a = i * 360 / 11 + phase * 16 + 8
        if 250 < a % 360 < 330: continue                       # 下（胴の 後ろ）は 炎を 引く
        ln = 4 + (1.5 if i % 2 else 0) + (1 if 60 < a % 360 < 200 else 0)
        pts, rad = [], []
        for j in range(5):
            t = j / 4; rr = RO - 1.5 + ln * t; aa = math.radians(a + 30 * t)    # 回る 向きと 逆へ なびく
            pts.append((RC[0] + rr * math.cos(aa), RC[1] - rr * math.sin(aa))); rad.append(2.4 * (1 - t) + .4)
        tube(p, pts, rad, 'F')
    for y in range(64):
        for x in range(64):
            if p[y][x] == 'F':
                d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
                p[y][x] = 'Y' if d < RO + 1.2 else 'O' if d < RO + 3.4 else 'R'
    g = ink(p); swap(g, {'k': 'r'})
    return g
def wheel(spin):
    p = G(); disc(p, RC[0], RC[1], RO, RO, '1')
    tube(p, [(21, 41), (14, 41), (8, 37), (6, 31)], [3, 3, 2.8, 2.8], '1')       # 尾の つけね → 輪へ
    s = shade(p, FUR, r=2, tilt=.5)
    for y in range(64):
        for x in range(64):
            if math.hypot(x + .5 - RC[0], y + .5 - RC[1]) < RI: s[y][x] = '.'
    g = ink(s)
    # 輪の 中：燃える 芯
    for y in range(64):
        for x in range(64):
            d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
            if d < RI - .6: g[y][x] = 'O' if d < RI - 2.2 else 'R'
    # 鉄の 輻（4本）：spin で 45度 回る
    cx, cy = RC[0] - .5, RC[1] - .5
    for a in ((0, 90, 180, 270) if spin == 0 else (45, 135, 225, 315)):
        x1, y1 = round(cx + 5 * math.cos(math.radians(a))), round(cy - 5 * math.sin(math.radians(a)))
        line(g, round(cx), round(cy), x1, y1, 'S')
    hx, hy = RC[0] - 1, RC[1] - 1
    for (x, y, c) in ((0, 0, 'w'), (1, 0, 'S'), (0, 1, 'S'), (1, 1, 's'), (-1, 0, 'k'), (2, 1, 'k'), (0, -1, 'k'), (1, 2, 'k'), (-1, 1, 'k'), (2, 0, 'k'), (0, 2, 'k'), (1, -1, 'k')):
        put(g, hx + x, hy + y, c)
    # 輪の ふち：鉄の たが（内がわ）＋ 毛の すじ
    for y in range(64):
        for x in range(64):
            d = math.hypot(x + .5 - RC[0], y + .5 - RC[1])
            if RI <= d < RI + 1.2 and g[y][x] in 'ABDk': g[y][x] = 'S' if (x < RC[0] and y < RC[1] + 2) else 's'
    for a in range(0, 360, 30):
        x, y = round(RC[0] + 9 * math.cos(math.radians(a)) - .5), round(RC[1] - 9 * math.sin(math.radians(a)) - .5)
        if g[y][x] in 'AB': g[y][x] = 'D' if g[y][x] == 'B' else 'B'
    return g

# ---------- 胴：背を 弓なりに 立てる（威嚇の 猫）----------
def body(arch=0):
    p = G()
    tube(p, [(21, 42), (25, 37 - arch), (32, 36 - arch), (38, 39)], [5.5, 6, 6, 5.8], '1')
    tube(p, [(23, 45), (36, 44)], [3.2, 3.8], '1')
    s = shade(p, FUR, r=3, tilt=.6)
    g = ink(s)
    # 背の 逆立つ 毛（とげの ように 3つ）
    for (x, y) in ((22, 34 - arch), (27, 30 - arch), (33, 30 - arch)):
        stamp(g, ['..k', '.kA', 'kAB'], x, y)
    # 腹の 下の 影と 肩の 筋
    dots(g, 'D', [(33, 43), (34, 44), (35, 44), (24, 46), (25, 47)])
    return g

# ---------- 脚：長く 細く、前足は 爪を 立てる ----------
LEGS = {
    'h': [(23, 44), (21, 51), (23, 56), (22, 59)],
    'f': [(38, 44), (39, 51), (40, 59)],
}
def leg(kind, back, dx=0, lift=0):
    p = G(); path = [(x + (dx if i else 0), y - (lift if i == len(LEGS[kind]) - 1 else 0)) for i, (x, y) in enumerate(LEGS[kind])]
    if kind == 'h':
        tube(p, path[:2], [4.5, 2.8], '1'); tube(p, path[1:], [2.4, 2, 2], '1')
    else:
        tube(p, path, [3.2, 2.4, 2.2], '1')
    fx, fy = path[-1]
    tube(p, [(fx - 1, fy), (fx + 2, fy)], [1.7, 1.7], '1')     # 足先
    s = shade(p, FUR_BACK if back else FUR, r=1, tilt=.3)
    g = ink(s)
    if not back or kind == 'f':
        fx, fy = round(fx), round(fy)
        dots(g, 'w', [(fx + 3, fy + 1), (fx + 1, fy + 2)] if kind == 'f' else [(fx + 3, fy + 1)])
    return g

# ---------- 頭：あたりは だ円、目・口・牙は 手で ----------
def head(mode='idle'):
    p = G()
    disc(p, 45, 33, 7.5, 6.5, '1'); disc(p, 51.5, 36.5, 4.3, 3.3, '1')
    poly(p, [(38, 31), (40, 20), (46, 28)], '1')      # 手前の 耳
    poly(p, [(45, 28), (51, 20), (53, 30)], '1')      # 奥の 耳
    poly(p, [(40, 36), (35, 39), (38, 40), (36, 43), (42, 41)], '1')   # ほおの 毛の 房
    s = shade(p, FUR, r=2, tilt=.5)
    g = ink(s)
    # 耳の 中（熾火）
    dots(g, 'r', [(41, 25), (41, 26), (42, 26), (42, 27), (41, 27), (43, 28)])
    dots(g, 'R', [(41, 24), (42, 25), (40, 26)])
    dots(g, 'r', [(49, 25), (50, 26), (49, 27), (50, 27), (50, 28), (51, 27)])
    dots(g, 'R', [(50, 24), (50, 25), (51, 26)])
    # まゆの ひさし（前へ 下がる 黒い 線）
    for x, y in ((44, 29), (45, 29), (46, 30), (47, 30), (48, 30), (49, 30), (50, 31), (51, 31), (52, 32)): g[y][x] = 'k'
    dots(g, 'A', [(44, 28), (45, 28), (46, 29), (47, 29), (48, 29)])
    # 目：つり上がった 炎色の 目＋たての ひとみ
    E = {'idle': ['YYYkOk', 'kYYkYk', '.kkkk.'], 'blink': ['kkkkkk', '.DDDD.', '......'], 'atk': ['YYYkYY', 'YYYkYk', '.kkkk.'],
         'hit': ['kkBBkk', 'BBkkBB', '......'], 'ko': ['k.k...', '.k....', 'k.k...']}[mode]
    stamp(g, E, 46, 31)
    if mode == 'ko':
        for x, y in ((47, 31), (49, 31), (48, 32), (47, 33), (49, 33)): g[y][x] = 'k'
        for x, y in ((48, 31), (47, 32), (49, 32), (48, 33), (46, 31), (50, 31)): g[y][x] = 'B'
    # 熾火の くまどり（ほおと ひたい）
    dots(g, 'R', [(41, 30), (42, 31), (43, 32), (40, 34), (41, 35), (42, 35), (39, 29)])
    dots(g, 'O', [(41, 31), (40, 35)])
    # 鼻
    stamp(g, ['kk', 'kD'], 54, 34)
    if mode == 'atk':
        # 大きく 開いた 口（シャーッ）：上下の 牙
        stamp(g, ['kkkkkkkk.', 'kwkpppwkk', 'kppppppk.', 'kwkpppwk.', '.kkkkkk..'], 47, 37)
        for y in range(42, 44):
            for x in range(47, 56):
                if g[y][x] in 'ABD': g[y][x] = '.'
    elif mode in ('ko', 'blink', 'hit'):
        for x, y in ((48, 38), (49, 38), (50, 39), (51, 39), (52, 39), (53, 38)): g[y][x] = 'k'
        if mode != 'ko': dots(g, 'w', [(51, 40)])
    else:
        # とじた 口から 牙が のぞく
        for x, y in ((47, 38), (48, 38), (49, 39), (50, 39), (51, 39), (52, 39), (53, 38), (54, 38)): g[y][x] = 'k'
        dots(g, 'w', [(50, 40), (53, 39)])
        dots(g, 'k', [(50, 41), (53, 40)])
    return g

# ---------- 爪の ひと振り（炎の 弧）----------
SLASH = [
    '........kkk...',
    '.....kkkRYk...',
    '...kkROYYk....',
    '..kROYYkk.kk..',
    '.kROYkk.kkRYk.',
    'kROYk.kkROYk..',
    'kRYk.kROYkk...',
    'kRk.kROYk..kk.',
    'kk..kRYk.kkRYk',
    '...kRYk.kROYk.',
    '...kRk.kROYk..',
    '...kk..kRYk...',
    '.......kRk....',
    '.......kk.....',
]

def layers():
    return [
        L('fl', 'tail', flames(0), alt={'idle1|idle3|walk1|walk3|atk1': rows_of(flames(1))}, not_='ko'),
        L('wheel', 'tail', wheel(0), alt={'idle2|idle3|walk1|walk3|atk1': rows_of(wheel(1))}),
        L('hb', 'legB', leg('h', True)),
        L('fb', 'legA', leg('f', True, 1)),
        L('body', 'body', body(), alt={'atk0': rows_of(body(2))}),
        L('hf', 'legA', leg('h', False)),
        L('ff', 'legB', leg('f', False), alt={'atk1|atk2': rows_of(leg('f', False, 4, 3))}),
        L('head', 'head', head(), alt={'blink': rows_of(head('blink')), 'atk0|atk1|atk2': rows_of(head('atk')), 'hit': rows_of(head('hit')), 'ko': rows_of(head('ko'))}),
        dict(n='slash', g='root', x=49, y=31, rows=SLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'head': (0, 0)}, 'idle2': {'body': (0, 1)}, 'idle3': {'body': (0, 0), 'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 1), 'tail': (0, -1), 'legA': (-1, 0), 'legB': (-1, 0)},
    'atk1': {'root': (5, -2), 'legB': (2, 0)},
    'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
