# キノコモリ（くさ・どく × コウモリ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：毒キノコの かさの 翼（翼膜の 骨 ⇔ かさの うらの ひだ）
EYE_BOX = (36, 18, 10, 6)
META = dict(id='kinokomori', name='キノコモリ', types=['grass', 'poison'], base='コウモリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c1632',
    'A': '#b896cc', 'B': '#7a5492', 'D': '#46305c',      # 毛（すみれ色）
    'P': '#ee6a9a', 'p': '#a02a62',                      # 毒キノコの かさ
    'S': '#f6e8c4', 'T': '#c8a47a',                      # かさの うらの ひだ
    'G': '#c4f466', 'g': '#5ea432',                      # 毒の 胞子・目
    'w': '#ffffff', 'x': '#060208',                      # 目の 黒い 強膜
}
LIGHT = set('ASPGw')
KEEP_BLACK = set('wGgx')
# ---------- 下書きの 道具（あたり → 左上光の 3段 → 輪郭。目・牙・模様・線は 手で 打つ）----------
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, poly, line
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def E(g, cx, cy, rx, ry, ch='1'): ellipse(g, cx, cy, rx, ry, ch)
def P(g, pts, ch='1'): poly(g, pts, ch)
def Ln(g, x0, y0, x1, y1, ch): line(g, x0, y0, x1, y1, ch)
def dots(g, ch, pts, on=None):
    """手で 1ドットずつ 打つ（on を 指定すると その 色の 上だけ）"""
    for x, y in pts:
        if 0 <= x < N and 0 <= y < N and (on is None or g[y][x] in on): g[y][x] = ch
def hand(g, x, y, rows):
    """手打ちの 絵（文字の 行）を はりつける。'.' は すける"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= x + i < N and 0 <= y + j < N: g[y + j][x + i] = c
def shade(g, ramps, lw=1, dw=2):
    """マスクに 光（左上）：上・左の ふち lw は 明、下・右の ふち dw は 暗"""
    src = [r[:] for r in g]
    for y in range(N):
        for x in range(N):
            m = src[y][x]
            if m not in ramps: continue
            Lc, Mc, Dc = ramps[m]
            def run(dy, dx):
                i = 1
                while i < 9 and at(src, x + dx * i, y + dy * i) == m: i += 1
                return i
            dr = min(run(1, 0), run(0, 1) + 1); ul = min(run(-1, 0), run(0, -1))
            g[y][x] = Dc if dr <= dw else Lc if ul <= lw else Mc
def part(draw, ramps, lw=1, dw=2, post=None, cut=()):
    """1つの パーツ：draw で 形 → 陰影 → post で 手打ち → 輪郭。cut の 四角では 輪郭を 開けて 体と つなぐ"""
    g = G(); draw(g); shade(g, ramps, lw, dw)
    if post: post(g)
    rows = [list(r) for r in outline(rows_of(g))]
    for (x0, y0, x1, y1) in cut:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if rows[y + 1][x + 1] == 'k' and at(g, x, y) == '.': rows[y + 1][x + 1] = '.'
    return [''.join(r) for r in rows]
def L(n, gr, rows, **kw): return dict(n=n, g=gr, x=-1, y=-1, rows=rows, **kw)
def H(n, gr, x, y, rows, **kw): return dict(n=n, g=gr, x=x, y=y, rows=rows, **kw)
import math
FUR = {'1': 'ABD'}
# ---- 翼＝毒キノコの かさ：前の ふち（腕の 骨）が 斑点の かさ、
#      手首から 放射に のびる 指の 骨と 膜 ⇔ かさの うらの ひだ ----
def wing(ang=0, dark=False, sx=30, sy=33):
    def tf(pts):
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        return [(sx + (x - sx) * c - (y - sy) * s_, sy + (x - sx) * s_ + (y - sy) * c) for x, y in pts]
    wr = tf([(14, 14)])[0]
    tips = tf([(1, 22), (3, 33), (12, 42)])
    def d(g):
        # 膜（ひだ）：手首 → 指先、指の 間は 内へ へこむ
        P(g, tf([(31, 31), (14, 14), (1, 22), (7, 26), (3, 33), (10, 35), (12, 42), (18, 39), (28, 43), (33, 38)]), '8')
        # かさ（腕の 骨の 上の ドーム）
        P(g, tf([(32, 32), (27, 22), (20, 13), (12, 8), (5, 9), (0, 14), (0, 22), (6, 17), (13, 15), (21, 21), (28, 31)]), '9')
    def p(g):
        for y in range(N):
            for x in range(N):
                c = g[y][x]
                if c == '9':
                    up = at(g, x, y - 1) == '.' or at(g, x - 1, y) == '.' or at(g, x, y - 2) == '.'
                    dn = at(g, x, y + 1) not in '9' or at(g, x + 1, y) not in '9'
                    g[y][x] = 'p' if dark else ('P' if up and not dn else 'p' if dn else 'P')
                elif c == '8': g[y][x] = 'T' if dark else 'S'
        # ひだ（放射の すじ）と 指の 骨
        edge = tf([(1, 22), (7, 26), (3, 33), (10, 35), (12, 42), (18, 39), (28, 43)])
        seg = list(zip(edge, edge[1:]))
        for i in range(13):
            t = i / 12 * len(seg); j = min(int(t), len(seg) - 1); f = t - j
            (x0, y0), (x1, y1) = seg[j]; ex, ey = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
            Ln(g, round(wr[0]), round(wr[1]), round(ex), round(ey), 'T' if not dark else 'B')
        # 膜の 右下は 影
        for y in range(N):
            for x in range(N):
                if g[y][x] == 'S' and (at(g, x, y + 1) == '.' or at(g, x + 1, y) == '.' or at(g, x, y + 2) == '.'): g[y][x] = 'T'
        for tx, ty in tips:
            Ln(g, round(wr[0]), round(wr[1]), round(tx), round(ty), 'B' if not dark else 'D')
            dots(g, 'w', [(round(tx), round(ty))])
        # かさの 斑点（手で 置く）
        for (x, y) in tf([(8, 11), (15, 13), (22, 19), (4, 15), (26, 26)]):
            dots(g, 'w' if not dark else 'P', [(round(x), round(y)), (round(x) + 1, round(y))], 'Pp')
        # 手首の かぎ爪
        hand(g, round(wr[0]) - 1, round(wr[1]) - 3, ['.w', 'wk'] if not dark else ['.T', 'Tk'])
    return part(d, {}, post=p)
W_FAR = wing(0, True, 36, 30); W_FAR_UP = wing(14, True, 36, 30); W_FAR_DN = wing(-16, True, 36, 30)
W_NEAR = wing(0); W_NEAR_UP = wing(16); W_NEAR_DN = wing(-18)
# ---- 胴（小さく 丸い）と 足 ----
def body_d(g): E(g, 33, 40, 7, 7)
def body_p(g):
    for (x, y) in ((33, 37), (35, 39), (32, 41), (34, 43)): dots(g, 'A', [(x, y)], 'B')
    Ln(g, 28, 44, 37, 44, 'D')
BODY = part(body_d, FUR, dw=2, post=body_p)
def foot(x):
    def d(g): P(g, [(x, 44), (x + 3, 44), (x + 3, 49), (x + 4, 51), (x - 1, 51), (x, 49)])
    def p(g): dots(g, 'w', [(x - 1, 51), (x + 2, 51)])
    return part(d, {'1': 'BDD'}, post=p)
FOOT_A = foot(35); FOOT_B = foot(29)
# ---- 頭（とがった 大きい 耳、鼻の 葉、毒の 牙）----
def head_d(g):
    E(g, 38, 24, 10, 8.5)
    P(g, [(31, 19), (29, 6), (37, 16)]); P(g, [(39, 16), (45, 5), (46, 19)])
    P(g, [(45, 21), (50, 23), (50, 28), (45, 29)])
def head_p(g, open_=False):
    # 耳の 内がわ
    Ln(g, 31, 15, 30, 9, 'p'); Ln(g, 32, 16, 31, 11, 'p'); Ln(g, 43, 15, 45, 9, 'p'); Ln(g, 42, 16, 44, 11, 'p')
    # 鼻の 葉（とがる）
    dots(g, 'D', [(49, 24), (48, 25), (49, 26)]); dots(g, 'A', [(46, 22), (47, 22)], 'B')
    # 口と 牙（毒の しずく）
    if not open_:
        hand(g, 39, 28, ['kkkkkkkkk', '.kwk..kwk', '..w....w.', '.......G.'])
    else:
        hand(g, 38, 27, ['kkkkkkkkkk', 'kwkpppkwkk', 'kpppppppk.', '.kwkkkwk..', '..G...G...'])
    dots(g, 'D', [(x, 32) for x in range(30, 46)], 'AB')
HEAD = part(head_d, FUR, lw=1, dw=2, post=head_p)
HEAD_OPEN = part(head_d, FUR, lw=1, dw=2, post=lambda g: head_p(g, True))
# ---- 目：黒い 強膜（F）。白目の かわりに まっ黒な 目（x）、その 中に 毒の 黄緑の 細い たて瞳（G、にじみ g）。
#      光は 左上に 小さく 1点（つやの ある 黒） ----
EYE = ['kkk.......', '.kkkkkkk..', '.kwxxgGxkk', '..kxxgGxxk', '..kxxxGxk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['kkk.......', '.kkkkkkk..', '.kBBBBBBkk', '..kkkkkkkk', '...kkkkk..', '..........'],
    'atk0|atk1|atk2': ['kkk.......', '.kkkkkkk..', '.kwxgGGgkk', '..kxgGGgxk', '..kxxgGxk.', '...kkkkk..'],
    'hit': ['kkk.......', '.kkkkkkk..', '.kBBBBBBkk', '..kxxxgxxk', '..kkkkkkk.', '..........'],
    'ko': ['kkk.......', '.kkkkkkk..', '.kxgxxgxkk', '..kxxgxxxk', '..kxgxxgk.', '...kkkkk..'],
}
# ---- 毒の 胞子（翼の ふちから こぼれる：はなれた つぶ＝意図的）----
SPORE1 = ['.G...', 'GgG..', '.G..G', '...Gg', '.G.....', 'GgG..']
SPORE2 = ['...G.', '..GgG', 'G..G.', 'gG...', '...G.', '..GgG']
CLOUD = [
    '....kkk.......',
    '..kkGGGkkk....',
    '.kGGGgGGGGk...',
    'kGGwGGGgGGGkk.',
    'kGgGGGGGGwGGGk',
    '.kGGGgGGGGGgGk',
    '..kkGGGGgGGkk.',
    '....kkkkkkk...',
]
CLOUD2 = ['.G..kkk..G', 'G.kkGGGkk.', '.kGgGGGgGk', 'kGGGwGGGGk', '.kgGGGgGk.', 'G.kkkkkk.G']

def layers():
    return [
        H('wfar', 'wfar', 3, -6, W_FAR, alt={'idle1|walk1|walk2|atk0': W_FAR_UP, 'walk3|atk1': W_FAR_DN}),
        L('footB', 'body', FOOT_B),
        L('body', 'body', BODY),
        L('footA', 'body', FOOT_A),
        L('head', 'head', HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        H('eye', 'head', 36, 18, EYE, alt=EYE_ALT),
        L('wnear', 'wnear', W_NEAR, alt={'idle1|walk1|walk2|atk0': W_NEAR_UP, 'walk3|atk1': W_NEAR_DN}),
        H('sp', 'wnear', 3, 40, SPORE1, alt={'idle2|idle3|walk2|walk3': SPORE2}, not_='atk1|atk2|hit|ko'),
        H('cloud', 'root', 52, 26, CLOUD, only='atk1'),
        H('cloud2', 'root', 54, 27, CLOUD2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1)}, 'idle3': {},
    'blink': {},
    'walk0': {}, 'walk1': {'root': (0, -2)}, 'walk2': {'root': (0, -1)}, 'walk3': {'root': (0, 1)},
    'atk0': {'root': (-2, 0), 'head': (-1, 1)}, 'atk1': {'root': (3, 1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, 1)},
    'ko': {'_flip': True, 'root': (0, 6)},
}
PARENT = {'head': 'body', 'wfar': 'body', 'wnear': 'body', 'body': 'root'}
