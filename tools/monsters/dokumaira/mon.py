# ドクマイラ（どく・ドラゴン × キマイラ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='dokumaira', name='ドクマイラ', types=['poison', 'dragon'], base='キマイラ', size='L')
PAL = {
    'k': '#101018', 'l': '#3c1a40',
    'F': '#ecc472', 'G': '#b8823e', 'H': '#6e442c',      # 獅子の 毛（明・中・暗）
    'M': '#c88ae6', 'N': '#8648b0', 'O': '#4a2268',      # 竜の うろこ・たてがみ（明・中・暗）
    'V': '#dcff5c', 'U': '#78c832', 'T': '#2c7438',      # 毒（明・中・暗）／翼の 膜
    'w': '#ffffff', 'r': '#b02848', 'd': '#4c0c24',      # きば・口の 中（明・暗）
}
LIGHT = set('FMVw')
KEEP_BLACK = set('wVUrd')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 胴：分厚い 胸と 肩 → くびれた 腹 → 丸い もも（あたりは 多角形、筋肉の みぞは 手で）----
def torso():
    W, H = 42, 27; g = grid(W, H)
    poly(g, [(1, 9), (5, 6), (12, 6), (19, 7), (25, 3), (31, 0), (37, 1), (41, 6), (42, 14), (40, 21), (36, 26), (29, 26),
             (25, 22), (20, 19), (14, 19), (10, 23), (4, 23), (0, 18)], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 4 or rt <= 2: c = 'H'
            elif dn == 5 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 3): c = 'F'
            out[y][x] = c
    # 背骨に そって 竜の うろこ（腰から 肩へ だんだん 大きく）
    for i, x in enumerate(range(4, 26, 3)):
        y = next(j for j in range(H) if g[j][x] != '.')
        out[y][x] = 'M'; out[y][x + 1] = 'N'; out[y + 1][x] = 'N'; out[y + 1][x + 1] = 'O'
        if i >= 3: out[y - 1 if y > 0 else y][x] = out[y][x]
    # 肩甲骨の もりあがり（弧）と ひじ
    for (x, y) in ((27, 4), (26, 5), (25, 6), (25, 7), (25, 8), (25, 9), (26, 10), (26, 11), (27, 12), (28, 13), (29, 14)):
        out[y][x] = 'l'; out[y][x + 1] = 'F' if out[y][x + 1] in 'G' else out[y][x + 1]
    for (x, y) in ((30, 15), (31, 16), (32, 17), (32, 18)): out[y][x] = 'H'
    # 胸の 筋肉（前の 丸み）
    for (x, y) in ((37, 9), (36, 10), (36, 11), (36, 12), (37, 13), (38, 14)): out[y][x] = 'l'
    for (x, y) in ((38, 7), (39, 8), (38, 8), (37, 10)): out[y][x] = 'F'
    # あばら
    for (x, y) in ((19, 11), (20, 12), (22, 11), (23, 12), (21, 14), (22, 15)): out[y][x] = 'l'
    # ももの 丸み
    for (x, y) in ((10, 9), (9, 10), (8, 11), (8, 12), (8, 13), (9, 14), (10, 15), (11, 16), (12, 16)):
        out[y][x] = 'l'
    for (x, y) in ((10, 10), (9, 11), (9, 12)): out[y][x] = 'F'
    # 腹の 毛ふさ（下に ぎざぎざ）
    for x in range(15, 25, 3): out[H - 8 + (x - 15) // 4][x] = 'l'
    return outline(rows_of(out))

# ---- 竜の 翼（骨の あたりは 線、膜の 陰影は 骨からの 距離で）----
def wing(spread=False):
    W, H = 34, 34; g = grid(W, H)
    if not spread:
        wrist, tips, scal = (24, 4), [(3, 4), (1, 14), (6, 24)], [(10, 11), (9, 20), (16, 26)]
    else:
        wrist, tips, scal = (21, 0), [(0, 0), (0, 9), (2, 19)], [(9, 6), (7, 15), (12, 22)]
    root = (29, 32)
    pts = [root, (30, 20), wrist, tips[0], scal[0], tips[1], scal[1], tips[2], scal[2], (24, 32)]
    poly(g, pts, 'T')
    out = [r[:] for r in g]
    bones = grid(W, H)
    for t in tips: line(bones, wrist[0], wrist[1], t[0], t[1], 'N')
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'T': continue
            if any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (1, 2)): out[y][x] = 'U'
            elif any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (3,)) and (x + y) % 2: out[y][x] = 'U'
            if run(g, x, y, 0, 1) <= 1 and out[y][x] == 'T': out[y][x] = 'l'
    for t in tips: line(out, wrist[0], wrist[1], t[0], t[1], 'N')
    line(out, root[0], root[1], wrist[0], wrist[1], 'N'); line(out, root[0] + 1, root[1], wrist[0] + 1, wrist[1], 'O')
    line(out, root[0] - 1, root[1] - 1, wrist[0] - 1, wrist[1], 'M')
    for t in tips: out[t[1]][t[0]] = 'V'
    cx, cy = wrist   # 手首の かぎ爪
    out[cy][cx] = 'M'
    if cy >= 1: out[cy - 1][cx + 1] = 'w'
    if cy >= 2: out[cy - 2][cx + 2] = 'w'
    return outline(rows_of(out))

# ---- たてがみ：竜の うろこが とげ状に 逆立つ（とげの あたりは 三角、先は 毒）----
def mane():
    W, H = 22, 38; g = grid(W, H)
    ellipse(g, 13, 19, 8, 15.5, '#')
    spikes = [((9, 6), (14, 5), (8, 0)), ((14, 5), (18, 6), (16, 0)), ((6, 9), (9, 6), (2, 3)), ((5, 12), (6, 8), (0, 9)),
              ((5, 17), (5, 12), (0, 15)), ((5, 22), (5, 17), (1, 21)), ((6, 27), (5, 22), (1, 28)), ((8, 31), (6, 26), (3, 34)),
              ((12, 33), (8, 30), (8, 37)), ((17, 32), (12, 33), (15, 37))]
    for a, b, t in spikes: poly(g, [a, b, t], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            lf, rt, up = run(g, x, y, -1, 0), run(g, x, y, 1, 0), run(g, x, y, 0, -1)
            c = 'N'
            if lf <= 2 or up <= 1: c = 'M'
            if rt <= 4: c = 'O'
            out[y][x] = c
    for a, b, t in spikes:
        out[t[1]][t[0]] = 'V'
        mx, my = (t[0] * 2 + a[0] + b[0]) // 4, (t[1] * 2 + a[1] + b[1]) // 4
        if out[my][mx] != '.': out[my][mx] = 'U'
    # うろこの すじ（手で）
    for (x, y) in ((10, 10), (11, 11), (9, 15), (10, 16), (9, 21), (10, 22), (10, 27), (11, 28), (13, 12), (13, 24)):
        if out[y][x] in 'NM': out[y][x] = 'O'
    return outline(rows_of(out))

# ---- 獅子の 顔（横顔）：重い まゆの ひさし・つり上がった たての ひとみ・むき出しの きば ----
HEAD = [
    '.......kkkkkk...........',
    '.....kkFFFFFFkk.........',
    '....kFFFFGGGGFFkk.......',
    '...kFFGGGGGGGGGFFk......',
    '..kFGGGGGGGGGGGGGFkk....',
    '..kFGGGGGGGGkkkGGGGFkk..',
    '.kFGGGGGGGkkHHHkkkGGGFk.',
    '.kGGGGGGGkHHHHHHHHkkFGFk',
    '.kGGGGGGkkkkkkkHHHHkFGGk',
    '.kGGGGGGGGGGGGGkkkkGGGkk',
    '.kGGGGGGGHGGGGGGGGGGGkkk',
    '.kHGGGGGGGHGGGHGGHGGGHkk',
    '.kHGGGGGGHGGGHGGHGGGGGHk',
    '.kHHGGGGGkkkkkkkkkkkkkkk',
    '.kHHGGGGkwddddddwddddwk.',
    '.kHHGGGGkwwddrrrrrrdwk..',
    '..kHHGGGGkdrrrrrrrwwk...',
    '..kHHGGGGGkwkkkwkkkk....',
    '...kHHGGGGGGGGGGGHk.....',
    '....kkHHHHHHHHHHHk......',
    '......kkkkkkkkkkk.......',
]
HEAD_OPEN = HEAD[:13] + [
    '.kHHGGGGkkkkkkkkkkkkkkkk',
    '.kHHGGGkwddddddwddddwk..',
    '.kHHGGGkwddrrrrrrrrdk...',
    '..kHHGGkdrrrrrrrrrrrk...',
    '..kHHGGkdrrrrrrrrrrk....',
    '..kHHGGGkwddrrrrrwwk....',
    '...kHHGGGkwkkkkwkkk.....',
    '....kHHGGGGGGGGGHk......',
    '.....kkHHHHHHHHHk.......',
    '.......kkkkkkkkk........',
]
# 目：ひさしの 下で 光る つり目（たての ひとみ）
EYE = ['kVVkVk']
EYE_ALT = {'blink': ['kHHHHk'], 'hit': ['kkVkkk'], 'atk0|atk1|atk2': ['wVVkVV'], 'ko': ['kVkVkk']}
HORN = ['kk......', 'kMkk....', '.kMNkk..', '.kMNNNkk', '..kMNNOk', '...kkkk.']
# 毒蛇の しっぽ（S字に 立ち上がり、前を にらむ）
SNAKE = [
    '..kkkkkk......',
    '.kMMMMNNkk....',
    'kMNNNNNNNNkk..',
    'kMNNkkkNNNNNkk',
    'kNNNkVVkNNNNOk',
    'kNNNNkkNNNNNOk',
    'kONNNNNNkkkkkk',
    '.kONNNkwkkwk..',
    '..kONNNkk.k...',
    '..kUNNNOk.....',
    '..kVUNNOk.....',
    '...kUNNOk.....',
    '...kVUNNOk....',
    '....kUNNOk....',
    '....kVUNNOk...',
    '.....kUNNOOk..',
    '......kUNNOOk.',
    '.......kUNNOk.',
    '........kNNOk.',
    '........kkkk..',
]
SNAKE_OPEN = [
    '..kkkkkk......',
    '.kMMMMNNkk....',
    'kMNNNNNNNNkkk.',
    'kMNNkkkNNNNNNk',
    'kNNNkwVkNkkkkk',
    'kNNNNkkNkwdddw',
    'kONNNNNkrrrrk.',
    '.kONNNkwkwkk..',
    '..kONNNkk.....',
] + SNAKE[9:]
LEG_F = [
    '.kkkkkkkk..',
    'kFFGGGGGHk.',
    'kFGGGGGGHHk',
    'kFGGGGGGHHk',
    '.kFGGGGGHHk',
    '.kFGGGGHHk.',
    '..kFGGGHHk.',
    '..kFGGGHk..',
    '..kFGGGHk..',
    '..kFGGGHHk.',
    '.kFGGGGGHk.',
    '.kFGGGGGHHk',
    'kFGGGGGGHHHk',
    'kGGGlGGlGHHk',
    'kHHHlHHlHHHk',
    '.kwkkwkkwkk.',
]
LEG_H = [
    'kkkkkkkkkk.',
    'kFGGGGGGHHk',
    'kFGGGGGGHHk',
    '.kFGGGGGHk.',
    '..kFGGGHk..',
    '...kFGGHk..',
    '...kFGGHk..',
    '...kFGGHk..',
    '..kFGGGHk..',
    '..kFGGGHHk.',
    '.kFGGGGGHk.',
    '.kGGGlGGlHk',
    '.kHHHlHHlHk',
    '..kwkkwkkw.',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'M': 'N', 'N': 'O', 'O': 'l', 'V': 'U', 'U': 'T'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 毒の ブレス（もくもく）
BREATH1 = [
    '....kkk.......',
    '..kkVVUkk.kk..',
    '.kVVUUUTTkVUk.',
    'kVUUUTTTTkUTk.',
    'kUUTTTTTkkkk..',
    '.kTTTTkk......',
    '..kkkk........',
]
BREATH2 = [
    '........kkkk...........',
    '...kkk.kVVUUkk...kkk...',
    '..kVVUkVUUUTTTk.kVVUk..',
    '.kVUUUTUUTTTTTkkVUUTTk.',
    'kVUUUTTTTTTTTTTUUTTTTk.',
    'kUUTTTTTTkTTTTTTTTTTkVk',
    '.kTTTTTkk.kTTTTTTkkk.k.',
    '..kkkkk....kkkkkk......',
]
DRIP = ['kVk', 'kUk', '.k.']
TORSO = torso(); MANE = mane()

def layers():
    return [
        dict(n='wingF', g='wingF', x=18, y=-2, rows=dark(wing()), alt={'atk0|atk1|atk2': dark(wing(True))}),
        dict(n='snake', g='tail', x=0, y=16, rows=SNAKE, alt={'atk0|atk1|atk2': SNAKE_OPEN}),
        dict(n='legFF', g='legB', x=43, y=45, rows=dark(LEG_F)),
        dict(n='legHF', g='legA', x=13, y=46, rows=dark(LEG_H)),
        dict(n='torso', g='body', x=4, y=26, rows=TORSO),
        dict(n='legH', g='legB', x=6, y=46, rows=LEG_H),
        dict(n='legF', g='legA', x=35, y=44, rows=LEG_F),
        dict(n='wing', g='wing', x=8, y=-1, rows=wing(), alt={'atk0|atk1|atk2': wing(True)}),
        dict(n='mane', g='head', x=31, y=5, rows=MANE),
        dict(n='horn', g='head', x=42, y=8, rows=HORN),
        dict(n='head', g='head', x=40, y=11, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=50, y=19, rows=EYE, alt=EYE_ALT),
        dict(n='drip', g='drip', x=58, y=31, rows=DRIP, only='idle1|idle2|walk1|walk3'),
        dict(n='breath1', g='fx', x=62, y=24, rows=BREATH1, only='atk1'),
        dict(n='breath2', g='fx', x=58, y=21, rows=BREATH2, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0), 'wing': (0, -1), 'drip': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'wing': (0, 0), 'tail': (0, 1), 'drip': (0, 2)},
    'idle3': {'body': (0, 0), 'head': (0, 1), 'wing': (0, -1), 'tail': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1), 'wing': (0, -1), 'drip': (0, 0)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1), 'wing': (0, -1), 'drip': (0, 0)},
    'atk0': {'body': (-1, 2), 'head': (-2, 1), 'wing': (0, -2), 'tail': (-1, -1), 'legA': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (1, 0), 'wing': (0, -2), 'tail': (1, 0)},
    'atk2': {'root': (4, 0), 'head': (1, -1), 'wing': (0, 0)},
    'hit': {'root': (-3, 0), 'head': (-3, -2), 'wing': (-1, 2), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'wingF': 'wing', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'drip': 'head', 'fx': 'head'}
