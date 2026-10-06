# クビナシバ（ゴースト・あく × 馬）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり用。陰影の 仕上げ・目・牙は 手で 打つ）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def put(g, x0, y0, rows):
    """手で 打った 小さな 絵を 置く（'.' は すける）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < 64 and 0 <= x0 + i < 64: g[y0 + j][x0 + i] = c
def ink(p, keep=None):
    """色の かたまりの まわりに 黒い 輪郭"""
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
            elif p[y][x] != '.': g[y][x] = p[y][x]
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
def shade(p, ramps, r=2, hi=.35, lo=-.3):
    """光は 左上：上と 左の ふちは 明、右下は 暗（ramps: 下書き文字 → (明, 中, 暗)）"""
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64: p[y][x] = ch
def oval(p, cx, cy, rx, ry, ch): ellipse(p, cx, cy, rx, ry, ch)
def recol(g, mp, box=None):
    x0, y0, x1, y1 = box or (0, 0, 64, 64)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if g[y][x] in mp: g[y][x] = mp[g[y][x]]
def shift(g, dx, dy):
    o = G()
    for y in range(64):
        for x in range(64):
            if g[y][x] != '.' and 0 <= x + dx < 64 and 0 <= y + dy < 64: o[y + dy][x + dx] = g[y][x]
    return o

META = dict(id='kubinashiba', name='クビナシバ', types=['ghost', 'dark'], base='馬', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1a3a',
    'A': '#7a7498', 'B': '#46405e', 'D': '#26213a',      # 体（黒馬の 青ずみ）
    'S': '#9c7ab8', 'T': '#58387a',                      # 黒煙の たてがみ
    'W': '#f2fff6', 'C': '#78f0d8', 'V': '#2a98b8',      # 霊火の 頭
    'U': '#ddd4c0', 'X': '#8a7f6c',                      # ひづめ（骨）
    'r': '#ff3050',
}
LIGHT = set('AWCSU')
KEEP_BLACK = set('WCVr')

RB = {'1': 'ABD', '2': 'STl', '3': 'UUX'}

def body():
    p = G()
    oval(p, 28, 36, 13, 7.5, '1')          # 胴
    oval(p, 18, 34, 8.5, 8.5, '1')         # しり
    oval(p, 38, 35, 7.5, 8.5, '1')         # 胸
    tube(p, [(38, 33), (43, 25), (46, 19)], [7, 5.6, 4.6], '1')   # 太い 首
    s = shade(p, RB, r=2)
    # 首の 切り口：上の ふちが 焦げて 暗い
    for x in range(64):
        ys = [y for y in range(64) if s[y][x] != '.' and y < 24]
        for y in ys[:2]: s[y][x] = 'D'
    # 肩と もも の すじ（筋肉の 影）
    dots(s, 'D', [(34, 33), (33, 34), (33, 35), (32, 36), (24, 32), (23, 33), (22, 34), (22, 35), (22, 36)])
    dots(s, 'A', [(35, 32), (36, 31), (25, 31), (26, 30)])
    return ink(s)

def leg(path, rad):
    p = G(); tube(p, path, rad, '1'); s = shade(p, RB, r=1, hi=.2, lo=-.2)
    x, y = path[-1]; x = round(x)
    for i in range(-2, 3):
        s[61][x + i] = 'X'; s[60][x + i] = 'U' if i < 1 else 'X'
    return ink(s)
FRONT_N = lambda: leg([(39, 38), (40, 46), (40, 52), (41, 59)], [3.6, 2.6, 1.8, 1.6])
FRONT_F = lambda: leg([(34, 38), (35, 46), (34, 52), (35, 59)], [3, 2.4, 1.7, 1.5])
HIND_N = lambda: leg([(16, 37), (15, 44), (12, 50), (14, 55), (15, 59)], [4.6, 3.4, 2, 1.7, 1.6])
HIND_F = lambda: leg([(22, 39), (21, 45), (19, 50), (21, 55), (22, 59)], [3.6, 2.8, 1.8, 1.6, 1.5])

def smoke(paths):
    p = G()
    for path, rad in paths: tube(p, path, rad, '2')
    s = shade(p, RB, r=1, hi=.2, lo=-.25)
    return ink(s)
MANE = [
    ([(41, 26), (37, 22), (33, 21), (30, 18)], [2.6, 2.4, 1.6, .6]),
    ([(43, 21), (40, 16), (36, 14), (33, 10)], [2.6, 2.2, 1.6, .6]),
    ([(44, 16), (42, 11), (39, 8)], [2.2, 1.6, .6]),
]
MANE2 = [
    ([(41, 26), (36, 23), (32, 21), (29, 19)], [2.6, 2.4, 1.6, .6]),
    ([(43, 21), (39, 17), (35, 15), (32, 12)], [2.6, 2.2, 1.6, .6]),
    ([(44, 16), (41, 12), (38, 10)], [2.2, 1.6, .6]),
]
TAIL = [([(11, 32), (6, 30), (3, 33), (2, 40), (4, 45)], [2.8, 2.6, 2.2, 1.6, .6]),
        ([(11, 34), (8, 38), (7, 44)], [2, 1.6, .6])]
TAIL2 = [([(11, 32), (6, 31), (4, 35), (4, 41), (2, 46)], [2.8, 2.6, 2.2, 1.6, .6]),
         ([(11, 34), (9, 39), (9, 45)], [2, 1.6, .6])]

# ---------- 霊火の 頭（見せ所）：馬の 頭の 形を した 炎。耳と たてがみが 炎の 舌 ----------
def flame(var=0, big=0):
    p = G()
    sh = [(41, 21), (42, 12), (45, 6), (51, 5), (56, 8), (61, 13), (63, 17), (62, 20), (56, 21), (50, 21), (47, 23)]
    if big: sh = [(x + (1 if x > 50 else 0), y - (1 if y < 12 else 0)) for x, y in sh]
    poly(p, sh, 'V')
    # 炎の 舌（耳・後ろへ なびく）
    tongues = [[(44, 9), (46, 0 + var), (49, 6)], [(48, 6), (52, 1 - var), (53, 6)], [(42, 13), (36, 5 + var), (45, 8)], [(41, 18), (35, 13 - var), (42, 15)]]
    for t in tongues: poly(p, t, 'V')
    # 内側ほど 明るい
    def inner(ch_from, ch_to, n, ox=0, oy=0):
        q = [r[:] for r in p]
        for y in range(64):
            for x in range(64):
                if p[y][x] == ch_from and all(at(p, x + dx + ox, y + dy + oy) != '.' for dx in range(-n, n + 1) for dy in range(-n, n + 1) if abs(dx) + abs(dy) <= n): q[y][x] = ch_to
        return q
    p = inner('V', 'C', 2, 1, 1)
    p = inner('C', 'W', 4, 1, 2)
    g = ink(p)
    return g
EYE = ['kkk.....', '.kkkkk..', '..krrrkk', '...kkkk.']   # つり上がった 切れ目、赤く 光る ひとみ
EYE_ALT = {'blink': ['........', '.kkkk...', '..kkkkkk', '........'],
           'hit': ['.k.....k', '..kk.kk.', '....k...', '..kk.kk.'],
           'atk0|atk1|atk2': ['kkk.....', '.kkkkkk.', '..krrrrk', '...kkkk.'],
           'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...']}
MOUTH = ['......kk', '..kkkk.k', 'kkWkWkk.', '.kkkkk..']  # 裂けた 口と 炎の 牙
MOUTH_OPEN = ['.......kk', '..kkkkk.k', 'kkWkWkWkk', 'krrrrrrk.', 'kkWkWkk..', '.kkkkk...']
BLAST = [
    '.....VV.......',
    '..VVCCVV..V...',
    'VVCCWWCCVVCV..',
    'VCWWWWWWCCVVV.',
    'VCWWWWWWWCCVVV',
    'VVCCWWWCCVV.V.',
    '..VVCCCVV..V..',
    '....VV........',
]

def layers():
    BODY = rows_of(body())
    return [
        dict(n='tail', g='tail', x=0, y=0, rows=rows_of(smoke(TAIL)), alt={'idle1|idle2|walk1|walk3|atk1': rows_of(smoke(TAIL2))}),
        dict(n='legHF', g='legB', x=0, y=0, rows=rows_of(HIND_F())),
        dict(n='legFF', g='legA', x=0, y=0, rows=rows_of(FRONT_F())),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='legHN', g='legA', x=0, y=0, rows=rows_of(HIND_N())),
        dict(n='legFN', g='legB', x=0, y=0, rows=rows_of(FRONT_N())),
        dict(n='mane', g='neck', x=0, y=0, rows=rows_of(smoke(MANE)), alt={'idle1|idle2|walk1|walk3|atk1': rows_of(smoke(MANE2))}),
        dict(n='flame', g='head', x=0, y=0, rows=rows_of(flame()), alt={'idle1|idle2|walk1|walk3': rows_of(flame(1)), 'atk0|atk1|atk2': rows_of(flame(1, 1))}),
        dict(n='eye', g='head', x=48, y=9, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=53, y=16, rows=MOUTH, alt={'atk1|atk2': MOUTH_OPEN}),
        dict(n='blast', g='head', x=63, y=11, rows=BLAST, only='atk1'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'body': (0, 1), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, -1), 'legB': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (2, 1)},
    'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-3, 1), 'legA': (1, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'neck', 'neck': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
