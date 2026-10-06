# ハチショウグン（むし・どく × スズメバチ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

EYE_BOX = (46, 18, 7, 11)
META = dict(id='hachishogun', name='ハチショウグン', types=['bug', 'poison'], base='スズメバチ', size='M')
PAL = {
    'k': '#101018', 'l': '#3a2412',
    'R': '#ffcc4a', 'Q': '#e08a1e', 'P': '#9a4a12',      # こはく色の 体
    'S': '#d4dcea', 'T': '#72809c', 'U': '#363e5a',      # はがねの よろい
    'g': '#c8ff5c', 'G': '#4eae30',                      # 毒
    'w': '#f4fbff', 'c': '#a6c6e2',                      # すきとおる 翅
    'r': '#ff3a3a', 'd': '#8a1420', 'o': '#ff9c8c',      # 目（複眼の 赤・濃い 赤・反射）
}
LIGHT = set('RSgwr')
RAMP = {'1': 'RQP', '4': 'STU', '6': 'TUU', '7': 'gGG', '8': 'wcc'}

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
def rell(g, cx, cy, a, b, ang, ch):
    """かたむけた だ円（あたり用）"""
    ca, sa = math.cos(ang), math.sin(ang)
    for y in range(64):
        for x in range(64):
            dx, dy = x - cx, y - cy; u = dx * ca + dy * sa; v = -dx * sa + dy * ca
            if (u / a) ** 2 + (v / b) ** 2 <= 1: g[y][x] = ch

# ---------- 腹（こはくと はがねの しま、先に 光る 毒ぶくろ と 槍の 針）----------
AB = {   # 腰の つけね → 先の 向き、中心、針の 先
    'rest': dict(c=(26, 40), d=(-1, .55), a=8.5, b=5.8, sting=(12, 49)),
    'curl': dict(c=(31, 44), d=(-.15, 1), a=8.5, b=5.8, sting=(35, 59)),
    'stab': dict(c=(37, 43), d=(.75, .66), a=8.5, b=5.8, sting=(58, 54)),
}
def abdomen(pose):
    P = AB[pose]; g = G()
    dx, dy = P['d']; L = (dx * dx + dy * dy) ** .5; dx, dy = dx / L, dy / L
    cx, cy = P['c']; a, b = P['a'], P['b']
    tx, ty = round(cx + dx * (a - 1)), round(cy + dy * (a - 1))
    sx, sy = P['sting']
    p = G(); stroke(p, tx, ty, sx, sy, 2.2, .5, '4'); ink(g, p)
    # 槍の かえし
    bx_, by_ = round(tx + (sx - tx) * .6), round(ty + (sy - ty) * .6)
    p = G(); stroke(p, bx_, by_, bx_ - round((sx - tx) * .18) + round((sy - ty) * .2), by_ - round((sy - ty) * .18) - round((sx - tx) * .2), 1.0, .4, '4'); ink(g, p)
    p = G(); rell(p, cx, cy, a, b, math.atan2(dy, dx), '1')
    # しま：軸に そって 4ドットごとに はがね色の 帯
    for y in range(64):
        for x in range(64):
            if p[y][x] != '1': continue
            u = (x - cx) * dx + (y - cy) * dy
            if -a * .75 < u and (u + a) % 5 < 2: p[y][x] = '6'
            if u > a * .62: p[y][x] = '7'
    ink(g, p)
    g = shade(g)
    # 毒ぶくろの 光（手で）と 針の 先の しずく
    gx, gy = round(cx + dx * a * .8), round(cy + dy * a * .8)
    dots(g, 'w', [(gx - 1, gy - 1)])
    dots(g, 'g', [(sx, sy + 1)] if pose == 'rest' else [])
    return rows_of(g)

# ---------- 翅（すきとおる 2対）----------
WG = {'up': [(28, 1), (24, 9)], 'hi': [(19, 6), (22, 14)], 'mid': [(13, 13), (19, 20)], 'down': [(14, 28), (20, 30)]}
def wings(pose, far=False):
    g = G()
    for (tx, ty), (bx, by), bb in reversed(list(zip(WG[pose], [(38, 28), (36, 29)], (3.6, 2.6)))):
        p = G(); ang = math.atan2(ty - by, tx - bx); L = ((tx - bx) ** 2 + (ty - by) ** 2) ** .5
        rell(p, (bx + tx) / 2, (by + ty) / 2, L / 2 + .5, bb, ang, '8'); ink(g, p)
    g = shade(g, {'8': 'wcc'}, dk=.6)
    # 翅脈（軸の すじ）と 市松の すきとおり
    for y in range(64):
        for x in range(64):
            if g[y][x] == 'c' and (x + y) % 2 == 0 and y > 0 and g[y - 1][x] == 'w': g[y][x] = 'w'
    for (tx, ty), (bx, by) in zip(WG[pose], [(38, 28), (36, 29)]):
        n = max(abs(tx - bx), abs(ty - by))
        for i in range(2, n - 2):
            x, y = round(bx + (tx - bx) * i / n), round(by + (ty - by) * i / n + 1)
            if g[y][x] in 'wc': g[y][x] = 'T'
    if far: g = recolor(g, {'w': 'c', 'c': 'T', 'T': 'U'})
    return rows_of(g)

# ---------- 胸（はがねの よろい、こはくの ふち）----------
def thorax():
    g = G()
    p = G(); rell(p, 32, 35, 2.6, 2.2, 0, '6'); ink(g, p)          # くびれた 腰
    p = G(); rell(p, 39, 32, 6.8, 5.6, -.3, '4')
    for y in range(64):
        for x in range(64):
            if p[y][x] == '4' and 0 <= (x - 39) * .5 + (y - 32) - 2 < 2.2: p[y][x] = '1'   # こはくの 帯
    ink(g, p)
    # 肩の 大袖（よろいの 板）
    p = G(); poly(p, [(37, 27), (43, 26), (45, 30), (41, 32), (36, 31)], '4'); ink(g, p)
    g = shade(g)
    dots(g, 'k', [(42, 29), (40, 36)])
    dots(g, 'S', [(41, 28), (39, 35)])     # 鋲
    return rows_of(g)

LEGS = [   # 3対の 足（こはくの 関節、はがねの すね、白い かぎ爪）
    '..........kk..',
    '.kk...kk.kQRk.',
    'kQRk.kQRkkTUk.',
    'kTUk.kTUk.kTUk',
    'kTUk.kTUk..kTUk',
    '.kTUkkTUk...kTk',
    '.kTUk.kTk...kSk',
    '..kSk.kSk....k.',
    '...k...k.......',
]

# ---------- 頭（かぶとの 頭、大きな 赤い 複眼、刃の あご、三日月の 触角）----------
def head():
    g = G()
    # 三日月の 触角（ひじで 折れて 前へ）：かぶとの 前立ての よう
    for pts, ch in [([(48, 20), (46, 10), (51, 3)], '6'), ([(51, 20), (52, 9), (58, 4)], '1')]:
        p = G()
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]): stroke(p, x0, y0, x1, y1, 1.0, .7, ch)
        ink(g, p)
    p = G(); rell(p, 50, 25, 9.2, 8.2, .15, '1')
    poly(p, [(42, 21), (48, 15), (56, 16), (53, 20), (43, 26)], '4')    # かぶとの 板
    ink(g, p)
    g = shade(g)
    put(g, 55, 27, [   # 刃の あご（上下で はさむ）
        '.kkkk.....',
        'kSSSTkk...',
        'kTSSSSTk..',
        '.kkkkSSTk.',
        '.kk...kTk.',
        'kSSTkkTk..',
        '.kTTTTk...',
        '..kkkk....',
    ])
    dots(g, 'P', [(46, 32), (47, 32), (48, 32), (49, 33)])
    return rows_of(g)

# D 複眼：たて長の そら豆形（前の ふちが へこむ）。赤い 地に 濃い 赤の 点の 段（あみ目）、上に 白〜うす赤の 反射の 帯。
# ひとみは なし。前へ 下がる 黒い まゆの 板で 怒り顔
EYE = ['kkk....', '.kkkkkk', 'kwwookk', 'korrrrk', 'krdrdrk', 'krrrrk.', 'kdrdrk.', 'krrrrrk', 'krdrdrk', '.kdddk.', '..kkk..']
EYE_ALT = {
    'blink': ['kkk....', '.kkkkkk', 'kkkkkkk', 'kkkkkkk', 'krdrdrk', 'krrrrk.', 'kdrdrk.', 'krrrrrk', 'krdrdrk', '.kdddk.', '..kkk..'],
    'atk0|atk1|atk2': ['kkk....', '.kkkkkk', 'kwwwwkk', 'kwooook', 'kororok', 'kooook.', 'krorok.', 'koooook', 'kororok', '.krrrk.', '..kkk..'],
    'hit': ['....kkk', '.kkkk..', 'kddrrdk', 'kdrdrdk', 'kddddk.', 'kddddk.', 'kdrdrk.', 'kdddddk', 'kdrdrdk', '.kdddk.', '..kkk..'],
    'ko': ['.......', '.kkkkk.', 'kddddkk', 'kkdddkk', 'kdkdkdk', 'kddkdk.', 'kdkdkk.', 'kkdddkk', 'kddddkk', '.kdddk.', '..kkk..'],
}

LEGS = [   # 3対の 足（短く 太く：こはくの 関節、はがねの すね、白い かぎ爪）。前足は つかみかかる 形
    '.kk.....kk.....kkk.',
    'kQRk...kQRk...kRQQk',
    'kTUk...kTUk..kTUkk.',
    '.kTUk..kTUk...kTUk.',
    '.kTUk..kTUk....kTSk',
    '..kSSk.kSSk.....kSk',
    '...kSk..kSk......k.',
    '....k....k.........',
]

SPLASH = [   # 毒の しぶき
    '...g.....',
    '.g..gG...',
    'g.gGgGg.g',
    '..gGg..g.',
    '.g...g...',
]
DRIP = ['g.', '..', 'g.', 'G.']

def OL(rows): return outline(rows)
def layers():
    W = {p: wings(p) for p in WG}; WF = {p: wings(p, True) for p in WG}
    A = {p: abdomen(p) for p in AB}
    return [
        dict(n='wingB', g='wingB', x=3, y=-2, rows=WF['hi'], alt={'idle1|idle3|walk1|walk3|atk2': WF['mid'], 'walk0|atk0|hit': WF['up'], 'walk2|atk1': WF['down']}),
        dict(n='abd', g='abd', x=0, y=0, rows=A['rest'], alt={'atk0': A['curl'], 'atk1|atk2': A['stab']}),
        dict(n='legs', g='legs', x=31, y=35, rows=LEGS),
        dict(n='thorax', g='body', x=0, y=0, rows=thorax()),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='eye', g='head', x=46, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=0, rows=W['mid'], alt={'idle1|idle3': W['hi'], 'walk0|atk0|hit': W['up'], 'walk2|atk1': W['down'], 'walk1|walk3|atk2': W['mid']}),
        dict(n='drip', g='abd', x=12, y=51, rows=OL(DRIP), only='idle1|idle2|walk1|walk3'),
        dict(n='splash', g='root', x=58, y=47, rows=OL(SPLASH), only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1), 'abd': (0, 1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'abd': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1), 'legs': (-1, 0)},
    'walk1': {'abd': (0, -1)},
    'walk2': {'body': (0, -2), 'legs': (1, -1)},
    'walk3': {'body': (0, -1), 'abd': (0, 1)},
    'atk0': {'root': (-4, -2), 'head': (-1, 1)},
    'atk1': {'root': (1, -2), 'head': (1, 0)},
    'atk2': {'root': (3, -2), 'head': (1, 1)},
    'hit': {'root': (-4, -1), 'head': (-2, -1), 'abd': (1, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'abd': 'body', 'legs': 'body', 'body': 'root'}
