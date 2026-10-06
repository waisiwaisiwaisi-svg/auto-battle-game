# テッケンザル（かくとう・はがね × 大猿）手打ち GBA風
from pix import outline
META = dict(id='tekkenzaru', name='テッケンザル', types=['fighting', 'steel'], base='大猿（ゴリラ）', size='L')
PAL = {
    'k': '#101018', 'l': '#2e1a1c',
    'A': '#a8705a', 'B': '#6c4036', 'C': '#3c2224',      # 毛（赤黒）
    'D': '#b4a8a0', 'E': '#6e6260',                      # 顔の はだ
    'S': '#f2f6fa', 'T': '#a4b0c2', 'U': '#566276',      # はがね
    'R': '#ff3424', 'O': '#ffb22e', 'w': '#ffffff',
}
LIGHT = set('ADSOw')
KEEP_BLACK = set('wRO')
DK = {'A': 'B', 'B': 'C', 'D': 'E', 'S': 'T', 'T': 'U'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=44, H=44):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

# 胴：行ごとの はば（左右の 端）を 手で 指定。背中（左上）が 光、右下が 影。毛の すじは 手で 置く
SPANS = [(26, 34), (23, 37), (20, 39), (18, 41), (16, 42), (15, 43), (14, 43), (13, 44), (12, 44), (11, 44), (10, 44), (10, 44),
         (9, 43), (9, 43), (8, 42), (8, 42), (8, 41), (7, 41), (7, 40), (7, 40), (7, 39), (7, 39), (7, 38), (7, 38), (7, 37),
         (7, 37), (8, 36), (8, 36), (9, 35), (9, 34), (10, 33), (11, 32), (12, 30), (14, 28)]
STROKES = [(20, 4), (21, 5), (27, 3), (28, 4), (16, 9), (17, 10), (24, 8), (25, 9), (12, 14), (13, 15), (20, 13), (21, 14), (30, 10), (31, 11),
           (10, 20), (11, 21), (17, 19), (18, 20), (26, 17), (27, 18), (13, 26), (14, 27), (21, 24), (22, 25), (11, 31), (18, 29), (19, 30)]
# デフォルメ：胴は 小さく 起こした 形（頭の はばと ほぼ 同じ）。肩（右上）が 高く、背中は 丸く 下がる。行ごとの はばを 手で 指定
SPANS = [(10, 18), (7, 20), (5, 21), (4, 22), (3, 22), (2, 23), (1, 23), (1, 23), (1, 23), (1, 23), (1, 23), (1, 23),
         (1, 23), (1, 23), (1, 23), (1, 23), (1, 22), (1, 22), (1, 22), (2, 22), (2, 21), (3, 20), (5, 18)]
STROKES = [(9, 2), (10, 3), (14, 2), (15, 3), (6, 6), (7, 7), (12, 6), (13, 7), (4, 10), (5, 11), (10, 10), (11, 11), (16, 9), (17, 10),
           (4, 15), (5, 16), (10, 14), (11, 15), (15, 14), (16, 15), (7, 19), (8, 20), (13, 18), (14, 19)]
def body():
    W, H = 25, len(SPANS); g = [['.'] * W for _ in range(H)]
    for y, (a, b) in enumerate(SPANS):
        for x in range(a, b + 1):
            dl, dr = x - a, b - x
            c = 'B'
            if dl <= 1 or y <= 1 or (dl <= 2 and y <= 9): c = 'A'
            if dr <= 3 or y >= H - 4 or (y >= H - 7 and dr <= 6): c = 'C'
            g[y][x] = c
    for x, y in STROKES:
        if y >= H or x >= W: continue
        if g[y][x] == 'B': g[y][x] = 'C'
        elif g[y][x] == 'A': g[y][x] = 'B'
    return [''.join(r) for r in g]
BODY = body()
HEAD = [
    "....AAAAAA........",
    "..AABBBBBBAA......",
    ".ABBBBBBBBBBA.....",
    "ABBBBBBBBBBBBA....",
    "ABBBBSSSSSSSSTU...",
    "ABBBBTTkTTTTkTU...",
    "BBBBEDDDDDDDDDDE..",
    "BBBBEDDDDDDDDDDDE.",
    "BBBBEDDDDDDDEDEDE.",
    "BBBBEDDDDDDDDDDDE.",
    "BBBBEDkkkkkkkkkkk.",
    "BBBBEDkwkkkkkkwk..",
    ".BBBBEDwDDDDDDwE..",
    ".CBBBEEDDDDDDDE...",
    "..CCBBBEEEEEEE....",
    "....CCCCCC........",
]
HEAD_ROAR = [
    "....AAAAAA........",
    "..AABBBBBBAA......",
    ".ABBBBBBBBBBA.....",
    "ABBBBBBBBBBBBA....",
    "ABBBBSSSSSSSSTU...",
    "ABBBBTTkTTTTkTU...",
    "BBBBEDDDDDDDDDDE..",
    "BBBBEDDDDDDDDDDDE.",
    "BBBBEDDDDDDDEDEDE.",
    "BBBBEDkkkkkkkkkkk.",
    "BBBBEkwkwkkkkwkwk.",
    "BBBBEkRRRRRRRRRk..",
    ".BBBEkwkkkkkkwwk..",
    ".CBBBEwDDDDDDwE...",
    "..CCBBBEEEEEEE....",
    "....CCCCCC........",
]
# 目：ハイライト w ＋ 虹彩 2色（O 明・R 暗）＋ たての ひとみ k、まゆと 下まぶたで かこむ
EYE = ['kkkkkk', 'kwOkOk', '.kRkRk', '..kkk.']
EYE_ALT = {'blink': ['kkkkkk', 'Ekkkkk', '.EEEEE', '..EEE.'], 'hit': ['.kk.kk', 'DDkkDD', '.kkDkk', '..DDD.'],
           'atk0|atk1|atk2': ['kkkkkk', 'kwwkOk', '.kOkRk', '..kkk.'], 'ko': ['.k.k..', '..k...', '.k.k..', '......']}
ARM = [
    "..AAAAAAA....",
    ".AABBBBBBAA..",
    "AABBBBBBBBBC.",
    "ABBBBBBBBBBCC",
    "ABBBCBBBBBBCC",
    "ABBBBCBBBBCCC",
    "ABBBBBBBBBCCC",
    ".ABBBBBBCBCCC",
    ".ABBBBBBBCCC.",
    ".ABBBCBBBBCC.",
    ".ABBBBCBBBCC.",
    "..ABBBBBBBCC.",
    "..ABBBBBBCCC.",
    "..ABBBCBBBCC.",
    "..ABBBBBBBCC.",
    "..ABBBBBBCC..",
    "..ABBBBCBCC..",
    "..ABBBBBBCC..",
    "..ABBBBBCCC..",
    "..ABBBBBCC...",
    "..ABBBBBCC...",
]
GAUNT = [
    "..SSSSSSSSSSSS....",
    ".STTTTTTTTTTTTU...",
    ".STkTTTTTTTTkTU...",
    ".STTTTTTTTTTTTU...",
    ".SUUUUUUUUUUUUU...",
    ".STTTTTTTTTTTTU...",
    "SSTTTTTTTTTTTTUU..",
    "SSSSSSSSSSSSSSSSU.",
    "STTkTTTkTTTkTTTTUU",
    "STTTTTTTTTTTTTTTUU",
    "STTkTTTkTTTkTTTTUU",
    ".UUUUUUUUUUUUUUUU.",
]
# 鎖：手描きの 輪（たて・よこ）を 交互に つなぐ
LINK_V = ['.SS.', 'S..T', 'S..U', '.UU.']
LINK_H = ['.ST.', '.TU.']
def chain(pts):
    parts = []
    for i, (x, y) in enumerate(pts): parts.append((LINK_V if i % 2 == 0 else LINK_H, x, y))
    return parts
ARM = [ARM[i] for i in (0, 1, 2, 3, 5, 7, 9, 12, 15, 18, 20)]   # 腕を 短く（デフォルメ）
ARMS = {'base': place([(outline(ARM), 1, 0), (outline(GAUNT), 0, 11)], H=26)}
# ため：こぶしを 頭の 上へ
ARM_UP = [
    "............AAAA",
    "..........AABBBB",
    "........AABBBBBC",
    "......AABBBBBBC.",
    "....AABBBBBBBC..",
    "..AABBBBBBBBC...",
    ".ABBBBBBBBCC....",
    "ABBBBBBBCC......",
    "ABBBBBCC........",
    "BBBCCC..........",
]
ARMS['up'] = place([(outline([r[::-1] for r in ARM_UP]), 2, 11), (outline(GAUNT), 0, 0)], W=24, H=24)   # こぶしを 頭の うしろへ ふりかぶる
# 決め：こぶしが 鎖ごと 前へ とんで いく（ロケットの ような 鉄拳）
GAUNT_FWD = [
    "...SSSSSSSSSSSSS.",
    "..STTTTTTTTTTTTkS",
    ".STTkTTTTTTTkTTTS",
    "SSUUUUUUUUUUUTkTS",
    "SSTTTTTTTTTTTTTTS",
    "STTkTTTTTTTkTTkTU",
    ".UUUUUUUUUUUUUUU.",
]
ARM_FWD = [
    "AAAAAAAAAAAA",
    "ABBBBBBBBBBB",
    "BBBBBBBBBBBC",
    "CCCCCCCCCCC.",
]
ARMS['shot'] = place([(outline(ARM_FWD), 0, 6)] + [(outline(LINK_H if i % 2 else ['SS', 'TU']), 13 + i * 3, 7) for i in range(3)] + [(outline(GAUNT_FWD), 21, 3)], W=56, H=24)
ARMS['back'] = place([(outline(ARM_FWD), 0, 6)] + [(outline(LINK_H if i % 2 else ['SS', 'TU']), 13 + i * 3, 7) for i in range(1)] + [(outline(GAUNT_FWD), 15, 3)], W=56, H=24)
LEG0 = [
    "..AAAAAAAA....",
    ".AABBBBBBBBA..",
    "ABBBBBBBBBBBC.",
    "ABBBCBBBBBBBC.",
    "ABBBBBBBBBBCC.",
    ".ABBBBBBBBBCC.",
    "..ABBBBBBBCC..",
    "..ABBBBCBBC...",
    "...ABBBBBBC...",
    "...ABBBBBCC...",
    "...ABBBBBC....",
    "..AABBBBBC....",
    "..ABBBBBBC....",
    ".ABBBBBBBCC...",
    ".DDDDDDDDDDE..",
    "DDDEDDEDDDDEE.",
    "EEEEEEEEEEEEE.",
]
BANG = [
    "...k....k...",
    "..kOk..kOk..",
    "k.kwOkkOwk.k",
    "kOkwwwwwwkOk",
    ".kwwwwwwwwk.",
    "kOOwwwwwwOOk",
    ".kkOwwwwOkk.",
    "..kOkkkkOk..",
    "...k....k...",
]

# 足：短く 太い（デフォルメ）。ももは 胴の 下に 3ドット 食いこむ
LEG = [
    "..AAAAAAA..",
    ".ABBBBBBBA.",
    "ABBBBBBBBBC",
    "ABBBCBBBBBC",
    "ABBBBBBBBCC",
    ".ABBBBBBBC.",
    ".ABBBBCBBC.",
    ".ABBBBBBBC.",
    ".ABBBBBBCC.",
    "DDDDDDDDDDE",
    "DDEDDEDDDEE",
    "EEEEEEEEEEE",
]
def base():
    return [
        dict(n='legB', g='legB', x=13, y=47, rows=outline(dk(LEG))),
        dict(n='armB', g='armB', x=39, y=36, rows=dk(ARMS['base'])),
        dict(n='body', g='body', x=14, y=28, rows=outline(BODY)),
        dict(n='chain', g='body', x=14, y=28, rows=place(chain([(3, 19), (4, 17), (5, 15), (7, 13), (8, 11), (10, 9), (12, 7), (14, 5), (17, 3)]), W=40, H=30)),
        dict(n='legA', g='legA', x=20, y=47, rows=outline(LEG)),
        dict(n='armF', g='armF', x=31, y=36, rows=ARMS['base'], not_='atk0|atk1|atk2'),
        dict(n='head', g='head', x=29, y=18, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_ROAR)}),
        dict(n='eye', g='head', x=35, y=25, rows=EYE, alt=EYE_ALT),
    ]
def fx():
    return [dict(n='bang', g='root', x=68, y=33, rows=BANG, only='atk1')]
def knocked():
    g = [['.'] * 80 for _ in range(70)]
    for l in base():
        rows = l['rows']
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.' and 0 <= l['y'] + j < 70 and 0 <= l['x'] + i < 80: g[l['y'] + j][l['x'] + i] = c
    ys = [y for y in range(70) if any(c != '.' for c in g[y])]; xs = [x for x in range(80) if any(g[y][x] != '.' for y in range(70))]
    return [r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]
def layers():
    L = base()
    i = [l['n'] for l in L].index('head')
    up = dict(n='armUp', g='armF', x=14, y=14, rows=ARMS['up'], only='atk0')
    shot = dict(n='armShot', g='armF', x=31, y=27, rows=ARMS['shot'], alt={'atk2': ARMS['back']}, only='atk1|atk2')
    return L[:i] + [up] + L[i:] + [shot] + fx()

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (0, -1)}, 'idle2': {'body': (0, 1), 'armF': (0, -1), 'head': (0, 1)}, 'idle3': {'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'armB': (-2, 0), 'armF': (1, -2)}, 'walk1': {'body': (0, -1), 'armF': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'armF': (-1, 0), 'armB': (1, -2)}, 'walk3': {'body': (0, -1), 'armB': (0, -1)},
    'atk0': {'body': (-2, -1), 'head': (-1, -1), 'armB': (-1, 0)},
    'atk1': {'root': (2, 0), 'body': (1, 1), 'armF': (0, 5), 'head': (1, 0)},
    'atk2': {'root': (3, 0), 'body': (1, 1), 'armF': (0, 5), 'head': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'armF': (-2, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
