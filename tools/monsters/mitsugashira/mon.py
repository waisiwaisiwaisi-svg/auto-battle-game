# ミツガシラ（はがね・あく × ケルベロス）手打ち GBA風
META = dict(id='mitsugashira', name='ミツガシラ', types=['steel', 'dark'], base='ケルベロス', size='L')
PAL = {
    'k': '#101018', 'l': '#2c2440',
    'F': '#6c6a8e', 'G': '#43405c', 'H': '#25223a',
    'S': '#d4d8e4', 'T': '#868ca2', 'U': '#4a4e62',
    'R': '#ff2e6a', 'Y': '#ffd6e6',
    'P': '#c46cff', 'Q': '#6a24b0',
    'M': '#9c1838', 'w': '#ffffff',
}
LIGHT = set('FSYPw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, lit=1, dk=2):
    """あたりの はば（行ごと）→ 左上が 明、右下が 暗。広い 中間色は 手で こわす"""
    H = len(spans); m = [[a <= x <= b for x in range(W)] for (a, b) in spans]
    def ins(y, x): return 0 <= y < H and 0 <= x < W and m[y][x]
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            du = next(i for i in range(1, 9) if not ins(y - i, x) or i == 8)
            dl = next(i for i in range(1, 9) if not ins(y, x - i) or i == 8)
            dd = next(i for i in range(1, 9) if not ins(y + i, x) or i == 8)
            dr = next(i for i in range(1, 9) if not ins(y, x + i) or i == 8)
            c = 'G'
            if dd <= dk: c = 'H'
            elif du <= lit or dl <= 1: c = 'F'
            elif dr <= 1: c = 'H'
            g[y][x] = c
    return g

# ---- 胴：胸が 深く 腰が しまった 番犬の 体 ----
SPAN = [(26, 31), (19, 35), (6, 35), (4, 36), (3, 37), (2, 38), (1, 38), (1, 38), (1, 39), (1, 39), (1, 39), (1, 39),
        (1, 39), (1, 39), (2, 38), (3, 38), (4, 38), (6, 37), (17, 36), (22, 35), (23, 34), (26, 31)]
def body():
    g = shade(SPAN, 40, lit=2, dk=3)
    # 筋肉の すじ・毛の 流れ（手で 打つ）
    for (x, y) in ((8, 6), (9, 7), (10, 8), (10, 9), (9, 10), (13, 12), (14, 12), (15, 13), (20, 11), (21, 12), (22, 12),
                   (27, 8), (28, 9), (29, 10), (29, 11), (28, 12), (26, 15), (27, 15), (30, 16), (31, 17)):
        if g[y][x] == 'G': g[y][x] = 'H'
    for (x, y) in ((7, 5), (8, 5), (11, 7), (25, 6), (26, 7), (17, 9), (18, 10), (6, 9), (32, 13)):
        if g[y][x] == 'G': g[y][x] = 'F'
    return [''.join(r) for r in _ol(g)]

# 背中の 鉄の くら（びょう と とげ）
ARMOR = [
    '...k....k....k...',
    '..kSk..kSk..kSk..',
    '.kkSTkkkSTkkkSTkk',
    'kSSSSSSSSTTTTTTUk',
    'kSTTSTTTTTSTTTUUk',
    'kTTTUTTTTTUTTUUUk',
    'kUUUUUUUUUUUUUUUk',
    '.kkkkkkkkkkkkkkk.',
]
# 頭（犬の 頭・耳は 鉄の 先）：口は いつも うなって 牙が 見える
HEAD = [
    '..kk................',
    '.kSUk...............',
    '.kSTUk..............',
    '..kTUGk..kkkk.......',
    '..kGGGGkkFFFFkk.....',
    '.kGGGFFFFFGGGGGkk...',
    'kGGFFFGGGGGGGGGGGkk.',
    'kGFFGGkkkkkGGGGGGGGk',
    'kGFGGkGGGGkkGGGGGkkk',
    'kGGGGGkGGkGGGGGGGkHk',
    'kGGGGGGkkGGGGkkkkkk.',
    'kHGGGGGGGGGkwMwkMwk.',
    '.kHGGGGGGGkMMMMMMk..',
    '..kHHGGGHHkwkkwkk...',
    '...kkHHHHHHHHkk.....',
    '.....kkkkkkkk.......',
]
HEAD_OPEN = HEAD[:10] + [
    'kGGGGGGkkGkkkkkkkk..',
    'kHGGGGGGGkwMwMMwMk..',
    '.kHGGGGGkMMMMMMMk...',
    '..kHGGGkMMMMMMk.....',
    '..kHGGGGkwMMwMwk....',
    '...kHHHHHHHHHHk.....',
    '....kkkkkkkkkk......',
]
EYE = ['YYRR', 'kRRk']
EYE_ALT = {'blink': ['kkkk', 'GkkG'], 'atk0|atk1|atk2': ['YYYY', 'kYRk'], 'hit': ['RkkR', 'kRRk'], 'ko': ['RkRk', 'kRkG']}
COLLAR = [
    '.......',
    'k......',
    'kSkkk..',
    '..kSTUk',
    '.kkSTUk',
    'kSSSTUk',
    '.kkTTUk',
    '..kSTUk',
    '..kTUUk',
    '...kkk.',
]
NECK = [
    '...kkkkkk.',
    '..kFFGGGGk',
    '.kFGGGGGHk',
    '.kFGGGGGHk',
    'kFGGGGGHHk',
    'kFGGGGGHHk',
    'kGGGGGHHHk',
    'kGGGGGHHk.',
    'kGGGGHHHk.',
    'kGGGGHHk..',
]
FLEG = [
    '.kkkkkk.',
    'kFFGGGHk',
    'kFGGGGHk',
    'kFGGGGHk',
    'kGGGGHHk',
    '.kGGGHHk',
    '.kGGGHk.',
    '.kSSTUk.',
    '.kSTTUk.',
    '.kSTUUk.',
    'kSTTUUUk',
    'kkkkkkkkk',
    '.kwkwkwk.',
]
HLEG = [
    '..kkkkkkk...',
    '.kFFFGGGGkk.',
    'kFFGGGGGGGHk',
    'kFGGGGGGGGHk',
    'kFGGGGGGGHHk',
    'kGGGGGGGHHHk',
    '.kGGGGGHHHk.',
    '..kGGGGHHk..',
    '...kGGGHk...',
    '..kGGGHk....',
    '.kGGGHk.....',
    '.kSTTUk.....',
    '.kSTUUk.....',
    '.kTTUUk.....',
    '.kSTTUUk....',
    '.kkkkkkkk...',
    '..kwkwkwk...',
]
TAIL = [
    '..P.....',
    '.PQP....',
    '.PQQP...',
    'PQQQPk..',
    '.kQkkGk.',
    '..kSTUk.',
    '...kGHk.',
    '...kGHk.',
    '...kSTUk',
    '....kGHk',
    '....kGHk',
    '.....kGk',
]
TAIL2 = ['.P......', '..PP....', '.PQQP...', 'PQQQPk..'] + TAIL[4:]
MANE = [
    '.....P........',
    '....PP....P...',
    '...PQP...PP...',
    '...PQQP..PQP..',
    '..PQQQP.PQQP..',
    '.P.PQQQPPQQQP.',
    'PP.PQYQQQQQQP.',
    'PQPPQQQQQYQQQP',
    'PQQQQQQQQQQQQP',
    '.PQQQQQQQQQQQP',
    '..QQQQQQQQQQQ.',
    '..QQQQQQQQQQ..',
]
MANE2 = [
    '......P.......',
    '.....PP...P...',
    '....PQP..PP..P',
    '...PQQP.PQP..P',
    '..PQQQPPQQP.PQ',
    '..PQQQQPQQQPQP',
    '.PPQQYQQQQQQP.',
    'PQQPQQQQQYQQQP',
    'PQQQQQQQQQQQQP',
    '.PQQQQQQQQQQQP',
    '..QQQQQQQQQQQ.',
    '..QQQQQQQQQQ..',
]
# 攻撃：やみの 火の つめあと
SLASH = [
    '.....P......',
    '....PQ...P..',
    '...PQ...PQ..',
    '..PQ...PQ...',
    '.PQ...PQ...P',
    'PQ...PQ...PQ',
    'Q...PQ...PQ.',
    '...PQ...PQ..',
    '...Q...PQ...',
    '.......Q....',
]
SLASH2 = [
    '..........',
    '.....P....',
    '....P...P.',
    '...P...P..',
    '..P...P...',
    '.P...P...P',
    '....P...P.',
    '...P...P..',
    '.......P..',
    '..........',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'U': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=22, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='legHF', g='legB', x=11, y=42, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=40, y=46, rows=dark(FLEG)),
        dict(n='mane', g='body', x=29, y=17, rows=MANE, alt={'idle1|idle3|walk1|walk3': MANE2}),
        dict(n='body', g='body', x=5, y=30, rows=BODY),
        dict(n='armor', g='body', x=12, y=28, rows=ARMOR),
        dict(n='neckB', g='body', x=38, y=21, rows=dark(NECK)),
        dict(n='headB', g='h1', x=39, y=9, rows=dark(HEAD), alt={'atk1': dark(HEAD_OPEN)}),
        dict(n='eyeB', g='h1', x=45, y=17, rows=EYE, alt=EYE_ALT),
        dict(n='collB', g='h1', x=37, y=15, rows=COLLAR),
        dict(n='headM', g='h2', x=43, y=19, rows=HEAD, alt={'atk1': HEAD_OPEN}),
        dict(n='eyeM', g='h2', x=49, y=27, rows=EYE, alt=EYE_ALT),
        dict(n='collM', g='h2', x=41, y=25, rows=COLLAR),
        dict(n='legH', g='legA', x=5, y=43, rows=HLEG),
        dict(n='legF', g='legB', x=35, y=47, rows=FLEG),
        dict(n='headF', g='h3', x=40, y=31, rows=HEAD, alt={'atk1': HEAD_OPEN}),
        dict(n='eyeF', g='h3', x=46, y=39, rows=EYE, alt=EYE_ALT),
        dict(n='collF', g='h3', x=38, y=37, rows=COLLAR),
        dict(n='slash', g='root', x=64, y=25, rows=SLASH, alt={'atk2': SLASH2}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'h1': (0, 1), 'body': (0, 0)},
    'idle2': {'body': (0, 1), 'h2': (0, 0)},
    'idle3': {'h3': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'h1': (-2, 0), 'h2': (-2, 0), 'h3': (-1, 0)},
    'atk1': {'root': (3, 0), 'h1': (3, 2), 'h2': (4, 0), 'h3': (3, -1)},
    'atk2': {'root': (4, 0), 'h1': (2, 1), 'h2': (2, 0), 'h3': (1, 0)},
    'hit': {'root': (-3, 0), 'h1': (-2, -1), 'h2': (-2, -1), 'h3': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'h1': 'body', 'h2': 'body', 'h3': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
