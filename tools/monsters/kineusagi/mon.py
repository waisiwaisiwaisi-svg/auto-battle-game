# キネウサギ（フェアリー・かくとう × ウサギ）手打ち GBA風・デフォルメ（2〜3頭身）
EYE_BOX = (29, 23, 9, 7)
META = dict(id='kineusagi', name='キネウサギ', types=['fairy', 'fighting'], base='ウサギ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1c2a',
    'F': '#fff6f6', 'G': '#ecd0dc', 'H': '#b48ca2',
    'A': '#eab474', 'B': '#b2723e', 'C': '#6a3c22',
    'R': '#ff3c52', 'D': '#a8142e',
    'P': '#ffa0d0',
    'Y': '#fff07a',
    'w': '#ffffff',
}
LIGHT = set('FAPYw')
import pix
from pix import grid, rows_of, outline, ellipse, poly, line, recolor


# ---- 下書きの 道具（あたりは 図形で、仕上げは 手で 打つ）----
def G(w, h): return grid(w, h)
def ell(g, cx, cy, rx, ry, ch): ellipse(g, cx, cy, rx, ry, ch); return g
def pl(g, pts, ch): poly(g, pts, ch); return g
def thick(g, pts, ch, w=2):
    """太い 線（尾・首などの あたり）"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for dx in range(w):
            for dy in range(w): line(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, ch)
    return g
def edge(g, mats, ch='k'):
    """素材の さかい目に 内側の 線（あとで エンジンが 濃い色に する）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if src[y][x] not in mats: continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and src[yy][xx] not in mats and src[yy][xx] not in '.k': g[y][x] = ch; break
    return g
def shade(g, ramps, hl=1, dk=2, dr=1):
    """光は 左上：上・左の ふち hl ドットは 明、下の ふち dk・右の ふち dr ドットは 暗"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, m):
        n = 0
        while n < 9 and 0 <= y + dy * (n + 1) < H and 0 <= x + dx * (n + 1) < W and src[y + dy * (n + 1)][x + dx * (n + 1)] == m: n += 1
        return n
    for y in range(H):
        for x in range(W):
            m = src[y][x]
            if m not in ramps: continue
            L, M, D = ramps[m]
            u, l, d, r = run(y, x, -1, 0, m), run(y, x, 0, -1, m), run(y, x, 1, 0, m), run(y, x, 0, 1, m)
            c = M
            if d < dk or r < dr: c = D
            elif u < hl or l < hl: c = L
            g[y][x] = c
    return g
def at(g, x, y, *rows):
    """手打ち：( x, y ) から 文字を 置く（空白と '.' は そのまま）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c not in ' .' and 0 <= y + j < len(g) and 0 <= x + i < len(g[y + j]): g[y + j][x + i] = c
    return g
def done(g, open_top=0, open_left=0):
    """輪郭を つける。付け根側の 輪郭を 開けて 体に なじませる"""
    rows = [list(r) for r in outline(rows_of(g))]
    for y in range(open_top): rows[y] = ['.' if c == 'k' else c for c in rows[y]]
    for r in rows:
        for x in range(open_left):
            if r[x] == 'k': r[x] = '.'
    return [''.join(r) for r in rows]
RAMP = {'f': 'wFG', 'a': 'ABC', 'r': 'RRD', 'p': 'PPG', 'b': 'wwF'}
DARKER = {'F': 'G', 'G': 'H', 'H': 'l', 'A': 'B', 'B': 'C', 'C': 'l', 'R': 'D', 'P': 'G'}
def dark(rows): return recolor(rows, DARKER)


# ---- 耳（見せ所）：根もとは 毛、先は 太い 杵（きね）の 木。なわの 帯 ----
import math
TIPS = {'back': (-11, -18), 'up': (-3, -22), 'fwd': (22, -6), 'down': (20, 10)}
def ear(d='back', tip=None):
    """根もと（16,16）から 先へ。根もとは 毛、先ほど 太い 杵の 木"""
    N = 48; g = G(N, N); bx, by = 24, 24
    tx, ty = tip or TIPS[d]; ln = math.hypot(tx, ty); ux, uy = tx / ln, ty / ln; px, py = -uy, ux
    ex, ey = bx + tx, by + ty
    pl(g, [(bx + px * 2.6, by + py * 2.6), (ex + px * 4, ey + py * 4), (ex - px * 4, ey - py * 4), (bx - px * 2.6, by - py * 2.6)], 'a')
    for y in range(N):
        for x in range(N):
            if g[y][x] != 'a': continue
            t = ((x + .5 - bx) * ux + (y + .5 - by) * uy)
            if t < 8: g[y][x] = 'f'
            elif abs(t - ln * .55) < 1.1: g[y][x] = 'r'
            elif t > ln - 1.6: g[y][x] = 'e'
    edge(g, 'f'); edge(g, 'r'); edge(g, 'e')
    shade(g, {'f': 'wFG', 'a': 'ABC', 'r': 'RRD', 'e': 'AAB'}, hl=1, dk=2, dr=2)
    for y in range(N):                                              # 木目（手打ちの 点）
        for x in range(N):
            if g[y][x] == 'B' and (x * 3 + y * 5) % 11 == 0: g[y][x] = 'C'
    ix, iy = int(bx + ux * 3 + px * .5), int(by + uy * 3 + py * .5)
    at(g, ix, iy, 'P'); at(g, int(ix + ux * 2), int(iy + uy * 2), 'P')                                              # 耳の 内側の ピンク
    return done(g)

# ---- 頭：丸く 大きい、赤い つり目、出っ歯と 牙 ----
def head(eye=None, ko=False, mouth=0):
    g = G(23, 20)
    ell(g, 11, 10, 10.5, 9, 'f')
    ell(g, 18, 13, 4.5, 4, 'b')                                     # 口もと
    shade(g, RAMP, hl=1, dk=3, dr=1)
    at(g, 21, 10, 'kP', '.k')                                       # 鼻
    at(g, 3, 12, 'GG'); at(g, 4, 14, 'G'); at(g, 5, 15, 'H')         # ほおの 毛
    if mouth: at(g, 14, 15, 'kkkkkkkk', 'kRRRRRRk', '.kwwkkk.', '..kk')
    else: at(g, 15, 15, 'kkkkkkk', '.kwwk..', '..kk...'); at(g, 21, 14, 'k')
    at(g, 9, 3, *(EYE_KO if ko else (eye or EYE)))                  # 目（C 三白眼）
    return done(g)
# 三白眼（C）：たてに 見開いた 白目の 上の まん中に、赤い 小さな 瞳が まぶたに 半分 かくれて 寄る（下と 左右が 白い）。下まぶたは 太く 赤く 血走る
EYE = ['kk.......',
       'lkkkkkkk.',
       'kGwRkRwwk',
       'kGwwRwwGk',
       'kDGwwwGDk',
       '.kDDDDDk.',
       '..kkkkk..']
EYE_BLINK = ['kk.......', 'lkkkkkkk.', 'kGGGGGGGk', '.kkkkkkk.', '..kDDDk..', '.........', '.........']
EYE_HIT = ['kk.......', 'lkkkk....', 'kGwkkkk..', '.kkwRwkk.', '..kDDDk..', '.........', '.........']     # ぎゅっと つぶり、瞳が 下へ ずれる
EYE_ATK = ['kk.......', 'lkkkkkkk.', 'kGwwkwwwk', 'kGwwRwwGk', 'kGwwwwwGk', 'kDDwwwDDk', '.kkDDDkk.']   # 白目を むいて 瞳が 点に
EYE_KO = ['kk.......', 'lkkkkkkk.', '.kGGGGk..', '..kGGk...', '..GkkG...', '.kG..Gk..', '.........']

# ---- 胴：小さく 丸い、赤い 帯（格闘の しるし）----
def body():
    g = G(19, 17)
    ell(g, 9.5, 9, 9, 8, 'f')
    ell(g, 13, 10, 4, 5.5, 'b')
    pl(g, [(0, 10), (19, 8), (19, 11), (0, 13)], 'r')               # 帯
    edge(g, 'r')
    shade(g, RAMP, hl=1, dk=3, dr=2)
    at(g, 3, 11, 'kk'); at(g, 2, 13, 'kRk', 'kD')                   # 帯の むすび目
    return done(g)

# ---- 腕：短く、さらしを まいた こぶし ----
FIST = ['.kkkk.....', 'kFFGGkkkk.', 'kGGGkFFFGk', '.kkkkFGkGk', '....kGGkGk', '....kkkkk.']
FIST_PUNCH = ['.kkkkkkkk.....', 'kFFGGGGGkkkkk.', 'kGGGGGGkFFFFGk', '.kkkkkkkFGkGkGk', '.......kGGkGGk', '.......kkkkkk.']
# ---- 足：ウサギの 長い 足 ----
LEG_M = ['.ffffff....', 'fffffff....', 'fffffff....', '.fffff.....', '.ffffffff..', 'fffffffffff']
def leg():
    g = pix.grid_of(LEG_M); shade(g, RAMP, dk=1)
    at(g, 5, 2, 'H')
    r = done(g, open_top=2)
    return r
TAIL = ['.kkk.', 'kFFGk', 'kFGGk', 'kGGHk', '.kkk.']

# ---- 衝撃（エフェクト：はなれて いるのは 意図的）----
POW = ['....k....', '...kYk...', 'k..kYk..k', '.kkYwYkk.', 'kYYwwwYYk', '.kkYwYkk.', 'k..kYk..k', '...kYk...', '....k....']
SPARK = ['.k.', 'kPk', '.k.']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='earB', g='earB', x=-1, y=-1, rows=dark(ear(tip=(-18, -10))), alt={'atk0': dark(ear(tip=(-8, -20))), 'atk1': dark(ear(tip=(21, -9))), 'atk2': dark(ear(tip=(22, 17)))}),
        dict(n='tail', g='body', x=11, y=44, rows=TAIL),
        dict(n='legF', g='legB', x=16, y=52, rows=dark(leg())),
        dict(n='armF', g='armB', x=32, y=40, rows=dark(FIST)),
        dict(n='body', g='body', x=14, y=37, rows=body()),
        dict(n='leg', g='legA', x=24, y=52, rows=leg()),
        dict(n='earD', g='ear', x=5, y=0, rows=ear(tip=(25, 14)), only='atk2'),
        dict(n='head', g='head', x=19, y=19, rows=head(),
             alt={'blink': head(EYE_BLINK), 'hit': head(EYE_HIT), 'atk0': head(EYE_ATK), NB: head(EYE_ATK, mouth=1), 'ko': head(ko=True)}),
        dict(n='ear', g='ear', x=4, y=0, rows=ear(), alt={'atk0': ear('up'), 'atk1': ear('fwd')}, not_='atk2'),
        dict(n='arm', g='armA', x=28, y=41, rows=FIST, alt={NB: FIST_PUNCH}),
        dict(n='pow', g='fx', x=54, y=37, rows=POW, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'ear': (0, 1), 'earB': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1), 'armA': (0, 1), 'armB': (0, 1)}, 'idle3': {'body': (0, 1), 'armA': (0, 1), 'armB': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'armA': (0, -1), 'armB': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'armA': (0, -1), 'armB': (0, -1), 'ear': (0, 1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 1), 'armA': (-2, 0)},
    'atk1': {'root': (3, 0)}, 'atk2': {'root': (4, 0), 'armA': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'ear': (-2, 0), 'earB': (-2, 0)},
    'ko': {'_flip': True},
}
PARENT = {'ear': 'head', 'earB': 'head', 'head': 'body', 'armA': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
