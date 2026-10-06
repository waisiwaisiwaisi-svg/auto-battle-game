# エンジャク（ほのお・ひこう(風) × 炎の 猛禽）手打ち GBA風
import pix
META = dict(id='enjaku', name='エンジャク', types=['fire', 'wind'], base='不死鳥', size='L')
PAL = {
    'k': '#101018', 'l': '#3c1620',
    'A': '#86728a', 'B': '#4c3e56', 'C': '#2a2234',
    'Y': '#fff2a0', 'O': '#ffb030', 'R': '#f05020', 'r': '#a01e24',
    'W': '#f2e2c4', 'V': '#b49a7c',
    'w': '#ffffff',
}
LIGHT = set('AYOWw')

HEAD = [
    'kkkk..................',
    'kWWWkkk...............',
    '.kVWWWWkkk............',
    '..kkVVWWWWkk..........',
    '....kkBAAAAAkk........',
    '....kBBAAAAAAAkk......',
    '...kBBAAkkkkkAABk.....',
    '...kBAkkYYYOkkAABk....',
    '..kBBBAkkkkkRkkkkkk...',
    '..kBBBBAAAkWWWWWWWWkk.',
    '.kBBBBBAAkWWWWWWWWWWWk',
    '.kCBBBBBkWWVVVVWWWWVWk',
    '.kCCBBBBkWkkkkkkVVVkVk',
    '..kCCBBBkVkWkWkWkkkkk.',
    '...kkCCBBkkkkkkkk.....',
    '.....kkkkk............',
]
BODY = [
    '......................kkkk......',
    '...................kkkBAAAk.....',
    '.................kkBBAAAAABk....',
    '...............kkBBBAAAAAABk....',
    '.............kkBBBBBAAAAABBk....',
    '...........kkBBBBBBBBAAAABBBk...',
    '.........kkBBBBBRBBBBBBAABBBk...',
    '........kBBBBBBBORBBBBBBBBBBCk..',
    '.......kBBBBBBBBBORBBBBBBBBBCk..',
    '......kBBBBBBBBBBBOBBBBBBBBCCk..',
    '.....kBBBBBBBBBBBBBBBBBRBBBCCk..',
    '....kBBBBBBBBBBBBBBBBBROBBCCCk..',
    '...kBBBBBBBBBBBBBBBBBBBOBCCCk...',
    '..kCBBBBBBBBBBBBBBBBBBBBCCCk....',
    '.kCCBBBBBBBBBBBBBBBBBBCCCCk.....',
    'kCCCBBBBBBBBBBBBBBBBCCCCkk......',
    'kCCCCBBBBBBBBBBBBCCCCCkk........',
    '.kkCCCCCCBBBBCCCCCCkk...........',
    '...kkkCCCCCCCCCCkkk.............',
    '......kkkkkkkkkk................',
]
TAIL0 = [
    '.....................kk.',
    '..................kkkRRk',
    '................kkROOOk.',
    '..............kkROYYOk..',
    '............kkROYYwOk...',
    '..........kkROYYYOkk....',
    '........kkROOYYOkk......',
    '.......kROOOOkkk........',
    '......kROOkk............',
    '.....kROk...............',
    '....kROk................',
    '....kROk................',
    '....kROOk...............',
    '.....kROOk..............',
    '......kROOkk............',
    '.......kRROOkk..........',
    '..k.....kkRROk..........',
    '.kRk......kROk..........',
    '..kRk....kROk...........',
    '...kRkkkROOk............',
    '....kRROOkk.............',
    '.....kkkk...............',
]
WING_UP = [
    '.......kk...kk..............',
    '......kYk..kYk..kk..........',
    '.....kYOk.kYOk.kYk...kk.....',
    '....kOOk.kOOk.kYOk..kYk.....',
    '...kROk.kROk.kOOk.kYOk......',
    '..kRRk.kRAk.kROk.kOOk.......',
    '.kRkAk.kAAkkRAk.kROk........',
    '.kkAAk.kABkkAAkkRAk.........',
    '..kABk.kABkkABkkAAkkkk......',
    '..kABBkkABBkABkkABkkAAk.....',
    '..kABBkkABBkABBkABBkRAAk....',
    '...kABBkkABBkABkkABkAAAk....',
    '...kABBBkABBkABBkABkAARBk...',
    '....kABBkkABBkABkABkAABOk...',
    '...kRkBBBkABBkABkABkAARBk...',
    '..kROkkBBkkABBkABkBkAABBk...',
    '..kOOOkkBBkABBkBBkBkAABBBk..',
    '..kYOOk.kBBkBBkBBkBkAABRBk..',
    '...kYOOkkkBkBBkBBkBkABBBOk..',
    '....kYOOOkkkBBkBBkkAABBRBk..',
    '.....kROOOOkkkkkkkkAABBBBk..',
    '......kRROOOOkCCCCkAABBBBBk.',
    '.......kkRROOkCCCkAABBBBBBk.',
    '.........kkRRkCCkAABBRBBBBk.',
    '...........kkkCkAABBBBORBCk.',
    '.............kkAABBBBBBBCCk.',
    '..............kABBBBBBBCCk..',
    '...............kkBBBBBCCk...',
    '.................kkkkkkk....',
]
NECK = [  # 首（頭と 胴を つなぐ。頭が 上下しても すき間が できない よう 長め）
    '....kkkkkk',
    '...kBAAABk',
    '..kBAAABBk',
    '..kAAABBBk',
    '.kBAABBBBk',
    '.kAABBBBCk',
    'kBAABBBBCk',
    'kAABBBBCk.',
    'kAABBBCCk.',
    'kABBBBCCk.',
    'kBBBBCCk..',
    'kBBBCCCk..',
    '.kkkkkk...',
]
TALON = [
    '..kBBk...',
    '..kBCCk..',
    '.kBCCCk..',
    'kWkkWkWk.',
    'kWVkWkWVk',
    '.kVkkVkkVk',
    '..k...k..k',
]

TAIL1 = pix.recolor([r[1:] + '.' for r in TAIL0], {})
def swept(rows):
    """あたり：上げた 翼を 45度ほど 後ろへ 倒した 形（行を 間引いて 上ほど 左へ ずらす）"""
    keep = [r for y, r in enumerate(rows) if y % 3 != 1]
    H = len(keep); out = []
    for y, r in enumerate(keep):
        sh = (H - 1 - y) * 2 // 3
        out.append('.' * 12 + r)
        out[-1] = out[-1][sh:] if sh else out[-1]
    w = max(len(r) for r in out); return [r.ljust(w, '.') for r in out]
WING_MID = swept(WING_UP)
def fan(W, H, cov, feathers):
    """あたり：打ちおろしの 翼。羽を 1枚ずつ（奥 → 手前）多角形で ぬり、黒で ふちどり、先に 炎。仕上げは 手で"""
    g = pix.grid(W, H)
    def put(pts, body):
        t = pix.grid(W, H); pix.poly(t, pts, body)
        o = pix.grid_of(pix.outline(pix.rows_of(t)))
        for y in range(H):
            for x in range(W):
                c = o[y + 1][x + 1]
                if c == '.': continue
                if c == body:
                    left = x == 0 or t[y][x - 1] == '.'
                    c = 'A' if left else 'B'
                    if x + 1 < W and t[y][x + 1] == '.' and body != 'C': c = 'C'
                g[y][x] = c
    for pts in feathers: put(pts, 'B')
    put(cov, 'B')
    # 炎の 先（手で：羽の いちばん 下の 3ドットを 赤 → だいだい → 黄）
    for x in range(W):
        ys = [y for y in range(H) if g[y][x] in 'ABC']
        if not ys: continue
        b = ys[-1]
        for d, c in ((0, 'Y'), (1, 'O'), (2, 'O'), (3, 'R')):
            if b - d >= 0 and g[b - d][x] in 'ABC' and b > H * .55: g[b - d][x] = c
    return pix.rows_of(g)
WING_DN = fan(26, 30, [(17, 1), (24, 0), (25, 5), (22, 10), (13, 11), (12, 7)],
              [[(20, 6), (24, 8), (21, 24), (18, 25)], [(15, 7), (21, 8), (15, 27), (12, 27)],
               [(11, 7), (17, 9), (9, 29), (6, 28)], [(8, 6), (13, 9), (3, 28), (1, 26)]])
for (x, y, c) in ((18, 3, 'O'), (19, 3, 'R'), (21, 6, 'R'), (15, 7, 'O')):   # 雨覆いの 残り火（手打ち）
    WING_DN[y] = WING_DN[y][:x] + c + WING_DN[y][x + 1:]
EYE = ['YYYO']
EYE_ALT = {'blink': ['kkkk'], 'atk0|atk1|atk2': ['wYYY'], 'hit': ['kYkk'], 'ko': ['OkOk']}
def dark(rows): return pix.recolor(rows, {'A': 'B', 'B': 'C', 'Y': 'O', 'O': 'R', 'R': 'r'})

GUST = [  # 攻撃：炎の つむじ風
    '........kkkk........',
    '.....kkkYYYOkk......',
    '...kkYYwwwYYOOkk....',
    '..kYwwkkkkkkYYOOk...',
    '.kYwkk......kkYORk..',
    '.kYk..........kYORk.',
    'kYOk...kkk.....kORk.',
    'kOOk..kYYOk....kORk.',
    'kOk..kYwOOk....kRk..',
    'kORk.kYOk.....kRRk..',
    '.kORk.kk....kkRRk...',
    '.kROOkk...kkROOk....',
    '..kRROOkkkROOkk.....',
    '...kkRRROOOkk.......',
    '.....kkkkkk.........',
]
UP, MID, DN = 'idle0|blink|walk0|atk0', 'idle1|idle3|walk1|walk3|atk2|hit|ko', 'idle2|walk2|atk1'

def lying_body(W, H):
    """あたり：たおれた 胴（横長の だ円）。光は 左上、右下は 影。仕上げは 下で 手で"""
    g = pix.grid(W, H); cx, cy, rx, ry = W / 2, H / 2, W / 2 - .2, H / 2 - .2
    for y in range(H):
        for x in range(W):
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if nx * nx + ny * ny > 1: continue
            l = -nx * .5 - ny * .85
            g[y][x] = 'A' if l > .55 else 'C' if l < -.35 else 'B'
    return pix.rows_of(g)
def ko_body():
    g = pix.grid_of(pix.outline(lying_body(32, 13)))
    for (x, y, c) in ((9, 4, 'r'), (10, 4, 'R'), (16, 6, 'r'), (21, 3, 'R'), (22, 3, 'r'), (13, 9, 'r'), (25, 7, 'r')): g[y][x] = c   # 消えかけの 残り火
    return pix.rows_of(g)
def squash(rows, drop=3):
    return [r for y, r in enumerate(rows) if y % drop != 1]
def cool(rows): return pix.recolor(rows, {'Y': 'O', 'O': 'R', 'R': 'r', 'w': 'Y'})   # ダウン：炎が 弱まる
TAIL_KO = [
    '...........kkkk.........',
    '.kk......kkROOOkk.......',
    'kROk...kkRORRRRROkkkkk..',
    '.kROkkkRRkk...kkRRROOOk.',
    '..kRRRROk.......kkkkkkk.',
    '...kkkkk................',
]
TALON_KO = pix.flip_v(TALON)
# ダウン：力なく 地面に たれた 翼（手打ち）。炎の 先は 消えかけ
WING_KO = [
    '...................kkkkkkkk.....',
    '..............kkkkkAAAAAAABkk...',
    '..........kkkkAAAAABBBBBBBBBBk..',
    '.......kkkAAABBBBBBBBBRBBBBBCk..',
    '.....kkAABBBkBBBBkBBBBBBBBBCCk..',
    '....kABBBkkABBBkkABBBkBBBBCCk...',
    '...kABBkkABBBkkABBBkkABBCCCk....',
    '..kABkkkABBkkkABBkkkABBCCkk.....',
    '.kABk.kABBk.kABBk.kABCCk........',
    'kRBk.kRBBk.kRBBk.kRBCk..........',
    'kOrk.kOrk..kOrk..kOrk...........',
    '.kk...kk....kk....kk............',
]
def head_ko():
    g = pix.grid_of(HEAD)
    for (x, y, c) in ((7, 6, 'Y'), (9, 6, 'Y'), (8, 7, 'O'), (7, 8, 'Y'), (9, 8, 'Y'), (8, 6, 'k'), (7, 7, 'k'), (9, 7, 'k'), (10, 7, 'k'), (11, 7, 'k'), (8, 8, 'k')): g[y][x] = c
    return pix.rows_of(g)
EYE_KO = ['kVk', 'VkV', 'kVk']
def ko_layers():
    return [
        dict(n='ko_tail', g='root', x=-9, y=54, rows=cool(TAIL_KO)),
        dict(n='ko_body', g='root', x=10, y=46, rows=ko_body()),
        dict(n='ko_talon', g='root', x=30, y=52, rows=TALON_KO),
        dict(n='ko_head', g='root', x=40, y=45, rows=head_ko()),
        dict(n='ko_wingF', g='root', x=3, y=49, rows=WING_KO),
    ]

def layers():
    L = base_layers()
    for l in L: l['not_'] = (l['not_'] + '|ko') if l.get('not_') else 'ko'
    return L + [dict(l, only='ko') for l in ko_layers()]
def base_layers():
    return [
        dict(n='wingB_up', g='wingB', x=18, y=0, rows=dark(WING_UP), only=UP),
        dict(n='wingB_mid', g='wingB', x=9, y=8, rows=dark(WING_MID), only=MID),
        dict(n='wingB_dn', g='wingB', x=20, y=24, rows=dark(WING_DN), only=DN),
        dict(n='tail', g='tail', x=1, y=33, rows=TAIL0, alt={'idle1|idle3|walk1|walk3|atk1': TAIL1}),
        dict(n='neck', g='head', x=38, y=17, rows=NECK),
        dict(n='body', g='body', x=17, y=22, rows=BODY),
        dict(n='talon', g='talon', x=31, y=40, rows=TALON),
        dict(n='head', g='head', x=40, y=8, rows=HEAD),
        dict(n='eye', g='head', x=48, y=15, rows=EYE, alt=EYE_ALT),
        dict(n='wingF_up', g='wingF', x=9, y=2, rows=WING_UP, only=UP),
        dict(n='wingF_mid', g='wingF', x=0, y=10, rows=WING_MID, only=MID),
        dict(n='wingF_dn', g='wingF', x=9, y=29, rows=WING_DN, only=DN),
        dict(n='gust', g='fx', x=57, y=17, rows=GUST, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'root': (0, 1)},
    'idle2': {'root': (0, 2), 'head': (0, -1), 'talon': (0, -1)},
    'idle3': {'root': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)},
    'walk1': {'root': (0, 0)},
    'walk2': {'root': (0, 1), 'talon': (-1, -1)},
    'walk3': {'root': (0, 0)},
    'atk0': {'root': (-3, -2), 'head': (-2, -1), 'talon': (1, 0)},
    'atk1': {'root': (3, 2), 'head': (2, 1), 'talon': (2, -1)},
    'atk2': {'root': (5, 2), 'head': (1, 1)},
    'hit': {'root': (-4, 0), 'head': (-1, -1), 'talon': (1, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'tail': 'body', 'talon': 'body', 'wingF': 'body', 'wingB': 'body', 'body': 'root', 'fx': 'root'}
