# ヒサソリ（ほのお・どく × サソリ）手打ち GBA風
import pix
EYE_BOX = (33, 37, 12, 6)
META = dict(id='hisasori', name='ヒサソリ', types=['fire', 'poison'], base='サソリ', size='M')
PAL = {
    'k': '#101018', 'l': '#4a1424',
    'A': '#f08a64', 'B': '#c23a36', 'C': '#6e1a2a',      # こうら（赤銅）明・中・暗
    'Y': '#fff27a', 'O': '#ff8a1e',                      # 熱（熾火）
    'V': '#e6a0ff', 'U': '#9a48d0', 'X': '#4e1c72',      # 毒
    'w': '#fff6e8',
    'E': '#ff2a34',                                      # 目の 赤
}
LIGHT = set('AYVw')
KEEP_BLACK = set('wYE')

# ---- 胴（下書きの シルエットは 手で、3段の 陰影は ふちからの きょりで、継ぎ目は 手で）----
def shade(mask, lt, md, dk, t=2, lf=1, r=2, b=2):
    g = pix.grid_of(mask); H, W = len(g), len(g[0])
    on = lambda y, x: 0 <= y < H and 0 <= x < W and g[y][x] != '.'
    out = [r_[:] for r_ in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '#': continue
            dt = 0
            while on(y - dt - 1, x): dt += 1
            db = 0
            while on(y + db + 1, x): db += 1
            dl = 0
            while on(y, x - dl - 1): dl += 1
            dr = 0
            while on(y, x + dr + 1): dr += 1
            c = md
            if dt < t or dl < lf: c = lt
            if dr < r or db < b: c = dk
            if dt < t and dr < r: c = md
            out[y][x] = c
    return [''.join(r_) for r_ in out]
def put(rows, det, x0=0, y0=0):
    g = pix.grid_of(rows)
    for j, r in enumerate(det):
        for i, c in enumerate(r):
            if c not in '. ' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c
    return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'V': 'U', 'U': 'X'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# デフォルメ：腹は 短く 丸く（背板 3枚）
BODY_M = [
    '...######.#####.#####..',
    '.#####################.',
    '#######################',
    '#######################',
    '#######################',
    '#######################',
    '#######################',
    '.#####################.',
    '..###################..',
    '....###############....',
]
def body(hot=False):
    rows = shade(BODY_M, 'A', 'B', 'C', t=3, r=3, b=3)
    g = pix.grid_of(rows)
    # 背板の 継ぎ目：熾火が もれる（左＝影、右＝光の ふち）
    for sx in (6, 12, 18):
        for y in range(0, 7):
            if g[y][sx] == '.': continue
            g[y][sx] = 'Y' if (2 <= y <= 4 and (hot or y == 3)) else 'O'
            if g[y][sx - 1] != '.': g[y][sx - 1] = 'l' if y > 0 else 'C'
            if sx + 1 < len(g[0]) and g[y][sx + 1] in 'BC': g[y][sx + 1] = 'A' if y < 5 else 'B'
    # わき腹の すじ と 腹の 板
    for x in range(1, 22):
        if g[6][x] != '.': g[6][x] = 'l' if x % 6 else 'O'
    for (x, y) in ((2, 3), (9, 2), (15, 2), (21, 4)):
        if g[y][x] in 'BC': g[y][x] = 'A'
    return pix.outline(pix.rows_of(g))

# 頭（デフォルメで 大きく）：平たい よろいの かぶと、重い まゆ、口もとに 白い きば
HEAD = [
    '.....kkkkkkkk.........',
    '...kkAAAAAAABkkk......',
    '..kAAABBBBBBBBBBkk....',
    '.kAABBBBBBBBBBBBBBk...',
    '.kABBBBBBBBBBBBBBBBk..',
    'kABBBBBBkkkkkkkkkBBBk.',
    'kABBBBBkBBBBBBBkkBBBBk',
    'kABBBBBkBBBBBBBkCBBBBk',
    'kBBBBBBBkkkkkkkCCBBBBk',
    'kBBBBBBBBBBBBBBCCCBBCk',
    'kBBBBBBBBBBBBCCkkkkkk.',
    'kCBBBBBBBBBBCkwkkwk...',
    'kCCBBBBBBBBCkCCCCCk...',
    '.kCCBBBBBBCCCCCCCk....',
    '..kkCCCCCCCCCCkk......',
    '....kkkkkkkkkk........',
]
# 目（N 多眼）：頭の 横に 大・中・小・豆の 4つの 赤い 目。どれも 黒い ふちの つやつやの 玉（瞳なし）、大きさを 変えて 前へ 並べる
def _eyes(st='open'):
    g = [list(r) for r in ['BBBBBBBBBBBB', 'BBBBBBBBBBBB', 'BBBBBBBBBBBB', 'BBBBBBBBBBBB',
                           'BBBBBBBBBBCB', 'BBBBBBBBBCCB', 'BBBBBBBBBCCC']]
    E = {'open': 'EwC', 'atk': 'YwO', 'blink': 'CCC', 'hit': 'CCC', 'ko': 'CCC'}[st]
    def eye(x0, y0, w, h, hl=True):
        for y in range(y0 - 1, y0 + h + 1):
            for x in range(x0 - 1, x0 + w + 1):
                if (y in (y0 - 1, y0 + h)) != (x in (x0 - 1, x0 + w)): g[y][x] = 'k'
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w): g[y][x] = E[2] if (y == y0 + h - 1 and x == x0 + w - 1 and h > 1) else E[0]
        if w * h >= 4: g[y0][x0] = E[1]
        if st in ('blink', 'hit'):
            for x in range(x0, x0 + w): g[y0 + h - 1][x] = 'k'
    eye(1, 3, 4, 2); eye(6, 2, 2, 2); eye(9, 5, 2, 1); eye(10, 1, 1, 1)
    if st == 'hit':
        for x in range(1, 5): g[3][x] = 'k'; g[4][x] = 'C'
        g[4][2] = g[3][3] = 'k'
    if st == 'ko':
        for (x, y) in ((1, 3), (4, 3), (2, 4), (3, 4)): g[y][x] = 'k'
        g[3][2] = g[3][3] = 'C'; g[4][1] = g[4][4] = 'C'
        g[2][6] = g[3][7] = 'k'
    return [''.join(r) for r in g]
EYE = _eyes()
EYE_ALT = {'blink': _eyes('blink'), 'atk0|atk1|atk2': _eyes('atk'), 'hit': _eyes('hit'), 'ko': _eyes('ko')}

# はさみ（腕＋大きな はさみ。すき間から 火花）
CLAW = [
    '...kkkkkk........',
    '..kAAAAABkkkkk...',
    '.kAAABBBBBAAABkk.',
    'kAABBBBBBBBBBBBCk',
    'kABBBBBBBkwkwkkCk',
    'kABBBBBBk......kk',
    'kABBBBBBk........',
    'kBBBBBBBk.....kk.',
    'kBBBBBBBBkwkwkCk.',
    'kCBBBBBBBBBBBCCk.',
    '.kCCBBBBBCCCCkk..',
    '..kkCCCCCkkk.....',
    '....kkkkk........',
]
ARM = [
    '....kkk',
    '..kkABk',
    '.kABBCk',
    'kABBCk.',
    'kBCCk..',
    '.kkk...',
]
SPARK = {'idle0|walk0|walk2': ['....', '.Y..', '..O.', '....'],
         'idle1|walk1|walk3|blink': ['..Y.', 'O...', '...O', '.Y..'],
         'idle2': ['Y...', '..Y.', 'O...', '..O.'],
         'idle3': ['.O..', '...Y', '.Y..', '....']}

# 足：短く 太く（付け根は 腹の 下に もぐる）
LEG = [
    '.kkkk...',
    'kAABBk..',
    'kBBBBCk.',
    '.kBBBCk.',
    '..kBBCk.',
    '..kBBCCk',
    '...kBBCk',
    '...kBCCk',
    '...kCCk.',
    '....kk..',
]
LEGR = pix.flip_h(LEG)

# ---- しっぽ：節（手打ち）を 弧に そって 置く。節の あいだは 熾火 ----
SEG = [
    '..kkkk..',
    '.kAAABk.',
    'kAABBBCk',
    'kABBBBCk',
    'kBBBBCCk',
    '.kCCCCk.',
    '..kkkk..',
]
SEG = put(SEG, ['', '', '...O', '...l'])
SEG_HOT = put(SEG, ['', '', '...Y', '..lO', '', '.kOYOk.'])
STING = [
    '...kkkk......',
    '.kkVVVUkk....',
    'kVVVUUUUXk...',
    'kVVUUUUXXkOk.',
    'kVUUUUXXkYYOk',
    'kUUUXXXk.kYOk',
    '.kUXXXk...kYk',
    '..kkkk....kYk',
    '.........kYk.',
    '.........kYk.',
    '.........kk..',
]
# 突き：針が 前へ まっすぐ
STING_FWD = [
    '...kkkk.........',
    '.kkVVVUkk.......',
    'kVVVUUUUXkk.....',
    'kVVUUUUXXOOk....',
    'kVUUUUXXkYYOk...',
    'kUUUXXXk.kYYOk..',
    '.kUXXXk...kYYOk.',
    '..kkkk.....kYYk.',
    '............kYYk',
    '.............kYk',
    '..............k.',
]
DRIP = ['.V.', 'VUX', '.X.']
def tail(pos, sting, hot=False, drip=None):
    g = pix.grid(64, 48)
    for i, (x, y) in enumerate(pos):
        pix.stamp(g, SEG_HOT if hot or i % 2 else SEG, x, y)
    sx, sy = pos[-1]
    pix.stamp(g, sting, sx + 4, sy - 4)
    if drip: pix.stamp(g, DRIP, drip[0], drip[1])
    return pix.rows_of(g)
T_IDLE = [(9, 33), (6, 27), (6, 21), (9, 15), (14, 11)]
T_UP = [(9, 33), (6, 27), (6, 20), (9, 14), (15, 10)]
T_COCK = [(8, 33), (4, 27), (3, 20), (5, 13), (10, 8)]
T_STRIKE = [(9, 32), (12, 26), (17, 21), (23, 18), (29, 16)]
T_HIT = [(8, 33), (4, 28), (2, 22), (3, 16), (7, 12)]
SPINE = ['.k..', 'kYk.', 'kOAk', 'kBBk']
SPINE_H = ['.kk.', 'kYYk', 'kOAk', 'kBBk']
# かぶとの 後ろへ 反った 角（付け根は かぶとの 中に 2ドット もぐる）
HSPINE = ['kk...', 'kYkk.', '.kOAk', '.kBBk', '.kBBk']
HSPINE_H = ['kk...', 'kYkk.', '.kYAk', '.kOBk', '.kBBk']
SPLASH = [
    '....V....',
    '.V..Y..U.',
    '...kYOk..',
    'VYYYYYYOV',
    '...kOYk..',
    '.U..O..V.',
    '....U....',
]

def layers():
    T = 'tail'
    return [
        dict(n='legF1', g='legB', x=40, y=50, rows=dark(LEG)),
        dict(n='legF2', g='legA', x=32, y=50, rows=dark(LEG)),
        dict(n='legF3', g='legB', x=19, y=50, rows=dark(LEGR)),
        dict(n='legF4', g='legA', x=11, y=50, rows=dark(LEGR)),
        dict(n='clawF', g='clawB', x=45, y=34, rows=dark(CLAW)),
        dict(n='tail', g=T, x=0, y=4, rows=tail(T_IDLE, STING),
             alt={'idle1|idle3|walk1|walk3': tail(T_UP, STING, hot=True), 'atk0': tail(T_COCK, STING, hot=True),
                  'atk1': tail(T_STRIKE, STING_FWD, hot=True), 'atk2': tail(T_STRIKE, STING_FWD, hot=True),
                  'hit': tail(T_HIT, STING), 'ko': tail(T_HIT, STING)}),
        dict(n='body', g='body', x=7, y=40, rows=body(), alt={'idle1|idle3|atk0|atk1|atk2': body(True)}),
        *[dict(n='sp%d' % i, g='body', x=x, y=y, rows=SPINE, alt={'idle1|idle3|atk0|atk1|atk2': SPINE_H})
          for i, (x, y) in enumerate(((10, 38), (16, 38), (22, 38)))],
        dict(n='leg1', g='legA', x=37, y=51, rows=LEG),
        dict(n='leg2', g='legB', x=29, y=51, rows=LEG),
        dict(n='leg3', g='legA', x=16, y=51, rows=LEGR),
        dict(n='leg4', g='legB', x=8, y=51, rows=LEGR),
        *[dict(n='hs%d' % i, g='head', x=x, y=y, rows=HSPINE, alt={'idle1|idle3|atk0|atk1|atk2': HSPINE_H})
          for i, (x, y) in enumerate(((30, 32), (35, 31)))],
        dict(n='head', g='head', x=27, y=34, rows=HEAD),
        dict(n='eye', g='head', x=33, y=37, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='claw', x=44, y=46, rows=ARM),
        dict(n='claw', g='claw', x=47, y=40, rows=CLAW),
        dict(n='spark', g='claw', x=56, y=45, rows=SPARK['idle0|walk0|walk2'],
             alt={k: v for k, v in SPARK.items()}, not_='hit|ko'),
        dict(n='splash', g='tail', x=44, y=22, rows=SPLASH, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, -1), 'claw': (0, -1)},
    'idle2': {'body': (0, 1), 'tail': (0, 0), 'claw': (0, -1)},
    'idle3': {'body': (0, 0), 'claw': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'claw': (1, 0)},
    'walk1': {'body': (0, -1), 'clawB': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'clawB': (1, 0)},
    'walk3': {'body': (0, -1), 'clawB': (0, -1)},
    'atk0': {'body': (-2, 1), 'claw': (-1, -2), 'clawB': (-2, -1), 'legA': (-1, 0), 'legB': (-1, 0)},
    'atk1': {'root': (4, 0), 'body': (0, -1), 'claw': (1, 1)},
    'atk2': {'root': (4, 0), 'tail': (1, 1), 'claw': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, 1), 'claw': (-1, 2), 'clawB': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'claw': 'head', 'clawB': 'head', 'body': 'root', 'legA': 'root', 'legB': 'root'}
