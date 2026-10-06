# カゼワイバ（かぜ・ドラゴン × ワイバーン）手打ち GBA風
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, grid_of, poly, ellipse, stamp, outline

META = dict(id='kazewaiba', name='カゼワイバ', types=['wind', 'dragon'], base='ワイバーン', size='L')
PAL = {
    'k': '#101018', 'l': '#183436',
    'R': '#9ee6b2', 'Q': '#3c9e80', 'P': '#1e5c58',      # うろこ（ひすい色）
    'F': '#f4eec4', 'G': '#c2b27a',                      # 腹
    'm': '#dcf8f6', 'n': '#8ccad8', 'o': '#4a7e9c',      # 翼の 膜（風の 空色）
    'S': '#f6f9fc', 'T': '#a2aec4', 'U': '#5a6482',      # 刃（尾・角・爪）
    'Y': '#ffe23a', 'r': '#e23c3c',                      # 目・口
}
LIGHT = set('RFmSY')
KEEP_BLACK = set('S')
RAMP = {'1': 'RQP', '2': 'FGG', '3': 'mnQ', '4': 'STU', '5': 'QPP'}

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
DARK = {'R': 'Q', 'Q': 'P', 'P': 'l', 'm': 'n', 'n': 'o', 'o': 'l', 'S': 'T', 'T': 'U', 'F': 'G'}

# ---------- 翼：腕の 骨（肩→ひじ→手首）＋ 3本の 指の 骨 ＋ 膜（指の あいだは 内へ えぐれた 波形）----------
WOY = 8   # 翼の 下書きは 上に 8ドット 余白を とる（ふりあげ用）
WP = {   # S=肩 E=ひじ W=手首 F=指先（前→後ろ） A=膜の 胴への つけね
    'up':   dict(E=(35, 14), W=(33, 2), F=[(22, -8), (16, 4), (20, 18)], A=(28, 32)),
    'hi':   dict(E=(33, 16), W=(28, 5), F=[(8, -1), (6, 13), (15, 25)], A=(27, 33)),
    'mid':  dict(E=(31, 18), W=(24, 10), F=[(1, 6), (4, 21), (14, 30)], A=(27, 33)),
    'down': dict(E=(30, 35), W=(24, 43), F=[(2, 41), (6, 53), (19, 58)], A=(33, 36)),
}
S0 = (37, 28)
def segd(px, py, a, b):
    (x0, y0), (x1, y1) = a, b; vx, vy = x1 - x0, y1 - y0; L = vx * vx + vy * vy or 1
    t = max(0, min(1, ((px - x0) * vx + (py - y0) * vy) / L)); return ((px - x0 - vx * t) ** 2 + (py - y0 - vy * t) ** 2) ** .5
def wing(pose, far=False):
    H = 64 + WOY
    def sh(p): return (p[0], p[1] + WOY)
    P = WP[pose]; S, E, W, A = sh(S0), sh(P['E']), sh(P['W']), sh(P['A']); F = [sh(f) for f in P['F']]
    # 膜の りんかく：指先と 指先の あいだは 手首へ 向かって えぐる（スカラップ）
    def notch(a, b, k=.32):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; return (round(mx + (W[0] - mx) * k), round(my + (W[1] - my) * k))
    edge = [F[0], notch(F[0], F[1]), F[1], notch(F[1], F[2]), F[2], notch(F[2], A, .25), A]
    g = grid(64, H); p = grid(64, H); poly(p, [S, E, W] + edge, 'n')
    # 膜の 色：骨の すぐ 下（光の 側）は 明、まん中は 中、うしろの ふちと 骨の 影は 暗（市松は 使わない）
    bones = [(S, E), (E, W)] + [(W, f) for f in F]
    for y in range(H):
        for x in range(64):
            if p[y][x] != 'n': continue
            d = min(segd(x, y, a, b) for a, b in bones)
            de = min(segd(x, y, a, b) for a, b in zip(edge, edge[1:]))
            p[y][x] = 'o' if de < 1.5 else 'm' if d < 1.8 and y < max(by for _, (bx, by) in bones) else 'n'
    if far:   # 奥の 翼は 影絵：外の 輪郭だけ、骨は 色の すじ（内側に 黒線を 入れない）
        for y in range(H):
            for x in range(64):
                if p[y][x] != '.': p[y][x] = 'o' if p[y][x] != 'm' else 'Q'
        for f in F:
            q = grid(64, H); stroke(q, W[0], W[1], f[0], f[1], .6, .4, 'P')
            for y in range(H):
                for x in range(64):
                    if q[y][x] != '.' and p[y][x] != '.': p[y][x] = 'P'
        q = grid(64, H); stroke(q, S[0], S[1], E[0], E[1], 2.0, 1.5, 'Q'); stroke(q, E[0], E[1], W[0], W[1], 1.5, 1.2, 'Q')
        for y in range(H):
            for x in range(64):
                if q[y][x] != '.': p[y][x] = 'Q' if (y > 0 and q[y - 1][x] != '.') else 'R'
        ink(g, p)
        return rows_of(recolor(g, {'R': 'Q', 'Q': 'P', 'k': 'k'}))
    # 指の 骨：膜の 中の すじ（上がわ 明・下がわ 中。内がわには 黒線を 入れず すっきり）
    for f in F:
        q = grid(64, H); stroke(q, W[0], W[1], f[0], f[1], .9, .4, 'Q')
        for y in range(H):
            for x in range(64):
                if q[y][x] != '.' and p[y][x] != '.': p[y][x] = 'R' if (y > 0 and q[y - 1][x] == '.') else 'Q'
        for y in range(H - 1):   # 骨の すぐ 下に 影
            for x in range(64):
                if q[y][x] != '.' and q[y + 1][x] == '.' and p[y + 1][x] in 'mn': p[y + 1][x] = 'o'
    ink(g, p)
    q = grid(64, H); stroke(q, S[0], S[1], E[0], E[1], 2.4, 1.8, '1'); stroke(q, E[0], E[1], W[0], W[1], 1.8, 1.4, '1'); ink(g, q)
    g = shade(g, {'1': 'RQP', '5': 'RPP'})
    # 手首の 刃の かぎ爪（手で）
    cl = ['.k.', 'kSk', 'kTk', '.k.'] if pose != 'down' else ['.k.', 'kTk', 'kSk', '.k.']
    put(g, W[0] - 1, W[1] - 4 if pose != 'down' else W[1] + 1, cl)
    if far: g = recolor(g, DARK)
    return rows_of(g)

# ---------- 胴・首・足 ----------
def body():
    g = G()
    p = G(); ellipse(p, 31, 32, 11, 6.5, '1')
    poly(p, [(22, 35), (41, 33), (38, 38), (26, 39)], '2')
    ink(g, p)
    # 首（下側は 腹の 色）
    p = G(); stroke(p, 38, 30, 45, 25, 4.4, 3.6, '1'); stroke(p, 45, 25, 49, 21, 3.6, 3.2, '1')
    stroke(p, 41, 33, 48, 26, 1.6, 1.4, '2'); ink(g, p)
    g = shade(g, dk=.85)
    # 背中の ひれ（風を 切る 小さな 刃）を 手で
    for (x, y) in ((24, 27), (29, 26), (34, 26), (40, 22), (45, 18)):
        put(g, x, y - 2, ['k..', 'Sk.', 'TTk'])
    # 腹の 段（うろこの すじ）
    dots(g, 'G', [(26, 37), (29, 37), (32, 37), (35, 36), (38, 35), (44, 29)])
    dots(g, 'R', [(28, 29), (31, 28), (34, 28)])
    dots(g, 'P', [(29, 31), (32, 30), (35, 30), (38, 31)])
    return rows_of(g)

LEG = [   # ちぢめた 後ろ足（白い 刃の かぎ爪）
    '.kkk...',
    'kRQQk..',
    'kQQPPk.',
    '.kQPPk.',
    '..kPPk.',
    '.kQPPkk',
    'kSkSkSk',
    'kk.k.k.',
]
LEG_FAR = [
    '.kkk..',
    'kQPPk.',
    '.kPPk.',
    '..kPk.',
    '.kTkTk',
    '.k.k..',
]

# ---------- 頭（細長い 竜の 頭、後ろへ 反った 刃の 角）----------
HEAD = [   # 手打ち：細長い くさび形の 頭、あごは 腹の 色
    '.....kkkkkk.......',
    '...kkRRRRRRkkk....',
    '..kRRRRRRRRRRRkk..',
    '.kRRQQQQQQQQQQRRk.',
    '.kRQQQQQQQQQQQQQRk',
    'kRQQQQQQQQQQQQQQQk',
    'kQQQQQQQQQQQQQQkQk',
    'kQQQQQQQQQQQQQQQPk',
    'kPQQQQQkkkkkkkkkkk',
    'kPQQQkkSkSkkSkSk..',
    '.kPPkFFFFFFFFFkk..',
    '..kPGGGGGGGGkk....',
    '...kkkkkkkkk......',
]
def head():
    g = G()
    for (bx, by, tx, ty) in [(50, 15, 39, 9), (50, 18, 41, 15)]:
        p = G(); stroke(p, bx, by, tx, ty, 2.0, .6, '4'); ink(g, p)
    g = shade(g, {'4': 'STU'})
    put(g, 47, 13, HEAD)
    put(g, 45, 21, ['kkk.', 'kSTk', '.kTk', '..k.'])   # ほおの 刃
    return rows_of(g)

EYE = ['kkk....', '.Rkkkk.', '..YYkk.', '..kkk..']   # まゆの 刃で おおわれた つり目
EYE_ALT = {
    'blink': ['kkk....', '.Rkkkk.', '..kkkk.', '.......'],
    'atk0|atk1|atk2': ['kkk....', '.Rkkkk.', '..SSYk.', '..kkk..'],
    'hit': ['.......', '.kk.kk.', '...k...', '.kk.kk.'],
    'ko': ['.......', '..k.k..', '...k...', '..k.k..'],
}
MOUTH_OPEN = [   # 攻撃：口を 開く
    'kkkkkkkkkkk.',
    'kSkSrrSkSkk.',
    'krrrrrrrrrk.',
    'kkSrSrrSrk..',
    '.kFFFFFFkk..',
    '..kkkkkkk...',
]

# ---------- 尾（長い むち、先は 三日月の 刃）----------
def tail(pose):
    g = G()
    path = {
        'rest': [(25, 33), (17, 34), (11, 37), (7, 42), (6, 47)],
        'up':   [(25, 32), (19, 27), (16, 19), (19, 11), (26, 6)],
        'fwd':  [(25, 31), (21, 21), (28, 10), (40, 5), (52, 6)],
        'low':  [(25, 33), (23, 40), (32, 46), (45, 46), (55, 42)],
    }[pose]
    p = G()
    n = len(path) - 1
    for i in range(n):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        stroke(p, x0, y0, x1, y1, 3.2 - 2.4 * i / n, 3.2 - 2.4 * (i + 1) / n, '1')
    ink(g, p)
    g = shade(g, dk=.85)
    # 尾の 節（すじ）
    for (x0, y0), (x1, y1) in zip(path[1:-1], path[2:]):
        g[y0][x0] = 'P'
    ex, ey = path[-1]
    BL = {
        'rest': (-6, -3, ['......kkk..', '.kk..kSSTk.', 'kSSkkSSTTk.', 'kSSSSSTTk..', '.kSSSTTk...', '.kSSTTUk...', '.kSTTUk....', '..kTUk.....', '..kUk......', '...k.......']),
        'up':   (-1, -6, ['..kkk.......', '.kSSSkkk....', 'kSSSSSSTkk..', '.kTTSSSSTTk.', '..kkTTTTTUUk', '....kkkkkkk.']),
        'fwd':  (-1, -2, ['kkkk.......', 'kSSSkk.....', '.kTSSSkk...', '..kTTSSSk..', '...kkTTSSk.', '.....kkTTSk', '.......kTSk', '........kTk', '.........k.']),
        'low':  (-1, -8, ['.......kk.', '......kSk.', '.....kSSk.', '....kSSTk.', '...kSSTk..', '..kSSTTk..', '.kSTTUk...', 'kTTUkk....', 'kkkk......']),
    }[pose]
    put(g, ex + BL[0], ey + BL[1], BL[2])
    return rows_of(g)

def OL(rows): return outline(rows)
SLASH = [   # 尾の 刃が 頭ごしに 切りさく 風の 三日月
    '...mm.........',
    '.....mmm......',
    '........mmS...',
    '..........mST.',
    '...........mST',
    '............mS',
    '............mS',
    '............mS',
    '...........mST',
    '..........mST.',
    '.........mST..',
    '.......mmS....',
    '....mmm.......',
]
GUST = ['m..mm....mm', '.mm..m..m..', '......mm...']

def layers():
    W = {p: wing(p) for p in WP}; WF = {p: wing(p, True) for p in WP}
    T = {p: tail(p) for p in ('rest', 'up', 'fwd', 'low')}
    return [
        dict(n='wingB', g='wingB', x=-4, y=-1 - WOY, rows=WF['up'], alt={'walk1|walk3|atk2': WF['hi'], 'walk2|atk1': WF['mid']}),
        dict(n='legFar', g='body', x=35, y=36, rows=LEG_FAR),
        dict(n='tail', g='tail', x=0, y=0, rows=T['rest'], alt={'atk0': T['up'], 'atk1': T['fwd'], 'atk2': T['low']}),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='leg', g='body', x=27, y=36, rows=LEG),
        dict(n='head', g='head', x=0, y=0, rows=head()),
        dict(n='mouth', g='head', x=53, y=21, rows=MOUTH_OPEN, only='atk1|atk2|hit'),
        dict(n='eye', g='head', x=52, y=16, rows=EYE, alt=EYE_ALT),
        dict(n='wingF', g='wingF', x=0, y=-WOY, rows=W['mid'], alt={'idle1|idle3': W['hi'], 'walk0|hit|atk0': W['up'], 'walk2|atk1': W['down'], 'walk1|walk3|atk2': W['mid']}),
        dict(n='gust', g='root', x=26, y=56, rows=OL(GUST), only='walk2'),
        dict(n='slash', g='root', x=51, y=10, rows=OL(SLASH), only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, -1), 'tail': (0, -1)},
    'idle2': {'head': (0, 1)},
    'idle3': {'body': (0, 1), 'head': (0, -1)},
    'blink': {},
    'walk0': {'body': (0, 1)},
    'walk1': {},
    'walk2': {'body': (0, -2)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-3, 1), 'head': (-2, 2)},
    'atk1': {'root': (2, 1), 'head': (-1, 4)},
    'atk2': {'root': (4, 0), 'head': (0, 2)},
    'hit': {'root': (-4, -1), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wingF': 'body', 'wingB': 'body', 'tail': 'body', 'body': 'root'}
