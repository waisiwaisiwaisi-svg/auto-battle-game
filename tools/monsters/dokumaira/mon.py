# ドクマイラ（どく・ドラゴン × キマイラ）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='dokumaira', name='ドクマイラ', types=['poison', 'dragon'], base='キマイラ', size='L')
EYE_BOX = (41, 27, 11, 7)   # 隈取りの 目（idle0）
PAL = {
    'k': '#101018', 'l': '#3c1a40',
    'F': '#ecc472', 'G': '#b8823e', 'H': '#6e442c',      # 獅子の 毛（明・中・暗）
    'M': '#c88ae6', 'N': '#8648b0', 'O': '#4a2268',      # 竜の うろこ・たてがみ（明・中・暗）
    'V': '#dcff5c', 'U': '#78c832', 'T': '#2c7438',      # 毒（明・中・暗）／翼の 膜
    'w': '#ffffff', 'r': '#b02848', 'd': '#4c0c24',      # きば・口の 中（明・暗）
}
LIGHT = set('FMVw')
KEEP_BLACK = set('wVUrd')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 胴：分厚い 胸と 肩 → くびれた 腹 → 丸い もも（あたりは 多角形、筋肉の みぞは 手で）----
def torso():
    W, H = 42, 28; g = grid(W, H)
    poly(g, [(1, 11), (5, 8), (12, 8), (19, 8), (25, 3), (31, 0), (37, 1), (41, 6), (42, 14), (41, 22), (37, 28), (29, 28),
             (25, 22), (20, 18), (14, 18), (10, 22), (4, 22), (0, 18)], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 4 or rt <= 2: c = 'H'
            elif dn == 5 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 3): c = 'F'
            out[y][x] = c
    # 背骨に そって 竜の うろこ（腰から 肩へ だんだん 大きく）
    for i, x in enumerate(range(4, 26, 3)):
        y = next(j for j in range(H) if g[j][x] != '.')
        out[y][x] = 'M'; out[y][x + 1] = 'N'; out[y + 1][x] = 'N'; out[y + 1][x + 1] = 'O'
        if i >= 3: out[y - 1 if y > 0 else y][x] = out[y][x]
    # 肩甲骨の もりあがり（弧）と ひじ
    for (x, y) in ((27, 4), (26, 5), (25, 6), (25, 7), (25, 8), (25, 9), (26, 10), (26, 11), (27, 12), (28, 13), (29, 14)):
        out[y][x] = 'l'; out[y][x + 1] = 'F' if out[y][x + 1] in 'G' else out[y][x + 1]
    for (x, y) in ((30, 15), (31, 16), (32, 17), (32, 18)): out[y][x] = 'H'
    # 胸の 筋肉（前の 丸み）
    for (x, y) in ((37, 9), (36, 10), (36, 11), (36, 12), (37, 13), (38, 14)): out[y][x] = 'l'
    for (x, y) in ((38, 7), (39, 8), (38, 8), (37, 10)): out[y][x] = 'F'
    # あばら
    for (x, y) in ((19, 11), (20, 12), (22, 11), (23, 12), (21, 14), (22, 15)): out[y][x] = 'l'
    # ももの 丸み
    for (x, y) in ((10, 10), (9, 11), (8, 12), (8, 13), (8, 14), (9, 15), (10, 16), (11, 17)):
        out[y][x] = 'l'
    for (x, y) in ((10, 11), (9, 12), (9, 13)): out[y][x] = 'F'
    # 腹の 毛ふさ（下に ぎざぎざ）
    for x in range(14, 24, 3): out[17 + (x - 14) // 4][x] = 'l' if g[17 + (x - 14) // 4][x] != '.' else '.'
    return outline(rows_of(out))


# ---- デフォルメ用の 胴（小さく 丸く：胸は 厚く、腰は 低く）----
def torso2():
    W, H = 27, 17; g = grid(W, H)
    poly(g, [(0, 8), (3, 3), (8, 1), (14, 2), (19, 0), (24, 1), (26, 5), (27, 11), (25, 17), (18, 17), (16, 14), (11, 14), (9, 17), (3, 17), (0, 13)], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 3 or rt <= 2: c = 'H'
            elif dn == 4 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 3): c = 'F'
            out[y][x] = c
    # 背骨に そって 竜の うろこ
    for i, x in enumerate(range(4, 18, 3)):
        y = next(j for j in range(H) if g[j][x] != '.')
        out[y][x] = 'M'; out[y][x + 1] = 'N'; out[y + 1][x] = 'N'; out[y + 1][x + 1] = 'O'
    # 肩の もりあがり と 胸
    for (x, y) in ((18, 3), (17, 4), (17, 5), (17, 6), (18, 7), (19, 8), (20, 9)):
        out[y][x] = 'l'; out[y][x + 1] = 'F' if out[y][x + 1] == 'G' else out[y][x + 1]
    for (x, y) in ((24, 7), (23, 8), (23, 9), (24, 10)): out[y][x] = 'l'
    # ももの 丸み
    for (x, y) in ((8, 6), (7, 7), (6, 8), (6, 9), (7, 10), (8, 11)): out[y][x] = 'l'
    for (x, y) in ((8, 7), (7, 8)): out[y][x] = 'F'
    # あばら
    for (x, y) in ((13, 7), (14, 8), (15, 7)): out[y][x] = 'l'
    return outline(rows_of(out))

# ---- 竜の 翼（骨の あたりは 線、膜の 陰影は 骨からの 距離で）----
def wing(spread=False):
    W, H = 30, 30; g = grid(W, H)
    if not spread:
        wrist, tips, scal = (20, 3), [(3, 3), (1, 12), (6, 20)], [(9, 9), (8, 16), (14, 22)]
    else:
        wrist, tips, scal = (18, 0), [(0, 0), (0, 8), (2, 17)], [(8, 6), (6, 13), (11, 20)]
    root = (25, 28)
    pts = [root, (26, 17), wrist, tips[0], scal[0], tips[1], scal[1], tips[2], scal[2], (21, 28)]
    poly(g, pts, 'T')
    out = [r[:] for r in g]
    bones = grid(W, H)
    for t in tips: line(bones, wrist[0], wrist[1], t[0], t[1], 'N')
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'T': continue
            if any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (1, 2)): out[y][x] = 'U'
            elif any(0 <= y - d < H and bones[y - d][x] == 'N' for d in (3,)) and (x + y) % 2: out[y][x] = 'U'
            if run(g, x, y, 0, 1) <= 1 and out[y][x] == 'T': out[y][x] = 'l'
    for t in tips: line(out, wrist[0], wrist[1], t[0], t[1], 'N')
    line(out, root[0], root[1], wrist[0], wrist[1], 'N'); line(out, root[0] + 1, root[1], wrist[0] + 1, wrist[1], 'O')
    line(out, root[0] - 1, root[1] - 1, wrist[0] - 1, wrist[1], 'M')
    for t in tips: out[t[1]][t[0]] = 'V'
    cx, cy = wrist   # 手首の かぎ爪
    out[cy][cx] = 'M'
    if cy >= 1: out[cy - 1][cx + 1] = 'w'
    if cy >= 2: out[cy - 2][cx + 2] = 'w'
    return outline(rows_of(out))

# ---- たてがみ：竜の うろこが とげ状に 逆立つ（とげの あたりは 三角、先は 毒）----
def mane():
    W, H = 24, 40; canvas = grid(W, H)
    spikes = [((10, 8), (16, 7), (9, 0)), ((14, 7), (20, 8), (18, 1)), ((7, 10), (11, 7), (2, 3)), ((6, 14), (7, 9), (0, 9)),
              ((6, 19), (6, 13), (0, 16)), ((6, 24), (6, 18), (1, 23)), ((8, 28), (6, 23), (2, 31)), ((13, 30), (8, 27), (9, 35)),
              ((19, 28), (12, 30), (16, 34))]
    def shade(g):
        out = [r[:] for r in g]
        for y in range(len(g)):
            for x in range(len(g[0])):
                if g[y][x] == '.': continue
                lf, rt, up = run(g, x, y, -1, 0), run(g, x, y, 1, 0), run(g, x, y, 0, -1)
                c = 'N'
                if lf <= 1 or up <= 1: c = 'M'
                if rt <= 2 and lf > 1: c = 'O'
                out[y][x] = c
        return out
    for a, b, t in spikes:
        g = grid(W - 2, H - 2); poly(g, [(a[0] - 1, a[1] - 1), (b[0] - 1, b[1] - 1), (t[0] - .5, t[1] - .5)], '#')
        g = shade(g)
        o = [list(r) for r in outline(rows_of(g))]
        # 先っぽは 毒
        ty = min(y for y in range(len(o)) for x in range(len(o[0])) if o[y][x] in 'MNO') if t[1] < a[1] else max(y for y in range(len(o)) for x in range(len(o[0])) if o[y][x] in 'MNO')
        for x in range(len(o[0])):
            if o[ty][x] in 'MNO': o[ty][x] = 'V'
        for y in range(len(o)):
            for x in range(len(o[0])):
                if o[y][x] != '.': canvas[y][x] = o[y][x]
    core = grid(W - 2, H - 2); ellipse(core, 12.5, 18, 7.5, 12.5, '#'); core = shade(core)
    for (x, y) in ((8, 11), (9, 12), (8, 16), (9, 17), (8, 22), (9, 23), (12, 13), (12, 25), (11, 19)):
        if core[y][x] in 'NM': core[y][x] = 'O'
    for (x, y) in ((8, 12), (8, 17), (8, 23)):
        if core[y][x] == 'N': core[y][x] = 'M'
    o = outline(rows_of(core))
    for y, r in enumerate(o):
        for x, c in enumerate(r):
            if c != '.': canvas[y][x] = c
    return rows_of(canvas)

# ---- 獅子の 顔（横顔）：重い まゆの ひさし・つり上がった たての ひとみ・むき出しの きば ----
HEAD = [
    '.....kkkkkkk.............',
    '...kkFFFFFFFkkk..........',
    '..kFFFFGGGGGGFFkk........',
    '.kFFGGGGGGGGGGGGFk.......',
    '.kFGGGGGGGGGGGGGGGkk.....',
    'kFGGGGGGGGGGkkkkGGGFkk...',
    'kFGGGGGGGGkkHHHHkkkGFFkk.',
    'kGGGGGGGGkHHHHHHHHHkFFFFk',
    'kGGGGGGGGGkk.....HHkFGGkk',
    'kGGGGGGGGGGk.....kHkGGGkk',
    'kGGGGGGGHGGGkkkkkkGlGGGGk',
    'kHGGGGGGGlGGGlGGlGGlGGHGk',
    'kHGGGGGGGGlGGGlGGlGGGHHk.',
    'kHGGGGGGGGGGkkkkkkkkkkkk.',
    'kHHGGGGGGGkkkrrrrrrrrrk..',
    'kHHGGGGGGkdwwddddddwwk...',
    '.kHHGGGGGkddwdddwddwk....',
    '.kHHGGGGGGkkkkkwwkkk.....',
    '..kHHGGGGGGGGGGGGHk......',
    '...kkHHHHHHHHHHHHk.......',
    '.....kkkkkkkkkkkk........',
]
HEAD_OPEN = HEAD[:13] + [
    'kHGGGGGGGGGkkkkkkkkkkkkk.',
    'kHHGGGGGGkkrrrrrrrrrrrk..',
    'kHHGGGGGkdwwddddddwwk....',
    '.kHHGGGGkddwdddddddwk....',
    '.kHHGGGkddddddddddddk....',
    '.kHHGGGkdddrrrrrrrrk.....',
    '.kHHGGGGkddddddwddwk.....',
    '..kHHGGGGkkkkkwwkkkk.....',
    '...kHHGGGGGGGGGGHk.......',
    '....kkHHHHHHHHHHk........',
    '......kkkkkkkkkk.........',
]
# 顔の まわりの えりまき（頭の 後ろ半分を おおい、ぎざぎざが 顔へ むかう）
RUFF = [
    '.....k....',
    '....kMk...',
    '...kMNMk..',
    '..kMNNNk..',
    '.kMNNNNMk.',
    'kMNNNNNNk.',
    'kMNNMkk...',
    'kMNNNMMk..',
    '.kMNNNNMk.',
    '.kMNNNNNk.',
    'kMNNNNNOk.',
    'kMNNNNNk..',
    '.kMNNNNOk.',
    '.kMNNNNNOk',
    'kMNNNNNOk.',
    'kMNNNNNk..',
    '.kMNNNNOk.',
    '.kMNNNNNOk',
    'kMNNNNNOk.',
    'kMNNNNOk..',
    '.kNNNNNOk.',
    '.kNNNNNNOk',
    'kVNNNNNOk.',
    '.kkNNNOk..',
    '...kNOk...',
    '....kk....',
]
# 目：隈取りの 目（L）。毒の 紫の 隈（N 中・O 暗・M 明）が 目じりから 後ろへ はね上がり、下まぶたの 下にも 帯と しずくが たれる。
#   目の 形は つり目：白目 w ＋ 緑の 虹彩（V 明・U 暗）＋ たての ひとみ k
EYE = ['M...........', 'NM..........', '.NM.........', '..NMkwVkVkk.', '...NkUUkUUk.', '...NMkkkkkk.', '....NMMMMMN.', '......NMN...']
EYE_ALT = {'blink': ['M...........', 'NM..........', '.NM.........', '..NMkHHHHkk.', '...Nkkkkkkk.', '...NMGGGGGk.', '....NMMMMMN.', '......NMN...'],
           'hit': ['M...........', 'NM..........', '.NM.........', '..NMkkkkkkk.', '...NkVkkUkk.', '...NMkkkkGk.', '....NMMMMMN.', '......NMN...'],
           'atk0|atk1|atk2': ['M...........', 'MM..........', '.MM.........', '..MMkwwkVkk.', '...MkVVkVUk.', '...MMkkkkkk.', '....MMMMMMM.', '......MMM...'],
           'ko': ['M...........', 'NM..........', '.NM.........', '..NMkGkGkGk.', '...NGkGkGkk.', '...NMkGkGkk.', '....NMMMMMN.', '......NMN...']}
HORN = ['kk......', 'kMkk....', '.kMNkk..', '.kMNNNkk', '..kMNNOk', '...kkkk.']
# 毒蛇の しっぽ（S字に 立ち上がり、前を にらむ）
SNAKE = [
    '..kkkkkk......',
    '.kMMMMNNkk....',
    'kMNNNNNNNNkk..',
    'kMNNkkkNNNNNkk',
    'kNNNkwVkNNNNOk',
    'kNNNNUkNNNNNOk',
    'kONNNNNNkkkkkk',
    '.kONNNkwkkwk..',
    '..kONNNkk.k...',
    '..kUNNNOk.....',
    '..kVUNNOk.....',
    '...kUNNOk.....',
    '...kVUNNOk....',
    '....kUNNOk....',
    '....kVUNNOk...',
    '.....kUNNOOk..',
    '......kUNNOOk.',
    '.......kUNNOk.',
    '........kNNOk.',
    '........kkkk..',
]
SNAKE_OPEN = [
    '..kkkkkk......',
    '.kMMMMNNkk....',
    'kMNNNNNNNNkkk.',
    'kMNNkkkNNNNNNk',
    'kNNNkwVkNkkkkk',
    'kNNNNUkNkwdddw',
    'kONNNNNkrrrrk.',
    '.kONNNkwkwkk..',
    '..kONNNkk.....',
] + SNAKE[9:]
# 足：短く 太く（付け根は 胴に 3ドット 食いこむ。上の 輪郭は 打たない）
LEG_F = [
    'kFGGGGHk.',
    'kFGGGGHHk',
    'kFGGGGHHk',
    '.kFGGGHk.',
    '.kFGGGHk.',
    'kFGGGGHHk',
    'kGGlGGlHHk',
    'kHHlHHlHHk',
    '.kwkkwkkwk',
]
LEG_H = [
    'kFGGGGHHk',
    'kFGGGGHHk',
    'kFGGGGHHk',
    '.kFGGGHk.',
    '.kFGGGHk.',
    '.kFGGGHHk',
    'kGGlGGlHk',
    'kHHlHHlHk',
    '.kwkwkkwk',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'M': 'N', 'N': 'O', 'O': 'l', 'V': 'U', 'U': 'T'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 毒の ブレス（もくもく）
BREATH1 = [
    '....kkk.......',
    '..kkVVUkk.kk..',
    '.kVVUUUTTkVUk.',
    'kVUUUTTTTkUTk.',
    'kUUTTTTTkkkk..',
    '.kTTTTkk......',
    '..kkkk........',
]
BREATH2 = [
    '........kkkk...........',
    '...kkk.kVVUUkk...kkk...',
    '..kVVUkVUUUTTTk.kVVUk..',
    '.kVUUUTUUTTTTTkkVUUTTk.',
    'kVUUUTTTTTTTTTTUUTTTTk.',
    'kUUTTTTTTkTTTTTTTTTTkVk',
    '.kTTTTTkk.kTTTTTTkkk.k.',
    '..kkkkk....kkkkkk......',
]
DRIP = ['kVk', 'kUk', '.k.']
TORSO = torso2(); MANE = mane()
HX, HY = 34, 21          # 顔の 位置（頭は 元の 大きさの まま）
def layers():
    return [
        dict(n='wingF', g='wingF', x=13, y=6, rows=dark(wing(True)), only='atk0|atk1|atk2'),
        dict(n='snake', g='tail', x=2, y=24, rows=SNAKE, alt={'atk0|atk1|atk2': SNAKE_OPEN}),
        dict(n='legFF', g='legB', x=31, y=51, rows=dark(LEG_F)),
        dict(n='legHF', g='legA', x=15, y=51, rows=dark(LEG_H)),
        dict(n='torso', g='body', x=9, y=36, rows=TORSO),
        dict(n='legH', g='legB', x=9, y=52, rows=LEG_H),
        dict(n='legF', g='legA', x=26, y=52, rows=LEG_F),
        dict(n='wing', g='wing', x=5, y=12, rows=wing(), alt={'atk0|atk1|atk2': wing(True)}),
        dict(n='mane', g='head', x=HX - 8, y=HY - 7, rows=MANE),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='ruff', g='head', x=HX - 2, y=HY - 3, rows=RUFF),
        dict(n='horn', g='head', x=HX + 5, y=HY - 4, rows=HORN),
        dict(n='eye', g='head', x=HX + 7, y=HY + 5, rows=EYE, alt=EYE_ALT),
        dict(n='drip', g='drip', x=HX + 19, y=HY + 20, rows=DRIP, only='idle1|idle2|walk1|walk3'),
        dict(n='breath1', g='fx', x=HX + 23, y=HY + 13, rows=BREATH1, only='atk1'),
        dict(n='breath2', g='fx', x=HX + 19, y=HY + 10, rows=BREATH2, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0), 'wing': (0, -1), 'drip': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'wing': (0, 0), 'tail': (0, 1), 'drip': (0, 2)},
    'idle3': {'body': (0, 0), 'head': (0, 1), 'wing': (0, -1), 'tail': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1), 'wing': (0, -1), 'drip': (0, 0)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1), 'wing': (0, -1), 'drip': (0, 0)},
    'atk0': {'body': (-1, 1), 'head': (-1, 1), 'wing': (0, -2), 'tail': (-1, -1), 'legA': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (1, 0), 'wing': (0, -2), 'tail': (1, 0)},
    'atk2': {'root': (4, 0), 'head': (1, -1), 'wing': (0, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'wing': (-1, 1), 'tail': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'wingF': 'wing', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'drip': 'head', 'fx': 'head'}
