# キババーバー（ノーマル・みず × ビーバー）手打ち GBA風
META = dict(id='kibabeaver', name='キババーバー', types=['normal', 'water'], base='ビーバー', size='M')
PAL = {
    'k': '#101018', 'l': '#42201c',
    'F': '#cc7a4e', 'G': '#8c4630', 'H': '#4e2420',
    'Y': '#ffd47a', 'T': '#f08a22',
    'N': '#b49a72', 'L': '#6e5a42', 'M': '#3e3226',
    'C': '#e6fbff', 'A': '#5cc6f0', 'B': '#2470c0',
    'w': '#ffffff',
}
LIGHT = set('FYNCw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, ramp='FGH', lit=1, dk=2):
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
            c = ramp[1]
            if dd <= dk: c = ramp[2]
            elif du <= lit or dl <= 1: c = ramp[0]
            elif dr <= 1: c = ramp[2]
            g[y][x] = c
    return g
def rot90(rows):
    h, w = len(rows), max(len(r) for r in rows); rows = [r.ljust(w, '.') for r in rows]
    return [''.join(rows[h - 1 - y][x] for y in range(h)) for x in range(w)]

# ---- 胴：まるく 盛り上がった 背中。ぬれた 毛の すじと 水てきは 手で ----
SPAN = [(12, 20), (8, 24), (6, 26), (4, 27), (3, 28), (2, 29), (1, 29), (0, 30), (0, 30), (0, 30), (0, 30), (0, 30),
        (0, 30), (0, 30), (0, 30), (1, 30), (2, 29), (3, 28), (5, 27), (8, 25)]
def body():
    g = shade(SPAN, 31, 'FGH', lit=2, dk=3)
    for (x, y) in ((8, 4), (9, 5), (9, 6), (14, 3), (15, 4), (15, 5), (20, 4), (21, 5), (21, 6), (5, 8), (6, 9), (11, 9), (12, 10), (17, 8),
                   (18, 9), (23, 8), (24, 9), (4, 12), (9, 13), (14, 12), (15, 13), (20, 12), (25, 12)):
        if g[y][x] == 'G': g[y][x] = 'H'
    for (x, y) in ((7, 4), (13, 3), (19, 3), (4, 7), (10, 8), (16, 7), (22, 7), (3, 11), (8, 12), (13, 11), (19, 11)):
        if g[y][x] == 'G': g[y][x] = 'F'
    for (x, y) in ((11, 2), (17, 2), (6, 5)):   # 水てきの つや
        g[y][x] = 'C'; g[y + 1][x] = 'A'
    return [''.join(r) for r in _ol(g)]

# 頭：太い まゆ、小さな 耳、つき出た オレンジの のみの 歯
HEAD = [
    '....kkkkkk........',
    '..kkFFFFFGkk......',
    '.kFFkkFGGGGGkk....',
    'kFFkGHkGGGGGGGk...',
    'kFGkkkGGGGHGGGGk..',
    'kFGFkkkkkGGHGGGGk.',
    'kFGGGGGGGGGGHGGGGk',
    'kGGGGGGGGGGGGHGGHk',
    'kGGGGGGGGGGGGGGkkk',
    '.kGGGGGGGGGGGGHHHk',
    '.kHGGGGGGGGkkkkkk.',
    '..kHHGGGGGkYYYTk..',
    '...kkHHHHHkYYTTk..',
    '.....kkkkkkYYTTk..',
    '..........kYYTTk..',
    '..........kYTTk...',
    '..........kkkk....',
]
TEETH_GLINT = ['w', 'w', 'w']
EYE = ['CAAkk', '.AAAk', '..kk.']
EYE_ALT = {'blink': ['kkkkk', '.GGGk', '..GG.'], 'atk0|atk1|atk2': ['CCCkk', '.CCCk', '..kk.'], 'hit': ['AkkAk', '.kAkk', '..GG.'], 'ko': ['AkAkk', '.kAkk', '.AkA.']}
# 丸太の しっぽ：木の 皮の すじ と 切り口の 年輪
TAIL = [
    '..kkkkkkkkkkkkkk..',
    '.kNkkNLLNNNkLLNLk.',
    'kNkNNkLLLLLkLLLMk.',
    'kNkNYkkLLMLkLLMMk.',
    'kNkNNkLLLLLLkLMMk.',
    'kNNkkLLMLLLLkMMMk.',
    'kLMMMMkMMMMMkMMMk.',
    '.kMMMMMMMMMMMMMk..',
    '..kkkkkkkkkkkkk...',
]
TAIL_UP = rot90(TAIL)
DRIP = ['C.', 'A.', '..', '.A', '.B']
DRIP2 = ['..', 'C.', 'A.', '..', '.A']
FLEG = [
    '.kkkkk.',
    'kFGGGHk',
    'kFGGGHk',
    'kGGGHHk',
    'kGGGHHk',
    'kGGHHHk',
    'kHHHHHkk',
    'kwkwkwk.',
]
HLEG = [
    '.kkkkkk...',
    'kFGGGGHk..',
    'kFGGGGHk..',
    'kGGGGHHk..',
    'kGGGHHHk..',
    '.kGGHHk...',
    'kGGHHHHkk.',
    'kHAkHAkHBk',
    'kkkkkkkkkk',
]
PUDDLE = ['..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..', '.kAACCAAAAAACCAAAAAAAACCAAAAAAAACAABk.', '..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..']
PUDDLE2 = ['..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..', '.kAAAACCAAAAAAAACCAAAAAAACCAAAAAAAABk.', '..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk..']
# 攻撃：しっぽで たたいて 前へ 走る 大波
WAVE = [
    '.....kkkk.....',
    '...kkCCCAkk...',
    '..kCCAAAAABk..',
    '.kCAAABBkkABk.',
    '.kCAABk...kk..',
    'kCAABBk.......',
    'kAABBBBk......',
    'kABBBBBBkkk...',
    'kkkkkkkkkkk...',
]
WAVE2 = [
    '......kkkk......',
    '....kkCCCAkk....',
    '...kCCAAAAABk...',
    '..kCAAABBkkABk..',
    '.kCAAABk...kABk.',
    '.kCAABBk....kk..',
    'kCAABBBBk.......',
    'kAABBBBBBkk.....',
    'kABBBBBBBBBkkk..',
    'kkkkkkkkkkkkkk..',
]
SPLASH = ['C...A..C', '.A.C..A.', 'A..A.C..', '.C...A.A']
DARK = {'F': 'G', 'G': 'H', 'H': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    return [
        dict(n='puddle', g='root', x=4, y=58, rows=PUDDLE, alt={'idle1|idle3|walk1|walk3': PUDDLE2}, not_='ko'),
        dict(n='tail', g='tail', x=1, y=44, rows=TAIL, not_='atk0'),
        dict(n='tailup', g='tail', x=8, y=25, rows=TAIL_UP, only='atk0'),
        dict(n='drip', g='tail', x=4, y=53, rows=DRIP, alt={'idle1|idle3|walk1|walk3': DRIP2}, not_='atk0|atk1|atk2|ko'),
        dict(n='splash', g='root', x=0, y=40, rows=SPLASH, only='atk1'),
        dict(n='legHF', g='legB', x=21, y=52, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=41, y=53, rows=dark(FLEG)),
        dict(n='body', g='body', x=13, y=34, rows=BODY),
        dict(n='legH', g='legA', x=13, y=52, rows=HLEG),
        dict(n='legF', g='legB', x=35, y=53, rows=FLEG),
        dict(n='head', g='head', x=37, y=30, rows=HEAD),
        dict(n='eye', g='head', x=42, y=36, rows=EYE, alt=EYE_ALT),
        dict(n='glint', g='head', x=48, y=41, rows=TEETH_GLINT, only='atk0|atk1'),
        dict(n='wave', g='fx', x=54, y=48, rows=WAVE, alt={'atk2': WAVE2}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'tail': (0, 0)},
    'idle3': {'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'tail': (0, -1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'tail': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, -1), 'head': (-1, -1)},
    'atk1': {'root': (3, 0), 'tail': (0, 2), 'head': (1, 1)},
    'atk2': {'root': (4, 0), 'tail': (0, 2), 'fx': (4, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'tail': (0, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
