# ライウンクラゲ（でんき・かぜ × クラゲ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：積乱雲の かさ（傘の ふくらみ ⇔ もこもこの 雲）
META = dict(id='raiunkurage', name='ライウンクラゲ', types=['elec', 'wind'], base='クラゲ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c3050',
    'A': '#ffffff', 'B': '#d2daf0', 'D': '#8a92b8', 'E': '#474e78',   # 雲（白 → 嵐の 灰）
    'Y': '#fff27a', 'y': '#f2b630', 'g': '#a0601a',                   # 稲妻の 触手・目
    'w': '#ffffff', 'C': '#9cf6ff', 'c': '#3ca8d8',                   # 光・電気・風
    'r': '#b01c3c',
}
LIGHT = set('AYwC')
KEEP_BLACK = set('wYr')
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

CL = {c: 'ABD' for c in '12345'}; CL['6'] = 'DEE'
MASK = []
# ---- かさ＝積乱雲（もこもこの 半球が 上に もり上がる）。ふくらみごとに 光と 影 ----
def bell_d(g):
    E(g, 30, 25, 19, 4, '1'); E(g, 21, 21, 9, 8, '1'); E(g, 39, 18, 10, 9, '2'); E(g, 29, 12, 9, 8.5, '3')
    E(g, 14, 25, 6, 5, '5'); E(g, 45, 24, 7, 6, '4')
    P(g, [(9, 27), (52, 27), (50, 30), (11, 30)], '6')
    MASK[:] = [r[:] for r in g]
def bell_p(g, hot=False):
    # ふくらみの さかい目に 線（左上の ふちは 明るく）
    for y in range(1, N):
        for x in range(1, N):
            m = MASK[y][x]
            if m == '.': continue
            if MASK[y - 1][x] not in ('.', m) and m != '6' or MASK[y][x - 1] not in ('.', m) and MASK[y][x - 1] > m: g[y][x] = 'D'
    # 下の ふち：クラゲの 傘の ひだ（ぎざぎざ）
    for x in range(10, 52):
        if at(g, x, 27) != '.': g[27][x] = 'l'
        if x % 3 == 0: dots(g, 'B', [(x, 28)], 'DE')
    # 雲の 中で 光る 電気（ひび）
    pts = [(27, 9), (28, 10), (27, 11), (28, 12), (29, 13)]
    if hot: pts += [(20, 17), (21, 18), (20, 19), (21, 20), (36, 12), (37, 13), (13, 23), (14, 24)]
    dots(g, 'Y' if hot else 'C', pts, 'ABD')
    hand(g, 39, 23, ['kkkkkkkkkk', 'kwkwkwkwkk', '.k.k.k.kk.'])
def bell_open(g):
    bell_p(g, True)
    hand(g, 39, 23, ['kkkkkkkkkk', 'kwkwkwkwkk', 'krrrrrrrk.', '.kwkwkwk..'])
BELL = part(bell_d, CL, lw=2, dw=2, post=bell_p)
BELL_HOT = part(bell_d, CL, lw=2, dw=2, post=lambda g: bell_p(g, True))
BELL_OPEN = part(bell_d, CL, lw=2, dw=2, post=bell_open)
# 風の うず（かさの 後ろの 雲が 渦を 巻いて のびる：手打ち）
WIND = ['..kkkk.......', '.kCccCkk.....', 'kCkkkkcCkk...', 'kck.kCkcCCk..', 'kCkkCck.kcCCk', '.kccck...kkcC', '..kkk......kk']
WIND2 = ['...kkkk......', '..kCccCkk....', '.kCkkkkcCkk..', '.kck.kCkcCCk.', '.kCkkCck.kcCC', '..kccck...kkc', '...kkk.......']
# ---- 稲妻の 触手（つけ根は かさの 底に 3ドット もぐる）----
def tents(ph=0):
    def d(g):
        for i, (x, ln) in enumerate(((14, 49), (23, 55), (32, 53), (41, 56))):
            s = 1 if ph % 2 else -1
            pts = [(x, 28), (x + 3 * s, 34), (x - 1 * s, 38), (x + 3 * s, 44), (x - 1 * s, 49), (x + 2 * s, ln)]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                for o in (0, 1, 2): Ln(g, x0 + o, y0, x1 + o, y1, '7')
    def p(g):
        for y in range(N):
            for x in range(N):
                if g[y][x] == 'Y' and at(g, x + 1, y) in 'yg' and (x + y) % 5 == 0: g[y][x] = 'w'
    return part(d, {'7': 'Yyg'}, lw=1, dw=1, post=p)
T0, T1 = tents(0), tents(1)
# ---- 目：白い 光＋金の 虹彩（明 Y・暗 y）＋ひとみ。V字の まゆ ----
EYE_L = ['kkk....', '.kkkkkk', '.kwYYkk', '..kyykk', '...kkk.']
EYE_R = ['....kkk', 'kkkkkk.', 'kwYYkk.', '.kyykk.', '..kkk..']
EYE_L_ALT = {'blink': ['kkk....', '.kkkkkk', '..kkkk.'], 'hit': ['kk.....', '..kk...', '....kk.', '..kk...'],
             'atk0|atk1|atk2': ['kkkk...', '.kkkkkk', '.kwwYkk', '..kyykk', '...kkk.'], 'ko': ['k...k.', '.k.k..', '..k...', '.k.k..', 'k...k.']}
EYE_R_ALT = {'blink': ['....kkk', 'kkkkkk.', '.kkkk..'], 'hit': ['.....kk', '...kk..', '.kk....', '...kk..'],
             'atk0|atk1|atk2': ['...kkkk', 'kkkkkk.', 'kwwYkk.', '.kyykk.', '..kkk..'], 'ko': ['k...k.', '.k.k..', '..k...', '.k.k..', 'k...k.']}
# ---- 攻撃：触手から 前へ 落ちる 雷（はなれた エフェクト＝意図的）----
BOLT = [
    'kk..........',
    'kCkk........',
    '.kwCk.......',
    '..kwCkk.....',
    '..kCwwCk....',
    '...kkCwCk...',
    '....kCwk....',
    '...kCwkkk...',
    '...kwwwwCk..',
    '....kkCwwCk.',
    '.....kCwCk..',
    '....kCwk....',
    '....kwCkkk..',
    '...kwwwwwCk.',
    '...kkkCwwCk.',
    '.....kCwCk..',
    '....kCwkk...',
    '...kCwk.....',
    '..kwwk......',
    '..kkk.......',
]
def limp_d(g):
    for x0, x1 in ((12, 2), (22, 16), (40, 46), (47, 58)):
        for o in (0, 1): Ln(g, x0, 57 + o, x1, 59 + o - (1 if x1 > x0 else 0), '7')
LIMP = part(limp_d, {'7': 'Yyg'})
SPARK = ['k.k.k', '.kCk.', 'kCwCk', '.kCk.', 'k.k.k']

def layers():
    return [
        H('wind', 'bell', 2, 16, WIND, alt={'idle1|idle3|walk1|walk3': WIND2}),
        L('tent', 'tent', T0, not_='ko', alt={'idle2|idle3|walk1|walk3|atk1': T1}),
        L('bell', 'bell', BELL, alt={'atk0|idle1': BELL_HOT, 'atk1|atk2': BELL_OPEN}),
        H('eyeL', 'bell', 33, 16, EYE_L, alt=EYE_L_ALT),
        H('eyeR', 'bell', 42, 16, EYE_R, alt=EYE_R_ALT),
        L('limp', 'root', LIMP, only='ko'),
        H('bolt', 'root', 45, 38, BOLT, only='atk1'),
        H('spk', 'root', 47, 50, SPARK, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'bell': (0, 1)}, 'idle2': {'root': (0, 1)}, 'idle3': {'root': (0, 1), 'bell': (0, -1)},
    'blink': {},
    'walk0': {'root': (0, -1)}, 'walk1': {'root': (1, -2), 'tent': (-1, 0)}, 'walk2': {'root': (0, -1)}, 'walk3': {'root': (1, 0), 'tent': (-1, 0)},
    'atk0': {'bell': (0, 2), 'tent': (-1, 1)}, 'atk1': {'root': (3, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'bell': (-1, 1)},
    'ko': {'bell': (0, 28)},
}
PARENT = {'bell': 'root', 'tent': 'root'}
