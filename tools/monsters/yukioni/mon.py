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

# 胴（デフォルメ）：小さく 丸い 毛の かたまり。肩が いちばん 高い 前かがみ
BODY = fur(32, 23, [(5, 19), (2, 12), (4, 6), (10, 1), (18, 0), (25, 1), (30, 5), (31, 12), (28, 18), (20, 22), (9, 22)],
           tufts=[(8, 5, 'u'), (13, 2, 'u'), (19, 0, 'u'), (25, 1, 'u'), (4, 10, 'l'), (3, 15, 'l'), (5, 20, 'l'),
                  (9, 22, 'd'), (15, 22, 'd'), (21, 21, 'd')],
           strands=[(10, 6), (17, 4), (24, 5), (8, 12), (15, 10), (22, 11), (11, 16), (18, 16)], shadow=.95)
# 頭：毛の ずきんに あい色の 鬼の 顔（頭は 元の 大きさの まま）。せり出した まゆ、赤く 光る 目、下あごから 上向きの きば
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
    return [_] * 7 + [eye[0], eye[1], eye[2], eye[3], "..................kk.."] + mouth
# 目：まゆの 線（前へ 下がる つり目）＋ ハイライト w ＋ 虹彩 2色（O 明・R 暗）＋ たての ひとみ k
EYE = ["..........kk..........", "...........kkkkk......", "..........kwOOkOk.....", "...........kRRkRk....."]
MOUTH = ["...........w.....w....", "..........kwkkkkkkwkkk", "...........kEEEEEEEEk.", _]
ROAR = ["..........kkkkkkkkkkkk", "..........kwkwkkkwkwkk", "..........kRRRRRRRRRk.", "...........kwkkkkkwk.."]
FACE = face(EYE, MOUTH)
FACE_ALT = {
    'blink': face(["..........kk..........", "...........kkkkk......", "..........EkkkkkE.....", "..........DDDDDDD....."], MOUTH),
    'atk0|atk1|atk2': face(["..........kk..........", "...........kkkkkk.....", "..........kwwOkOOk....", "...........kOOkRRk...."], ROAR),
    'hit': face(["..........kk..........", "...........kk..kk.....", "............kkkk......", "...........kk..kk....."], ROAR),
    'ko': face(["..........kk..........", "...........k.k........", "............k.........", "...........k.k........"], [_, "..........kwkkkkkkwkkk", _, _]),
}
# つららの 角（前へ 反る）
HORN = ['.....I', '....IJ', '....IJ', '...IJK', '...IJK', '..IIJK', '..IJJK', '.IIJK.', '.IJJK.', 'IIJKK.', 'IJJK..']
HORN_S = ['...I', '..IJ', '..IJ', '.IJK', '.IJK', 'IIJK', 'IJK.']
# 氷の こぶし（ぎざぎざの 結晶）：見せ所 なので 大きい まま
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
# 腕：短く 太く（肩は 胴の 中へ 食いこむ）
ARM = fur(15, 15, [(0, 0), (8, 0), (13, 7), (15, 14), (6, 14), (1, 7)],
          tufts=[(2, 7, 'l'), (5, 12, 'l'), (12, 8, 'r')], strands=[(5, 4), (8, 8)], shadow=1.1)
ARM_UP = fur(12, 18, [(2, 0), (12, 0), (12, 7), (11, 17), (1, 17), (1, 8)],
             tufts=[(2, 8, 'l'), (2, 13, 'l'), (11, 5, 'r')], strands=[(6, 5), (7, 11)])
ARM_SLAM = fur(22, 17, [(0, 0), (9, 0), (17, 6), (21, 12), (16, 16), (11, 13), (1, 8)],
               tufts=[(6, 0, 'u'), (12, 3, 'u'), (4, 9, 'd'), (11, 13, 'd')],
               strands=[(6, 4), (12, 8)])
# 太く 短い 足：毛の すその 下に あい色の 足と 白い 爪
LEG = [
    "ABBBBBBBBBC.",
    "ABBCBBBBBCC.",
    ".ABBBBCBCC..",
    ".ABBCBBCCC..",
    ".DDDDDDDDDE.",
    "DDDDDDDDDDEw",
    "EEwEEwEEEEE.",
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
HX, HY = 36, 15     # 頭の 位置
def base():
    A = 'atk0|atk1|atk2'
    return [
        dict(n='armB', g='armB', x=27, y=33, rows=outline(dk(ARM)), not_=A),
        dict(n='fistB', g='armB', x=34, y=45, rows=outline(dk(FIST)), not_=A),
        dict(n='legB', g='legB', x=11, y=52, rows=outline(dk(LEG))),
        dict(n='legA', g='legA', x=22, y=52, rows=outline(LEG)),
        dict(n='hornB', g='head', x=HX + 2, y=HY - 7, rows=outline(dk(HORN_S))),
        dict(n='body', g='body', x=8, y=28, rows=outline(BODY)),
        dict(n='horn', g='head', x=HX + 8, y=HY - 11, rows=outline(HORN)),
        dict(n='head', g='head', x=HX, y=HY, rows=outline(HEAD)),
        dict(n='face', g='head', x=HX + 1, y=HY + 1, rows=FACE, alt=FACE_ALT),
        dict(n='armF', g='armF', x=33, y=32, rows=outline(ARM), not_=A),
        dict(n='fistF', g='armF', x=41, y=45, rows=outline(FIST), not_=A),
        dict(n='armS', g='armF', x=32, y=32, rows=outline(ARM_SLAM), only='atk1|atk2'),
        dict(n='fistS', g='armF', x=47, y=46, rows=outline(FIST), only='atk1|atk2'),
        dict(n='armU', g='armF', x=27, y=19, rows=outline(ARM_UP), only='atk0'),
        dict(n='fistU', g='armF', x=24, y=7, rows=outline(FIST), only='atk0'),
    ]
def fx():
    return [
        dict(n='shards', g='root', x=60, y=53, rows=SHARDS, only='atk1|atk2'),
        dict(n='snow1', g='root', x=6, y=22, rows=SNOW, only='idle1|idle2'),
        dict(n='snow2', g='root', x=60, y=12, rows=SNOW, only='idle2|idle3'),
        dict(n='snow3', g='root', x=4, y=40, rows=SNOW, only='idle3|idle0'),
    ]
def layers():
    return base() + fx()

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (0, 0)}, 'idle2': {'body': (0, 1), 'head': (0, 0)}, 'idle3': {'body': (0, 0), 'head': (0, -1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'armF': (-1, -1), 'armB': (1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'armF': (1, 0), 'armB': (-1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (0, 2)},
    'atk1': {'root': (2, 0), 'body': (1, 2), 'head': (1, 1)},
    'atk2': {'root': (3, 0), 'body': (1, 3), 'head': (1, 2), 'armF': (0, 2)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-2, 0), 'armB': (-1, 0)},
    'ko': {'_flip': True, 'armF': (-4, -3)},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
