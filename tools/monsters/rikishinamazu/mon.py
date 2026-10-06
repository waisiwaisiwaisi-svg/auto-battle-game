# リキシナマズ（かくとう・みず × ナマズ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：顔の まえ はば いっぱいに さける 巨大な 口（と 張り手）
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='rikishinamazu', name='リキシナマズ', types=['fighting', 'water'], base='ナマズ', size='L')
EYE_BOX = (40, 15, 10, 8)
PAL = {
    'k': '#101018', 'l': '#1c2c40',
    'A': '#86aebe', 'B': '#4c7088', 'D': '#2a4058',      # ぬめる 皮
    'E': '#f2e8cc', 'F': '#c6b48e',                      # 腹・あご
    'm': '#ec6c5c', 'M': '#b8303c', 'N': '#661626',      # まわし・口の 中
    'O': '#06060a', 'Y': '#4c5a70',                      # 目（ビーズの 黒・つやの 灰青）・太い まゆ
    'c': '#c4eeff', 'C': '#4aa6e8',                      # 水しぶき
    'w': '#ffffff',
}
LIGHT = set('AEmcw')
KEEP_BLACK = set('wYMO')
RAMP = {'1': 'ABD', '2': 'EFB', '4': 'mMN'}
FAR = {'A': 'B', 'B': 'D', 'E': 'F', 'F': 'B', 'm': 'M', 'M': 'N'}

# ---------- 胴：まるい 力士の 腹 ＋ まわし ----------
@lru_cache(None)
def body():
    def d(g):
        ell(g, 30, 44, 14, 11, '1')
        for Y in range(H):
            for X in range(W):
                x, y = X - MX, Y - MY
                if g[Y][X] != '1': continue
                if x > 31 + (y - 45) * -.5 and y > 37: g[Y][X] = '2'             # 腹
                if 48 <= y <= 52 + (1 if x > 34 else 0): g[Y][X] = '4'           # まわし
    def p(g):
        dots(g, 'F', [(37, 41), (38, 42), (36, 44), (37, 45)])                    # 腹の しわ
        for x in range(17, 45):
            if at(g, x, 48) in 'mMN': put(g, x, 48, 'N')
        dots(g, 'N', [(40, 49), (40, 50), (40, 51), (40, 52)])                    # 前の 結び目
        dots(g, 'm', [(41, 49), (41, 50)])
    return part(d, RAMP, p, r=3, hi=.2, tilt=.7)

# さがり（まわしから 垂れる ひも ＝ ひげと 同じ 垂れる 形）
@lru_cache(None)
def sagari():
    g = G()
    for i, x in enumerate((36, 39, 42)):
        for y in range(53, 58 + (i % 2)):
            put(g, x, y, 'M' if y < 56 else 'N')
        put(g, x, 53, 'm')
    return Part(ink(g))

def leg(x0, far=False):
    def d(g):
        poly(g, [(x0, 49), (x0 + 8, 49), (x0 + 9, 57), (x0 + 11, 58), (x0 + 11, 61), (x0 - 1, 61), (x0 - 1, 56)], '1')
    def p(g):
        dots(g, 'w', [(x0 + 7, 60), (x0 + 9, 60)])                              # 足の 爪
        dots(g, 'D', [(x0 + 8, 59), (x0 + 6, 60)])
        if far: recol(g, FAR)
    return part(d, RAMP, p, open=[(x0 - 2, 48, x0 + 10, 53)], r=2, tilt=.6)

# ---------- 腕と 張り手（大きく ひらいた 手のひら）----------
@lru_cache(None)
def arm(mode='rest'):
    def d(g):
        if mode == 'rest':
            tube(g, [(38, 39), (44, 44), (47, 47)], [3.5, 3, 2.8], '1')
            ell(g, 49, 49, 3.6, 3.4, '1')
            for fx in (47, 49.5, 52):
                tube(g, [(fx, 50), (fx + .5, 54)], [1.2, 1.1], '1')
        elif mode == 'back':
            tube(g, [(36, 40), (31, 44), (28, 44)], [3.5, 3, 2.8], '1')
            ell(g, 26, 43, 3.4, 3.8, '1')
        else:
            tube(g, [(38, 39), (46, 39), (51, 38.5)], [3.5, 3, 2.8], '1')
            ell(g, 54, 38, 4, 6, '1')
            for fy in (32.5, 35.5, 38.5, 41.5):
                tube(g, [(56, fy), (60, fy - .5)], [1.4, 1.3], '1')
            tube(g, [(54, 44), (58, 46)], [1.4, 1.2], '1')                         # 親指
    def p(g):
        if mode == 'rest': dots(g, 'w', [(47, 55), (50, 55), (52, 55)])
        elif mode == 'push':
            dots(g, 'w', [(61, 32), (61, 35), (61, 38), (61, 41)])
            dots(g, 'E', [(53, 35), (54, 36), (53, 37), (54, 38), (53, 39), (54, 40), (53, 41)])     # 手のひら
            dots(g, 'D', [(51, 37), (51, 39)])
    return part(d, RAMP, p, open=[(33, 35, 40, 44)], r=2, tilt=.5)

# ---------- 頭：平たく 横に はばの ある ナマズ頭。目は 上に、口は 前 はば いっぱい ----------
# 目（S ビーズ目＋太い まゆ）：小さな 黒い ビーズの 目に 白い 光 1点・下に 灰青の つや。
# その上に 前へ ぐっと 下がる 太い 黒の まゆ毛（3段）で こわく にらむ
EYES = {
    'open': ['OO........', 'OOOO......', '.OOOOOO...', '...OOOOOO.', '..kkk.OOOO', '.kwOOk..O.', '.kOOYk....', '..kkk.....'],
    'atk':  ['O.........', 'OOOO......', '.OOOOOO...', '..kkOOOOO.', '.kwwOk.OOO', '.kwOOk..O.', '.kOOYk....', '..kkk.....'],
    'blink': ['OO........', 'OOOO......', '.OOOOOO...', '...OOOOOO.', '.....OOOO.', '.kkkkk..O.', '..OOO.....', '..........'],
    'hit':  ['....OO....', '..OOOOOO..', 'OOOO..OOO.', 'OO......O.', '..k.k.....', '...k......', '..k.k.....', '..........'],
    'ko':   ['OO........', 'OOOO......', '.OOOOOO...', '...OOOOOO.', '.k...kOOOO', '..k.k...O.', '...k......', '..k.k.....', '.k...k....'],
}
@lru_cache(None)
def head(eye='open', mouth='shut'):
    op = mouth == 'open'
    def d(g):
        poly(g, [(25, 25), (28, 18), (34, 14), (44, 13), (52, 15), (57, 19), (60, 24), (60, 28), (57, 32), (50, 35), (40, 36), (32, 35), (27, 31)], '1')
        if op: poly(g, [(38, 30), (48, 33), (58, 32), (60, 36), (54, 41), (44, 41), (36, 37)], '2')     # 下あご（落ちる）
        else: poly(g, [(36, 30), (46, 30), (57, 28), (59, 30), (55, 34), (46, 36), (36, 35)], '2')
    def p(g):
        if op:
            poly(g, [(40, 29), (60, 24.5), (61, 26), (59, 35), (52, 38), (44, 37), (39, 33)], 'N')   # 口の 中
            poly(g, [(43, 33), (58, 31), (56, 36), (47, 36)], 'M')                                  # 舌
            dots(g, 'm', [(50, 33), (51, 33), (52, 32)])
            for i, x in enumerate(range(43, 60, 3)):
                stamp(g, x, 29 - (x - 43) // 4, ['ww', '.w'])                                      # 上の 牙
            for x in (46, 51, 56):
                stamp(g, x, 36 - (x - 46) // 6, ['.w', 'ww'])                                      # 下の 牙
            for Y in range(H):
                for X in range(W):
                    if g[Y][X] in 'NMm' and any(g[Y + dy][X + dx] in 'ABDEF' for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))): g[Y][X] = 'k'
        else:
            for x in range(36, 60):                                                    # 口：前へ 上がる 太い 線＋牙
                y = 30 - (x - 36) * 3 // 23
                put(g, x, y, 'k')
                if 39 <= x <= 57: put(g, x, y + 1, 'N')
                if 39 <= x <= 57: put(g, x, y + 2, 'k')
            for x in (41, 46, 51, 56):
                y = 31 - (x - 36) * 3 // 23
                stamp(g, x, y, ['ww', 'w.'])
            for x in (44, 49, 54):
                y = 31 - (x - 36) * 3 // 23
                stamp(g, x, y, ['.w'])
            dots(g, 'k', [(35, 31), (34, 32), (35, 32)])                               # 口の はし（への字）
        dots(g, 'D', [(33, 18), (36, 16), (31, 22), (29, 26), (38, 18)])             # ぬめりの 斑
        dots(g, 'B', [(34, 18), (37, 16), (30, 22)])
        stamp(g, 40, 15, EYES[eye])
        dots(g, 'k', [(58, 22), (57, 22)])                                             # 鼻の 穴
    return part(d, RAMP, p, open=[(25, 30, 44, 37)], r=3, hi=.2, tilt=.8)

# 髷（まげ）＝ 前へ 折れた 背びれ。白い 元結
@lru_cache(None)
def mage():
    def d(g):
        poly(g, [(33, 16), (34, 10), (38, 7), (44, 7), (46, 9), (41, 10), (39, 13), (40, 16)], '1')
    def p(g):
        recol(g, {'A': 'B', 'B': 'D', 'D': 'l'})
        dots(g, 'A', [(38, 8), (39, 8), (40, 8), (36, 9)])
        dots(g, 'w', [(34, 13), (35, 13), (36, 13), (37, 13), (38, 13)])                # 元結
        dots(g, 'F', [(35, 12), (36, 12)])
    return part(d, RAMP, p, open=[(31, 14, 42, 18)], r=1)

# ひげ（上あごの 角から 長く 垂れる 2本、あごに 短い 2本）
@lru_cache(None)
def whisker(sway=0, open_=False):
    g = G(); a = 4 if open_ else 0
    for pts in ([(57, 27 - a), (61, 30 - a), (62, 35), (61 + sway, 40), (59 + sway, 44)],
                [(54, 30 - a // 2), (56, 34), (55 + sway, 39), (53 + sway, 42)]):
        for i in range(len(pts) - 1):
            from pix import line as L
            gg = [r for r in g]
            L(g, pts[i][0] + MX, pts[i][1] + MY, pts[i + 1][0] + MX, pts[i + 1][1] + MY, 'B')
    for y in range(H):
        for x in range(W):
            if g[y][x] == 'B' and (y + 1 >= H or g[y + 1][x] != 'B') and (x + 1 < W and g[y][x + 1] != 'B'): pass
    out = ink(g)
    return Part(out, [(52, 22, 60, 32)])

# 尾（ナマズの 長い しりびれ）
@lru_cache(None)
def tail(sw=0):
    def d(g):
        tube(g, [(20, 48), (12, 51), (6, 50 + sw)], [4, 3, 2], '1')
        poly(g, [(8, 46 + sw), (2, 42 + sw), (3, 50 + sw), (2, 57 + sw), (8, 53 + sw)], '1')
    def p(g):
        for y in (45, 48, 51, 54):
            for x in range(2, 7):
                if at(g, x, y + sw) in 'ABD': put(g, x, y + sw, 'D')
    return part(d, RAMP, p, open=[(16, 42, 24, 56)], r=2)

# ---------- 水しぶき（張り手の しょうげき。はなれて 飛ぶのは 意図的）----------
SPL = ['....kk.......', '...kcck..kk..', '.kkcCCck.kck.', 'kcccCCCckccck', '.kcCCCCCCcck.', 'kccCCwwCCCck.',
       '.kcCCwwCCck..', 'kccCCCCCcck..', '.kkcCCCcck...', '...kcck.kk...', '....kk.......']
SPL2 = ['k.....kk.....', 'ck...kcck..k.', '.k..kcCck.kck', '...kcCCCck.k.', '..kcCCCCCk...', 'kk.kcCCCk..kk',
        'cck.kcCck.kcc', '.k...kck...k.', '....k.k.k....', '...kck.kck...', '....k...k....']

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    b = h = la = lb = (0, 0); sw = 0; am = 'rest'; mo = 'shut'; fx = None; root = (0, 0); ts = 0
    if f in ('idle1', 'idle3'): h = (0, 1); sw = 1; ts = 1
    if f == 'idle2': b = (0, 1); h = (0, 1)
    if f == 'walk0': la = (1, -2); b = (0, -1); sw = 1
    if f == 'walk1': b = (0, 0)
    if f == 'walk2': lb = (1, -2); b = (0, -1); sw = -1; ts = 1
    if f == 'atk0': b = (-2, 1); h = (-3, 2); am = 'back'
    if f == 'atk1': root = (3, 0); am = 'push'; mo = 'open'; fx = (SPL, 62, 31)
    if f == 'atk2': root = (4, 0); am = 'push'; mo = 'open'; fx = (SPL2, 63, 30); b = (0, 1)
    if f == 'hit': root = (-3, 0); h = (-3, -1); b = (-1, 0); sw = 2
    if f == 'ko': mo = 'shut'
    def A(o, *more):
        x, y = root[0] + o[0], root[1] + o[1]
        for m in more: x += m[0]; y += m[1]
        return (x, y)
    items = [(tail(ts), A(b)), (leg(19, True), A(lb)), (body(), A(b)), (sagari(), A(b)), (leg(29), A(la)),
             (mage(), A(b, h)), (head(E, mo), A(b, h)), (whisker(sw, mo == 'open'), A(b, h)), (arm(am), A(b))]
    g = compose(items)
    if fx: stamp(g, fx[1] + root[0] - 4, fx[2] - 1, fx[0])
    if f == 'ko':   # ばったり 前へ たおれる：腹ばいで 頭を 地面に つけ、目は ×
        b = (-4, 6); hk = (4, 20)
        g = compose([(tail(0), b), (leg(19, True), (-4, 1)), (body(), b), (sagari(), b), (leg(29), (-3, 1)), (arm('back'), (-2, 8)),
                     (mage(), hk), (head('ko', 'shut'), hk), (whisker(2, False), hk)])
    return g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
