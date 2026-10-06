# エンロウ（ほのお・あく × オオカミ）手打ち GBA風
import pix
META = dict(id='enrou', name='エンロウ', types=['fire', 'dark'], base='オオカミ', size='M')
PAL = {
    'k': '#101018', 'l': '#5a1e1a',
    'A': '#7c7490', 'B': '#4a4458', 'C': '#2a2636',
    'S': '#c4bcd0',
    'Y': '#ffe470', 'O': '#ff7a1a', 'R': '#c02a1a',
    'w': '#ffffff',
}
LIGHT = set('ASYw')

def shade(rows, ramps, low=99):
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            hi, mid, lo = ramps[m]
            def e(dy, dx):
                yy, xx = y + dy, x + dx
                return not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m
            a = e(-1, 0) or e(-2, 0) or (e(0, -1) and y < low)
            b = e(1, 0) or e(0, 1) or e(1, 1) or e(0, 2)
            c = lo if y >= low else mid
            if a and not b: c = hi
            elif b and not a: c = lo
            o[y][x] = c
    return pix.rows_of(o)
def put(base, over, x=0, y=0):
    g = pix.grid_of(base); w = max(len(r) for r in over) + x; h = len(over) + y
    if w > len(g[0]): g = [r + ['.'] * (w - len(r)) for r in g]
    while len(g) < h: g.append(['.'] * len(g[0]))
    pix.stamp(g, over, x, y); return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'w': 'B', 'O': 'R'}
def dark(rows): return pix.recolor(rows, DARK)

# ---- 胴：背中の 毛が 後ろへ 逆立つ。ひびの 奥で 熾火が 光る ----
BODY_M = [
    '......#.....#.....#.....',
    '....###...###...###.....',
    '..####################..',
    '.######################.',
    '########################',
    '########################',
    '########################',
    '########################',
    '.#######################',
    '..#####################.',
    '....##################..',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'ABC'}, low=9), [
    '', '', '',
    '..........C.....C',
    '....C....C.....kO',
    '...C....kO....kOY',
    '..C....kOY...kOk',
    '.......kOk...kRk',
    '.......Rk.....k',
]))

# ---- 足（細く 長い。爪は 白）----
HLEG_M = [
    '..#####...',
    '.#######..',
    '#########.',
    '#########.',
    '.#######..',
    '..#####...',
    '..####....',
    '..####....',
    '..####....',
    '..####....',
    '..####....',
    '.######...',
    '.#######..',
]
def notop(r): return ['.' * len(r[0])] + r[1:]
HLEG = notop(pix.outline(put(shade(HLEG_M, {'#': 'ABC'}), [
    '', '', '', '', '', '', '', '', '', '', '', '',
    '..k.k.k',
])))
FLEG_M = [
    '.#####.',
    '######.',
    '######.',
    '.#####.',
    '.####..',
    '.####..',
    '.####..',
    '.####..',
    '.####..',
    '.####..',
    '.#####.',
    '#######',
]
FLEG = notop(pix.outline(put(shade(FLEG_M, {'#': 'ABC'}), [
    '', '', '', '', '', '', '', '', '', '', '',
    '..k.k.k',
])))

# ---- 頭（手打ち）：低い まゆ、熾火の 目、口の すき間が 燃える ----
HEAD = [
    '....kkkkkkk...............',
    '..kkAAAAAAAkkk............',
    '.kAAABBBBBBBBBkk..........',
    'kAABBBBBBBBBBBBBkk........',
    'kABBBBBBBBBBBBBBBBkk......',
    'kABBBBBkkkkkkkkkBBBBkkk...',
    'kABBBBkBBBBBBBkkBBBBBBBkk.',
    'kABBBBkBBBBBBBkAAAAAAAAABk',
    'kBABBBBkkkkkkkBBBBBBBBBBkk',
    'kBCABBBBBBBBBBBBBBBBBkkCCk',
    'kCBCABBBBBBBBBBBBBkkkkkkk.',
    '.kCBCBBBBBBBBBBkOYYYYYOOk.',
    '.kCCBBBBBBBBBBBkkwkwkwkk..',
    'kCBCBBBBBBBBBBBBBBBCCk....',
    '.kCkCCBBBBBBBBBCCCkk......',
    '..k.kkCCCCCCCCCkk.........',
    '......kkkkkkkkk...........',
]
HEAD_OPEN = HEAD[:10] + [
    'kCBCABBBBBBBBBBBkkkwkwkwk.',
    '.kCBCBBBBBBBBBkROOOOOOO...',
    '.kCCBBBBBBBBBkROYYYYYYY...',
    'kCBCBBBBBBBBBBkROOOOOOO...',
    '.kCkCCBBBBBBBBBkkwkwkwk...',
    '..k.kkCCCCCCCCCCCCCk......',
    '......kkkkkkkkkkkkk.......',
]
# 目：まゆの ひさしの 下、白い 光＋熾火の 虹彩（黄・だいだい）＋たての ひとみ
EYE = ['wYYkOkk', 'YOOkOOk']
EYE_ALT = {'blink': ['BBBBBkk', 'kkkkkkk'], 'hit': ['kkBBBkk', 'BBkkkBk'], 'atk0|atk1|atk2': ['wwYkYkk', 'YYOkOOk'], 'ko': ['OkBkOkk', 'BOkOBBk']}
EAR = [
    'k........',
    'kk.......',
    'kAkk.....',
    'kAAAkk...',
    'kAABBBk..',
    '.kAlBBBk.',
    '.kAllBBk.',
    '..kAlBBk.',
    '..kABBk..',
]
EAR_BACK = [
    '.........',
    '.........',
    'kkk......',
    'kAAkkk...',
    '.kAABBkk.',
    '.kAlBBBBk',
    '..kAlBBBk',
    '..kAlBBk.',
    '..kABBk..',
]
# 首の まわりの 逆立つ 毛（えりまき）
RUFF = [
    '......k....',
    '.....kAk...',
    '..k.kABk...',
    '.kAkkABBk..',
    'kABBkABBk..',
    'kABBBBBBCk.',
    '.kBBBBBBCk.',
    'kABBBBBCCk.',
    'kBBBBBBCk..',
    '.kBBBBCCk..',
    'kABBBBCk...',
    '.kBBBCCk...',
    '..kkCCk....',
    '....kk.....',
]
# ---- しっぽ：先が 黒煙に ほどける ----
# しっぽ：黒煙の 大きな 房。先は 白い 煙に ほどけ、根もとに 熾火
def tail(ph):
    W, H = 18, 16; m = pix.grid(W, H)
    tip = (0, 1 + ph)
    pix.poly(m, [(17, 10), (14, 14), (9, 13), (5, 10), tip, (6, 4), (10, 6), (15, 7)], '#')
    pix.poly(m, [(7, 10), (2, 13 - ph), (6, 8)], '#')
    o = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            if m[y][x] != '#': continue
            e = lambda dy, dx: not (0 <= y + dy < H and 0 <= x + dx < W) or m[y + dy][x + dx] != '#'
            c = 'B'
            if e(-1, 0) or e(0, -1): c = 'A'
            if e(1, 0) or e(0, 1) or e(1, 1): c = 'C'
            if x < 5 and (e(-1, 0) or e(0, -1) or e(1, 0)): c = 'S'
            o[y][x] = c
    for (x, y) in ((8, 6), (11, 8), (6, 9)): o[y][x] = 'A'
    o[10][14] = 'R'; o[9][15] = 'O'
    return pix.outline(pix.rows_of(o))
TAIL = tail(0); TAIL2 = tail(1)
# ---- 背中から 立ちのぼる 黒煙と 火の粉 ----
# 背すじの 黒煙の たてがみ：煙の 舌が 後ろへ なびき、根もとで 熾火が 光る
def smoke(ph):
    W, H = 26, 15; out = pix.grid(W, H)
    T = [(22, 14, 18, 2, 6), (16, 14, 10, 0, 7), (11, 14, 4, 2, 7), (6, 14, 0, 7, 6)]
    for i, (bx, by, tx, ty, w) in enumerate(T):
        s = ((i + ph) % 2) * 2 - 1 if ph else 0
        tx += s; dx, dy = tx - bx, ty - by; n = (dx * dx + dy * dy) ** .5; px, py = -dy / n, dx / n
        mx, my = bx + dx * .5 - 1, by + dy * .5
        m = pix.grid(W, H)
        pix.poly(m, [(bx - px * w / 2, by - py * w / 2), (mx - px * w / 3, my - py * w / 3), (tx, ty),
                     (mx + px * w / 3, my + py * w / 3), (bx + px * w / 2, by + py * w / 2)], '#')
        for y in range(H):
            for x in range(W):
                if m[y][x] != '#': continue
                e = lambda dy, dx: not (0 <= y + dy < H and 0 <= x + dx < W) or m[y + dy][x + dx] != '#'
                if y <= ty + 2: c = 'S' if e(-1, 0) or e(0, -1) else 'A'
                elif e(-1, 0) or e(0, -1): c = 'A'
                elif e(1, 0) or e(0, 1): c = 'C'
                else: c = 'B'
                core = not (e(0, -1) or e(0, 1) or e(0, -2) or e(0, 2))
                if y >= H - 3 and core: c = 'Y' if (x * 7 + y * 3 + ph) % 5 == 0 else 'O' if (x + y + ph) % 2 else 'R'
                elif y == H - 4 and core: c = 'R'
                out[y][x] = c
    return pix.outline(pix.rows_of(out))
SMOKE = smoke(0); SMOKE2 = smoke(1)
# ---- 熾火の ブレス（攻撃）----
BREATH = [
    '..............kk.........',
    '.........kk..kROk...kk...',
    '.....kk.kROkkROOkk.kROk..',
    '..kkkROkROOOOOYOOkkROOk..',
    'kkROOOOOOYYYYYYYYOOOOYOk.',
    'kOYYYYYYYYYYYwwYYYYYYOk..',
    'kOYYwwwwwYYYYwwwYYYYYOOk.',
    'kOYYYYYYYYYYYYYYYYYOOk...',
    'kkROOOOYYYYYYOOOOOOROk...',
    '..kkkROOkkROOOkkROOkk....',
    '.....kkk..kRk..kkkk......',
    '...........k.............',
]
BREATH2 = [
    '...........kk....kSk.......',
    '.....kk...kROk..kSSk..kk...',
    '..kkkROk.kROOk.kSkk..kSSk..',
    'kkROOOOkkROYOOkkkROk.kSk...',
    'kOYYYOOOOOYYYOOOOROOk.kk...',
    'kOYYYYYOOYYYYYOOkkROOk.....',
    'kOYYYYYYYYYOOOkkROOkkSSk...',
    'kROOYYOOOOOOOkROOk..kSSk...',
    '.kkROOkkROOOkkRkk....kk....',
    '...kkk..kkRk..k....kk......',
    '.........kk.......kSSk.....',
    '...................kk......',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=-2, y=25, rows=TAIL, alt={'idle1|idle2|walk1|walk3': TAIL2}),
        dict(n='hlegF', g='legB', x=17, y=46, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=34, y=46, rows=dark(FLEG), not_='ko'),
        dict(n='body', g='body', x=9, y=34, rows=BODY),
        dict(n='hleg', g='legA', x=10, y=46, rows=HLEG, not_='ko'),
        dict(n='fleg', g='legA', x=29, y=46, rows=FLEG, not_='ko'),
        dict(n='smoke', g='mane', x=8, y=23, rows=SMOKE, alt={'idle1|idle3|walk1|walk3|atk1': SMOKE2}),
        dict(n='ruff', g='head', x=28, y=27, rows=RUFF),
        dict(n='ear', g='ear', x=33, y=14, rows=EAR, alt={'atk0|atk1|atk2|hit|ko': EAR_BACK}),
        dict(n='head', g='head', x=31, y=21, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='eye', g='head', x=38, y=27, rows=EYE, alt=EYE_ALT),
        dict(n='breath', g='head', x=53, y=29, rows=BREATH, alt={'atk2': BREATH2}, only=NB),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, -1)},
    'idle2': {'body': (0, 1), 'ear': (0, -1)},
    'idle3': {'body': (0, 0)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'legA': (-1, 0), 'tail': (1, -1)},
    'atk1': {'root': (2, 0), 'head': (1, -1)},
    'atk2': {'root': (3, 0), 'head': (1, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'ear': (0, 0)},
    'ko': {'body': (0, 12), 'head': (1, 2), 'tail': (0, 1)},
}
PARENT = {'mane': 'body', 'head': 'body', 'ear': 'head', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
