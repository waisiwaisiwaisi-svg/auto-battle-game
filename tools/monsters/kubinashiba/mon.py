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
    oval(p, 27, 36, 13, 7.5, '1')          # 胴
    oval(p, 16, 34, 8, 8, '1')             # しり
    oval(p, 37, 35, 7.5, 8.5, '1')         # 胸
    tube(p, [(37, 33), (41, 26), (44, 20)], [7, 5.4, 4.4], '1')   # 太い 首
    s = shade(p, RB, r=2)
    # 首の 切り口：上の ふちが 焦げて 暗い
    for x in range(64):
        ys = [y for y in range(64) if s[y][x] != '.' and y < 24]
        for y in ys[:2]: s[y][x] = 'D'
    # 肩と もも の すじ（筋肉の 影）
    dots(s, 'D', [(33, 33), (32, 34), (32, 35), (31, 36), (22, 32), (21, 33), (20, 34), (20, 35), (20, 36), (12, 39), (13, 40), (26, 42), (30, 42)])
    dots(s, 'A', [(34, 32), (35, 31), (23, 31), (24, 30)])
    return ink(s)

def leg(path, rad):
    p = G(); tube(p, path, rad, '1'); s = shade(p, RB, r=1, hi=.2, lo=-.2)
    x, y = path[-1]; x = round(x)
    for i in range(-2, 2):
        s[61][x + i] = 'X'; s[60][x + i] = 'U' if i < 0 else 'X'
    return ink(s)
FRONT_N = lambda: leg([(38, 39), (39, 46), (39, 52), (40, 59)], [3.2, 2.2, 1.6, 1.5])
FRONT_F = lambda: leg([(33, 39), (34, 46), (33, 52), (34, 59)], [2.8, 2, 1.5, 1.4])
HIND_N = lambda: leg([(14, 37), (14, 44), (11, 50), (13, 55), (14, 59)], [4, 3, 1.7, 1.5, 1.5])
HIND_F = lambda: leg([(20, 39), (20, 45), (18, 50), (20, 55), (21, 59)], [3.2, 2.4, 1.5, 1.4, 1.4])

def KO_LEGS():
    p = G()
    tube(p, [(36, 54), (42, 57), (48, 59)], [3, 2, 1.5], '1')
    tube(p, [(14, 53), (20, 57), (26, 59)], [3.4, 2.2, 1.5], '1')
    s = shade(p, RB, r=1, hi=.2, lo=-.2)
    dots(s, 'U', [(48, 58), (49, 58), (26, 58), (27, 58)]); dots(s, 'X', [(49, 59), (50, 59), (27, 59), (28, 59)])
    return ink(s)

def smoke(paths):
    p = G()
    for path, rad in paths: tube(p, path, rad, '2')
    s = shade(p, RB, r=1, hi=.2, lo=-.25)
    return ink(s)
# 黒煙の たてがみ：首すじから 後ろ上へ 立ちのぼる 筋
MANE = [
    ([(38, 28), (33, 25), (29, 25), (25, 22)], [2.4, 2.2, 1.6, .6]),
    ([(40, 24), (35, 19), (30, 18), (27, 14)], [2.6, 2.2, 1.6, .6]),
    ([(42, 20), (38, 14), (34, 11), (32, 7)], [2.4, 2, 1.4, .6]),
]
MANE2 = [
    ([(38, 28), (33, 26), (28, 25), (24, 23)], [2.4, 2.2, 1.6, .6]),
    ([(40, 24), (35, 20), (30, 19), (26, 16)], [2.6, 2.2, 1.6, .6]),
    ([(42, 20), (38, 15), (34, 13), (31, 9)], [2.4, 2, 1.4, .6]),
]
TAIL = [([(9, 32), (5, 33), (3, 38), (3, 44), (5, 49)], [2.8, 2.6, 2.2, 1.6, .6]),
        ([(9, 34), (7, 40), (8, 46)], [2, 1.5, .6])]
TAIL2 = [([(9, 32), (5, 34), (4, 39), (3, 45), (2, 50)], [2.8, 2.6, 2.2, 1.6, .6]),
         ([(9, 34), (8, 40), (10, 45)], [2, 1.5, .6])]

# ---------- 霊火の 頭（見せ所）：馬の 頭の 形を した 炎。耳と たてがみが 炎の 舌 ----------
def flame(var=0, big=0, ko=False):
    p = G()
    sh = [(40, 22), (41, 14), (44, 7), (50, 5), (55, 8), (62, 14), (63, 19), (60, 22), (54, 21), (50, 24), (45, 25)]
    if big: sh = [(x, y - (1 if y < 12 else 0)) for x, y in sh]
    poly(p, sh, 'V')
    # 炎の 舌（耳・後ろへ なびく 炎の たてがみ）
    tongues = [[(45, 8), (46, 0 + var), (50, 6)], [(49, 6), (54, 1 + var), (54, 8)],
               [(42, 12), (33, 4 + var), (46, 8)], [(41, 16), (32, 12 - var), (42, 13)], [(40, 21), (34, 19 + var), (41, 18)]]
    for t in tongues: poly(p, t, 'V')
    def inner(src, dst, n, ox=0, oy=0):
        q = [r[:] for r in p]
        for y in range(64):
            for x in range(64):
                if p[y][x] == src and all(at(p, x + dx + ox, y + dy + oy) != '.' for dx in range(-n, n + 1) for dy in range(-n, n + 1) if abs(dx) + abs(dy) <= n): q[y][x] = dst
        return q
    p = inner('V', 'C', 1, 1, 0)
    if not ko:
        p = inner('C', 'W', 3, -1, 2)
        for y in range(64):          # 白い 芯は 下半分だけ（炎の 根もと）
            for x in range(64):
                if p[y][x] == 'W' and (y < 15 or x > 58): p[y][x] = 'C'
    else:
        for y in range(64):
            for x in range(64):
                if p[y][x] == 'C' and (x + y) % 2: p[y][x] = 'V'
    # 炎の すじ（右下 → 左上へ なめる 線）
    for (x0, y0, x1, y1) in ((47, 21, 42, 15), (52, 20, 47, 13), (58, 19, 55, 15), (44, 12, 40, 8)):
        line(p, x0, y0, x1, y1, 'V')
    # ほお骨の かげ
    dots(p, 'V', [(48, 16), (49, 17), (50, 17), (51, 17)])
    return ink(p)
# まゆの ひさし＋つり上がった 切れ目、赤く 光る ひとみ
EYE = ['kk.......', 'kkkk.....', '.kkkkkk..', '..krrrrk.', '...kkkkk.']
EYE_ALT = {'blink': ['kk.......', 'kkkk.....', '.kkkkkk..', '..kkkkkk.', '.........'],
           'hit': ['k........', '.kk......', '...kkkkk.', '.kk......', 'k........'],
           'atk0|atk1|atk2': ['kk.......', 'kkkk.....', '.kkkkkkk.', '..krrrrrk', '...kkkkk.'],
           'ko': ['kk...kk..', '..k.k....', '...k.....', '..k.k....', 'kk...kk..']}
MOUTH = ['.......kk', '...kkkk.k', 'kkkWkWkk.', '.kkkkkk..']  # 裂けた 口と 炎の 牙
MOUTH_OPEN = ['.......kk', '..kkkkkk.', 'kkWkWkWkk', 'krrrrrrk.', 'kkWkWkWk.', '.kkkkkk..']
BLAST = [
    '.....VV........',
    '..VVCCVV..V....',
    'VVCCWWCCVVCV.V.',
    'VCWWWWWWCCVVV..',
    'VCWWWWWWWCCVVVV',
    'VVCCWWWCCVV.V..',
    '..VVCCCVV..V...',
    '....VV.........',
]
BLAST2 = ['..V..V..', 'VCCVV.V.', 'CWWCCV..', 'VCCV.V..', '..V.....']

def layers():
    BODY = rows_of(body())
    return [
        dict(n='kolegs', g='root', x=0, y=0, rows=rows_of(KO_LEGS()), only='ko'),
        dict(n='tail', g='tail', x=0, y=0, rows=rows_of(smoke(TAIL)), alt={'idle1|idle2|walk1|walk3|atk1': rows_of(smoke(TAIL2))}),
        dict(n='legHF', not_='ko', g='legB', x=0, y=0, rows=rows_of(HIND_F())),
        dict(n='legFF', not_='ko', g='legA', x=0, y=0, rows=rows_of(FRONT_F())),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='legHN', not_='ko', g='legA', x=0, y=0, rows=rows_of(HIND_N())),
        dict(n='legFN', not_='ko', g='legB', x=0, y=0, rows=rows_of(FRONT_N())),
        dict(n='mane', g='neck', x=0, y=0, rows=rows_of(smoke(MANE)), alt={'idle1|idle2|walk1|walk3|atk1': rows_of(smoke(MANE2))}),
        dict(n='flame', g='head', x=0, y=0, rows=rows_of(flame()), alt={'idle1|idle2|walk1|walk3': rows_of(flame(1)), 'atk0|atk1|atk2': rows_of(flame(1, 1)), 'ko': rows_of(flame(0, 0, True))}),
        dict(n='eye', g='head', x=48, y=10, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=55, y=18, rows=MOUTH, alt={'atk1|atk2': MOUTH_OPEN}),
        dict(n='blast', g='head', x=63, y=13, rows=BLAST, only='atk1'),
        dict(n='blast2', g='head', x=64, y=15, rows=BLAST2, only='atk2'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'body': (0, 1), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, -1), 'legB': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (2, 1)},
    'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-3, 1), 'legA': (1, 0)},
    'ko': {'body': (-2, 15), 'head': (5, 22), 'tail': (0, -2)},
}
PARENT = {'head': 'neck', 'neck': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
