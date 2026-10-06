# ユキノスグモ（こおり・むし × クモ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭胸部と 顔、小さな 腹、雪の 結晶の 枝の ついた 脚が 六方に 出る）
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
META = dict(id='yukinosugumo', name='ユキノスグモ', types=['ice', 'bug'], base='クモ', size='M')
import math
PAL = {
    'k': '#101018', 'l': '#1e1a40',
    'A': '#a2a8e6', 'B': '#5c60aa', 'C': '#2e2c64',      # 甲（明・中・暗）
    'c': '#f4ffff', 'i': '#a8e6ff', 'j': '#58a2dc',      # 氷の 結晶（白・水色・青）
    'R': '#ff5a6a', 'r': '#a01a34',                      # 目の 虹彩（明・暗）
    'w': '#ffffff',
}
LIGHT = set('Acw')
KEEP_BLACK = set('wR')
RAMP = {'1': 'ABC', '3': 'cij'}
DARK = {'c': 'i', 'i': 'j', 'A': 'B', 'B': 'C'}
HUB = (31, 41)

def vec(a): return math.cos(math.radians(a)), math.sin(math.radians(a))
# ---------- 結晶の 脚（見せ所）：まっすぐ 放射し、とちゅうに 雪の 結晶の 枝 ----------
def leg(a, L=24, far=False):
    ux, uy = vec(a); hx, hy = HUB
    P = lambda t: (hx + ux * t, hy + uy * t)
    def d(p):
        tube(p, [P(3), P(L * .55), P(L)], [2.2, 1.5, 1], '3')
        for t, b in ((L * .55, 6), (L * .8, 4)):                 # 雪の 結晶の 枝（±60度）
            x0, y0 = P(t)
            for sg in (1, -1):
                bx, by = vec(a + sg * 60)
                line(p, round(x0), round(y0), round(x0 + bx * b), round(y0 + by * b), '3')
    def post(s):
        x, y = map(round, P(L * .55)); s[y][x] = 'c'
        x, y = map(round, P(L * .8)); s[y][x] = 'c'
    def post2(g):
        x, y = map(round, P(L + 1.5))
        if 0 <= x < 64 and 0 <= y < 64: g[y][x] = 'w'
    return make(d, RAMP, r=1, hi=.15, lo=-.2, dk=DARK if far else None, post=post, post2=post2)
ANG = [(210, 'legB', True), (330, 'legA', True), (165, 'legA', False), (120, 'legB', False), (60, 'legA', False), (0, 'legB', False)]
LEN = {210: 24, 330: 24, 165: 24, 120: 20, 60: 20, 0: 23}

# ---------- 腹（小さく 丸い）：雪の 結晶の 模様 ----------
def abdomen():
    def d(p): ellipse(p, 21, 35, 8, 6.5, '1')
    def post(s):
        cx, cy = 20, 34
        for (dx, dy) in ((0, -4), (0, 4), (-4, -2), (4, 2), (-4, 2), (4, -2)):
            line(s, cx, cy, cx + dx, cy + dy, 'i')
        dots(s, 'c', [(cx, cy), (cx, cy - 4), (cx - 4, cy - 2), (cx - 4, cy + 2)])
    return make(d, RAMP, post=post)
# ---------- 頭胸部 ＋ 顔（大きい）----------
def head(open_=False):
    def d(p):
        ellipse(p, 37, 36, 10.5, 9.5, '1')
        poly(p, [(30, 28), (36, 24), (42, 25), (35, 30)], '1')               # 頭の 氷の とさか（つけ根）
    def post(s):
        # 小さい 目（2つ）と 甲の みぞ
        for (x, y) in ((39, 28), (42, 29)): s[y][x] = 'k'; s[y][x + 1] = 'R'
        line(s, 30, 33, 33, 41, 'C')
        # 口：きば（鋏角）
        if open_:
            put(s, ['kkkkkkk', 'krrrrrk', 'krrrrrk', 'kkrrrkk'], 40, 40)
    def post2(g):
        # 下へ 曲がった 2本の きば
        if open_:
            put(g, ['kwwk...kwwk', '.kwwk...kwwk', '..kwwk...kwwk', '...kwk....kwk', '....kk.....kk'], 37, 44)
        else:
            put(g, ['kkkk.kkkk', 'kwwk.kwwk', '.kwwk.kwwk', '.kwwk.kwwk', '..kwk..kwk', '...kk...kk'], 39, 43)
    return make(d, RAMP, lo=-.34, post=post, post2=post2)
def crest():
    """頭の 上の 氷の とさか（六角の 結晶）"""
    def d(p): poly(p, [(31, 29), (32, 20), (35, 17), (37, 22), (40, 18), (41, 27)], '3')
    def post(s): line(s, 33, 21, 33, 28, 'c'); line(s, 39, 20, 39, 26, 'j')
    return make(d, RAMP, r=1, hi=.1, lo=-.2, post=post)
# 目：甲の まゆ＋白い 光＋赤い 虹彩（明 R・暗 r）＋たての ひとみ
EYE = ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwRRkRRk', '.kwRRrkrRk', '.kRrrrkrrk', '..krrkkrk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAAAAAAAk', '.kkkkkkkkk', '.kBBBBBBBk', '..kBBBBBk.', '...kkkkk..'],
    'hit':   ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kkkAAAAkk', '.kAAkkkkAk', '.kBBBBBkkk', '..kkkBBBk.', '...kkkkk..'],
    'atk0|atk1|atk2': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwwRkRwk', '.kwRRRkRRk', '.kRRRRkRRk', '..krrkkrk.', '...kkkkk..'],
    'ko':    ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAkAAAkAk', '.kAAkAkAAk', '.kBkBBBkBk', '..kBBBBBk.', '...kkkkk..'],
}
# 氷の 糸・つぶて（はなれているのは 意図的：エフェクト）
ICE = ['c...i....', '.i.c..i..', '..cwc....', 'i.wwwci.c', '..cwc....', '.i.c..i..', 'c...i....']
SNOW = ['.i.', 'iwi', '.i.']

def layers():
    lay = []
    for n, (a, g, far) in enumerate(ANG):
        lay.append(dict(n='leg%d' % n, g=g, x=0, y=0, rows=leg(a, LEN[a], far),
                        alt={'atk1|atk2': leg(a - 25, LEN[a], far)} if a in (330, 0) else None))
        if n == 1: lay.append(dict(n='abd', g='body', x=0, y=0, rows=abdomen()))
    lay += [
        dict(n='crest', g='head', x=0, y=0, rows=crest()),
        dict(n='head', g='head', x=0, y=0, rows=head(), alt={'atk1|atk2': head(True)}),
        dict(n='eye', g='head', x=36, y=30, rows=EYE, alt=EYE_ALT),
        dict(n='ice', g='fx', x=54, y=36, rows=ICE, only='atk1'),
        dict(n='ice2', g='fx', x=58, y=34, rows=SNOW, only='atk0|atk2'),
        dict(n='snow', g='fx', x=8, y=10, rows=SNOW, only='idle1|idle2'),
    ]
    # ふつうの 位置に 足を 並べかえ（手前の 足を 頭の 前に）
    return lay
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'head': (0, 1), 'body': (0, 1)}, 'idle3': {'body': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'head': (0, -1), 'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'head': (0, -1), 'body': (0, -1)},
    'atk0': {'root': (-3, 1), 'head': (-1, 1)},
    'atk1': {'root': (3, -1)},
    'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
