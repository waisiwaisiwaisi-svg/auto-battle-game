# ヒノコギリ（ほのお・はがね × ノコギリザメ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と のこぎりの 吻、小さく 丸い 胴、短い ひれ）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり → 左上光の 陰影 → 輪郭）。仕上げの 目・牙・模様は 手で 打つ ----------
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < N and 0 <= x < N: g[y][x] = ch
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g
def tube(p, path, rad, ch):
    """太さの かわる 管（手足・首・尾の あたり）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < N and 0 <= y < N and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def ink(p, ch='k'):
    """まわりに 1ドットの 輪郭"""
    g = G()
    for y in range(N):
        for x in range(N):
            if p[y][x] != '.': g[y][x] = p[y][x]
            elif any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = ch
    return g
def shade(p, ramps, r=2, hi=.3, lo=-.28):
    """左上から 光：ふくらみの 向きで 明・中・暗、上と 左の ふちは 明（三日月）、下と 右の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(N)] for y in range(N)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1): n += 1; s += m[yy][xx] if 0 <= yy < N and 0 <= xx < N else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(N):
        for x in range(N):
            c = p[y][x]
            if c not in ramps: continue
            h, md, d = ramps[c]
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5
            out[y][x] = h if v > hi else d if v < lo else md
            if at(p, x, y - 1) == '.' or at(p, x - 1, y) == '.': out[y][x] = h
            if at(p, x, y + 1) == '.' or at(p, x + 1, y) == '.': out[y][x] = d
    return out
def recol(g, mp): return [[mp.get(c, c) for c in r] for r in g]
def make(draw, ramps, r=2, hi=.3, lo=-.28, post=None, post2=None, dk=None):
    """draw(p) で あたり → 陰影 → post(s) 手打ち → 輪郭 → post2(g) 手打ち"""
    p = G(); draw(p); s = shade(p, ramps, r, hi, lo)
    if post: post(s)
    if dk: s = recol(s, dk)
    g = ink(s)
    if post2: post2(g)
    return rows_of(g)
def shift(rows, dx, dy):
    g = G()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.' and 0 <= x + dx < N and 0 <= y + dy < N: g[y + dy][x + dx] = c
    return rows_of(g)
def over(*rowsets):
    g = G()
    for rs in rowsets: stamp(g, rs, 0, 0)
    return rows_of(g)
META = dict(id='hinokogiri', name='ヒノコギリ', types=['fire', 'steel'], base='ノコギリザメ', size='M')
PAL = {
    'k': '#101018', 'l': '#262a40',
    'S': '#e2e8f2', 'T': '#98a4bc', 'U': '#566080',      # 鋼の からだ（明・中・暗）
    'N': '#34304a', 'P': '#6a6880',                      # 刃の 黒鉄（暗・中）
    'Y': '#ffe45c', 'O': '#ff7a1e', 'R': '#c02a22',      # 赤熱（目の 虹彩も 兼ねる）
    'E': '#f4e2c8', 'F': '#c4a888',                      # 腹（焼けた 白）
    'w': '#ffffff',
}
LIGHT = set('SYEw')
KEEP_BLACK = set('wYO')
RAMP = {'1': 'STU', '2': 'EEF', '3': 'PPN'}
DARK = {'S': 'T', 'T': 'U', 'E': 'F'}

def rivets(s, pts):
    for x, y in pts:
        if s[y][x] != '.': s[y][x] = 'S'
        if at(s, x + 1, y + 1) not in '.k': s[y + 1][x + 1] = 'U'

# ---------- 胴（小さく 丸い）と 尾 ----------
def body():
    def d(p):
        ellipse(p, 16, 32, 8, 5.5, '1')
        poly(p, [(12, 35), (24, 35), (24, 38), (13, 37)], '2')
    def post(s):
        line(s, 15, 27, 14, 36, 'U'); line(s, 16, 27, 15, 36, 'S')     # 鋼の 板の つぎ目
        rivets(s, [(11, 31), (19, 29)])
    return make(d, RAMP, post=post)
def tail(ph=0):
    def d(p):
        tube(p, [(10, 31), (5, 30)], [4.5, 3.2], '1')
        if ph == 0: poly(p, [(7, 30), (0, 17), (3, 17), (9, 27), (8, 33), (3, 44), (0, 44), (5, 33)], '1')
        else: poly(p, [(7, 30), (1, 19), (4, 19), (9, 27), (8, 33), (4, 42), (1, 42), (5, 33)], '1')
    def post(s):
        line(s, 8, 29, 8, 33, 'U'); dots(s, 'O', [(2, 19), (2, 42)] if ph == 0 else [(2, 21), (2, 40)])
    return make(d, RAMP, r=1, post=post)
def dorsal():
    return make(lambda p: poly(p, [(16, 26), (21, 10), (25, 10), (28, 22)], '1'), RAMP, r=1,
                post=lambda s: (line(s, 22, 11, 21, 15, 'O'), line(s, 23, 11, 22, 14, 'Y')))
def pfin(far=False):
    return make(lambda p: poly(p, [(25, 35), (32, 36), (27, 46), (22, 46)], '1'), RAMP, r=1, dk=DARK if far else None,
                post=None if far else (lambda s: line(s, 26, 37, 24, 44, 'U')))

# ---------- 頭（大きい）：鋼の かぶと、赤熱の えら、下あごの 牙 ----------
def head(open_=False):
    def d(p):
        ellipse(p, 33, 27, 12.5, 12, '1')
        poly(p, [(40, 19), (46, 23), (50, 27), (50, 32), (45, 37), (36, 39)], '1')
        poly(p, [(25, 35), (46, 34), (43, 39), (29, 40)], '2')
    def post(s):
        # 鋼の かぶとの つぎ目と びょう
        line(s, 27, 17, 30, 29, 'U'); line(s, 26, 17, 29, 29, 'S')
        # 頭の 上の 黒鉄の かぶと板（まゆの ひさしへ つづく）
        for y in range(15, 21):
            for x in range(28, 46):
                if s[y][x] in 'STU' and y - 15 < (x - 26) // 3 + 2 and y < 20: s[y][x] = 'P' if y > 15 and at(s, x, y - 1) != '.' else 'S'
        rivets(s, [(23, 24), (37, 31), (23, 31)])
        # 赤熱の えら（3本）
        for x in (25, 27, 29):
            line(s, x + 1, 29, x, 34, 'O'); s[30][x + 1] = 'Y'; s[31][x + 1] = 'Y'
        # 口：上あごの 牙
        if open_:
            put(s, ['kkkkkkkkkkkkk', 'kwRwRRwRRwRwk', 'kRRRRRRRRRRRk', 'kRRRRRRRRRRk.', 'kRwRRRwRRwkk.', '.kkkkkkkkk...'], 36, 32)
        else:
            put(s, ['...kkkkkkkkk', 'kkkkwFkwFFwk', '.FwFFFwFFFk.'], 36, 34)
    return make(d, RAMP, lo=-.34, post=post)

# 目：鋼の まゆの ひさし＋白い 光＋赤熱の 虹彩（明 Y・暗 O）＋たての ひとみ
EYE = ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwYYkYYk', '.kwYYOkOYk', '.kYOOOkOOk', '..kOOkkOk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kSSSSSSSk', '.kkkkkkkkk', '.kTTTTTTTk', '..kTTTTTk.', '...kkkkk..'],
    'hit':   ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kkkTTTTkk', '.kTTkkkkTk', '.kTTTTTkkk', '..kkkTTTk.', '...kkkkk..'],
    'atk0|atk1|atk2': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwwYkYwk', '.kwYYYkYYk', '.kYYYYkYYk', '..kOOkkOk.', '...kkkkk..'],
    'ko':    ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kTkTTTkTk', '.kTTkTkTTk', '.kTkTTTkTk', '..kTTTTTk.', '...kkkkk..'],
}

# ---------- のこぎりの 吻（見せ所）：黒鉄の 刃と 赤熱した 大きな 歯の 列 ----------
def saw(hot=0):
    def d(p): poly(p, [(47, 25), (62, 27), (64, 29), (64, 31), (62, 33), (47, 35)], '3')
    def post(s):
        for x in range(48, 63):
            if s[29][x] != '.': s[29][x] = 'P'
            if s[30][x] != '.': s[30][x] = 'k' if x % 4 == 0 else 'N'
        if hot:
            for x in range(49, 62, 2): s[28][x] = 'R'; s[31][x + 1] = 'R'
    def post2(g):
        # 上と 下に 歯（三角 2はば×3だか）：つけ根 O、先 Y
        for i, x in enumerate(range(49, 63, 4)):
            ty = 25 if x < 56 else 26
            for (dx, dy, c) in ((0, 0, 'O'), (1, 0, 'O'), (0, -1, 'O'), (1, -1, 'Y' if hot else 'O'), (1, -2, 'Y'), (0, -2, 'k'), (2, -1, 'k'), (2, -2, 'k'), (1, -3, 'k'), (-1, -1, 'k')):
                g[ty + dy][x + dx] = c
            by = 35 if x < 56 else 34
            for (dx, dy, c) in ((0, 0, 'O'), (1, 0, 'O'), (0, 1, 'O'), (1, 1, 'Y' if hot else 'O'), (1, 2, 'Y'), (0, 2, 'k'), (2, 1, 'k'), (2, 2, 'k'), (1, 3, 'k'), (-1, 1, 'k')):
                g[by + dy][x + dx] = c
    return make(d, RAMP, r=1, post=post, post2=post2)
SPARK = ['Y...O..Y', '..Y..O..', 'O..YwY.O', '.Y.wwwY.', 'O..YwY..', '..O..Y.O', 'Y...O...']
SLASH = ['......YY', '....YYO.', '..YYOO..', 'YYOO....', 'OO......']

def layers():
    H = head(); HO = head(True)
    return [
        dict(n='finF', g='finB', x=4, y=-1, rows=pfin(True)),
        dict(n='tail', g='tail', x=0, y=0, rows=tail(0), alt={'idle1|idle2|walk1|walk2|atk1': tail(1)}),
        dict(n='dorsal', g='body', x=0, y=1, rows=dorsal()),
        dict(n='body', g='body', x=0, y=0, rows=body()),
        dict(n='saw', g='saw', x=0, y=0, rows=saw(), alt={'atk0|atk1|atk2': saw(1)}),
        dict(n='head', g='head', x=0, y=0, rows=H, alt={'atk1': HO}),
        dict(n='eye', g='head', x=36, y=18, rows=EYE, alt=EYE_ALT),
        dict(n='fin', g='finA', x=0, y=0, rows=pfin()),
        dict(n='spark', g='saw', x=57, y=26, rows=SPARK, only='atk1'),
        dict(n='slash', g='saw', x=55, y=18, rows=SLASH, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'finA': (0, 1)}, 'idle2': {'body': (0, 1), 'finA': (0, 2), 'finB': (0, 1)}, 'idle3': {'finA': (0, 1)}, 'blink': {},
    'walk0': {'tail': (0, -1), 'finA': (-1, 0)}, 'walk1': {'body': (0, -1), 'finB': (0, -1)},
    'walk2': {'tail': (0, 1), 'finA': (1, 0)}, 'walk3': {'body': (0, 1), 'finB': (0, 1)},
    'atk0': {'root': (-3, 1), 'head': (0, 1), 'tail': (1, 0)},
    'atk1': {'root': (4, 0)},
    'atk2': {'root': (3, 0), 'saw': (0, -1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'saw': 'head', 'tail': 'body', 'finA': 'body', 'finB': 'body', 'body': 'root'}
