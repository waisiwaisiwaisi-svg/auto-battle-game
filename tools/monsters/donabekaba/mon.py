# ドナベカバ（じめん・ほのお × カバ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：土鍋の ふたの ように 上下に ぱかっと ひらく 大口。中で 溶岩の 煮汁が 煮えたぎる
import os, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='donabekaba', name='ドナベカバ', types=['ground', 'fire'], base='カバ', size='L')
PAL = {
    'k': '#101018', 'l': '#2e1a14',
    'A': '#cc9c6a', 'B': '#8e5e3a', 'D': '#4e3020',      # 土の 皮（素焼き）
    'E': '#f2e4c4', 'F': '#c4ac84',                      # 白い 釉（うわぐすり）
    'Y': '#ffe86a', 'O': '#ff8a24', 'R': '#c8301c',      # 煮える 溶岩
    'G': '#7c6c92', 'N': '#4a3c5c', 'M': '#28203a',      # 黒い 釉（ふた）
    'c': '#e4eef4',                                      # 湯気
    'w': '#ffffff',
}
LIGHT = set('AEGYcw')
KEEP_BLACK = set('wYOc')
RAMP = {'1': 'ABD', '2': 'EFB', '5': 'GNM'}
FAR = {'A': 'B', 'B': 'D', 'E': 'F', 'G': 'N', 'N': 'M'}

# ---------- 胴：小さく 丸い。背に 釉の 流れ ----------
@lru_cache(None)
def body():
    def d(g): ell(g, 25, 45, 16, 11.5, '1')
    def p(g):
        for x in range(12, 40):                                                # 釉の たれ（波の ふち）
            y0 = 38 + round(math.sin(x * .8) * 1.3) + (0 if x < 30 else (x - 30) // 3)
            for y in range(30, y0):
                if at(g, x, y) in 'ABD': put(g, x, y, 'G' if y < 37 else 'N')
            if at(g, x, y0) in 'ABD': put(g, x, y0, 'E')
        dots(g, 'E', [(16, 36), (22, 35), (28, 36)])                            # 釉の そばかす
        dots(g, 'D', [(20, 50), (26, 51), (32, 50)])
        stamp(g, 7, 44, ['.k', 'kD', '.k'])                                      # 小さな しっぽ
    return part(d, RAMP, p, r=3, hi=.2, tilt=.7)

def leg(x0, far=False, lift=0):
    def d(g):
        poly(g, [(x0, 50), (x0 + 8, 50), (x0 + 8.5, 58), (x0 + 8, 61 - lift), (x0, 61 - lift), (x0 - .5, 57)], '1')
    def p(g):
        for x in range(x0, x0 + 9):
            if at(g, x, 60 - lift) != '.': put(g, x, 60 - lift, 'D')
        dots(g, 'w', [(x0 + 1, 60 - lift), (x0 + 4, 60 - lift), (x0 + 7, 60 - lift)])
        if far: recol(g, FAR)
    return part(d, RAMP, p, open=[(x0 - 2, 47, x0 + 10, 52)], r=1, tilt=.6)

# ---------- 頭：上あご＝ふた（つまみ・釉）、下あご＝鍋。間の すき間が 赤く 光る ----------
EYES = {
    'open': ['kk......', '.kkkkk..', '..kwYkOk', '..kYOkOk', '...kkkk.'],
    'atk':  ['kk......', '.kkkkk..', '..kwwYYk', '..kYwYOk', '...kkkk.'],
    'blink': ['kk......', '.kkkkk..', '........', '..kkkkkk', '........'],
    'hit':  ['kk......', '.kkkkk..', '..OO....', '....OOO.', '..OO....'],
    'ko':   ['........', '..O...O.', '...O.O..', '....O...', '...O.O..', '..O...O.'],
}
LIDS = {   # 上あご（ふた）の 形：ひらき ぐあいで 前が 上がる
    0: [(33, 33), (35, 27), (40, 23.5), (48, 23), (56, 24.5), (61, 28), (63, 33)],
    1: [(33, 33), (35, 25), (40, 20), (48, 18.5), (56, 19.5), (61, 22), (63, 28), (60, 30.5)],
    2: [(33, 33), (33, 24), (36, 17), (42, 12), (50, 9), (57, 9), (62, 12), (60, 17), (50, 23), (40, 30)],
}
@lru_cache(None)
def jaw():
    def d(g):
        poly(g, [(34, 33), (63, 33), (61, 38), (56, 42), (44, 43), (37, 41), (34, 38)], '1')
    def p(g):
        for x in range(36, 63): put(g, x, 34, 'E'); put(g, x, 35, 'F') if at(g, x, 35) != '.' else None   # 鍋の ふち（釉）
        stamp(g, 37, 37, ['kk', 'kDk', '.k'])                                    # 鍋の 取っ手の あと
        dots(g, 'D', [(44, 41), (48, 41), (52, 40)])
    return part(d, RAMP, p, open=[(31, 36, 37, 46)], r=2, tilt=.5)
@lru_cache(None)
def lid(op=0, eye='open'):
    pts = LIDS[op]
    def d(g):
        poly(g, pts, '5')
        ell(g, 37, 24 - (1 if op == 2 else 0), 3, 3, '5')                       # 目の こぶ
        poly(g, [(35, 25), (34, 20), (37, 21)], '5')                              # 耳
    def p(g):
        # ふたの 釉：上半分が 白く、ふちが 波打って たれる
        for Y in range(H):
            for X in range(W):
                x, y = X - MX, Y - MY
                if g[Y][X] in 'GNM' and x > 39 and op < 2:
                    if y > LIDS[op][-1][1] - 3 - round(math.sin(x * .9)): g[Y][X] = 'E' if y > LIDS[op][-1][1] - 2 else 'F'
                if g[Y][X] in 'GNM' and op == 2 and y + (x - 40) * .6 > 28 - round(math.sin(x * .9)): g[Y][X] = 'E'
        kx = (48, 48, 46)[op]; ky = (23, 19, 12)[op]
        stamp(g, kx - 2, ky - 4, ['.kkk.', 'kEEFk', 'kEFBk', '.kkk.'])           # ふたの つまみ
        stamp(g, (59, 59, 58)[op], (26, 22, 11)[op], ['kk', '.k'])            # 鼻の 穴
        stamp(g, 34, 20 - (1 if op == 2 else 0), EYES[eye])
    return part(d, RAMP, p, open=[(31, 26, 36, 35)], r=2, tilt=.7)

# 口の 中（ひらいた ときだけ）：煮える 溶岩と 牙
@lru_cache(None)
def maw(op=2):
    g = G()
    if op == 1:
        poly(g, [(40, 32), (61, 29), (62, 33), (40, 34)], 'R')
        for x in range(42, 61, 3): put(g, x, 33, 'O')
        stamp(g, 52, 31, ['w', 'w']); stamp(g, 58, 30, ['w'])
    else:
        poly(g, [(38, 32), (44, 26), (52, 20), (61, 15), (62, 33), (40, 34)], 'R')
        for Y in range(H):
            for X in range(W):
                if g[Y][X] == 'R' and Y - MY >= 27: g[Y][X] = 'O'
                if g[Y][X] == 'O' and Y - MY >= 31: g[Y][X] = 'Y'
        for cx, cy in ((46, 31), (52, 29), (57, 30), (55, 25)):                            # 泡
            stamp(g, cx - 1, cy - 1, ['.Y.', 'YwY', '.Y.'])
        stamp(g, 59, 16, ['ww', '.w', '.w']); stamp(g, 53, 20, ['w', 'w'])               # 上の 牙
        stamp(g, 55, 31, ['.w', 'ww']); stamp(g, 60, 30, ['w', 'w', 'w'])        # 下の きば
    return Part(g)

@lru_cache(None)
def seam():
    g = G()
    for x in range(42, 62): put(g, x, 33, 'O' if x % 4 else 'Y')
    stamp(g, 59, 31, ['kw', 'kw', 'k.']); stamp(g, 52, 32, ['w'])                 # 下の きば
    return Part(g)

# 湯気（はなれて 立つのは 意図的）
STEAM = [['.kk.', 'kcck', 'kcck', '.kk.'], ['..kk', '.kcck', 'kcck.', '.kk..']]
BLAST = ['....kkk.....', '..kkcccckk..', '.kccwwwccck.', 'kcccwwwwccck', 'kccYYwwYYcck', '.kcOYYYYOck.', 'kcOOYwwYOOck', '.kcROOOORck.', '..kkRRRRkk..', '....kkkk....']

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    b = h = la = lb = root = (0, 0); op = 0; steam = None; fx = None
    if f == 'idle0': steam = (0, 62, 19)
    if f == 'idle1': b = (0, 1); steam = (1, 63, 17)
    if f == 'idle2': b = (0, 1); h = (0, 1)
    if f == 'idle3': steam = (0, 62, 15)
    if f == 'walk0': la = (1, -2); h = (0, -1)
    if f == 'walk1': b = (0, -1); h = (0, -1)
    if f == 'walk2': lb = (1, -2); h = (0, -1)
    if f == 'walk3': b = (0, -1)
    if f == 'atk0': b = (-1, 1); h = (-2, 1); op = 1; steam = (1, 60, 22)
    if f == 'atk1': root = (3, 0); op = 2; fx = (BLAST, 61, 6)
    if f == 'atk2': root = (2, 0); op = 2; steam = (0, 64, 12)
    if f == 'hit': root = (-3, 0); h = (-2, -1)
    def A(*o): return (root[0] + sum(a[0] for a in o), root[1] + sum(a[1] for a in o))
    hb = A(b, h) if not f.startswith('walk') else A(h)
    items = [(leg(14, True), A(lb)), (leg(30, True), A(la)), (body(), A(b)), (leg(19), A(la)), (leg(36), A(lb)), (jaw(), hb)]
    if op: items.append((maw(op), hb))
    items.append((lid(op, E), hb))
    if not op: items.append((seam(), hb))
    g = compose(items)
    if steam: stamp(g, steam[1] + hb[0] - 3, steam[2] + hb[1], STEAM[steam[0]])
    if fx: stamp(g, fx[1] + root[0] - 4, fx[2], fx[0])
    if f == 'ko':   # 横だおれ：胴が しずみ、頭（ふた）は 地面に べたり。目は ×
        g = compose([(leg(14, True), (0, 2)), (body(), (0, 6)), (leg(19), (-3, 1)), (leg(36), (3, 1)), (jaw(), (1, 18)), (lid(0, 'ko'), (1, 18)), (seam(), (1, 18))])
        stamp(g, 60, 34, STEAM[1])
    return g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
