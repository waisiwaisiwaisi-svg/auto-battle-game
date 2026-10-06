# ハガマ（くさ・むし × カマキリ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 三角の 頭、胴は 小さく 丸く、足は 短く 太く）
META = dict(id='hagama', name='ハガマ', types=['grass', 'bug'], base='カマキリ', size='M')
PAL = {
    'k': '#101018', 'l': '#2e2014',
    'A': '#d2a874', 'B': '#8c6038', 'C': '#4e3220',      # 樹皮の よろい
    'G': '#c4ee6a', 'H': '#5cb444', 'J': '#246a3a',      # 葉の 鎌
    'O': '#ff9a3c', 'R': '#c0302c', 'Y': '#fff07a',      # 複眼（明・暗の 虹彩＋赤い ふち）
    'w': '#ffffff',
}
LIGHT = set('AGYw')
KEEP_BLACK = set('wOYR')     # 目の まわりの 黒は 黒の まま
from pix import grid, rows_of, outline, flip_v

DK = {'A': 'B', 'B': 'C', 'G': 'H', 'H': 'J'}
def dk(rows): return [''.join(DK.get(c, c) for c in r) for r in rows]
def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def shade(g, ramp, lw=1, dw=2):
    """塗った 形に 左上の 光（上・左の ふち lw は 明、下・右の ふち dw は 暗）"""
    L, M, D = ramp; H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def f(y, x): return 0 <= y < H and 0 <= x < W and src[y][x] == M
    for y in range(H):
        for x in range(W):
            if src[y][x] != M: continue
            dr = min(next((i for i in range(1, 9) if not f(y + i, x)), 9), next((i for i in range(1, 9) if not f(y, x + i)), 9))
            ul = min(next((i for i in range(1, 9) if not f(y - i, x)), 9), next((i for i in range(1, 9) if not f(y, x - i)), 9))
            if dr <= dw: g[y][x] = D
            elif ul <= lw: g[y][x] = L
    return g
def spans(sp, ch='B'):
    W = max(b for a, b in sp) + 1; g = grid(W, len(sp))
    for y, (a, b) in enumerate(sp):
        for x in range(a, b + 1): g[y][x] = ch
    return g

# ---- 三角の 頭：後ろは 丸く、目は 前の 上、口先は 右下へ とがる ----
def head(eye='open'):
    g = spans([(7, 15), (4, 18), (2, 20), (1, 22), (0, 23), (0, 24), (0, 24), (0, 24), (0, 24), (1, 24),
               (2, 23), (3, 23), (5, 22), (7, 22), (9, 21), (11, 21), (13, 20), (14, 19), (15, 18)])
    shade(g, 'ABC', 2, 3)
    put(g, [(9, 2), (10, 2), (11, 2), (9, 3), (3, 6), (3, 7), (2, 8)], 'A')      # 頭の てっぺんの つや
    # 後ろ頭の 板の さかい目（弧）と ほおの 影
    put(g, [(7, 3), (6, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 9), (7, 10)], 'C')
    put(g, [(8, 3), (7, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 9), (8, 10)], 'A')
    put(g, [(10, 12), (11, 13), (12, 14), (13, 15), (12, 12), (13, 13), (14, 14)], 'C')
    # 大きな 複眼：まゆの ひさし（前へ 下がる）＋ 2段の 虹彩（黄・だいだい）＋ たての ひとみ ＋ 赤い ふち
    E = {'open':  ['kk........', '.kkkk.....', '..kkkkkkk.', '.kwYYYkYYk', 'kRYYYYkYOk', 'kROOOOkOOk', '.kRROOkOk.', '..kkkkkk..'],
         'blink': ['kk........', '.kkkk.....', '..kkkkkkk.', '.kBBBBBBBk', 'kkkkkkkkkk', '.kBBBBBBk.', '..kkkkkk..', '..........'],
         'hit':   ['kk........', '.kkkk.....', '..kkkkkkk.', '.kOkkkOkkk', 'kkkOkOkOkk', '.kOkkkOkk.', '..kkkkkk..', '..........'],
         'glow':  ['kk........', '.kkkk.....', '..kkkkkkk.', '.kwwYYkYYk', 'kOYwYYkYYk', 'kOYYYYkYOk', '.kOOYYkOk.', '..kkkkkk..'],
         'ko':    ['..........', '.kkkkkkk..', '.kOOOOOk..', '.kkOOOkk..', '.kOkOkOk..', '.kOOkOOk..', '.kOkOkOk..', '..kkkkk...']}[eye]
    for j, r in enumerate(E):
        for i, c in enumerate(r):
            if c != '.': g[2 + j][13 + i] = c
    put(g, [(14, 16), (15, 16), (16, 15), (17, 15), (18, 14)], 'k')       # 口の 線
    return outline(rows_of(g))
def neck():
    """前胸（首）：胸から 頭の 下へ ななめに のびる 樹皮の 柱"""
    n = 11; g = grid(12, n)
    for j in range(n):
        x0 = 5 - j * 5 // (n - 1)
        for i in range(6): g[j][x0 + i] = 'A' if i == 0 else 'C' if i >= 4 else 'B'
        if j % 4 == 2: g[j][x0 + 4] = 'C'; g[j][x0 + 1] = 'A'      # 節の すじ
    return outline(rows_of(g))
MAND = ['ACk.ACk', 'Bwk.Bwk', '.w...w.']
MAND_OPEN = ['ACk..ACk', 'Bwk..Bwk', 'w......w', '.......w']
# 触角（頭の 中から 生える）と 葉の とさか
ANT = ['.........kk', '......kkk..', '....kk.....', '..kk.......', 'kkk........', 'kB.........']
CREST = ['G.......', 'GG......', '.GHG....', '.JHHHG..', '..JHHHHG', '...JJHHH', '.....JJ.']

# ---- 小さく 丸い 胸（樹皮の よろい）----
def body():
    g = spans([(5, 12), (3, 15), (2, 16), (1, 17), (0, 17), (0, 17), (0, 17), (0, 17), (1, 16), (2, 15), (4, 13)])
    shade(g, 'ABC', 1, 2)
    for (x0, y0) in ((6, 1), (11, 2)):                              # 板の さかい目
        for d in range(7):
            x, y = x0 - (1 if d in (0, 6) else 0), y0 + d
            if g[y][x] == 'B': g[y][x] = 'C'
            if g[y][x + 1] == 'B': g[y][x + 1] = 'A'
    return outline(rows_of(g))
THORN = ['k....', 'Akk..', 'kABk.', '.kABk']

# ---- 葉の 腹（尾の ように 後ろへ）----
ABD = [
    "...........GGGGG",
    "........GGGHHHHH",
    ".....GGGHHHHHHHH",
    "...GGHHHHGHHHHHH",
    ".GGHHHGGGGGGGHHH",
    "GHHHHHHJHJHHHHHJ",
    ".JHHHHJHHHJHHHJJ",
    "..JJHJHHHHHJHJJJ",
    "....JJJHHHHJJJ..",
    ".......JJJJJ....",
]

# ---- 葉の 鎌（見せ所：大きく。内がわ＝左下に 白い のこぎり歯）----
BLADE = [
    "AAGGGGG....",
    "BBHHHHHGG..",
    "CCJHHHHHHG.",
    "..JJGHHHHHJ",
    ".wGJHGHHHHJ",
    "..GJHGHHHHJ",
    "...JHHGHHHJ",
    ".wGJHHGHHHJ",
    "..GJHHGHHJ.",
    "...JHHGHHJ.",
    ".wGJHHGHJ..",
    "..GJHGHHJ..",
    "...JHGHJ...",
    "..wGHGHJ...",
    "...GJGJ....",
    "....GJ.....",
    "..wGJ......",
]
BLADE_UP = [x.replace('A', '@').replace('C', 'A').replace('@', 'C') for x in flip_v(BLADE)]
BLADE_SWING = [
    "AAAGGGGGGGGGGG.....",
    "BBBHHHHHHHHHHHGGG..",
    "CCCJGGGGGGGGGGGHHG.",
    "...JHHHHHHHHHHHHHHG",
    "...JJJJJHHHHHHHHHJG",
    "...GG.GG.JJJJHHHJJ.",
    "....w..w..GG.GJJJG.",
    "...........w...GJ..",
    "................w..",
]
# 腕（胸から 鎌の 根もとまで。関節の 丸で つなぐ）
ARM = ['....AAA', '...ABBB', '..ABBBC', '.ABBBC.', 'ABBBC..', 'BBBC...', 'CCC....']
ARM_SW = ['.AAAA.', 'ABBBBA', 'BBBBBB', 'CBBBBB', '.CCCCC']

# ---- 短く 太い 足（ひざを 曲げて ふんばる）----
LEG = ['..AAA..', '.ABBBA.', 'ABBBBBC', 'ABBBBBC', '.CBBBBC', '..ABBC.', '..ABBC.', '.ABBBC.', 'ABBBBBw', 'CCCCCC.']

# ---- 斬撃と 舞う 葉 ----
SLASH = [
    "....kkkkk.......", "..kkGGGGGkk.....", ".kGGkkkkkGGk....", "kGk......kHGk...", "kk........kHGk..", "...........kHGk.",
    "............kHHk", "............kHHk", "...........kHHJk", "..........kHJJk.", "........kkJJk...", "......kkkkk.....",
]
LEAF1 = ['.kk.', 'kGHk', 'kHJk', '.kk.']
LEAF2 = ['..kk', '.kGk', 'kHJk', 'kk..']

SW = 'atk1|atk2'
def layers():
    H = head()
    return [
        dict(n='legB', g='legB', x=19, y=49, rows=outline(dk(LEG)), not_='ko'),
        dict(n='abd', g='tail', x=1, y=34, rows=outline(ABD), not_='ko'),
        dict(n='neck', g='body', x=31, y=30, rows=neck(), not_='ko'),
        dict(n='armBu', g='armB', x=36, y=35, rows=outline(dk(ARM)), not_=SW + '|ko'),
        dict(n='armB', g='armB', x=42, y=34, rows=outline(dk(BLADE)), not_=SW + '|ko'),
        dict(n='armBsu', g='armB', x=35, y=38, rows=outline(dk(ARM_SW)), only=SW),
        dict(n='armBs', g='armB', x=39, y=36, rows=outline(dk(BLADE_SWING)), only=SW),
        dict(n='body', g='body', x=15, y=39, rows=body(), not_='ko'),
        dict(n='thorn1', g='body', x=18, y=36, rows=THORN, not_='ko'),
        dict(n='thorn2', g='body', x=23, y=35, rows=THORN, not_='ko'),
        dict(n='legA', g='legA', x=27, y=49, rows=outline(LEG), not_='ko'),
        dict(n='crest', g='head', x=22, y=9, rows=outline(CREST), not_='ko'),
        dict(n='ant', g='head', x=40, y=9, rows=ANT, not_='ko'),
        dict(n='head', g='head', x=27, y=13, rows=H, alt={'blink': head('blink'), 'hit': head('hit'), 'atk0|atk1|atk2': head('glow')}, not_='ko'),
        dict(n='mand', g='head', x=40, y=31, rows=outline(MAND), alt={'atk0|atk1|atk2': outline(MAND_OPEN)}, not_='ko'),
        dict(n='armFu', g='armF', x=32, y=38, rows=outline(ARM), not_=SW + '|ko'),
        dict(n='armF', g='armF', x=38, y=37, rows=outline(BLADE), not_=SW + '|ko'),
        dict(n='armFsu', g='armF', x=31, y=41, rows=outline(ARM_SW), only=SW),
        dict(n='armFs', g='armF', x=35, y=40, rows=outline(BLADE_SWING), only=SW),
        dict(n='slash', g='root', x=56, y=30, rows=SLASH, only='atk1'),
        dict(n='leaf1', g='root', x=60, y=50, rows=LEAF1, only=SW),
        dict(n='leaf2', g='root', x=60, y=34, rows=LEAF2, only='atk2'),
        dict(n='ko', g='root', x=0, y=0, rows=knocked(), only='ko'),
    ]

# ---- ダウン：あおむけに たおれ、足と 鎌が 上を むく ----
def knocked():
    g = grid(64, 64)
    def st(rows, x0, y0):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.' and 0 <= y0 + j < 64 and 0 <= x0 + i < 64: g[y0 + j][x0 + i] = c
    st(outline(flip_v(dk(LEG))), 15, 38)                 # 足は 上を むいて 力なく
    st(outline(flip_v(ABD)), 0, 49)                      # 葉の 腹は 地面に ぺたり
    st(outline(flip_v(LEG)), 23, 39)
    st(flip_v(body()), 13, 48)                           # 胸は あおむけ
    st(outline(dk(BLADE_SWING)), 30, 51)                 # 鎌は 前に 投げだす
    st(outline(flip_v(['..AAAA..', '.ABBBBC.', 'ABBBBBBC', 'ABBBBBBC', '.CCCCCC.'])), 29, 50)   # 首の 根もと
    st(head('ko'), 33, 40)                               # 頭は 横だおし、目は ×
    st(outline(MAND_OPEN), 46, 56)
    return [''.join(r) for r in g]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'tail': (0, -1)}, 'idle2': {'body': (0, 1), 'tail': (-1, -1), 'armF': (0, -1)},
    'idle3': {'armF': (0, -1), 'armB': (0, 1), 'tail': (-1, 0)}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 0), 'armF': (-2, -2), 'armB': (-1, -2), 'tail': (1, 0)},
    'atk1': {'root': (5, 0), 'body': (1, 0)},
    'atk2': {'root': (6, 0), 'body': (1, 1), 'armF': (0, 2), 'armB': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, 1), 'armF': (-1, 1), 'armB': (-1, 1)},
    'ko': {},
}
PARENT = {'tail': 'body', 'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
