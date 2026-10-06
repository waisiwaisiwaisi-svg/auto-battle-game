# キバセイウチ（こおり・みず × セイウチ）手打ち GBA風
from pix import grid, rows_of, ellipse, outline, recolor
META = dict(id='kibaseiuchi', name='キバセイウチ', types=['ice', 'water'], base='セイウチ', size='L')
EYE_BOX = (42, 23, 9, 5)   # 重い まぶたの 目（idle0）
PAL = {
    'k': '#101018', 'l': '#3c1e2a',
    'A': '#d49a74', 'B': '#9a6048', 'C': '#5e3432',      # 皮（明・中・暗）
    'i': '#e6fbff', 'j': '#8cd6f2', 'h': '#3f86c0',      # 氷（明・中・暗）
    'w': '#ffffff', 'e': '#ff5a3c',                      # きらめき・目の 芯
    'm': '#7a2638', 'b': '#e8cfa8',                      # 口の 中・ひげ
    'r': '#a8203a',                                      # 目（虹彩の 暗）
}
LIGHT = set('Aiwb')
KEEP_BLACK = set('wijer')

# ---- 胴（デフォルメ：小さく 丸い 肉の 山。あたりは だ円 → 陰影は 行・列の きょりで 3段 → しわ・いぼは 手で 打つ）----
def body():
    W, H = 34, 27; g = grid(W, H)
    ellipse(g, 18, 14, 12, 12, '#'); ellipse(g, 22, 11, 9.5, 10, '#'); ellipse(g, 9, 17, 8.5, 8, '#'); ellipse(g, 4.5, 21, 4.5, 4, '#')
    for y in range(25, H):
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
            if dn <= 4 or (rt <= 3 and up > 3): c = 'C'
            if dn == 5 and (x + y) % 2: c = 'C'
            if up <= 2 or lf <= 2 or (up <= 3 and lf <= 5): c = 'A'
            if up <= 1 and rt <= 3: c = 'B'
            out[y][x] = c
    # 脂肪の ひだ（たてに 弧を えがく みぞ）：1点ずつ 手で
    folds = [[(22, 4), (21, 5), (21, 6), (21, 7), (21, 8), (22, 9), (22, 10)],
             [(15, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (15, 14), (15, 15), (16, 16)],
             [(9, 12), (8, 13), (8, 14), (8, 15), (8, 16), (9, 17), (9, 18)],
             [(3, 17), (3, 18), (3, 19), (4, 20)]]
    for f in folds:
        for (x, y) in f:
            if out[y][x] != '.': out[y][x] = 'l'
            if out[y][x - 1] in 'B': out[y][x - 1] = 'A'
            if out[y][x + 1] in 'AB': out[y][x + 1] = 'C'
    # 古傷（ななめの 線）といぼ
    for (x, y) in ((11, 9), (12, 10), (13, 11)):
        out[y][x] = 'C'
    for (x, y) in ((6, 15), (12, 18), (18, 12), (26, 9), (20, 20), (28, 17)):
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
# 目：重い まぶた（M）。皮の 厚い 上まぶたが 平らに おりて 虹彩の 上半分を かくす。下半分に 血走った 白目（w に 赤い すじ e）と 赤い 虹彩（e 明・r 暗）、半月の ひとみ k。冷たく 見下す
EYE = ['.BAAAAB..', 'kkkkkkkkk', 'kwewrkkrk', '.kwwekekk', '..kkkkkk.']
EYE_ALT = {'blink': ['.BAAAAB..', 'kABBBBBBk', 'kBBBBBBCk', '.kkkkkkkk', '..CCCCC..'],
           'hit': ['.BAAAAB..', 'kkkABBkkk', '.kkkkkkk.', '..kwkekk.', '...kkkk..'],
           'atk0|atk1|atk2': ['.BAAAAB..', 'kkkkkkkkk', 'kwewwkkwk', '.kwwwewek', '..kkkkkk.'],
           'ko': ['.BAAAAB..', 'kkBBBBBkB', 'BBkBBkBBB', 'B.BkkBBB.', '..kBBkB..']}

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
BX, BY = 6, 29
HX, HY = 29, 14     # 頭の 位置（頭は 元の 大きさ）
def top(x, x0=BX, y0=BY):
    for j, r in enumerate(BODY):
        if 0 <= x - x0 < len(r) and r[x - x0] != '.': return y0 + j
    return 60
def on_back(x, rows, sink=3): return dict(x=x, y=top(x + len(rows[-1]) // 2) - len(rows) + sink, rows=rows)

def layers():
    return [
        dict(n='flipFF', g='legB', x=38, y=51, rows=dark(FLIP_F)),
        dict(n='flipHF', g='legA', x=11, y=52, rows=dark(FLIP_H)),
        dict(n='body', g='body', x=BX, y=BY, rows=BODY),
        dict(n='flipH', g='legB', x=5, y=53, rows=FLIP_H),
        dict(n='shA', g='body', **on_back(9, SHARD_C)),
        dict(n='shB', g='body', **on_back(14, SHARD_A), alt={'idle2|idle3': SHARD_GLINT}),
        dict(n='shC', g='body', **on_back(20, SHARD_B, 2)),
        dict(n='shD', g='body', **on_back(26, SHARD_A)),
        dict(n='ftusk', g='head', x=HX + 15, y=HY + 19, rows=FTUSK),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=HX + 13, y=HY + 9, rows=EYE, alt=EYE_ALT),
        dict(n='tusk', g='head', x=HX + 9, y=HY + 19, rows=TUSK),
        dict(n='flipF', g='legA', x=29, y=51, rows=FLIP_F),
        dict(n='frost', g='fx', x=HX + 22, y=HY + 9, rows=FROST, only='idle1|idle2|atk0'),
        dict(n='burst', g='fx2', x=HX + 15, y=48, rows=burst(), alt={'atk2': burst(True)}, only='atk1|atk2'),
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
