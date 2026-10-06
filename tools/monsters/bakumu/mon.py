# バクム（エスパー・あく × バク）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：煙管（きせる）に なった 長い 鼻。先の 雁首（がんくび）の 火皿から 夢の 煙
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='bakumu', name='バクム', types=['psychic', 'dark'], base='バク', size='M')
PAL = {
    'k': '#100c18', 'l': '#2c1c40',
    'A': '#6c6290', 'B': '#3e365e', 'D': '#221c38',      # 黒い 皮
    'E': '#ece4f4', 'F': '#b6a8d0', 'H': '#7a6c9e',      # 白い 鞍
    'U': '#ffe596', 'V': '#d39a36', 'W': '#83521c',      # 煙管の 真鍮
    'P': '#ffb4ee', 'Q': '#b45ad8',                      # 夢の 煙
    'R': '#ff5ca0', 'S': '#a01850', 'w': '#ffffff',      # 目（明・暗）・きば
}
LIGHT = set('AEUPw')
KEEP_BLACK = set('wRSPU')
RAMP = {'1': 'ABD', '2': 'EFH', '3': 'UVW'}
FAR = {'A': 'B', 'B': 'D', 'E': 'F', 'F': 'H', 'H': 'D'}

# ---------- 胴：小さく 丸く。前は 黒、まん中から 後ろが 白い 鞍 ----------
@lru_cache(None)
def body():
    def d(g):
        ell(g, 24, 47, 12.5, 9, '1')
        for y in range(36, 58):
            for x in range(10, 38):
                if at(g, x, y) == '1' and 13 <= x + (y - 44) * .35 <= 28 and y <= 52: put(g, x, y, '2')
    def p(g):
        dots(g, 'H', [(14, 51), (17, 52), (20, 52), (23, 52), (26, 51)])     # 鞍の すその ひだ
        dots(g, 'l', [(29, 41), (30, 44), (30, 47)])                          # 肩の 筋
        stamp(g, 9, 44, ['.kk', 'kDk', '.k.'])                                # 短い しっぽ（胴に 食いこむ）
    return part(d, RAMP, p, r=3, hi=.22, tilt=.8)

def leg(x0, far=False, lift=0):
    def d(g):
        poly(g, [(x0, 50), (x0 + 6, 50), (x0 + 6.5, 58), (x0 + 6, 60 - lift), (x0, 60 - lift), (x0 - .5, 57)], '1')
    def p(g):
        for x in range(x0, x0 + 7): put(g, x, 59 - lift, 'D') if at(g, x, 59 - lift) != '.' else None
        dots(g, 'w', [(x0 + 1, 59 - lift), (x0 + 4, 59 - lift)])   # ひづめの 爪
        if far: recol(g, FAR)
    return part(d, RAMP, p, open=[(x0 - 2, 48, x0 + 8, 52)], r=1, tilt=.6)

# ---------- 頭：大きな くさび形、小さな とがり耳 ----------
EYES = {
    'open': ['kk......', '.kkkkk..', '..kwRkSk', '..kRSkSk', '...kkkk.'],
    'atk':  ['kk......', '.kkkkk..', '..kwwwRk', '..kRwRSk', '...kkkk.'],
    'blink': ['kk......', '.kkkkk..', '........', '..kkkkkk', '........'],
    'hit':  ['........', '.kk..kk.', '...kk...', '.kk..kk.', '........'],
    'ko':   ['........', '.k...k..', '..k.k...', '...k....', '..k.k...'],
}
@lru_cache(None)
def head(eye='open'):
    def d(g):
        poly(g, [(30, 34), (32, 28), (37, 25), (43, 25), (48, 28), (51, 32), (50, 37), (46, 41), (39, 43), (33, 42), (30, 39)], '1')
        poly(g, [(32, 29), (31, 21), (34, 22), (37, 27)], '1')      # 耳（頭に 食いこむ）
        poly(g, [(40, 26), (42, 20), (45, 26)], '1')                  # 額の とがり（あくの 角）
    def p(g):
        dots(g, 'E', [(31, 22), (32, 22), (31, 23)])                 # 耳の ふち（白）
        dots(g, 'Q', [(32, 24), (33, 25), (32, 25)])                 # 耳の 中
        stamp(g, 41, 22, ['P', 'Q'])                                  # 額に 夢の 宝玉
        dots(g, 'D', [(33, 39), (34, 40), (36, 41)])
        stamp(g, 35, 27, EYES[eye])
        # 口：ななめに さけて 下向きの きば
        dots(g, 'k', [(39, 40), (40, 40), (41, 39), (42, 39), (43, 39), (44, 38), (45, 38), (46, 37)])
        stamp(g, 41, 40, ['wk', 'w.'] if eye != 'ko' else ['w'])
        stamp(g, 44, 39, ['w'])
    return part(d, RAMP, p, r=2, tilt=.6)

# ---------- 鼻＝煙管：皮の 羅宇（ふしの ある 管）＋真鍮の 輪 ＋ 雁首と 火皿 ----------
GAN = [
    'kkkkkkkk',
    'kUPPPPQk',
    'kUUUUVWk',
    '.kUVVWk.',
    '..kVWk..',
    '...kk...',
]
GAN_HOT = [r.replace('P', 'w').replace('Q', 'P') for r in GAN]
@lru_cache(None)
def nose(lift=0, hot=False):
    path = [(46, 35), (52, 37), (56, 40.5 - lift), (58.5, 45 - lift)]
    def d(g):
        tube(g, path, [3.2, 2.6, 2.2, 2.0], '1')
        for Y in range(H):
            for X in range(W):
                x = X - MX
                if g[Y][X] == '1' and (48 <= x <= 49 or x >= 56): g[Y][X] = '3'
    def p(g):
        for x in (51, 54):                                            # 羅宇の ふし
            for y in range(30, 46):
                if at(g, x, y) in 'ABD' and at(g, x, y - 1) not in '.': put(g, x, y, 'l')
    g = part(d, RAMP, p, open=[(42, 30, 47, 41)], r=1, tilt=.6)
    stamp(g.g, 55, 44 - lift, GAN_HOT if hot else GAN)
    return g

# ---------- 夢の 煙（火皿から 立ちのぼる。火皿に つながる）----------
@lru_cache(None)
def smoke(ph=0):
    o = (0, 1, -1)[ph]
    g = G(); t = G()
    for cx, cy, r in ((60.5, 42, 1.2), (61.5 + o * .5, 38.5, 1.8), (60, 34, 2.3), (57.5 - o, 30, 2.6), (54.5, 25.5, 2.9), (57 + o, 21, 2.6), (53 + o, 19, 2.2)):
        ell(t, cx, cy, r, r * .9, 'P')
    for Y in range(H):
        for X in range(W):
            if t[Y][X] == '.': continue
            e = (X + 1 < W and t[Y][X + 1] == '.') or (Y + 1 < H and t[Y + 1][X] == '.')
            g[Y][X] = 'Q' if e else 'P'
    for x, y in ((53, 17), (54, 17), (55, 18), (54, 19), (61, 34), (60, 35), (58, 28)):
        put(g, x + o, y, 'Q')                                          # 夢の うず
    return Part(ink(g))

# ---------- 攻撃：にらむ 目玉の ある 悪夢の 雲（はなれて 飛ぶのは 意図的）----------
@lru_cache(None)
def blast(big=True):
    def d(g):
        cs = ((52, 26, 5), (58, 21, 6), (64, 24, 5.5), (58, 28, 5.5)) if big else ((52, 24, 3), (59, 20, 3.5), (66, 25, 3), (58, 29, 2.5))
        for cx, cy, r in cs: ell(g, cx, cy, r, r * .87, 'P')
    def p(g):
        for Y in range(H):
            for X in range(W):
                if g[Y][X] == 'P' and Y + 1 < H and X + 1 < W and (g[Y + 1][X] == '.' or g[Y][X + 1] == '.' or (Y + 2 < H and g[Y + 2][X] == '.')): g[Y][X] = 'Q'
        if big: stamp(g, 54, 22, ['..kkkkk..', '.kRwRRSk.', 'kRRkkkSSk', '.kSSSSSk.', '..kkkkk..'])
        else:
            for Y in range(H):
                for X in range(W):
                    if g[Y][X] in 'PQ' and (X + Y) % 2: g[Y][X] = '.'
    return part(d, None, p)

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    b = h = la = lb = (0, 0); ph = 0; lift = 0; hot = False; fx = []
    if f == 'idle1': b = (0, 1); ph = 1
    if f == 'idle2': b = (0, 1); h = (0, 1); ph = 2
    if f == 'idle3': h = (0, 0); ph = 1
    if f == 'blink': ph = 2
    if f == 'walk0': la = (1, -1); lb = (-1, 0); h = (0, -1)
    if f == 'walk1': b = (0, -1); h = (0, -1); ph = 1
    if f == 'walk2': la = (-1, 0); lb = (1, -1); h = (0, -1); ph = 2
    if f == 'walk3': b = (0, -1); ph = 0
    if f == 'atk0': b = (-1, 1); h = (-2, 1); hot = True
    if f == 'atk1': b = (1, 0); h = (2, -1); lift = 1; hot = True; fx = [(blast(True), (0, 0))]
    if f == 'atk2': b = (1, 0); h = (1, 0); lift = 1; fx = [(blast(False), (4, -2))]
    if f == 'hit': b = (-2, 0); h = (-4, -1); la = lb = (-2, 0)
    def add(p, o): return (p, (o[0], o[1]))
    hh = (h[0] + b[0], h[1] + b[1]) if f not in ('walk0', 'walk2') else h
    items = [add(leg(15, True), lb), add(leg(30, True), la), add(body(), b), add(leg(11), la), add(leg(26), lb)]
    if f not in ('atk1', 'atk2', 'hit', 'ko'): items.append(add(smoke(ph), hh))
    items += [add(nose(lift, hot), hh), add(head(E), hh)] + fx
    g = compose(items)
    return flip_ko(g) if f == 'ko' else g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
