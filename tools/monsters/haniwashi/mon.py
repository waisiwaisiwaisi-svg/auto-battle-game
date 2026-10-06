# ハニワシ（じめん・ゴースト × ワシ）手打ち GBA風・デフォルメ（2〜3頭身：大きな はにわの 頭と かぎ形の くちばし、丸い 胴、短い 足、ひろげた 土の 翼）
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
META = dict(id='haniwashi', name='ハニワシ', types=['ground', 'ghost'], base='ワシ', size='M')
PAL = {
    'k': '#101018', 'l': '#3e1e1c',
    'A': '#f2b684', 'B': '#c46e44', 'C': '#7c3c2a',      # 素焼きの 土（明・中・暗）
    'E': '#fae0b4', 'F': '#c8a070',                      # くちばし・つめ（明・暗）
    'c': '#e4fff2', 'G': '#7cf0c8', 'V': '#2e9488',      # 霊の 光（白・みどり・濃い みどり）＝目の 虹彩
    'P': '#2a1428',                                      # はにわの 穴の 中
    'w': '#ffffff',
}
LIGHT = set('AEcw')
KEEP_BLACK = set('wcG')
RAMP = {'1': 'ABC', '2': 'EEF'}
DARK = {'A': 'B', 'B': 'C', 'E': 'F'}

def crack(s, pts, glow=True):
    """土の ひび（中から 霊の 光）"""
    for i in range(len(pts) - 1): line(s, *pts[i], *pts[i + 1], 'P')
    if glow:
        for (x, y) in pts[1:-1]: s[y][x] = 'G'

# ---------- 翼（土の 板の 羽根。ふちは ぎざぎざ）----------
def wing(far=False, up=0):
    def d(p):
        poly(p, [(24, 38), (30, 32), (24, 22), (16, 10 - up), (8, 6 - up), (4, 10 - up), (6, 18), (5, 22), (9, 26), (8, 30), (13, 33), (13, 37), (18, 40)], '1')
    def post(s):
        # 羽根の 段（3段の 板）
        for k0, (a, b) in enumerate((((7, 14), (24, 30)), ((9, 22), (22, 35)), ((12, 30), (20, 39)))):
            line(s, *a, *b, 'C')
            line(s, a[0] + 1, a[1] - 1, b[0] + 1, b[1] - 1, 'A')
        crack(s, [(12, 10 - up), (14, 14), (13, 18)])
    return make(d, RAMP, post=post, dk=DARK if far else None)
def wing_far(up=0):
    def d(p): poly(p, [(36, 32), (40, 22), (44, 10 - up), (49, 6 - up), (50, 12 - up), (47, 22), (44, 32)], '1')
    def post(s): line(s, 42, 20, 46, 12 - up, 'C')
    return make(d, RAMP, r=1, dk=DARK)

# ---------- 胴（小さく 丸い はにわの 筒）・尾・足 ----------
def body():
    def d(p):
        ellipse(p, 31, 42, 9, 8, '1')
        poly(p, [(24, 44), (14, 50), (13, 54), (24, 50)], '1')         # 尾羽（短い 板）
    def post(s):
        # 胸の はにわの 穴（丸い 穴）と 帯
        put(s, ['.PP.', 'PPPP', 'PGGP', '.PP.'], 32, 40)
        for x in range(23, 40):
            if s[47][x] in 'ABC': s[47][x] = 'C' if x % 3 else 'A'
        line(s, 16, 51, 23, 47, 'C')
    return make(d, RAMP, post=post)
def leg(x0, far=False):
    def d(p):
        tube(p, [(x0, 47), (x0 + 1, 55)], [3, 2.2], '2')
    def post2(g):
        # かぎ爪（3本）
        put(g, ['kkkkkkk.', 'kEkEkEk.', 'kEkEkFk.', '.k.k.kk.'], x0 - 2, 56)
        for x in range(x0 - 2, x0 + 5):
            if g[56][x] == 'k' and g[55][x] != '.': g[56][x] = 'F'
    return make(d, RAMP, r=1, dk=DARK if far else None, post2=post2)

# ---------- 頭（大きい はにわの 頭）＋ かぎ形の くちばし ----------
def head(open_=False):
    def d(p):
        ellipse(p, 38, 24, 11, 10, '1')
        poly(p, [(30, 16), (34, 9), (37, 15)], '1'); poly(p, [(36, 15), (41, 9), (43, 15)], '1')    # 冠の 羽（とがった）
    def post(s):
        # 目の まわりの 黒い ふち（ワシの 目の 筋 ⇔ はにわの 穴）
        line(s, 34, 28, 30, 30, 'P'); line(s, 34, 29, 31, 31, 'P')
        crack(s, [(30, 20), (32, 23), (31, 26)])
        line(s, 33, 11, 34, 15, 'C'); line(s, 40, 11, 40, 15, 'C')
    return make(d, RAMP, lo=-.34, post=post)
def beak(open_=False):
    def d(p):
        if open_:
            poly(p, [(44, 20), (52, 18), (58, 21), (60, 26), (58, 28), (55, 24), (46, 26)], '2')
            poly(p, [(45, 29), (54, 29), (56, 33), (46, 32)], '2')
        else:
            poly(p, [(44, 21), (52, 20), (58, 23), (60, 28), (59, 32), (56, 30), (54, 28), (46, 30)], '2')
    def post(s):
        if open_:
            for x in range(47, 55): s[27][x] = 'P' if s[27][x] == '.' else s[27][x]
        else: line(s, 46, 28, 54, 27, 'F')
    def post2(g):
        if open_:
            for y in range(26, 30):
                for x in range(46, 56):
                    if g[y][x] == '.': g[y][x] = 'P'
            dots(g, 'G', [(50, 27), (51, 28)])
        dots(g, 'k', [(51, 23)])                     # 鼻の あな
    return make(d, RAMP, r=1, post=post, post2=post2)
# 目：はにわの 穴の ふち（P）＋白い 光＋霊の 虹彩（明 G・暗 V）＋ひとみ（k）。まゆの 線で かこむ
EYE = ['kk.........', 'kkkk.......', '.kkkkkk....', '..kPPPPPkk.', '.kPwGGkGGPk', '.kPGVVkVGPk', '..kPPkkPPk.', '...kkkkkk..']
EYE_ALT = {
    'blink': ['kk.........', 'kkkk.......', '.kkkkkk....', '..kPPPPPkk.', '.kPPPPPPPPk', '.kkkkkkkkkk', '..kAAAAAAk.', '...kkkkkk..'],
    'hit':   ['kk.........', 'kkkk.......', '.kkkkkk....', '..kPPPPPkk.', '.kPGPPPPGPk', '.kPPGGGGPPk', '..kPPPPPPk.', '...kkkkkk..'],
    'atk0|atk1|atk2': ['kk.........', 'kkkk.......', '.kkkkkk....', '..kPPPPPkk.', '.kPwccwccPk', '.kPGGGkGGPk', '..kPVkkVPk.', '...kkkkkk..'],
    'ko':    ['kk.........', 'kkkk.......', '.kkkkkk....', '..kPPPPPkk.', '.kPVPPPVPPk', '.kPPPVPPPPk', '..kPVPVPPk.', '...kkkkkk..'],
}
# 霊の 光（はなれているのは 意図的：霊火の つぶ と 攻撃の 波）
WISP = ['.c.', 'cGc', '.V.']
WAVE = ['....GGcc', '..GGcc..', 'GGcc..G.', '..GGcc..', '....GGcc']

def layers():
    return [
        dict(n='wingF', g='wingB', x=0, y=0, rows=wing_far(), alt={'idle1|idle2|walk1|walk3|atk0': wing_far(2)}),
        dict(n='legF', g='legB', x=0, y=0, rows=leg(34, True)),
        dict(n='wing', g='wingA', x=0, y=0, rows=wing(), alt={'idle1|idle2|walk1|walk3|atk0': wing(False, 2)}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='leg', g='legA', x=0, y=0, rows=leg(28)),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='beak', g='head', x=0, y=0, rows=beak(), alt={'atk1|atk2': beak(True)}),
        dict(n='eye', g='head', x=34, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='wisp', g='fx', x=46, y=8, rows=WISP, only='idle1|idle3|walk1|walk3'),
        dict(n='wave', g='fx', x=56, y=25, rows=WAVE, only='atk1|atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 1), 'head': (-1, 1)},
    'atk1': {'root': (3, 0), 'head': (1, 0)},
    'atk2': {'root': (4, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'wingA': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingA': 'body', 'wingB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
