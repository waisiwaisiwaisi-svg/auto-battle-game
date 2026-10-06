# バクム（エスパー・あく × バク）手打ち GBA風
# 見せ所：煙管（きせる）に なった 長い 鼻。先の 雁首（がんくび）から 夢の 煙
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

META = dict(id='bakumu', name='バクム', types=['psychic', 'dark'], base='バク', size='M')
PAL = {
    'k': '#100c18', 'l': '#2c1c40',
    'A': '#6c6290', 'B': '#3e365e', 'D': '#221c38',      # 黒い 皮（前と 後ろ）
    'E': '#ece4f4', 'F': '#b6a8d0', 'H': '#7a6c9e',      # 白い 鞍（せなかの 帯）
    'U': '#ffe596', 'V': '#d39a36', 'W': '#83521c',      # 煙管の 金具（真鍮）
    'P': '#ffb4ee', 'Q': '#b45ad8',                      # 夢の 煙
    'R': '#ff3c8c', 'w': '#ffffff',                      # 目の 光・きば
}
LIGHT = set('AEUPw')
KEEP_BLACK = set('wRP')

# ---------- 下書きの 道具 ----------
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
def shade(p, ramps, r=2, hi=.3, lo=-.25, tilt=.5):
    """光は 左上：ふちの むき＋上ほど 明るい（tilt）"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    ys = [y for y in range(64) if any(m[y])]; y0, y1 = ys[0], ys[-1]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for y in range(64):
        for x in range(64):
            c = p[y][x]
            if c in ramps:
                v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 + tilt * (.45 - (y - y0) / max(1, y1 - y0))
                h, md, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else md
    return out
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64: p[y][x] = ch
RAMP = {'1': 'ABD', '2': 'EFH', '3': 'UVW'}

# ---------- 胴：黒い 前後に 白い 鞍（マレーバクの 2色）----------
def body():
    p = G(); ellipse(p, 21, 44, 13, 10, '1')
    for y in range(64):
        for x in range(64):
            # 鞍：肩の うしろから 腰まで、腹の 線より 上
            if p[y][x] == '1' and 10 <= x + (y - 40) * .3 <= 25 and y <= 48: p[y][x] = '2'
    s = shade(p, RAMP, r=3, hi=.22, tilt=.8)
    dots(s, 'H', [(12, 48), (15, 48), (18, 48), (21, 48), (24, 47)])
    dots(s, 'F', [(13, 47), (16, 47), (19, 47), (22, 46)])
    return ink(s)
def leg(x0, far=False):
    p = G()
    poly(p, [(x0, 49), (x0 + 6, 49), (x0 + 6, 54), (x0 + 5.5, 58), (x0 + .5, 58), (x0, 55)], '1')
    s = shade(p, RAMP, r=1, tilt=.6)
    for x in range(x0, x0 + 6): s[57][x] = 'D' if s[57][x] != '.' else '.'
    s[57][x0 + 1] = 'w'; s[57][x0 + 3] = 'w'
    if far:
        for y in range(64):
            for x in range(64):
                if s[y][x] in 'AB': s[y][x] = 'D' if s[y][x] == 'B' else 'B'
    g = ink(s)
    for x in range(x0, x0 + 6): g[58][x] = 'k'
    return g

# ---------- 頭：くさび形、小さな 耳（ふちが 白い）----------
def head():
    p = G()
    poly(p, [(25, 34), (29, 28), (35, 26), (41, 28), (46, 31), (47, 35), (44, 39), (38, 42), (31, 43.5), (26, 41)], '1')
    poly(p, [(28, 29), (28.5, 23), (32, 23.5), (33, 27.5)], '1')
    s = shade(p, RAMP, r=2, tilt=.6)
    dots(s, 'E', [(29, 23), (30, 23), (31, 23), (29, 24)])
    dots(s, 'Q', [(30, 25), (30, 26), (31, 26)])
    dots(s, 'A', [(34, 27), (35, 27), (36, 27), (37, 27), (38, 28)])
    dots(s, 'D', [(31, 37), (32, 38), (33, 39), (39, 40), (40, 40)])
    g = ink(s)
    # 口：ななめに さけて きば
    dots(g, 'k', [(37, 39), (38, 39), (39, 38), (40, 38), (41, 38), (42, 37), (43, 37)])
    dots(g, 'w', [(39, 39), (41, 39)])
    return g

# ---------- 鼻＝煙管：真鍮の 吸い口 → 皮の 羅宇（らお）→ 真鍮の 雁首 ----------
def nose(lift=0):
    p = G()
    tube(p, [(45, 34), (51, 35.5), (56.5, 37.5 - lift)], [2.6, 2.0, 1.7], '1')
    s = shade(p, RAMP, r=1, tilt=.6)
    for x in (49, 52, 55):                      # 鼻の しわ＝竹の ふし
        for y in range(30, 42):
            if s[y][x] in 'ABD': s[y][x] = 'D' if s[y - 1][x] not in '.' else 'A'
    g = ink(s)
    stamp(g, ['kUk', 'UVk', 'UVk', 'VWk', 'kk.'], 45, 31)     # 吸い口の 金の 輪
    stamp(g, GAN if not lift else [r.replace('Q', 'P') for r in GAN], 55, 35 - lift)
    if lift: dots(g, 'P', [(57, 39 - lift), (59, 38 - lift)])                               # 雁首
    return g
# 雁首：細い 金の 首が 下へ のび、先で 上むきに 火皿が ひらく
GAN = [
    'kkk.....',
    'kUVk....',
    'kVUVk...',
    '.kVVWk..',
    '..kVWk..',
    '.kkkkkkk',
    'kUPPPQUk',
    'kUUUVVWk',
    '.kUVVWk.',
    '..kWWk..',
    '...kk...',
]

# ---------- 夢の 煙（くねって 立ちのぼる 帯、黒い 線は なし）----------
def smoke(ph=0):
    p = G(); o = (0, 1, -1)[ph]
    path = [(59, 41), (60 + o * .5, 37), (58, 33), (56 - o, 29), (56.5, 25), (59 + o, 22)]
    tube(p, path, [1, 1.4, 1.7, 1.8, 1.9, 2.0], 'P')
    ellipse(p, 56.5 + o, 19.5, 2.8, 2.2, 'P')
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.':
                # 光の 当たらない 右下だけ 濃い ふち、ところどころ 切れる
                edge = at(p, x + 1, y) == '.' or at(p, x, y + 1) == '.'
                g[y][x] = 'Q' if edge else 'P'
                if (y + ph) % 5 == 0 and x % 2 == 0: g[y][x] = '.'
    dots(g, 'Q', [(56 + o, 19), (57 + o, 19), (57 + o, 20)])
    return g
# 攻撃：夢の 煙の 大きな かたまり（中に にらむ 目玉）
def blast(big=True):
    p = grid(30, 24)
    for (cx, cy, r) in ((8, 13, 6), (15, 9, 7), (22, 12, 6.5), (15, 16, 6), (4, 15, 3)) if big else ((6, 12, 3), (14, 8, 3.5), (21, 13, 3), (12, 16, 2.5)):
        for y in range(24):
            for x in range(30):
                if (x + .5 - cx) ** 2 + ((y + .5 - cy) * 1.15) ** 2 <= r * r: p[y][x] = 'Q'
    for y in range(24):
        for x in range(30):
            if p[y][x] == 'Q' and (y == 0 or x == 0 or p[y - 1][x] == '.' or p[y][x - 1] == '.' or (y > 1 and p[y - 2][x] == '.')): p[y][x] = 'P'
    g = [r[:] for r in p]
    for y in range(24):
        for x in range(30):
            if p[y][x] == '.' and any(0 <= y + dy < 24 and 0 <= x + dx < 30 and p[y + dy][x + dx] != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
    if big:
        stamp(g, ['..kkkkk..', '.kRRRRwk.', 'kRRkkkRRk', '.kRRRRRk.', '..kkkkk..'], 10, 10)
    else:
        for y in range(24):
            for x in range(30):
                if g[y][x] == 'Q' and (x + y) % 2: g[y][x] = '.'
    return rows_of(g)
EYE = ['kk.....', '.kkkk..', '..RRkRk', '...kkk.']
EYE_ALT = {
    'blink': ['kk.....', '.kkkk..', '..kkkkk', '.......'],
    'atk0|atk1|atk2': ['kk.....', '.kkkk..', '..RRRRk', '...kkk.'],
    'hit': ['.......', '.kk.kk.', '...k...', '.kk.kk.'],
    'ko': ['.......', '.k.k...', '..k....', '.k.k...'],
}

def layers():
    N0 = rows_of(nose()); N1 = rows_of(nose(1)); SM = [rows_of(smoke(i)) for i in range(3)]
    return [
        dict(n='legFH', g='legB', x=0, y=0, rows=rows_of(leg(13, True))),
        dict(n='legFF', g='legA', x=0, y=0, rows=rows_of(leg(28, True))),
        dict(n='body', g='body', x=0, y=0, rows=rows_of(body())),
        dict(n='legH', g='legA', x=0, y=0, rows=rows_of(leg(9))),
        dict(n='legF', g='legB', x=0, y=0, rows=rows_of(leg(24))),
        dict(n='smoke', g='nose', x=0, y=0, rows=SM[0], alt={'idle1|walk1|walk2': SM[1], 'idle2|idle3|walk3|blink': SM[2]}, not_='atk1|atk2|hit|ko'),
        dict(n='nose', g='nose', x=0, y=0, rows=N0, alt={'atk0|atk1|atk2': N1}),
        dict(n='head', g='head', x=0, y=0, rows=rows_of(head())),
        dict(n='eye', g='head', x=33, y=28, rows=EYE, alt=EYE_ALT),
        dict(n='blast', g='nose', x=56, y=18, rows=blast(), only='atk1'),
        dict(n='blast2', g='nose', x=62, y=18, rows=blast(False), only='atk2'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'body': (0, 0), 'head': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-2, 1)},
    'atk1': {'root': (3, 0), 'head': (2, -1)},
    'atk2': {'root': (2, 0), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'nose': 'head', 'body': 'root', 'legA': 'root', 'legB': 'root'}
