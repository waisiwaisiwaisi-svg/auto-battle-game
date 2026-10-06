# ハガマ（くさ・むし × カマキリ）手打ち GBA風
from pix import outline, flip_v
META = dict(id='hagama', name='ハガマ', types=['grass', 'bug'], base='カマキリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2e2014',
    'A': '#d2a874', 'B': '#8c6038', 'C': '#4e3220',      # 樹皮の よろい
    'G': '#c4ee6a', 'H': '#5cb444', 'J': '#246a3a',      # 葉の 鎌
    'O': '#ff9a3c', 'R': '#d02c2c', 'Y': '#fff07a',      # 複眼
    'w': '#ffffff',
}
LIGHT = set('AGYw')
KEEP_BLACK = set('wOYR')
DK = {'A': 'B', 'B': 'C', 'G': 'H', 'H': 'J'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

# ---- 三角の 頭（後ろが 広く、口先は 右下）----
HEAD = [
    "......AAAAAAA.......",
    "...AAABBBBBBBAAA....",
    "..ABBBBBBBBBBBBBA...",
    ".ABBBBBBBBBBBBBBBA..",
    "ABBBBBBBBBBBBBBBBBA.",
    "ABBBBBBBBBBBBBBBBBB.",
    "ABBBBBBBBBBBBBBBBBC.",
    "ABBBBBBBBBBBBBBBBBC.",
    ".CBBBBBBBBBBBBBBBC..",
    "..CBBBBBBBBBBBBBBC..",
    "...CCBBBBBBBBBBBC...",
    ".....CCBBBBBBBBC....",
    ".......CBBBBBBC.....",
    "........CCBBBC......",
]
# 光る 複眼：まゆの ひさし（前へ 下がる）＋ たての ひとみ
EYE = [
    "kk.......",
    "kAkkk....",
    "kYYOOkkk.",
    "kYwYOOOOk",
    "kYYOOkRRk",
    ".kOOOkRk.",
    "..kRRkk..",
    "...kkk...",
]
EYE_ALT = {
    'blink': ["kk.......", "kAkkk....", "kBBBBkkk.", "kkkkkkkkk", ".kBBBBBk.", "..kkkkk..", ".........", "........."],
    'hit': ["kk.......", "kAkkk....", "kOkkOkkk.", "kkOkkOkOk", "kOkkOkOk.", ".kkkkkk..", ".........", "........."],
    'atk0|atk1|atk2': ["kk.......", "kAkkk....", "kYYYYkkk.", "kYwwYYYYk", "kYYYYkOOk", ".kYYYkOk.", "..kOOkk..", "...kkk..."],
    'ko': [".........", ".........", ".k...k...", "..k.k....", "...k.....", "..k.k....", ".k...k...", "........."],
}
# 大あご（白い 牙の はさみ）
MAND = [
    "BB..BC",
    "AwC.Bw",
    ".wk..w",
    "..w...",
]
MAND_OPEN = [
    "BB...BC",
    "AwC..Bw",
    ".wk...w",
    "..w..w.",
]
ANT = ['..........kk', '.......kkk..', '.....kk.....', '...kk.......', 'kkk.........']
# 葉の とさか（頭の 後ろ）
CREST = [
    "GG.......",
    "GHHG.....",
    ".GHHHG...",
    ".JHHHHHG.",
    "..JJHHHHG",
    "....JJJHH",
]

# ---- よろいの 胸（前胸＝首 は 太い 板の かさね）----
NECK = [
    ".......AAAAA",
    "......ABBBBC",
    ".....ABBBBBC",
    ".....ABBBBBC",
    "....ABBBBBC.",
    "....ABBBBBC.",
    "...ABBBBBBC.",
    "...ABBBBBBC.",
    "..ABBBBBBBC.",
    "..ABBBBBBBC.",
    ".ABBBBBBBC..",
    "ABBBBBBBBC..",
    "ABBBBBBBBC..",
]
BODY = [
    "........AAAAAA....",
    ".....AAABBBBBBA...",
    "...AABBBBBBBBBBA..",
    "..ABBBBBBBBBBBBBC.",
    ".ABBBBBBBBBBBBBBC.",
    ".ABBBBBBBBBBBBBBBC",
    "ABBBBBBBBBBBBBBBBC",
    "ABBBBBBBBBBBBBBBCC",
    "ABBBBBBBBBBBBBBBC.",
    ".CBBBBBBBBBBBBBCC.",
    "..CCBBBBBBBBBCCC..",
    "....CCCCCCCCCC....",
]
# よろいの 板の さかい目（左上が 光る 弧）を 手で 置く
def plates(rows):
    g = [list(r) for r in rows]
    for c, ys in ((5, (2, 9)), (9, (1, 10)), (13, (2, 9))):
        for y in range(ys[0], ys[1] + 1):
            off = 1 if y in (ys[0], ys[1]) else 0
            x = c + off
            if g[y][x] == 'B': g[y][x] = 'C'
            if g[y][x + 1] == 'B': g[y][x + 1] = 'A' if y < 6 else 'B'
    for (x, y) in ((3, 4), (7, 3), (11, 3), (2, 6)):
        if g[y][x] == 'B': g[y][x] = 'A'
    return [''.join(r) for r in g]
BODY = plates(BODY)
NECK = [r[:-4] + r[-4:].replace('B', 'C', 1) if i % 3 == 2 else r for i, r in enumerate(NECK)]
# 背の とげ（後ろへ 反る）
THORN = ['k....', 'Akk..', 'kABk.', '.kABk']

# ---- 葉の 腹（大きな 一枚葉。葉脈は 手で）----
ABD = [
    "...............GGGGGG.",
    "...........GGGGHHHHHHH",
    "........GGGHHHHHHHHHHH",
    ".....GGGHHHHHGHHHHHHHH",
    "...GGHHHHGHHGHHHHHHHHJ",
    ".GGHHHHGGGGGGGGGGGGHHJ",
    "GHHHHHHHHJHJHHHHHHHHJJ",
    ".JHHHHHHJHHHJHHHHHHJJJ",
    "..JJHHHJHHHHHJHHHHJJJ.",
    "....JJHHHHHHHHHHJJJJ..",
    "......JJJJHHHHJJJJ....",
    "..........JJJJJ.......",
]

# ---- 葉の 鎌（のこぎり歯は 内がわ＝下と 左に 白で）----
BLADE = [
    "AAGGGGG....",
    "BBHHHHHGG..",
    "CCJHHHHHHG.",
    "..wJGHHHHHJ",
    "..wwJGHHHHJ",
    "...wJHGHHHJ",
    "....JHGHHHJ",
    "...wJHGHHHJ",
    "..wwJHGHHHJ",
    "...wJHGHHJ.",
    "....JHGHHJ.",
    "...wJHGHHJ.",
    "..wwJHGHJ..",
    "...wJGHHJ..",
    "....JGHJ...",
    "...wJGHJ...",
    "..wwJGJ....",
    "...wGJ.....",
    "...GJ......",
    "..GJ.......",
]
# 鎌を ふりあげた 形（攻撃の ため）
def _up(rows):
    r = flip_v(rows)
    return [x.replace('A', '@').replace('C', 'A').replace('@', 'C') for x in r]
BLADE_UP = _up(BLADE)
# 鎌を 前へ ふりぬいた 形（よこ）
BLADE_SWING = [
    "AAAGGGGGGGGGGG....",
    "BBBHHHHHGHHHHHHGG.",
    "CCCJHHHHHHGHHHHHHG",
    "...wJJJHHHHHGHHHHG",
    "......w.wJJJHHHHG.",
    "............wJJHG.",
    "..............wJG.",
    "...............G..",
]
# 腕の つけね（樹皮）
UPPER = [
    "AAAA..",
    "BBBBA.",
    "CBBBBA",
    ".CBBBB",
    "..CBBC",
]
# 太い 足：もも は 上へ、すね は 下へ
LEG_F = [
    ".....AAA..",
    "..AAABBBA.",
    "ABBBBBBBBA",
    "BBBBCCCBBB",
    "CCC....ABBC",
    "......ABBBC",
    "......ABBC.",
    "......ABBC.",
    ".....ABBBC.",
    ".....ABBC..",
    ".....ABBC..",
    ".....ABBC..",
    "....ABBBC..",
    "....ABBC...",
    "....ABBBBBw",
    "....CCCCCC.",
]
LEG_B = [
    "...AAA.....",
    "..ABBBAAA..",
    ".ABBBBBBBBA",
    ".BBBCCCBBBB",
    "ABBC....CCC",
    "ABBC.......",
    "ABBC.......",
    ".ABBC......",
    ".ABBC......",
    ".ABBC......",
    "..ABBC.....",
    "..ABBC.....",
    "..ABBC.....",
    "..ABBC.....",
    "wABBBBB....",
    ".CCCCCC....",
]
# 葉の 斬撃（三日月）と 舞う 葉
SLASH = [
    "....kkkkk.......",
    "..kkGGGGGkk.....",
    ".kGGkkkkkGGk....",
    "kGk......kHGk...",
    "kk........kHGk..",
    "...........kHGk.",
    "............kHHk",
    "............kHHk",
    "...........kHHJk",
    "..........kHJJk.",
    "........kkJJk...",
    "......kkkkk.....",
]
LEAF1 = ['.kk.', 'kGHk', 'kHJk', '.kk.']
LEAF2 = ['..kk', '.kGk', 'kHJk', 'kk..']

ATK_UP = 'atk0'
ATK_SW = 'atk1|atk2'
def base():
    return [
        dict(n='legB', g='legB', x=12, y=43, rows=outline(dk(LEG_B))),
        dict(n='abd', g='tail', x=3, y=29, rows=outline(ABD)),
        dict(n='armB_u', g='armB', x=40, y=24, rows=outline(dk(UPPER))),
        dict(n='armB', g='armB', x=43, y=6, rows=outline(dk(BLADE_UP)), alt={ATK_UP: outline(dk(BLADE_UP)), ATK_SW: outline(dk(BLADE_SWING))}),
        dict(n='body', g='body', x=19, y=31, rows=outline(BODY)),
        dict(n='thorn1', g='body', x=21, y=28, rows=THORN),
        dict(n='thorn2', g='body', x=26, y=27, rows=THORN),
        dict(n='neck', g='body', x=27, y=19, rows=outline(NECK)),
        dict(n='legA', g='legA', x=29, y=44, rows=outline(LEG_F)),
        dict(n='crest', g='head', x=21, y=4, rows=outline(CREST)),
        dict(n='ant', g='head', x=43, y=2, rows=ANT),
        dict(n='head', g='head', x=28, y=7, rows=outline(HEAD)),
        dict(n='mand', g='head', x=38, y=21, rows=outline(MAND), alt={'atk0|atk1|atk2': outline(MAND_OPEN)}),
        dict(n='eye', g='head', x=37, y=9, rows=EYE, alt=EYE_ALT),
        dict(n='armF_u', g='armF', x=35, y=29, rows=outline(UPPER)),
        dict(n='armF', g='armF', x=39, y=29, rows=outline(BLADE), alt={ATK_UP: outline(BLADE_UP), ATK_SW: outline(BLADE_SWING)}),
    ]
def fx():
    return [
        dict(n='slash', g='root', x=50, y=18, rows=SLASH, only='atk1'),
        dict(n='leaf1', g='root', x=62, y=34, rows=LEAF1, only='atk1|atk2'),
        dict(n='leaf2', g='root', x=66, y=22, rows=LEAF2, only='atk2'),
        dict(n='leaf3', g='root', x=58, y=46, rows=LEAF2, only='atk2'),
    ]
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if 'ko' in k.split('|'): rows = v
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[l['y'] + j][l['x'] + i] = c
    ys = [y for y in range(70) if any(c != '.' for c in g[y])]; xs = [x for x in range(80) if any(g[y][x] != '.' for y in range(70))]
    g = [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
    h, w = len(g), len(g[0])
    return [''.join(g[y][w - 1 - x] for y in range(h)) for x in range(w)]
def layers():
    ko = knocked()
    return [dict(l, not_='ko') for l in base()] + fx() + [dict(n='ko', g='root', x=0, y=61 - len(ko), rows=ko, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'tail': (0, -1)}, 'idle2': {'body': (0, 1), 'tail': (-1, -1), 'armF': (0, -1)}, 'idle3': {'armF': (0, -1), 'armB': (0, 1), 'tail': (-1, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (-2, -16), 'armB': (-3, -1)},
    'atk1': {'root': (5, 0), 'body': (1, 1), 'armF': (2, 4), 'armB': (3, 2)},
    'atk2': {'root': (6, 0), 'body': (1, 2), 'armF': (2, 10), 'armB': (3, 8)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 1), 'armB': (-1, 1)},
    'ko': {},
}
PARENT = {'tail': 'body', 'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
