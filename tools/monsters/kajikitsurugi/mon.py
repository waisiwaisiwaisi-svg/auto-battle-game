# カジキツルギ（はがね・みず × カジキ）手打ち GBA風
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, outline

META = dict(id='kajikitsurugi', name='カジキツルギ', types=['steel', 'water'], base='カジキ', size='L')
PAL = {
    'k': '#101018', 'l': '#14204a',
    'A': '#62a6f4', 'B': '#2a5cc0', 'D': '#162f78',      # 背（深い 青）
    'S': '#f6faff', 'T': '#b4c0d4', 'U': '#6e7a96', 'V': '#3a4260',   # 鋼
    'c': '#b4f6ff', 'C': '#38a4f0',                      # 水
    'Y': '#ffdc4a', 'O': '#c4781a',                      # 金（目・つば）
    'r': '#e8304a',                                      # 目の 奥の 赤
}
LIGHT = set('ASTcY')
KEEP_BLACK = set('Yr')

# ---------- 下書きの 道具 ----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def ink(g, p):
    """パーツ p を 黒の ふちごと g に 重ねる（下の パーツとの さかいに 線）"""
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
def light_map(p, r=2):
    """光は 左上。ふちの 向きから 明るさ（+ 明 / - 影）"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    L = {}
    for y in range(64):
        for x in range(64):
            if not m[y][x]: continue
            gx = B(x + 1, y) - B(x - 1, y); gy = B(x, y + 1) - B(x, y - 1)
            L[(x, y)] = (gx * .55 + gy * .85) * 3
    return L
def shade(p, ramps, r=2, hi=.35, lo=-.3, ybias=None):
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c not in ramps: continue
        if ybias: v -= (y - ybias[0]) * ybias[1]
        h, m, d = ramps[c]
        out[y][x] = h if v > hi else d if v < lo else m
    return out

# ---------- 体：背は 深い 青、腹は 鋼の うろこ ----------
BODY_PTS = [(48, 42), (45, 38), (39, 35), (31, 34), (24, 35), (18, 38), (14, 42), (12, 44), (12, 47), (15, 49), (21, 52), (28, 55), (35, 55), (41, 53), (45, 50), (48, 47)]
def belly_y(x): return 45 + (1 if x > 41 else 0) - (1 if x < 18 else 0)
def body():
    p = G(); poly(p, BODY_PTS, '1')
    for y in range(64):
        for x in range(64):
            if p[y][x] == '1' and y > belly_y(x): p[y][x] = '2'
    s = shade(p, {'1': 'ABD', '2': 'STU'}, r=2, hi=.3, lo=-.25, ybias=(44, .035))
    # 腹の 鋼の うろこ：ずらして 重ねた 弧（下の ふちが 影、左上が 光）を 手で 打つ
    DK = {'S': 'T', 'T': 'U', 'U': 'V', 'V': 'V'}; LT = {'T': 'S', 'U': 'T', 'V': 'U', 'S': 'S'}
    for row, cy in enumerate((47, 50, 53)):
        for cx in range(14 + (2 if row % 2 else 0), 48, 5):
            for (dx, dy) in ((-2, 0), (-1, 1), (0, 1), (1, 1), (2, 0)):
                x, y = cx + dx, cy + dy
                if p[y][x] == '2' and y > belly_y(x): s[y][x] = DK[s[y][x]]
            x, y = cx - 1, cy - 1
            if p[y][x] == '2' and y > belly_y(x) + 1: s[y][x] = LT[s[y][x]]
    # 背と 腹の さかい：側線（青の 濃い線 → 鋼の 光）
    for x in range(13, 48):
        y = belly_y(x)
        if s[y][x] in 'ABD': s[y][x] = 'D'
        if s[y + 1][x] in 'STUV' and x < 41: s[y + 1][x] = 'S'
    # 背の 鎧の 板（よろいの さね）：後ろへ そった すじ
    for x0 in (21, 27, 33):
        for i in range(0, 10):
            x, y = x0 - i // 3, 36 + i
            if p[y][x] == '1' and s[y][x] in 'ABD':
                s[y][x] = 'D'
                if s[y][x + 1] in 'BD': s[y][x + 1] = 'A' if i < 5 else 'B'
    # 背の 光の すじ（手で）
    dots(s, 'A', [(29, 35), (30, 35), (31, 35), (25, 36), (24, 36), (35, 36), (36, 36), (20, 38), (19, 39)])
    g = G(); ink(g, s)
    return g

# ---------- えら（鋼の かぶとの ほお当て）と 頭 ----------
def head_g(atk=False):
    g = G()
    # ほお当て：鋼の 板
    p = G(); poly(p, [(38, 39), (46, 40), (49, 43), (49, 48), (45, 51), (40, 52), (37, 48)], '2')
    s = shade(p, {'2': 'STU'}, r=1, hi=.3, lo=-.3); ink(g, s)
    # かぶと：ひさしが 目の 上に 張り出し、後ろへ 角が のびる
    p = G(); poly(p, [(35, 37), (40, 35), (46, 36), (50, 39), (51, 42), (47, 41), (42, 41), (37, 42), (32, 41), (27, 39)], '2')
    s = shade(p, {'2': 'STU'}, r=1, hi=.25, lo=-.25); ink(g, s)
    # かぶとの 鋲・板の すじ・ひさしの 下の 影（手で）
    dots(g, 'V', [(38, 38), (39, 39), (40, 40), (34, 38), (35, 39)])
    dots(g, 'S', [(37, 37), (41, 36), (42, 36), (43, 36), (33, 38), (30, 39)])
    dots(g, 'U', [(44, 42), (45, 42), (46, 42), (47, 42), (39, 42), (40, 42)])
    dots(g, 'Y', [(45, 38)]); dots(g, 'O', [(45, 39)])
    # 口：深く 切れこむ 線と 牙
    if atk:
        for x in range(41, 50): g[47][x] = 'k'
        for x in range(43, 50): g[48][x] = 'r'
        for x in range(42, 50): g[49][x] = 'k'
        dots(g, 'S', [(45, 48), (48, 48)])
    else:
        for x in range(42, 50): g[47][x] = 'k'
        dots(g, 'S', [(46, 48), (44, 48)]); dots(g, 'k', [(41, 46)])
    # えらの 切れめ（後ろの ふち）
    dots(g, 'V', [(39, 44), (39, 45), (40, 46), (40, 47), (41, 49)])
    return g

# ---------- 剣の くちばし（刀）と つば：上の ふちが 光る 刃、下は 刃文 ----------
BILL = [
    '...............kk',
    '...........kkkkSk',
    '.......kkkkSSSSkk',
    'kkkkkkkSSSSTTUkk.',
    'SSSSSSSTTTTUkk...',
    'TTTTcTTTUUkk.....',
    'UUUUUUUVkk.......',
    'kkkkkkkkk........',
]
BILL_ATK = [r.replace('T', 'S', 3) for r in BILL]
TSUBA = ['kkk', 'YOk', 'YVk', 'OVk', 'YOk', 'OOk', 'kkk']

# ---------- 帆の 背びれ：鋼の 骨が 刃の ように つき出る ----------
RAYS = [((38, 36), (35, 17)), ((34, 35), (30, 19)), ((30, 35), (25, 22)), ((26, 36), (21, 25)), ((22, 37), (17, 29)), ((19, 39), (14, 33))]
def sail(up=0):
    rays = [((a, b), (c + up, d - up * 2)) for (a, b), (c, d) in RAYS]
    p = G()
    pts = [rays[0][0]]
    for i, (_, t) in enumerate(rays):
        pts.append((t[0], t[1] + 2))
        if i + 1 < len(rays):
            n = rays[i + 1][1]; pts.append(((t[0] + n[0]) // 2 - 1, (t[1] + n[1]) // 2 + 4))
    pts.append(rays[-1][0]); pts.append((30, 40))
    poly(p, pts, '1')
    s = shade(p, {'1': 'ABD'}, r=2, hi=.3, lo=-.25)
    # 膜の 下は 濃く（ひかえめな 市松）
    for y in range(64):
        for x in range(64):
            if s[y][x] in 'AB' and y > 31 and (x + y) % 2 == 0: s[y][x] = 'B' if s[y][x] == 'A' else 'D'
            if s[y][x] == 'B' and y > 34: s[y][x] = 'D'
    # 骨：鋼の 刃。先は 膜より つき出る
    for i, ((x0, y0), (x1, y1)) in enumerate(rays):
        q = G(); line(q, x0, y0, x1, y1, '1')
        for y in range(64):
            for x in range(64):
                if q[y][x] == '1':
                    s[y][x] = 'S' if (i == 0 or y < y1 + 4) else 'T'
                    if s[y][x + 1] in 'ABD' and i == 0: s[y][x + 1] = 'T'
                    elif s[y][x + 1] in 'ABD' and y < 34: s[y][x + 1] = 'U' if y > y1 + 3 else 'T'
    g = G(); ink(g, s)
    return g

# ---------- 尾びれ（三日月の 刃）----------
def tail(f=0):
    p = G()
    poly(p, [(15, 42), (11, 38), (7, 33), (4, 30 + f), (6, 35 + f), (9, 41), (11, 45)], '1')
    poly(p, [(11, 45), (9, 50), (6, 54), (4, 58 - f), (9, 55 - f), (12, 51), (15, 48)], '2')
    poly(p, [(10, 43), (15, 42), (15, 49), (10, 48)], '1')
    s = shade(p, {'1': 'ABD', '2': 'STU'}, r=1, hi=.3, lo=-.3)
    # 後ろの ふちは 刃（光る 線）
    for y in range(64):
        for x in range(64):
            if s[y][x] != '.' and at(s, x - 1, y) == '.' and y < 40: s[y][x] = 'S'
    dots(s, 'D', [(12, 44), (12, 45), (13, 46)])
    g = G(); ink(g, s)
    return g

# ---------- ひれ ----------
PEC = [
    'kkkkk....',
    'kSSTTkk..',
    '.kTTTUUkk',
    '..kkUUVVk',
    '....kkkVk',
    '.......kk',
]
PEC_B = [
    'kkkkkk...',
    'kSSTTUkkk',
    '.kkTTUUVk',
    '...kkkkkk',
]
ANAL = ['kkk...', 'kTUkk.', '.kUVVk', '..kkVk', '....kk']
DORS2 = ['..kk', '.kAk', 'kABk', 'kBDk']

# 目：かぶとの ひさしの 下、金の つり目に 赤い 奥
EYE = ['kkkkkk', '.kYYrk', '..kYrk', '...kk.']
EYE_ALT = {'blink': ['kkkkkk', '..kkkk', '......', '......'], 'atk0|atk1|atk2': ['kkkkkk', '.kYYYk', '..kYYk', '...kk.'],
           'hit': ['k...k.', '.k.k..', '..k...', '.k.k..'], 'ko': ['k...k.', '.k.k..', '..k...', '.k.k..']}
GLINT = ['...c...', '...S...', '..cSc..', 'cSSSSSc', '..cSc..', '...S...', '...c...']
SPEED = [
    'cCCCCCC.......',
    '..............',
    '....cCCCCCCCCC',
    '..............',
    '.cCCCCCCC.....',
    '..............',
    '......cCCCCCC.',
    '..............',
    '..cCCCCC......',
]
SPLASH = ['.c..c.', 'c.cC..', 'C.....', '......', '......', '......', 'C.....', 'c.cC..', '.c..c.']
WAKE_A = ['.c.', 'cCc', '.c.']

def layers():
    BODY = rows_of(body()); HEAD = rows_of(head_g()); HEAD_ATK = rows_of(head_g(True))
    SAIL = rows_of(sail()); SAIL_UP = rows_of(sail(1)); T0 = rows_of(tail()); T1 = rows_of(tail(1))
    return [
        dict(n='sail', g='sail', x=0, y=0, rows=SAIL, alt={'atk0|atk1|atk2': SAIL_UP}),
        dict(n='pecB', g='fin', x=37, y=53, rows=PEC_B),
        dict(n='tail', g='tail', x=0, y=0, rows=T0, alt={'idle1|idle2|walk1|walk3|atk1': T1}),
        dict(n='anal', g='body', x=22, y=53, rows=ANAL),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='head', g='head', x=0, y=0, rows=HEAD, alt={'atk1|atk2': HEAD_ATK}),
        dict(n='bill', g='head', x=47, y=37, rows=BILL, alt={'atk0|atk1': BILL_ATK}),
        dict(n='tsuba', g='head', x=47, y=40, rows=TSUBA),
        dict(n='eye', g='head', x=41, y=41, rows=EYE, alt=EYE_ALT),
        dict(n='pec', g='fin', x=31, y=48, rows=PEC),
        dict(n='glint', g='head', x=58, y=34, rows=GLINT, only='atk0'),
        dict(n='speed', g='root', x=-8, y=38, rows=SPEED, only='atk1|atk2'),
        dict(n='splash', g='head', x=65, y=34, rows=SPLASH, only='atk1'),
        dict(n='wake', g='root', x=56, y=56, rows=WAKE_A, only='idle1|idle3|walk1|walk3'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1), 'fin': (0, 1)}, 'walk1': {'root': (0, -1), 'sail': (-1, 0)}, 'walk2': {'tail': (0, 1), 'fin': (-1, 0)}, 'walk3': {'root': (0, -1)},
    'atk0': {'root': (-4, 0), 'tail': (0, -1), 'head': (0, 1)}, 'atk1': {'root': (8, 0)}, 'atk2': {'root': (11, 0), 'tail': (0, 1)},
    'hit': {'root': (-3, 1), 'head': (0, 1), 'tail': (0, -1), 'sail': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'sail': 'body', 'fin': 'body', 'tail': 'body', 'body': 'root'}
