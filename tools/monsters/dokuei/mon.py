# ドクエイ（どく・みず × エイ）手打ち GBA風・デフォルメ（2〜3頭身：前に 大きな 頭と つり目、つばさは 小さく、毒針の 尾は 大きい まま）
META = dict(id='dokuei', name='ドクエイ', types=['poison', 'water'], base='エイ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c1a2a',
    'A': '#6e9e8c', 'B': '#3e6a62', 'D': '#22403e',
    'E': '#c8d8c0',
    'P': '#ff7ae0', 'p': '#c03aa8', 'q': '#6a1a6a',
    'Y': '#ffe040', 'y': '#c08a10',
    'w': '#f4ecd8', 'n': '#b0a080',
    'c': '#a8f0ff',
}
LIGHT = set('AEPwYc')
KEEP_BLACK = set('wYyPp')

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, poly, outline, rows_of
def _run(g, x, y, dx, dy, ch):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] == ch: n += 1; x += dx; y += dy
    return n
# 体：つばさ（デフォルメで 小さく）と 大きな 頭を 1枚で 描く（頭は つばさに 食いこむ。輪郭で 切らない）
# 奥の つばさは 上、手前の つばさは 下（裏の 白い ふちが 見える）。頭は 前へ つき出た 頭びれ（角の ような ひれ）と 下の 牙の 口
def body():
    g = grid(64, 64)
    poly(g, [(10, 46.5), (18, 39), (27, 35), (36, 34), (42, 37), (44, 44), (10, 47)], '1')          # 奥の つばさ
    poly(g, [(10, 46), (44, 44), (45, 47), (38, 52), (29, 56), (22, 57), (16, 54)], '2')            # 手前の つばさ
    poly(g, [(36, 43), (38, 37), (42, 33), (48, 31), (54, 31), (58, 33), (61, 37), (62, 42), (60, 47), (55, 50.5), (47, 51.5), (40, 49.5)], '3')
    poly(g, [(56, 33), (60, 30), (63.5, 30), (61, 34), (59, 36)], '3')                              # 奥の 頭びれ
    poly(g, [(58, 44), (63.5, 46), (63, 49), (58, 48)], '3')                                        # 手前の 頭びれ
    out = [r[:] for r in g]
    for y in range(64):
        for x in range(64):
            c = g[y][x]
            if c == '.': continue
            up = _run(g, x, y, 0, -1, c); dn = _run(g, x, y, 0, 1, c)
            if c == '1': out[y][x] = 'A' if up <= 1 else 'D' if dn <= 1 else 'B'
            elif c == '2': out[y][x] = 'A' if up <= 1 else 'E' if dn <= 2 else 'D' if dn == 3 else 'B'
            else:
                lf = _run(g, x, y, -1, 0, c); rt = _run(g, x, y, 1, 0, c)
                out[y][x] = 'D' if (dn <= 2 or rt <= 1) else 'A' if (up <= 2 or (lf <= 1 and y < 44)) else 'B'
    def P(pts, ch):
        for x, y in pts: out[y][x] = ch
    # 奥の つばさの 光の すじ（ひれの 骨）
    for x, y in ((22, 39), (23, 40), (24, 41), (30, 37), (31, 38), (32, 39)):
        if out[y][x] == 'B': out[y][x] = 'A'
    # 頭と つばさの さかい：影の 線（輪郭で 切らない）
    for y in range(64):
        for x in range(1, 64):
            if g[y][x] == '3' and g[y][x - 1] in '12': out[y][x - 1] = 'D'
    # 頭の まるみの 光（左上の 三日月）
    P([(41, 35), (40, 36), (39, 37), (39, 38)], 'A')
    # まゆの ひさし（黒い 線、目の 上で つり上がる）
    P([(41, 35), (42, 35), (43, 36), (44, 36), (45, 36), (46, 36), (47, 36), (48, 37), (49, 37)], 'k')
    P([(51, 34), (52, 34), (53, 34), (54, 34), (55, 35), (56, 35)], 'k')
    # 毒の いぼ（頭の 上）
    P([(46, 32), (50, 32)], 'p'); P([(45, 33), (49, 33)], 'P')
    # 口：下がわに 横に さけた 口と 牙、白い あご
    P([(46, 47), (47, 47), (48, 47), (49, 47), (50, 47), (51, 47), (52, 47), (53, 46), (54, 46), (55, 46), (56, 46), (57, 45), (58, 45), (59, 45)], 'k')
    P([(48, 48), (51, 48), (54, 47), (57, 46)], 'w'); P([(53, 45), (56, 44)], 'w')
    for x in range(44, 60):
        for y in range(49, 53):
            if g[y][x] == '3' and out[y][x] in 'BD': out[y][x] = 'E'
    ys = [y for y in range(64) if any(c != '.' for c in out[y])]; xs = [x for x in range(64) if any(out[y][x] != '.' for y in range(64))]
    return xs[0] - 1, ys[0] - 1, outline(rows_of([r[xs[0]:xs[-1] + 1] for r in out[ys[0]:ys[-1] + 1]]))
DX, DY, DISC = body()
SEG = [(0, 12), (12, 24), (24, 99)]   # つばさの 波うち用（列で 3つに 分ける。前の 列は 頭と いっしょ）
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]

# 尾：うしろへ 出て、さそりの ように 上へ 反り返る
TAIL = [
    '..............kkkk.',
    '...........kkkAAABk',
    '.........kkAAABBBDk',
    '........kAABBBDDDk.',
    '.......kAABDDDkkk..',
    '.....kkABBDkkk.....',
    '....kAABBDk........',
    '....kABBDk.........',
    '...kABDDk..........',
    '...kABDk...........',
    '..kABDk............',
    '.kAABDk............',
    '.kABDk.............',
    'kAABDk.............',
    'kAABDk.............',
    'kAABDk.............',
    'kAABDk.............',
    'kAABDk.............',
    'kAABDk.............',
    'kABBDk.............',
    'kABBDk.............',
    'kABBDk.............',
    'kABBDDk............',
    '.kAABDk............',
    '..kABBDk...........',
    '...kABBDkkkkkk.....',
    '...kAABAAAAAAAk....',
    '....kAABBBBBBAAk...',
    '.....kADDDDDBBBk...',
    '......kkkkkkDDk....',
    '............kk.....',
]
# 尾で 突く（攻撃）：体の 上を こえて 前へ
TAIL_STRIKE = [
    '....................kkkkkkkkkkkkkkkk..............',
    '.................kkkAAAAAAAAAAAAAAAAkkkkk.........',
    '...............kkAAAABBBBBBBBBBBBBBBBAAAAkk.......',
    '............kkkAAABBBDDDDDDDDDDkDDDDDBBBBAAkk.....',
    '.........kkkAAABBBDDkkkkkkkkkkk.kkkkkkDDDDBAAk....',
    '........kAAABBBDDDkk..................kkkkDBAAk...',
    '.......kAABBBDDkkk........................kDBBAk..',
    '......kAABDDDkk............................kDBBAk.',
    '.....kAABDDkk...............................kDDBAk',
    '....kAABDDk..................................kkDBk',
    '...kAABDDk.....................................kk.',
    '..kAABDDk.........................................',
    '.kAABDDk..........................................',
    '.kABBDk...........................................',
    '.kABDk............................................',
    '.kABDk............................................',
    '.kABDk............................................',
    '.kABDk............................................',
    '.kABDk............................................',
    '.kABDk............................................',
    'kAABDk............................................',
    'kAABDk............................................',
    'kABBAAk...........................................',
    '.kDBBAk...........................................',
    '..kDBBAk..........................................',
    '...kDBBAk.........................................',
    '....kDBAAk........................................',
    '....kDDBAAk.......................................',
    '.....kDDBAk.......................................',
    '......kDBk........................................',
    '.......kk.........................................',
]
def cut(rows, x0, x1): return [r[x0:x1] for r in rows]
SEG = [(0, 16), (16, 32), (32, 49)]   # つばさの 波うち用
# 尾の 先の 毒針：ぎざぎざの 骨の 返し
BARB = [
    'kkk.......',
    'kwwkkk....',
    '.kwwnnkk..',
    '..kkwwnnk.',
    '...kkkwnnk',
    '....kPkkkk',
    '.....kk...',
]
BARB_HOT = [
    'kkk.......',
    'kPPkkk....',
    '.kPPppkk..',
    '..kkPPppk.',
    '...kkkPppk',
    '....kPkkkk',
    '....kpk...',
]
BARB_D = [
    'kkk...',
    'kwnk..',
    'kwnnk.',
    '.kwnk.',
    '.kwnk.',
    '..kwk.',
    '..kPk.',
    '...k..',
]
# 毒の ふくろ（つばさに 光る）
GL = ['Pp', 'pq']
GL_HOT = ['PP', 'Pp']
# 目：まゆの ひさしの 下の 金の つり目（白い 光＋金 2段＋たての ひとみ）。手前は 大きく、奥は 小さく
EYE = ['kwYYkYk', 'kYyykyk', '.kkyykk']
EYE_ALT = {'blink': ['BBBBBBB', 'kkkkkkk', '.BBBBBB'], 'atk0|atk1|atk2': ['kwwYkYk', 'kYYYkYk', '.kkYYkk'],
           'hit': ['BkkBBBB', 'BBBkkkk', 'BkkBBBB'], 'ko': ['BkBBkBB', 'BBkkBBB', 'BkBBkBB']}
EYE2 = ['wYkY', 'yykk']
EYE2_ALT = {'blink': ['AAAA', 'kkkk'], 'atk0|atk1|atk2': ['wwkY', 'YYkk'], 'hit': ['kkAA', 'AAkk'], 'ko': ['kAkA', 'AkAA']}
# 毒しぶき
SPRAY = [
    '.P...p..',
    'p.Pp..P.',
    '..pP.p..',
    '.P..p..P',
    '...p..p.',
]
DRIP = ['P', 'p']
# 海底の 砂けむり（すべる）
DUST = [['c....c', '.c..c.'], ['.c..c.', 'c....c']]
def layers():
    L = [
        dict(n='tail', g='tail', x=2, y=17, rows=TAIL, not_='atk1|atk2'),
        dict(n='barb', g='tail', x=17, y=15, rows=BARB, alt={'atk0': BARB_HOT}, not_='atk1|atk2'),
        dict(n='drip', g='tail', x=22, y=22, rows=DRIP, only='idle2|idle3|walk1|walk3'),
    ]
    for i, (a, b) in enumerate(SEG):
        L.append(dict(n=f'd{i}', g=f'w{i}', x=DX + a, y=DY, rows=cut(DISC, a, b)))
    L += [
        dict(n='g1', g='w1', x=26, y=38, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g2', g='w2', x=34, y=38, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g3', g='w0', x=18, y=42, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g4', g='w0', x=20, y=50, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g5', g='w1', x=27, y=49, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g7', g='w2', x=35, y=47, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='eye', g='w2', x=42, y=37, rows=EYE, alt=EYE_ALT),
        dict(n='eye2', g='w2', x=52, y=35, rows=EYE2, alt=EYE2_ALT),
        dict(n='strike', g='root', x=5, y=17, rows=TAIL_STRIKE, only='atk1|atk2'),
        dict(n='barbd', g='root', x=50, y=23, rows=BARB_D, only='atk1|atk2'),
        dict(n='spray', g='root', x=52, y=31, rows=SPRAY, only='atk1'),
        dict(n='dust', g='root', x=4, y=58, rows=DUST[0], alt={'walk1|walk3': DUST[1]}, only='walk0|walk1|walk2|walk3'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'w0': (0, -1), 'tail': (0, -1)}, 'idle2': {'w1': (0, -1), 'tail': (0, -1)}, 'idle3': {'w2': (0, -1)},
    'blink': {},
    'walk0': {'w0': (0, -1)}, 'walk1': {'w1': (0, -1), 'tail': (1, 0)}, 'walk2': {'w2': (0, -1)}, 'walk3': {'w1': (0, 1), 'tail': (-1, 0)},
    'atk0': {'tail': (-1, -2), 'root': (-2, 0), 'w2': (0, 1)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (3, 0), 'w2': (0, 1)},
    'hit': {'root': (-3, 0), 'w2': (0, -2), 'w1': (0, -1), 'tail': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'w0': 'root', 'w1': 'root', 'w2': 'root', 'tail': 'root'}
