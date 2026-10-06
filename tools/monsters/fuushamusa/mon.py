# フウシャムサ（かぜ・ノーマル × ムササビ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭、小さな 胴、短い 手足の 先に 風車の 羽根の 膜）
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
META = dict(id='fuushamusa', name='フウシャムサ', types=['wind', 'normal'], base='ムササビ', size='M')
import math
PAL = {
    'k': '#101018', 'l': '#3e2a26',
    'A': '#f2d8a6', 'B': '#c48c58', 'C': '#7c4e32',      # 毛（明・中・暗）
    'D': '#f8f4e4', 'E': '#b4a07c',                      # 膜（帆布の 色：明・暗）
    'c': '#e0fff6', 'm': '#6ad6bc', 'T': '#23806e',      # 風（白・みどり・濃い みどり）＝目の 虹彩も
    'R': '#a02838',                                      # 口の 中
    'w': '#ffffff',
}
LIGHT = set('ADcw')
KEEP_BLACK = set('wcm')
RAMP = {'1': 'ABC', '2': 'DDE'}
DARK = {'A': 'B', 'B': 'C', 'D': 'E'}
HUB = (29, 36)

def vec(a): return math.cos(math.radians(a)), math.sin(math.radians(a))
def blade(a, L=24, w=12):
    """風車の 羽根 ＝ 手足の あいだに 張った 四角い 膜。前の ふちは 手足の 骨、うしろに 帆の 格子"""
    ux, uy = vec(a); vx, vy = -uy, ux; hx, hy = HUB
    P = lambda t, s: (round(hx + ux * t + vx * s), round(hy + uy * t + vy * s))
    def d(p): poly(p, [P(4, 0), P(L, 0), P(L, w), P(8, w * .7)], '2')
    def post(s):
        for t in (11, 16, 21):          # 帆の 格子（よこ）
            line(s, *P(t, 1), *P(t, w - 1), 'E')
        line(s, *P(10, w // 2), *P(L - 1, w // 2), 'E')
    return make(d, RAMP, r=1, post=post)
def limb(a, L=24):
    ux, uy = vec(a); hx, hy = HUB
    P = lambda t: (hx + ux * t, hy + uy * t)
    def d(p):
        tube(p, [P(2), P(L * .5), P(L)], [2.8, 2, 1.6], '1')
    def post2(g):
        # 先の かぎ爪（白）
        x, y = map(round, P(L + 1.5)); x2, y2 = map(round, P(L + 2.5))
        for (xx, yy) in ((x, y), (x2, y2)):
            if 0 <= xx < 64 and 0 <= yy < 64: g[yy][xx] = 'w'
        for (xx, yy) in ((x2 + 1, y2), (x2, y2 + 1), (x2 - 1, y2), (x2, y2 - 1)):
            if 0 <= xx < 64 and 0 <= yy < 64 and g[yy][xx] == '.': g[yy][xx] = 'k'
    return make(d, RAMP, r=1, post2=post2)
ANG = (225, 315, 45, 135)        # 風車の 向き（ふだん：×）
ANG2 = (270, 0, 90, 180)         # まわった 向き（攻撃：＋）

def body():
    def d(p):
        ellipse(p, 29, 37, 7, 7.5, '1')
        tube(p, [(29, 42), (29, 47), (30, 51)], [3, 4, 3.2], '1')       # 平たい しっぽ（短く）
    def post(s):
        for y in range(36, 44):
            for x in range(27, 32):
                if s[y][x] == 'B' and (x + y) % 3: s[y][x] = 'A'      # おなかの 白い 毛
        dots(s, 'C', [(31, 50), (32, 52), (27, 51)])
    return make(d, RAMP, post=post)
def head(open_=False):
    def d(p):
        ellipse(p, 29, 22, 10.5, 9, '1')
        poly(p, [(34, 18), (42, 21), (43, 24), (38, 29), (32, 29)], '1')      # 鼻づら（右むき）
        poly(p, [(20, 16), (20, 8), (26, 14)], '1')                          # 耳（とがった 房）
        poly(p, [(27, 14), (31, 7), (34, 15)], '1')
    def post(s):
        line(s, 21, 9, 22, 14, 'C'); line(s, 31, 8, 31, 14, 'C')
        for (x, y) in ((33, 27), (34, 28), (35, 28), (36, 28), (37, 27), (32, 26), (22, 26), (21, 25), (23, 27)): s[y][x] = 'A'
        dots(s, 'k', [(42, 21), (42, 22)])
        if open_:
            put(s, ['kkkkkk', 'kRRRRk', 'kRRRRR', 'kkkkkk'], 37, 24)
            dots(s, 'w', [(41, 25), (41, 26), (40, 25)])
        else:
            line(s, 35, 26, 42, 24, 'k')
            dots(s, 'w', [(40, 25), (41, 25), (40, 26), (38, 26), (38, 27)]); dots(s, 'C', [(41, 26), (39, 27), (37, 27)])
    return make(d, RAMP, lo=-.34, post=post)
# 目：まゆの 毛＋白い 光＋風色の 虹彩（明 m・暗 T）＋たての ひとみ
EYE = ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwmmkmmk', '.kwmmTkTmk', '.kmTTTkTTk', '..kTTkkTk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAAAAAAAk', '.kkkkkkkkk', '.kBBBBBBBk', '..kBBBBBk.', '...kkkkk..'],
    'hit':   ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kkkAAAAkk', '.kAAkkkkAk', '.kBBBBBkkk', '..kkkBBBk.', '...kkkkk..'],
    'atk0|atk1|atk2': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwwckcwk', '.kwcccmccm', '.kmmmmkmmk', '..kTTkkTk.', '...kkkkk..'],
    'ko':    ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kBkBBBkBk', '.kBBkBkBBk', '.kBkBBBkBk', '..kBBBBBk.', '...kkkkk..'],
}
# 風（はなれているのは 意図的：風の すじ）
WIND1 = ['..cccc.....', '.c....mm...', 'c.......m..', '.........m.', '.mmm.....m.', 'm...m...m..', '.....mmm...']
WIND2 = ['...cc....', '.cc..m...', 'c.....m..', '......m..', '..mmmm...']
GUST = ['....cccccc..', '..cc......c.', 'cc..mmmmm..c', '..mm.....m.c', 'mm..ccc..m..', '...c...cm...', '....mmm.....']

def layers():
    BL = {a: blade(a) for a in ANG + ANG2}; LM = {a: limb(a) for a in ANG + ANG2}
    lay = []
    for i, (a, a2) in enumerate(zip(ANG, ANG2)):
        g = 'legA' if i % 2 else 'legB'
        lay.append(dict(n='bl%d' % i, g=g, x=0, y=0, rows=BL[a], alt={'atk1|walk1|walk3': BL[a2]}))
    for i, (a, a2) in enumerate(zip(ANG, ANG2)):
        g = 'legA' if i % 2 else 'legB'
        lay.append(dict(n='lm%d' % i, g=g, x=0, y=0, rows=LM[a], alt={'atk1|walk1|walk3': LM[a2]}))
    H = head(); HO = head(True)
    lay += [
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='head', g='head', x=0, y=0, rows=H, alt={'atk1|atk2': HO}),
        dict(n='eye', g='head', x=27, y=14, rows=EYE, alt=EYE_ALT),
        dict(n='wind', g='fx', x=1, y=26, rows=WIND1, only='idle1|idle3|walk1|walk3'),
        dict(n='wind2', g='fx', x=50, y=28, rows=WIND2, only='idle2|walk2'),
        dict(n='gust', g='fx', x=48, y=20, rows=GUST, only='atk1|atk2'),
    ]
    return lay
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'legA': (0, 1)}, 'idle3': {'legB': (0, 1)}, 'blink': {},
    'walk0': {'root': (0, -1), 'legA': (1, 0)}, 'walk1': {'root': (0, -2), 'legB': (0, 1)},
    'walk2': {'root': (0, -1), 'legA': (-1, 0)}, 'walk3': {'legB': (0, -1)},
    'atk0': {'root': (-3, 1), 'head': (-1, 1), 'legA': (1, 1), 'legB': (1, -1)},
    'atk1': {'root': (3, 0)},
    'atk2': {'root': (5, 0), 'legA': (-1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'legA': 'body', 'legB': 'body', 'body': 'root', 'fx': 'root'}
