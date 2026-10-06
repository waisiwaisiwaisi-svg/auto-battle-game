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

# ---- 胴：肩が もり上がった 前のめりの 体（あたりは 多角形）→ ぬれた 毛の たば・筋肉・きずあとは 手で ----
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, poly, outline, rows_of
def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def body():
    W, H = 34, 30; g = grid(W, H)
    poly(g, [(0, 16), (2, 9), (7, 5), (13, 3), (19, 0), (25, 1), (30, 6), (33, 13), (32, 22), (28, 28), (20, 26), (14, 29), (4, 29), (0, 23)], '#')
    # 背中の ぬれた 毛の たば（後ろへ とがる）
    for (x, y) in ((5, 6), (6, 5), (10, 3), (11, 2), (16, 1), (17, 0)):
        if 0 <= y < H: g[y][x] = '#'
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 4 or rt <= 2: c = 'H'
            elif dn == 5 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 4): c = 'F'
            if x >= 27 and y >= 16 and c == 'G' and (x + y) % 2: c = 'H'      # 頭の 下の 影（ディザ）
            out[y][x] = c
    # 毛の すじ（後ろ下へ ながれる）
    for (x, y) in ((8, 7), (9, 8), (13, 5), (14, 6), (19, 3), (20, 4), (24, 4), (25, 5), (5, 11), (6, 12), (11, 10), (12, 11), (17, 8), (18, 9)):
        if out[y][x] == 'G': out[y][x] = 'H'
        if out[y][x - 1] == 'G': out[y][x - 1] = 'F'
    # ももの 筋肉（大きな 弧）
    for (x, y) in ((10, 13), (9, 14), (8, 15), (8, 16), (8, 17), (8, 18), (9, 19), (10, 20), (11, 21), (12, 22), (13, 23)):
        out[y][x] = 'l'
        if out[y][x + 1] == 'G': out[y][x + 1] = 'F'
    # 肩の きずあと（3本の 爪あと）
    for i in range(3):
        for j in range(5):
            x, y = 19 + i * 2 + j // 2, 6 + j + i
            out[y][x] = 'l'
            if out[y][x - 1] in 'GH': out[y][x - 1] = 'N'
    # 水てき
    for (x, y) in ((9, 5), (15, 2), (4, 10), (26, 4)):
        out[y][x] = 'C'; out[y + 1][x] = 'A'
    return outline(rows_of(out))

# 頭：低く 前へ つき出す。重い まゆの ひさし・きずあと・するどい 目・大きな のみの 歯
HEAD = [
    '..kk..kkkkkk...........',
    '.kFHkkFFFFFFkk.........',
    '.kGHkFGGGGGGFFkk.......',
    'kFGGGGGGGGGGGGGFkk.....',
    'kFGGGGGGGNkkkkkkGFkk...',
    'kGGGGGGGkNlHHHHHkkGFk..',
    'kGGGGGGkHHl......HkGFk.',
    'kGGGGGGGkkkN......GGGFk',
    'kGGGGGGGGGGlNGGGNNNNkkk',
    'kHGGGGGGGGGGlGNNNNNNkkk',
    'kHGGGGGGGGGGGNNNNNNNLLk',
    '.kHGGGGGGGGGGGNNNNLLLk.',
    '.kHHGGGGGGGkkkkkkkkkk..',
    '..kHHGGGGGkYYYkYTk.....',
    '...kkHHHHkYYYYkYTTk....',
    '.....kkkkkYYYTkYTTk....',
    '.........kYYYTkYTTk....',
    '.........kYYTTkTTTk....',
    '.........kYYTTkTTk.....',
    '..........kkkkkkk......',
]
TEETH_GLINT = ['w', 'w', 'w']
EYE = ['CCAkAk', '.kkkkk']
EYE_ALT = {'blink': ['kkkkkk', '.GGGGk'], 'atk0|atk1|atk2': ['wCCkCk', '.kkkkk'], 'hit': ['kkAkkk', '.kkkkk'], 'ko': ['AkAkAk', '.kAkGk']}
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
    '.kkkkkkk..',
    'kFGGGGGHk.',
    'kFGGGGGHHk',
    'kFGGGGGHHk',
    '.kFGGGGHHk',
    '.kFGGGGHk.',
    '.kFGGGHHk.',
    '.kGGGGHHk.',
    '.kFGGGGHHk',
    'kFGGGGGHHk',
    'kGGGlGGlHk',
    'kHHHlHHlHk',
    'kwkkwkkwk.',
]
HLEG = [
    '..kkkkkk.....',
    '.kGGGGGHk....',
    'kGGGGGGHHk...',
    'kGGGGHHHHkk..',
    'kHHHHHHHHHHk.',
    'kHAAkHAAkHBBk',
    'kkkkkkkkkkkkk',
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
        dict(n='puddle', g='root', x=1, y=58, rows=PUDDLE, alt={'idle1|idle3|walk1|walk3': PUDDLE2}, not_='ko'),
        dict(n='tail', g='tail', x=0, y=40, rows=TAIL, not_='atk0'),
        dict(n='tailup', g='tail', x=3, y=21, rows=TAIL_UP, only='atk0'),
        dict(n='drip', g='tail', x=3, y=49, rows=DRIP, alt={'idle1|idle3|walk1|walk3': DRIP2}, not_='atk0|atk1|atk2|ko'),
        dict(n='splash', g='root', x=0, y=36, rows=SPLASH, only='atk1'),
        dict(n='legHF', g='legB', x=17, y=53, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=40, y=47, rows=dark(FLEG)),
        dict(n='body', g='body', x=9, y=26, rows=BODY),
        dict(n='legH', g='legA', x=9, y=53, rows=HLEG),
        dict(n='legF', g='legB', x=33, y=47, rows=FLEG),
        dict(n='head', g='head', x=34, y=33, rows=HEAD),
        dict(n='eye', g='head', x=44, y=39, rows=EYE, alt=EYE_ALT),
        dict(n='glint', g='head', x=45, y=47, rows=TEETH_GLINT, only='atk0|atk1'),
        dict(n='wave', g='fx', x=50, y=50, rows=WAVE, alt={'atk2': WAVE2}, only='atk1|atk2'),
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
