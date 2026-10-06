# 手打ち ドラゴン（64x64・8bit風）。パーツごとに 1ドットずつ 打った 文字マップ
PAL = {
    'k': '#1a1028',
    'A': '#c8f070', 'B': '#7fd34e', 'C': '#45a845', 'D': '#2a7a4a', 'E': '#1c4f48',
    'a': '#fff4c8', 'b': '#f4cf80', 'd': '#c8904e',
    'r': '#ff9a7a', 's': '#e0585a', 't': '#9a2f52', 'u': '#5a1c44',
    'H': '#fff4dc', 'I': '#dcc49a', 'J': '#9a8068',
    'w': '#ffffff', 'y': '#ffd84a', 'Y': '#e8962a', 'p': '#1a1028',
    'm': '#5a1028', 'n': '#ff6a7a',
    'F': '#fff6c0', 'G': '#ffd23f', 'K': '#ff8a1f', 'L': '#d8341a',
}

HEAD = [
    '.........kkkkk',
    '.......kkAAABBkk',
    '.....kkAAABBBBBBk',
    '....kAABBBBBBBBBCk',
    '...kABBBBBBBBBBBCCkk',
    '..kABBBBBBBBBBBCCCCCkkkk',
    '..kBBBBBBBBkkkkkkkCCBBBBkk',
    '.kABBBBBBBkEEEEEEkCBBBBBBk',
    '.kBBBBBBBBk......kCCBBBBCCk',
    '.kBBBBBBBBk......kCCCCCCkCk',
    '.kBBBBBBBBk......kCCCCCCCCCk',
    '.kCBBBBBBBk......kCCCCCCCCDk',
    '.kCCBBBBBBBkkkkkkCCCCCCCCDDk',
    '.kCCCBBBBBBCCCCCCCCCCCCCDDk',
    '..kDCCCBBBCCCCCCCDDDDDDDDk',
    '..kDDCCCCCCCDDDkkkkkkkkkk',
    '...kDDDCCCDDDk',
    '....kEDDDDDDEk',
    '.....kkEEEEkk',
    '.......kkkk',
]
EYE = ['wwyppy', 'wyyppy', 'yyyppY', 'YYYppY']
EYE_ALT = {
    'blink': ['DDDDDD', 'CCCCCC', 'kkkkkk', 'DDDDDD'],
    'hit': ['kDDDDk', 'DkkDkD', 'DDDkDD', 'DDDDDD'],
    'atk0|atk1|atk2': ['kkwyyp', 'wyyppy', 'yyyppY', 'YYYppY'],
    'ko': ['kDDDDk', 'DkDDkD', 'DDkkDD', 'DkDDkD'],
}
FIN = ['..kk', '.kHk', 'kHIk', '.kIJk', '..kk']
HORN = [
    '.kk',
    '.kHkk',
    '..kHIkk',
    '..kHHIIkk',
    '...kHHIIIkk',
    '....kHHIIIJkk',
    '.....kHHIIIJJk',
    '......kHHIIJJJk',
    '......kHHIIJJk',
    '.......kIIJJk',
    '........kkkk',
]
HORN2 = ['.kk', '.kIkk', '..kIJkk', '..kIIJJkk', '...kIIJJJk', '....kkIJJk', '......kkk']
JAW = [
    'kCCCCCCCCHCk',
    'kCCCCCCCCCDk',
    '.kbbaaaaabdk',
    '..kkkkkkkkk',
]
MOUTH = ['kHmHmmmmHk', 'kmmnnnnnmk', 'kmmmnnnmmk', '.kkkkkkkk']
BODY = [
    '',
    '..........................kBBCaabk',
    '.........................kBBCCabbk',
    '........................kABBCCaabk',
    '........................kBBCCCdddk',
    '.......................kABBCCCaabk',
    '......................kABBBCCCaabk',
    '......................kBBBCCCCaabk',
    '......................kBBCCCCCdddk',
    '.....................kABBCCCCCaabk',
    '.....................kBBBCCCCCaabk',
    '.....................kBBCCCCCCaabk',
    '.....................kBCCCCCCCdddk',
    '............kkkkkkkkkBCCCCCCCCaabk',
    '.........kkkAAABBBBBBBBCCCCCCCaabk',
    '.......kkAAAABBBBBBBBBBCCCCCCaabbk',
    '.....kkAAABBBBBBBBBBBBCCCCCCCaabbk',
    '....kAABBBBBBBBBBBBBBCCCCCCCdddddk',
    '...kABBBBBBBBBBBBBBCCCCCCCCaaabbbk',
    '..kABBBBBBBBBBBBBCCCCCCCCCCaaabbbk',
    '..kBBBBBBBBBBBBCCCCCCCCCCCdddddk',
    '.kABBBBBBBBBBBCCCCCCCCCCCCaaabbk',
    '.kBBBBBBBBBBBCCCCCCCCCCCCCaaabbk',
    '.kBBBBBBBBBBCCCCCCCCCCCCCCaabbbk',
    '.kCBBBBBBBBCCCCCCCCCCCCCCCdddddk',
    '.kCCBBBBBBCCCCCCCCCCCCCCDDaabbbk',
    '.kCCCBBBBCCCCCCCCCCCCCDDDbbbbbdk',
    '..kCCCCCCCCCCCCCCCCCCDDDDbbbbdk',
    '..kDCCCCCCCCCCCCCCCCDDDDDdddddk',
    '...kDDCCCCCCCCCCCCDDDDDDDEEddk',
    '....kDDDCCCCCCCCCDDDDDDDEEEdk',
    '.....kEDDDDCCCCCDDDDDDDEEEEk',
    '.......kEEDDDDDDDDDDDDEEEk',
    '.........kkEEEEEEEEEEEkk',
    '............kkkkkkkkk',
]
BODY_MARKS = [(15, 12, 'A'), (15, 13, 'A'), (16, 10, 'A'), (16, 11, 'A'), (18, 8, 'C'), (18, 9, 'C'), (19, 9, 'C'), (17, 14, 'C'), (17, 15, 'C'), (18, 15, 'C'), (20, 11, 'C'), (20, 12, 'C'), (21, 12, 'C'), (19, 18, 'C'), (19, 19, 'C'), (20, 19, 'C'), (22, 7, 'C'), (22, 8, 'C'), (23, 8, 'C'), (23, 16, 'D'), (23, 17, 'D'), (24, 17, 'D')]
for (r, c, ch) in BODY_MARKS: BODY[r] = BODY[r][:c] + ch + BODY[r][c + 1:]
SPINE = ['..kk', 'kHIk', '..kk']
HIND = [
    '......kkkkk',
    '....kkAABBBkk',
    '...kAABBBBBBCk',
    '..kABBBBBBBBCCk',
    '.kABBBBBBBBBCCCk',
    '.kBBBBBBBBBBCCCk',
    'kABBBBBBBBBCCCCDk',
    'kBBBBBBBBBCCCCCDk',
    'kBBBBBBBBCCCCCDDk',
    'kCBBBBBBCCCCCDDDk',
    'kCCBBBBCCCCCDDDk',
    '.kCCCCCCCCDDDDk',
    '.kDCCCCCDDDDEk',
    '..kDDCCDDDEEk',
    '..kBDDDDEEk',
    '.kBBCDDEk',
    '.kBBCDDk',
    '.kBCCDDk',
    '..kBCDDk',
    '..kBCCDk',
    '..kBBCDDk',
    '..kBBCCDDkk',
    '..kABBCCCDDkk',
    '.kBBBBCCCCDDDkk',
    '.kBDDCCCCDDDDHkHk',
    '..kkkkkkkkkkkkkk',
]
FRONT = [
    '...kkkk',
    '..kABBBk',
    '.kABBBBCk',
    'kABBBBBCCk',
    'kBBBBBBCCk',
    'kBBBBBCCCk',
    'kCBBBBCCDk',
    '.kCBBCCDDk',
    '..kBCCDDk',
    '..kBCCDDk',
    '..kBBCDDk',
    '..kBBCDDk',
    '..kBBCCDk',
    '..kBBCCDDk',
    '..kBBCCDDk',
    '.kkBBBCCDDkk',
    'kABBBBBCCDDDk',
    'kBBBBBCCCDDDHk',
    'kDDDCCCCDDHkHk',
    '.kkkkkkkkkkkk',
]
TAIL = [
    '....kk',
    '...kAAk',
    '..kABBCk',
    '.kABBBCCk',
    'kABBBBCCDk',
    'kBBBBCCCDk',
    '.kkBCCDkk',
    '...kCDk',
    '..kBCCDk',
    '..kBCCDDk',
    '.kBBCCDDk',
    '.kBBCCCDk',
    '.kBBCCCDDk',
    '.kBBCCCDDk',
    '.kBBBCCCDDk',
    '.kABBCCCDDk',
    '.kABBBCCCDDk',
    '..kABBCCCDDDk',
    '..kABBBCCCDDDk',
    '...kABBBCCCDDDkk',
    '....kABBBCCCCDDDDkk',
    '.....kkBBBBCCCCCDDDDkk',
    '.......kkBBBBBCCCCCDDDk',
    '.........kkDDDCCCCCCDDDk',
    '...........kkkDDDDDDEEk',
    '..............kkkkkkkk',
]
DARK = {'A': 'C', 'B': 'C', 'C': 'D', 'D': 'E', 'H': 'I', 'I': 'J', 'r': 's', 's': 't', 't': 'u'}
def dark(rows): return [''.join(DARK.get(ch, ch) for ch in r) for r in rows]

# ---- 翼：骨（ピクセルパーフェクトな 直線）と 膜（多角形）を 手で 指定して 打つ ----
def bres(x0, y0, x1, y1):
    pts = []; dx = abs(x1 - x0); dy = -abs(y1 - y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1; e = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1: break
        e2 = 2 * e
        if e2 >= dy: e += dy; x0 += sx
        if e2 <= dx: e += dx; y0 += sy
    return pts
def inpoly(x, y, P):
    c = False
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
def wing(darker=False):
    W, H = 38, 36; g = [['.'] * W for _ in range(H)]
    root, wrist = (31, 33), (21, 9)
    tips = [(1, 1), (2, 14), (9, 24)]
    # 膜（指と指の あいだ）。ふちは ほたて形に へこませる
    panels = [
        ([wrist, tips[0], (2, 5), (4, 10), tips[1]], 'r'),
        ([wrist, tips[1], (5, 18), (7, 22), tips[2]], 's'),
        ([wrist, tips[2], (14, 26), (19, 29), (24, 31), root], 's'),
    ]
    for P, c in panels:
        for y in range(H):
            for x in range(W):
                if inpoly(x + .5, y + .5, P): g[y][x] = c
    # 膜の さかいめを 市松模様（ディザ）で なじませる（GBAの 翼の ぬり方）
    src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c not in 'rst' or (x + y) % 2: continue
            for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and src[yy][xx] in 'rst' and src[yy][xx] > c:
                    g[y][x] = src[yy][xx]; break
    # 骨
    def bone(a, b, c1='B', c2='D'):
        for (x, y) in bres(*a, *b):
            g[y][x] = c1
            if y + 1 < H and g[y + 1][x] in 'rst.': g[y + 1][x] = c2
            # 骨の すぐ下の 膜に 影（濃い膜色）
            if y + 2 < H and g[y + 2][x] in 'rs': g[y + 2][x] = 't'
    bone(root, wrist, 'B', 'C'); bone((root[0] + 1, root[1]), (wrist[0] + 1, wrist[1]), 'C', 'D')
    for t in tips: bone(wrist, t, 'A' if t == tips[0] else 'B', 'D')
    # つめ（手首）
    g[wrist[1] - 1][wrist[0]] = 'H'; g[wrist[1] - 2][wrist[0] - 1] = 'I'
    # 外側の 輪郭
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.': continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    rows = [''.join(r) for r in out]
    return dark(rows) if darker else rows

# ---- 組み立て（下から 順に 重ねる）----
def layers():
    return [
        dict(n='wing2', g='wing2', x=12, y=-5, rows=wing(True)),
        dict(n='horn2', g='head', x=39, y=0, rows=HORN2),
        dict(n='legFF', g='legB', x=41, y=42, rows=dark(FRONT)),
        dict(n='legFH', g='legA', x=22, y=36, rows=dark(HIND)),
        dict(n='tail', g='tail', x=0, y=22, rows=TAIL),
        dict(n='body', g='body', x=14, y=18, rows=BODY),
        dict(n='sp1', g='body', x=32, y=21, rows=SPINE), dict(n='sp2', g='body', x=31, y=25, rows=SPINE), dict(n='sp3', g='body', x=29, y=29, rows=SPINE),
        dict(n='legH', g='legB', x=13, y=36, rows=HIND),
        dict(n='legF', g='legA', x=35, y=42, rows=FRONT),
        dict(n='wing', g='wing', x=0, y=-3, rows=wing()),
        dict(n='head', g='head', x=36, y=4, rows=HEAD),
        dict(n='fin', g='head', x=34, y=13, rows=FIN),
        dict(n='mouth', g='head', x=50, y=19, rows=MOUTH, only='atk1|atk2'),
        dict(n='jaw', g='jaw', x=49, y=19, rows=JAW),
        dict(n='eye', g='head', x=47, y=12, rows=EYE, alt=EYE_ALT),
        dict(n='horn', g='head', x=32, y=0, rows=HORN),
    ]

# ほのおの いき（攻撃の 2・3コマ目だけ）
FIRE = [
    '....kk.....',
    '..kkFFkk...',
    '.kFFFGGKk..',
    'kFFFGGKKLk.',
    'kFFGGGKKLLk',
    '.kFFGGKKLk.',
    '..kkGKKkk..',
    '....kkk....',
]
FIRE2 = [
    '.....kk..kk.',
    '...kkGGkkKLk',
    '.kkGGGKKKLLk',
    'kFFGGKKKLLk.',
    'kFFFGGKKLk..',
    '.kkFGGKKLLk.',
    '...kkKKLLkk.',
    '.....kkkk...',
]

# 動き：グループごとの ずらし（右向き、y は 下が +）。親が 動くと 子も 動く
FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'wing': (0, -1), 'wing2': (0, -1)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'wing': (0, -1), 'wing2': (0, -1), 'tail': (-1, 0)},
    'idle3': {'tail': (-1, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'tail': (1, 0)},
    'walk1': {'body': (0, -1), 'wing': (0, 1), 'wing2': (0, 1), 'head': (0, 1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'tail': (-1, 0)},
    'walk3': {'body': (0, -1), 'wing': (0, 1), 'wing2': (0, 1), 'head': (0, 1)},
    'atk0': {'root': (-2, 0), 'head': (-2, -2), 'wing': (0, -3), 'wing2': (0, -3), 'tail': (-1, -1), 'legA': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (2, 1), 'jaw': (0, 3), 'wing': (-1, 1), 'wing2': (-1, 1), 'legA': (2, 0), 'tail': (1, 1)},
    'atk2': {'root': (2, 0), 'head': (1, 0), 'jaw': (0, 2), 'legA': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'wing': (0, -3), 'wing2': (0, -3), 'tail': (-1, -2), 'legA': (-1, 0)},
    'ko': {'body': (0, 5), 'head': (3, 6), 'wing': (2, 7), 'wing2': (2, 7), 'tail': (0, 4), 'legA': (2, 1), 'legB': (-2, 1)},
}
_layers = layers
def layers():
    L = _layers()
    L.insert(len(L), dict(n='fire', g='head', x=61, y=17, rows=FIRE, alt={'atk2': FIRE2}, only='atk1|atk2'))
    return L
