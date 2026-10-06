# ライエリマキ（でんき・ドラゴン × エリマキトカゲ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と えりまき、胴は 小さく、足は 短く 太く）
from pix import outline
META = dict(id='raierimaki', name='ライエリマキ', types=['elec', 'dragon'], base='エリマキトカゲ', size='M')
EYE_BOX = (43, 20, 10, 7)   # つり目（idle0）
PAL = {
    'k': '#101018', 'l': '#1c1c48',
    'A': '#82b4f4', 'B': '#4a72cc', 'C': '#283c84',      # うろこ（こん）
    'E': '#e6dcb8', 'F': '#a89a78',                      # はら
    'G': '#ece4d0', 'H': '#8a8078',                      # 骨の とげ・つの
    'W': '#b4f6ff', 'V': '#2cb8ea',                      # でんきの 膜
    'Y': '#fff04a', 'O': '#ffa424', 'w': '#ffffff',
}
LIGHT = set('AEGWYw')
KEEP_BLACK = set('wYO')
DK = {'A': 'B', 'B': 'C', 'E': 'F', 'G': 'H'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def place(parts, W=40, H=40):
    g = [['.'] * W for _ in range(H)]
    for rows, dx, dy in parts:
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': g[dy + j][dx + i] = c
    return [''.join(r) for r in g]

HEAD_T = [
    ".....AAAAAA.............",
    "...AABBBBBBAAA..........",
    "..ABBBBBBBBBBBAA........",
    ".ABBBBBBBBBBBBBBAA......",
    "ABBBBBBBBBBBBBBBBBAA....",
    "ABBBBBBBBBBBBBBBBBBBAA..",
    "ABBBBBBBBBBBBBBBBBBBBBA.",
    "ABBBBBBBBBBBBBBBBBBBBBBA",
    "ABBBBBBBBBBBBBBBBBBBBBBC",
]
HEAD_SHUT = [
    "CBBBBBBkkkkkkkkkkkkkkkkk",
    "CBBBBBkwkwkkwkkwkkwkkwC.",
    ".CBBBEEEEEEEEEEEEEEEEC..",
    "..CBBEEEEEEEEEEEEEEC....",
    "...CCFFFFFFFFFFFFCC.....",
    ".....CCCCCCCCCCCC.......",
]
HEAD_GAPE = [
    "CBBBBBBkwkwkkwkkwkkwkkwk",
    "CBBBBkkkkkkkkkkkkkkkkk..",
    "CBBBkOOOOOOOOOOOOk......",
    "CBBBkkwkkwkkwkkwkk......",
    ".CBBEEEEEEEEEEEEEC......",
    "..CCFFFFFFFFFFFCC.......",
    "....CCCCCCCCCCC.........",
]
# 目：爬虫類の つり目（A）。白目なし、黄（明）・だいだい（暗）の 虹彩いっぱいに 細い たての スリット。上まぶたは 太い 黒、下まぶたは 細い 紺の 線。うしろへ つり上がる
EYES = {
    'open':  ['kk........', '.kkkkkk...', '..kkYkYkk.', '..kYYkYYkk', '..kYOkOYk.', '...kOkOk..', '....CCC...'],
    'glow':  ['kk........', '.kkkkkk...', '..kkwkwkk.', '..kwYkYwkk', '..kYYkYYk.', '...kOkOk..', '....CCC...'],
    'blink': ['kk........', '.kkkkkk...', '..kkBBBkk.', '..kABBBBkk', '..kkkkkkk.', '...CCCCC..', '..........'],
    'hit':   ['kk........', '.kkkkkk...', '..kkkkkkk.', '..kkkkkkkk', '..kOYkYOk.', '...kkkkk..', '....CCC...'],
    'ko':    ['..........', '..........', '..k...k...', '...k.k....', '....k.....', '...k.k....', '..k...k...'],
}
def head(eye='open', gape=False):
    g = [list(r) for r in HEAD_T + (HEAD_GAPE if gape else HEAD_SHUT)]
    for j, r in enumerate(EYES[eye]):
        for i, c in enumerate(r):
            if c != '.': g[2 + j][9 + i] = c
    for (x, y) in ((6, 1), (7, 1), (3, 3), (2, 4)): g[y][x] = 'A'
    for (x, y) in ((3, 7), (4, 8), (17, 6), (18, 7), (19, 7)): g[y][x] = 'C'
    return outline([''.join(r) for r in g])
HORN = ['GG......', '.GGH....', '..GHHH..', '...HHHH.', '....HHH.']
# えりまき：骨の すじ（G/H）の あいだに でんきの 膜（W/V）、いなずまの もよう（Y）
FRILL = [
    "..................G.......",
    "..................GW......",
    "......G..........WHW......",
    ".......GW.......WWHW......",
    ".......WHW.....WWWHV......",
    "........WHWWWWWWYHV.......",
    "........WWHWWWYWWHV.......",
    ".G.......WWHWYWWWHV.......",
    "..GW.....WWWHWWWWHV.......",
    "..WHWW..WWWYWHWWWHV.......",
    "...WWHWWWWYWWWHWWHV.......",
    "....WWWHHWWYWWWHWHV.......",
    ".....WWWWHHHWWWWHHV.......",
    "......WWYWWWHHWWWHV.......",
    "GWWWWWWWWWWWWHHHHHV.......",
    "HHHHHHHHHHHHHHHHHHV.......",
    ".VWWYWWWWWWWVVHHVV........",
    "..VWWWYWWWVVHHVVV.........",
    "...VWWWWVHHHVVVV..........",
    "..HHHHHHHHVVVVV...........",
    ".HVWWWYWWVVVVHV...........",
    "....VWWWYWVVHHV...........",
    "......VWWVVHHVV...........",
    ".......VWVHHVV............",
    ".......VVHHV..............",
    "......HHV.................",
]
BODY = [
    "...................AABB..",
    ".................AABBBC..",
    "...............AABBBBC...",
    "............AAABBBBBBC...",
    ".........AAABBBBBBBBBCC..",
    "......AAABBBBBBBBBBBBBC..",
    "....AABBBBBBBBBBBBBBBEEC.",
    "...ABBBBBBBBBBBBBBBBEEEC.",
    "..ABBBBBBBBBBBBBBBEEEEFC.",
    ".ABBBBBBBBBBBBBBEEEEEFC..",
    ".ABBBBBBBBBBBEEEEEEFFC...",
    "ABBBBBBBBBEEEEEEEFFCC....",
    "ABBBBBBBEEEEEEFFFCC......",
    "CBBBBBBCFFFFFFFCC........",
    ".CCCCCCCCCCCCCC..........",
]
TAIL = [
    "..........AAAAAAAAAA",
    "......AAAABBBBBBBBBB",
    "..AAAABBBBBBBBBBBBBB",
    "AABBBBBBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBBCCCCCC",
    "CBBBBBCCCCCCCCCC....",
    ".CCCCC..............",
]
SPIKE = ['G..', 'GH.', '.GH', '.GHH', '.GHH']
BOLT = ['..YY', '.YY.', 'YYYY', '..Y.', '.Y..']
LEG = [
    "..AAAABBB...",
    ".ABBBBBBBC..",
    "ABBBBBBBBBC.",
    "ABBBBBBBBC..",
    ".ABBBBBBC...",
    "..ABBBBC....",
    "...ABBC.....",
    "..ABBC......",
    "..ABBBBBBC..",
    "..ABBBBBBBCw",
    "..CCCCCCCCC.",
]
ARM = [
    "ABBC.....",
    "ABBBC....",
    ".ABBBC...",
    "..ABBBBC.",
    "...ABBBBw",
    "....CC.w.",
    ".....w...",
]
ARM_STRIKE = ['ABBBBBBBBC..', 'ABBBBBBBBBBw', '.CCCCCCCCBCw', '.........w..']
LIGHTNING = [
    "..............kk.",
    "......kkk....kYYk",
    "kkk..kYYYk..kYwYk",
    "kwwkkYwwwYkkYwwk.",
    "kYwwwwwkwwwYwwYk.",
    "kYYwwwYkkYwwwYk..",
    ".kkYYYk..kYwYYk..",
    "...kkk...kYwwk...",
    ".........kYYk....",
    "..........kk.....",
]
SPARK = ['..k..', '.kYk.', 'kYwYk', '.kYk.', '..k..']

def base():
    return [
        dict(n='legB', g='legB', x=16, y=48, rows=outline(dk(LEG))),
        dict(n='armB', g='armB', x=44, y=37, rows=outline(dk(ARM)), alt={'atk1': outline(dk(ARM_STRIKE))}),
        dict(n='tail', g='tail', x=2, y=42, rows=outline(TAIL)),
        dict(n='bolt', g='tail', x=0, y=44, rows=outline(BOLT)),
        dict(n='sp0', g='body', x=20, y=37, rows=outline(SPIKE)),
        dict(n='sp1', g='body', x=24, y=34, rows=outline(SPIKE)),
        dict(n='frill', g='frill', x=16, y=6, rows=outline(FRILL), alt={'atk0|atk1': outline([r.replace('W', 'w').replace('V', 'W').replace('H', 'V') for r in FRILL])}),
        dict(n='body', g='body', x=17, y=33, rows=outline(BODY)),
        dict(n='legA', g='legA', x=24, y=48, rows=outline(LEG)),
        dict(n='horn', g='head', x=30, y=15, rows=outline(HORN)),
        dict(n='head', g='head', x=33, y=17, rows=head(), alt={'blink': head('blink'), 'hit': head('hit'), 'atk0': head('glow'), 'atk1|atk2': head('glow', True)}),
        dict(n='armF', g='armF', x=40, y=39, rows=outline(ARM), alt={'atk1': outline(ARM_STRIKE)}),
    ]
def fx():
    return [
        dict(n='zap', g='root', x=58, y=24, rows=LIGHTNING, only='atk1'),
        dict(n='sp1', g='root', x=62, y=18, rows=SPARK, only='atk2'),
        dict(n='sp2', g='root', x=68, y=24, rows=SPARK, only='atk2'),
        dict(n='spi', g='frill', x=19, y=4, rows=SPARK, only='idle1|atk0'),
        dict(n='spi2', g='frill', x=28, y=2, rows=SPARK, only='idle3|atk0'),
    ]
def layers():
    return base() + fx()

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'frill': (0, -1)}, 'idle3': {},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-2, 0), 'tail': (0, 1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-2, 0), 'legB': (2, -1), 'tail': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 1), 'frill': (-1, -2), 'tail': (1, -1)},
    'atk1': {'root': (3, 0), 'head': (1, 0)}, 'atk2': {'root': (4, 0), 'body': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'frill': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'frill': 'head', 'armF': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
