# トンボギリ（かくとう・むし × トンボ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：薙刀（なぎなた）に なった 細長い 腹。先が 反った 鋼の 刃
import os, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='tonbogiri', name='トンボギリ', types=['fighting', 'bug'], base='トンボ', size='M')
PAL = {
    'k': '#101018', 'l': '#3e1418',
    'A': '#ff7c5c', 'B': '#c63a30', 'D': '#6a1a22',      # 赤い 体
    'Y': '#ffe27a', 'O': '#c88a24',                      # 金の 輪（はばき）
    'g': '#a6f6c6', 'G': '#2a9a76',                      # 複眼（明・暗）
    'S': '#f4f8ff', 'T': '#a6b2ca', 'U': '#566080',      # 鋼の 刃
    'c': '#dcf6ff', 'C': '#80bce4',                      # はね
    'w': '#ffffff',
}
LIGHT = set('AYgScw')
KEEP_BLACK = set('wgYS')
RAMP = {'1': 'ABD', '3': 'YOO', '5': 'STU'}

# ---------- はね（細長い 2枚。すじと ディザで すける 膜）----------
WINGS = {
    0: ([(36, 28), (34, 17), (32, 8), (35, 7), (38, 14), (39, 27)], [(32, 29), (25, 18), (18, 11), (20, 8), (27, 13), (35, 27)]),
    1: ([(36, 28), (37, 17), (38, 9), (41, 9), (41, 16), (39, 28)], [(32, 29), (22, 21), (14, 16), (15, 13), (24, 16), (35, 27)]),
    2: ([(36, 28), (30, 19), (24, 13), (27, 11), (34, 17), (39, 27)], [(32, 29), (21, 25), (13, 23), (14, 20), (23, 21), (35, 27)]),
}
@lru_cache(None)
def wing(ph=0, which=0):
    pts = WINGS[ph][which]
    g = G(); poly(g, pts, 'c')
    for Y in range(H):
        for X in range(W):
            if g[Y][X] != 'c': continue
            e = g[Y + 1][X] == '.' or g[Y][X + 1] == '.'
            g[Y][X] = 'C' if e or (X + Y) % 2 == 0 and (Y - MY) > 14 else 'c'
    # 前の ふちの 太い すじ と 縁紋（えんもん）
    x0, y0 = pts[0]; x1, y1 = pts[2]
    from pix import line as L
    L(g, x0 + MX, y0 + MY - 1, x1 + MX, y1 + MY + 1, 'U')
    put(g, (x1 + x0 * 3) // 4 + (x1 - x0) // 2, (y1 + y0 * 3) // 4 + (y1 - y0) // 2, 'D')
    return Part(ink(g), [(28, 25, 42, 31)])

# ---------- 胸（小さく 丸い）と 頭（大きな 複眼）----------
@lru_cache(None)
def thorax():
    def d(g): ell(g, 35, 34, 7.5, 7, '1')
    def p(g):
        dots(g, 'D', [(33, 33), (34, 34), (35, 35), (38, 31), (39, 32)])        # 胸の すじ
        dots(g, 'Y', [(31, 29), (32, 29)])
    return part(d, RAMP, p, r=2, tilt=.6)

EYES = {   # 複眼の 中に するどい 目：光（w）＋ 明・暗の 緑 ＋ たての ひとみ。上に まゆの ひさし（前へ 下がる）
    'open': ['kk.........', '.kkkk......', '..kgkkkkk..', '.kgwwggGGk.', '.kgwgkkGGk.', '.kggGkkGGk.', '.kgGGGGGGk.', '..kGGGGGk..', '...kkkkk...'],
    'atk':  ['kk.........', '.kkkk......', '..kgkkkkk..', '.kwwwwggGk.', '.kgwwkkgGk.', '.kggwkkGGk.', '.kgGGGGGGk.', '..kGGGGGk..', '...kkkkk...'],
    'blink': ['kk.........', '.kkkk......', '..kgkkkkk..', '.kgGGGGGGk.', '.kkkkkkkkk.', '.kGGGGGGGk.', '.kGGGGGGGk.', '..kGGGGGk..', '...kkkkk...'],
    'hit':  ['...........', '.kkk...kk..', '..kgk.kkk..', '.kgGkkGGGk.', '.kkkkkkkkk.', '.kgGkkGGGk.', '.kgk..kGGk.', '..kGGGGGk..', '...kkkkk...'],
    'ko':   ['...........', '...kkkkk...', '..kgggGGk..', '.kgkGGGkGk.', '.kgGkGkGGk.', '.kgGGkGGGk.', '.kgGkGkGGk.', '..kkGGGkk..', '...kkkkk...'],
}
@lru_cache(None)
def head(eye='open', bite=False):
    def d(g):
        ell(g, 47, 29, 8.5, 8.5, '1')
        poly(g, [(52, 33), (57, 33), (57, 36), (53, 38)], '1')                 # 口もと
    def p(g):
        stamp(g, 44, 20, EYES[eye])
        dots(g, 'D', [(41, 33), (42, 34), (44, 35), (46, 36)])
        # 大あご（白い きば 2本、かみつきで ひらく）
        if bite: stamp(g, 54, 32, ['kkkk.', '.kwwk', '..kwk', '.....', '..kwk', '.kwwk', 'kkkk.'])
        else: stamp(g, 54, 33, ['kkkk.', '.kwwk', '..kwk', '...k.'])
        dots(g, 'k', [(52, 35), (53, 35)])
    return part(d, RAMP, p, open=[(37, 27, 42, 40)], r=2, tilt=.6)

# ---------- 脚（2本だけ。胸から 前へ、先は かぎ爪）----------
@lru_cache(None)
def legs(sw=0):
    g = G()
    for path in ([(37, 39), (41, 43), (40 + sw, 47)], [(33, 39), (32, 44), (34 - sw, 47)]):
        tube(g, path, [1.3, 1.1, 1], '1')
    g = shade(g, RAMP, r=1)
    dots(g, 'w', [(41 + sw, 48), (35 - sw, 48)])
    return Part(ink(g), [(30, 36, 40, 41)])

# ---------- 腹＝薙刀の 柄（節が 輪の ように 並ぶ）＋ 先の 刃 ----------
def bez(p0, p1, p2, n=12):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]
@lru_cache(None)
def naginata(mode='rest'):
    if mode == 'rest': path = bez((30, 37), (20, 39), (15, 39)); tip, d = (15, 39), (-1, -.3)
    elif mode == 'up': path = bez((30, 36), (21, 34), (15, 29)); tip, d = (15, 29), (-1, -.9)
    elif mode == 'swing': path = bez((31, 39), (24, 54), (43, 51)); tip, d = (43, 51), (1, -.15)
    else: path = bez((31, 39), (30, 52), (44, 47)); tip, d = (44, 47), (1, -.6)
    n = math.hypot(*d); d = (d[0] / n, d[1] / n); nv = (d[1], -d[0])
    if nv[1] > 0: nv = (-nv[0], -nv[1])
    def P(a, b): return (tip[0] + d[0] * a + nv[0] * b, tip[1] + d[1] * a + nv[1] * b)
    def dr(g):
        tube(g, path, [2.6 - 1.0 * i / (len(path) - 1) for i in range(len(path))], '1')
        tube(g, [P(-1, 0), P(1.5, 0)], [2.2, 2.2], '3')                        # はばき（金の 輪）
        poly(g, [P(1, 2.2), P(6, 3.6), P(11, 5.6), P(15.5, 9), P(12, 2.6), P(6, -1.2), P(1, -2.4)], '5')
    def p(g):
        for i in range(2, len(path) - 2, 2):                                   # 柄の 節（輪）
            x, y = path[i]
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-1, 0, 1):
                    if abs(path[i + 1][0] - x) > abs(path[i + 1][1] - y):
                        if dx == 0 and at(g, round(x), round(y) + dy) in 'ABD': put(g, round(x), round(y) + dy, 'D')
                    elif dy == 0 and at(g, round(x) + dx, round(y)) in 'ABD': put(g, round(x) + dx, round(y), 'D')
        for a in range(2, 14):                                                 # 刃の 光る しのぎ
            x, y = P(a, 2.4 + a * .3)
            if at(g, int(x), int(y)) in 'STU': put(g, int(x), int(y), 'S')
    return part(dr, RAMP, p, open=[(26, 31, 34, 42)], r=1, tilt=.4)

# 斬撃の 弧（はなれて いるのは 意図的な エフェクト）
@lru_cache(None)
def slash(big=True):
    g = G(); cx, cy, r = (47, 45, 11) if big else (49, 44, 12)
    for Y in range(H):
        for X in range(W):
            x, y = X - MX + .5, Y - MY + .5
            d1 = math.hypot(x - cx, y - cy); d2 = math.hypot(x - cx + 4, y - cy)
            if x > cx and d1 <= r and d2 > r - (1.2 if big else .4):
                g[Y][X] = 'w' if d1 > r - 1.4 else 'c' if d1 > r - 3 else 'C'
                if not big and (X + Y) % 2: g[Y][X] = '.'
    return Part(ink(g) if big else g)

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    b = (0, 0); h = (0, 0); ph = 0; nm = 'rest'; bite = False; fx = None; sw = 0
    seq = {'idle0': (0, 0), 'idle1': (1, -1), 'idle2': (2, 0), 'idle3': (1, 1), 'blink': (0, 0),
           'walk0': (1, -1), 'walk1': (2, -2), 'walk2': (1, -1), 'walk3': (0, 0)}
    if f in seq: ph, dy = seq[f]; b = (0, dy); sw = 1 if f in ('walk1', 'walk3', 'idle2') else 0
    if f.startswith('walk'): b = (1 if f in ('walk1', 'walk2') else 0, b[1])
    if f == 'atk0': b = (-2, -2); nm = 'up'; ph = 1
    if f == 'atk1': b = (2, 0); h = (0, 0); nm = 'swing'; ph = 2; bite = True; fx = slash(True)
    if f == 'atk2': b = (3, 1); nm = 'thrust'; ph = 0; fx = slash(False)
    if f == 'hit': b = (-4, -1); h = (-1, -1); ph = 2
    hb = (b[0] + h[0], b[1] + h[1])
    items = [(wing(ph, 1), b), (naginata(nm), b), (legs(sw), b), (thorax(), b), (head(E, bite), hb), (wing(ph, 0), b)]
    if fx: items.append((fx, b))
    g = compose(items)
    if f == 'ko':
        g = compose([(wing(2, 1), (0, 0)), (naginata('rest'), (0, 0)), (legs(0), (0, 0)), (thorax(), (0, 0)), (head('ko'), (0, 0)), (wing(2, 0), (0, 0))])
        return flip_ko(g, 60)
    return g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
