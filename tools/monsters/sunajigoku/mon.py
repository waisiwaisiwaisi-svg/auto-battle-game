# スナジゴク（じめん・むし × アリジゴク）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：すり鉢の ふちと 同じ 内向きの 弧を えがく 巨大な 大あご（内がわに 歯の 列）
import os, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='sunajigoku', name='スナジゴク', types=['ground', 'bug'], base='アリジゴク', size='M')
PAL = {
    'k': '#101018', 'l': '#2e2014',
    'A': '#e6c690', 'B': '#b08850', 'D': '#684828',      # 体（砂色）
    'S': '#f0a676', 'T': '#a8462a', 'U': '#561c14',      # 大あご（赤茶の かたい からだ）
    'c': '#f6e4b0', 'C': '#d0aa68',                      # 砂
    'Y': '#ffee6a', 'O': '#d8801c',                      # 目（明・暗）
    'w': '#ffffff',
}
LIGHT = set('AScYw')
KEEP_BLACK = set('wY')
RAMP = {'1': 'ABD', '3': 'STU', '6': 'cCC'}

def bez(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]

# ---------- 腹：大きく 丸い（ふしの すじ と 短い 剛毛）----------
@lru_cache(None)
def abdomen(b=0):
    def d(g):
        ell(g, 20, 46 - b, 13, 10.5 + b, '1')
    def p(g):
        for cx in (13, 19, 25):                                                # ふしの すじ（弧）
            for y in range(37, 57):
                x = cx + round(((y - 46) / 10) ** 2 * 2)
                if at(g, x, y) in 'AB': put(g, x, y, 'D')
        for x, y in ((10, 41), (16, 38), (22, 39), (12, 50), (18, 52), (24, 50)):  # 毛の 点
            if at(g, x, y) in 'ABD': put(g, x, y, 'l')
    g = part(d, RAMP, p, r=3, tilt=.7)
    for x, y in ((9, 37 - b), (14, 35 - b), (20, 35 - b), (26, 36 - b), (6, 41 - b)):   # 剛毛（せなかの とげ毛）
        put(g.g, x, y - 1, 'k'); put(g.g, x - 1, y - 2, 'k')
    return g

@lru_cache(None)
def thorax():
    def d(g): ell(g, 33, 45, 6.5, 6.5, '1')
    def p(g): dots(g, 'D', [(32, 42), (33, 43), (35, 48)])
    return part(d, RAMP, p, open=[(26, 38, 30, 52)], r=2)

# ---------- 脚（短く 太い 3本。先は かぎ爪）----------
@lru_cache(None)
def legs(sw=0):
    g = G()
    for i, (x0, x1) in enumerate(((26, 24), (32, 33), (38, 41))):
        s = sw if i % 2 == 0 else -sw
        tube(g, [(x0, 50), (x0 + (x1 - x0) * .5, 54), (x1 + s, 58)], [1.8, 1.5, 1.3], '1')
    g = shade(g, RAMP, r=1)
    for x1 in (24, 33, 41): put(g, x1 + 1, 59, 'w')
    return Part(ink(g), [(20, 45, 44, 52)])

# ---------- 頭：平たく はばの ある 頭。目は 上に ----------
EYES = {
    'open': ['kk......', '.kkkkk..', '..kwYkOk', '..kYOkOk', '...kkkk.'],
    'atk':  ['kk......', '.kkkkk..', '..kwwYYk', '..kYwYOk', '...kkkk.'],
    'blink': ['kk......', '.kkkkk..', '........', '..kkkkkk', '........'],
    'hit':  ['........', '.kk..kk.', '...kk...', '.kk..kk.', '........'],
    'ko':   ['........', '.k...k..', '..k.k...', '...k....', '..k.k...'],
}
@lru_cache(None)
def head(eye='open'):
    def d(g):
        poly(g, [(34, 40), (37, 34), (43, 32), (49, 34), (52, 38), (52, 44), (48, 48), (40, 48), (35, 46)], '1')
    def p(g):
        stamp(g, 38, 34, EYES[eye])
        dots(g, 'D', [(37, 44), (39, 46), (42, 46)])
        dots(g, 'k', [(51, 41), (50, 41)])                                     # 口
    return part(d, RAMP, p, open=[(32, 38, 37, 50)], r=2, tilt=.7)

# ---------- 大あご：上下 2本の 鎌。内向きの 弧と 歯 ----------
@lru_cache(None)
def mandible(op=0):
    """op: 0=ふつう 1=大きく ひらく 2=とじる"""
    up = [((47, 37), (60, 24), (61, 34)), ((47, 37), (62, 18), (64, 30)), ((47, 37), (58, 32), (62, 40))][op]
    lo = [((47, 45), (60, 54), (61, 45)), ((47, 45), (62, 59), (64, 49)), ((47, 45), (58, 50), (62, 42))][op]
    def d(g):
        for c in (up, lo):
            pth = bez(*c); tube(g, pth, [3.2 - 2.4 * i / (len(pth) - 1) for i in range(len(pth))], '3')
    def p(g):
        for c, sgn in ((up, 1), (lo, -1)):                                     # 内がわの 歯
            pth = bez(*c)
            for i in (5, 8, 11):
                x, y = pth[i]; x2, y2 = pth[i + 1]; dx, dy = x2 - x, y2 - y; n = math.hypot(dx, dy) or 1
                nx, ny = -dy / n, dx / n
                if ny * sgn < 0: nx, ny = -nx, -ny
                r = 3.2 - 2.4 * i / (len(pth) - 1)
                put(g, round(x + nx * (r + .6)), round(y + ny * (r + .6)), 'w')
    return part(d, RAMP, p, open=[(44, 34, 50, 48)], r=1, tilt=.4)

# ---------- 砂の すり鉢の ふち（足もとの 砂山）----------
@lru_cache(None)
def sand():
    def d(g):
        pts = [(2, 61)] + [(x, 59.5 - 6 * ((x - 31) / 29) ** 4) for x in range(2, 62)] + [(61, 61)]
        poly(g, pts, '6')
    def p(g):
        dots(g, 'C', [(5, 57), (8, 58), (12, 59), (50, 59), (54, 58), (57, 57)])
    return part(d, RAMP, p, r=1)

# 攻撃の 砂しぶき（はなれて 飛ぶのは 意図的）
SPRAY = ['..kk....kk..', '.kcck..kcck.', 'kcCck.kcCCk.', '.kck.kcCck..', '..k.kcck....', '...kcCk..kk.', '..kcck..kcck', '...kk....kk.']
SPRAY2 = ['..k....k....', '.kck..kck...', '..k....k..k.', '.......k.kck', '..k.......k.', '.kck..k.....', '..k..kck....', '......k.....']

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    b = 0; h = (0, 0); op = 0; sw = 0; root = (0, 0); fx = None
    if f == 'idle1': b = 1; op = 0
    if f == 'idle2': b = 1; h = (0, 1); op = 1 if False else 0
    if f == 'idle3': h = (0, 0)
    if f == 'walk0': sw = 1; h = (0, -1)
    if f == 'walk1': root = (1, 0); b = 1
    if f == 'walk2': sw = -1; h = (0, -1); root = (1, 0)
    if f == 'walk3': b = 1
    if f == 'atk0': op = 1; h = (-2, -1); b = 1
    if f == 'atk1': op = 2; h = (3, 0); root = (2, 0); fx = (SPRAY, 52, 46)
    if f == 'atk2': op = 2; h = (2, 0); root = (2, 0); fx = (SPRAY2, 54, 44)
    if f == 'hit': root = (-3, 0); h = (-2, -2); op = 1
    R = lambda o: (o[0] + root[0], o[1] + root[1])
    items = [(abdomen(b), R((0, 0))), (legs(sw), R((0, 0))), (thorax(), R((0, 0))), (mandible(op), R(h)), (head(E), R(h))]
    if f == 'ko':
        g = compose([(abdomen(0), (0, 0)), (legs(0), (0, 0)), (thorax(), (0, 0)), (mandible(0), (0, 0)), (head('ko'), (0, 0))])
        return over(flip_ko(g, 59), compose([(sand(), (0, 0))]))
    g = compose([(sand(), (0, 0))] + items)
    if fx: stamp(g, fx[1] + root[0], fx[2], fx[0])
    return g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
