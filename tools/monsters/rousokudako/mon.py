# ロウソクダコ（ゴースト・ほのお × タコ）手打ち GBA風・デフォルメ（2〜3頭身：燭台の 頭と 霊火、短い ろうの 足）
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
META = dict(id='rousokudako', name='ロウソクダコ', types=['ghost', 'fire'], base='タコ', size='M')
PAL = {
    'k': '#101018', 'l': '#3a2440',
    'A': '#f6eefa', 'B': '#cdb8dc', 'C': '#8c72aa',      # ゆうれいの ろう（明・中・暗）
    'G': '#f2c454', 'H': '#a8682a',                      # 燭台の 真ちゅう
    'c': '#e4fbff', 'b': '#78d4ff', 'V': '#6a52d8',      # 霊火（白・水色・青むらさき）＝目の 虹彩も
    'O': '#ff8a3a',                                      # 炎の しん
    'P': '#4a1a50',                                      # 口の 中
    'w': '#ffffff',
}
LIGHT = set('AGcw')
KEEP_BLACK = set('wcb')
RAMP = {'1': 'ABC', '2': 'GGH'}
DARK = {'A': 'B', 'B': 'C', 'C': 'C'}

# ---------- 頭（外とう膜 ＝ ろうそくの 本体）：後ろへ ふくらみ、上の 溶け口に 霊火。首には 燭台の 皿 ----------
def head(open_=False):
    def d(p):
        ellipse(p, 27, 23, 12, 10, '1')
        ellipse(p, 36, 28, 12, 7.5, '1')
    def post(s):
        # 溶けた ろうの ふち（てっぺんの 溶け口）と、たれる すじ
        for (x, n) in ((18, 5), (22, 8), (29, 6), (33, 3)):
            for y in range(15, 15 + n):
                if s[y][x] != '.': s[y][x] = 'A'
                if s[y][x + 1] != '.' and y > 15: s[y][x + 1] = 'C'
            if s[15 + n][x] != '.': s[15 + n][x] = 'B'
        # 口：牙の ならぶ さけた 口
        if open_:
            put(s, ['kkkkkkkkkk', 'kwPwPPwPwP', 'kPPPPPPPPP', 'kPwPPwPwkk', '.kkkkkkk..'], 38, 30)
        else:
            put(s, ['kkkkkkkkkk', '.wkwBwkwBw', '..B.B.B.B.'], 38, 32)
    def post2(g):
        dots(g, 'k', [(25, 12), (25, 11), (26, 10)])          # しん
        if open_:
            for y in range(30, 35): g[y][48] = 'k'
    return make(d, RAMP, lo=-.34, post=post, post2=post2)
def dish():
    """首の 燭台の 皿（真ちゅうの 輪）"""
    def d(p): poly(p, [(20, 35), (45, 35), (47, 37), (44, 39), (21, 39), (18, 37)], '2')
    def post(s):
        for x in range(18, 48):
            if s[35][x] != '.': s[35][x] = 'G'
        for x in range(22, 46, 4):
            if s[37][x] != '.': s[37][x] = 'H'
        dots(s, 'A', [(26, 38), (34, 38), (41, 38)])
    return make(d, RAMP, r=1, post=post)
# 霊火（3つの ゆらぎ ＋ 大きく 燃える ため）
FL0 = [
    ['....V.....', '...VbV....', '...VbbV...', '..VbcbV.V.', '..VbccbVb.', '.VbccccbV.', '.VbcOOcbV.', '..VbOObV..', '...VbbV...'],
    ['.....V....', '....VbV...', '...VbbV...', '.V.VbcbV..', '.bVbccbV..', '.VbccccbV.', '.VbcOOcbV.', '..VbOObV..', '...VbbV...'],
    ['....V.V...', '....bVb...', '...VbbbV..', '..VbccbV..', '..VbccbbV.', '.VbccccbV.', '.VbcOOcbV.', '..VbOObV..', '...VbbV...'],
]
FL = [
    ['.....V......', '....VbV.....', '....VbbV....', '...VbcbV..V.', '..VbccbV.Vb.', '..VbcccbVbV.', '.VbccwccbbV.', '.VbcccccccbV', '.VbccOOOccbV', '..VbcOOOcbV.', '...VbOOObV..', '....VbbbV...'],
    ['......V.....', '.....VbV....', '....VbbV....', '.V..VbcbV...', '.bV.VbccbV..', '.VbVbcccbV..', '.VbbccwccbV.', 'VbcccccccbV.', 'VbccOOOccbV.', '.VbcOOOcbV..', '..VbOOObV...', '...VbbbV....'],
    ['....V..V....', '....bVVb....', '...VbbbbV...', '..VbccccbV..', '..VbcccbbV..', '..VbccccbV..', '.VbccwcccbV.', '.VbcccccccbV', '.VbccOOOccbV', '..VbcOOOcbV.', '...VbOOObV..', '....VbbbV...'],
]
FL_BIG = ['..V...V...V..', '.VbV.VbV.VbV.', '.VbbVbbbVbbV.', 'VbccbbccbbcbV', 'VbcccccccccbV', 'VbcccwwwcccbV', 'VbccwwwwwccbV', 'VbcccwwwcccbV', '.VbccOOOccbV.', '.VbcOOOOOcbV.', '..VbcOOOcbV..', '...VbOOObV...', '....VbbbV....']
FL_KO = ['..C.', '.C..', '..C.', '.C..']
# 目：ろうの まゆ＋白い 光＋霊火の 虹彩（明 b・暗 V）＋たての ひとみ
EYE = ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwbbkbbk', '.kwbbVkVbk', '.kbVVVkVVk', '..kVVkkVk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAAAAAAAk', '.kkkkkkkkk', '.kBBBBBBBk', '..kBBBBBk.', '...kkkkk..'],
    'hit':   ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kkkAAAAkk', '.kAAkkkkAk', '.kBBBBBkkk', '..kkkBBBk.', '...kkkkk..'],
    'atk0|atk1|atk2': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwwckcwk', '.kwcccbccbk', '.kbbbbkbbk', '..kVVkkVk.', '...kkkkk..'],
    'ko':    ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAkAAAkAk', '.kAAkAkAAk', '.kBkBBBkBk', '..kBBBBBk.', '...kkkkk..'],
}

# ---------- ろうの 足（見せ所）：太く たれさがり、先が 丸まる。ろうの しずく ----------
def leg(path, rad, far=False, drips=()):
    def post(s):
        for (x, y) in drips:
            if s[y][x] != '.': s[y][x] = 'A'
        # 吸盤（下がわの 丸い 点）
        if not far:
            for i in range(1, len(path) - 1):
                x, y = path[i]
                for (dx, dy) in ((1, 1), (2, 2)):
                    if at(s, x + dx, y + dy) in 'BC' and at(s, x + dx + 1, y + dy + 1) != '.': s[y + dy][x + dx] = 'A' if dy == 1 else 'C'
    def post2(g):
        for (x, y) in drips:
            # たれた しずく（足に つながった まま）
            if g[y + 1][x] in 'k.': g[y + 1][x] = 'B'; g[y + 2][x] = 'C' if far else 'B'; g[y + 3][x] = 'k'
            for dx in (-1, 1):
                for dy in (1, 2):
                    if g[y + dy][x + dx] == '.': g[y + dy][x + dx] = 'k'
        for x, y in path[1:-1]:
            pass
    return make(lambda p: tube(p, path, rad, '1'), RAMP, r=1, dk=DARK if far else None, post=post, post2=post2)
LEGS = {
    'f1': ([(23, 37), (15, 43), (10, 46), (8, 42)], [3, 2.4, 1.8, 1.2], True, ()),
    'f2': ([(30, 38), (28, 47), (25, 52), (27, 56)], [3, 2.4, 1.8, 1.2], True, ()),
    'f3': ([(42, 37), (50, 41), (56, 41), (58, 37)], [3, 2.4, 1.8, 1.2], True, ()),
    'n1': ([(26, 38), (21, 47), (17, 53), (20, 57)], [3.6, 3, 2.2, 1.4], False, ((21, 48),)),
    'n2': ([(34, 38), (36, 48), (39, 54), (44, 55)], [3.6, 3, 2.2, 1.4], False, ((36, 49),)),
    'n3': ([(40, 38), (47, 45), (53, 48), (57, 45)], [3.4, 2.8, 2, 1.3], False, ()),
}
def legs(alt=0):
    out = {}
    for k, (path, rad, far, dr) in LEGS.items():
        if alt:
            # 攻撃：足先を 前へ のばす
            path = [path[0], (path[1][0] + 2, path[1][1] - 1), (path[2][0] + 4, path[2][1] - 3), (path[3][0] + 6, path[3][1] - 6)]
        out[k] = leg(path, rad, far, dr if not alt else ())
    return out
BALL = ['...VbbV...', '.VbbccbV..', 'Vbccwccbbb', 'bccwwwcccb', 'Vbccwccbbb', '.VbbccbV..', '...VbbV...']
BALL2 = ['..VbV..', '.Vbcbb.', 'Vbcwcbb', '.Vbcbb.', '..VbV..']

def layers():
    L = legs(); LA = legs(1); H = head(); HO = head(True)
    return [
        dict(n='f1', g='legB', x=0, y=0, rows=L['f1'], alt={'atk1|atk2': LA['f1']}),
        dict(n='f2', g='legA', x=0, y=0, rows=L['f2'], alt={'atk1|atk2': LA['f2']}),
        dict(n='f3', g='legB', x=0, y=0, rows=L['f3'], alt={'atk1|atk2': LA['f3']}),
        dict(n='flame', g='flame', x=20, y=2, rows=FL[0], alt={'idle1|walk1|blink': FL[1], 'idle2|walk2|hit': FL[2], 'idle3|walk3': FL[1]}, not_='atk0|atk1|ko'),
        dict(n='flameB', g='flame', x=19, y=0, rows=FL_BIG, only='atk0|atk1'),
        dict(n='flameK', g='flame', x=24, y=7, rows=FL_KO, only='ko'),
        dict(n='n1', g='legB', x=0, y=0, rows=L['n1'], alt={'atk1|atk2': LA['n1']}),
        dict(n='n2', g='legA', x=0, y=0, rows=L['n2'], alt={'atk1|atk2': LA['n2']}),
        dict(n='n3', g='legB', x=0, y=0, rows=L['n3'], alt={'atk1|atk2': LA['n3']}),
        dict(n='head', g='head', x=0, y=0, rows=H, alt={'atk1|atk2': HO}),
        dict(n='dish', g='dish', x=0, y=0, rows=dish()),
        dict(n='eye', g='head', x=36, y=20, rows=EYE, alt=EYE_ALT),
        dict(n='ball', g='root', x=52, y=18, rows=BALL, only='atk1'),
        dict(n='ball2', g='root', x=57, y=19, rows=BALL2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'head': (0, 1), 'legA': (0, 1)}, 'idle3': {'legB': (0, 1)}, 'blink': {},
    'walk0': {'root': (0, -1), 'legA': (1, 0)}, 'walk1': {'root': (0, -2), 'legB': (-1, 1)},
    'walk2': {'root': (0, -1), 'legA': (-1, 1)}, 'walk3': {'legB': (1, 0)},
    'atk0': {'root': (-2, 1), 'head': (-1, 0)},
    'atk1': {'root': (2, -1)},
    'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 0), 'flame': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'flame': 'head', 'head': 'dish', 'dish': 'root', 'legA': 'root', 'legB': 'root'}
