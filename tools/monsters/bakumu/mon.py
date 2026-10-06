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
    p = G(); ellipse(p, 25, 43, 16, 10.5, '1')
    for y in range(64):
        for x in range(64):
            # 鞍：肩の うしろから 腰まで、腹の 線より 上
            if p[y][x] == '1' and 13 <= x + (y - 40) * .25 <= 31 and y <= 48: p[y][x] = '2'
    s = shade(p, RAMP, r=3)
    # 鞍の ふちの 毛（ぎざぎざ）を 手で
    dots(s, 'H', [(14, 48), (16, 47), (19, 48), (22, 47), (25, 48), (28, 47)])
    dots(s, 'D', [(31, 34), (32, 37), (32, 41), (33, 44)])
    return ink(s)
def leg(x0, far=False):
    p = G()
    poly(p, [(x0, 49), (x0 + 6, 49), (x0 + 6, 58), (x0, 58)], '1')
    s = shade(p, RAMP, r=1, tilt=.2)
    for x in range(x0, x0 + 7): s[58][x] = 'D'
    s[57][x0 + 1] = 'w'; s[57][x0 + 3] = 'w'; s[58][x0 + 1] = 'k'; s[58][x0 + 3] = 'k'
    if far:
        for y in range(64):
            for x in range(64):
                if s[y][x] in 'AB': s[y][x] = 'D' if s[y][x] == 'B' else 'B'
    g = ink(s)
    for x in range(x0, x0 + 7): g[59][x] = 'k'
    return g

# ---------- 頭：くさび形、耳は うしろへ とがる ----------
def head():
    p = G()
    ellipse(p, 43, 35, 8.5, 8, '1')
    poly(p, [(44, 27.5), (53, 31), (55, 35), (53, 40), (44, 43)], '1')   # 鼻すじ
    poly(p, [(36, 31), (37, 23), (41, 22), (43, 29)], '1')               # 耳（とがる）
    s = shade(p, RAMP, r=2)
    # 耳の 内がわ
    dots(s, 'Q', [(38, 25), (39, 25), (38, 26), (39, 26), (39, 27), (40, 27)])
    # ほおの しわ・口の 線
    dots(s, 'D', [(46, 40), (47, 40), (48, 40), (49, 39), (50, 39), (51, 39)])
    g = ink(s)
    dots(g, 'k', [(47, 41), (48, 41), (49, 40), (50, 40), (51, 40), (52, 40)])
    dots(g, 'w', [(50, 41), (52, 41)])    # きば
    return g

# ---------- 鼻＝煙管：皮の 鼻 → 真鍮の 輪 → 細い 羅宇（らお）→ 雁首 ----------
NOSE_PATH = [(52, 36), (56, 38), (59, 41), (60, 45)]
def nose(lift=0):
    p = G()
    tube(p, [(51, 35), (55, 37.5)], [3.2, 2.6], '1')
    tube(p, [(55, 37.5), (58.5, 40.5 - lift), (60.5, 45 - lift)], [2.2, 1.8, 1.8], '1')
    s = shade(p, RAMP, r=1, tilt=.3)
    # 鼻の しわ（輪）
    for (x, y) in ((53, 35), (53, 36), (53, 37), (56, 37), (56, 38), (56, 39)):
        if s[y][x] in 'ABD': s[y][x] = 'D'
    g = ink(s)
    # 真鍮の 吸い口の 輪（手で）
    stamp(g, ['kUk', 'UVW', 'VWk'], 57, 39 - lift)
    stamp(g, BOWL, 57, 44 - lift)
    return g
# 雁首：上むきに ひらいた 金の 火皿。中で 夢の 火が くすぶる
BOWL = [
    '.kkkkkk',
    'kPQQQPk',
    'kUUUVWk',
    '.kUVWk.',
    '..kWk..',
    '...k...',
]
BOWL_HOT = [
    '.kkkkkk',
    'kPPPPPk',
    'kUUUVWk',
    '.kUVWk.',
    '..kWk..',
    '...k...',
]

# ---------- 夢の 煙（くるくる 立ちのぼる）----------
SMOKE = [
    [
        '...PPQ......',
        '..PQ..Q.....',
        '..Q...Q.....',
        '...QQQ......',
        '.....PQ.....',
        '......Q.....',
        '.....PQ.....',
        '.....Q......',
    ],
    [
        '....PPQ.....',
        '...PQ..Q....',
        '...Q...Q....',
        '....QQQ.....',
        '.....PQ.....',
        '.....Q......',
        '.....PQ.....',
        '......Q.....',
    ],
    [
        '..PPQ.......',
        '.PQ..Q......',
        '.Q..PQ......',
        '..QQ........',
        '....PQ......',
        '.....Q......',
        '......Q.....',
        '.....PQ.....',
    ],
]
# 攻撃：夢の 煙の かたまり（中に 目玉）
BLAST = [
    '.......PPPP.......',
    '....PPPQQQQPP.....',
    '..PPQQQQQQQQQPP...',
    '.PQQQQkkkkkQQQQP..',
    'PQQQQkRRRRwkQQQQP.',
    'PQQQkRRkkRRRkQQQQP',
    'PQQQQkRRRRRkQQQQP.',
    '.PQQQQkkkkkQQQQP..',
    '..PPQQQQQQQQQPP...',
    '....PPPQQQPP......',
    '.......PP.........',
]
BLAST2 = [
    '...P..PP....P.',
    '.PQ..PQQP..PQ.',
    'PQ..PQ..QP..Q.',
    '.Q..Q....Q.PQ.',
    '..PQ...PQ...Q.',
    '....P....QP...',
]
EYE = ['kk.....', '.kkkk..', '..RRkRk', '...kkk.']
EYE_ALT = {
    'blink': ['kk.....', '.kkkk..', '..kkkkk', '.......'],
    'atk0|atk1|atk2': ['kk.....', '.kkkk..', '..RRRRk', '...kkk.'],
    'hit': ['.......', '.kk.kk.', '...k...', '.kk.kk.'],
    'ko': ['.......', '.k.k...', '..k....', '.k.k...'],
}

def layers():
    N0 = rows_of(nose()); N1 = rows_of(nose(1))
    return [
        dict(n='legFH', g='legB', x=0, y=0, rows=rows_of(leg(11, True))),
        dict(n='legFF', g='legA', x=0, y=0, rows=rows_of(leg(33, True))),
        dict(n='body', g='body', x=0, y=0, rows=rows_of(body())),
        dict(n='legH', g='legA', x=0, y=0, rows=rows_of(leg(14))),
        dict(n='legF', g='legB', x=0, y=0, rows=rows_of(leg(29))),
        dict(n='smoke', g='nose', x=52, y=31, rows=SMOKE[0], alt={'idle1|walk1|walk2': SMOKE[1], 'idle2|idle3|walk3|blink': SMOKE[2]}, not_='atk1|atk2|hit|ko'),
        dict(n='nose', g='nose', x=0, y=0, rows=N0, alt={'atk0|atk1|atk2': N1}),
        dict(n='head', g='head', x=0, y=0, rows=rows_of(head())),
        dict(n='eye', g='head', x=42, y=29, rows=EYE, alt=EYE_ALT),
        dict(n='blast', g='nose', x=58, y=30, rows=BLAST, only='atk1'),
        dict(n='blast2', g='nose', x=60, y=28, rows=BLAST2, only='atk2'),
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
