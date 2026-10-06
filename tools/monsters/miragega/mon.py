# ミラージュガ（エスパー・むし × ガ）手打ち GBA風
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

META = dict(id='miragega', name='ミラージュガ', types=['psychic', 'bug'], base='ガ', size='M')
PAL = {
    'k': '#101018', 'l': '#2e1a40',
    'R': '#d8bcf2', 'Q': '#9a6ccc', 'P': '#58328a',      # 翅（すみれ色）
    'F': '#fff2d2', 'G': '#d2b08a', 'H': '#8a6452',      # 毛と 触角
    'Y': '#ffd850', 'O': '#e07a30',                      # 目玉もようの 金
    'm': '#ff52b8', 'n': '#a01c78',                      # 念力の 光
    'w': '#ffffff', 'c': '#a8f0ff',                      # 鱗粉
}
LIGHT = set('RFYmwc')
RAMP = {'1': 'RQP', '2': 'FGH', '3': 'QPP', '4': 'mmn', '5': 'GHH'}

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
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'F': 'G', 'G': 'H', 'Y': 'O', 'O': 'n', 'm': 'n', 'w': 'R', 'c': 'Q'}

# ---------- 翅（前翅に 大きな 目玉もよう、外の ふちは 鱗粉の 帯）----------
import math
# 前翅の りんかく（手で 打った 点）：前の ふちは 弧、先は かぎ形、外の ふちは 波（スカラップ）、後ろの ふちは ゆるい 弧
FW_BASE = (41, 25)
FW_PTS = [(41, 24), (36, 17), (29, 11), (21, 7), (13, 4), (7, 2), (2, 1),    # 前の ふち → 先
          (4, 4), (6, 6),                                                     # かぎの 内がわ
          (4, 9), (3, 12), (6, 13), (4, 16), (7, 17), (6, 20), (9, 21), (9, 24), (12, 24),   # 波の ふち
          (15, 27), (21, 30), (28, 32), (34, 32), (39, 29)]                    # 後ろの ふち
FW_VEIN = [5, 12, 16, 20]          # 翅脈を のばす 先（点の 番号）
HW_BASE = (38, 31)
HW_PTS = [(38, 30), (31, 31), (23, 34), (17, 38), (14, 43), (16, 45), (15, 48), (19, 48), (20, 51), (24, 50),
          (27, 52), (29, 48), (33, 47), (36, 42), (39, 36)]
HW_VEIN = [4, 8, 11]
def turn(pts, base, deg):
    """あたりの 点を つけねで まわす（下書き用。ぬりは あとで）"""
    a = math.radians(deg); bx, by = base
    return [(round(bx + (x - bx) * math.cos(a) - (y - by) * math.sin(a)), round(by + (x - bx) * math.sin(a) + (y - by) * math.cos(a))) for x, y in pts]
FW = {'mid': FW_PTS, 'hi': turn(FW_PTS, FW_BASE, 14), 'up': turn(FW_PTS, FW_BASE, 34), 'down': turn(FW_PTS, FW_BASE, -112)}
HW = {'rest': HW_PTS, 'down': turn(HW_PTS, HW_BASE, -30)}
SPOT = [   # 翅の 目玉：アーモンド形に たての ひとみ（にらむ 目）
    '....kkkkk....',
    '..kkYYYYYkk..',
    '.kYYOOkOOYYk.',
    'kYOOmmkmwOOYk',
    '.kYYOOkOOYYk.',
    '..kkYYYYYkk..',
    '....kkkkk....',
]
SPOT_GLOW = [
    '....kkkkk....',
    '..kkwwwwwkk..',
    '.kwwmmkmmwwk.',
    'kwmmwwkwwmmwk',
    '.kwwmmkmmwwk.',
    '..kkwwwwwkk..',
    '....kkkkk....',
]
SPOT_S = ['.kkkk.', 'kYOkYk', '.kkkk.']
def wingpart(pts, spot, glow=False, small=False, base=None, veins=()):
    g = G(); p = G(); poly(p, pts, '1'); ink(g, p)
    g = shade(g, dk=.8)
    bx, by = base or pts[0]
    cells = [(x, y) for y in range(64) for x in range(64) if g[y][x] in 'RQP']
    far = max(((x - bx) ** 2 + (y - by) ** 2) ** .5 for x, y in cells)
    for x, y in cells:
        d = ((x - bx) ** 2 + (y - by) ** 2) ** .5 / far
        z = .035 * ((x // 2 + y // 2) % 2)
        # 中ほどに 暗い 波形の 帯、外の ふちは 明るい 鱗粉の 帯（境に 細い 線）
        if .40 + z < d < .52 + z: g[y][x] = 'n' if .43 + z < d < .49 + z else 'P'
        elif .82 + z < d < .87 + z: g[y][x] = 'P'
        elif d >= .87 + z: g[y][x] = 'R' if g[y][x] != 'P' else 'Q'
    # 翅脈（つけねから 外へ、手で 打つ 線）
    for (ex, ey) in [pts[v] for v in veins]:
        n = max(abs(ex - bx), abs(ey - by))
        for i in range(3, n - 2):
            x, y = round(bx + (ex - bx) * i / n), round(by + (ey - by) * i / n)
            if g[y][x] in 'RQ': g[y][x] = 'P'
    for x, y in cells:
        if g[y][x] == 'R' and (x * 3 + y * 2) % 7 == 0 and ((x - bx) ** 2 + (y - by) ** 2) ** .5 / far > .88: g[y][x] = 'w'
    cx = sum(x for x, y in cells) / len(cells); cy = sum(y for x, y in cells) / len(cells)
    cx, cy = cx + (cx - bx) * spot, cy + (cy - by) * spot
    S = SPOT_S if small else SPOT_GLOW if glow else SPOT
    put(g, round(cx) - len(S[0]) // 2, round(cy) - len(S) // 2, S)
    return g
def wing(pose, far=False, glow=False):
    g = wingpart(FW[pose], .35, glow, base=FW_BASE, veins=FW_VEIN)
    if far: g = recolor(g, DARK)
    return rows_of(g)
def hindwing(pose, far=False):
    g = wingpart(HW[pose], .2, small=True, base=HW_BASE, veins=HW_VEIN)
    if far: g = recolor(g, DARK)
    return rows_of(g)

# ---------- 胴（ふさふさの 胸、しま模様の 腹）----------
def body():
    g = G()
    # 腹（後ろ下へ のびる、節の しま）
    p = G(); ellipse(p, 31, 38, 9, 5, '2'); poly(p, [(24, 36), (18, 42), (23, 41)], '2'); ink(g, p)
    g = shade(g)
    for x in (26, 30, 34):
        for y in range(30, 46):
            if g[y][x] in 'FGH' and g[y][x - 1] != 'k': g[y][x] = 'P' if g[y - 1][x] != 'k' else 'k'
    for x in (25, 29, 33):
        for y in range(30, 46):
            if g[y][x] in 'FGH' and g[y][x + 1] == 'P': g[y][x] = 'H'
    # 胸の 毛（もこもこの ふち）
    p = G(); ellipse(p, 40, 31, 6.5, 6.5, '2')
    for (x, y) in ((34, 27), (35, 35), (39, 38), (43, 37), (45, 33), (33, 31)): ellipse(p, x, y, 2, 2, '2')
    ink(g, p)
    g = shade(g)
    dots(g, 'H', [(38, 33), (41, 35), (37, 30), (42, 30)])
    dots(g, 'w', [(37, 27), (36, 28)])
    return rows_of(g)

# ---------- 頭（大きな 複眼、羽毛の 触角、うず巻きの 針の 口）----------
def head():
    g = G()
    for i, (bx, by, tx, ty) in enumerate([(49, 21, 40, 8), (46, 22, 32, 14)]):
        p = G(); stroke(p, bx, by, tx, ty, 1.8, .7, '5')
        n = max(abs(tx - bx), abs(ty - by))
        for j in range(2, n, 2):   # くしの 歯（下がわに 切れこみ）
            x, y = round(bx + (tx - bx) * j / n), round(by + (ty - by) * j / n)
            if p[y + 1][x] == '5': p[y + 1][x] = '.'
            p[y + 2][x] = '.'
        ink(g, p)
    g = shade(g, {'5': 'GHH'})
    if True:
        pass
    p = G(); ellipse(p, 49, 26, 6, 5.5, '2')
    for (x, y) in ((44, 23), (44, 29), (47, 31)): ellipse(p, x, y, 1.8, 1.8, '2')
    ink(g, p)
    g = shade(g, {'2': 'FGH'})
    dots(g, 'H', [(45, 26), (46, 29), (44, 24)])
    put(g, 50, 30, ['.kkk..', 'kYOOk.', 'kOkYOk', '.kkYOk', '...kk.'])
    return rows_of(g)

EYE = ['kkkkkk..', '.kkkkkkk', '.knnmmwk', '.knmmmmk', '..knnnk.', '...kkk..']       # まゆの 板で つり上がった 複眼
EYE_ALT = {
    'blink': ['kkkkkk..', '.kkkkkkk', '.kkkkkkk', '.kGGGGk.', '..kkkk..'],
    'atk0|atk1|atk2': ['kkkkkk..', '.kkkkkkk', '.kmwwwwk', '.kmwwwmk', '..kmmmk.', '...kkk..'],
    'hit': ['.......', '.kk.kk.', '..kkk..', '.kk.kk.', '.......'],
    'ko': ['.......', '.k...k.', '..k.k..', '...k...', '..k.k..'],
}
PROBO = ['kkkkkkkk..', 'kYYYYOOOkk', '.kkkkkkkOk', '........kk']   # 攻撃：針を のばす

# 前足：かぎ爪の ついた とげの 足（前へ かまえる）
LEGS = [
    '.......kk.',
    '......kQPk',
    '.kk..kQPk.',
    'kQPkkQPk..',
    'kPPPPPk...',
    '.kkPPk....',
    '...kwk....',
    '...kwk....',
    '....k.....',
]
LEGS_BACK = [
    'kk...kk.',
    'kPk.kPk.',
    '.kPkkPk.',
    '..kPPk..',
    '..kPk...',
    '.kwk....',
    '.kk.....',
]

# ---------- 念力の 輪と 鱗粉 ----------
RING1 = [
    '..mm.....',
    '....mm...',
    '......m..',
    '......mn.',
    '.......mn',
    '.......mn',
    '.......mn',
    '......mn.',
    '......m..',
    '....mm...',
    '..mm.....',
]
RING2 = [
    '..mmm......',
    '.....mm....',
    '.......mm..',
    '........mn.',
    '.........mn',
    '.........mn',
    '.........mn',
    '.........mn',
    '.........mn',
    '........mn.',
    '.......mm..',
    '.....mm....',
    '..mmm......',
]
DUST_A = ['.w.......', 'wcw......', '.w....c..', '.........', '...c.....']
DUST_B = ['....c....', '.........', 'c....w...', '....wcw..', '.....w...']

def layers():
    W = {p: wing(p) for p in FW}; WF = {p: wing(p, True) for p in FW}; WG = wing('mid', glow=True)
    H = {p: hindwing(p) for p in HW}; HF = {p: hindwing(p, True) for p in HW}
    return [
        dict(n='hindB', g='wingB', x=3, y=-3, rows=HF['rest'], alt={'walk2': HF['down']}),
        dict(n='wingB', g='wingB', x=3, y=-3, rows=WF['hi'], alt={'idle1|idle3|walk1|walk3|atk1|atk2': WF['mid'], 'walk0|atk0|hit': WF['up'], 'walk2': WF['down']}),
        dict(n='legB', g='legs', x=33, y=40, rows=OL(LEGS_BACK) if False else LEGS_BACK),
        dict(n='hindF', g='wingF', x=0, y=0, rows=H['rest'], alt={'walk2': H['down']}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='legs', g='legs', x=39, y=34, rows=LEGS),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='probo', g='head', x=51, y=29, rows=PROBO, only='atk1|atk2'),
        dict(n='eye', g='head', x=46, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['mid'], alt={'idle1|idle3': W['hi'], 'walk0|atk0|hit': W['up'], 'walk2': W['down'], 'walk1|walk3|atk2': W['mid'], 'atk1': WG}),
        dict(n='dust', g='root', x=8, y=46, rows=OL(DUST_A), alt={'idle1|idle3|walk1|walk3': OL(DUST_B)}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='ring1', g='root', x=55, y=20, rows=OL(RING1), only='atk1'),
        dict(n='ring2', g='root', x=58, y=17, rows=OL(RING2), only='atk2'),
        dict(n='ring1b', g='root', x=53, y=20, rows=OL(RING1), only='atk2'),
    ]
def OL(rows): return outline(rows)

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'legs': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-3, 0), 'head': (-1, 1), 'legs': (-1, -1)},
    'atk1': {'root': (2, -1)},
    'atk2': {'root': (3, -1)},
    'hit': {'root': (-4, 1), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'legs': 'body', 'body': 'root'}
