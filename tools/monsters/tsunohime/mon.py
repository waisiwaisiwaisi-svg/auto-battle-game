# ツノヒメ（フェアリー・エスパー × ユニコーン）手打ち GBA風・デフォルメ（2〜3頭身：頭と 角は 大きく、胴は 小さく 丸く、足は 短く 太く）
META = dict(id='tsunohime', name='ツノヒメ', types=['fairy', 'psychic'], base='ユニコーン', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1e48',
    'F': '#7272c4', 'G': '#43428a', 'H': '#24224e',
    'C': '#fff0fa', 'P': '#ff7ad2', 'Q': '#a8389c',
    'S': '#ffe98e', 'T': '#d9a23c', 'U': '#8a5622',
    'E': '#6ef4ff', 'e': '#2a9cc8', 'w': '#ffffff',
}
LIGHT = set('FCSEw')
EYE_BOX = (45, 21, 7, 5)   # 目（idle0 の 64x64 座標）
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, poly, ellipse, outline, rows_of


# ---- 下書き用の 小道具（あたりは 多角形、陰影の 基本は 左上の 光。仕上げは 手で 打つ）----
def shade(g, ramp, lw=1, dw=2):
    L, M, D = ramp; H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def f(y, x): return 0 <= y < H and 0 <= x < W and src[y][x] == '#'
    for y in range(H):
        for x in range(W):
            if src[y][x] != '#': continue
            du = next(i for i in range(1, 10) if not f(y - i, x) or i == 9)
            dl = next(i for i in range(1, 10) if not f(y, x - i) or i == 9)
            dd = next(i for i in range(1, 10) if not f(y + i, x) or i == 9)
            dr = next(i for i in range(1, 10) if not f(y, x + i) or i == 9)
            c = M
            if dd <= dw or dr <= 1: c = D
            elif du <= lw or dl <= 1: c = L
            g[y][x] = c
    return g
class Part:
    """絶対座標で 描く パーツ（x, y は 左上、rows は 輪郭つき）"""
    def __init__(s, pts=None, ramp='FGH', lw=1, dw=2, ells=()):
        g = grid(72, 72)
        if pts: poly(g, pts, '#')
        for e in ells: ellipse(g, *e, '#')
        shade(g, ramp, lw, dw)
        ys = [y for y in range(72) if any(c != '.' for c in g[y])]; xs = [x for x in range(72) if any(g[y][x] != '.' for y in range(72))]
        s.x, s.y = xs[0] - 1, ys[0] - 1
        s.g = [list(r) for r in outline(rows_of([r[xs[0]:xs[-1] + 1] for r in g[ys[0]:ys[-1] + 1]]))]
    def P(s, pts, ch, only=None):
        for x, y in pts:
            X, Y = x - s.x, y - s.y
            if 0 <= Y < len(s.g) and 0 <= X < len(s.g[0]) and (only is None or s.g[Y][X] in only): s.g[Y][X] = ch
    def S(s, x0, y0, rows):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.': s.P([(x0 + i, y0 + j)], c)
    def at(s, x, y):
        X, Y = x - s.x, y - s.y
        return s.g[Y][X] if 0 <= Y < len(s.g) and 0 <= X < len(s.g[0]) else '.'
    def rows(s): return rows_of(s.g)

# ---- 頭（大きく）：戦馬の 頭。金の 面よろいが 鼻すじを おおう ----
# 目（P：星の 瞳）：虹彩は 上が 赤むらさき（Q）→ 下が 青（e）の グラデーション。その 中に 水色の 十字星の 瞳（E）、芯は 白（w）
EYE = ['kQQEQkk', 'kQEwEek', 'keeEeek', '.kkkkk.']
def head():
    h = Part([(35, 30), (37, 25), (41, 21), (47, 19), (52, 20), (55, 23), (58, 27), (61, 31), (61.5, 35), (60, 37.5), (55, 38), (51, 37), (48, 39.5), (41, 39.5), (37, 36)], 'FGH', 1, 2)
    h.P([(51, 36), (50, 35), (49, 34), (48, 33)], 'H', 'FG')                         # あごの 線（ほおと 口先を 分ける）
    # 頭の まるみ（後頭部の 光）と ほおの すじ
    h.P([(38, 26), (38, 27), (37, 28), (37, 29)], 'F')
    h.P([(41, 31), (42, 33), (43, 34), (44, 35), (46, 35), (48, 35)], 'H', 'FG')
    h.P([(42, 32), (43, 33), (44, 34)], 'F', 'G')
    # 金の 面よろい（ひたい → 鼻すじ）
    for x, y0 in ((47, 20), (48, 20), (49, 20), (50, 20), (51, 21), (52, 21), (53, 22), (54, 23), (55, 24), (56, 25), (57, 27), (58, 28), (59, 30)):
        h.P([(x, y0)], 'S'); h.P([(x, y0 + 1)], 'T'); h.P([(x, y0 + 2)], 'U')
    h.P([(46, 20), (46, 21)], 'S'); h.P([(45, 21)], 'T')
    h.P([(59, 31), (59, 32)], 'U')
    # 目：つり上がった まゆの 線の 下に 星の 瞳の 目（EYE）
    h.P([(42, 22), (43, 22), (43, 23), (44, 23), (45, 23), (46, 24), (47, 24), (48, 24), (49, 24), (50, 24), (51, 24), (52, 25), (53, 25)], 'k')
    h.P([(44, 22), (45, 22)], 'F')
    h.S(45, 25, EYE)
    # 鼻の あな・口（牙）
    h.P([(58, 32), (57, 32), (57, 33), (58, 33)], 'k'); h.P([(59, 32)], 'F')
    h.P([(61, 36), (60, 36), (59, 36), (58, 36), (57, 36), (56, 36), (55, 37), (54, 37), (53, 37), (52, 37)], 'k')
    h.P([(58, 37), (59, 37)], 'w'); h.P([(55, 38)], 'w'); h.P([(58, 38)], 'k')
    return h
HEAD = head()
def eye_alt():
    base = HEAD.rows()
    def with_eye(*rs):
        h = [list(r) for r in base]
        for j, r in enumerate(rs):
            for i, c in enumerate(r):
                if c != '.': h[25 + j - HEAD.y][45 + i - HEAD.x] = c
        return rows_of(h)
    return {'blink': with_eye('FFFFFFF', 'kkkkkkk', '.GGGGGG', 'GGHHHHG'), 'hit': with_eye('FkkFFFF', 'FFFkkkk', 'FkkFFFF', 'GGHHHHG'),
            'atk0|atk1|atk2': with_eye('kPQEQkk', 'kEEwEEk', 'kePEPek', '.kkkkk.'), 'ko': with_eye('FkFFkFF', 'FFkkFFF', 'FkFFkFF', 'GGHHHHG')}
HEAD_ALT = eye_alt()
# 耳（後ろへ ねる・付け根は 頭に 食いこむ）
EAR = ['kk....', 'kFk...', 'kFGk..', 'kFGGk.', '.kFGGk', '.kFGGG', '..kGGG']
EAR2 = ['.kk...', 'kGHk..', 'kGHHk.', '.kGHHH', '..kHHH']
# 結晶の やり（ツノ）：見せ所。らせんの きざみ つき、大きく 前上へ
HORN = [
    '..............kk',
    '............kkCk',
    '...........kCCPk',
    '.........kkCPQk.',
    '........kCPQPk..',
    '......kkCPQPk...',
    '.....kCPQPkk....',
    '...kkCPQPk......',
    '..kCPQPkk.......',
    '.kSPQPk.........',
    'kSTUQk..........',
    'kTTUk...........',
    '.kkk............',
]
HORN_HOT = [r.replace('P', 'C').replace('Q', 'P') for r in HORN]

# ---- 胴（小さく 丸い 馬体）：胸は 前へ 張りだし、頭の 下に もぐる ----
def body():
    b = Part([(16, 43), (19, 39), (25, 37), (33, 37), (39, 35), (44, 37), (47, 41), (47, 46), (44, 50), (38, 52), (22, 52), (17, 50)], 'FGH', 1, 2)
    b.P([(26, 41), (25, 42), (24, 43), (24, 44), (25, 45), (26, 46)], 'H', 'FG')     # 腰の 筋肉
    b.P([(27, 42), (26, 43), (26, 44)], 'F', 'G')
    b.P([(36, 40), (35, 41), (35, 42), (35, 43), (36, 44)], 'H', 'FG')               # 肩
    b.P([(37, 41), (37, 42)], 'F', 'G')
    b.P([(29, 47), (30, 48), (32, 47), (33, 48)], 'H', 'G')                          # あばら
    return b
BODY = body()
# 胸の 金の むないた（水色の 宝石）
PLATE = [
    '.kkkkkk.',
    'kSSSSTTk',
    'kSTwETUk',
    'kSTEeTUk',
    '.kTTTUk.',
    '..kUUk..',
    '...kk...',
]
# 足：短く 太く。上の 3行は 胴に もぐる（輪郭なし）→ 金の わ → 結晶の ひづめ
LEG = ['kFGGGHk', 'kFGGGHk', 'kFGGGHk', 'kFGGGHk', '.kFGGHk', '.kFGHHk', 'kFGGGHk', 'kSTTTUk', 'kGGGHHk', 'kGGGHHk', 'kCPPPQk', 'kCPPQQk', 'kkkkkkk']
LEG_UP = ['kFGGGHk', 'kFGGGHk', 'kFGGGHk', '.kFGGGHk', '..kFGGHHk', '...kFGGHk', '...kSTTUk', '...kGGHHk', '..kCPPQk.', '..kCPQQk.', '..kkkkk..']
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'C': 'P', 'P': 'Q'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
def notop(rows): return ['.' + r[1:-1] + '.' if i < 2 else r for i, r in enumerate(rows)]

# ---- 結晶の たてがみ：頭の 後ろから 首・肩へ、房を 重ねて 後ろへ なびかせる ----
CREST = [(37, 38), (36, 34), (36, 30), (37, 26), (39, 23), (42, 21)]
def mane(shine=0):
    W, H = 40, 40; canvas = grid(W, H); X0, Y0 = 14, 12
    for i, (ax, ay) in enumerate(CREST):
        ax -= X0; ay -= Y0
        L = 8 + (i % 2) * 2 + (1 if 1 <= i <= 3 else 0)
        tip = (ax - L, ay - L // 3 + (2 if i == 0 else 0))
        g = grid(W, H)
        poly(g, [(ax + 1, ay - 2), (ax + 2, ay + 2), (ax - 1, ay + 2.5), tip], '#')
        out = [r[:] for r in g]
        for y in range(H):
            for x in range(W):
                if g[y][x] == '.': continue
                up = next(j for j in range(1, 9) if y - j < 0 or g[y - j][x] == '.' or j == 8)
                dn = next(j for j in range(1, 9) if y + j >= H or g[y + j][x] == '.' or j == 8)
                out[y][x] = 'C' if up <= 1 else 'Q' if dn <= 1 else 'P'
        if shine and i % 3 == shine % 3:
            for y in range(H):
                for x in range(W):
                    if out[y][x] == 'P': out[y][x] = 'C'; break
        o = outline(rows_of(out))
        for y, r in enumerate(o[1:H + 1]):
            for x, c in enumerate(r[1:W + 1]):
                if c != '.': canvas[y][x] = c
    return X0 - 1, Y0 - 1, outline(rows_of(canvas))
MX, MY, MANE = mane(); _, _, MANE2 = mane(1)
TAIL = [
    '.......kkk..',
    '.....kkCCPk.',
    '....kCCPPQk.',
    '...kCPPQQk..',
    '..kCPPQk....',
    '.kCPPQk.kk..',
    'kCPPQk.kCPk.',
    'kCPQk.kCPQk.',
    'kPQk.kCPQk..',
    'kPQk.kPQk...',
    '.kQk.kPQk...',
    '.kQk.kQk....',
    '..kk.kk.....',
]
# しっぽの 付け根（腰に 食いこむ 結晶の たば）
TAILROOT = ['..kkk.', '.kCPPk', 'kCPPQQ', 'kPPQQQ', '.kQQQQ']
MOTE = ['.k.', 'kCk', 'kPk', '.k.']
BURST = [
    '......C......',
    '......C......',
    '..P...C...P..',
    '...P..P..P...',
    '....P.C.P....',
    '.....CwC.....',
    'CCPPCwwwCPPCC',
    '.....CwC.....',
    '....P.C.P....',
    '...P..P..P...',
    '..P...C...P..',
    '......C......',
    '......C......',
]
BURST2 = [
    '...P.....P...',
    '.............',
    'P....PCP....P',
    '....P...P....',
    '...P.....P...',
    '..C...w...C..',
    '..P..www..P..',
    '..C...w...C..',
    '...P.....P...',
    '....P...P....',
    'P....PCP....P',
    '.............',
    '...P.....P...',
]

DY = -3
def layers():
    L = [
        dict(n='tail', g='tail', x=5, y=32, rows=TAIL),
        dict(n='troot', g='tail', x=13, y=38, rows=TAILROOT),
        dict(n='legHF', g='legB', x=27, y=45, rows=notop(dark(LEG))),
        dict(n='legFF', g='legA', x=41, y=44, rows=notop(dark(LEG)), alt={'atk0|atk1': notop(dark(LEG_UP))}),
        dict(n='ear2', g='head', x=36, y=17, rows=EAR2),
        dict(n='body', g='body', x=BODY.x, y=BODY.y, rows=BODY.rows()),
        dict(n='legH', g='legA', x=19, y=46, rows=notop(LEG)),
        dict(n='legF', g='legB', x=36, y=46, rows=notop(LEG), alt={'atk0': notop(LEG_UP)}),
        dict(n='plate', g='body', x=40, y=42, rows=PLATE),
        dict(n='mane', g='neck', x=MX, y=MY, rows=MANE, alt={'idle1|idle3': MANE2}),
        dict(n='head', g='head', x=HEAD.x, y=HEAD.y, rows=HEAD.rows(), alt=HEAD_ALT),
        dict(n='ear', g='head', x=39, y=15, rows=EAR),
        dict(n='horn', g='head', x=46, y=8, rows=HORN, alt={'atk0|atk1|atk2': HORN_HOT}),
        dict(n='m1', g='m1', x=24, y=18, rows=MOTE),
        dict(n='m2', g='m2', x=4, y=24, rows=MOTE),
        dict(n='m3', g='m3', x=56, y=44, rows=MOTE, not_='atk1|atk2'),
        dict(n='burst', g='head', x=55, y=0, rows=BURST, alt={'atk2': BURST2}, only='atk1|atk2'),
    ]
    for l in L:
        if not l['n'].startswith('leg'): l['y'] += DY
    return L

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'idle2': {'body': (0, 1), 'm1': (0, -2), 'm2': (0, 2), 'm3': (0, -2)},
    'idle3': {'body': (0, 1), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'm1': (0, -1)},
    'walk1': {'body': (0, -1), 'm2': (0, 1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'm1': (0, -1)},
    'walk3': {'body': (0, -1), 'm2': (0, 1)},
    'atk0': {'body': (-1, 0), 'head': (-1, 1), 'legB': (1, -2), 'm1': (8, 0), 'm2': (14, -2)},
    'atk1': {'root': (6, 0), 'head': (1, 2), 'legA': (1, -1), 'm1': (14, 2), 'm2': (28, 0)},
    'atk2': {'root': (8, 0), 'head': (1, 1), 'm1': (6, 0), 'm2': (10, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -2), 'm1': (-2, 2), 'm2': (1, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'neck', 'neck': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'm1': 'root', 'm2': 'root', 'm3': 'root'}
