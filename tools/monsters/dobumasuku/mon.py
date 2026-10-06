# ドブマスク（あく・どく × ドブネズミ）手打ち GBA風
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

META = dict(id='dobumasuku', name='ドブマスク', types=['dark', 'poison'], base='ドブネズミ', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1e30',
    'A': '#948aa0', 'B': '#5e5268', 'D': '#382c42',      # 毛（ドブねずみ色）
    'M': '#f2e4c0', 'N': '#c4a674', 'O': '#7a5e3c',      # くちばし 仮面（骨）
    'G': '#c0f450', 'g': '#4ca83a',                      # 毒の 霧
    'R': '#ff5a3a', 'r': '#8a1a2a',                      # 光る 目
    'P': '#e8a0a4', 'p': '#a05a68',                      # しっぽ・耳の 皮
    'w': '#ffffff',
}
LIGHT = set('AMGRPw')
KEEP_BLACK = set('wGRr')
RAMP = {'1': 'ABD', '2': 'MNO', '3': 'PPp', '4': 'BBD', '5': 'ppp'}

CLAW = ['kkkk...', 'kwwwkk.', '.kkwwwk', '...kkwk', '....kwk', '.....k.']
CLAWB = ['kkk...', 'kNNkk.', '.kkNNk', '...kNk', '....k.']
# ---------- しっぽ（はだかの 長い しっぽ、ふしの すじ）----------
def tail():
    def pa(p): tube(p, [(19, 50), (11, 54), (5, 52), (2, 46), (3, 39), (7, 35), (10, 34)], [2.4, 2.1, 1.8, 1.5, 1.2, .9, .6], '3')
    def post(s):
        for y in range(N):
            for x in range(N):
                if s[y][x] in 'Pp' and (x + y) % 4 == 0: s[y][x] = 'p'
    return part(pa, RAMP, r=1, post=post)

# ---------- うしろの 足・うで（奥は 暗く）----------
def leg_back():
    def pa(p):
        ell(p, 21, 50, 6, 5.5, '4')
        pol(p, [(17, 52), (23, 52), (22, 58), (27, 59), (28, 61), (16, 61), (16, 56)], '4')
    return part(pa, RAMP, r=1, after=lambda g: dots(g, 'w', [(27, 61), (29, 61)]))
def arm_back():
    def pa(p): tube(p, [(36, 33), (42, 34), (47, 36)], [2.6, 2.2, 2], '4')
    def af(g):
        stamp(g, CLAWB, 46, 31); stamp(g, CLAWB, 48, 35)
    return part(pa, RAMP, r=1, after=af)

# ---------- 胴：前かがみ、背中に さか立つ 毛 ----------
def body():
    def pa(p):
        pol(p, [(15, 42), (18, 34), (24, 29), (31, 27), (37, 29), (40, 35), (40, 44), (36, 51), (27, 54), (19, 52)], '1')
        for (x, y) in ((16, 37), (19, 32), (23, 29), (28, 27)):     # 背の さか毛
            pol(p, [(x, y + 4), (x - 4, y - 2), (x + 3, y + 1)], '1')
    def post(s):
        for (x, y) in ((22, 38), (25, 35), (21, 44), (27, 42), (30, 33)):   # 毛の すじ（手で）
            dots(s, 'D', [(x, y), (x + 1, y + 1), (x + 1, y + 2)], 'AB')
        for y in range(40, 54):            # 腹は 少し 明るく
            for x in range(31, 40):
                if s[y][x] == 'B' and (x + y) % 2 == 0 and x < 37: s[y][x] = 'A'
    return part(pa, RAMP, r=2, post=post)
def leg():
    def pa(p):
        ell(p, 31, 49, 6.5, 6, '1')
        pol(p, [(27, 52), (34, 52), (33, 57), (39, 58), (41, 61), (27, 61), (27, 56)], '1')
    return part(pa, RAMP, r=1, after=lambda g: dots(g, 'w', [(40, 61), (42, 61), (38, 61)]))

# ---------- 頭：耳と 後ろ頭の 毛、くちばし 仮面 ----------
def ear_back():
    def pa(p): ell(p, 30, 15, 4, 5, '4'); pol(p, [(27, 15), (30, 7), (33, 13)], '4')
    return part(pa, RAMP, r=1)
def head():
    def pa(p):
        ell(p, 36, 24, 8, 7.5, '1')
        pol(p, [(29, 20), (26, 27), (31, 29)], '1')                        # ほおの 毛の とげ
    return part(pa, RAMP, r=2)
def jaw():      # 仮面の 下から のぞく あご と 黄色い 前歯
    def pa(p): pol(p, [(36, 28), (46, 30), (48, 33), (44, 35), (37, 34)], '1')
    def af(g): stamp(g, ['kkk', 'NMk', 'NMk', 'kNk', '.k.'], 45, 30); stamp(g, ['kk', 'Nk', 'Nk', 'k.'], 44, 31)
    return part(pa, RAMP, r=1, after=af)
def ear():
    def pa(p):
        ell(p, 35, 13, 4.5, 5.5, '1'); pol(p, [(31, 14), (33, 4), (37, 10)], '1')
        ell(p, 35.5, 13.5, 1.8, 3.2, '5')
    def af(g): dots(g, 'k', [(37, 12), (38, 12)])                        # 耳の 切れこみ
    return part(pa, RAMP, r=1, after=af)
def mask():
    def pa(p):
        pol(p, [(36, 16), (43, 16), (49, 19), (54, 23), (58, 27), (62, 32), (62, 34), (57, 33), (51, 32), (45, 31), (39, 30), (35, 27), (34, 20)], '2')
    def post(s):
        for x in range(42, 62):            # くちばしの ぬい目（上と 下の 合わせ目）
            y = round(24 + (x - 42) * .42)
            if at(s, x, y) in 'MN': s[y][x] = 'O'
            if at(s, x, y - 1) == 'N': s[y - 1][x] = 'M'
        for y in range(17, 30):            # 仮面の 革ひも
            if at(s, 37, y) != '.': s[y][37] = 'O'
            if at(s, 38, y) != '.': s[y][38] = 'N'
    def af(g):
        dots(g, 'k', [(55, 27), (56, 28), (59, 30)])                    # 鼻の あな
        dots(g, 'O', [(44, 29), (48, 30), (52, 31)])                    # 鋲
    return part(pa, RAMP, r=2, hi=.25, post=post, after=af)
# するどい 目：仮面の 目あなから 赤く 光る（つり目）
EYE = ['kkO.....', 'NkkkO...', 'NkRwkkO.', '.kRRRRkO', '..kkkkkO']
EYE_ALT = {
    'blink': ['kkO.....', 'NkkkO...', 'NOkkkkO.', '.kkkkkkO', '..OOOOOO'],
    'atk0|atk1|atk2': ['kkO.....', 'NkkkO...', 'NkRwRkO.', '.kRRRRRk', '..kRRRkO'],
    'hit': ['kkO.....', 'NkkkO...', 'NkRkkRO.', '.kkRRkkO', '..kkkkkO'],
    'ko': ['kkO.....', 'NkkkO...', 'NkRkRkO.', '.kkRkkkO', '..kRkRkO'],
}
def arm():
    def pa(p): tube(p, [(33, 36), (38, 41), (44, 43)], [3.2, 2.8, 2.6], '1')
    def af(g):     # 大きな かぎ爪 3本（下へ 曲がる）
        stamp(g, CLAW, 44, 38); stamp(g, CLAW, 46, 41); stamp(g, CLAW, 43, 44)
    return part(pa, RAMP, r=1, after=af)

# ---------- 毒の 霧 ----------
MIST0 = ['...kk..', '..kGGk.', '.kGgGk.', '..kgk..', '...k...', '..kGk..', '..kgk..', '...k...']
MIST1 = ['.....kk', '...kkGk', '..kGGgk', '.kGgGk.', '..kgk..', '...k...', '..kGk..', '...k...']
WISP0 = ['.kk..', 'kGGk.', '.kgGk', '..kk.']
WISP1 = ['..kk.', '.kGGk', 'kGgk.', '.kk..']
CLOUD_OLD = [
    '..........kkk.........',
    '...kkk...kGGGk..kk....',
    '..kGGGkkkGGGGGkkGGk...',
    '.kGGGGGGGGgGGGGGGGGkk.',
    'kGGgGGGGgggGGGGgGGGGGk',
    'kGgggGGggkggGGgggGGgGk',
    '.kgggggggkkgggggggggk.',
    '..kkgggkk..kkgggkkkk..',
    '....kkk......kkk......',
]
CLOUD = [
    '.........kkk......',
    '....kkk.kGGGk.....',
    '...kGGGkGGGGGkkk..',
    '..kGGGGGGgGGGGGGk.',
    '.kGGgGGGggGGGgGGGk',
    'kGGgggGGGGGGgggGGk',
    'GGGgggGGGgGGgggGGk',
    'kGGGGggGggggGGGGGk',
    '.kGggggkgggkgggGk.',
    '..kggkkkggk.kggk..',
    '...kk...kk...kk...',
]
CLOUD2 = [
    '....kk.......kk.....',
    '..kkGGk....kkGGk....',
    '.kGGgGk...kGGgGGk...',
    'kGgggk...kGgggggk.kk',
    '.kggk.....kggkgk.kGk',
    '..kk.......kk.k...k.',
]

def parts():
    return [
        dict(n='tail', g='tail', x=0, y=0, rows=tail()),
        dict(n='legB', g='legB', x=0, y=0, rows=leg_back()),
        dict(n='armB', g='armB', x=0, y=0, rows=arm_back()),
        dict(n='earB', g='head', x=0, y=0, rows=ear_back()),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legA', g='legA', x=0, y=0, rows=leg()),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='jaw', g='head', x=0, y=0, rows=jaw()),
        dict(n='ear', g='ear', x=0, y=0, rows=ear()),
        dict(n='mask', g='head', x=0, y=0, rows=mask()),
        dict(n='eye', g='head', x=39, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='arm', x=0, y=0, rows=arm()),
    ]
_C = {}
def layers():
    if 'L' not in _C:
        P = parts()
        L = [dict(d, not_='ko') for d in P]
        L.append(ko_plan(P, [
            (['tail'], None, 4, 9),
            (['body', 'legA', 'arm'], rot_cw, 10, None),
            (['earB', 'head', 'jaw', 'ear', 'mask', 'eye'], None, 4, 27)]))
        L += [
            dict(n='mist', g='head', x=58, y=33, rows=MIST0, alt={'idle2|idle3|walk1|walk3': MIST1}, not_='ko|atk0|atk1|atk2|hit'),
            dict(n='wisp', g='head', x=52, y=23, rows=WISP0, alt={'idle1|idle3|walk0|walk2': WISP1}, not_='ko|atk1|atk2|hit'),
            dict(n='cloud', g='head', x=55, y=24, rows=CLOUD, only='atk1'),
            dict(n='cloud2', g='head', x=60, y=24, rows=CLOUD2, only='atk2'),
        ]
        _C['L'] = L
    return _C['L']

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'tail': (0, -1)}, 'idle3': {'body': (0, 0), 'ear': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'arm': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'arm': (1, 0)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 0), 'arm': (-2, 0), 'armB': (-2, 0), 'tail': (0, -1)},
    'atk1': {'root': (4, 0), 'body': (1, 1), 'head': (2, 1), 'arm': (3, -1), 'armB': (2, 0)},
    'atk2': {'root': (5, 0), 'body': (1, 1), 'head': (1, 1), 'arm': (3, 2)},
    'hit': {'root': (-3, 0), 'body': (-1, 0), 'head': (-2, -1), 'arm': (-2, -1), 'ear': (-1, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'ear': 'head', 'arm': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
