# ドクツボ（どく・みず × ウツボ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：壺の 口と 同じ まるい 穴に ひらく 毒の 大口
import os, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='dokutsubo', name='ドクツボ', types=['poison', 'water'], base='ウツボ', size='M')
EYE_BOX = (39, 16, 8, 8)
PAL = {
    'k': '#101018', 'l': '#2c1a36',
    'A': '#dce672', 'B': '#96aa3a', 'D': '#4e5e22',      # ウツボの 皮（黄緑）
    'P': '#d070ec', 'Q': '#6e2c96',                      # 毒（斑・しずく）
    'E': '#86ccdc', 'F': '#3a7ca0', 'H': '#1e3c5e',      # 壺の 青い 釉（うわぐすり）
    'r': '#e8506a', 'R': '#8c1838',                      # 口の 中
    'Y': '#f6f2cc', 'O': '#b4a03c',                      # 目（白く にごった 黄 明・暗）
    'w': '#ffffff',
}
LIGHT = set('AEPYw')
KEEP_BLACK = set('wYrRP')
RAMP = {'1': 'ABD', '2': 'EFH'}

# ---------- 壺（胴の かわり）：まるい 胴と せまい 首、ふちは あつい 輪 ----------
@lru_cache(None)
def pot():
    def d(g):
        ell(g, 24, 50, 12.5, 10.5, '2')
        poly(g, [(17, 41), (31, 41), (29, 37), (19, 37)], '2')
        for x in range(13, 36):
            for y in (59, 60):
                if at(g, x, y) != '.' or 15 <= x <= 33: put(g, x, y, '2')
    def p(g):
        for x in range(13, 36):                                                # 波の もよう（みず）
            y = 49 + round(math.sin(x * .9) * 1.2)
            if at(g, x, y) in 'EFH': put(g, x, y, 'H' if at(g, x, y) != 'H' else 'l')
            if at(g, x, y - 1) in 'EF': put(g, x, y - 1, 'E')
        for x, y in ((17, 54), (21, 55), (25, 55), (29, 54)):
            put(g, x, y, 'E')
        stamp(g, 30, 44, ['k.', '.k', 'k.'])                                    # ひび
        ell(g, 24, 37.5, 7.5, 2.2, 'E')                                         # ふち（口）
        for x in range(18, 31): put(g, x, 39, 'F')
        ell(g, 24, 37.5, 5, 1.2, 'k')                                           # 口の やみ
    return part(d, RAMP, p, r=3, hi=.2, tilt=.6)

# ---------- 首（壺の 口から 出る 太い 胴）----------
def bez(p0, p1, p2, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]
NECK = {
    'rest': ((24, 40), (22, 28), (36, 27)), 'sway': ((24, 40), (23, 28), (36, 28)),
    'low': ((24, 41), (22, 34), (33, 31)), 'lunge': ((24, 40), (28, 26), (44, 27)),
    'back': ((24, 40), (20, 28), (32, 26)), 'ko': ((24, 40), (30, 40), (37, 50)),
}
@lru_cache(None)
def neck(mode='rest'):
    path = bez(*NECK[mode])
    def d(g):
        tube(g, path, [4.8 - .3 * i / len(path) for i in range(len(path))], '1')
        # 背びれ（毒の むらさきの ふち）
        for i in range(2, len(path) - 1):
            x, y = path[i]; x2, y2 = path[i - 1]; dx, dy = x - x2, y - y2; n = math.hypot(dx, dy) or 1
            nx, ny = dy / n, -dx / n
            if nx > 0: nx, ny = -nx, -ny
            for t in (4.8, 5.6):
                put(g, round(x + nx * t), round(y + ny * t), 'P' if t > 5 else '1')
    def p(g):
        for i, (x, y) in enumerate(path[1:-2]):                                 # 毒の 斑
            if i % 3 == 0: put(g, round(x) + 1, round(y), 'Q'); put(g, round(x), round(y) + 2, 'Q')
    return part(d, RAMP, p, open=[(14, 33, 34, 42)], r=2, tilt=.5)

# ---------- 頭：大きく、口は 壺の 口の ように まるく ひらく ----------
# 目（K 魚の 目）：まぶたの ない 丸い 目。白く にごった 黄の 細い 輪＋平たい 大きな ひとみ（上に にごりの 膜の 点）。
# まわりは 濃い うろこの ふち
EYES = {
    'open': ['DDD.....', '.DDDDDD.', '.kkkkkDD', 'kwYYYYk.', 'kYkYkkOk', 'kYkkkYOk', '.kYOOOk.', '..kkkk..'],
    'atk':  ['DD......', '.DDDDDD.', '.kkkkkDD', 'kwYYYYkD', 'kYYOkYOk', 'kYYkkYOk', '.kOOOOk.', '..kkkk..'],
    'blink': ['DDD.....', '.DDDDDD.', '.kkkkkDD', 'kDDDDDk.', 'kkkkkkkk', 'kOOOOOOk', '.kOOOOk.', '..kkkk..'],
    'hit':  ['........', '.DDDD...', 'DDkkkkD.', 'kYYkkYk.', 'kYYkkYOk', 'kYYYYOOk', '.kOOOOk.', '..kkkk..'],
    'ko':   ['DDD.....', '.DDDDDD.', '.kkkkkDD', 'kkYYYkk.', 'kYkYkOOk', 'kYYkOOOk', '.kOkOkk.', '.kkkkkk.'],
}
@lru_cache(None)
def head(eye='open', gape=1):
    def d(g):
        poly(g, [(32, 25), (35, 19), (41, 15), (49, 15), (55, 17), (59, 20), (61, 23), (58, 25), (58, 31), (61, 33), (58, 36), (50, 36), (42, 35), (36, 33), (32, 30)], '1')
    def p(g):
        # 口：まるい 大穴（ひらき ぐあい gape 0〜2）
        ry = (3, 5.5, 7)[gape]; cx, cy = 53, 28
        ell(g, cx, cy, 7 + gape * .6, ry + 1.2, 'B')                             # 唇の 輪（壺の ふちと 同じ）
        ell(g, cx, cy, 6 + gape * .5, ry, 'R')
        ell(g, cx - 1, cy + 1, 4.5, ry - 1.6, 'r')
        ell(g, cx - 2, cy + ry - 1.5, 3, 1.2, 'P')                                # 舌の 上の 毒
        for Y in range(H):
            for X in range(W):
                if g[Y][X] in 'Rr' and any(g[Y + dy][X + dx] in 'ABD1' for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))): g[Y][X] = 'k'
        for x in (48, 51, 54, 57):                                             # 上の 牙（内へ 反る）
            y = cy - int(ry) + (1 if x in (47, 56) else 0)
            stamp(g, x, y, ['w', 'w'])
        for x in (49, 53, 56):                                                 # 下の 牙
            y = cy + int(ry) - 1 - (1 if x in (48, 55) else 0)
            stamp(g, x, y - 1, ['w', 'w'])
        recol(g, {'1': 'B'}, None)
        for x, y in ((38, 18), (36, 22), (40, 30), (46, 16), (35, 27), (44, 33)):   # 毒の 斑
            if at(g, x, y) in 'ABD': put(g, x, y, 'Q'); put(g, x + 1, y, 'P')
        stamp(g, 39, 16, EYES[eye])
        dots(g, 'k', [(57, 19), (56, 19)])                                      # 鼻の 管
    return part(d, RAMP, p, open=[(30, 22, 37, 34)], r=2, tilt=.6)

# 毒の しずく（はなれて 落ちるのは 意図的）
DRIP = [['.kk.', 'kPPk', 'kPQk', '.kk.'], ['.k.', 'kPk', 'kQk', '.k.']]
# 攻撃：毒の しぶき
SPRAY = ['...kk..kk...', '..kPPkkPPk..', '.kPPQPPQPPk.', 'kPPwPPPPQPPk', '.kPPPQPPPPk.', 'kPQPPPwPPQk.', '.kPPkkPPQPk.', '..kk..kkPk..', '.......kk...']
SPRAY2 = ['..k...k.....', '.kPk.kPk..k.', '..k...k..kPk', 'k...k.....k.', '.k.kPk..k...', 'kPk.k..kPk..', '.k.......k..']

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    nm = 'rest'; h = (0, 0); root = (0, 0); gape = 1; drip = None; fx = None
    if f in ('idle1', 'idle3'): nm = 'sway'; h = (0, 1); drip = (0, 55, 37)
    if f == 'idle2': drip = (1, 55, 41)
    if f == 'blink': drip = None
    if f in ('walk0', 'walk2'): root = (1 if f == 'walk2' else 0, -2); nm = 'sway'; h = (0, 1)
    if f in ('walk1', 'walk3'): root = (1 if f == 'walk1' else 0, 0)
    if f == 'atk0': nm = 'low'; h = (-3, 4); gape = 0
    if f == 'atk1': nm = 'lunge'; h = (8, 0); gape = 2; fx = (SPRAY, 63, 21)
    if f == 'atk2': nm = 'lunge'; h = (7, 1); gape = 2; fx = (SPRAY2, 64, 19)
    if f == 'hit': nm = 'back'; h = (-4, -2); root = (-2, 0); gape = 0
    if f == 'ko': nm = 'ko'; h = (3, 24); gape = 0
    R = lambda o: (o[0] + root[0], o[1] + root[1])
    items = [(neck(nm), R((0, 0))), (head(E, gape), R(h)), (pot(), R((0, 0)))]
    if f == 'ko': items = [(pot(), (0, 0)), (neck(nm), (0, 0)), (head(E, gape), h)]
    g = compose(items)
    if drip: stamp(g, drip[1] + root[0] + h[0], drip[2] + root[1] + h[1], DRIP[drip[0]])
    if fx: stamp(g, fx[1] + root[0] - 5, fx[2] + h[1], fx[0])
    return g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
