# ハガネハリネズ（はがね × ハリネズミ）手打ち GBA風
META = dict(id='haganeharinezu', name='ハガネハリネズ', types=['steel'], base='ハリネズミ', size='S')
PAL = {
    'k': '#101018', 'l': '#3a1a2c',
    'S': '#f4f6fa', 'T': '#a9b1c0', 'U': '#5a6070', 'C': '#9ef0ff',
    'F': '#c48a8a', 'G': '#8a4a5c', 'H': '#4e2438',
    'R': '#ff2e3e', 'Y': '#ffe04a', 'w': '#ffffff',
}
LIGHT = set('SCFYw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out

# ---- 刃の 針：1本ずつ 根もと・先・はばを 手で 決めて、奥から 手前へ 重ねる（1本ごとに 輪郭）----
BLADES = [  # (根もと x, y), (先 x, y), はば
    ((12, 27), (4, 24), 3), ((12, 23), (3, 15), 3), ((15, 19), (7, 7), 3), ((19, 17), (13, 2), 3),
    ((23, 16), (21, 0), 3), ((27, 17), (28, 2), 3), ((30, 19), (34, 9), 3),
    ((15, 26), (6, 20), 3), ((18, 22), (9, 13), 3), ((22, 20), (16, 7), 3), ((26, 20), (24, 6), 3),
    ((29, 22), (30, 11), 3), ((32, 24), (36, 16), 2),
]
FLARE = [  # 逆立てた 針（攻撃）：長く、上へ
    ((12, 27), (3, 20), 3), ((12, 23), (3, 10), 3), ((15, 19), (8, 2), 3), ((19, 17), (15, -3), 3),
    ((23, 16), (24, -4), 3), ((27, 17), (32, -1), 3), ((30, 19), (38, 6), 3),
    ((15, 26), (5, 16), 3), ((18, 22), (10, 8), 3), ((22, 20), (18, 3), 3), ((26, 20), (27, 3), 3),
    ((29, 22), (33, 9), 3), ((32, 24), (39, 15), 2),
]
def quills(bl, oy=4):
    W, H = 46, 36; g = [['.'] * W for _ in range(H)]
    for (bx, by), (tx, ty), w in bl:
        by += oy; ty += oy
        ax, ay = tx - bx, ty - by; L = (ax * ax + ay * ay) ** .5; ux, uy = ax / L, ay / L
        nx, ny = -uy, ux
        if nx + ny > 0: nx, ny = -nx, -ny   # n は 光（左上）の 側
        t = [['.'] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                px, py = x + .5 - bx, y + .5 - by
                a = (px * ux + py * uy) / L; d = px * nx + py * ny
                if not (-.15 <= a <= 1): continue
                hw = w * (1 - a) + .35
                if abs(d) > hw: continue
                s = d / hw
                c = 'S' if s > .3 else ('T' if s > -.35 else 'U')
                if a > .72 and s > -.2: c = 'S'
                if a < .12: c = 'U' if s < .3 else 'T'
                t[y][x] = c
        t = _ol(t)
        for y in range(H):
            for x in range(W):
                if t[y][x] != '.': g[y][x] = t[y][x]
    return g
def quill_rows(bl, glint=()):
    g = quills(bl)
    for (x, y) in glint:
        if g[y][x] in 'ST': g[y][x] = 'C'
    return [''.join(r) for r in g]
QUILL = quill_rows(BLADES, ((8, 12), (15, 7), (23, 6), (11, 26), (29, 9)))
QUILL2 = quill_rows(BLADES, ((7, 13), (14, 8), (22, 7), (10, 27), (30, 10), (34, 18)))
QFLARE = quill_rows(FLARE, ((6, 9), (15, 3), (24, 2), (7, 22), (33, 7), (37, 15)))

# ---- 体と 頭（手打ち）----
BODY = [
    '........kkkkkkkkkkkkkkkk.........',
    '.....kkkHHHHHHHHHHHHHHHHkkk......',
    '...kkHHHGHHHGHHHHGHHHHGHHHHkk....',
    '..kHHGGGGGGGGGGGGGGGGGGGGGGHHk...',
    '.kHGGGGHGGGGGHGGGGGHGGGGGGGGHHk..',
    'kHGGGGGGGGGGGGGGGGGGGGGGGGGGGHk..',
    'kHGGGFGGGFGGGGFGGGGFGGGGGGGGHHk..',
    'kHHGGFFFFFFFFFFFFFFFFGGGGGGHHk...',
    '.kHHHGFFFGFFFFGFFFFGFGGGGGHHk....',
    '..kHHHGGFFGFFFFGFFFGGGGGHHHk.....',
    '...kkHHHHGGGGGGGGGGGGGHHHkk......',
    '.....kkkkHHHHHHHHHHHHHHkk........',
    '.........kkkkkkkkkkkkkk..........',
]
HEAD = [
    '...kkkkk........',
    '.kkGGGGGkkk.....',
    'kGGGGGGGGGGkk...',
    'kGGGkkkkkkGGGkk.',
    'kGFFFFFFFFkkGGGk',
    'kGFFFFFFFFFFkkGGk',
    'kFFFFFFFFFFFFFkkk',
    'kFFFFFFFkkkkkkkHk',
    'kFFFFFFkwRwRwkk..',
    '.kFFFFFkkwkwk....',
    '..kHHHHHHkk......',
    '...kkkkkk........',
]
# つり目：まゆの 黒線の 下で 赤く 光る、たての ひとみ
EYE = ['kYYRRk', '.kRkk.']
EYE_ALT = {'blink': ['kkkkkk', '.FFFF.'], 'atk0|atk1|atk2': ['kYYYYk', '.kYkk.'], 'hit': ['kRkkRk', '.FkkF.'], 'ko': ['FkFkFF', 'FFkFFF']}
NOSE = ['kk', 'kU']
LEG = ['.kkkk.', 'kGGGHk', 'kGGHHk', 'kGHHHk', 'kHHHHk', 'kSkSkk']
LEGF = ['.kkkk..', 'kFGGHk.', 'kGGGHk.', 'kGGHHk.', 'kGHHHkk', 'kSkSkSk']
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 飛ばす 刃（攻撃）
SHOT = ['kkk......', 'kSSkkk...', '.kTTSSSkk', '.kTTTTUUk', 'kUUUkkk..', 'kk.......']
STREAK = ['TT.TTT', '......', '.TTT..']

def layers():
    return [
        dict(n='legBF', g='legB', x=24, y=54, rows=dark(LEG)),
        dict(n='legFF', g='legA', x=42, y=54, rows=dark(LEG)),
        dict(n='body', g='body', x=12, y=46, rows=BODY),
        dict(n='quill', g='quill', x=6, y=20, rows=QUILL, alt={'idle1|idle3|walk1|walk3': QUILL2, 'atk0|atk1|atk2': QFLARE}),
        dict(n='legB', g='legA', x=19, y=55, rows=LEG),
        dict(n='legF', g='legB', x=38, y=54, rows=LEGF),
        dict(n='head', g='head', x=36, y=41, rows=HEAD),
        dict(n='eye', g='head', x=39, y=45, rows=EYE, alt=EYE_ALT),
        dict(n='shot1', g='fx', x=50, y=28, rows=SHOT, only='atk1|atk2'),
        dict(n='shot2', g='fx2', x=54, y=35, rows=SHOT, only='atk1|atk2'),
        dict(n='streak1', g='fx', x=43, y=29, rows=STREAK, only='atk1'),
        dict(n='streak2', g='fx2', x=47, y=36, rows=STREAK, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'quill': (0, -1)},
    'idle2': {'body': (0, 1)},
    'idle3': {'body': (0, 1), 'quill': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1)},
    'atk1': {'body': (1, 0), 'fx': (0, 0), 'fx2': (0, 0)},
    'atk2': {'body': (1, 0), 'fx': (8, -2), 'fx2': (6, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -2), 'quill': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'quill': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root', 'fx2': 'root'}
