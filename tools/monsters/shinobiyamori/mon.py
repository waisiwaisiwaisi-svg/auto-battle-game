# シノビヤモリ（あく・かくとう × ヤモリ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, stamp

# ---------- 下書きの 道具（あたり用。陰影の 仕上げ・目・牙などは 手で 打つ）----------
N = 72
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < len(g) and 0 <= x < len(g[0]) else '.'
def put(g, x, y, ch):
    if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def dots(g, ch, pts, only=None):
    for x, y in pts:
        if only is None or at(g, x, y) in only: put(g, x, y, ch)
def ell(g, cx, cy, rx, ry, ch):
    for y in range(N):
        for x in range(N):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: g[y][x] = ch
def pol(g, pts, ch):
    for y in range(N):
        for x in range(N):
            px, py, c = x + .5, y + .5, False
            for i in range(len(pts)):
                (x1, y1), (x2, y2) = pts[i], pts[i - 1]
                if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
            if c: g[y][x] = ch
def tube(g, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: put(g, x, y, ch)
def light_map(p, r=2):
    H, W = len(p), len(p[0]); m = [[1 if p[y][x] != '.' else 0 for x in range(W)] for y in range(H)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < H and 0 <= xx < W else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(H) for x in range(W) if m[y][x]}
def shade(p, ramps, r=2, hi=.3, lo=-.3):
    """光は 左上：上と 左の ふちは 明、右下は 暗"""
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps: h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def ink(s):
    g = G()
    for y in range(N):
        for x in range(N):
            if s[y][x] == '.' and any(at(s, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
            elif s[y][x] != '.': g[y][x] = s[y][x]
    return g
def part(paint, ramps, r=2, hi=.3, lo=-.3, post=None, after=None):
    p = G(); paint(p); s = shade(p, ramps, r, hi, lo)
    if post: post(s)
    g = ink(s)
    if after: after(g)
    return rows_of(g)
def flat(parts, frame):
    g = grid(N + 32, N + 32)
    for d in parts:
        if d.get('only') and frame not in d['only'].split('|'): continue
        if d.get('not_') and frame in d['not_'].split('|'): continue
        rows = d['rows']
        for k, v in (d.get('alt') or {}).items():
            if frame in k.split('|'): rows = v
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c not in '. ': put(g, d['x'] + i + 16, d['y'] + j + 16, c)
    return g
def crop(g):
    ys = [y for y in range(len(g)) if any(c != '.' for c in g[y])]; xs = [x for x in range(len(g[0])) if any(g[y][x] != '.' for y in range(len(g)))]
    return [''.join(g[y][xs[0]:xs[-1] + 1]) for y in range(ys[0], ys[-1] + 1)]
def rot_cw(rows): h, w = len(rows), len(rows[0]); return [''.join(rows[h - 1 - y][x] for y in range(h)) for x in range(w)]
def rot_ccw(rows): h, w = len(rows), len(rows[0]); return [''.join(rows[y][w - 1 - x] for y in range(h)) for x in range(w)]
def ko_layer(parts, rot, cx=32, ground=61):
    """ダウン：体ごと 横だおしに（90度 回転）して 地面に 置く"""
    rows = rot(crop(flat(parts, 'ko')))
    return dict(n='ko', g='root', x=cx - len(rows[0]) // 2, y=ground - len(rows) + 1, rows=rows, only='ko')
def ko_plan(parts, plan, ground=61):
    """ダウン（専用の ポーズ）：plan = [(パーツ名, 回転 or None, x, y)]。回転した かたまりは 左上を (x, 地面) に、回転なしは (x, y) だけ ずらす"""
    g = grid(N + 32, N + 32)
    for names, rot, x, y in plan:
        f = flat([d for d in parts if d['n'] in names], 'ko')
        if rot:
            rows = rot(crop(f)); ox, oy = x + 16, (ground - len(rows) + 1 if y is None else y) + 16
        else:
            rows = rows_of(f); ox, oy = x, y
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': put(g, ox + i, oy + j, c)
    return dict(n='ko', g='root', x=-16, y=-16, rows=rows_of(g), only='ko')

META = dict(id='shinobiyamori', name='シノビヤモリ', types=['dark', 'fighting'], base='ヤモリ', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2034',
    'A': '#b4cc6a', 'B': '#6e903c', 'D': '#3a5428',      # ヤモリの 皮
    'C': '#6a6ea4', 'E': '#3e4272', 'F': '#24254a',      # 忍び 装束（こん）
    'R': '#ec4a4a', 'r': '#8a2232',                      # 赤い 襟巻き・帯
    'S': '#eef2f8', 'T': '#8a94ac',                      # 手裏剣の 刃（鋼）
    'Y': '#ffe040', 'w': '#ffffff',
}
LIGHT = set('ACRSYw')
KEEP_BLACK = set('wY')
RAMP = {'1': 'ABD', '2': 'CEF', '3': 'RRr', '4': 'SST', '5': 'BBD', '6': 'EFF'}

def deg(a, r, cx, cy): return (cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r)

# ---------- しっぽ ----------
def tail():
    def pa(p): tube(p, [(21, 49), (13, 53), (7, 52), (4, 47), (5, 41), (9, 38)], [3.4, 2.8, 2.2, 1.7, 1.2, .7], '1')
    def post(s):     # しまもよう（手で）
        for (x, y) in ((14, 52), (8, 50), (5, 44)):
            dots(s, 'D', [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], 'ABD')
    return part(pa, RAMP, r=1, post=post)

# ---------- 奥の うで（地面に 手を つく 低い かまえ）と 奥の 足 ----------
def arm_back():
    def pa(p): tube(p, [(36, 36), (41, 46), (44, 56)], [2.4, 2, 1.8], '5')
    def af(g):
        stamp(g, ['.kk.kk.', 'kBkkBBk', 'kBBBBDk', '.kkkkk.'], 41, 56)
        dots(g, 'D', [(41, 57), (45, 56)])
    return part(pa, RAMP, r=1, after=af)
def leg_back():
    def pa(p):
        ell(p, 22, 50, 5, 4, '5'); tube(p, [(21, 52), (16, 56), (17, 59)], [2.4, 2, 1.8], '5')
    def af(g): stamp(g, ['kk.kk.kk', 'kBkkBkkBk', '.kkkkkkk.'], 12, 58)
    return part(pa, RAMP, r=1, after=af)

# ---------- 襟巻きの 後ろへ たなびく 2本の 帯 ----------
def scarf(ph=0):
    def pa(p):
        w = [0, 1, 0, -1][ph]
        tube(p, [(36, 26), (29, 22 + w), (22, 20), (15, 21 - w), (10, 19)], [2.2, 2, 1.8, 1.6, 1.3], '3')
        tube(p, [(35, 28), (28, 28 - w), (21, 27), (15, 29 + w)], [1.8, 1.6, 1.4, 1.1], '3')
    def post(s):
        for y in range(N):
            for x in range(N):
                if s[y][x] == 'R' and x % 5 == 0: s[y][x] = 'r'
    return part(pa, RAMP, r=1, hi=.2, post=post)

# ---------- 胴：忍び 装束、赤い 帯 ----------
def body():
    def pa(p):
        pol(p, [(21, 49), (23, 39), (29, 31), (36, 28), (41, 31), (41, 40), (37, 48), (29, 52)], '2')
    def post(s):
        for x in range(20, 44):            # 赤い 帯（ななめ）
            for d in (0, 1, 2):
                y = round(46 - (x - 20) * .25) + d
                if at(s, x, y) in 'CEF': s[y][x] = 'R' if d == 0 else 'r' if d == 2 else 'R'
        for (x, y) in ((30, 34), (31, 35), (32, 36), (33, 37), (34, 38)):   # えりの 合わせ
            if at(s, x, y) in 'CEF': s[y][x] = 'F'
    return part(pa, RAMP, r=2, post=post)
def leg():
    def pa(p):
        ell(p, 32, 49, 6.5, 4.5, '1')
        tube(p, [(35, 51), (37, 56), (36, 59)], [2.8, 2.4, 2], '1')
    def af(g):      # ゆびの 吸盤
        stamp(g, ['.kk.kk.kk', 'kAAkAAkAAk', 'kBBBBBBBBk', '.kkkkkkkk.'], 32, 57)
    return part(pa, RAMP, r=1, after=af)

# ---------- 頭：平たい ヤモリの 頭、ずきんと するどい 目 ----------
def head():
    def pa(p):
        pol(p, [(36, 18), (44, 16), (51, 18), (56, 21), (59, 24), (57, 27), (49, 29), (39, 30), (35, 26)], '1')
    def post(s):
        for x in range(44, 58):            # 口の 線（長く さける）
            y = round(27 - (x - 44) * .15)
            if at(s, x, y) != '.': s[y][x] = 'k'
        dots(s, 'w', [(46, 28), (49, 28), (52, 27)], 'ABD')             # 牙
        dots(s, 'k', [(56, 22)])                                       # 鼻の あな
        for (x, y) in ((40, 26), (43, 25), (38, 23)):                  # つぶつぶの うろこ
            dots(s, 'A', [(x, y)], 'B')
    return part(pa, RAMP, r=2, post=post)
def hood():
    def pa(p):
        pol(p, [(33, 25), (34, 18), (38, 14), (44, 13), (49, 15), (51, 18), (45, 19), (40, 22), (37, 27)], '2')
    def af(g):     # 額あての 鉄板
        stamp(g, ['kkkkk', 'kSSTk', 'kSTTk', 'kkkkk'], 42, 14)
    return part(pa, RAMP, r=1, after=af)
# 大きな 目：ずきんの ふちが まゆの ひさし、たての ひとみ
EYE = ['kkkkk.', 'kYYkYk', 'kYYkYk', '.kkkk.']
EYE_ALT = {
    'blink': ['kkkkk.', 'kBBBBk', 'kkkkkk', '......'],
    'atk0|atk1|atk2': ['kkkkk.', 'kYYkYk', 'kwYkYk', '.kkkk.'],
    'hit': ['kkkkk.', 'kYkkYk', 'kkYYkk', '.kkkk.'],
    'ko': ['kkkkk.', 'kYkYkk', 'kkYkkk', 'kYkYk.'],
}

# ---------- 見せ所：手裏剣の 手（放射する ゆび、吸盤が 刃）----------
def hand(cx=52, cy=37, rot=0):
    def pa(p):
        tube(p, [(37, 33), (44, 36), (cx - 2, cy)], [2.8, 2.4, 2.2], '1')
        ell(p, cx, cy, 3.6, 3.6, '1')
        for a in (-80, -25, 30, 85):
            a += rot
            tube(p, [deg(a, 2, cx, cy), deg(a, 7, cx, cy)], [1.6, 1.2], '1')
    def af(g):
        for a in (-80, -25, 30, 85):
            a += rot
            # 吸盤＝刃：ゆびの 先に 鋼の 刃（とがった ひし形）
            bx, by = deg(a, 9, cx, cy); tx, ty = deg(a, 13, cx, cy); lx, ly = deg(a + 40, 8, cx, cy); rx, ry = deg(a - 40, 8, cx, cy)
            q = G(); pol(q, [(bx - (bx - lx) * .4 + .5, by - (by - ly) * .4 + .5), (tx + .5, ty + .5), (bx - (bx - rx) * .4 + .5, by - (by - ry) * .4 + .5), (deg(a, 7, cx, cy)[0] + .5, deg(a, 7, cx, cy)[1] + .5)], '4')
            s = shade(q, RAMP, r=1); o = ink(s)
            for y in range(N):
                for x in range(N):
                    if o[y][x] != '.' and g[y][x] in '.k': g[y][x] = o[y][x]
        dots(g, 'D', [(cx, cy), (cx - 1, cy), (cx, cy + 1)])
    return part(pa, RAMP, r=1, after=af)

# 飛ぶ 手裏剣
STAR = [
    '...kk....',
    '...kSk...',
    '...kSTk..',
    'kkkkSkkkk',
    'kSSSkTTTk',
    'kkkkTkkkk',
    '..kTTk...',
    '...kTk...',
    '....kk...',
]
STAR2 = [
    '..k....kk',
    '..kSk.kSk',
    '...kSkSk.',
    '...kkTkk.',
    '..kTkkTk.',
    '.kTk..kTk',
    '.kk....kk',
]
SPEED = ['kkkk.kkk', '........', '.kkkkk..']

def parts():
    return [
        dict(n='scarf', g='scarf', x=0, y=0, rows=scarf(0), alt={'idle1|idle3|walk1|walk3': scarf(1), 'atk1|atk2|hit': scarf(2)}),
        dict(n='tail', g='tail', x=0, y=0, rows=tail()),
        dict(n='legB', g='legB', x=0, y=0, rows=leg_back()),
        dict(n='armB', g='armB', x=0, y=0, rows=arm_back()),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legA', g='legA', x=0, y=0, rows=leg()),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='hood', g='head', x=0, y=0, rows=hood()),
        dict(n='eye', g='head', x=45, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='hand', g='arm', x=0, y=0, rows=hand(), alt={'atk1|atk2': hand(55, 33, 45)}),
    ]
_C = {}
def layers():
    if 'L' not in _C:
        P = parts()
        L = [dict(d, not_='ko') for d in P]
        L.append(ko_plan(P, [(['scarf', 'tail', 'legB', 'body', 'legA', 'hand'], rot_cw, 8, None), (['head', 'hood', 'eye'], None, 2, 30)]))
        L += [
            dict(n='star', g='fx', x=63, y=26, rows=STAR, only='atk1'),
            dict(n='star2', g='fx', x=66, y=27, rows=STAR2, only='atk2'),
            dict(n='speed', g='fx', x=57, y=30, rows=SPEED, only='atk2'),
        ]
        _C['L'] = L
    return _C['L']

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'tail': (0, -1)}, 'idle3': {'body': (0, 0), 'arm': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'armB': (1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'armB': (-1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'arm': (-4, 1), 'head': (-1, 0), 'tail': (1, 0)},
    'atk1': {'root': (3, 0), 'body': (1, 0), 'arm': (2, 0)},
    'atk2': {'root': (3, 0), 'body': (1, 0), 'arm': (2, 1)},
    'hit': {'root': (-3, 0), 'body': (-1, 0), 'head': (-2, -1), 'arm': (-2, 1), 'scarf': (0, -1)},
    'ko': {},
}
PARENT = {'head': 'body', 'scarf': 'body', 'arm': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
