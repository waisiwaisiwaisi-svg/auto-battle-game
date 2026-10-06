# ヒョウリュウ（ドラゴン・こおり × 竜）手打ち GBA風・デフォルメ（頭を 大きく、胴を 短く、足を 短く。結晶の 柱は 大きい まま）
from pix import grid, rows_of, ellipse, poly, line, outline, recolor
META = dict(id='hyoryu', name='ヒョウリュウ', types=['dragon', 'ice'], base='竜', size='L')
EYE_BOX = (40, 36, 7, 4)   # 目（idle0 の 64x64 座標）
PAL = {
    'k': '#101018', 'l': '#221c50',
    'D': '#96a6e8', 'E': '#5a5eb0', 'F': '#2e2c6c',      # うろこ（明・中・暗）
    'B': '#eaeeff', 'C': '#a6b0de',                      # 腹（霜）
    'I': '#f2ffff', 'J': '#8ae8f6', 'K': '#3a9ccc',      # 氷の 結晶（明・中・暗）
    'm': '#4a1a52', 'w': '#ffffff',
    'x': '#07060e',                                      # 目の 黒い 強膜
}
LIGHT = set('DBIw')
KEEP_BLACK = set('wIJx')

def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n

# ---- 胴と 尾（低い かまえ）：あたり → 陰影 → 腹の 霜・うろこを 手の ルールで ----
def body():
    W, H = 38, 17; g = grid(W, H)
    ellipse(g, 22, 8, 13, 7.5, '#')
    poly(g, [(11, 4), (2, 10), (1, 13), (4, 13), (13, 12)], '#')
    poly(g, [(31, 3), (37, 5), (37, 11), (31, 13)], '#')     # 首の つけね
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'E'
            if dn <= 3: c = 'F'
            if up <= 2 or lf <= 1: c = 'D'
            if dn <= 3 and x > 15: c = 'B' if dn >= 2 else 'C'
            out[y][x] = c
    # うろこ（ずらした 小さな 弧）
    for y in range(4, 11, 3):
        for x in range(6 + (y % 2) * 2, 34, 4):
            if out[y][x] == 'E' and out[y][x + 1] == 'E': out[y][x] = 'F'; out[y][x + 1] = 'F'; out[y - 1][x] = 'D' if out[y - 1][x] == 'E' else out[y - 1][x]
    # 腹板の 段
    for x in range(18, 34, 3):
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
COLS = [(14, 36, 8, 4), (19, 28, 14, 5), (25, 19, 22, 6), (31, 25, 17, 5), (36, 34, 10, 4)]

# 頭（デフォルメで 大きく）：後ろへ のびた 氷の 角、前へ さがる 重い まゆ、ぎざぎざの きば
HEAD = [
    '...kk...................',
    '..kIJk..................',
    '..kIJKk.................',
    '...kIJKkkkkk............',
    '...kDDDDDDDDkk..........',
    '..kDDEEEEEEEEEkk........',
    '.kDEEEEEEEEEEEEEkk......',
    'kDEEEEkkkkkkkEEEEEkk....',
    'kDEEEk.......kkEEEEEkk..',
    'kEEEEEk......kEEEEEEEEk.',
    'kEEEEEEkkkkkkEEEEEEEEEDk',
    'kEEEEEEEEEEEEEEEEEEEEkkk',
    'kFEEEEEEEEEkkkkkkkkkkk..',
    'kFFEEEEEEkwCCwCCwCwk....',
    '.kFFEEEEEEkkkkkkkkkk....',
    '..kFFFFFFFFFFFFFFk......',
    '...kkkkkkkkkkkkkk.......',
]
HEAD_OPEN = HEAD[:11] + [
    'kEEEEEEEEEEkwkkwkkwkkkkk',
    'kFEEEEEEEEkmmmmmmmmk....',
    'kFFEEEEEEkmmmmmmmk......',
    'kFFFEEEEEkwmmmwmk.......',
    '.kFFFFFFFFkkkkkk........',
    '..kkkkkkkkk.............',
]
# 目（F：黒い 強膜）：白目の かわりに 真っ黒。その 中に 氷の 青の 細い たて瞳（芯は 白っぽい 青）が 光る。下ぶちは 暗い 紫
EYE = ['xxxxIxx', 'mxxxJxk']
EYE_ALT = {'blink': ['kkkkkkk', 'kEEEEEk'], 'hit': ['kkxxxkk', 'kxJxxxk'],
           'atk0|atk1|atk2': ['xxKIwKx', 'mxKJIKk'],
           'ko': ['kxKxKxk', 'kxxKxxk', 'kxKxKxk']}
LEG_F = ['.kkkkkk..', 'kDEEEEFk.', 'kDEEEEFk.', '.kDEEEFFk', 'kDEEEEFFk', 'kFFFFFFFk', 'kIkIkIkk.']
LEG_H = ['.kkkkkkk.', 'kDEEEEEFk', 'kDEEEEFFk', '.kEEEEFFk', '.kDEEEFFk', 'kFFFFFFFk', 'kIkIkIkk.']
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
        dict(n='legFF', g='legB', x=37, y=53, rows=dark(LEG_F)),
        dict(n='legHF', g='legA', x=17, y=53, rows=dark(LEG_H)),
        *[dict(n='col%d' % i, g='body', x=x - h // 3, y=y, rows=crystal(h, w), alt={'atk0|atk1|idle2': crystal(h, w, 1, True)}) for i, (x, y, h, w) in enumerate(COLS)],
        dict(n='body', g='body', x=2, y=38, rows=BODY),
        dict(n='tailtip', g='body', x=0, y=47, rows=TAILTIP),
        dict(n='legH', g='legB', x=9, y=55, rows=LEG_H[1:]),  # 付け根の 線を ぬいて 胴に 食いこませる
        dict(n='head', g='head', x=34, y=29, rows=HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        dict(n='eye', g='head', x=40, y=37, rows=EYE, alt=EYE_ALT),
        dict(n='legF', g='legA', x=30, y=55, rows=LEG_F[1:]),
        dict(n='snow', g='fx0', x=12, y=15, rows=SNOW, only='idle1|idle2'),
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
