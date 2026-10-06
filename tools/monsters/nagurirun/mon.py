# ナグリルー（かくとう × カンガルー）手打ち GBA風
from pix import outline
META = dict(id='nagurirun', name='ナグリルー', types=['fighting'], base='カンガルー', size='M')
PAL = {
    'k': '#101018', 'l': '#40201a',
    'A': '#f2ac62', 'B': '#c46a32', 'C': '#7c3820',      # 毛（赤茶）
    'E': '#f6e0b4', 'F': '#cca474',                      # はら・耳の 内がわ
    'R': '#f44a44', 'S': '#a4243a',                      # 拳闘の グローブ
    'G': '#c4c4d4', 'H': '#6c6c80',                      # 鉄の びょう・石
    'Y': '#ffe23a', 'y': '#d0821e', 'w': '#ffffff',
}
LIGHT = set('AERGYw')
KEEP_BLACK = set('wYy')
DK = {'A': 'B', 'B': 'C', 'E': 'F', 'R': 'S', 'G': 'H'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=40, H=30):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

HEAD = [
    "....AAAAAA..........",
    "..AABBBBBBAA........",
    ".ABBBBBBBBBBAA......",
    "ABBBBBBBBBBBBBAAA...",
    "ABBBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBkk",
    "ABBBBBBBBBBBBBBBBkkk",
    "BBBBBBBBBBBBBBBBBBC.",
    "BBBBBBBEEEEEEkkkkkk.",
    "CBBBBBEEEEEkwkwEEC..",
    ".CBBBBEEEEEEEEEEC...",
    "..CBBBBEEEEEEEFC....",
    "...CCBBBFFFFFCC.....",
    ".....CCCCCCC........",
]
HEAD_YELL = [
    "....AAAAAA..........",
    "..AABBBBBBAA........",
    ".ABBBBBBBBBBAA......",
    "ABBBBBBBBBBBBBAAA...",
    "ABBBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBkk",
    "ABBBBBBBBBBBBBBBBkkk",
    "BBBBBBBBBBBBBBBBBBC.",
    "BBBBBBBEEEkkkkkkkkk.",
    "CBBBBBEEEkwkkkkwkk..",
    ".CBBBBEEEkSSSSSSk...",
    "..CBBBBEEEkwkkwk....",
    "...CCBBBFFFkkkC.....",
    ".....CCCCCCC........",
]
# 目：ハイライト w ＋ 虹彩 2色（Y 明・y 暗）＋ たての ひとみ k。上を 古傷（E）が ななめに 走る
EYE = ['kkE....', 'kkkEkk.', 'kwYkYk.', '.kykyk.', '..kkE..']
EYE_ALT = {'blink': ['kkE....', 'kkkEkk.', 'BkkkkkB', '.BBBBB.', '..BBE..'], 'hit': ['..E....', '.kkEk..', 'kkBBkk.', '.BkkB..', '..BBE..'],
           'atk0|atk1|atk2': ['kkE....', 'kkkEkk.', 'kwwkYk.', '.kYkyk.', '..kkE..'], 'ko': ['..E....', 'k...k..', '.k.k...', '..k....', '.k.k...']}
EAR = [
    "A.......",
    "AA......",
    "ABA.....",
    "ABFA....",
    ".BFFA...",
    ".BFFFB..",
    ".CBFFBC.",
    "..CBFFBC",
    "...CBBBC",
    "....CCC.",
]
# 胴（デフォルメ：小さく 丸く）。はらの ふくろに お守りの 石
BODY = [
    "....AAAAAA......",
    "..AABBBBBBAA....",
    ".ABBBBBBBBEEA...",
    ".ABBBBBBBEEEEB..",
    "ABBBBBBBEEEEEEC.",
    "ABBBBBBBEEFFEEC.",
    "ABBBBBBEEEEEEEEC",
    "ABBBBBBEEEGGEEFC",
    "ABBBBBBEEGGGHEFC",
    "ABBBBBBEFFHHHFFC",
    "BBBBBBBEEEEEEFFC",
    "CBBBBBBCFEEEFFC.",
    ".CCBBBCCCFFFCC..",
    "...CCCCC........",
]
# 後ろ足（短く した ももと 大きな 足）
LEG = [
    "..AAAAAA..........",
    ".ABBBBBBA.........",
    "ABBBBBBBBA........",
    "ABBBBBBBBC........",
    "ABBBBBBBCC........",
    ".ABBBBBCC.........",
    "..ABBBC...........",
    "..ABBBC...........",
    "..ABBBBAAAAAAAA...",
    "..ABBBBBBBBBBBBBA.",
    "..CBBBBBBBBBBBBBBw",
    "...CCCCCCCCCCCCCCw",
]
TUFT = ['A..A..', 'AA.AA.', 'ABAABA', 'BBBBBC']
# 太い 尾（見せ所の ひとつ：地面を ささえて けりを 出す）
TAIL = [
    "....................AB",
    "..................ABBB",
    "...............AABBBBC",
    ".............ABBBBBBC.",
    "..........AABBBBBBCC..",
    "........ABBBBBBBCC....",
    "......ABBBBBBCC.......",
    "....ABBBBBCC..........",
    "..ABBBBCC.............",
    "ABBCC.................",
]
GLOVE = [
    "..RRRRR...",
    ".RwRRRRRS.",
    "RRRRRRRRSS",
    "RRRRRRRRSS",
    "RRRRRRRSSS",
    "SRRRRRSSSS",
    ".SSSSSSSS.",
    "..GHGHG...",
]
ARM = [
    "AAB......",
    "ABBC.....",
    ".ABBC....",
    "..ABBAAA.",
    "...ABBBBC",
    "....CCCC.",
]
ARM_PUNCH = [
    "AAAAAAAAAAAA",
    "ABBBBBBBBBBB",
    "BBBBBBBBBBBC",
    "CCCCCCCCCCC.",
]
ARMS = {
    'base': place([(outline(ARM), 0, 4), (outline(GLOVE), 8, 0)]),
    'punch': place([(outline(ARM_PUNCH), 0, 6), (outline(GLOVE), 12, 3)]),
}
IMPACT = [
    "....k.....",
    "...kYk..k.",
    "k.kYwYkkYk",
    "kYkwwwYYk.",
    ".kYwwwwYk.",
    "kYYwwwYkk.",
    ".kkYwYkYk.",
    "..kYk.k.k.",
    "...k......",
]
SWEAT = ['.k.', 'kwk', 'kGk', '.k.']

HX, HY = 28, 22     # 頭の 位置（頭は 元の 大きさ）
def base():
    return [
        dict(n='armB', g='armB', x=33, y=31, rows=dk(ARMS['base']), alt={'atk2': dk(ARMS['punch'])}),
        dict(n='earB', g='head', x=HX + 1, y=HY - 6, rows=outline(dk(EAR))),
        dict(n='tail', g='tail', x=4, y=44, rows=outline(TAIL)),
        dict(n='legB', g='legB', x=16, y=47, rows=outline(dk(LEG))),
        dict(n='body', g='body', x=24, y=33, rows=outline(BODY)),
        dict(n='legA', g='legA', x=21, y=47, rows=outline(LEG)),
        dict(n='tuft', g='head', x=HX + 3, y=HY - 2, rows=outline(TUFT)),
        dict(n='ear', g='head', x=HX - 2, y=HY - 5, rows=outline(EAR)),
        dict(n='head', g='head', x=HX, y=HY, rows=outline(HEAD), alt={'atk1|atk2|hit': outline(HEAD_YELL)}),
        dict(n='eye', g='head', x=HX + 9, y=HY + 2, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=30, y=33, rows=ARMS['base'], alt={'atk1': ARMS['punch']}),
    ]
def fx():
    return [dict(n='impact', g='root', x=58, y=35, rows=IMPACT, only='atk1')]
def layers():
    return base() + fx()

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'armF': (1, 0)}, 'idle2': {'body': (0, 1), 'armB': (0, 1)}, 'idle3': {'armF': (1, 0)},
    'blink': {},
    'walk0': {'legA': (2, -2), 'legB': (0, 0), 'body': (1, -1)}, 'walk1': {'body': (0, -2), 'legA': (0, -1), 'legB': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'armF': (-7, 1), 'armB': (-2, 0), 'tail': (1, 1), 'head': (-1, 0)},
    'atk1': {'root': (4, 0), 'body': (2, 0), 'armF': (0, 0), 'armB': (-3, 1)},
    'atk2': {'root': (5, 0), 'body': (2, 0), 'armF': (-6, 2), 'armB': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-3, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
