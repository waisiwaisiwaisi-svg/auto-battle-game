# ヒョウリュウ（ドラゴン・こおり × 竜）手打ち GBA風
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='hyoryu', name='ヒョウリュウ', types=['dragon', 'ice'], base='竜', size='L')
PAL = {
    'k': '#101018', 'l': '#221c50',
    'D': '#96a6e8', 'E': '#5a5eb0', 'F': '#2e2c6c',      # うろこ（明・中・暗）
    'B': '#eaeeff', 'C': '#a6b0de',                      # 腹（霜）
    'I': '#f2ffff', 'J': '#8ae8f6', 'K': '#3a9ccc',      # 氷の 結晶（明・中・暗）
    'r': '#ff3a5a', 'm': '#4a1a52', 'w': '#ffffff',
}
LIGHT = set('DBIw')
KEEP_BLACK = set('wrIJ')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 胴と 尾（低い かまえ）：あたり → 陰影 → 腹の 霜・うろこを 手の ルールで ----
def body():
    W, H = 52, 22; g = grid(W, H)
    ellipse(g, 32, 9, 17.5, 8.5, '#')
    poly(g, [(16, 4), (3, 12), (2, 15), (5, 15), (18, 14)], '#')
    poly(g, [(44, 3), (51, 6), (51, 12), (44, 15)], '#')     # 首の つけね
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'E'
            if dn <= 3: c = 'F'
            if up <= 2 or lf <= 1: c = 'D'
            if dn <= 3 and x > 22: c = 'B' if dn >= 2 else 'C'
            out[y][x] = c
    # うろこ（ずらした 小さな 弧）
    for y in range(5, 12, 3):
        for x in range(8 + (y % 2) * 2, 46, 4):
            if out[y][x] == 'E' and out[y][x + 1] == 'E': out[y][x] = 'F'; out[y][x + 1] = 'F'; out[y - 1][x] = 'D' if out[y - 1][x] == 'E' else out[y - 1][x]
    # 腹板の 段
    for x in range(25, 48, 3):
        for y in range(H):
            if out[y][x] == 'B': out[y][x] = 'C'
    return outline(rows_of(out))

# ---- 氷の 結晶の 柱：後ろへ かたむいた 六角柱。左面＝明、中＝中、右面＝暗、上は とがる ----
def crystal(h, w=5, lean=1, glint=False):
    W = w + h * lean // 3 + 1; rows = []
    for i in range(h):                      # i = 0 が 下
        t = max(0, i - (h - 3)); ww = max(1, w - 2 * t)
        sh = (i * lean) // 3; x0 = W - w - sh + (w - ww) // 2
        a = max(1, ww // 3); c = max(1, ww // 3) if ww > 2 else 0
        seg = 'I' * a + 'J' * (ww - a - c) + 'K' * c
        if i % 5 == 2 and ww >= 4: seg = seg[:a] + 'K' + seg[a + 1:]     # 結晶の 段
        rows.append('.' * x0 + seg)
    rows = rows[::-1]
    if glint:
        r = list(rows[3]); j = len(r) - len(r.lstrip('.')) if False else next(k for k, ch in enumerate(r) if ch != '.'); r[j] = 'w'; rows[3] = ''.join(r)
        r = list(rows[4]); j = next(k for k, ch in enumerate(r) if ch != '.'); r[j] = 'w'; rows[4] = ''.join(r)
    return outline(rows)
COLS = [(13, 33, 8, 4), (18, 25, 15, 5), (25, 14, 25, 6), (32, 19, 20, 5), (38, 27, 12, 4), (43, 33, 6, 3)]

HEAD = [
    '...kk.................',
    '..kIJk................',
    '..kIJKk...............',
    '...kIJKkkkkk..........',
    '...kDDDDDDDDkk........',
    '..kDDEEEEEEEEEkk......',
    '.kDEEEEEEEEEEEEEkk....',
    'kDEEEEkkkkkkEEEEEEkk..',
    'kDEEEEEFFFFFkkkEEEEEk.',
    'kEEEEEEEEEEEEEEEEEEEDk',
    'kEEEEEEEEEEEEEEEEEEkkk',
    'kFEEEEEEEkkkkkkkkkkk..',
    'kFFEEEEkwCCwCCwCwk....',
    '.kFFEEEEEkkkkkkkkk....',
    '..kFFFFFFFFFFFFk......',
    '...kkkkkkkkkkkk.......',
]
HEAD_OPEN = HEAD[:10] + [
    'kEEEEEEEEEkwkkwkkwkkkk',
    'kFEEEEEEEkmmmmmmmmk...',
    'kFFEEEEEkmmmmmmmk.....',
    'kFFFEEEEkwmmmwmk......',
    '.kFFFFFFFkkkkkk.......',
    '..kkkkkkkk............',
]
EYE = ['krrrk', '.krk']
EYE_ALT = {'blink': ['kkkkk', '.EEE'], 'hit': ['kEkEk', '.kEk'], 'atk0|atk1|atk2': ['kwwrk', '.krk'], 'ko': ['kEkEk', '.EkE']}
LEG_F = ['.kkkkkk..', 'kDEEEEFk.', 'kDEEEEFk.', '.kDEEFFk.', '..kEEFFk.', '.kDEEEFFk', 'kDEEEEFFk', 'kFFFFFFFk', 'kIkIkIkk.']
LEG_H = ['.kkkkkkk.', 'kDEEEEEFk', 'kDEEEEFFk', '.kEEEEFFk', '..kkEEFk.', '..kDEEFk.', '.kDEEEFFk', 'kFFFFFFFk', 'kIkIkIkk.']
TAILTIP = ['.kk...', 'kIJk..', 'kIJKkk', '.kIJJK', '..kkkk']
DARK = {'D': 'E', 'E': 'F', 'F': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 結晶の ブレス（氷の かけらが 円すい状に 広がる）
BREATH1 = [
    '......kk..w...',
    '..kk.kIJk.....',
    'kkIJkkJKk..kk.',
    'IIJJJKkk..kIJk',
    'wIIJJKkk...kk.',
    'kkJKkkIJk.....',
    '..kk..kk...w..',
]
BREATH2 = [
    '.........kk....w....',
    '....w...kIJk....kk..',
    '..kk...kIJKk...kIJk.',
    '.kIJk.kkJKk..kk.kk..',
    'kkIJJkIJkk..kIJk..w.',
    'IIJJJKJJKkkkkJKk....',
    'wwIIJJJKKIIJJkk..kk.',
    'IIJJKkJKk.kJKk..kIJk',
    'kkJKkkkk...kk....kk.',
    '.kkk..kIJk.....w....',
    '.......kk...........',
]
BREATH1 = [r[:13] for r in BREATH2]
SNOW = ['.w.', 'wIw', '.w.']
BODY = body()

def layers():
    return [
        dict(n='legFF', g='legB', x=46, y=51, rows=dark(LEG_F)),
        dict(n='legHF', g='legA', x=20, y=51, rows=dark(LEG_H)),
        *[dict(n='col%d' % i, g='body', x=x - h // 3, y=y, rows=crystal(h, w), alt={'atk0|atk1|idle2': crystal(h, w, 1, True)}) for i, (x, y, h, w) in enumerate(COLS)],
        dict(n='body', g='body', x=0, y=37, rows=BODY),
        dict(n='tailtip', g='body', x=0, y=49, rows=TAILTIP),
        dict(n='legH', g='legB', x=14, y=52, rows=LEG_H),
        dict(n='head', g='head', x=42, y=31, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=49, y=39, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='legA', x=40, y=52, rows=LEG_F),
        dict(n='snow', g='fx0', x=16, y=11, rows=SNOW, only='idle1|idle2'),
        dict(n='br1', g='fx', x=56, y=36, rows=BREATH1, only='atk1'),
        dict(n='br2', g='fx', x=56, y=36, rows=BREATH2, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'head': (0, 0), 'fx0': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'fx0': (1, 2)},
    'idle3': {'body': (0, 0), 'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, 1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 2), 'head': (-1, 2), 'fx0': (0, -2)},
    'atk1': {'root': (2, 0), 'head': (1, -1)},
    'atk2': {'root': (2, 0), 'head': (1, -1)},
    'hit': {'root': (-3, 0), 'head': (-3, -3), 'body': (0, 0)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'head', 'fx0': 'root'}
