# キバセイウチ（こおり・みず × セイウチ）手打ち GBA風
from pix import grid, rows_of, ellipse, outline, recolor
META = dict(id='kibaseiuchi', name='キバセイウチ', types=['ice', 'water'], base='セイウチ', size='L')
PAL = {
    'k': '#101018', 'l': '#3c1e2a',
    'A': '#d49a74', 'B': '#9a6048', 'C': '#5e3432',      # 皮（明・中・暗）
    'i': '#e6fbff', 'j': '#8cd6f2', 'h': '#3f86c0',      # 氷（明・中・暗）
    'w': '#ffffff', 'e': '#ff5a3c',                      # きらめき・目の 芯
    'm': '#7a2638', 'b': '#e8cfa8',                      # 口の 中・ひげ
}
LIGHT = set('Aiwb')
KEEP_BLACK = set('wije')

# ---- 胴（あたりは だ円 → 陰影は 行・列の きょりで 3段 → しわ・いぼは 手で 打つ）----
def body():
    W, H = 50, 40; g = grid(W, H)
    ellipse(g, 28, 23, 19, 15, '#'); ellipse(g, 33, 16, 14, 14, '#'); ellipse(g, 15, 28, 14, 9.5, '#'); ellipse(g, 6, 32, 5.5, 5, '#')
    for y in range(37, H):
        for x in range(W): g[y][x] = '.'
    def run(x, y, dx, dy):
        n = 0
        while 0 <= x < W and 0 <= y < H and g[y][x] != '.': n += 1; x += dx; y += dy
        return n
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(x, y, 0, -1), run(x, y, -1, 0), run(x, y, 0, 1), run(x, y, 1, 0)
            c = 'B'
            if dn <= 6 or (rt <= 4 and up > 4): c = 'C'
            if dn == 7 and (x + y) % 2: c = 'C'
            if up <= 2 or lf <= 2 or (up <= 4 and lf <= 6): c = 'A'
            if up <= 1 and rt <= 4: c = 'B'
            out[y][x] = c
    # 脂肪の ひだ（たてに 弧を えがく みぞ）と 首の しわ：1点ずつ 手で
    folds = [[(31, 5), (30, 6), (30, 7), (29, 8), (29, 9), (29, 10), (29, 11), (30, 12), (30, 13), (31, 14)],
             [(36, 3), (35, 4), (35, 5), (34, 6), (34, 7), (34, 8), (34, 9), (34, 10), (35, 11), (35, 12), (36, 13)],
             [(23, 12), (22, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 18), (21, 19), (21, 20), (22, 21), (22, 22), (23, 23), (23, 24), (24, 25)],
             [(13, 16), (12, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 22), (11, 23), (12, 24), (12, 25), (13, 26), (13, 27)],
             [(4, 22), (4, 23), (4, 24), (4, 25), (5, 26), (5, 27)]]
    for f in folds:
        for (x, y) in f:
            if out[y][x] != '.': out[y][x] = 'l'
            if out[y][x - 1] in 'B': out[y][x - 1] = 'A'
            if out[y][x + 1] in 'AB': out[y][x + 1] = 'C'
    # 古傷（ななめの 線）といぼ
    for (x, y) in ((16, 13), (17, 14), (18, 15), (17, 13)):
        out[y][x] = 'C'
    for (x, y) in ((8, 20), (17, 21), (26, 18), (7, 28), (16, 29), (27, 27), (40, 18), (40, 24)):
        if out[y][x] in 'BC': out[y][x] = 'A'; out[y + 1][x] = 'l'
    return outline(rows_of(out))

HEAD = [
    '.....kk.....kk.............',
    '....kik....kik.............',
    '...kiijk..kiijk............',
    '...kijhk..kijhk............',
    '..kAijhkkkkijhkkk..........',
    '..kAkjhkAAAkjhkBBkk........',
    '..kAAkkAAAAAkkBBBBBkk......',
    '..kAAAABBBBBBBBBBBBBBkk....',
    '.kAABBBBBBBkkkkiiijjjhkk...',
    '.kABBBBBBBBBBkkkkhhhhhhkk..',
    '.kABBBBBBBBBBBBBBBBBBBBBBk.',
    '.kABBBBBBBBBBBBBBBBBBBBBBk.',
    '.kABBBBBBBBBBBAAAAAAAAABBBk',
    '.kABBBBBBBBBAAbAAAbAAAAABCk',
    '.kBBBBBBBBBAAAAAbAAAbAAABCk',
    '.kBBBBBBBBBAbAAAAbAAAbABBCk',
    '.kCBBBBBBBBBAAbAAAAbAABBBCk',
    '.kCBBBBBBBBBBBBBBBBBBBBBCCk',
    '.kCCBBBBBBBBCCCCCCCCCCCCCk.',
    '..kCCBBBBBCkkkkkkkkkkkkkk..',
    '..kCCCCBBCkmmmmmmmmmmk.....',
    '...kCCCCCCCkkkkkkkkkk......',
    '....kkCCCCCk...............',
    '......kkkkk................',
]
HEAD_OPEN = HEAD[:19] + [
    '..kCCBBBBBCkkkkkkkkkkkkkkk.',
    '..kCCCCBBCkmmmmmmmmmmmmmk..',
    '...kCCCCCkmmmmmmmmmmmmk....',
    '....kCCCCkmmmmmmmmmmk......',
    '....kCCCCCkkkkkkkkkk.......',
    '.....kkkkk.................',
]
# するどい 目：まゆの ひさしの 下で 氷色に 光る、たての ひとみ
EYE = ['kkweek', '.kweek', '..kkk']
EYE_ALT = {'blink': ['kkkkkk', '.BBBBk', '..BBB'], 'hit': ['kkBkBk', '.BkBk', '..BBB'], 'atk0|atk1|atk2': ['kkwwek', '.kweek', '..kkk'], 'ko': ['kBkBkB', '.BkBk', '..BBB']}

# つららの きば（左＝光、右＝影、先が とがる）
TUSK = [
    'kiijhk', 'kiijhk', 'kiijhk', 'kwijhk', 'kiijhk', 'kiijjhk', '.kiijhk', '.kijjhk', '.kiijhk', '.kwijhk',
    '..kijhk', '..kiijhk', '..kijjhk', '..kiijk', '...kijhk', '...kijk', '...kiik', '....kik', '....kjk', '....kk',
]
FTUSK = recolor(TUSK, {'i': 'j', 'j': 'h', 'w': 'j', 'h': 'h'})

# 背の 氷の よろい（結晶の 板）
SHARD_A = ['....kk', '...kik', '..kiijk', '.kiijhk', '.kijjhk', 'kiijhhk', 'kijjhk.', 'kkkkk..']
SHARD_B = ['..kk..', '.kiik.', '.kijk.', 'kiijhk', 'kijjhk', 'kijhhk', 'kkkkkk']
SHARD_C = ['...kk', '..kik', '.kiik', '.kijk', 'kijhk', 'kjhhk', 'kkkk.']
SHARD_GLINT = ['....kk', '...kwk', '..kwijk', '.kiijhk', '.kijjhk', 'kiijhhk', 'kijjhk.', 'kkkkk..']
# ひれ足（前・後ろ）とつめ
FLIP_F = [
    '.kkkkk......',
    'kABBBCk.....',
    'kABBBCk.....',
    'kABBBBCk....',
    'kABBBBCCk...',
    'kBBBBBBCCkk.',
    'kBBBBBBBCCCk',
    '.kCCCCCCCCCk',
    '..kwkwkwkkk.',
]
FLIP_H = [
    '....kkkkk.',
    '...kABBBCk',
    '..kABBBCCk',
    '.kABBBCCk.',
    'kABBCCCk..',
    'kBCCCCk...',
    'kkwkwkk...',
]
DARK = {'A': 'B', 'B': 'C', 'C': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# 攻撃の 氷の 柱（地面から 突き出す）
def burst(big=False):
    a = [
        '..........kk.........',
        '.........kik.........',
        '....kk..kiijk........',
        '...kik..kijhk...kk...',
        '..kiijk.kijhk..kik...',
        '..kijhk.kiijhk.kijk..',
        '.kiijhk.kijjhk.kijhk.',
        '.kijjhk.kijhhk.kijhk.',
        'kiijhhkkiijhhk.kiijhk',
        'kkkkkkkkkkkkkkkkkkkkk',
    ]
    if not big: return a[4:]
    return [
        '.w.......kk.....w....',
        'wiw.....kik....wiw...',
        '.w..kk..kiijk...w.kk.',
        '...kik..kijhk...kkik.',
        '..kiijk.kijhk..kiijk.',
        '..kijhk.kiijhk.kijhk.',
        '.kiijhk.kijjhk.kijhk.',
        '.kijjhk.kijhhk.kijhk.',
        'kiijhhkkiijhhk.kiijhk',
        'kkkkkkkkkkkkkkkkkkkkk',
    ]
FROST = ['.w.', 'wiw', '.w.']
BODY = body()
def top(x, x0=-1, y0=17):
    for j, r in enumerate(BODY):
        if 0 <= x - x0 < len(r) and r[x - x0] != '.': return y0 + j
    return 60
def on_back(x, rows, sink=3): return dict(x=x, y=top(x + len(rows[-1]) // 2) - len(rows) + sink, rows=rows)

def layers():
    return [
        dict(n='flipFF', g='legB', x=46, y=50, rows=dark(FLIP_F)),
        dict(n='flipHF', g='legA', x=5, y=52, rows=dark(FLIP_H)),
        dict(n='body', g='body', x=-1, y=17, rows=BODY),
        dict(n='flipH', g='legB', x=1, y=53, rows=FLIP_H),
        dict(n='shA', g='body', **on_back(7, SHARD_C)),
        dict(n='shB', g='body', **on_back(13, SHARD_A), alt={'idle2|idle3': SHARD_GLINT}),
        dict(n='shC', g='body', **on_back(20, SHARD_B, 2)),
        dict(n='shD', g='body', **on_back(26, SHARD_A)),
        dict(n='shE', g='body', **on_back(32, SHARD_B, 2)),
        dict(n='ftusk', g='head', x=52, y=31, rows=FTUSK),
        dict(n='head', g='head', x=37, y=12, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=51, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='tusk', g='head', x=46, y=31, rows=TUSK),
        dict(n='flipF', g='legA', x=36, y=51, rows=FLIP_F),
        dict(n='frost', g='fx', x=59, y=22, rows=FROST, only='idle1|idle2|atk0'),
        dict(n='burst', g='fx2', x=50, y=48, rows=burst(), alt={'atk2': burst(True)}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0), 'fx': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'fx': (1, -2)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, -1), 'head': (-2, -4), 'legA': (0, -1), 'fx': (-3, -5)},
    'atk1': {'root': (3, 0), 'body': (0, 2), 'head': (2, 5)},
    'atk2': {'root': (4, 0), 'body': (0, 2), 'head': (2, 5), 'fx2': (0, 0)},
    'hit': {'root': (-3, 0), 'head': (-3, -2), 'body': (0, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root', 'fx2': 'root'}
