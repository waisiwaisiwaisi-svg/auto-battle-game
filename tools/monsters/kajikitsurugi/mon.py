# カジキツルギ（はがね・みず × カジキ）手打ち GBA風・デフォルメ（2〜3頭身：かぶとの 頭を 大きく、胴は 短く 丸く。帆の 背びれと 剣の くちばしは 大きい まま）
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
# 胴は 短く 丸く（元の 形を 横に 0.62倍）
def CX(x): return round(20 + (x - 12) * .62)
BODY_PTS = [(CX(x), y) for x, y in [(48, 42), (45, 37), (39, 34), (31, 33), (24, 34), (18, 37), (14, 41), (12, 44), (12, 47), (15, 50), (21, 53), (28, 56), (35, 56), (41, 54), (45, 51), (48, 47)]]
def belly_y(x): return 46 - (1 if x < 24 else 0)
def body():
    p = G(); poly(p, BODY_PTS, '1')
    for y in range(64):
        for x in range(64):
            if p[y][x] == '1' and y > belly_y(x): p[y][x] = '2'
    s = shade(p, {'1': 'ABD', '2': 'STU'}, r=2, hi=.3, lo=-.25, ybias=(44, .035))
    # 腹の 鋼の うろこ：ずらして 重ねた 弧（下の ふちが 影、左上が 光）を 手で 打つ
    DK = {'S': 'T', 'T': 'U', 'U': 'V', 'V': 'V'}; LT = {'T': 'S', 'U': 'T', 'V': 'U', 'S': 'S'}
    for row, cy in enumerate((48, 51, 54)):
        for cx in range(21 + (2 if row % 2 else 0), 44, 4):
            for (dx, dy) in ((-2, 0), (-1, 1), (0, 1), (1, 1), (2, 0)):
                x, y = cx + dx, cy + dy
                if p[y][x] == '2' and y > belly_y(x): s[y][x] = DK[s[y][x]]
            x, y = cx - 1, cy - 1
            if p[y][x] == '2' and y > belly_y(x) + 1: s[y][x] = LT[s[y][x]]
    # 背と 腹の さかい：側線（青の 濃い線 → 鋼の 光）
    for x in range(20, 43):
        y = belly_y(x)
        if s[y][x] in 'ABD': s[y][x] = 'D'
        if s[y + 1][x] in 'STUV': s[y + 1][x] = 'S'
    # 背の 鎧の 板（よろいの さね）：後ろへ そった すじ
    for x0 in (27, 32):
        for i in range(0, 10):
            x, y = x0 - i // 3, 36 + i
            if p[y][x] == '1' and s[y][x] in 'ABD':
                s[y][x] = 'D'
                if s[y][x + 1] in 'BD': s[y][x + 1] = 'A' if i < 5 else 'B'
    # 背の 光の すじ（手で）
    dots(s, 'A', [(29, 35), (30, 35), (25, 36), (24, 37), (34, 35), (22, 39), (21, 40)])
    g = G(); ink(g, s)
    return g

# ---------- えら（鋼の かぶとの ほお当て）と 頭 ----------
def head_g(atk=False):
    """大きな 頭（よこ 20 × たて 24）：かぶと＋ほお当て"""
    g = G()
    # ほお当て：鋼の 板
    p = G(); poly(p, [(35, 39), (48, 39), (54, 43), (54, 50), (50, 54), (42, 56), (36, 52)], '2')
    s = shade(p, {'2': 'TUV'}, r=1, hi=.3, lo=-.3); ink(g, s)
    # かぶと：ひさしが 目の 上に 張り出し、後ろへ 角が のびる
    p = G(); poly(p, [(35, 35), (41, 31), (49, 32), (54, 36), (56, 41), (51, 40), (45, 40), (38, 42), (33, 41), (29, 37)], '2')
    s = shade(p, {'2': 'STU'}, r=1, hi=.25, lo=-.25); ink(g, s)
    # かぶとの 鋲・板の すじ・ひさしの 下の 影（手で）
    dots(g, 'V', [(37, 36), (38, 37), (39, 38), (40, 39), (33, 38)])
    dots(g, 'S', [(36, 35), (41, 33), (42, 33), (43, 33), (44, 33), (32, 37)])
    dots(g, 'S', [(37, 44), (37, 45), (38, 43)]); dots(g, 'V', [(44, 46), (47, 46), (50, 46), (44, 53), (47, 54)])   # ほお当ての 光と 鋲
    dots(g, 'U', [(46, 41), (47, 41), (48, 41), (49, 41), (50, 41), (51, 41)])
    dots(g, 'Y', [(48, 36)]); dots(g, 'O', [(48, 37)])
    # 口：深く 切れこむ 線と 牙
    if atk:
        for x in range(44, 55): g[49][x] = 'k'
        for x in range(46, 55): g[50][x] = 'r'; g[51][x] = 'r'
        for x in range(45, 54): g[52][x] = 'k'
        dots(g, 'S', [(48, 50), (51, 50), (47, 51), (50, 51)])
    else:
        for x in range(45, 55): g[50][x] = 'k'
        dots(g, 'S', [(47, 51), (50, 51), (52, 51)]); dots(g, 'k', [(44, 49)])
    # えらの 切れめ（後ろの ふち）
    dots(g, 'V', [(39, 45), (39, 46), (40, 47), (40, 48), (41, 50), (41, 51)])
    return g

# ---------- 剣の くちばし（刀）と つば：上の ふちが 光る 刃、下は 刃文 ----------
BILL = [
    '......kkkkkkkkk.',
    'kkkkkkSSSSSSSSSk',
    'SSSSSSSTTTTTTkk.',
    'TTcTTTTUUUkkk...',
    'UUUUUVkkkk......',
    'kkkkkkk.........',
]
BILL_ATK = [BILL[0], BILL[1], 'SSSSSSSSSSSSSkk.', 'TTcTTTTTTTkkk...'] + BILL[4:]
TSUBA = ['kkk', 'YOk', 'YVk', 'OVk', 'YOk', 'OOk', 'kkk']

# ---------- 帆の 背びれ：鋼の 骨が 刃の ように つき出る ----------
RAYS = [((36, 34), (34, 15)), ((33, 34), (29, 17)), ((30, 34), (24, 20)), ((27, 35), (20, 24)), ((24, 37), (17, 28)), ((22, 39), (15, 33))]
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
    p = G(); D = 7   # 胴が 短く なった ぶん 前へ（根もとは 胴の 中へ 3ドット）
    poly(p, [(x + D, y) for x, y in [(15, 42), (12, 38), (9, 33), (6, 30 + f), (8, 35 + f), (10, 41), (11, 45)]], '1')
    poly(p, [(x + D, y) for x, y in [(11, 45), (10, 50), (8, 54), (6, 58 - f), (10, 55 - f), (13, 51), (15, 48)]], '2')
    poly(p, [(x + D, y) for x, y in [(10, 43), (18, 42), (18, 50), (10, 48)]], '1')
    s = shade(p, {'1': 'ABD', '2': 'STU'}, r=1, hi=.3, lo=-.3)
    # 後ろの ふちは 刃（光る 線）
    for y in range(64):
        for x in range(64):
            if s[y][x] != '.' and at(s, x - 1, y) == '.' and y < 40: s[y][x] = 'S'
    dots(s, 'D', [(19, 44), (19, 45), (20, 46)])
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
# 目：ひさしの 下の 金の つり目。光 S＋虹彩 2色（Y／O）＋たての ひとみ＋赤い 奥＋下まぶた
EYE = ['kkkkkkkk.', '.kSSYYkrk', '.kSYYYkrk', '..kOOOkrk', '...kkkkk.']
EYE_ALT = {'blink': ['kkkkkkkk.', '.kkkkkkkk', '..UUUUUU.', '...UUUU..', '.........'],
           'atk0|atk1|atk2': ['kkkkkkkk.', '.kSSYYkYk', '.kSYYYkYk', '..kYYYkYk', '...kkkkk.'],
           'hit': ['kkkkkkkk.', '..kk..kk.', '....kk...', '..kk..kk.', '.........'],
           'ko': ['.........', '.kT...kT.', '..kT.kT..', '...kTT...', '..kT.kT..']}
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
        dict(n='tail', g='tail', x=0, y=0, rows=T0, alt={'idle1|idle2|walk1|walk3|atk1': T1}),
        dict(n='anal', g='body', x=26, y=54, rows=ANAL),
        dict(n='body', g='body', x=0, y=0, rows=BODY),
        dict(n='head', g='head', x=0, y=0, rows=HEAD, alt={'atk1|atk2': HEAD_ATK}),
        dict(n='bill', g='head', x=54, y=41, rows=BILL, alt={'atk0|atk1': BILL_ATK}),
        dict(n='tsuba', g='head', x=53, y=41, rows=TSUBA),
        dict(n='eye', g='head', x=40, y=40, rows=EYE, alt=EYE_ALT),
        dict(n='pec', g='fin', x=36, y=50, rows=PEC),
        dict(n='glint', g='head', x=64, y=38, rows=GLINT, only='atk0'),
        dict(n='speed', g='root', x=-2, y=38, rows=SPEED, only='atk1|atk2'),
        dict(n='splash', g='head', x=70, y=38, rows=SPLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'tail': (0, 1)}, 'idle3': {'tail': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1), 'fin': (0, 1)}, 'walk1': {'root': (0, -1), 'sail': (-1, 0)}, 'walk2': {'tail': (0, 1), 'fin': (-1, 0)}, 'walk3': {'root': (0, -1)},
    'atk0': {'root': (-4, 0), 'tail': (0, -1), 'head': (0, 1)}, 'atk1': {'root': (8, 0)}, 'atk2': {'root': (11, 0), 'tail': (0, 1)},
    'hit': {'root': (-3, 1), 'head': (0, 1), 'tail': (0, -1), 'sail': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'sail': 'body', 'fin': 'body', 'tail': 'body', 'body': 'root'}
