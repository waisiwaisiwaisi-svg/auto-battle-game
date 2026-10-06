# ホムラジシ（ほのお・かくとう × ライオン）手打ち GBA風
import pix
META = dict(id='homurajishi', name='ホムラジシ', types=['fire', 'fighting'], base='ライオン', size='L')
PAL = {
    'k': '#101018', 'l': '#4a1c1c',
    'F': '#f4c878', 'G': '#cc8a3c', 'H': '#7e4424',
    'Y': '#fff27a', 'O': '#ff9a24', 'R': '#d8381c', 'D': '#7c1a1e',
    'S': '#e4eaf4', 'T': '#9098b4', 'U': '#4c5070',
    'w': '#ffffff',
}
LIGHT = set('FYSw')

# ---- 下書き用：マスクに 光（左上）の 3段階を つける（仕上げは 下で 手打ち）----
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
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'U': 'l', 'w': 'T'}
def dark(rows): return pix.recolor(rows, DARK)

# ---- 胴（デフォルメ：小さく 丸く、胸が 少し 深い）----
BODY_M = [
    '.......############.....',
    '....##################..',
    '..#####################.',
    '.#######################',
    '########################',
    '########################',
    '########################',
    '########################',
    '########################',
    '.#######################',
    '..#####################.',
    '...###################..',
    '.....###############....',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'FGH'}, low=10), [
    # 肋と ももの 筋（手打ち）
    '', '',
    '...F',
    '..FG.......HG',
    '.FG.......HG',
    '.G.......H.GG',
    '........H',
    '.......H...HHH',
]))

# ---- 後ろ足（短く 太い もも＋大きな 足）：付け根は 胴に 3ドット もぐる ----
HLEG_M = [
    '..#######...',
    '.#########..',
    '###########.',
    '###########.',
    '.##########.',
    '..########..',
    '...######...',
    '...#####....',
    '...#####....',
    '...#######..',
    '..#########.',
    '..##########',
]
HLEG = pix.outline(put(shade(HLEG_M, {'#': 'FGH'}), [
    '', '', '.........H', '........H', '.......H', '', '', '', '', '', '',
    '....k.k.k.w',
]))

# ---- 前足：鉄の こて（短く 太く、こぶしに びょう）----
FLEG = [
    '.kkkkkkkkk....',
    'kFFGGGGGGHk...',
    'kFGGGGGGHHk...',
    'kkkkkkkkkkkk..',
    'kSSSSTTTTUUk..',
    'kSUSTTUTTUUSk.',
    'kSTTTTTTTUSSTk',
    'kSUSTTUTTUUkk.',
    'kkkkkkkkkkkk..',
    '.kFGGGGGGHk...',
    '.kFGGGGGHHk...',
    '.kFGGGGGHHk...',
    'kFFGGGGGGGHk..',
    'kGHGGHGGHGHk..',
    '.kwkkwkkwkk...',
]
# 付け根は 胴に うめる：上の 輪郭を 消して 胴の 色と なじませる
HLEG[0] = '.' * len(HLEG[0]); FLEG[0] = '.' * len(FLEG[0])
FLEG_FAR = dark(FLEG)

# ---- 頭（手打ち）：重い まゆ、長い 鼻すじ、きばの 見える 口 ----
HEAD = [
    '.....kkkkkkkkk.........',
    '...kkFFFFFFFFFkkk......',
    '..kFFFFGGGGGGGGGGkk....',
    '.kFGGFFFFFFFGGGGGGGkk..',
    '.kFkkkkkkkkkkGGGGGGGGk.',
    '.kGGGGGGGGGGkkkFFFFFFkk',
    'kGGGGGGGGGGGGGkGGGGGkHk',
    'kGGGGGGGGGGGGGkGGGGGGkk',
    'kGHGHGGGGGGGGkHGHGHGGHk',
    'kHGHGGHGGGGGGGGGGGkkkkk',
    'kHGGHGGGGGGGGkkwkkwkkwk',
    'kHGHGGGGGGGGkDDDDDDDDk.',
    '.kHGGGGGGGGkDDDDDDDk...',
    '.kHHGGGGGGGGkkwkkwkk...',
    '..kHHGGGGGGGGGGGHHk....',
    '...kkHHHHHHHHHHHk......',
    '.....kkkkkkkkkkk.......',
]
HEAD_ATK = HEAD[:9] + [
    'kHGHGGHGGGGGGGGkkkkkkkk',
    'kHGGHGGGGGGGkkwkwkwkwkw',
    'kHGHGGGGGGGkDDDDDDDDDk.',
    '.kHGGGGGGGkDDDOODDDk...',
    '.kHGGGGGGGkDDDDDDDDDk..',
    '.kHHGGGGGGGkkwkwkwkwk..',
    '..kHHGGGGGGGGGGGGGHk...',
    '...kkHHHHHHHHHHHHkk....',
    '.....kkkkkkkkkkkk......',
]
# 頭の 上に かぶさる 前の 炎（たてがみの 前がみ）
TUFT = [
    '.kk.......kk..',
    'kRk......kRk..',
    'kOk..kk.kROk..',
    'kYOkkRk.kOYk..',
    '.kYOkOkkOYOk..',
    '.kYYOYOkYYOk..',
    '..kYYYOYYOk...',
    '...kkYYYOk....',
    '.....kkkk.....',
]
TUFT2 = [
    'kk.........k..',
    'kRk.....k.kRk.',
    '.kOk..kRk.kOk.',
    '.kYOkkOk.kROk.',
    '.kYOkOOkkOYk..',
    '.kYYOYOkYYOk..',
    '..kYYYOYYOk...',
    '...kkYYYOk....',
    '.....kkkk.....',
]
# するどい 目：まゆの ひさしの 下、白い 光＋金と だいだいの 虹彩＋たての ひとみ、下まぶた
EYE = ['kwYYkOk', 'kYOOkOk', '.kkkkkk']
EYE_ALT = {'blink': ['kGGGGGk', 'kkkkkkk', '.HHHHH.'], 'hit': ['kkGGGkk', 'GGkkkGG', '.k...k.'],
           'atk0|atk1|atk2': ['kwwYkYk', 'kYYOkOk', '.kkkkkk'], 'ko': ['kGkGkGG', 'GGkGGGG', 'GkGkGGG']}

# ---- 燃える たてがみ：舌の 形の 炎を 奥から 重ねる（外側＝赤、内＝黄）----
TONGUES = [(26, 12, 26, 1, 8), (21, 11, 13, 1, 9), (16, 14, 4, 5, 9), (13, 19, 1, 14, 9), (12, 24, 1, 24, 9),
           (14, 28, 3, 32, 8), (17, 30, 9, 36, 7), (22, 31, 17, 38, 6), (27, 30, 27, 37, 6)]
def mane(ph=0):
    W, H = 34, 40; out = pix.grid(W, H)
    core = pix.grid(W, H); pix.ellipse(core, 25, 20, 9, 11, '#')
    def ring(m, y, x):
        r = 9
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                yy, xx = y + dy, x + dx
                if not (0 <= yy < H and 0 <= xx < W) or m[yy][xx] == '.': r = min(r, max(abs(dx), abs(dy)))
        return r
    for y in range(H):
        for x in range(W):
            if core[y][x] == '#':
                out[y][x] = 'D' if ring(core, y, x) <= 2 or (x - y // 2) % 3 else 'R'
    for i, (bx, by, tx, ty, w) in enumerate(TONGUES):
        s = (1 if (i + ph) % 2 else -1) if ph else 0
        tx += s; dx, dy = tx - bx, ty - by; n = (dx * dx + dy * dy) ** .5; px, py = -dy / n, dx / n
        mx, my = bx + dx * .55 - 1.5, by + dy * .55
        m = pix.grid(W, H)
        pix.poly(m, [(bx - px * w / 2, by - py * w / 2), (mx - px * w / 3, my - py * w / 3), (tx, ty),
                     (mx + px * w / 3, my + py * w / 3), (bx + px * w / 2, by + py * w / 2)], '#')
        for y in range(H):
            for x in range(W):
                if m[y][x] != '#': continue
                r = ring(m, y, x)
                out[y][x] = ('D' if (y > 30 or x > 26) else 'R') if r == 1 else 'O' if r == 2 else 'Y'
    return pix.outline(pix.rows_of(out))
MANE = mane(); MANE2 = mane(1)

TAIL = [
    '.kkk.........',
    'kYOkk........',
    'kOYORk.......',
    '.kOYOk.......',
    '..kRRk.......',
    '...kGk.......',
    '...kGHk......',
    '....kGHk.....',
    '....kGGHk....',
    '.....kGGHkk..',
    '......kGGGHkk',
    '.......kkGGGH',
    '.........kkkk',
]
TAIL_KO = [
    '.............',
    '.........kkkk',
    '......kkkGGGH',
    '...kkkGGGHHkk',
    'kkkRGGHHkkk..',
    'kYOOkkkk.....',
    '.kkkk........',
]
TAIL2 = [
    '..kk.........',
    '.kYOk........',
    'kOYYRk.......',
    'kROYOk.......',
    '.kkRRk.......',
] + TAIL[5:]

# ---- こぶしの 一撃（攻撃）：前へ のびた こて ＋ 炎の はじけ ----
PUNCH = [
    '..............kkkkkk....',
    '.kkkkkkkkkkkkkSSSSSSkk..',
    'kGGGGkSSSSSkkSSTTTTTTUk.',
    'kGGGHkSTTTTkSSTkkTkkTUk.',
    'kGGHHkSTTTTkSTTSSTSSTUUk',
    'kHHHHkTTTTUkTTTTTTTTTUUk',
    'kHHHHkUUUUUkTTkkTkkTTUUk',
    '.kkkkkkkkkkkkUUUUUUUUUk.',
    '.............kkkkkkkkk..',
]
BURST = [
    '.......kk.......',
    '..kk..kRk...kk..',
    '..kRk.kOk..kRk..',
    '...kOkkYkkkOk...',
    'kk..kOYYYYOk..kk',
    'kROOOYYwwYYOOORk',
    'kk..kOYYYYOk..kk',
    '...kOkkYkkkOk...',
    '..kRk.kOk..kRk..',
    '..kk..kRk...kk..',
    '.......kk.......',
]
BURST2 = [
    '..k....k....k...',
    '.kRk..kRk..kRk..',
    '..k..kOYOk..k...',
    '....kOYYYOk.....',
    'kk.kOYwwwYOk.kk.',
    'kROOYYwwwYYOORk.',
    'kk.kOYwwwYOk.kk.',
    '....kOYYYOk.....',
    '..k..kOYOk..k...',
    '.kRk..kRk..kRk..',
    '..k....k....k...',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=7, y=30, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2, 'ko': TAIL_KO}),
        dict(n='hlegF', g='legB', x=25, y=47, rows=dark(HLEG), not_='ko'),
        dict(n='flegF', g='legB', x=46, y=46, rows=FLEG_FAR, not_='ko'),
        dict(n='body', g='body', x=17, y=37, rows=BODY),
        dict(n='hleg', g='legA', x=15, y=47, rows=HLEG, not_='ko'),
        dict(n='mane', g='mane', x=21, y=4, rows=MANE, alt={'idle1|idle3|walk1|walk3|atk2': MANE2}),
        dict(n='fleg', g='legA', x=39, y=46, rows=FLEG, not_=NB + '|ko'),
        dict(n='head', g='head', x=39, y=17, rows=HEAD, alt={'atk1|atk2': HEAD_ATK}),
        dict(n='tuft', g='head', x=36, y=10, rows=TUFT, alt={'idle1|idle3|walk1|walk3|atk2': TUFT2}),
        dict(n='eye', g='head', x=42, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='punch', g='punch', x=36, y=40, rows=PUNCH, only=NB + '|ko'),
        dict(n='burst', g='punch', x=59, y=38, rows=BURST, alt={'atk2': BURST2}, only=NB),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, -1)},
    'idle2': {'body': (0, 1), 'mane': (0, -1)},
    'idle3': {'body': (0, 0), 'mane': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'mane': (-1, 1), 'legA': (-1, 0), 'tail': (1, 0)},
    'atk1': {'root': (3, 0), 'body': (0, 1), 'punch': (1, 0)},
    'atk2': {'root': (5, 0), 'body': (0, 1), 'punch': (2, 0)},
    'hit': {'root': (-3, 0), 'mane': (-1, 1), 'head': (-1, 0)},
    'ko': {'body': (-2, 9), 'mane': (2, 6), 'head': (3, 3), 'tail': (2, 4), 'punch': (6, 12)},
}
PARENT = {'head': 'mane', 'mane': 'body', 'tail': 'body', 'body': 'root', 'punch': 'root', 'legA': 'root', 'legB': 'root'}
