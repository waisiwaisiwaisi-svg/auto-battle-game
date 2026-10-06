# デントウイカ（でんき・みず × イカ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 目、小さな とがった 胴（外とう膜）、短い 腕、電線の 長い 触腕 2本）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり → 左上光の 陰影 → 輪郭）。仕上げの 目・牙・模様は 手で 打つ ----------
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < N and 0 <= x < N: g[y][x] = ch
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g
def tube(p, path, rad, ch):
    """太さの かわる 管（手足・首・尾の あたり）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < N and 0 <= y < N and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def ink(p, ch='k'):
    """まわりに 1ドットの 輪郭"""
    g = G()
    for y in range(N):
        for x in range(N):
            if p[y][x] != '.': g[y][x] = p[y][x]
            elif any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = ch
    return g
def shade(p, ramps, r=2, hi=.3, lo=-.28):
    """左上から 光：ふくらみの 向きで 明・中・暗、上と 左の ふちは 明（三日月）、下と 右の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(N)] for y in range(N)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1): n += 1; s += m[yy][xx] if 0 <= yy < N and 0 <= xx < N else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(N):
        for x in range(N):
            c = p[y][x]
            if c not in ramps: continue
            h, md, d = ramps[c]
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5
            out[y][x] = h if v > hi else d if v < lo else md
            if at(p, x, y - 1) == '.' or at(p, x - 1, y) == '.': out[y][x] = h
            if at(p, x, y + 1) == '.' or at(p, x + 1, y) == '.': out[y][x] = d
    return out
def recol(g, mp): return [[mp.get(c, c) for c in r] for r in g]
def make(draw, ramps, r=2, hi=.3, lo=-.28, post=None, post2=None, dk=None):
    """draw(p) で あたり → 陰影 → post(s) 手打ち → 輪郭 → post2(g) 手打ち"""
    p = G(); draw(p); s = shade(p, ramps, r, hi, lo)
    if post: post(s)
    if dk: s = recol(s, dk)
    g = ink(s)
    if post2: post2(g)
    return rows_of(g)
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < N and 0 <= y + dy < N: g[y + dy][x + dx] = c
    return rows_of(g)
def over(*rowsets):
    g = G()
    for rs in rowsets: stamp(g, rs, 0, 0)
    return rows_of(g)
EYE_BOX = (32, 23, 11, 9)
META = dict(id='dentouika', name='デントウイカ', types=['elec', 'water'], base='イカ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c2448',
    'A': '#a4e0f4', 'B': '#4c90cc', 'C': '#283e7c',      # からだ（明・中・暗）
    'D': '#58587a', 'H': '#2c2c44',                      # 電線の 被覆（中・暗）
    'E': '#eeeadc',                                      # がいし（白い 輪）
    'Y': '#fff062', 'O': '#f0a020',                      # 電気（目の 虹彩も）
    'R': '#a02840',                                      # 口の 中
    'w': '#ffffff',
}
LIGHT = set('AEYw')
KEEP_BLACK = set('wYO')
RAMP = {'1': 'ABC', '4': 'DDH', '5': 'EED'}
DARK = {'A': 'B', 'B': 'C', 'D': 'H', 'E': 'D'}

# ---------- 胴（外とう膜：小さく とがる。先に ひれ）----------
def mantle():
    def d(p):
        poly(p, [(24, 33), (39, 26), (32, 17), (16, 5), (19, 20)], '1')               # とがった 胴（円すい）
        poly(p, [(13, 1), (29, 6), (25, 12), (20, 13), (8, 17), (9, 9)], '1')          # 先の ひし形の ひれ（矢じり）
    def post(s):
        # 電気の すじ（背の 発光線）
        line(s, 27, 26, 18, 11, 'O'); line(s, 26, 26, 17, 11, 'Y')
        line(s, 20, 13, 28, 7, 'C'); line(s, 18, 13, 9, 16, 'C')
        for (x, y) in ((22, 22), (30, 20), (20, 25)): s[y][x] = 'A' if s[y][x] != '.' else '.'
    return make(d, RAMP, post=post)
# ---------- 頭（大きい）：目と 口。下に 短い 腕 ----------
def head(open_=False):
    def d(p): ellipse(p, 35, 32, 11, 9, '1')
    def post(s):
        if open_: put(s, ['kkkkkkk', 'kwRRwRw', 'kRRRRRR', 'kwRRwRw', '.kkkkkk'], 39, 33)
        else:
            put(s, ['..kkkkk', '.kwkwkw', '..w..w.'], 39, 34)
        dots(s, 'Y', [(29, 36), (31, 37), (27, 34)])                       # 発光点
    return make(d, RAMP, lo=-.34, post=post)
def arm(path, far=False):
    return make(lambda p: tube(p, path, [2.8, 2.2, 1.6, 1][:len(path)], '1'), RAMP, r=1, dk=DARK if far else None)
ARMS = [
    ([(28, 38), (25, 46), (24, 51), (27, 53)], True),
    ([(40, 38), (44, 45), (47, 49), (50, 48)], True),
    ([(31, 39), (30, 47), (31, 52), (34, 53)], False),
    ([(36, 39), (38, 47), (41, 51), (44, 50)], False),
]
# ---------- 電線の 触腕（見せ所）：がいしの 輪＋先に 電極の こぶ ----------
def cable(path, end, far=False, hot=False):
    def d(p):
        tube(p, path, [2.2] * len(path), '4')
        ex, ey = end; ellipse(p, ex, ey, 3.6, 3.6, '5')
    def post(s):
        # がいしの 輪（白）を 4ドットおきに
        n = 0
        for i in range(len(path) - 1):
            (x0, y0), (x1, y1) = path[i], path[i + 1]
            m = max(abs(x1 - x0), abs(y1 - y0))
            for j in range(m):
                n += 1
                if n % 5 == 0:
                    x, y = round(x0 + (x1 - x0) * j / m), round(y0 + (y1 - y0) * j / m)
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if s[y + dy][x + dx] in 'DH': s[y + dy][x + dx] = 'E' if dx + dy < 0 else 'D'
        ex, ey = end
        for (dx, dy) in ((0, 0), (-1, 0), (0, -1), (1, 0)): s[ey + dy][ex + dx] = 'Y'
        s[ey + 1][ex] = 'O'; s[ey][ex + 1] = 'O' if not hot else 'Y'
        if hot: s[ey - 1][ex - 1] = 'w'
    return make(d, RAMP, r=1, dk=DARK if far else None, post=post)
C1 = ([(41, 40), (49, 46), (56, 48), (61, 43)], (61, 39))
C1A = ([(41, 40), (48, 40), (55, 37), (59, 32)], (60, 28))
C2 = ([(29, 40), (22, 49), (16, 53), (11, 50)], (9, 46))
# 目：よこ瞳（G）。イカの W形の 黒い 瞳。広い 電気の 虹彩（明 Y・暗 O）、ななめの まゆ線
B2 = ['kk.........', '.kkkkk.....', '..kkkkkkkk.']
EYE = B2 + ['.kwYYYYYYYk', 'kYkkYYYkkYk', 'kYkkkYkkkYk', 'kOOkkkkkOOk', '.kOOOkOOOk.', '..kkkkkkk..']
EYE_ALT = {
    'blink': B2 + ['.kAAAAAAAAk', 'kAAAAAAAAAk', 'kkkkkkkkkkk', 'kBBBBBBBBBk', '.kBBBBBBBk.', '..kkkkkkk..'],
    'hit':   B2 + ['.kAAAAAAAAk', 'kkkkkkkkkkk', 'kYYkYYYkYYk', 'kOOOkkkOOOk', '.kkOOOOOkk.', '..kkkkkkk..'],
    'atk0|atk1|atk2': B2 + ['.kwwwYYYYYk', 'kwYYYYYYYYk', 'kYkYYYYYkYk', 'kYkkYkYkkYk', '.kOOkkkOOk.', '..kkkkkkk..'],
    'ko':    B2 + ['.kAkAAAAkAk', 'kAAAkAAkAAk', 'kAAAAkkAAAk', 'kBBBkBBkBBk', '.kBkBBBBkk.', '..kkkkkkk..'],
}
# 放電（はなれているのは 意図的：電気の エフェクト）
ZAP = ['..Y...', '.YO..Y', 'Y..YO.', '..Y..O', '.O..Y.']
ZAP2 = ['Y...Y..', '.Y.Y.Y.', '..YwY..', 'YYwwwYY', '..YwY..', '.Y.Y.Y.', 'Y...Y..']
BOLT = ['......YY', '....YYO.', '..YwY...', 'YYO.....', '..YY....', '....YO..']

def layers():
    H = head(); HO = head(True)
    return [
        dict(n='c2', g='legB', x=0, y=0, rows=cable(*C2, far=True), alt={'atk1|atk2': cable(*C2, far=True, hot=True)}),
        *[dict(n='armF%d' % i, g='legB', x=0, y=0, rows=arm(p, True)) for i, (p, f) in enumerate(ARMS) if f],
        dict(n='mantle', g='body', x=0, y=0, rows=mantle()),
        *[dict(n='arm%d' % i, g='legA', x=0, y=0, rows=arm(p)) for i, (p, f) in enumerate(ARMS) if not f],
        dict(n='head', g='head', x=0, y=0, rows=H, alt={'atk1|atk2': HO}),
        dict(n='eye', g='head', x=32, y=23, rows=EYE, alt=EYE_ALT),
        dict(n='c1', g='cable', x=0, y=0, rows=cable(*C1), alt={'atk1|atk2': cable(*C1A, hot=True), 'atk0': cable(*C1, hot=True)}),
        dict(n='zap', g='cable', x=58, y=31, rows=ZAP, only='idle1|idle3|walk1|walk3'),
        dict(n='zap2', g='cable', x=57, y=24, rows=ZAP2, only='atk1'),
        dict(n='bolt', g='cable', x=56, y=22, rows=BOLT, only='atk2'),
        dict(n='zap3', g='legB', x=4, y=38, rows=ZAP, only='idle2|walk2|atk0'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'legA': (0, 1)}, 'idle2': {'head': (0, 1), 'body': (0, 1), 'legA': (0, 1), 'cable': (0, 1)}, 'idle3': {'body': (0, 1)}, 'blink': {},
    'walk0': {'root': (0, -1), 'legA': (1, 0)}, 'walk1': {'root': (0, -2), 'legB': (-1, 1)},
    'walk2': {'root': (0, -1), 'legA': (-1, 1)}, 'walk3': {'legB': (1, 0)},
    'atk0': {'root': (-2, 1), 'cable': (-1, 0)},
    'atk1': {'root': (2, -1)},
    'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'cable': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'cable': 'head', 'body': 'root', 'legA': 'head', 'legB': 'head'}
