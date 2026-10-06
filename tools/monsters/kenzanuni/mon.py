# ケンザンウニ（はがね・みず × ウニ）手打ち GBA風・デフォルメ（まるい 体＝頭）
META = dict(id='kenzanuni', name='ケンザンウニ', types=['steel', 'water'], base='ウニ', size='S')
PAL = {
    'k': '#101018', 'l': '#221a36',
    'S': '#f2f6fc', 'T': '#a4aec8', 'U': '#5a6284',
    'P': '#d886d6', 'Q': '#a2509e', 'R': '#6c2c74',
    'G': '#7c8a9c', 'H': '#434c60',
    'C': '#94f6ff', 'E': '#2896d0',
    'w': '#ffffff',
}
LIGHT = set('SPGCw')
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
import math
CX, CY, RX, RY = 22, 26, 15, 12.5

def needles(g, scale=1.0, short=False):
    """剣山の 針：ドームの 上に まっすぐ びっしり 並び、外側ほど 外へ ひらく（ウニの とげ）"""
    for x0 in range(CX - 15, CX + 13, 3):
        t = (x0 + 1 - CX) / RX
        if abs(t) >= 1: continue
        ys = CY - RY * math.sqrt(1 - t * t)
        L = (13 - 6 * abs(t) ** 1.5) * scale * (0.6 if short else 1)
        if x0 > CX + 6: L *= .55                                   # 顔の 上は 短く
        lean = t * 8 * scale
        y0 = int(ys + 3); y1 = int(ys - L); x1 = int(round(x0 + lean))
        line(g, x0, y0, x1, y1, 'S'); line(g, x0 + 1, y0, x1 + 1, y1, 'T')
        g[y1][x1 + 1] = '.'                                        # 先は 1ドットに とがる
        if 0 <= y1 + 1 < len(g): g[y1 + 1][x1 + 1] = 'U' if g[y1 + 1][x1 + 1] == 'T' else g[y1 + 1][x1 + 1]
    for deg, L in ((165, 8), (182, 9), (199, 7)):                  # 後ろ（左）に ひらく とげ
        a = math.radians(deg); L *= scale * (0.6 if short else 1)
        sx, sy = CX + (RX - 3) * math.cos(a), CY - (RY - 3) * math.sin(a)
        ex, ey = CX + (RX + L) * math.cos(a), CY - (RY + L * .5) * math.sin(a)
        line(g, int(sx), int(sy), int(ex), int(ey), 'S'); line(g, int(sx), int(sy) + 1, int(ex) + 1, int(ey) + 1, 'T')

def body(scale=1.0, short=False, eye='open', mouth=0):
    g = G(46, 40)
    needles(g, scale, short)
    d = G(46, 40); ell(d, CX, CY, RX, RY, 'p')
    for y in range(40):
        for x in range(46):
            if d[y][x] == 'p':
                g[y][x] = 'i' if y >= 33 else 'p'
    for x in range(CX - 13, CX + 14):                              # 剣山の 台（重い 鉄の ふち、下は 平ら）
        for y in (38, 39):
            if abs(x - CX) < 13 - (y - 38) * 2: g[y][x] = 'i'
    edge(g, 'i')
    shade(g, {'p': 'PQR', 'i': 'GHH'}, hl=1, dk=2, dr=2)
    for x in range(CX - 10, CX + 11, 4): at(g, x, 35, 'S')   # 台の 鋲（びょう）
    # とげの 付け根の いぼ（ウニの 殻の もよう・手打ち）
    for x, y in ((11, 23), (14, 26), (17, 22), (10, 29), (15, 30), (20, 25), (13, 20)): at(g, x, y, 'P'); at(g, x + 1, y + 1, 'R')
    # 目：2つ 光る（白い 光＋水色 2段の 虹彩＋ひとみ）、まゆの 線
    if eye == 'open': e1, e2 = ['kkk....', '.kkkkkk', 'kwCCkEk', 'kCCEkEk', 'kEEEkEk', '.kkkkk.'], ['kk...', '.kkkk', 'kwCkk', 'kCEkk', 'kEEkk', '.kkk.']
    elif eye == 'atk': e1, e2 = ['kkk....', '.kkkkkk', 'kwwCkCk', 'kwCCkEk', 'kCCEkEk', '.kkkkk.'], ['kk...', '.kkkk', 'kwwkk', 'kwCkk', 'kCCkk', '.kkk.']
    elif eye == 'blink': e1, e2 = ['kkk....', '.kkkkkk', 'kQQQQQk', 'kkkkkkk', '.RRRRR.', '.......'], ['kk...', '.kkkk', 'kQQQk', 'kkkkk', '.RRR.', '.....']
    elif eye == 'hit': e1, e2 = ['k......', '.kkk...', 'kQQkkkk', 'kkkkQQk', '.......', '.......'], ['k....', '.kk..', 'kQkkk', 'kkkQk', '.....', '.....']
    else: e1, e2 = ['k...k..', '.k.k...', '..k....', '.k.k...', 'k...k..', '.......'], ['k..k.', '.kk..', '.kk..', 'k..k.', '.....', '.....']
    at(g, 21, 18, *e1); at(g, 31, 18, *e2)
    # 口：ちょうちん形の 牙（ウニの 口の 5本の 歯）
    if mouth: at(g, 25, 25, 'kkkkkkkkk', 'kwkwkwkwk', 'kRRRRRRRk', 'kRRRRRRRk', '.kwkwkwk.', '..kkkkk..')
    else: at(g, 25, 26, 'kkkkkkkkk', 'kwkwkwkwk', '.kRwRwRk.', '..kkkkk..')
    return done(g)

def foot(dark=False):
    g = G(5, 7); thick(g, [(1, 0), (1, 4)], 'p', 3); ell(g, 2.5, 5.5, 2.5, 1.5, 'a')
    shade(g, {'p': 'PQR', 'a': 'PPQ'}, dk=1)
    r = done(g, open_top=2)
    return recolor(r, {'P': 'Q', 'Q': 'R'}) if dark else r

def splash(big=False):
    """水の しぶき（エフェクト：はなれて いるのは 意図的）"""
    if big: return ['..kk.....', '.kCCk.kk.', 'kCwCk.kCk', 'kCCEk..k.', '.kEk..kk.', '..k..kCEk', '.kk...kk.', 'kCEk.....', '.kk......']
    return ['.kk...', 'kCCk..', 'kCEk.k', '.kk.kC', '....kE', '.kk..k', 'kCEk..', '.kk...']
def volley():
    """飛ぶ 鉄の 針（エフェクト）"""
    return ['kkkkkkkk.....', 'kTTTTTTSk....', 'kkkkkkkk.....', '.............', '..kkkkkkkk...', '..kTTTTTTSk..', '..kkkkkkkk...', '.............', 'kkkkkkkk.....', 'kTTTTTTSk....', 'kkkkkkkk.....']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='f1', g='legB', x=18, y=50, rows=foot(True)),
        dict(n='f2', g='legA', x=23, y=51, rows=foot()),
        dict(n='f3', g='legB', x=30, y=51, rows=foot(True)),
        dict(n='f4', g='legA', x=35, y=50, rows=foot()),
        dict(n='body', g='body', x=8, y=12, rows=body(),
             alt={'blink': body(eye='blink'), 'hit': body(.8, eye='hit'), 'atk0': body(1.12, eye='atk'),
                  'atk1': body(1.25, eye='atk', mouth=1), 'atk2': body(.9, eye='atk', mouth=1), 'ko': body(.9, eye='ko')}),
        dict(n='spl', g='fx', x=56, y=40, rows=splash(True), only='atk1'),
        dict(n='vol', g='fx', x=52, y=24, rows=volley(), only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'root': (0, -1), 'body': (0, -1)}, 'idle3': {'root': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'root': (1, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'root': (0, 0)},
    'atk0': {'body': (-2, 2), 'legA': (-1, 0), 'legB': (-1, 0)}, 'atk1': {'root': (5, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 0)},
    'ko': {'_flip': True},
}
PARENT = {'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
