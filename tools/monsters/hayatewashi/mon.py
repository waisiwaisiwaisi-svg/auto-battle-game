# ハヤテワシ（かぜ・かくとう × ワシ）手打ち GBA風
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp

META = dict(id='hayatewashi', name='ハヤテワシ', types=['wind', 'fighting'], base='ワシ', size='M')
PAL = {
    'k': '#101018', 'l': '#2c2a48',
    'R': '#a8bcd8', 'Q': '#5f7298', 'P': '#36405e',      # はね（はがね色の 青）
    'F': '#f4ead0', 'G': '#c8ac84', 'H': '#86684c',      # 頭の 羽と テーピング
    'Y': '#ffd23c', 'O': '#c87a18',                      # くちばし・足
    'r': '#ee3a3a', 'd': '#8c1c2c',                      # 闘志の とさか・くまどり
    'c': '#e4fbff', 'b': '#64c4e8',                      # 風
    'w': '#ffffff',
}
LIGHT = set('RFYcw')
RAMP = {'1': 'RQP', '2': 'FGH', '3': 'rrd', '4': 'YYO', '5': 'cbb', '6': 'QPP'}

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
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'c': 'b', 'b': 'Q', 'F': 'G', 'G': 'H', 'Y': 'O', 'w': 'G'}

# ---------- 翼（ワシの 翼：おおい羽＋風切り羽。風切りの 先は 刃の ように 白く 光る）----------
WP = {
    'up':   dict(w=(27, 5),  prim=[(25, 0), (20, 0), (15, 1), (11, 4)], sec=[(13, 9), (16, 14), (21, 18), (27, 22)]),
    'hi':   dict(w=(24, 10), prim=[(17, 2), (12, 4), (8, 8), (5, 12)], sec=[(7, 17), (12, 21), (18, 24), (25, 27)]),
    'mid':  dict(w=(22, 16), prim=[(9, 9), (5, 13), (3, 18), (3, 23)], sec=[(6, 27), (12, 30), (19, 32), (27, 32)]),
    'down': dict(w=(24, 30), prim=[(9, 34), (9, 40), (12, 45), (16, 49)], sec=[(20, 47), (25, 44), (29, 41), (33, 36)]),
}
def wing(pose, far=False):
    g = G()
    sx, sy = 38, 25
    S = .84   # 翼の 大きさ（肩からの 長さを ちぢめる）
    sc = lambda q: (round(sx + (q[0] - sx) * S), round(sy + (q[1] - sy) * S))
    P = {k: (sc(v) if k == 'w' else [sc(q) for q in v]) for k, v in WP[pose].items()}; wx, wy = P['w']
    bases = []
    for k, (tx, ty) in enumerate(P['sec']):
        t = .2 + .22 * (3 - k)
        bases.append((round(sx + (wx - sx) * t), round(sy + (wy - sy) * t)))
    # 次列風切り（うしろ）→ 初列風切り → おおい羽 の 順に 重ねる
    for (bx, by), (tx, ty) in reversed(list(zip(bases, P['sec']))):
        p = G(); stroke(p, bx, by, tx, ty, 2.4, 1.1, '1', '5', .84); ink(g, p)
    for (tx, ty) in reversed(P['prim']):
        p = G(); stroke(p, wx, wy, tx, ty, 2.0, .8, '1', '5', .8); ink(g, p)
    # おおい羽：肩〜手首〜風切りの ねもとを むすぶ 面
    cov = [(sx + 3, sy - 1), (sx - 1, sy - 4), (wx, wy)] + [(round(bx + (tx - bx) * .38), round(by + (ty - by) * .38)) for (bx, by), (tx, ty) in zip(bases, P['sec'])] + [(sx + 2, sy + 4)]
    p = G(); poly(p, cov, '1'); ink(g, p)
    # 中雨覆の うろこ列（小さな 羽を 手首側から 重ねる）
    for (bx, by), (tx, ty) in zip(bases, P['sec']):
        p = G(); stroke(p, round(bx + (sx - bx) * .15), round(by + (sy - by) * .15), round(bx + (tx - bx) * .3), round(by + (ty - by) * .3), 2.0, 1.2, '1'); ink(g, p)
    g = shade(g, dk=.6)
    # 肩の つけね（体との 境を 消す）と 刃の ような 白い ふち
    for y in range(64):
        for x in range(64):
            if g[y][x] == 'b' and y > 0 and g[y - 1][x] == 'k': g[y][x] = 'c'
    if far: g = recolor(g, DARK)
    return rows_of(g)

# ---------- 胴 ----------
def body():
    g = G()
    p = G(); poly(p, [(40, 20), (49, 19), (54, 25), (55, 32), (52, 39), (45, 44), (36, 47), (31, 45), (31, 36), (35, 27)], '1')
    # 胸の 羽毛（クリーム色の よだれかけ）
    poly(p, [(45, 19), (52, 21), (55, 29), (53, 32), (48, 28), (44, 22)], '2')
    ink(g, p)
    # ももの はね（ぎざぎざの ズボン）
    for (bx, by, tx, ty) in [(41, 38, 39, 47), (44, 38, 43, 48), (47, 37, 47, 47), (49, 36, 50, 45)]:
        p = G(); stroke(p, bx, by, tx, ty, 2.6, 1.0, '1'); ink(g, p)
    g = shade(g)
    # 胸の うろこ模様（手打ち）
    for (x, y) in [(41, 29), (45, 32), (38, 33), (48, 35), (42, 36), (36, 39), (39, 42)]:
        g[y][x] = 'P'; g[y][x - 1] = 'R' if g[y][x - 1] == 'Q' else g[y][x - 1]
    dots(g, 'H', [(50, 25), (52, 28), (49, 28), (51, 31)])
    return rows_of(g)

def tail():
    g = G()
    for (tx, ty) in [(23, 52), (26, 54), (30, 55)]:
        p = G(); stroke(p, 34, 44, tx, ty, 2.4, 1.3, '1', '2', .78); ink(g, p)
    g = shade(g)
    return rows_of(g)

# ---------- 頭（とさかは 闘志の 赤、目の 下に 黒い すじ）----------
def head():
    g = G()
    for (bx, by, tx, ty) in [(45, 12, 35, 7), (44, 14, 37, 13), (46, 10, 40, 3)]:
        p = G(); stroke(p, bx, by, tx, ty, 2.0, .8, '3'); ink(g, p)
    p = G(); ellipse(p, 49, 14, 7.2, 6.2, '2'); poly(p, [(42, 15), (50, 16), (53, 23), (44, 23)], '2'); ink(g, p)
    g = shade(g, dk=.75)
    put(g, 54, 9, [
        '.kkk....',
        'kYYYkk..',
        'YYYYYYk.',
        'YYYYYYYk',
        'kkkkkOYk',
        'OOOOkkOk',
        'kkkk..kk',
    ])
    # 目の 下から 後ろへ のびる 黒い すじ（ハヤブサの ような 隈）
    dots(g, 'P', [(47, 15), (46, 16), (47, 16), (46, 17), (45, 17), (45, 18), (44, 18), (44, 19)])
    dots(g, 'H', [(48, 16), (46, 18), (42, 14), (45, 19)])
    return rows_of(g)

EYE = ['kkkk.....', '.kkkkkkk.', '..kYYOk..', '...kkk...']   # 太い まゆの ひさし＋つり目
EYE_ALT = {
    'blink': ['kkkk.....', '.kkkkkkk.', '..kkkkk..', '.........'],
    'atk0|atk1|atk2': ['kkkk.....', '.kkkkkkk.', '..kccYk..', '...kkk...'],
    'hit': ['.........', '.kk..kk..', '...kk....', '.kk..kk..'],
    'ko': ['.........', '..k.k....', '...k.....', '..k.k....'],
}

# ---------- 足（テーピングを 巻いた 拳闘の 足、白い かぎ爪）----------
LEGS = [
    '..wGww......',
    '..Gwwk......',
    '..wGwk......',
    '..GwHk......',
    '.kOYYYk.....',
    'kYYOYYYYk...',
    'kYOkYOkYYk..',
    'wkk.wk.kwk..',
    'w...w...w...',
]
LEGS_ATK = [   # 前へ つき出す けり
    '..wGwGw.......',
    '...GwwGwwk....',
    '.....kkYYYk...',
    '....kYYOYYYYk.',
    '....kYOkYOkYYk',
    '.....wkk.wk.wk',
    '.....w...w...w',
]
LEGS_FAR = [
    'HGH...',
    'GHH...',
    'HGH...',
    'kOOk..',
    'kOOOOk',
    'Gk.Gk.',
]
def legs(rows):
    from pix import outline
    return outline(rows)

# ---------- 風の 刃（攻撃）と 羽ばたきの 風 ----------
SLASH = [   # 風の 刃：かぎ爪の 前に 走る 三日月
    '.....c........',
    '......cc......',
    '.......ccb....',
    '........ccb...',
    '.........ccb..',
    '.........cccb.',
    '..........ccb.',
    '..........ccbb',
    '..........ccbb',
    '..........ccb.',
    '.........cccb.',
    '.........ccb..',
    '........ccb...',
    '.......ccb....',
    '......cc......',
    '.....c........',
]
SLASH2 = [
    '..c.....',
    '...cb...',
    '....cb..',
    '....cb..',
    '....cb..',
    '...cb...',
    '..c.....',
]
GUST = ['.cc.....cc', 'c..c..cc..', '....cc....']

def OL(rows):
    from pix import outline
    return outline(rows)
def layers():
    W = {p: wing(p) for p in ('up', 'hi', 'mid', 'down')}
    WF = {p: wing(p, True) for p in ('up', 'hi', 'mid', 'down')}
    return [
        dict(n='wingB', g='wingB', x=1, y=-2, rows=WF['hi'], alt={'idle1|idle3|walk1|walk3|atk2': WF['mid'], 'walk0|atk0|hit': WF['up'], 'walk2|atk1': WF['down']}),
        dict(n='legFar', g='legs', x=39, y=46, rows=LEGS_FAR, not_='atk1|atk2'),
        dict(n='tail', g='tail', x=0, y=0, rows=tail()),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legs', g='legs', x=42, y=45, rows=legs(LEGS), alt={'atk1|atk2': legs(LEGS_ATK)}),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='eye', g='head', x=46, y=10, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['mid'], alt={'idle1|idle3': W['hi'], 'walk0|atk0|hit': W['up'], 'walk2|atk1': W['down'], 'walk1|walk3|atk2': W['mid']}),
        dict(n='gust', g='root', x=25, y=55, rows=OL(GUST), only='walk2'),
        dict(n='slash', g='root', x=51, y=33, rows=OL(SLASH), only='atk1'),
        dict(n='slash2', g='root', x=56, y=40, rows=OL(SLASH2), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {},
    'idle3': {'body': (0, 1), 'head': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-3, -3), 'head': (-1, 1), 'legs': (-1, -2)},
    'atk1': {'root': (5, 3), 'head': (1, 1)},
    'atk2': {'root': (8, 4), 'head': (1, 1)},
    'hit': {'root': (-4, -1), 'head': (-2, 1), 'legs': (-1, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'tail': 'body', 'legs': 'body', 'body': 'root'}
