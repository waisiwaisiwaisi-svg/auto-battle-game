# ヒョウザンワニ（こおり・みず × ワニ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 大あご、短く 丸い 胴、太く 短い 足、背に 氷山の とげ）
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
META = dict(id='hyouzanwani', name='ヒョウザンワニ', types=['ice', 'water'], base='ワニ', size='L')
PAL = {
    'k': '#101018', 'l': '#14303e',
    'A': '#86ccd6', 'B': '#3c8698', 'C': '#1e4a62',      # うろこ（明・中・暗）
    'E': '#eaf2dc', 'F': '#a4b89c',                      # 腹・あご下
    'c': '#f2ffff', 'i': '#a6e2ff', 'j': '#5aa2de',      # 氷（白・水色・青）
    'R': '#b0304a',                                      # 口の 中
    'Y': '#ffe466', 'O': '#e2862a',                      # 目の 虹彩（明・暗）
    'w': '#ffffff',
}
LIGHT = set('AEciYw')
KEEP_BLACK = set('wYO')
RAMP = {'1': 'ABC', '2': 'EEF', '3': 'cij'}
DARK = {'A': 'B', 'B': 'C', 'E': 'F', 'c': 'i', 'i': 'j'}

# ---------- 胴（短く 丸い）・尾・足 ----------
def body():
    def d(p):
        ellipse(p, 20, 42, 12, 8.5, '1')
        poly(p, [(12, 47), (31, 46), (29, 50), (14, 50)], '2')
    def post(s):
        # 背の うろこの 列（ぼこぼこ）
        for x in range(11, 31, 4):
            dots(s, 'A', [(x, 36), (x + 1, 35)]); dots(s, 'C', [(x + 2, 36)])
        for x in range(13, 30, 3):
            if s[49][x] in 'EF': s[49][x] = 'F'
    return make(d, RAMP, post=post)
def tail(ph=0):
    def d(p): tube(p, [(10, 42), (4, 44), (1, 40 + ph)], [6, 4, 2.2], '1')
    def post(s): dots(s, 'A', [(5, 40), (3, 39)]); dots(s, 'C', [(6, 41)])
    return make(d, RAMP, r=1, post=post)
def leg(x0, far=False):
    """短く 太い ワニの 足：外へ ふんばる ひじ＋ひらいた 指"""
    def d(p):
        tube(p, [(x0 + 1, 47), (x0 - 1, 52), (x0 + 2, 56)], [3.8, 3, 2.6], '1')
        ellipse(p, x0 + 4.5, 57.8, 5, 2.3, '1')
    def post2(g):
        for dx in (2, 5, 8): g[59][x0 + dx] = 'w'; g[60][x0 + dx] = 'k'; g[60][x0 + dx + 1] = 'k' if g[60][x0 + dx + 1] == '.' else g[60][x0 + dx + 1]
        g[57][x0 + 6] = 'k'
        g[52][x0 + 1] = 'k' if g[52][x0 + 1] != '.' else '.'
    return make(d, RAMP, r=1, dk=DARK if far else None, post2=post2)

# ---------- 氷山の とげ（背の うろこの 突起 ⇔ 氷山の 頂）----------
def shard(pts):
    def d(p): poly(p, pts, '3')
    def post(s):
        # 結晶の 面：左は 光、まん中に 稜線
        x0 = sum(x for x, _ in pts) // len(pts)
        top = min(pts, key=lambda q: q[1])
        line(s, top[0], top[1] + 1, x0, max(y for _, y in pts) - 1, 'i')
    return make(d, RAMP, r=1, hi=.1, lo=-.2, post=post)
SHARDS = [
    [(5, 37), (8, 29), (11, 37)],
    [(10, 36), (14, 23), (16, 22), (19, 35)],
    [(17, 35), (22, 16), (24, 15), (28, 34)],
    [(25, 35), (30, 23), (32, 23), (34, 36)],
    [(34, 30), (37, 22), (40, 29)],
]

# ---------- 頭（大きい）と 大あご（見せ所）----------
def head():
    def d(p):
        ellipse(p, 40, 31, 10.5, 9.5, '1')                               # 後頭部（大きく 丸い）
        poly(p, [(36, 24), (48, 25), (57, 28), (63, 30), (64, 35), (61, 38), (36, 39)], '1')   # 上あご（太い）
    def post(s):
        dots(s, 'C', [(61, 31), (60, 31)]); dots(s, 'A', [(59, 29), (60, 29)])                 # 鼻の こぶ
        for x in range(48, 59, 3): dots(s, 'A', [(x, 28)]); dots(s, 'C', [(x + 1, 29)])      # うろこの 段
        line(s, 37, 38, 61, 37, 'C')
    def post2(g):
        # 上あごの 牙：ふちから 下へ はみ出す
        for x in (40, 44, 48, 52, 56, 60):
            g[39][x] = 'w'; g[40][x] = 'w' if x in (44, 52, 60) else g[40][x]
    return make(d, RAMP, lo=-.32, post=post, post2=post2)
def jaw(open_=False):
    def d(p):
        if open_:
            poly(p, [(32, 38), (44, 42), (56, 47), (63, 49), (61, 53), (34, 49)], '1'); poly(p, [(35, 46), (60, 51), (57, 53), (36, 50)], '2')
        else:
            poly(p, [(32, 37), (62, 38), (61, 42), (53, 46), (34, 47)], '1'); poly(p, [(35, 43), (56, 43), (51, 46), (36, 46)], '2')
    def post2(g):
        # 下あごの 牙：上へ はみ出す
        if open_:
            for x in (41, 47, 53, 59):
                y = round(41 + (x - 41) * 7 / 20); g[y - 1][x] = 'w'; g[y - 2][x] = 'w'; g[y - 3][x] = 'k'
        else:
            for x in (42, 50, 58): g[38][x] = 'w'; g[37][x] = 'w'; g[36][x] = 'k'
    return make(d, RAMP, r=1, lo=-.32, post2=post2)
def head_open():
    """上あごを 上へ ふりあげ、口の 中（赤）が 見える 形"""
    def d(p):
        poly(p, [(38, 30), (58, 18), (54, 28), (53, 38), (56, 48), (44, 44), (38, 40)], '4')
        ellipse(p, 40, 30, 10.5, 9.5, '1')
        poly(p, [(36, 23), (46, 19), (55, 15), (62, 13), (64, 16), (60, 21), (44, 32), (36, 37)], '1')
    def post(s): dots(s, 'C', [(61, 15), (60, 15)]); line(s, 45, 31, 60, 20, 'C')
    def post2(g):
        for (x, y) in ((46, 32), (50, 29), (54, 26), (58, 23)):
            g[y][x] = 'w'; g[y + 1][x] = 'w'; g[y + 2][x] = 'k'
    return make(d, dict(RAMP, **{'4': 'RRR'}), lo=-.32, post=post, post2=post2)

# 目：ぶあつい まゆの こぶ＋白い 光＋金の 虹彩（明 Y・暗 O）＋たての ひとみ
EYE = ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwYYkYYk', '.kwYYOkOYk', '.kYOOOkOOk', '..kOOkkOk.', '...kkkkk..']
EYE_ALT = {
    'blink': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAAAAAAAk', '.kkkkkkkkk', '.kBBBBBBBk', '..kBBBBBk.', '...kkkkk..'],
    'hit':   ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kkkAAAAkk', '.kAAkkkkAk', '.kBBBBBkkk', '..kkkBBBk.', '...kkkkk..'],
    'atk0|atk1|atk2': ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kwwwYkYwk', '.kwYYYkYYk', '.kYYYYkYYk', '..kOOkkOk.', '...kkkkk..'],
    'ko':    ['k.........', 'kkk.......', '.kkkkk....', '..kkkkkkk.', '.kAkAAAkAk', '.kAAkAkAAk', '.kAkAAAkAk', '..kBBBBBk.', '...kkkkk..'],
}
# 目の こぶ（頭の 上に もりあがる）
def brow(): return make(lambda p: ellipse(p, 43, 25, 6.5, 4.5, '1'), RAMP, r=1)
FROST = ['..c...i..', 'i..ci.c..', '.cicwic.i', 'c.iwwwi.c', '.icwcic..', '..i.c..i.', '.c..i...c']
FROST2 = ['.i...c.', 'c.ici..', '.iwwi.c', 'c.ici..', '.c...i.']

def layers():
    return [
        dict(n='legF', g='legB', x=0, y=0, rows=leg(27, True)),
        dict(n='legR', g='legA', x=0, y=0, rows=leg(6, True)),
        dict(n='tail', g='tail', x=0, y=2, rows=tail(0), alt={'idle1|idle2|walk1|walk3': tail(1)}),
        *[dict(n='sh%d' % i, g='body', x=0, y=2, rows=shard(p)) for i, p in enumerate(SHARDS[:4])],
        dict(n='body', g='body', x=0, y=2, rows=body()),
        dict(n='legH', g='legB', x=0, y=0, rows=leg(10)),
        dict(n='jaw', g='jaw', x=0, y=2, rows=jaw(), not_='atk1'),
        dict(n='sh4', g='head', x=0, y=2, rows=shard(SHARDS[4])),
        dict(n='brow', g='head', x=0, y=2, rows=brow(), not_='atk1'),
        dict(n='head', g='head', x=0, y=2, rows=head(), alt={'atk1': head_open()}),
        dict(n='brow2', g='head', x=0, y=0, rows=brow(), only='atk1'),
        dict(n='jawO', g='jaw', x=0, y=2, rows=jaw(True), only='atk1'),
        dict(n='eye', g='head', x=38, y=20, rows=EYE, alt=EYE_ALT),
        dict(n='legFF', g='legA', x=0, y=0, rows=leg(30)),
        dict(n='frost', g='head', x=54, y=38, rows=FROST, only='atk2'),
        dict(n='frost0', g='head', x=56, y=26, rows=FROST2, only='atk0'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'head': (-1, 1), 'body': (0, 1)},
    'atk1': {'root': (2, 0), 'head': (0, -1), 'jaw': (0, 1)},
    'atk2': {'root': (3, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'jaw': 'head', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
