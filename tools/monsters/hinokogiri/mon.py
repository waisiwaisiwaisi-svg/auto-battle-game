# ヒノコギリ（ほのお・はがね × ノコギリザメ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

META = dict(id='hinokogiri', name='ヒノコギリ', types=['fire', 'steel'], base='ノコギリザメ', size='M')
PAL = {
    'k': '#101018', 'l': '#262a40',
    'S': '#e2e8f2', 'T': '#94a0b8', 'U': '#505a78',      # 鋼の からだ
    'N': '#3a3048', 'P': '#7a3a44',                      # 刃の 鉄（黒・焼けた 色）
    'Y': '#ffe45c', 'O': '#ff7a1e', 'R': '#c02a22',      # 赤熱
    'w': '#ffffff',
}
LIGHT = set('SYw')
KEEP_BLACK = set('wYO')

# ---------- 下書きの 道具（形の あたり → 左上光の 陰影 → 輪郭）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def ink(p):
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
            elif p[y][x] != '.': g[y][x] = p[y][x]
    return g
def shade(p, ramps, r=2, hi=.3, lo=-.28):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1): n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(64):
        for x in range(64):
            c = p[y][x]
            if c not in ramps: continue
            h, md, d = ramps[c]
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5
            out[y][x] = h if v > hi else d if v < lo else md
            if at(p, x, y - 1) == '.' or at(p, x - 1, y) == '.': out[y][x] = h
            if at(p, x, y + 1) == '.' or at(p, x + 1, y) == '.': out[y][x] = d
    return out
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if 0 <= x < 64 and 0 <= y < 64 and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: p[y][x] = ch
def recol(g, mp): return [[mp.get(c, c) for c in r] for r in g]
def put(g, rows, x0, y0): stamp(g, rows, x0, y0); return g

RAMP = {'1': 'STU', '2': 'TUN'}
DARK = {'S': 'T', 'T': 'U', 'U': 'N'}

# ---------- からだ：魚雷形の 鋼の 胴。板の 合わせ目と びょう ----------
def body():
    p = G()
    poly(p, [(11, 36), (16, 31), (24, 28), (32, 28), (38, 30), (43, 33), (45, 36), (43, 39), (37, 42), (27, 44), (17, 42), (12, 39)], '1')
    s = shade(p, RAMP, r=3, hi=.2, lo=-.2)
    # 腹がわは 白っぽい 板
    for y in range(64):
        for x in range(64):
            if s[y][x] in 'TU' and y >= 40 and at(s, x, y + 1) != '.' and x < 40: s[y][x] = 'T'
    # 板の 合わせ目（縦の すじ）＋ びょう
    for x0 in (19, 27):
        for y in range(64):
            if s[y][x0] in 'STU' and at(s, x0, y - 1) != '.' and at(s, x0, y + 1) != '.': s[y][x0] = 'U' if s[y][x0] != 'U' else 'N'
        for y in range(31, 42, 3):
            if s[y][x0 + 1] in 'STU': s[y][x0 + 1] = 'S'
    # えら：炉の ように 光る 3本の すじ（ほのお）
    for i, x in enumerate((33, 35, 37)):
        for y in range(34 - (i == 1), 40):
            s[y][x] = 'O'
        s[36][x] = 'Y'; s[37][x] = 'Y'
        s[34 - (i == 1)][x + 1] = 'N'
    # 口（あごの 下に 小さな 牙）
    line(s, 38, 41, 43, 39, 'k')
    dots(s, 'w', [(40, 41), (42, 40)])
    return rows_of(ink(s))

def gill_hot(rows):
    return [r.replace('O', 'Y') for r in rows]

def tail(ph=0):
    p = G()
    if ph == 0:
        poly(p, [(14, 34), (10, 28), (6, 21), (9, 22), (14, 28), (18, 32)], '1')
        poly(p, [(14, 38), (10, 42), (7, 46), (11, 45), (17, 40)], '1')
    else:
        poly(p, [(14, 34), (9, 29), (5, 23), (8, 23), (14, 29), (18, 32)], '1')
        poly(p, [(14, 38), (9, 41), (6, 44), (10, 44), (17, 40)], '1')
    s = shade(p, RAMP, r=1)
    return rows_of(ink(s))

def fins():
    p = G()
    poly(p, [(23, 29), (21, 22), (18, 17), (22, 18), (27, 23), (32, 29)], '1')    # 背びれ（刃の ように 後ろへ）
    poly(p, [(14, 32), (12, 29), (15, 29), (18, 31)], '1')                       # 小さな 第二背びれ
    s = shade(p, RAMP, r=1)
    # ひれの ふちに 焼けた 刃の 色
    dots(s, 'P', [(19, 18), (20, 19), (21, 20)])
    return rows_of(ink(s))
def pec(far=False):
    p = G()
    if far: poly(p, [(31, 42), (29, 47), (31, 47), (35, 42)], '1')
    else: poly(p, [(28, 42), (25, 48), (22, 51), (26, 51), (34, 43)], '1')
    s = shade(p, RAMP, r=1)
    if far: s = recol(s, DARK)
    return rows_of(ink(s))

# ---------- のこぎりの 吻（見せ所）：長い 鉄の 刃、両がわに 赤熱した 歯 ----------
def saw(hot=False):
    p = G()
    poly(p, [(41, 34), (62, 36), (63, 37), (62, 38), (41, 40)], '2')
    s = shade(p, {'2': 'TUN'}, r=1)
    for x in range(41, 64):
        if s[37][x] in 'TUN': s[37][x] = 'P' if x < 50 else 'R'
    for x in range(52, 63):
        if s[37][x] in 'PR': s[37][x] = 'O' if hot else 'R'
    g = ink(s)
    # 歯：上下に 外向きの 三角（手で 1本ずつ）
    for i, x in enumerate((44, 47, 50, 53, 56, 59)):
        yt = 34 + (x - 41) * 2 // 21 - 1
        yb = 40 - (x - 41) * 2 // 21 + 1
        c1, c2 = ('Y', 'O') if (hot or i >= 2) else ('O', 'R')
        g[yt][x] = c2; g[yt][x + 1] = c1; g[yt - 1][x + 1] = c1
        g[yt - 1][x] = 'k'; g[yt - 2][x + 1] = 'k'; g[yt - 1][x + 2] = 'k'; g[yt][x + 2] = 'k' if g[yt][x + 2] == '.' else g[yt][x + 2]
        g[yb][x] = c2; g[yb][x + 1] = c1; g[yb + 1][x + 1] = c1
        g[yb + 1][x] = 'k'; g[yb + 2][x + 1] = 'k'; g[yb + 1][x + 2] = 'k'; g[yb][x + 2] = 'k' if g[yb][x + 2] == '.' else g[yb][x + 2]
    return rows_of(g)

# するどい 目：まゆの ひさし＋たての ひとみ
EYE = ['kkkkk..', '.kUUUkk', '..kYYkY', '..kYkYk', '...kkk.']
EYE_ALT = {
    'blink': ['kkkkk..', '.kUUUkk', '..kkkkk', '..kTTTk', '...kkk.'],
    'atk0|atk1|atk2': ['kkkkk..', '.kUUUkk', '..kwYYk', '..kYYYk', '...kkk.'],
    'hit': ['kkkkk..', '.kUUUkk', '..kYkYk', '..kkYkk', '...kkk.'],
    'ko': ['kkkkk..', '.kUUUkk', '..kTkTk', '..kkTkk', '..kTkTk'],
}
SPARK = ['..Y...O.', 'O..Y.Y..', '.Y.wY..Y', 'O.YwwY..', '.Y.wY..Y', 'O..Y.Y..', '..Y...O.']
# ふりぬきの 斬撃（白い 弧）
SLASH = ['......wwS.', '....wwS...', '..wwS.....', '.wS.......', 'wS........', 'S.........']
SMOKE = ['.TT.', 'TSST', '.TT.']

def layers():
    B = body(); SAW = saw(); SAWH = saw(True)
    return [
        dict(n='pecF', g='body', x=0, y=0, rows=pec(True)),
        dict(n='tail', g='tail', x=0, y=0, rows=tail(0), alt={'idle1|idle2|walk1|walk2|atk0': tail(1)}),
        dict(n='fins', g='body', x=0, y=0, rows=fins()),
        dict(n='saw', g='head', x=0, y=0, rows=SAW, alt={'atk0|atk1|atk2': SAWH}),
        dict(n='body', g='body', x=0, y=0, rows=B, alt={'idle1|idle3|walk1|walk3|atk0|atk1': gill_hot(B)}),
        dict(n='pec', g='fin', x=0, y=0, rows=pec()),
        dict(n='eye', g='head', x=36, y=30, rows=EYE, alt=EYE_ALT),
        dict(n='spark', g='head', x=58, y=33, rows=SPARK, only='atk1'),
        dict(n='slash', g='head', x=53, y=26, rows=SLASH, only='atk2'),
        dict(n='smoke', g='root', x=36, y=26, rows=SMOKE, only='ko'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, 1), 'fin': (0, 0)},
    'idle2': {'root': (0, 1), 'fin': (0, 1)},
    'idle3': {'root': (0, 0), 'fin': (0, 1)},
    'blink': {},
    'walk0': {'tail': (0, -1), 'fin': (-1, 0)},
    'walk1': {'root': (0, -1), 'tail': (0, 0)},
    'walk2': {'tail': (0, 1), 'fin': (1, 0)},
    'walk3': {'root': (0, 1), 'tail': (0, 0)},
    'atk0': {'root': (-3, 1), 'head': (0, 0), 'tail': (-1, 0)},
    'atk1': {'root': (4, 0)},
    'atk2': {'root': (6, -1)},
    'hit': {'root': (-4, 0), 'head': (-1, 1), 'tail': (1, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'fin': 'body', 'tail': 'body', 'body': 'root'}
