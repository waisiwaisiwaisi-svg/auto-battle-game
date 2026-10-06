# ユキオニ（こおり・かくとう × イエティ）手打ち GBA風
from pix import outline, grid, poly, rows_of
META = dict(id='yukioni', name='ユキオニ', types=['ice', 'fighting'], base='イエティ', size='L')
PAL = {
    'k': '#101018', 'l': '#26304e',
    'A': '#f4f8ff', 'B': '#aebfe0', 'C': '#5e6fa4',      # 毛皮
    'D': '#4c5896', 'E': '#2c3266',                      # 鬼の はだ（顔・むね）
    'I': '#e4ffff', 'J': '#86dcf2', 'K': '#3a8ec6',      # 氷
    'R': '#ff3c3c', 'O': '#ffc23a', 'w': '#ffffff',
}
LIGHT = set('AIw')
KEEP_BLACK = set('wRO')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'I': 'J', 'J': 'K'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]

# ---- 毛の かたまり：あたりは 多角形、陰影は 左上から、房と 毛すじは 手で 置く ----
# 房（ふさ）：とがった 毛先。u=上 l=左 d=下 r=右（根元 3ドット → 先 1ドット）
TUFT = {'u': ([(0, 0), (1, 0), (2, 0), (0, -1), (1, -1), (0, -2), (-1, -3)], 'A'),
        'l': ([(0, 0), (0, 1), (0, 2), (-1, 0), (-1, 1), (-2, 0), (-3, -1)], 'A'),
        'd': ([(0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2), (2, 3)], 'C'),
        'r': ([(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2), (3, 3)], 'C')}
def fur(W, H, pts, tufts=(), strands=(), shadow=1.0):
    g = grid(W, H); poly(g, pts, 'B')
    def at(x, y): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
    def near(x, y, dirs, n): return any(at(x + dx * s, y + dy * s) == '.' for dx, dy in dirs for s in range(1, n + 1))
    o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'B': continue
            if near(x, y, ((0, -1), (-1, 0)), 2): o[y][x] = 'A'
            if near(x, y, ((0, 1), (1, 0)), 3) or near(x, y, ((1, 1),), 3): o[y][x] = 'C'
            # 右下ほど 影（光は 左上）。さかいは 手で 打った 毛すじで ぼかす
            if o[y][x] == 'B' and x / W * .55 + y / H + (.05 if (x + 2 * y) % 5 < 2 else 0) > shadow: o[y][x] = 'C'
    for x, y, d in tufts:
        pts_, c = TUFT[d]
        for dx, dy in pts_:
            X, Y = x + dx, y + dy
            if 0 <= X < W and 0 <= Y < H: o[Y][X] = c
    for x, y in strands:   # 毛すじ：毛の 房の さかい（影＋その 上に 光）
        for dx, dy, c in ((0, 0, 'C'), (1, 1, 'C'), (2, 1, 'C'), (0, -1, 'A'), (1, 0, 'A')):
            X, Y = x + dx, y + dy
            if 0 <= X < W and 0 <= Y < H and o[Y][X] in 'AB': o[Y][X] = c
    return rows_of(o)

# 胴：肩が いちばん 高く（前の 上）、背中は 後ろへ 下がる 前かがみ
BODY = fur(44, 44, [(8, 32), (6, 22), (9, 12), (15, 4), (23, 0), (32, 0), (38, 4), (41, 12), (41, 24), (36, 34), (26, 40), (12, 40)],
           tufts=[(11, 9, 'u'), (16, 5, 'u'), (22, 1, 'u'), (28, 0, 'u'), (34, 1, 'u'), (8, 15, 'l'), (6, 21, 'l'), (6, 27, 'l'), (8, 32, 'l'),
                  (12, 40, 'd'), (17, 40, 'd'), (23, 40, 'd'), (29, 37, 'd'), (34, 34, 'd')],
           strands=[(16, 10), (23, 6), (30, 6), (12, 17), (19, 15), (26, 13), (33, 12), (12, 25), (18, 23), (25, 21), (14, 32), (20, 31)], shadow=.9)
# 頭：毛の ずきんに あい色の 鬼の 顔。せり出した まゆ、赤く 光る 目、下あごから 上向きの きば
HEAD = [
    ".....AAAAAAA..........",
    "...AAAABBBBBAA........",
    "..AABBBBBBBBBBA.......",
    ".AABBBBBBBBBBBBA......",
    "AABBBBBBBBBBBBBBA.....",
    "ABBBBBBBBBBBBBBBBA....",
    "ABBBBBBBBBEEEEEEEEE...",
    "ABBBBBBBBEEEEEEEEEEEE.",
    "BBBBBBBBEDDDDDDDDDEEE.",
    "BBBBBBBEDDDDDDDDDDD...",
    "BBBBBBBEDDDDDDDDDDDD..",
    "BBBBBBBEDDDDDDDDDDDDD.",
    "BBBBBBEDDDDDDDDDDDDDDD",
    "CBBBBBEDDDDDDDDDDDDDDD",
    ".CBBBBBEDDDDDDDDDDDDDE",
    "..CBBBBEDDDDDDDDDDDDE.",
    "...CBBBBEEEEEEEEEEEE..",
    "....CCBBBCC...........",
]
_ = "......................"
def face(eye, mouth):
    return [_] * 8 + [eye[0], eye[1], eye[2], "..................kk.."] + mouth
EYE = ["..........kkkkkk......", "..........kRRROwk.....", "...........kRkkk......"]
MOUTH = ["...........w.....w....", "..........kwkkkkkkwkkk", "...........kEEEEEEEEk.", _]
ROAR = ["..........kkkkkkkkkkkk", "..........kwkwkkkwkwkk", "..........kRRRRRRRRRk.", "...........kwkkkkkwk.."]
FACE = face(EYE, MOUTH)
FACE_ALT = {
    'blink': face(["..........kkkkkk......", "..........EEEEEEE.....", _], MOUTH),
    'atk0|atk1|atk2': face(["..........kkkkkk......", "..........kOwwwwk.....", "...........kOkkk......"], ROAR),
    'hit': face(["..........k.kk.k......", "..........kRkkRkk.....", "...........kkRkk......"], ROAR),
    'ko': face(["..........k.k.........", "...........k..........", "..........k.k........."], [_, "..........kwkkkkkkwkkk", _, _]),
}
# つららの 角（前へ 反る）
HORN = ['.....I', '....IJ', '....IJ', '...IJK', '...IJK', '..IIJK', '..IJJK', '.IIJK.', '.IJJK.', 'IIJKK.', 'IJJK..']
HORN_S = ['...I', '..IJ', '..IJ', '.IJK', '.IJK', 'IIJK', 'IJK.']
# 氷の こぶし（ぎざぎざの 結晶）
FIST = [
    ".....I...I......",
    "....IIJ.IJ..I...",
    "..IIIJJIJJJIJ...",
    ".IIIJJJJJJJJJJ..",
    "IIIJJJJIJJJJJJK.",
    ".IJJJIJJIJJJJJKK",
    "IIJJJJJJJIJJJKK.",
    ".IJJJJJJJJIJJKKK",
    "IIJJJJIJJJJJKKK.",
    ".IJJJJJIJJJKKKK.",
    "..JJJJJJJJKKKK..",
    "..JKKJKKJKKKK...",
    "...K..K..K......",
]
# 長い 腕：肩が 太く、手首で 毛が はねる
ARM = fur(16, 26, [(0, 0), (11, 0), (14, 6), (13, 14), (11, 20), (15, 25), (1, 25), (3, 20), (1, 12)],
          tufts=[(1, 6, 'l'), (1, 13, 'l'), (2, 22, 'l'), (13, 9, 'r'), (12, 16, 'r'), (14, 22, 'r')],
          strands=[(5, 4), (8, 9), (5, 13), (7, 18)], shadow=1.05)
ARM_UP = fur(16, 26, [(6, 0), (15, 0), (15, 8), (13, 18), (11, 25), (1, 25), (3, 12)],
             tufts=[(3, 10, 'l'), (2, 17, 'l'), (14, 6, 'r'), (13, 14, 'r')],
             strands=[(8, 5), (10, 12), (6, 17)])
ARM_SLAM = fur(26, 14, [(0, 0), (10, 1), (25, 4), (25, 13), (12, 13), (1, 11)],
               tufts=[(6, 0, 'u'), (13, 1, 'u'), (19, 3, 'u'), (6, 12, 'd'), (12, 13, 'd'), (18, 13, 'd')],
               strands=[(7, 5), (14, 6), (20, 8)])
# 太く 短い 足：毛の すその 下に あい色の 足と 白い 爪
LEG = [
    "AABBBBBBBBC..",
    "ABBBBBBBBBCC.",
    "ABBCBBBBBBCC.",
    "ABBBCBBBBCCC.",
    ".ABBBBBBBCC..",
    "..ABBBBCBCC..",
    "..ABCBBCCC...",
    "..DDDDDDDDE..",
    ".DDDDDDDDDDE.",
    "DDDDDDDDDDDEw",
    "EEwEEwEEEEEE.",
]
SHARDS = [
    "....k.......k....",
    "...kIk.....kJk...",
    "..kIJk.k..kIJJk..",
    "..kIJkkIk.kIJKk..",
    ".kIJJkIJk.kIJKk.k",
    ".kIJKkIJKkIJJKkkJ",
    "kIJJKkIJKkIJKKkIJ",
]
SNOW = ['.k.', 'kAk', '.k.']

def base():
    return [
        dict(n='armB', g='armB', x=31, y=25, rows=outline(dk(ARM)), not_='atk0|atk1|atk2'),
        dict(n='fistB', g='armB', x=29, y=47, rows=outline(dk(FIST)), not_='atk0|atk1|atk2'),
        dict(n='legB', g='legB', x=10, y=49, rows=outline(dk(LEG))),
        dict(n='hornB', g='head', x=40, y=5, rows=outline(dk(HORN_S))),
        dict(n='body', g='body', x=2, y=8, rows=outline(BODY)),
        dict(n='legA', g='legA', x=20, y=49, rows=outline(LEG)),
        dict(n='armF', g='armF', x=38, y=24, rows=outline(ARM), not_='atk0|atk1|atk2'),
        dict(n='fistF', g='armF', x=41, y=47, rows=outline(FIST), not_='atk0|atk1|atk2'),
        dict(n='armS', g='armF', x=36, y=26, rows=outline(ARM_SLAM), only='atk1|atk2'),
        dict(n='fistS', g='armF', x=56, y=34, rows=outline(FIST), only='atk1|atk2'),
        dict(n='horn', g='head', x=46, y=1, rows=outline(HORN)),
        dict(n='head', g='head', x=38, y=12, rows=outline(HEAD)),
        dict(n='face', g='head', x=39, y=13, rows=FACE, alt=FACE_ALT),
        dict(n='armU', g='armF', x=26, y=0, rows=outline(ARM_UP), only='atk0'),
        dict(n='fistU', g='armF', x=28, y=-10, rows=outline(FIST), only='atk0'),
    ]
def fx():
    return [
        dict(n='shards', g='root', x=56, y=53, rows=SHARDS, only='atk1|atk2'),
        dict(n='snow1', g='root', x=6, y=8, rows=SNOW, only='idle1|idle2'),
        dict(n='snow2', g='root', x=58, y=6, rows=SNOW, only='idle2|idle3'),
        dict(n='snow3', g='root', x=4, y=30, rows=SNOW, only='idle3|idle0'),
    ]
def knocked():
    g = [['.'] * 90 for _ in range(80)]
    for l in base():
        if l.get('only'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if 'ko' in k.split('|'): rows = v
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[l['y'] + j + 10][l['x'] + i] = c
    ys = [y for y in range(80) if any(c != '.' for c in g[y])]; xs = [x for x in range(90) if any(g[y][x] != '.' for y in range(80))]
    g = [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
    h, w = len(g), len(g[0])
    return [''.join(g[y][w - 1 - x] for y in range(h)) for x in range(w)]
def layers():
    ko = knocked()
    return [dict(l, not_=(l.get('not_', '') + '|ko').strip('|')) for l in base()] + fx() + [dict(n='ko', g='root', x=0, y=61 - len(ko), rows=ko, only='ko')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (0, 0)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'body': (0, 0), 'head': (0, -1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'armF': (-1, -1), 'armB': (1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'armF': (1, 0), 'armB': (-1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (0, 2)},
    'atk1': {'root': (2, 0), 'body': (1, 2), 'head': (1, 1)},
    'atk2': {'root': (3, 0), 'body': (1, 3), 'head': (1, 2), 'armF': (0, 2)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 0), 'armB': (-1, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
