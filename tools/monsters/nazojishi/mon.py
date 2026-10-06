# ナゾジシ（エスパー・いわ × スフィンクス）手打ち GBA風・デフォルメ（2〜3頭身：頭と 青石の たてがみは 大きい まま、
# 体は 小さく すわった 獅子＝立てた 胸・前足 2本・うしろに たたんだ 小さな もも。翼は 見せ所で 大きく 上へ）
import math
from pix import grid, rows_of, ellipse, poly, line, outline
EYE_BOX = (46, 6, 9, 13)
META = dict(id='nazojishi', name='ナゾジシ', types=['psychic', 'rock'], base='スフィンクス', size='L')
PAL = {
    'k': '#101018', 'l': '#40283c',
    'S': '#efdcaa', 'T': '#b89a6a', 'U': '#76603e',      # 砂岩（明・中・暗）
    'A': '#7ad6cc', 'B': '#2c8a96', 'C': '#1c4660',      # 頭かざりの 青石（明・中・暗）
    'P': '#ffc8ff', 'Q': '#ee4ad2', 'R': '#8a2498',      # 念力の 光（明・中・暗）
    'w': '#ffffff',
}
LIGHT = set('SAPw')
KEEP_BLACK = set('wPQ')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, Lc='S', Mc='T', Dc='U', lt=2, dk=3, rk=2):
    """光は 左上：上・左の ふち lt は 明、下 dk・右 rk は 暗"""
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = Mc
            if dn <= dk or rt <= rk: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if (up <= lt and rt <= rk) or (lf <= lt and dn <= dk): c = Mc
            out[y][x] = c
    return out
def P(g, pts, ch, only=None):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]) and (only is None or g[y][x] in only): g[y][x] = ch

# ---- 体：立てた 胸（右）＋ 小さく たたんだ もも（左下）。1枚の 形で 描き、ももの ふちだけ 線で 分ける ----
BX, BY = 14, 24          # 体の 置き場所（64x64 の 中）
def body(glow=False):
    W, H = 34, 34; g = grid(W, H)
    ellipse(g, 23.5, 12.5, 9.5, 11.5, '#')                                 # 胸（たて長の たる）
    poly(g, [(15, 8), (30, 8), (31, 21), (24, 25), (16, 30), (8, 33), (8, 26)], '#')   # 背〜腹
    ellipse(g, 11, 26, 8.5, 7.5, '#')                                # たたんだ もも（小さく）
    out = shade(g, lt=2, dk=3, rk=3)
    # ももの ふち（太ももの 丸い 線）：上半分の 弧
    for t in range(-170, -20, 6):
        a = math.radians(t); x = round(12 + 7 * math.cos(a)); y = round(27 + 6 * math.sin(a))
        if out[y][x] != '.':
            out[y][x] = 'l'
            if y + 1 < H and out[y + 1][x] in 'TU': out[y + 1][x] = 'S'
    # 胸の 毛（ひげの ような 石の みぞ）と 胸と 腹の さかい
    P(out, [(26, 14), (25, 15), (25, 16), (26, 17), (29, 15), (28, 16), (28, 17), (29, 18)], 'l', 'STU')
    P(out, [(26, 18), (29, 19)], 'S', 'TU')
    # 石の われ目
    P(out, [(15, 9), (16, 10), (5, 24)], 'l', 'STU')
    # ももの うず巻き（念力で 光る みぞ）
    c1, c2 = ('P', 'Q') if glow else ('Q', 'R')
    rune = [(10, 25), (11, 24), (12, 24), (13, 25), (14, 26), (14, 27), (13, 28), (12, 29), (10, 29), (9, 28), (9, 27), (10, 26), (11, 26), (12, 27)]
    for i, (x, y) in enumerate(rune): out[y][x] = c1 if i % 3 == 0 else c2
    # 胸の 三本 紋様（光る）
    P(out, [(21, 20), (21, 21), (21, 22), (23, 21), (23, 22), (23, 23), (23, 24), (25, 22), (25, 23), (25, 24)], c2)
    P(out, [(21, 20), (23, 21), (25, 22)], c1)
    return outline(rows_of(out))
BODY = body(); BODY_G = body(True)

# ---- 石の 翼：付け根（右下）から 左上へ ひらく。風切り羽 4枚の 先が ぎざぎざ、羽の あいだに 線 ----
def wing(up=0):
    W, H = 27, 27; g = grid(W, H)
    pts = [(25, 26), (26, 18), (22, 11), (15, 4 - up), (13, 0 - up), (10, 2 - up), (6, 1 - up), (5, 5 - up), (1, 6 - up), (2, 10), (4, 12), (1, 15), (4, 18), (9, 20), (14, 22), (18, 26)]
    poly(g, [(x, max(0, y)) for x, y in pts], '#')
    out = shade(g, lt=1, dk=2, rk=2)
    # 雨おおい（付け根の 丸い 羽の 列）
    for x, y in ((21, 14), (20, 15), (19, 16), (18, 17), (17, 18), (16, 19), (15, 20)):
        if out[y][x] != '.': out[y][x] = 'l'
        if out[y - 1][x - 1] != '.' and out[y - 1][x - 1] != 'k': out[y - 1][x - 1] = 'S'
    # 風切り羽の すじ（先へ 向かって）
    for (x0, y0, x1, y1) in ((20, 13, 11, 3), (19, 15, 6, 7), (17, 17, 4, 12), (15, 19, 5, 16)):
        line(out, x0, y0, x1, max(0, y1 - (up if y1 < 10 else 0)), 'l')
    for y in range(H):
        for x in range(1, W):
            if out[y][x] in 'TU' and out[y][x - 1] == 'l' and out[y - 1][x] != 'l': out[y][x] = 'S'
    return outline(rows_of(out))
DARK = {'S': 'T', 'T': 'U', 'U': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

# ---- 頭の 後ろの 石の 円盤（たてがみ）：青石に 念の 文字が 光る ----
def disc(glow=False):
    N = 27; c = (N - 1) / 2; g = grid(N, N)
    star = []
    for i in range(20):
        a = math.pi * 2 * i / 20 + .1; r = 13.4 if i % 2 == 0 else 10.6
        star.append((N / 2 + r * math.cos(a), N / 2 + r * math.sin(a)))
    poly(g, star, '#')
    out = shade(g, 'A', 'B', 'C', lt=2, dk=3, rk=3)
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            if 7.4 <= d < 8.4: out[y][x] = 'l'
            elif 8.4 <= d < 9.2 and out[y][x] == 'B' and x + y < 2 * c: out[y][x] = 'A'
    for (x, y) in ((4, 13), (5, 8), (8, 5), (13, 4), (6, 18), (9, 21)):
        out[y][x] = ('P' if glow else 'Q'); out[y + 1][x] = 'R'
    return outline(rows_of(out))
DISC = disc(); DISC_G = disc(True)

HEAD = [
    '....kkkkkkkkk.....',
    '..kkSSSSSSSSTkk...',
    '.kSSSTTTTTTTTTTk..',
    'kSSTTTTTTTTTTTTTk.',
    'kSTTTTTTTTTTTTTTk.',
    'kSTTTkkkkkkkkTTTTk',
    'kSTTTTkUUUUUUkkkTk',
    'kSTTTTkTTTTTTkTTTk',
    'kSTTTlTkkkkkkTTSSk',
    'kTTTTTlTTTTTTTSSSUk',
    'kTTTTTTTTTTTTTTkkkk',
    'kTTTTTTTTTkkkkkkkk.',
    'kUTTTTTTkwUUUwUwk..',
    'kUUTTTTTTkkkkkkk...',
    '.kUUTTTTTTTTTUk....',
    '..kUUUUUUUUUUk.....',
    '...kkkkkkkkkk......',
]
HEAD_ROAR = HEAD[:11] + [
    'kTTTTTTTTkkkkkkkkk',
    'kUTTTTTTkwRRRRRwk.',
    'kUUTTTTkRRRRRRRk..',
    'kUUUTTTkwRRRwkk...',
    '.kUUUTTTkkkkTk....',
    '..kUUUUUUUUUUk....',
    '...kkkkkkkkkk.....',
]
# 目（M 重い まぶた）：石の ひさしの 下、平らな 上まぶたが 虹彩の 上半分を かくす。見下す 半目（ピンクの 虹彩・横長の ひとみ）
EYE = ['UUUUUU', 'kkkkkk', 'PQkkRk', 'kkkkk.']
EYE_ALT = {'blink': ['UUUUUU', 'TTTTTT', 'kkkkkk', 'TTTTT.'],
           'hit': ['UUUUUU', 'kkTTkk', 'TTkkTT', 'kkTTk.'],
           'atk0|atk1|atk2': ['UUUUUU', 'kkkkkk', 'wPkkQk', 'kkkkk.'],
           'ko': ['UkUkUU', 'TTkTTT', 'TkTkTT', 'TTTTT.']}
# 額の 第三の 目（P 星・十字の 瞳・見せ所）：青石の 台座に はまった 丸い 目。虹彩は 桃→紫→濃紫の グラデーション、
# まん中に 白く 光る 十字の ひとみ
EYE3 = ['..kkkkk..', '.kkPPPkk.', 'kAPQkQPkC', 'kAQkwkQkC', 'kBRQkQRkC', '.kkRRRkk.', '..kkkkk..']
EYE3_ALT = {
    'blink': ['..kkkkk..', '.kkTTTkk.', 'kATTTTTkC', 'kAkkkkkkC', 'kBUUUUUkC', '.kkUUUkk.', '..kkkkk..'],
    'hit': ['..kkkkk..', '.kkTTTkk.', 'kATkTTTkC', 'kAkTkkkkC', 'kBUUUkUkC', '.kkUUUkk.', '..kkkkk..'],
    'ko': ['..kkkkk..', '.kkTTTkk.', 'kATkTkTkC', 'kATTkTTkC', 'kBTkTkTkC', '.kkUUUkk.', '..kkkkk..'],
    'atk0|atk1|atk2|idle1|idle2': ['..kkkkk..', '.kkwwwkk.', 'kAwPkPwkC', 'kAPkwkPkC', 'kBQPkPQkC', '.kkQQQkk.', '..kkkkk..'],
}
# 前足（太い 柱＋ 指 3本と 爪。上の 3行は 胸に 食いこむ）
LEG_F = [
    '.kSSTUk...',
    '.kSSTUk...',
    '.kSSTUk...',
    '.kSSTTUk..',
    '.kSSTTUk..',
    '.kSSTTUk..',
    '.kSSTTUk..',
    '.kSSTTUk..',
    'kSSTTTTUkk',
    'kSTlTTlTUk',
    'kUUlUUlUUk',
    '.kwkkwkkwk',
]
# うしろ足の 足先（ももの 下から 前へ）
PAW_H = ['..kTTTTTUk..', '.kSTTTTTTUk.', 'kSTTTlTlTTUk', 'kUUUUlUlUUUk', '.kwkwkwkkkk.']
# しっぽ：ももの うしろから 上へ 巻き、先は 念の 光の ふさ
TAIL = [
    '...kkk.....',
    '..kQPQk....',
    '.kPwPQRk...',
    '.kQPQRk....',
    '..kRRkSk...',
    '....kSTUk..',
    '....kSTUk..',
    '....kSTTUk.',
    '.....kSTTUk',
    '......kSTUk',
    '......kSTUk',
    '.....kSTTUk',
    '.....kTTUk.',
    '.....kSTTUk',
    '......kSTUk',
]
# 念力の 光線（第三の 目から）と 先の 輪
def beam(n, ring=False):
    core = ['k' * n, 'R' * n, 'Q' * n, 'P' * n, 'w' * n, 'P' * n, 'Q' * n, 'R' * n, 'k' * n]
    for j in (0, 8):
        core[j] = ''.join('k' if (i % 4) else '.' for i in range(n))
    if ring:
        R = ['...kkk..', '..kQRQk.', '.kQkkkQk', 'kQk...kQk', 'kQk...kQk', 'kQk...kQk', '.kQkkkQk', '..kQRQk.', '...kkk..']
        core = [c + r for c, r in zip(core, R)]
    return core
HX, HY = 41, 9
def layers():
    return [
        dict(n='wingF', g='wing', x=16, y=1, rows=dark(wing()), alt={'atk0|atk1|atk2': dark(wing(2))}),
        dict(n='legFF', g='legB', x=44, y=47, rows=dark(LEG_F)),
        dict(n='tail', g='tail', x=8, y=35, rows=TAIL),
        dict(n='body', g='body', x=BX, y=BY, rows=BODY, alt={'idle1|idle2|atk0|atk1|atk2': BODY_G}),
        dict(n='pawH', g='legA', x=17, y=55, rows=PAW_H),
        dict(n='wing', g='wing', x=11, y=6, rows=wing(), alt={'atk0|atk1|atk2': wing(2)}),
        dict(n='legF', g='legA', x=37, y=48, rows=LEG_F),
        dict(n='disc', g='head', x=HX - 13, y=HY - 5, rows=DISC, alt={'idle1|idle2|atk0|atk1|atk2': DISC_G}),
        dict(n='head', g='head', x=HX, y=HY, rows=HEAD, alt={'atk1|atk2': HEAD_ROAR}),
        dict(n='eye', g='head', x=HX + 7, y=HY + 6, rows=EYE, alt=EYE_ALT),
        dict(n='eye3', g='head', x=HX + 5, y=HY - 3, rows=EYE3, alt=EYE3_ALT),
        dict(n='beam1', g='fx', x=HX + 14, y=HY - 3, rows=beam(8), only='atk1'),
        dict(n='beam2', g='fx', x=HX + 14, y=HY - 3, rows=beam(10, True), only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {'body': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, -1), 'wing': (0, -2), 'tail': (0, -1)},
    'atk1': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -2)},
    'atk2': {'root': (2, 0), 'head': (1, 0), 'wing': (0, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, 2), 'wing': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'wing': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'head'}
