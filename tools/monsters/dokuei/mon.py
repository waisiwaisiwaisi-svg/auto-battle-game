# ドクエイ（どく・みず × エイ）手打ち GBA風
META = dict(id='dokuei', name='ドクエイ', types=['poison', 'water'], base='エイ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c1a2a',
    'A': '#6e9e8c', 'B': '#3e6a62', 'D': '#22403e',
    'E': '#c8d8c0',
    'P': '#ff7ae0', 'p': '#c03aa8', 'q': '#6a1a6a',
    'Y': '#ffe040',
    'w': '#f4ecd8', 'n': '#b0a080',
    'c': '#a8f0ff',
}
LIGHT = set('AEPwYc')
KEEP_BLACK = set('wYPp')

# 体（つばさ）：右前へ とがった やじりの 形。奥の つばさは 上、手前の つばさは 下（裏の 白い ふちが 見える）
DISC = [
    '................kkkk.............................',
    '.............kkkAAAAkkk..........................',
    '............kAAAAAAAAAAkkk.......................',
    '...........kAAAABBBBAAAAAAkk.....................',
    '..........kAABBBBBBBBBBAAAAAkkk..................',
    '.........kAABBBBBBBBBBBBBBAAAAAkkk...............',
    '........kAABBBBBBBBBBBBBBBBBAAAAAAkkk............',
    '.......kAABBBBBBBBBBBBBBBBBBBBBAAAAAAkk..........',
    '......kAABBBBBBBBBBBBBBBBBBBBBBBBBAAAAAkk........',
    '.....kAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAkk......',
    '....kAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAk.....',
    '...kAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAkk...',
    '..kAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAkk.',
    '.kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAk',
    'kEEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDEEEEEk',
    '.kEEDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDEEEEEkkk.',
    '..kEEDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDDDEEEEEkk....',
    '...kEEDBBBBBBBBBBBBBBBBBBBBBBBBBDDDEEEEEkkk......',
    '....kEEDBBBBBBBBBBBBBBBBBBBBBDDDEEEEEEkk.........',
    '.....kEEDBBBBBBBBBBBBBBBBBDDDEEEEEEkkk...........',
    '......kEEDBBBBBBBBBBBBBDDDEEEEEEkkk..............',
    '.......kEEDBBBBBBBBBDDDEEEEEEkkk.................',
    '........kEEDDBBBBDDDEEEEEEkkk....................',
    '.........kEEEDDDDEEEEEEkkk.......................',
    '..........kEEEEEEEEEkkk..........................',
    '...........kkEEEEkkk.............................',
    '.............kkkk................................',
]
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
# 目：背の 上に 突き出た 金の つり目
EYE = ['kk...', 'kkkkk', '.kYYk', '..kkk']
EYE_ALT = {'blink': ['kk...', 'kkkkk', '.kkkk', '.....'], 'atk0|atk1|atk2': ['kk...', 'kkkkk', 'kYYYk', '.kkkk'], 'hit': ['kk...', 'kkkkk', '.kYkk', '..k..'], 'ko': ['.....', 'k.k..', '.k...', 'k.k..']}
EYE2_ALT = {'blink': ['kkkk.', '....'], 'atk0|atk1|atk2': ['kYYk', 'kYk.'], 'hit': ['kkYk', '.k..'], 'ko': ['k.k.', '.k..']}
EYE2 = ['kYYk', '.kk.']
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
        dict(n='tail', g='tail', x=2, y=19, rows=TAIL, not_='atk1|atk2'),
        dict(n='barb', g='tail', x=17, y=17, rows=BARB, alt={'atk0': BARB_HOT}, not_='atk1|atk2'),
        dict(n='drip', g='tail', x=22, y=24, rows=DRIP, only='idle2|idle3|walk1|walk3'),
    ]
    for i, (a, b) in enumerate(SEG):
        L.append(dict(n=f'd{i}', g=f'w{i}', x=9 + a, y=33, rows=cut(DISC, a, b)))
    L += [
        dict(n='g1', g='w1', x=28, y=39, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g2', g='w2', x=35, y=41, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g3', g='w0', x=20, y=43, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g4', g='w0', x=21, y=50, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g5', g='w1', x=29, y=51, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g6', g='w1', x=26, y=54, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='g7', g='w2', x=36, y=49, rows=GL, alt={'atk0|atk1': GL_HOT}),
        dict(n='eye', g='w2', x=45, y=41, rows=EYE, alt=EYE_ALT),
        dict(n='eye2', g='w2', x=45, y=48, rows=EYE2, alt=EYE2_ALT),
        dict(n='strike', g='root', x=5, y=19, rows=TAIL_STRIKE, only='atk1|atk2'),
        dict(n='barbd', g='root', x=50, y=25, rows=BARB_D, only='atk1|atk2'),
        dict(n='spray', g='root', x=52, y=33, rows=SPRAY, only='atk1'),
        dict(n='dust', g='root', x=2, y=57, rows=DUST[0], alt={'walk1|walk3': DUST[1]}, only='walk0|walk1|walk2|walk3'),
    ]
    return L
FRAMES = {
    'idle0': {}, 'idle1': {'w0': (0, -1), 'tail': (0, -1)}, 'idle2': {'w1': (0, -1), 'tail': (0, -1)}, 'idle3': {'w2': (0, -1)},
    'blink': {},
    'walk0': {'w0': (0, -1)}, 'walk1': {'w1': (0, -1), 'tail': (1, 0)}, 'walk2': {'w2': (0, -1)}, 'walk3': {'w1': (0, 1), 'tail': (-1, 0)},
    'atk0': {'tail': (-1, -2), 'root': (-2, 0)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (3, 0), 'w2': (0, 1)},
    'hit': {'root': (-3, 0), 'w2': (0, -2), 'w1': (0, -1), 'tail': (-1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'w0': 'root', 'w1': 'root', 'w2': 'root', 'tail': 'root'}
