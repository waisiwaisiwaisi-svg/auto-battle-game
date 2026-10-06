# ヒトクイソウ（くさ・どく × 食虫植物）手打ち GBA風
META = dict(id='hitokuisou', name='ヒトクイソウ', types=['grass', 'poison'], base='食虫植物', size='M')
PAL = {
    'k': '#101018', 'l': '#1c3020',
    'F': '#a6e050', 'G': '#4e9c34', 'H': '#22562a',
    'P': '#cc84ea', 'Q': '#7c3ca2', 'Z': '#3c1a56',
    'E': '#eeff5c', 'R': '#c41e3e', 'w': '#ffffff',
    'S': '#8e6c4a', 'T': '#4c3828',
}
LIGHT = set('FPESw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out

# ---- 毒の ふくろ（球根の 体）：左上が 明るい 球、光る 斑点と すじは 手で ----
def bulb():
    W, H = 24, 19; cx, cy, rx, ry = 11.5, 9.5, 11.6, 9.4
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if nx * nx + ny * ny > 1: continue
            l = -nx * .6 - ny * .8
            g[y][x] = 'P' if l > .45 else ('Z' if l < -.4 else 'Q')
    for (x, y) in ((6, 6), (13, 4), (17, 9), (8, 12), (14, 13), (4, 10)):   # 光る 毒の 斑点
        g[y][x] = 'E'; g[y][x + 1] = 'E'
        for (dx, dy) in ((-1, 0), (2, 0), (0, 1), (1, 1), (0, -1), (1, -1)):
            if g[y + dy][x + dx] in 'PQ': g[y + dy][x + dx] = 'Z'
    for (x, y) in ((11, 1), (11, 2), (10, 3), (19, 5), (20, 6), (3, 6), (2, 7)):   # すじ
        if g[y][x] in 'PQ': g[y][x] = 'Z'
    return [''.join(r) for r in _ol(g)]

# ---- くき：中心の 道すじ（ポーズごとに 手で）→ 太い 管＋とげ ----
def stem(path, r=2.4):
    W = H = 64; g = [['.'] * W for _ in range(H)]
    for y in range(10, 50):
        for x in range(10, 60):
            best = None
            for (ax, ay), (bx, by) in zip(path, path[1:]):
                dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
                t = max(0, min(1, ((x + .5 - ax) * dx + (y + .5 - ay) * dy) / L2))
                px, py = ax + t * dx - (x + .5), ay + t * dy - (y + .5)
                d = (px * px + py * py) ** .5
                if best is None or d < best[0]:
                    L = L2 ** .5; nx, ny = -dy / L, dx / L
                    if nx + ny > 0: nx, ny = -nx, -ny
                    best = (d, -(px * nx + py * ny), nx, ny)
            if best[0] <= r:
                s = best[1] / r
                g[y][x] = 'F' if s > .4 else ('G' if s > -.4 else 'H')
    # とげ：道すじの 曲がり角の 光側へ 2ドット
    for (ax, ay), (bx, by) in zip(path[1:-1], path[2:]):
        dx, dy = bx - ax, by - ay; L = (dx * dx + dy * dy) ** .5; nx, ny = -dy / L, dx / L
        if nx + ny > 0: nx, ny = -nx, -ny
        for k in (3.4, 4.4):
            X, Y = int(ax + nx * k), int(ay + ny * k)
            if g[Y][X] == '.': g[Y][X] = 'F'
    return [''.join(r) for r in _ol(g)]
P_IDLE = [(24, 46), (25, 40), (27, 35), (31, 31), (36, 28)]
P_BACK = [(24, 46), (23, 40), (23, 35), (25, 31), (29, 27)]
P_LUNGE = [(24, 46), (27, 41), (33, 37), (40, 34), (46, 32)]
P_KO = [(24, 46), (27, 40), (32, 38), (37, 41), (41, 49)]
STEM, STEM_B, STEM_L, STEM_K = stem(P_IDLE), stem(P_BACK), stem(P_LUNGE), stem(P_KO)

# 頭：横に さける 種の さや。上の さやに つり目、口には とげの 歯
HEAD = [
    '.....kkkkkkk..........',
    '...kkFFFFFFGkkk.......',
    '..kFFFGGGGGGGGGkk.....',
    '.kFFGGkkkkGGGGGGGkk...',
    '.kFGGkGGGkkGGGGGGGGk..',
    'kFGGGGkkkGGHGGGGHGHHk.',
    'kFGGHGGGGGHGGGGHGGHHHk',
    'kGGGHGGGGHHHHHHHHHkkkk',
    'kGGGGGGkkkkkkkkkkkwkw.',
    'kHGGGGkwkwkRRRRRRRk...',
    '.kHGGGGkkwkwkwkwkk....',
    '.kHHGGGGGGGGHHHk......',
    '..kHHHHHHHHHHk........',
    '...kkkkkkkkkk.........',
]
HEAD_OPEN = HEAD[:8] + [
    'kGGGGGGkkkkkkkkkkkkkk.',
    'kHGGGGkwRwRRwRRwRRwk..',
    '.kHGGkRRRRRRRRRRRRk...',
    '.kHGGkRRRRRRRRRRRk....',
    '.kHGGGkwRRwRRwRRwk....',
    '..kHGGGkkkkkkkkkk.....',
    '..kHHHHHHHHHHk........',
    '...kkkkkkkkkk.........',
]
EYE = ['EEk', 'kE.']
# 頭の 後ろの がく（とがった 葉が 扇の ように 開く。先は 毒の 紫）
SEP_UL = ['kk.....', 'kQk....', '.kFGk..', '.kFGGk.', '..kGGHk', '...kHHk', '....kk.']
SEP_L = ['...kkkk...', '.kkFFGGkk.', 'kQFGGGGHHk', '.kkHHHHkk.', '...kkkk...']
SEP_DL = ['....kk.', '...kGHk', '..kGGHk', '.kFGHk.', '.kGHk..', 'kQk....', 'kk.....']
EYE_ALT = {'blink': ['kkk', 'GG.'], 'atk0|atk1|atk2': ['wEk', 'kw.'], 'hit': ['kEk', 'Ek.'], 'ko': ['kGk', 'Gk.']}
LEAF = [
    'kk...........',
    'kFkk.........',
    '.kFFkkk......',
    '.kFGFFGkkk...',
    '..kGGFGGGGkk.',
    '..kHGGFGGGGHk',
    '...kHHGGFGHk.',
    '....kkHHHHk..',
    '......kkkk...',
]
LEAF_R = [r[::-1] for r in LEAF]
SOIL = [
    '..........kkkkkkkkkkkkk.........',
    '.....kkkkkSSSSSSSSSSSSSkkkkk....',
    '..kkkSSSSSSSTSSSSSTSSSSSSSSSkk..',
    'kkSSTSSTTTTSSTTTTSTTTTSSTTTTSTkk',
    'kTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTk',
    'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',
]
ROOT_L = ['...kk', '.kkHk', 'kHHk.', 'kHk..', 'kk...']
ROOT_R = [r[::-1] for r in ROOT_L]
DROP = ['P.', 'Q.', '..', '.P']
DROP2 = ['..', 'P.', 'Q.', '..']
SPIT = [
    '......kk.....',
    '..kk.kPQk..k.',
    '.kPQk.kk..kPk',
    '..kk...kk..k.',
    '......kEPk...',
    '.kk....kk....',
    'kPQk......kk.',
    '.kk......kPQk',
    '..........kk.',
]
SPIT2 = [
    '...........kk',
    '.kk.......kPk',
    'kPk...kk...k.',
    '.k...kPQk....',
    '......kk.....',
    '...........kk',
    '..kk......kPk',
    '.kPk.......k.',
    '..k..........',
]

BULB = bulb()
def head_layers(x, y, head, eye, eyealt, only=None, not_=None, halt=None):
    ls = [dict(n='sepU', g='stem', x=x - 5, y=y - 3, rows=SEP_UL), dict(n='sepL', g='stem', x=x - 8, y=y + 4, rows=SEP_L),
          dict(n='sepD', g='stem', x=x - 4, y=y + 8, rows=SEP_DL),
          dict(n='head', g='stem', x=x, y=y, rows=head, alt=halt or {}), dict(n='eye', g='stem', x=x + 6, y=y + 4, rows=eye, **eyealt)]
    for l in ls:
        if only: l['only'] = only
        if not_: l['not_'] = not_
    return ls
def layers():
    return [
        dict(n='leafL', g='leaf', x=2, y=44, rows=LEAF),
        dict(n='stem', g='stem', x=0, y=0, rows=STEM, alt={'atk0': STEM_B, 'atk1|atk2': STEM_L, 'ko': STEM_K}),
        dict(n='bulb', g='body', x=12, y=38, rows=BULB),
        dict(n='leafR', g='leaf2', x=34, y=46, rows=LEAF_R),
        dict(n='soil', g='root', x=7, y=55, rows=SOIL),
        dict(n='rootL', g='leaf', x=4, y=56, rows=ROOT_L),
        dict(n='rootR', g='leaf2', x=37, y=56, rows=ROOT_R),
        *head_layers(34, 18, HEAD, EYE, dict(alt={'blink': ['kkk', 'GG.'], 'hit': EYE_ALT['hit'], 'ko': EYE_ALT['ko']}), not_='atk0|atk1|atk2|ko'),
        dict(n='drop', g='stem', x=46, y=31, rows=DROP, alt={'idle1|idle3|walk1|walk3': DROP2}, not_='atk0|atk1|atk2|ko'),
        *head_layers(40, 46, HEAD, ['kFk', 'FkF'], {}, only='ko'),
        *head_layers(27, 17, HEAD, EYE_ALT['atk0|atk1|atk2'], {}, only='atk0'),
        *head_layers(44, 21, HEAD_OPEN, EYE_ALT['atk0|atk1|atk2'], {}, only='atk1|atk2', halt={'atk2': HEAD}),
        dict(n='spit', g='fx', x=64, y=26, rows=SPIT, alt={'atk2': SPIT2}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'stem': (0, 1), 'body': (0, 0)},
    'idle2': {'stem': (1, 1), 'body': (0, 1), 'leaf': (0, -1)},
    'idle3': {'stem': (1, 0), 'leaf2': (0, -1)},
    'blink': {},
    'walk0': {'stem': (-1, 0), 'leaf': (0, -1), 'leaf2': (1, 0)},
    'walk1': {'stem': (0, 1), 'body': (0, 1)},
    'walk2': {'stem': (1, 0), 'leaf': (-1, 0), 'leaf2': (0, -1)},
    'walk3': {'stem': (0, 1), 'body': (0, 1)},
    'atk0': {'body': (0, 1), 'leaf': (0, -1), 'leaf2': (0, -1)},
    'atk1': {'body': (1, 0)},
    'atk2': {'fx': (6, 2)},
    'hit': {'stem': (-3, -1), 'body': (-1, 0)},
    'ko': {'body': (0, 1), 'leaf': (0, 2), 'leaf2': (0, 2)},
}
PARENT = {'stem': 'body', 'body': 'root', 'leaf': 'root', 'leaf2': 'root', 'fx': 'root'}
