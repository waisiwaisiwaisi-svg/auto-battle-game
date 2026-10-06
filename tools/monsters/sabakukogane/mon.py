# サバクコガネ（じめん・むし × スカラベ）手打ち GBA風
import pix
META = dict(id='sabakukogane', name='サバクコガネ', types=['ground', 'bug'], base='スカラベ', size='M')
PAL = {
    'k': '#101018', 'l': '#4a2a16',
    'A': '#f6dc94', 'B': '#c8964a', 'C': '#80522a',      # 砂金の 甲羅
    'Y': '#fff6b0', 'O': '#ff9c2e', 'R': '#c4461e',      # 太陽の 円盤
    'T': '#6ee0cc', 'U': '#1e7c7a',                      # トルコ石
    'w': '#ffffff',
}
LIGHT = set('AYTw')
KEEP_BLACK = set('wT')

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
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'T': 'U'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 前ばね：ひらたい ドーム。すじ（みぞ）と トルコ石の ふちどりは 手で ----
def elytra():
    W = 26; g = pix.grid(W, 16); pix.ellipse(g, 13, 12, 13.2, 12, '#')
    rows = shade(pix.rows_of(g), 'A', 'B', 'C', t=3, lf=2, r=3, b=3)
    g = pix.grid_of(rows)
    # たての みぞ（ドームに そって 曲がる）
    for gx in (6, 11, 16, 21):
        for y in range(2, 12):
            x = gx + (y - 7) * (gx - 13) // 30
            if g[y][x] in 'ABC':
                g[y][x] = 'l' if y > 3 else 'C'
                if g[y][x + 1] in 'BC' and y < 12: g[y][x + 1] = 'A' if y < 7 else 'B'
    # つや
    for (x, y) in ((8, 2), (9, 1), (10, 1), (4, 4), (3, 5)):
        if g[y][x] in 'ABC': g[y][x] = 'w' if (x, y) == (9, 1) else 'A'
    # トルコ石の ふち（すそ）
    for x in range(W):
        if g[12][x] != '.': g[12][x] = 'k'
        if g[13][x] != '.': g[13][x] = 'T' if x % 4 else 'k'
        if g[14][x] != '.': g[14][x] = 'U' if x % 4 else 'k'
        if g[15][x] != '.': g[15][x] = 'l'
    return pix.outline(pix.rows_of(g))

PRO = [
    '....kkkkkk......',
    '..kkAAAAAAkk....',
    '.kAAABBBBBBBkk..',
    'kAABBBBBBBBBBBk.',
    'kABBBlBBBBBBBBk.',
    'kABBBBlBBBBBBCCk',
    'kBBBBBBlBBBBCCCk',
    'kBBBBBBBBBBCCCk.',
    'kCBBBBBBBBCCCk..',
    '.kCCCCCCCCCkk...',
    '..kkkkkkkkk.....',
]
# 頭：くまでの ような ぎざぎざの 盾（頭楯）
# 頭：くまでの ような ぎざぎざの 盾（頭楯）。デフォルメで 大きく（目は 頭の 上に 重ねる）
HEAD = [
    '.....kkkkkkk.......',
    '...kkAAAAAAAkk.....',
    '..kAABBBBBBBBBk....',
    '.kABBBBBBBBBBBBk...',
    'kABBBBBBBBBBBBBAk..',
    'kABBBBBBBBBBBBBBAk.',
    'kBBBBBBBBBBBBBBBCAk',
    'kBBBBBBBBBBBBBBCkk.',
    'kCBBBBBBBBBBBBBBAAk',
    'kCBBBBBBBBBBBBBCCkk',
    'kCBBBBBBBBBBBBCBAAk',
    'kCCBBBBBBBBBBCCCkk.',
    '.kCCBBBBBBBBCCCCAk.',
    '..kCCCkwkwkwkCCCk..',
    '...kkkk.k.k.kkkk...',
]
# 目：まゆの 線＋ハイライト＋トルコ石 2色＋たての ひとみ（前へ むかって 下がる つり目）
EYE = ['kkkkkkk..', 'kwTTTkTkk', 'kTTUUkUk.', '.kkkkkk..']
EYE_ALT = {'blink': ['.........', 'kkkkkkkkk', '.CCCCCC..', '.........'], 'atk0|atk1|atk2': ['kkkkkkk..', 'kwYYYkYkk', 'kYYOOkOk.', '.kkkkkk..'],
           'hit': ['kkkkk...', 'BkBBBkB.', 'BBkBkBB.', '.kBBBk..'], 'ko': ['........', 'BkBkB...', 'BBkBB...', 'BkBkB...']}
# ---- 太陽の 円盤を 三日月の 角が かかえる（あたりは 円、光の 向きで 3段、光線と 角先は 手で）----
def disc(hot=False, turn=0):
    W, H = 25, 24; cx, cy = 12, 10; g = pix.grid(W, H)
    import math
    # 三日月の 角（下 半分を かかえ、先は 上へ とがる）
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if 9.0 <= d <= 11.4 and y >= cy - 2:
                l = -(x - cx) * .7 - (y - cy) * .3
                g[y][x] = 'A' if (d < 9.8 and l > -3) else ('C' if (d > 10.6 or l < -5) else 'B')
    for (x, y, c) in ((2, 7, 'B'), (2, 6, 'A'), (2, 5, 'A'), (3, 4, 'A'), (3, 7, 'A'), (3, 6, 'B'),
                      (22, 7, 'C'), (22, 6, 'C'), (22, 5, 'B'), (21, 4, 'B'), (21, 7, 'B'), (21, 6, 'C')):
        g[y][x] = c
    # 円盤
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if d <= 6.3:
                l = -(x - cx) * .6 - (y - cy) * .8
                if d <= 2.2: g[y][x] = 'Y' if hot else 'O'
                elif d > 5.3: g[y][x] = 'R' if l < 1 else 'O'
                else: g[y][x] = 'Y' if (l > 1.2 or hot) else 'O'
    # 光線：円盤の ふちに くっついた とげ（ゆらぎで 2通り）
    for k in range(8):
        a = k * math.pi / 4 + (math.pi / 8 if turn else 0)
        for r_ in (6.8, 7.8) if k % 2 == 0 else (6.8,):
            x, y = round(cx + r_ * math.cos(a)), round(cy + r_ * math.sin(a))
            if g[y][x] == '.': g[y][x] = 'Y' if r_ > 7 else 'O'
    g[cy][cx] = 'T'; g[cy - 1][cx] = 'Y' if hot else 'U'
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != '.': continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return pix.rows_of(out)
STALK = [
    '..kkkk.',
    '.kABBCk',
    '.kABCk.',
    'kABBCk.',
    'kABCk..',
    'kBBCk..',
    'kkkk...',
]
# 足：太く 短い。前足は くまでの ような 歯
LEG = [
    '.kABBk..',
    '.kABBk..',
    '.kBBCCk.',
    '..kBBCk.',
    '.kkBCkk.',
    '.kBCk...',
    'kBCCk...',
    'kkkk....',
]
LEGR = pix.flip_h(LEG)
RAKE = [
    '.kkk.....',
    'kABBk....',
    'kBBCCk...',
    '.kBBCk...',
    '..kBCkk..',
    '..kBBCCk.',
    '..kBBBCCk',
    '...kCkCkC',
    '...k.k.k.',
]
# 攻撃：砂を かためた 大玉（あたりは 円、すじと 光は 手で）
def ball(phase=0):
    N = 17; c = 8; g = pix.grid(N, N)
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            if d > 8.2: continue
            l = -(x - c) * .6 - (y - c) * .8
            g[y][x] = 'k' if d > 7.3 else ('A' if l > 2.5 else 'C' if l < -2.5 else 'B')
            if d <= 7.3 and (x + y + phase) % 6 == 0 and 2 < d < 7: g[y][x] = 'l'
    for (x, y) in ((5, 4), (6, 3), (4, 6)): g[y][x] = 'Y'
    return pix.rows_of(g)
DUST = ['.B..A...', 'A.k.B..B', '.kBk.kAk', 'BkCBkkBk', '.kkkkkk.']
SWIRL = {'atk0': ['.A..B.', 'B....A', '..kk..', '.kBAk.', '..kk..'], }

HX, HY = 29, 36
def layers():
    A = 'atk1|atk2'
    return [
        dict(n='legF1', g='legB', x=13, y=51, rows=dark(LEG)),
        dict(n='legF2', g='legA', x=23, y=51, rows=dark(LEGR)),
        dict(n='rakeF', g='legB', x=HX + 3, y=HY + 14, rows=dark(RAKE)),
        dict(n='stalk', g='head', x=HX + 6, y=HY - 6, rows=STALK),
        dict(n='disc', g='disc', x=HX - 4, y=HY - 27, rows=disc(), alt={'idle1|idle3|walk1|walk3': disc(False, 1), 'atk0': disc(True, 0), A: disc(True, 1)}),
        dict(n='ely', g='body', x=5, y=35, rows=elytra()),
        dict(n='pro', g='body', x=HX - 5, y=HY - 3, rows=PRO),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD),
        dict(n='eye', g='head', x=HX + 4, y=HY + 5, rows=EYE, alt=EYE_ALT),
        dict(n='leg1', g='legA', x=7, y=52, rows=LEG),
        dict(n='leg2', g='legB', x=17, y=52, rows=LEGR),
        dict(n='rake', g='legA', x=HX - 2, y=HY + 15, rows=RAKE),
        dict(n='swirl', g='head', x=HX + 19, y=HY + 4, rows=SWIRL['atk0'], only='atk0'),
        dict(n='ball', g='root', x=HX + 19, y=HY + 3, rows=ball(), alt={'atk2': ball(3)}, only=A),
        dict(n='dust', g='root', x=HX + 19, y=HY + 14, rows=DUST, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 1), 'disc': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'disc': (0, 2)},
    'idle3': {'disc': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1), 'head': (0, -1), 'disc': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1), 'head': (0, -1), 'disc': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 2), 'disc': (-1, 0)},
    'atk1': {'root': (2, 0), 'head': (1, 0), 'disc': (1, 0)},
    'atk2': {'root': (3, 0), 'head': (2, 0), 'disc': (1, 0), 'ball': (5, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'disc': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'disc': 'head', 'head': 'root', 'body': 'root', 'legA': 'root', 'legB': 'root', 'ball': 'root'}
