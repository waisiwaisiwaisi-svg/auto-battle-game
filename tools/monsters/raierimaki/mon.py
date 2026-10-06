# ライエリマキ（でんき・ドラゴン × エリマキトカゲ）手打ち GBA風
from pix import outline
META = dict(id='raierimaki', name='ライエリマキ', types=['elec', 'dragon'], base='エリマキトカゲ', size='M')
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

HEAD = [
    "....AAAAA..........",
    "..AABBBBBAAA.......",
    ".ABBBBBBBBBBAA.....",
    "ABBBBBBBBBBBBBAA...",
    "ABBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBA",
    "ABBBBBBBBBBBBBBBBBC",
    "CBBBBBkkkkkkkkkkkkk",
    ".CBBBkwkwkkwkkwkwC.",
    "..CBBEEEEEEEEEEEC..",
    "...CCFFFFFFFFFCC...",
    ".....CCCCCCCCC.....",
]
HEAD_OPEN = [
    "....AAAAA..........",
    "..AABBBBBAAA.......",
    ".ABBBBBBBBBBAA.....",
    "ABBBBBBBBBBBBBAA...",
    "ABBBBBBBBBBBBBBBAA.",
    "ABBBBBBBBBBBBBBBBBA",
    "CBBBBBBBBBBBBBBBBBC",
    ".CBBBBkwkwkkwkkwkwk",
    "..CBkkkkkkkkkkkkk..",
    "..CBkOOOOOOOOk.....",
    "..CBBkkwkkwkkwk....",
    "...CBBEEEEEEEEEC...",
    "....CCFFFFFFFCC....",
    "......CCCCCCC......",
]
EYE = ['kkkkk.', 'kYYYkk', 'kYkYYk', '.kkkk.']
EYE_ALT = {'blink': ['kkkkk.', 'kkkkkk', '.CCCC.', '......'], 'hit': ['.kkk..', 'kYkYk.', 'kkYkk.', '.kkk..'],
           'atk0|atk1|atk2': ['kkkkk.', 'kwwYkk', 'kwkwYk', '.kkkk.'], 'ko': ['k...k.', '.k.k..', '..k...', '.k.k..']}
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
    "ABBBBBBBBBC.",
    "ABBBBBBBBC..",
    ".ABBBBBBC...",
    "..ABBBBC....",
    "...ABBBC....",
    "....ABBC....",
    "....ABBC....",
    "...ABBC.....",
    "...ABC......",
    "..ABBC......",
    "..ABC.......",
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
        dict(n='legB', g='legB', x=17, y=38, rows=outline(dk(LEG))),
        dict(n='armB', g='armB', x=46, y=31, rows=outline(dk(ARM)), alt={'atk1': outline(dk(ARM_STRIKE))}),
        dict(n='tail', g='tail', x=6, y=35, rows=outline(TAIL)),
        dict(n='bolt', g='tail', x=3, y=38, rows=outline(BOLT)),
        dict(n='sp0', g='body', x=20, y=26, rows=outline(SPIKE)),
        dict(n='sp1', g='body', x=24, y=24, rows=outline(SPIKE)),
        dict(n='sp2', g='body', x=28, y=22, rows=outline(SPIKE)),
        dict(n='sp3', g='body', x=32, y=21, rows=outline(SPIKE)),
        dict(n='frill', g='frill', x=24, y=4, rows=outline(FRILL), alt={'atk0|atk1': outline([r.replace('W', 'w').replace('V', 'W').replace('H', 'V') for r in FRILL])}),
        dict(n='body', g='body', x=19, y=24, rows=outline(BODY)),
        dict(n='legA', g='legA', x=25, y=40, rows=outline(LEG)),
        dict(n='horn', g='head', x=36, y=12, rows=outline(HORN)),
        dict(n='head', g='head', x=40, y=14, rows=outline(HEAD), alt={'atk1|atk2': outline(HEAD_OPEN)}),
        dict(n='eye', g='head', x=48, y=17, rows=EYE, alt=EYE_ALT),
        dict(n='armF', g='armF', x=42, y=33, rows=outline(ARM), alt={'atk1': outline(ARM_STRIKE)}),
    ]
def fx():
    return [
        dict(n='zap', g='root', x=56, y=17, rows=LIGHTNING, only='atk1'),
        dict(n='sp1', g='root', x=62, y=14, rows=SPARK, only='atk2'),
        dict(n='sp2', g='root', x=68, y=24, rows=SPARK, only='atk2'),
        dict(n='spi', g='frill', x=27, y=2, rows=SPARK, only='idle1|atk0'),
        dict(n='spi2', g='frill', x=36, y=0, rows=SPARK, only='idle3|atk0'),
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
