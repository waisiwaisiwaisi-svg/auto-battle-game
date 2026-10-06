# ツノヒメ（フェアリー・エスパー × ユニコーン）手打ち GBA風
META = dict(id='tsunohime', name='ツノヒメ', types=['fairy', 'psychic'], base='ユニコーン', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1e48',
    'F': '#7272c4', 'G': '#43428a', 'H': '#24224e',
    'C': '#fff0fa', 'P': '#ff7ad2', 'Q': '#a8389c',
    'S': '#ffe98e', 'T': '#d9a23c', 'U': '#8a5622',
    'E': '#6ef4ff', 'w': '#ffffff',
}
LIGHT = set('FCSEw')

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, lit=1, dk=2):
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
            c = 'G'
            if dd <= dk: c = 'H'
            elif du <= lit or dl <= 1: c = 'F'
            elif dr <= 1: c = 'H'
            g[y][x] = c
    return g

# ---- 胴と 首：深い 胸・アーチを えがく 首（あたりは 多角形、筋肉は 手で）----
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, poly, outline, rows_of
BX, BY = 8, 6
def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
def body():
    W, H = 44, 42; g = grid(W, H)
    pts = [(9, 31), (12, 27), (18, 26), (25, 28), (32, 26), (36, 21), (39, 15), (42, 10), (46, 7), (50, 9), (50, 17), (48, 23),
           (47, 29), (46, 35), (43, 43), (37, 46), (27, 44), (19, 44), (13, 43), (9, 38)]
    poly(g, [(x - BX, y - BY) for x, y in pts], '#')
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 3 or rt <= 1: c = 'H'
            elif dn == 4 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 3): c = 'F'
            out[y][x] = c
    def P(pts, ch, hi=None):
        for (x, y) in pts:
            x -= BX; y -= BY
            if 0 <= y < H and 0 <= x < W and out[y][x] != '.':
                out[y][x] = ch
                if hi and out[y][x + 1] == 'G': out[y][x + 1] = hi
    # 肩の 筋肉（弧）と ひじ
    P([(36, 28), (35, 29), (34, 30), (34, 31), (34, 32), (34, 33), (35, 34), (36, 35), (37, 36), (38, 37), (39, 38)], 'H', 'F')
    # 首の すじ（アーチに そって）
    P([(42, 14), (41, 16), (40, 18), (39, 20), (39, 22)], 'H', 'F')
    P([(45, 12), (44, 15), (43, 18)], 'F')
    # 胸の もりあがり
    P([(44, 30), (44, 31), (45, 32)], 'F')
    # 腰の 筋肉（もも）
    P([(17, 28), (16, 29), (15, 30), (15, 31), (15, 32), (15, 33), (16, 34), (17, 35), (18, 36), (19, 37)], 'H', 'F')
    P([(11, 29), (12, 28), (13, 28)], 'F')
    # あばら（うすく）
    P([(25, 36), (26, 37), (28, 36), (29, 37), (31, 36), (32, 37)], 'H')
    return outline(rows_of(out))

# 頭：下向きに ひいた 戦馬の 頭。金の 面よろい、耳は 後ろへ ねる
HEAD = [
    '..kk............',
    '.kFGk...........',
    '.kFGHk..........',
    'kFGGHkkkk.......',
    'kFGGGkSSSkk.....',
    'kGGGkkkSTTTUk...',
    'kGGk......TTUk..',
    'kGGGkkkkkkSTTUk.',
    'kGGGGGGGGkkSTTUk',
    'kHGGGGGGGGGkSTUk',
    '.kHGGGGGGGGGkTUk',
    '..kHGGGGGGGGGkUk',
    '...kHGGGGGGGGGkk',
    '....kHGGGGGGGkkk',
    '.....kHHGGGkkwk.',
    '......kHHHHHkkk.',
    '.......kkkkkk...',
]
EYE = ['wEEkE']
EYE_ALT = {'blink': ['kkkkk'], 'atk0|atk1|atk2': ['wwEkw'], 'hit': ['kEkkk'], 'ko': ['kGkGk']}
# 結晶の やり（ツノ）：前へ つき出す。らせんの きざみ つき
HORN = [
    '.............kk',
    '...........kkCk',
    '.........kkCCPk',
    '.......kkCPQPk.',
    '.....kkCPQPkk..',
    '...kkCPQPkk....',
    '.kkCPQQkk......',
    'kCPQkk.........',
    'kkk............',
]
HORN_HOT = [r.replace('P', 'C').replace('Q', 'P') for r in HORN]
# 流れる 結晶の たてがみ：首の いただき（クレスト）に そって 結晶の 房を 下から 順に 重ねる。房は 後ろ上へ なびく
CREST = [(33, 25), (35, 22), (37, 19), (38, 16), (40, 13), (42, 10), (44, 8)]
MX, MY = 22, 0
def mane(shine=0):
    W, H = 28, 30; canvas = grid(W, H)
    for i, (ax, ay) in enumerate(CREST):
        ax -= MX; ay -= MY
        L = 7 + (i % 2) * 2 + (2 if 2 <= i <= 4 else 0)
        tip = (ax - L, ay - L // 2 + 1 - (i % 2))
        g = grid(W, H)
        poly(g, [(ax + 1, ay - 1.5), (ax + 2, ay + 2), (ax - 1, ay + 2.5), tip], '#')
        out = [r[:] for r in g]
        for y in range(H):
            for x in range(W):
                if g[y][x] == '.': continue
                up, dn = run(g, x, y, 0, -1), run(g, x, y, 0, 1)
                out[y][x] = 'C' if up <= 1 else 'Q' if dn <= 1 else 'P'
        if 0 <= tip[1] < H and 0 <= tip[0] < W: out[tip[1]][tip[0]] = 'C'
        if shine and i % 3 == shine % 3:
            for y in range(H):
                for x in range(W):
                    if out[y][x] == 'P': out[y][x] = 'C'; break
        o = outline(rows_of(out))
        for y, r in enumerate(o[1:H + 1]):
            for x, c in enumerate(r[1:W + 1]):
                if c != '.': canvas[y][x] = c
    return outline(rows_of(canvas))
MANE = mane(); MANE2 = mane(1)
TAIL = [
    '.......kkk..',
    '.....kkCCPk.',
    '....kCCPPQk.',
    '...kCPPQQk..',
    '..kCPPQk....',
    '.kCPPQk.kk..',
    'kCPPQk.kCPk.',
    'kCPQk.kCPQk.',
    'kPQk.kCPQk..',
    'kPQk.kPQk...',
    '.kQk.kPQk...',
    '.kQk.kQk....',
    '..kk.kk.....',
]
PLATE = [
    '..kkkkk.....',
    '.kSSSSTkk...',
    'kSSTTTTUCk..',
    'kSTTTTUkCPk.',
    'kSTwETUkPQQk',
    'kSTEETUkCPk.',
    'kSTTTUUkPk..',
    '.kTTTUUkk...',
    '.kTTUUk.....',
    '..kUUk......',
    '...kk.......',
]
# 前足（ふんばる）：ひじ → ひざ（こぶ）→ 金の わ → 結晶の ひづめ
FLEG = [
    '.kkkkkk..',
    'kFGGGGHk.',
    'kFGGGGHk.',
    '.kFGGGHk.',
    '.kFGGGHk.',
    '..kFGGHk.',
    '..kFGHk..',
    '..kFGHHk.',
    '..kGGGHk.',
    '..kFGHk..',
    '..kFGHk..',
    '..kFGHk..',
    '..kSTUk..',
    '..kGGHk..',
    '..kGGHHk.',
    '.kCPPQk..',
    'kCPPPQQk.',
    'kkkkkkkk.',
]
# 上げた 前足（ひざを 曲げて 前へ）
FLEG_UP = [
    '.kkkkk.....',
    'kFGGGHkk...',
    'kFGGGGHHk..',
    '.kFGGGGHHk.',
    '..kkFGGGHHk',
    '....kkGGGHk',
    '......kGGHk',
    '.....kGGHk.',
    '....kGGHk..',
    '...kSTUk...',
    '..kCPQk....',
    '.kCPQk.....',
    '.kkkk......',
]
# 後ろ足：もも → すね（後ろへ）→ 飛節（かかと）→ まっすぐな 管
HLEG = [
    '..kkkkkkk..',
    '.kFFGGGGHk.',
    'kFFGGGGGGHk',
    'kFGGGGGGGHk',
    'kFGGGGGGHHk',
    '.kFGGGGGHk.',
    '..kGGGGHk..',
    '.kGGGGHk...',
    '.kGGGHk....',
    'kFGGHk.....',
    'kGGGHk.....',
    '.kFGHk.....',
    '.kFGHk.....',
    '.kFGHk.....',
    '.kSTUk.....',
    '.kGGHk.....',
    '.kGGHHk....',
    'kCPPQk.....',
    'kCPPQQk....',
    'kkkkkkk....',
]
MOTE = ['.k.', 'kCk', 'kPk', '.k.']
BURST = [
    '......C......',
    '......C......',
    '..P...C...P..',
    '...P..P..P...',
    '....P.C.P....',
    '.....CwC.....',
    'CCPPCwwwCPPCC',
    '.....CwC.....',
    '....P.C.P....',
    '...P..P..P...',
    '..P...C...P..',
    '......C......',
    '......C......',
]
BURST2 = [
    '...P.....P...',
    '.............',
    'P....PCP....P',
    '....P...P....',
    '...P.....P...',
    '..C...w...C..',
    '..P..www..P..',
    '..C...w...C..',
    '...P.....P...',
    '....P...P....',
    'P....PCP....P',
    '.............',
    '...P.....P...',
]
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T', 'T': 'U', 'C': 'P', 'P': 'Q'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=26, rows=TAIL),
        dict(n='legHF', g='legB', x=17, y=40, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=40, y=40, rows=dark(FLEG_UP), alt={'walk0|walk1': dark(FLEG)}),
                dict(n='body', g='body', x=BX - 1, y=BY - 1, rows=BODY),
        dict(n='mane', g='neck', x=MX - 1, y=MY - 1, rows=MANE, alt={'idle1|idle3': MANE2}),
        dict(n='plate', g='body', x=40, y=29, rows=PLATE),
        dict(n='legH', g='legA', x=9, y=41, rows=HLEG),
        dict(n='legF', g='legB', x=35, y=43, rows=FLEG, alt={'atk0': FLEG_UP}),
        dict(n='head', g='head', x=43, y=4, rows=HEAD),
        dict(n='eye', g='head', x=47, y=10, rows=EYE, alt=EYE_ALT),
        dict(n='horn', g='head', x=49, y=-1, rows=HORN, alt={'atk0|atk1|atk2': HORN_HOT}),
        dict(n='m1', g='m1', x=22, y=4, rows=MOTE),
        dict(n='m2', g='m2', x=2, y=14, rows=MOTE),
        dict(n='m3', g='m3', x=58, y=30, rows=MOTE, not_='atk1|atk2'),
        dict(n='burst', g='head', x=57, y=-8, rows=BURST, alt={'atk2': BURST2}, only='atk1|atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'head': (0, 1), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'idle2': {'body': (0, 1), 'm1': (0, -2), 'm2': (0, 2), 'm3': (0, -2)},
    'idle3': {'body': (0, 1), 'head': (0, 0), 'm1': (0, -1), 'm2': (0, 1), 'm3': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'm1': (0, -1)},
    'walk1': {'body': (0, -1), 'm2': (0, 1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'm1': (0, -1)},
    'walk3': {'body': (0, -1), 'm2': (0, 1)},
    'atk0': {'body': (-2, 0), 'head': (-1, 2), 'legB': (2, -2), 'm1': (8, 2), 'm2': (14, -2)},
    'atk1': {'root': (6, 0), 'head': (2, 3), 'legB': (3, 0), 'm1': (14, 4), 'm2': (30, 0)},
    'atk2': {'root': (8, 0), 'head': (2, 2), 'm1': (6, 0), 'm2': (10, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'm1': (-2, 2), 'm2': (1, 2)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'neck', 'neck': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'm1': 'root', 'm2': 'root', 'm3': 'root'}
