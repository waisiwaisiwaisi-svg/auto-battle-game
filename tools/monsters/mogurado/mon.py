# モグラドン（じめん・はがね × モグラ）手打ち GBA風
META = dict(id='mogurado', name='モグラドン', types=['ground', 'steel'], base='モグラ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c2a2a',
    'S': '#e4ecf4', 'T': '#94a2b8', 'U': '#4c5870',
    'F': '#c08a58', 'G': '#84553a', 'H': '#4e3026',
    'Y': '#ffe25a', 'O': '#ff8a1e',
    'D': '#d8b880', 'R': '#a8283a', 'w': '#ffffff',
}
LIGHT = set('SFYDw')

def _outline(rows):
    W = max(len(r) for r in rows); g = [['.'] * (W + 2)] + [list('.' + r.ljust(W, '.') + '.') for r in rows] + [['.'] * (W + 2)]
    out = [r[:] for r in g]
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == '.' and any(0 <= y + dy < len(g) and 0 <= x + dx < len(g[0]) and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return [''.join(r) for r in out]

# ---- 胴：猫背の 体。背中は はがねの 板よろい（4枚・下の ふちが とがる）、下は 土色の 毛 ----
# デフォルメ：短く 高い ドーム（板よろい 3枚）。頭は 元の 大きさの まま
SPAN = [(10, 16), (7, 19), (5, 21), (4, 22), (3, 23), (2, 24), (1, 24), (1, 25), (0, 25), (0, 25), (0, 25), (0, 25),
        (0, 25), (0, 25), (0, 25), (0, 25), (0, 25), (0, 25), (1, 25), (1, 24), (2, 23), (4, 21)]
S1 = [None, 11, 11, 10, 10, 10, 9, 9, 9, 8, 8, 8]
S2 = [None, 17, 17, 17, 17, 18, 18, 18, 18, 18, 19, 19]
SEAMS = [() if a is None else (a, b) for a, b in zip(S1, S2)]
P = 11   # 板の 下の ふち（とがる）
def body():
    g = [['.'] * 26 for _ in range(len(SPAN))]
    for y, (a, b) in enumerate(SPAN):
        for x in range(a, b + 1):
            if y <= P:
                cuts = [a - 1] + [s for s in SEAMS[y] if a < s < b] + [b + 1]
                if x in cuts: g[y][x] = 'k'; continue
                lo = max(c for c in cuts if c < x); hi = min(c for c in cuts if c > x)
                dl, dr = x - lo - 1, hi - x - 1
                c = 'T'
                if dl == 0 or (dl <= 2 and 2 <= y <= 5) or y <= 1: c = 'S'
                if dr <= 1 or (y >= 7 and dr <= 3) or y >= P - 1: c = 'U'
                if y <= 1 and dr <= 1: c = 'T'
                if y == P:   # 板の 下の ふちは とがる
                    m = (lo + hi) / 2; c = 'U' if abs(x - m) <= (hi - lo) / 2 - 2 else 'k'
                g[y][x] = c
            elif y == P + 1:
                lo = max([a - 1] + [s for s in SEAMS[P] if s < x]); hi = min([b + 1] + [s for s in SEAMS[P] if s > x])
                m = (lo + hi) / 2; g[y][x] = 'k' if abs(x - m) <= (hi - lo) / 2 - 3 else 'H'
            else:
                c = 'G'
                if y == P + 2 or y >= 19 or x >= b - 2 or (y >= 17 and x >= b - 7): c = 'H'
                elif x <= a + 1 and y <= 16: c = 'F'
                g[y][x] = c
    rows = _outline([''.join(r) for r in g])
    g = [list(r) for r in rows]
    # 手で 打つ：びょう（リベット）・きず・毛の すじ
    for (x, y) in ((5, 10), (6, 5), (13, 6), (12, 10), (20, 6), (20, 10)):
        g[y][x] = 'S'; g[y + 1][x] = 'U'
    for (x, y) in ((16, 4), (17, 5)):  # 板の きず
        g[y][x] = 'U'
    for (x, y) in ((5, 17), (10, 16), (15, 17), (20, 16), (8, 19), (13, 19), (18, 19), (6, 15)):
        if g[y][x] in 'GF': g[y][x] = 'H'
        if g[y - 1][x - 1] in 'G': g[y - 1][x - 1] = 'F'
    return [''.join(r) for r in g]

# ---- ドリルの 鼻（らせんの みぞ、phase で 回る）----
def drill(phase=0, hot=False):
    W = [3, 6, 9, 12, 9, 6, 3]
    g = [['.'] * 12 for _ in range(7)]
    for y, w in enumerate(W):
        for x in range(w):
            base = 'S' if y <= 1 else 'T' if y <= 3 else 'U'
            if y == 2 and x < 4: base = 'S'
            if (x - 2 * (y - 3) + phase) % 4 == 0: base = {'S': 'T', 'T': 'U', 'U': 'k'}[base]
            elif (x - 2 * (y - 3) + phase) % 4 == 1 and base == 'T': base = 'S'
            g[y][x] = base
    if hot: g[3][11] = 'Y'; g[3][10] = 'O'; g[4][8] = 'O'
    return _outline([''.join(r) for r in g])

# 頭：はがねの かぶと＋ゴーグルの ような 目、下は 毛の あごと 牙の 口
HEAD = [
    '.....kkkkkk.......',
    '...kkSSSSSSkk.....',
    '..kSSSSTTTTTTk....',
    '.kSSTTTTTTTTTUk...',
    '.kSTTkkkkkkTTUUk..',
    'kSTTkTTTTTTkTUUUk.',
    'kSTTkTTTTTTkTUUUk.',
    'kTTTkTTTTTkTTUUUk.',
    'kTTTTkkkkkTTUUUUUk',
    'kUUTTTTTTTUUUUUUUk',
    'kkkkkkkkkkkkkkkkkk',
    'kFFGGGGGGGGGGGGGGk',
    'kFGGGGGkkkkkkkkkk.',
    'kGGGGGkwRRwRRRwRk.',
    'kGGGGHHkRwRRwRkk..',
    '.kHHHHHHkkkkkk....',
    '..kkkkkkk.........',
]
EYE = ['TkkkkT', 'kwYkOk', 'YYYkOk', 'kOOkk.']
EYE_ALT = {'blink': ['TkkkkT', 'kTTTTk', 'kkkkkk', 'kTTTk.'], 'atk0|atk1|atk2': ['TkkkkT', 'kwwkYk', 'YYYkYk', 'kOOkk.'], 'hit': ['TkkkkT', 'kOkkOk', 'kTOOkk', 'kOkkO.'], 'ko': ['TkkkkT', 'kOkOkk', 'kTOkTk', 'kOkOk.']}
SPK = ['.k....', 'kSk...', 'kSUk..', 'kSTUk.', 'kSTUUk', 'kSTTUk']
ARM = [
    '..kkkkk...........',
    '.kFGGGGk..........',
    'kFGGGGHk..........',
    'kFGGGHHk..........',
    'kGGGHHHk..........',
    'kkkkkkkkk.........',
    'kSSSTTUUk.........',
    'kTTTTUUUk.........',
    'kkkkkkkkkkkkk.....',
    'kFGGGHkSSSSTTkk...',
    'kGGGHkTTTTTUUUUk..',
    'kGGHkkkkkkkkkkUUk.',
    'kGHkSSSSSTTkk.kUk.',
    'kHHkTTTTUUUUUk.k..',
    '.kkkkkkkkkkkUUk...',
    '..kSSSSTTkk.kUk...',
    '..kTTUUUUUUk.k....',
    '...kkkkkkkUk......',
    '..........k.......',
]
LEG = [
    'kFGGGHk.',
    'kFGGGHk.',
    'kFGGGHk.',
    'kGGGGHk.',
    'kGGGHHk.',
    'kGGHHHkk',
    'kHHHHHHk',
    'kkkkkkkk',
    'kSkSkSk.',
    '.k.k.k..',
]
TAIL = ['kk...', 'kSkk.', 'kTUGk', '.kkHk', '...k.']
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'U': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 攻撃の エフェクト：ドリルの 先で 火花、くだけた 岩が とぶ（手打ち）
SPARK = [
    '......kk..',
    '..Y..kDDk.',
    '..Y...kHk.',
    'YYOYY.....',
    '..Y.....D.',
    '..Y..kk...',
    '....kDHk..',
    '.....kk...',
]
SPARK2 = [
    '.......kk.',
    '..O...kDHk',
    '.....O.kk.',
    'O.Y.......',
    '.....O..D.',
    '..O.......',
    '.....kk...',
    '....kHHk..',
]
SPEED = ['TTTTTT....', '..........', '...TTTTTTT', '..........', 'TTTTT.....', '..........', '..TTTTTT..']
DUST = ['...DD......DD..', '.DDDDD..DDDDD..', 'DD.DDDDDDD.DDD.']

BODY = body()
HX, HY = 26, 29
def layers():
    return [
        dict(n='armF', g='legA', x=HX + 2, y=HY + 10, rows=dark(ARM)),
        dict(n='legHF', g='legB', x=13, y=50, rows=dark(LEG)),
        dict(n='tail', g='body', x=2, y=44, rows=TAIL),
        dict(n='sp1', g='body', x=7, y=30, rows=SPK),
        dict(n='sp2', g='body', x=12, y=27, rows=SPK),
        dict(n='sp3', g='body', x=18, y=25, rows=SPK),
        dict(n='body', g='body', x=4, y=29, rows=BODY),
        dict(n='legH', g='legA', x=6, y=51, rows=LEG),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD),
        dict(n='eye', g='head', x=HX + 5, y=HY + 4, rows=EYE, alt=EYE_ALT),
        dict(n='drill', g='head', x=HX + 16, y=HY + 3, rows=drill(0), alt={'idle1|walk1|walk3': drill(1), 'idle2': drill(2), 'idle3': drill(3), 'atk0': drill(2, True), 'atk1': drill(1, True), 'atk2': drill(3, True)}),
        dict(n='arm', g='legB', x=HX - 3, y=HY + 11, rows=ARM),
        dict(n='fx', g='head', x=HX + 28, y=HY + 4, rows=SPARK, alt={'atk2': SPARK2}, only='atk1|atk2'),
        dict(n='speed', g='root', x=-4, y=38, rows=SPEED, only='atk1'),
        dict(n='dust', g='root', x=0, y=58, rows=DUST, only='atk0'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 0)},
    'idle3': {'body': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 2), 'head': (-1, 1), 'legB': (-2, 0), 'legA': (-1, 0)},
    'atk1': {'root': (6, 0), 'head': (1, 0), 'legB': (3, -1)},
    'atk2': {'root': (8, 0), 'legB': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
