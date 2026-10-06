# クロヤタ（あく・かぜ × 三本足の カラス）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

META = dict(id='kuroyata', name='クロヤタ', types=['dark', 'wind'], base='三本足の カラス', size='M')
PAL = {
    'k': '#101018', 'l': '#262444',
    'R': '#7c80c0', 'Q': '#3c3e6a', 'P': '#24243e',      # 黒い 羽（青むらさきの つや）
    'S': '#d6d6e0', 'T': '#8c8ca0', 'U': '#4c4c60',      # 鉄の くちばし・足
    'r': '#ff2a3c', 'Y': '#ffd862',                      # 赤い 目
    'v': '#b070f0', 'm': '#5c2c90',                      # 影の もや
    'c': '#dce6ff',                                      # 風
}
LIGHT = set('RSYvc')
KEEP_BLACK = set('S')
RAMP = {'1': 'RQP', '4': 'STU', '5': 'vmm', '6': 'QPP'}

# ---------- 下書き用の 小道具 ----------
def G(): return grid(64, 64)
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def put(g, x, y, rows): stamp(g, rows, x, y)
def stroke(g, x0, y0, x1, y1, r0, r1, ch, tipch=None, tipt=.8):
    """先が 細くなる 筆（羽の あたり用）"""
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n * 2 + 1):
        t = i / (n * 2); cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t; r = r0 + (r1 - r0) * t
        for y in range(int(cy - r - 2), int(cy + r + 3)):
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + .3 and 0 <= y < len(g) and 0 <= x < len(g[0]):
                    g[y][x] = tipch if (tipch and t >= tipt) else ch
def ink(g, p):
    """p（下書きの 1パーツ）を 黒の ふちごと g に 重ねる。下の パーツとの さかいに 線が できる"""
    H, W = len(p), len(p[0])
    for y in range(H):
        for x in range(W):
            if p[y][x] != '.': continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and p[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): g[y][x] = 'k'
    for y in range(H):
        for x in range(W):
            if p[y][x] != '.': g[y][x] = p[y][x]
def shade(g, ramps=RAMP, dk=1.0):
    """光は 左上：上と 左の ふちに 三日月の 明、右下に 影（ふち＝空白か 黒線）"""
    H, W = len(g), len(g[0])
    def e(y, x): return not (0 <= y < H and 0 <= x < W) or g[y][x] in '.k'
    def run(y, x, dy, dx, lim):
        n = 1
        while n <= lim and not e(y + dy * n, x + dx * n): n += 1
        return n
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c not in ramps: continue
            hi, md, lo = ramps[c]
            up, lf, ul = run(y, x, -1, 0, 3), run(y, x, 0, -1, 3), run(y, x, -1, -1, 3)
            dn, rt, dr = run(y, x, 1, 0, 4), run(y, x, 0, 1, 4), run(y, x, 1, 1, 4)
            L = 3 * (up == 1) + 2 * (lf == 1) + (ul == 1) + 1.5 * (up == 2) + .8 * (ul == 2)
            D = 3 * (dn == 1) + 2.5 * (rt == 1) + (dr == 1) + 1.5 * (dn == 2) + 1.2 * (rt == 2) + .8 * (dr == 2) + .5 * (dn == 3)
            D *= dk
            out[y][x] = md if L == D else hi if L > D else lo
    return out
def recolor(g, m): return [[m.get(c, c) for c in r] for r in g]
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'v': 'm', 'm': 'l', 'S': 'T', 'T': 'U'}
def rell(g, cx, cy, a, b, ang, ch):
    ca, sa = math.cos(ang), math.sin(ang)
    for y in range(64):
        for x in range(64):
            dx, dy = x - cx, y - cy; u = dx * ca + dy * sa; v = -dx * sa + dy * ca
            if (u / a) ** 2 + (v / b) ** 2 <= 1: g[y][x] = ch

# ---------- 翼（指の ように 分かれた 風切り、先は 影の もやに とける）----------
WP = {
    'up':   dict(w=(29, 7),  prim=[(30, 0), (25, 0), (20, 1), (15, 3), (12, 7)], sec=[(13, 12), (17, 17), (23, 21), (29, 25)]),
    'hi':   dict(w=(25, 13), prim=[(19, 3), (13, 4), (8, 7), (5, 11), (4, 16)], sec=[(7, 20), (13, 24), (20, 27), (27, 29)]),
    'mid':  dict(w=(24, 19), prim=[(10, 10), (5, 13), (2, 18), (2, 23), (4, 27)], sec=[(8, 30), (14, 33), (21, 34), (28, 33)]),
    'down': dict(w=(27, 32), prim=[(10, 37), (9, 42), (11, 47), (15, 51), (20, 53)], sec=[(23, 50), (27, 47), (31, 43), (35, 38)]),
}
def wing(pose, far=False):
    g = G(); sx, sy = 39, 27
    S_ = .81
    sc = lambda q: (round(sx + (q[0] - sx) * S_), round(sy + (q[1] - sy) * S_))
    P = {k: (sc(v) if k == 'w' else [sc(q) for q in v]) for k, v in WP[pose].items()}; wx, wy = P['w']
    bases = [(round(sx + (wx - sx) * t), round(sy + (wy - sy) * t)) for t in (.85, .65, .45, .25)]
    for (bx, by), (tx, ty) in reversed(list(zip(bases, P['sec']))):
        p = G(); stroke(p, bx, by, tx, ty, 2.4, 1.3, '1', '5', .88); ink(g, p)
    # 初列風切り：細く 分かれた 指（先が もや）
    for (tx, ty) in reversed(P['prim']):
        p = G(); stroke(p, wx, wy, tx, ty, 1.7, .6, '1', '5', .8); ink(g, p)
    cov = [(sx + 3, sy - 1), (sx - 1, sy - 4), (wx, wy)] + [(round(bx + (tx - bx) * .4), round(by + (ty - by) * .4)) for (bx, by), (tx, ty) in zip(bases, P['sec'])] + [(sx + 2, sy + 4)]
    p = G(); poly(p, cov, '1'); ink(g, p)
    g = shade(g, dk=.7)
    # 羽の つや（青むらさきの 光を 手で 点々と）
    for y in range(1, 63):
        for x in range(1, 63):
            if g[y][x] == 'Q' and g[y - 1][x] == 'R' and (x + y) % 3 == 0: g[y][x] = 'R'
    if far: g = recolor(g, DARK)
    return rows_of(g)

# ---------- 胴（ぼさぼさの 首の 羽、くさび形の 尾）----------
def body():
    g = G()
    p = G(); rell(p, 35, 33, 12, 7.5, -.3, '1')
    # 首の ぼさぼさ（とがった 羽を 後ろ下へ）
    for (bx, by, tx, ty) in [(47, 22, 41, 31), (46, 25, 39, 33), (48, 28, 43, 36), (45, 20, 38, 27)]:
        stroke(p, bx, by, tx, ty, 2.2, .6, '1')
    ink(g, p)
    # 首の 羽の すじ（とがった 先を 黒線で 分ける）
    g = shade(g)
    for (x, y) in [(42, 30), (41, 31), (40, 32), (44, 33), (43, 34), (40, 27), (39, 28)]:
        if g[y][x] != '.': g[y][x] = 'k'
    dots(g, 'R', [(43, 29), (45, 32), (41, 26), (30, 29), (31, 29), (34, 28), (26, 31)])
    # 胸の うろこ羽
    for (x, y) in [(36, 36), (40, 37), (32, 38), (44, 36)]:
        if g[y][x] in 'QP': g[y][x] = 'P'; g[y - 1][x - 1] = 'Q' if g[y - 1][x - 1] == 'P' else g[y - 1][x - 1]
    return rows_of(g)

def tail():
    g = G()
    for (tx, ty) in [(12, 42), (13, 46), (16, 49), (20, 50)]:
        p = G(); stroke(p, 27, 37, tx, ty, 2.6, 1.6, '1', '5', .8); ink(g, p)
    g = shade(g, dk=.8)
    return rows_of(g)

# ---------- 頭（太い 鉄の くちばし、赤く 光る 目、ぼさぼさの 冠）----------
def head():
    g = G()
    for (bx, by, tx, ty) in [(46, 18, 39, 14), (48, 17, 43, 10), (45, 21, 37, 19)]:
        p = G(); stroke(p, bx, by, tx, ty, 1.8, .6, '1'); ink(g, p)
    p = G(); rell(p, 50, 22, 6.5, 5.8, 0, '1'); rell(p, 45, 19, 3, 2.2, -.4, '1'); ink(g, p)
    g = shade(g)
    put(g, 54, 17, [   # 太く 重い 鉄の くちばし（先が かぎ）
        '.kkkk.....',
        'kSSSSkk...',
        'kSSSSSSkk.',
        'kTSSSSSSTk',
        'kkkkkkkTTk',
        'kTTTTTkkk.',
        '.kUUUk....',
        '..kkk.....',
    ])
    return rows_of(g)

EYE = ['kkkkk..', '.kkkkkk', 'rkrrrYk', '.rkrrk.', '...kk..']      # ひくい まゆの 下で 赤く 光る 目（光が 後ろへ 尾を 引く）
EYE_ALT = {
    'blink': ['kkkkk..', '.kkkkkk', '..kkkkk', '.......', '.......'],
    'atk0|atk1|atk2': ['kkkkk..', '.kkkkkk', 'rkYYYYk', 'r.krrk.', '...kk..'],
    'hit': ['.......', '.kk..kk', '...kk..', '.kk..kk', '.......'],
    'ko': ['.......', '..k.k..', '...k...', '..k.k..', '.......'],
}
LEG = outline([   # 鉄の すねと 白い かぎ爪（ふちは 自動）
    'TU....',
    'TU....',
    '.TU...',
    '.TU...',
    '.TU...',
    'TTTUU.',
    'STSTSU',
    'S.S..S',
])
LEG_ATK = outline([   # 攻撃：前へ のばして つかみかかる
    'TU.......',
    '.TU......',
    '..TTU....',
    '...TTUU..',
    '....TTTUU',
    '....STSTS',
    '....S..SS',
])
def far(rows): return [''.join({'T': 'U', 'U': 'P', 'S': 'T'}.get(c, c) for c in r) for r in rows]

# ---------- 影の 羽の 矢（攻撃）と もや ----------
DART = ['mvv.....', '.mmPPQRk', 'mvv.....']
DART = ['vv.....kk..', '.mmQQRRSSk.', 'vv.....kk..']
SMOKE_A = ['.v..', 'vm.m', '..m.']
SMOKE_B = ['..v.', '.m.v', 'm...']
GUST = ['c..cc....cc', '.cc..c..c..', '......cc...']

def OL(rows): return outline(rows)
def layers():
    W = {p: wing(p) for p in WP}; WF = {p: wing(p, True) for p in WP}
    return [
        dict(n='wingB', g='wingB', x=3, y=-3, rows=WF['hi'], alt={'idle1|idle3|walk1|walk3|atk2': WF['mid'], 'walk0|atk0|hit': WF['up'], 'walk2|atk1': WF['down']}),
        dict(n='tail', g='tail', x=0, y=0, rows=tail()),
        dict(n='smoke', g='tail', x=8, y=47, rows=OL(SMOKE_A), alt={'idle1|idle3|walk1|walk3': OL(SMOKE_B)}, not_='ko'),
        dict(n='leg3', g='legs', x=27, y=40, rows=far(LEG), alt={'atk1|atk2': far(LEG_ATK)}),
        dict(n='leg1', g='legs', x=39, y=39, rows=far(LEG), alt={'atk1|atk2': far(LEG_ATK)}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='leg2', g='legB', x=33, y=42, rows=LEG, alt={'atk1|atk2': LEG_ATK}),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='eye', g='head', x=46, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['mid'], alt={'idle1|idle3': W['hi'], 'walk0|atk0|hit': W['up'], 'walk2|atk1': W['down'], 'walk1|walk3|atk2': W['mid']}),
        dict(n='gust', g='root', x=14, y=56, rows=OL(GUST), only='walk2'),
        dict(n='dart1', g='root', x=52, y=29, rows=OL(DART), only='atk1'),
        dict(n='dart2', g='root', x=48, y=36, rows=OL(DART), only='atk1'),
        dict(n='dart3', g='root', x=55, y=43, rows=OL(DART), only='atk1'),
        dict(n='dart4', g='root', x=58, y=31, rows=OL(DART), only='atk2'),
        dict(n='dart5', g='root', x=56, y=40, rows=OL(DART), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'legs': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1), 'legs': (-1, 0), 'legB': (1, 0)},
    'walk1': {},
    'walk2': {'body': (0, -2), 'legs': (1, -1), 'legB': (-1, 0)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-4, -2), 'head': (-1, 1), 'legs': (-1, -1)},
    'atk1': {'root': (2, 1), 'head': (1, 1)},
    'atk2': {'root': (3, 1), 'head': (1, 1)},
    'hit': {'root': (-4, -1), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'tail': 'body', 'legs': 'body', 'legB': 'body', 'body': 'root'}
