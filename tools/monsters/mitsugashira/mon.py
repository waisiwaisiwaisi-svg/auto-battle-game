# ミツガシラ（はがね・あく × ケルベロス）手打ち GBA風・デフォルメ（2〜3頭身：3つの 頭を 大きく 描きなおし、胴は 短く 丸く、足は 短く 太く）
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
EYE_BOX = (40, 13, 15, 30)   # 3つの 頭の 目（idle0 の 64x64 座標）

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
SPAN = [(9, 20), (5, 25), (3, 27), (2, 28), (1, 29), (1, 29), (0, 29), (0, 29), (0, 29), (0, 29), (0, 29), (1, 29),
        (1, 29), (2, 28), (3, 28), (5, 27), (8, 26), (12, 24)]
def body():
    g = shade(SPAN, 30, lit=2, dk=3)
    # 筋肉の すじ・毛の 流れ（手で 打つ）
    for (x, y) in ((6, 6), (7, 7), (8, 8), (8, 9), (7, 10), (11, 11), (12, 11), (13, 12), (19, 8), (20, 9), (21, 10),
                   (21, 11), (20, 12), (17, 14), (18, 14)):
        if g[y][x] == 'G': g[y][x] = 'H'
    for (x, y) in ((5, 5), (6, 5), (9, 7), (18, 6), (19, 7), (14, 8), (15, 9), (4, 9), (23, 11)):
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
HEAD = [   # 大きく 描きなおした 頭（23×18）
    '..kk...................',
    '.kSUk..................',
    '.kSTUk.................',
    '..kTUGk...kkkkk........',
    '..kGGGGkkkFFFFFkk......',
    '.kGGGFFFFFFGGGGGGkk....',
    'kGGFFFFGGGGGGGGGGGGkk..',
    'kGFFGGGGGGGGGGGGGGGGGk.',
    'kGFFGGGGGGGGGGGGGGGGGGk',
    'kGFGGGGGGGGGGGGGGGGGkkk',
    'kGGGGGGGGGGGGGGGGGGGkHk',
    'kGGGGGGGGGGGGGGGGGGGGkk',
    'kGGGGGGGGGGkkkkkkkkkkk.',
    'kHGGGGGGGGkwMwkkMwkMwk.',
    '.kHGGGGGGkMMMMMMMMMMk..',
    '..kHHGGGHkkwkkwkkwkk...',
    '...kkHHHHHHHHHHkk......',
    '.....kkkkkkkkkk........',
]
HEAD_OPEN = HEAD[:12] + [
    'kGGGGGGGGGkkkkkkkkkkkk.',
    'kHGGGGGGGkwMwMMwMMwMk..',
    '.kHGGGGGkMMMMMMMMMMk...',
    '..kHGGGkMMMMMMMMk......',
    '..kHGGGGkwMMwMMwk......',
    '...kHHHHHHHHHHHk.......',
    '....kkkkkkkkkkk........',
]
def hshade(rows):
    """頭の 広い G に 光と 影：上の ふちは F、下・右の ふちは H（手打ちの 下地を こわす）"""
    g = [list(r) for r in rows]; H, W = len(g), len(g[0]); o = [r[:] for r in g]
    def at(y, x): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'G': continue
            if at(y - 1, x) in 'k.' or at(y - 2, x) in 'k.' and y < 8: o[y][x] = 'F'
            elif at(y + 1, x) in 'k.' or at(y, x + 1) in 'k.' or at(y + 2, x) in 'k.': o[y][x] = 'H'
    for (x, y) in ((14, 9), (15, 10), (16, 10), (12, 11), (17, 8)):   # ほおの 毛すじ
        if o[y][x] == 'G': o[y][x] = 'H'
    return [''.join(r) for r in o]
HEAD = hshade(HEAD); HEAD_OPEN = hshade(HEAD_OPEN)
# 目（E：光る目・瞳なし）：黒い まゆの 下で 赤い 光（R）が 細く 燃え、芯は 白〜うす桃（w／Y）。ふちは 黒線の かわりに 暗い 赤の にじみ（M）、光は 後ろへ 尾を 引く
EYE = ['kkkkkkk.', 'MRYwYRM.', '.MMRRRRk', '....MM..']
EYE_ALT = {
    'blink': ['kkkkkkk.', '.kkkkkkk', '..MMMMM.', '........'],
    'atk0|atk1|atk2': ['kkkkkkkY', 'MRYwwYRR', 'MMRYYRRR', '..MMMRM.'],
    'hit': ['kkkkkkk.', '.R.Y.Rk.', '..M.R.M.', '.M......'],
    'ko': ['........', '.MR..MR.', '..MRMR..', '.MR..MR.'],
}
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
    'kGGGGHHk',
    '.kGGGHk.',
    '.kSSTUk.',
    '.kSTTUk.',
    'kSTTUUUk',
    'kkkkkkkkk',
    '.kwkwkwk.',
]
HLEG = [
    '..kkkkkkk...',
    '.kFFFGGGGkk.',
    'kFFGGGGGGGHk',
    'kFGGGGGGGHHk',
    '.kGGGGGGHHk.',
    '..kGGGGHHk..',
    '..kGGGHk....',
    '.kSTTUk.....',
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
        dict(n='tail', g='tail', x=10, y=29, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='legHF', g='legB', x=19, y=49, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=40, y=50, rows=dark(FLEG)),
        dict(n='mane', g='body', x=25, y=23, rows=MANE, alt={'idle1|idle3|walk1|walk3': MANE2}),
        dict(n='body', g='body', x=14, y=36, rows=BODY),
        dict(n='armor', g='body', x=16, y=33, rows=ARMOR),
        dict(n='neckB', g='body', x=35, y=19, rows=dark(NECK)),
        dict(n='neckB2', g='body', x=33, y=26, rows=dark(NECK)),
        dict(n='headB', g='h1', x=35, y=5, rows=dark(HEAD), alt={'atk1': dark(HEAD_OPEN)}),
        dict(n='eyeB', g='h1', x=40, y=13, rows=EYE, alt=EYE_ALT),
        dict(n='collB', g='h1', x=33, y=12, rows=COLLAR),
        dict(n='headM', g='h2', x=42, y=18, rows=HEAD, alt={'atk1': HEAD_OPEN}),
        dict(n='eyeM', g='h2', x=47, y=26, rows=EYE, alt=EYE_ALT),
        dict(n='collM', g='h2', x=40, y=25, rows=COLLAR),
        dict(n='legH', g='legA', x=14, y=49, rows=HLEG),
        dict(n='legF', g='legB', x=35, y=50, rows=FLEG),
        dict(n='headF', g='h3', x=38, y=31, rows=HEAD, alt={'atk1': HEAD_OPEN}),
        dict(n='eyeF', g='h3', x=43, y=39, rows=EYE, alt=EYE_ALT),
        dict(n='collF', g='h3', x=36, y=38, rows=COLLAR),
        dict(n='slash', g='root', x=64, y=27, rows=SLASH, alt={'atk2': SLASH2}, only='atk1|atk2'),
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
