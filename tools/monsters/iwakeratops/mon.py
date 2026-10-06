# イワケラトプス（いわ・ドラゴン × トリケラトプス）手打ち GBA風
import math
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='iwakeratops', name='イワケラトプス', types=['rock', 'dragon'], base='トリケラトプス', size='L')
PAL = {
    'k': '#101018', 'l': '#381c1c',
    'R': '#d6905c', 'G': '#9c5838', 'H': '#5c3226',      # 岩の 皮（明・中・暗）
    'B': '#f6ecd0', 'C': '#c8ae84', 'D': '#84694a',      # 化石の 骨（明・中・暗）
    'E': '#74d0a8', 'F': '#2e7a6a',                      # 竜の うろこ板
    'Y': '#ffc838', 'O': '#e86a1c',                      # こはく色の 目・化石の 光
    'w': '#ffffff',
}
LIGHT = set('RBEYw')
KEEP_BLACK = set('wYO')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def shade(g, Lc, Mc, Dc, lt=2, dk=4):
    H, W = len(g), len(g[0]); out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = Mc
            if dn <= dk or rt <= 2: c = Dc
            if dn == dk + 1 and (x + y) % 2: c = Dc
            if up <= lt or lf <= lt: c = Lc
            if up <= 1 and rt <= 2: c = Mc
            out[y][x] = c
    return out

# ---- 胴と 尾：あたり → 陰影 → 岩の 板の われ目を 手で ----
def body():
    W, H = 50, 26; g = grid(W, H)
    ellipse(g, 30, 13, 19, 12.5, '#')
    poly(g, [(14, 6), (0, 18), (2, 20), (16, 22)], '#')
    out = shade(g, 'R', 'G', 'H', lt=2, dk=5)
    # 岩の 板（六角っぽい われ目）
    cracks = [((22, 3), (22, 4), (21, 5), (21, 6), (22, 7), (23, 8)), ((23, 8), (24, 9), (25, 10), (26, 10), (27, 10)),
              ((32, 2), (32, 3), (31, 4), (31, 5), (31, 6), (32, 7)), ((32, 7), (33, 8), (34, 9), (35, 9)),
              ((40, 4), (40, 5), (39, 6), (39, 7), (40, 8)), ((27, 10), (28, 11), (28, 12), (28, 13)),
              ((14, 10), (15, 11), (16, 12), (17, 12)), ((35, 9), (36, 10), (36, 11), (37, 12), (37, 13))]
    for c in cracks:
        for (x, y) in c:
            out[y][x] = 'l'
            if out[y][x + 1] == 'G': out[y][x + 1] = 'R'
    for (x, y) in ((8, 15), (19, 9), (26, 5), (35, 5), (44, 9), (30, 16), (20, 16)):
        if out[y][x] in 'GH': out[y][x] = 'R'; out[y + 1][x] = 'H'
    return outline(rows_of(out))

# ---- 化石の えり（半円＋ふちの とげ）：骨の 色、こはくの アンモナイト紋 ----
def frill(glow=False):
    N = 36; g = grid(N, N); c = 17.5
    pts = []
    for i in range(30):
        a = math.radians(i * 12 + 6); r = 1.0 if i % 2 == 0 else .8
        pts.append((c + 14.5 * r * math.cos(a), c - 17.5 * r * math.sin(a)))
    poly(g, pts, '#')
    out = shade(g, 'B', 'C', 'D', lt=2, dk=3)
    # 内側の みぞ（骨の 縁どり）
    for y in range(N):
        for x in range(N):
            d = ((x - c) ** 2 + (y - c) ** 2) ** .5
            e = (((x + .5 - c) / 14.5) ** 2 + ((y + .5 - c) / 17.5) ** 2) ** .5
            if out[y][x] != '.' and .62 <= e < .69: out[y][x] = 'l'
            elif out[y][x] == 'C' and .69 <= e < .75 and x + y < 2 * c: out[y][x] = 'B'
            elif out[y][x] == 'C' and e < .62 and (x + y) % 2 and e > .5: out[y][x] = 'D' if x + y > 2 * c else 'C'
    # 放射の 骨の すじ（扇の 骨）：中心から 外へ
    for deg in (60, 90, 120, 150, 180, 210, 240):
        a = math.radians(deg)
        for t in range(5, 11):
            x = round(c + t * math.cos(a) * .85); y = round(c - t * math.sin(a))
            if 0 <= x < N and 0 <= y < N and out[y][x] in 'BCD':
                out[y][x] = 'D'
                if out[y - 1][x] == 'C' and deg <= 180: out[y - 1][x] = 'B'
    # アンモナイトの 化石紋（手で）
    a1, a2 = ('Y', 'O') if glow else ('B', 'D')
    for (ox, oy) in ((9, 12), (11, 21), (17, 6)):
        for (dx, dy, ch) in ((0, 0, a2), (1, -1, a2), (2, -1, a2), (3, 0, a2), (3, 1, a2), (2, 2, a2), (1, 2, a2), (0, 1, a1), (1, 0, a1), (2, 0, a1), (2, 1, a1), (1, 1, a2)):
            out[oy + dy][ox + dx] = ch
    return outline(rows_of(out))

HEAD = [
    '....kkkkkkk...........',
    '..kkRRRRRRRkk.........',
    '.kRRRGGGGGGGRkk.......',
    'kRRGGGGGGGGGGGGkk.....',
    'kRGGGGkkkkkGGGGGGkk...',
    'kRGGGGGHHHHkkkGGGGGkk.',
    'kRGGGGGGGGGGGGGGGGGGGk',
    'kGGGGGGGGGGGGGGGGGGGCCk',
    'kGGGGGGGGGGGGGGGGGGCBBCk',
    'kHGGGGlGGGGGGGGGGkkCBCk',
    'kHGGGGGlGGGkkkkkkkkkCCk',
    'kHHGGGGGGGkHHHHHHHkCDk.',
    '.kHHGGGGGGGGGGGGGGkDk..',
    '..kHHHHGGGGGGGGHHHkk...',
    '...kkHHHHHHHHHHHk......',
    '.....kkkkkkkkkkk.......',
]
HEAD_ROAR = HEAD[:9] + [
    'kHGGGGlGGGGGGGGGGkkCBCk',
    'kHGGGGGlGGkkkkkkkkkkCCk',
    'kHHGGGGGkOOOOOOOOkkDk..',
    '.kHHGGGGkOOOOOOOkk.....',
    '..kHHHGGGkwOOOwk.......',
    '...kkHHHHGGGGGHHk......',
    '....kHHHHHHHHHHk.......',
    '.....kkkkkkkkkk........',
]
EYE = ['kYYOk', '.kYk']
EYE_ALT = {'blink': ['kkkkk', '.GGG'], 'hit': ['kGkGk', '.kGk'], 'atk0|atk1|atk2': ['kwYYk', '.kYk'], 'ko': ['kGkGk', '.GkG']}
# 額の 長い 角（2本：手前／おく）と 鼻の 角
HORN = [
    '...........kk',
    '.........kkBk',
    '.......kkBBCk',
    '.....kkBBCCk.',
    '...kkBBCCDk..',
    '..kBBCCDDk...',
    '.kBCCDDk.....',
    'kBCDDk.......',
    'kCDkk........',
    '.kk..........',
]
NHORN = ['..kk', '.kBk', 'kBCk', 'kCDk']
PLATE = ['..kk..', '.kEEk.', 'kEEFFk', 'kEFFFk']
LEG = [
    '.kkkkkkk.', 'kRGGGGGHk', 'kRGGGGGHk', '.kRGGGGHk', '.kRGGGHHk', '.kGGGGHHk', '.kGGlGHHk',
    'kRGGGGHHHk', 'kGGGGGHHHk', 'kHHHHHHHHk', 'kBkBkBkkk.',
]
DARK = {'R': 'G', 'G': 'H', 'H': 'l', 'B': 'C', 'C': 'D'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 踏みつけの 衝撃：地面の 波と 飛ぶ 岩
SHOCK1 = [
    '........kk.........kk...',
    '.......kRGk.......kRGk..',
    '...kk...kk.........kk...',
    '..kRk...................',
    '...k......kk......kk....',
    '.kkk.....kCBk....kBCk...',
    'kCBCk..kkCBBCk..kCBBCkk.',
    'kBBCCkkCCBBCCCkkCCBCCDk.',
    '.kkkkkkkkkkkkkkkkkkkkkk.',
]
SHOCK2 = [
    '.......kk...........kk...',
    '..kk..kRGk....kk...kRGk..',
    '.kRGk..kHk...kRGk...kk...',
    '..kk..........kk.........',
    '.........kk.........kk...',
    '...kk...kCBk..kk...kBCk..',
    '..kBCk.kCBBCkkBCk.kCBBCk.',
    '.kCBBCkCBBBCCkBBCkCBBBCCk',
    'kCBBCCCBBCCCDCCCCCBBCCDDk',
    '.kkkkkkkkkkkkkkkkkkkkkkk.',
]
BODY = body(); FRILL = frill(); FRILL_G = frill(True)

def layers():
    return [
        dict(n='legFF', g='fl2', x=45, y=50, rows=dark(LEG)),
        dict(n='legHF', g='hl2', x=18, y=50, rows=dark(LEG)),
        *[dict(n='pl%d' % i, g='body', x=x, y=y, rows=PLATE) for i, (x, y) in enumerate(((11, 32), (17, 28), (23, 26), (29, 25)))],
        dict(n='body', g='body', x=1, y=28, rows=BODY),
        dict(n='legH', g='hl', x=12, y=51, rows=LEG),
        dict(n='frill', g='head', x=24, y=7, rows=FRILL, alt={'idle1|idle2|atk0|atk1|atk2': FRILL_G}),
        dict(n='hornF', g='head', x=50, y=21, rows=dark(HORN)),
        dict(n='head', g='head', x=40, y=29, rows=HEAD, alt={'atk1|atk2': HEAD_ROAR}),
        dict(n='horn', g='head', x=46, y=23, rows=HORN),
        dict(n='nhorn', g='head', x=57, y=31, rows=NHORN),
        dict(n='eye', g='head', x=47, y=34, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='fl', x=39, y=51, rows=LEG),
        dict(n='shock1', g='fx', x=44, y=52, rows=SHOCK1, only='atk1'),
        dict(n='shock2', g='fx', x=44, y=51, rows=SHOCK2, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, -2), 'head': (-1, -4), 'fl': (-1, -6), 'fl2': (-1, -6), 'hl': (-1, 0), 'hl2': (-1, 0)},
    'atk1': {'root': (3, 0), 'body': (0, 1), 'head': (1, 2)},
    'atk2': {'root': (3, 0), 'body': (0, 1), 'head': (1, 2)},
    'hit': {'root': (-3, 0), 'head': (-3, -2), 'body': (0, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'body': 'root', 'fl': 'legA', 'hl2': 'legA', 'fl2': 'legB', 'hl': 'legB', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
