# チョウリュウ（フェアリー・ドラゴン × 蝶の 竜）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

META = dict(id='choryu', name='チョウリュウ', types=['fairy', 'dragon'], base='蝶の 竜', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1a3c',
    'R': '#ffe2ee', 'Q': '#f08ab4', 'P': '#a8467c',      # うろこ（さくら色）
    'A': '#b4eeff', 'B': '#50a6ea', 'C': '#2a56a6',      # 蝶の 翅（ステンドグラスの 青）
    'Y': '#ffe27a', 'O': '#d08e2c',                      # 金（翅脈・腹の 板・目）
    'w': '#ffffff', 'v': '#e8b2ff',                      # つの・牙・鱗粉
}
LIGHT = set('RAYwv')
RAMP = {'1': 'RQP', '2': 'ABC', '3': 'YOO', '6': 'QPP'}

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
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'A': 'B', 'B': 'C', 'C': 'l', 'Y': 'O', 'O': 'P', 'w': 'v'}

# ---------- 蝶の 翅（金の 翅脈で 区切られた ステンドグラス、外の ふちは 紺に 白い 点）----------
FW = {
    'up':   [(37, 28), (36, 14), (31, 3), (24, 0), (19, 5), (22, 18), (31, 30)],
    'mid':  [(37, 28), (29, 14), (19, 6), (11, 7), (8, 15), (13, 25), (29, 32)],
    'down': [(37, 30), (28, 37), (19, 45), (14, 53), (22, 55), (31, 48), (36, 38)],
}
HW = {   # 後翅：長い 燕尾の 先
    'up':   [(35, 31), (25, 26), (16, 26), (12, 31), (14, 37), (9, 44), (19, 40), (31, 36)],
    'mid':  [(35, 31), (24, 31), (15, 34), (12, 40), (15, 44), (11, 51), (21, 46), (31, 38)],
    'down': [(35, 33), (27, 39), (18, 43), (13, 48), (9, 54), (19, 51), (30, 45)],
}
def wingpart(pts, nv):
    g = G(); p = G(); poly(p, pts, '2'); ink(g, p)
    bx, by = pts[0]
    cells = [(x, y) for y in range(64) for x in range(64) if g[y][x] == '2']
    far = max(((x - bx) ** 2 + (y - by) ** 2) ** .5 for x, y in cells)
    for x, y in cells:
        d = ((x - bx) ** 2 + (y - by) ** 2) ** .5 / far
        ck = (x + y) % 2 == 0
        g[y][x] = 'C' if d < .3 or (d < .38 and ck) else 'B' if d < .62 or (d < .7 and ck) else 'A'
    # 外の ふち：紺の 帯に 白い 点
    for x, y in cells:
        if any(g[y + dy][x + dx] == 'k' and (g[y + 2 * dy][x + 2 * dx] == '.' if 0 <= y + 2 * dy < 64 and 0 <= x + 2 * dx < 64 else True) for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            g[y][x] = 'w' if (x * 2 + y) % 5 == 0 else 'C'
    # 金の 翅脈（つけねから 放射、手で 打つ 線）＋ ひとつの 弧
    for (ex, ey) in pts[2:2 + nv]:
        n = max(abs(ex - bx), abs(ey - by))
        for i in range(2, n - 1):
            x, y = round(bx + (ex - bx) * i / n), round(by + (ey - by) * i / n)
            if g[y][x] in 'ABCw': g[y][x] = 'Y' if i < n * .5 else 'O'
    for x, y in cells:
        d = ((x - bx) ** 2 + (y - by) ** 2) ** .5 / far
        if .54 < d < .6 and g[y][x] in 'ABC': g[y][x] = 'O'
    return g
def wing(pose, far=False):
    g = wingpart(HW[pose], 3); f = wingpart(FW[pose], 3)
    for y in range(64):
        for x in range(64):
            if f[y][x] != '.': g[y][x] = f[y][x]
    if far: g = recolor(g, DARK)
    return rows_of(g)

# ---------- 体（S字の ヘビの ような 竜。腹は 金の 板）----------
PATH = [(47, 21), (45, 28), (41, 34), (34, 38), (27, 40), (21, 40), (17, 37), (14, 33)]
R_ = [3.6, 4.2, 4.8, 4.6, 4.0, 3.2, 2.3, 1.4]
def body():
    g = G(); p = G()
    for i in range(len(PATH) - 1):
        (x0, y0), (x1, y1) = PATH[i], PATH[i + 1]
        stroke(p, x0, y0, x1, y1, R_[i], R_[i + 1], '1')
    # 腹の 板（体の 内がわ＝下がわに そって）
    for i in range(len(PATH) - 1):
        (x0, y0), (x1, y1) = PATH[i], PATH[i + 1]
        stroke(p, x0 + 1, y0 + round(R_[i] * .75), x1 + 1, y1 + round(R_[i + 1] * .75), R_[i] * .3, R_[i + 1] * .3, '3')
    ink(g, p)
    g = shade(g)
    # 腹の 板の 区切り（手で）
    for (x, y) in [(46, 28), (43, 33), (39, 38), (34, 41), (29, 43), (24, 43), (19, 43)]:
        for dy in range(-2, 3):
            if 0 <= y + dy < 64 and g[y + dy][x] in 'YO': g[y + dy][x] = 'O'
    # 背の うろこの 光
    dots(g, 'R', [(36, 34), (30, 37), (22, 37), (15, 36)])
    # 尾の 先の 花びらの ひれ
    put(g, 8, 26, ['kkk.....', 'kAAkk...', '.kABBkk.', '.kABBCCk', '..kBCCk.', '...kkk..'])   # 尾の 先の 花びらの ひれ（後ろへ）
    return rows_of(g)

ARM = outline(['QP..', 'QQP.', '.QPP', 'w.w.'])

# ---------- 頭（花びらの えり、白い つの、こん棒の 触角）----------
HEAD = [
    '....kkkkkk.......',
    '..kkRRRRRRkk.....',
    '.kRRQQQQQQRRkk...',
    'kRQQQQQQQQQQQRk..',
    'kRQQQQQQQQQQQQRk.',
    'kQQQQQQQQQQQQQQRk',
    'kQQQQQQQQQQQQQkQk',
    'kQQQQQQQQQQQQQQPk',
    'kPQQQQkkkkkkkkkk.',
    'kPQQQkwkwkkkwkk..',
    '.kPPkYYYYYYYYk...',
    '..kkkkkkkkkkk....',
]
def head():
    g = G()
    # 花びらの えり（頭の 後ろに 扇の ように）
    for (bx, by, tx, ty) in [(46, 13, 37, 6), (45, 16, 36, 13), (46, 19, 38, 21)]:
        p = G(); stroke(p, bx, by, tx, ty, 2.6, 1.2, '2'); ink(g, p)
    g = shade(g, {'2': 'ABC'})
    # 触角（先が まるい 金の こん棒）と つの
    for (pts, tip) in [([(50, 8), (49, 3), (53, 0)], (53, 0))]:
        p = G()
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]): stroke(p, x0, y0, x1, y1, .6, .5, '6')
        ink(g, p)
    g = shade(g, {'6': 'QPP'})
    put(g, 52, -1 + 1, ['kkk', 'YYk', 'Ok.'])
    p = G(); stroke(p, 49, 10, 43, 5, 1.6, .5, '4'); ink(g, p)
    g = recolor(g, {'4': 'w'})
    put(g, 46, 9, HEAD)
    dots(g, 'k', [(61, 14)])
    return rows_of(g)
EYE = ['kkkk...', '.kkkkkk', '.kYYOk.', '..kkk..']
EYE_ALT = {
    'blink': ['kkkk...', '.kkkkkk', '.kkkkk.', '.......'],
    'atk0|atk1|atk2': ['kkkk...', '.kkkkkk', '.kwwYk.', '..kkk..'],
    'hit': ['.......', '.kk.kk.', '...k...', '.kk.kk.'],
    'ko': ['.......', '..k.k..', '...k...', '..k.k..'],
}
MOUTH = [
    'kkkkkkkkkkk',
    'kwkwkkkwkk.',
    'kPPPPPPPPk.',
    'kkwkwkwkk..',
    '.kYYYYYk...',
    '..kkkkk....',
]

# ---------- 鱗粉の ブレス（攻撃）と きらめき ----------
BREATH = [   # きらめく 鱗粉の 息（円すい形に ひろがる）
    '.............v....',
    '........v.......vA',
    '....w.......w....v',
    '..v....vAv.....v..',
    'vvAv..vAwAv...vAwA',
    'AwYwAvvAwYwAvvAwYw',
    'vvAv..vAwAv...vAwA',
    '..v....vAv.....v..',
    '....w.......w....v',
    '........v.......vA',
    '.............v....',
]
BREATH2 = [
    '.....v......w..',
    '..w.....vAv....',
    '......vAwAv...v',
    'v..w...vAv.....',
    '..vAv.......w..',
    '...v...v.......',
    '.w.......vAv...',
    '..........v....',
]
SPARK_A = ['.v...', 'vwv..', '.v..w']
SPARK_B = ['w..v.', '..vwv', '...v.']

def layers():
    W = {p: wing(p) for p in FW}; WF = {p: wing(p, True) for p in FW}
    return [
        dict(n='wingB', g='wingB', x=4, y=-1, rows=WF['up'], alt={'idle1|idle3|walk1|walk3|atk2|atk1': WF['mid'], 'walk2': WF['down']}),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['mid'], alt={'idle1|idle3': W['up'], 'walk0|atk0|hit|atk1': W['up'], 'walk2': W['down'], 'walk1|walk3|atk2': W['mid']}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='arm', g='head', x=43, y=29, rows=ARM),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='mouth', g='head', x=51, y=17, rows=MOUTH, only='atk1|atk2|hit'),
        dict(n='eye', g='head', x=50, y=12, rows=EYE, alt=EYE_ALT),
        dict(n='spark', g='root', x=10, y=5, rows=outline(SPARK_A), alt={'idle1|idle3|walk1|walk3': outline(SPARK_B)}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='breath', g='root', x=58, y=11, rows=outline(BREATH), only='atk1'),
        dict(n='breath2', g='root', x=60, y=9, rows=outline(BREATH2), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'head': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'head': (-3, -2)},
    'atk1': {'root': (1, 0), 'head': (2, 1)},
    'atk2': {'root': (2, 0), 'head': (2, 1)},
    'hit': {'root': (-4, -1), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root'}
