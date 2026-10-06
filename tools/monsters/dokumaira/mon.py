# ドクマイラ（どく・ドラゴン × キマイラ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='dokumaira', name='ドクマイラ', types=['poison', 'dragon'], base='キマイラ', size='L')
PAL = {
    'k': '#101018', 'l': '#3c1a40',
    'F': '#ecc472', 'G': '#b8823e', 'H': '#6e442c',      # 獅子の 毛（明・中・暗）
    'M': '#c88ae6', 'N': '#8648b0', 'O': '#4a2268',      # 竜の うろこ・たてがみ（明・中・暗）
    'V': '#dcff5c', 'U': '#78c832', 'T': '#2c7438',      # 毒（明・中・暗）／翼の 膜
    'w': '#ffffff', 'r': '#b02848',
}
LIGHT = set('FMVw')
KEEP_BLACK = set('wVU')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 胴（あたり：だ円 → 3段の 陰影 → 筋肉の みぞ・背の うろこは 手で）----
def torso():
    W, H = 40, 24; g = grid(W, H)
    ellipse(g, 9, 11, 8.5, 9, '#'); ellipse(g, 19, 11, 14, 7.5, '#'); ellipse(g, 30, 11, 9.5, 11.5, '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 5: c = 'H'
            if dn == 6 and (x + y) % 2: c = 'H'
            if up <= 2 or lf <= 2: c = 'F'
            out[y][x] = c
    # 背骨に そって 竜の うろこ（毒色の ふち）
    for x in range(4, 30, 3):
        y = next(j for j in range(H) if g[j][x] != '.') + 1
        out[y][x] = 'N'; out[y][x + 1] = 'M'; out[y + 1][x] = 'O'; out[y + 1][x + 1] = 'N'
    # 肩と もものの 筋肉の みぞ・あばら
    for (x, y) in ((24, 6), (23, 7), (23, 8), (23, 9), (24, 10), (24, 11), (25, 12),
                   (9, 7), (8, 8), (8, 9), (8, 10), (9, 11), (9, 12), (10, 13),
                   (15, 11), (16, 12), (17, 11), (18, 12), (19, 11), (20, 12)):
        out[y][x] = 'l'
        if out[y][x - 1] == 'G': out[y][x - 1] = 'F'
    # 腹の 毛ふさ
    for x in range(12, 28, 3):
        out[H - 3][x] = 'k'; out[H - 4][x + 1] = 'H'
    return outline(rows_of(out))

# ---- 竜の 翼（骨は 線で あたり → 膜と 光の ふちは 手の ルールで）----
def wing(spread=False):
    W, H = 32, 32; g = grid(W, H)
    if not spread:
        wrist, tips, scal = (22, 4), [(2, 7), (3, 17), (9, 25)], [(9, 13), (11, 21), (18, 26)]
    else:
        wrist, tips, scal = (20, 1), [(0, 1), (0, 11), (4, 20)], [(8, 7), (8, 16), (14, 23)]
    root = (27, 30)
    pts = [root, (28, 20), wrist, tips[0], scal[0], tips[1], scal[1], tips[2], scal[2], (23, 30)]
    poly(g, pts, 'T')
    out = [r[:] for r in g]
    bones = grid(W, H)
    for t in tips: line(bones, wrist[0], wrist[1], t[0], t[1], 'N')
    line(bones, root[0], root[1], wrist[0], wrist[1], 'N')
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'T': continue
            near = any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (1, 2))
            if near: out[y][x] = 'U'
            elif any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (3,)) and (x + y) % 2: out[y][x] = 'U'
            if run(g, x, y, 0, -1) <= 1: out[y][x] = 'V'
            if run(g, x, y, 0, 1) <= 1 and out[y][x] == 'T': out[y][x] = 'l'
    for t in tips: line(out, wrist[0], wrist[1], t[0], t[1], 'N')
    line(out, root[0], root[1], wrist[0], wrist[1], 'N'); line(out, root[0] + 1, root[1], wrist[0] + 1, wrist[1], 'O')
    line(out, root[0] - 1, root[1] - 1, wrist[0] - 1, wrist[1], 'M')
    for t in tips: out[t[1]][t[0]] = 'O'
    # 手首の かぎ爪
    cx, cy = wrist
    out[cy - 1][cx] = 'w'; out[cy - 2][cx + 1] = 'w'; out[cy][cx] = 'M'
    return outline(rows_of(out))

MANE = [
    '.........kk.........',
    '....kk..kVk...kk....',
    '...kVk.kUMk..kVk....',
    '...kUMkkMNk.kUMk....',
    '....kMNkMNNkkMNk..kk',
    '.kk.kMNNMNNkMNNkkVk.',
    'kVkkMNNNNNNNNNNkUMk.',
    'kUMMNNNNNNNNNNNNMNk.',
    '.kMNNNNNNNNNNNNNNOk.',
    '..kMNNNNNNNNNNNNOOk.',
    'kkMNNNNNNNNNNNNNOk..',
    'kVUMNNNNNNNNNNNOOk..',
    '.kkMNNNNNNNNNNNOk...',
    '..kMNNNNNNNNNNOOk...',
    'kkMNNNNNNNNNNOOk....',
    'kVUMNNNNNNNNNOOk....',
    '.kkMNNNNNNNNNOOk....',
    '..kMNNNNNNNNOOk.....',
    'kkMNNNNNNNNNOOk.....',
    'kVUNNNNNNNNNOOk.....',
    '.kkNNNNNNNNNOOOk....',
    '..kNNNNNNNNNNOOk....',
    '.kNNNNNNNNNNNOOOk...',
    'kVkNNNNNNNNNNNOOOk..',
    '.kkNNNNNNNNNNNNOOOk.',
    '..kONNNNNNNNNNNOOOk.',
    '..kkONNNNNNNNNNOOk..',
    '.kVkkONNNkONNNOOk...',
    '..kk.kOOkkkONOOkk...',
    '......kVk..kOOkVk...',
    '.......k...kVk.k....',
    '............k.......',
]
def shade_mane(rows):
    g = [list(r) for r in rows]
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != 'N': continue
            lf = run(rows, x, y, -1, 0); rt = run(rows, x, y, 1, 0); up = run(rows, x, y, 0, -1)
            if lf <= 2 or up <= 1: g[y][x] = 'M'
            elif rt <= 3: g[y][x] = 'O'
    for (x, y) in ((5, 9), (6, 10), (7, 11), (4, 14), (5, 15), (6, 16), (4, 19), (5, 20), (6, 21), (7, 22), (8, 8), (9, 9), (10, 10), (11, 6), (12, 7)):
        if g[y][x] in 'NM': g[y][x] = 'O'
    return [''.join(r) for r in g]
MANE = shade_mane(MANE)
HORN = ['kk....', 'kMkk..', '.kMNkk', '.kMNNk', '..kNOk', '...kk.']
HEAD = [
    '.....kkkkkkk.........',
    '...kkFFFFFFGkk.......',
    '..kFFFFGGGGGGGk......',
    '.kFFGGGGGGGGGGGkk....',
    '.kFGGGGGGGGGGGGGGk...',
    'kFGGGGGkkkkkGGGGGGk..',
    'kFGGGGGHHHHHkkkkGGGk.',
    'kFGGGGGGGGGGGGGGkFGkk',
    'kGGGGGGGGGGGGGGGGFFHk',
    'kGGGGGGGGGGGGGGGGkkkk',
    'kHGGGGGGGGGGGGGGGFGk.',
    'kHGGGGGGGGkkkkkkkkkk.',
    'kHHGGGGkkkwHHHHwkwk..',
    '.kHHGGGGGGkGGGGkk....',
    'kHkHHGGGGGGGGGHk.....',
    '.kkHHHHHHHHHHHk......',
    '....kkkkkkkkkk.......',
]
HEAD_OPEN = HEAD[:9] + [
    'kGGGGGGGGGGGGGGGGkkkk',
    'kHGGGGGGGGGGGGGGGFGk.',
    'kHGGGGGGGkwkkkkwkkkkk',
    'kHHGGGGkrrrrrrrrrr...',
    '.kHHGGGkrrrrrrrrrrk..',
    'kHkHHGGGkrrrrrrrwk...',
    '.kkHHGGGGkwrrrwkkk...',
    '...kHHGGGGGkkkGHk....',
    '....kHHHHHHHHHHk.....',
    '.....kkkkkkkkkk......',
]
EYE = ['kVVkVk', '.kVkk']
EYE_ALT = {'blink': ['kkkkkk', '.GGG'], 'hit': ['kGkGkk', '.kGk'], 'atk0|atk1|atk2': ['kwVkVk', '.kVVk'], 'ko': ['kGkGkk', '.GkGk']}
SNAKE = [
    '..kkkkk.......',
    '.kMMMNNkk.....',
    'kMNNNNNNNkk...',
    'kMNkkkNNNNNkk.',
    'kNNNkVVkNNNNNk',
    'kNNNNkkNNNNkkk',
    'kONNNNNkkkkk..',
    '.kONNNkwk.wk..',
    '..kONNNkkkkk..',
    '..kUNNOk......',
    '..kVUNOk......',
    '..kUNNOk......',
    '..kVUNNOk.....',
    '...kUNNOk.....',
    '...kVUNNOk....',
    '....kUNNOOk...',
    '.....kUNNOOk..',
    '......kUNNOOk.',
    '.......kUNNOk.',
    '........kNNOk.',
    '........kkkk..',
]
SNAKE_OPEN = [
    '..kkkkk.......',
    '.kMMMNNkk.....',
    'kMNNNNNNNkkk..',
    'kMNkkkNNNNNNkk',
    'kNNNkwVkNkkkkk',
    'kNNNNkkNkwrrw.',
    'kONNNNNkrrrrk.',
    '.kONNNkwkkwk..',
    '..kONNNkkkk...',
] + SNAKE[9:]
LEG_F = [
    '.kkkkkkk.', 'kFFGGGGHk', 'kFGGGGGHk', 'kFGGGGGHHk', '.kFGGGGHHk', '.kFGGGGHk.', '..kGGGGHk.',
    '..kFGGGHk.', '..kFGGGHk.', '..kGGGGHk.', '.kGGGGGHHk', 'kFGGGGGHHHk', 'kGGGGGHHHHk', 'kHHHHHHHHHk', '.kwkwkwkkk.',
]
LEG_H = [
    '.kkkkkkkk.', 'kFFGGGGGHk', 'kFGGGGGGHk', '.kGGGGGGHk', '..kGGGGHk.', '...kGGGHk.', '...kGGHk..',
    '...kFGHk..', '..kFGGHk..', '..kGGGHk..', '.kGGGGHHk.', '.kFGGGHHHk', '.kGGGHHHHk', '.kHHHHHHHk', '..kwkwkwk.',
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
TORSO = torso()

def layers():
    return [
        dict(n='wingF', g='wingF', x=14, y=0, rows=dark(wing()), alt={'atk0|atk1|atk2': dark(wing(True))}),
        dict(n='legFF', g='legB', x=45, y=45, rows=dark(LEG_F)),
        dict(n='legHF', g='legA', x=16, y=45, rows=dark(LEG_H)),
        dict(n='snake', g='tail', x=0, y=12, rows=SNAKE, alt={'atk0|atk1|atk2': SNAKE_OPEN}),
        dict(n='torso', g='body', x=7, y=25, rows=TORSO),
        dict(n='legH', g='legB', x=9, y=46, rows=LEG_H),
        dict(n='legF', g='legA', x=38, y=46, rows=LEG_F),
        dict(n='wing', g='wing', x=6, y=-2, rows=wing(), alt={'atk0|atk1|atk2': wing(True)}),
        dict(n='mane', g='head', x=33, y=9, rows=MANE),
        dict(n='horn', g='head', x=42, y=13, rows=HORN),
        dict(n='head', g='head', x=42, y=19, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=51, y=26, rows=EYE, alt=EYE_ALT),
        dict(n='drip', g='drip', x=57, y=31, rows=DRIP, only='idle1|idle2|walk1|walk3'),
        dict(n='breath1', g='fx', x=59, y=27, rows=BREATH1, only='atk1'),
        dict(n='breath2', g='fx', x=52, y=24, rows=BREATH2, only='atk2'),
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
