# キカンリュウ（ドラゴン・はがね × 竜）手打ち GBA風・デフォルメ（2〜3頭身：鋼の 竜頭は 大きく、ボイラーの 胴は 小さく 丸く、車輪の 足は 短く）
import pix
from pix import grid, rows_of, grid_of, outline, ellipse, poly, recolor, flip_v


# ---- 下書きの 道具（あたり用。目・きば・模様などの 仕上げは 下で 手打ち）----
def mask(W, H, shapes):
    """('e', cx, cy, rx, ry, ch) だ円 / ('p', [(x, y)...], ch) 多角形 / ('r', x0, y0, x1, y1, ch) 四角。ch='.' で けずる"""
    g = grid(W, H)
    for s in shapes:
        if s[0] == 'e': ellipse(g, s[1], s[2], s[3], s[4], s[5])
        elif s[0] == 'p': poly(g, s[1], s[2])
        elif s[0] == 'r':
            for y in range(max(0, s[2]), min(H, s[4])):
                for x in range(max(0, s[1]), min(W, s[3])): g[y][x] = s[5]
    return rows_of(g)
def shade(rows, ramps, lw=1, dw=2, drw=None):
    """左上の 光：上・左の ふち lw ドットは 明、下 dw・右 drw ドットは 暗（素材ごとに）"""
    drw = dw if drw is None else drw
    g = grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            def run(dy, dx):
                for i in range(1, 9):
                    yy, xx = y + dy * i, x + dx * i
                    if not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m: return i
                return 9
            hi, mid, lo = ramps[m]
            if run(1, 0) <= dw or run(0, 1) <= drw: o[y][x] = lo
            elif run(-1, 0) <= lw or run(0, -1) <= lw: o[y][x] = hi
            else: o[y][x] = mid
    return rows_of(o)
def over(base, ov, x=0, y=0):
    """手打ちの 小さな 絵を 重ねる（' ' と '.' は すける、'_' は 消す）"""
    g = grid_of(base)
    for j, r in enumerate(ov):
        for i, c in enumerate(r):
            if c in '. ': continue
            if 0 <= y + j < len(g) and 0 <= x + i < len(g[0]): g[y + j][x + i] = '.' if c == '_' else c
    return rows_of(g)
def opentop(rows, n=1):
    """付け根を 胴に うめる：上 n 行の 輪郭を 消す"""
    return [r.replace('k', '.') if j < n else r for j, r in enumerate(rows)]
def mirror(rows): return pix.flip_h(rows)


import math
META = dict(id='kikanryu', name='キカンリュウ', types=['dragon', 'steel'], base='竜', size='L')
EYE_BOX = (41, 13, 10, 5)
PAL = {
    'k': '#101018', 'l': '#2a2438',
    'S': '#e2e8f2', 'T': '#8e9ab4', 'U': '#4c5470',      # 鋼（頭・首・車輪）
    'R': '#e4604c', 'Q': '#a42e34', 'P': '#5a1a2a',      # ボイラー（赤い 機関車）
    'Y': '#ffd85a', 'O': '#c0862a', 'y': '#fff6c6',      # 真ちゅう・炎
    'C': '#7ae8ff', 'B': '#2a8ab8',                      # 目
    'w': '#ffffff',
}
LIGHT = set('SRYyw')
KEEP_BLACK = set('wYyCB')

# ---- 頭：鋼の 竜頭。下あごは 機関車の 排障器（はいしょうき）の ような 格子、角は 汽笛 ----
HEAD_M = [
    '........#########...............',
    '......#############.............',
    '....#################...........',
    '...###################..........',
    '..######################........',
    '.#########################......',
    '.###########################....',
    '##############################..',
    '###############################.',
    '################################',
    '################################',
    '###############################.',
    '##############################..',
    '###########.....................',
    '############....................',
    '################################',
    '################################',
    '.##############################.',
    '..############################..',
    '...#########################....',
    '.....####################.......',
]
def head(mode=''):
    m = shade(HEAD_M, {'#': 'STU'}, 2, 2, 2)
    m = over(m, ['', '', '',
                 '...........T.....T',            # 鋼板の つなぎ目と びょう
                 '..........T.....T',
                 '...T.....T.....T..............k',
                 '..T.T...T.....T...............k',
                 '...T',
                 ])
    if mode == 'atk':   # 口を 開いて 火を ふく
        m = over(m, [''] * 12 + [
            '..........kkkkkkkkkkkkkkkkkkkkkkk',
            '.........kwkkwkkwkkwkkwkkwkkwkk__',
            '.........kOOOOOOOOOOOOOOOOOOOOO__',
            '.........kOOOOOOOOOOOOOOOOOOOOO__',
            '.........kwkkwkkwkkwkkwkkwkkwkkk_',
            '..........kTkTkTkTkTkTkTkTkTkTk',
        ])
    else:               # 閉じた 口：きばと 格子の あご
        m = over(m, [''] * 12 + [
            '..........kkkkkkkkkkkkkkkkkkkkkk',
            '.........kwkkwkkwkkwkkwkkwkkwkkk',
            '.........kkkkkkkkkkkkkkkkkkkkkkk',
            '..........TkTkTkTkTkTkTkTkTkTkT',
            '...........TkTkTkTkTkTkTkTkTkT',
            '............kTkTkTkTkTkTkTkTk',
        ])
    return outline(m)
HEAD = head(); HEAD_ATK = head('atk')
# 汽笛の 角（真ちゅう）
HORN = ['kk.........', 'kYkk.......', 'kYYOkk.....', '.kYYOOkk...', '.kkYYOOOkk.', '..kYYYOOOk.', '..kkYYOOOOk', '...kkkkkkkk']
# バイザー（J）：機関車の 前照灯。鋼の ひさしの 下に 横長の 光る レンズ（黄・薄黄・真ちゅう）と 斜めの 反射線。瞳なし
EYE = ['kkkkkkkkk.',
       'kyywyYYYOk',
       'kYwyYYYOOk',
       '.kkkkkkkkk',
       '..UUUUUU..']
EYE_ALT = {'blink': ['kkkkkkkkk.', 'kOOUOOOOUk', 'kUUUUUUUUk', '.kkkkkkkkk', '..UUUUUU..'],     # 灯が 落ちる
           'hit': ['kkkkkkkkk.', 'kyOkYUYkOk', 'kOkYkOkOUk', '.kkkkkkkkk', '..UUUUUU..'],      # レンズに ひび、ちらつく
           'atk0|atk1|atk2': ['kkkkkkkkk.', 'kywwyyyyyky', 'kwwyyyyyYkyy', '.kkkkkkkkky', '..UUUUUU..'],   # 全開で 照らす
           'ko': ['kkkkkkkkk.', 'kUkUUUkUUk', 'kUUkUkUUUk', '.kkkkkkkkk', '..UUUUUU..']}

# ---- 首（煙突の ような 太い 筒。真ちゅうの 輪）----
NECK = outline(over(shade(mask(14, 16, [('p', [(0, 16), (3, 0), (13, 0), (13, 16)], '#')]), {'#': 'STU'}, 2, 2, 2), [
    '', '', '', '...YYYYYYYYYY', '...OOOOOOOOOO', '', '', '', '', '..YYYYYYYYYYY', '..OOOOOOOOOOO']))
# ---- 胴：ボイラー（丸い 筒、真ちゅうの 帯と びょう）----
def boiler():
    m = shade(mask(34, 20, [('e', 17, 10, 16.5, 9.5, '#')]), {'#': 'RQP'}, 2, 2, 3)
    g = grid_of(m)
    for bx in (9, 18, 27):
        for y in range(20):
            if g[y][bx] != '.': g[y][bx] = 'Y' if y < 7 else 'O'
            if g[y][bx + 1] != '.': g[y][bx + 1] = 'O'
    for bx in (5, 14, 23):
        for y in (5, 9, 13):
            if g[y][bx] in 'RQ': g[y][bx] = 'Y'
    return outline(rows_of(g))
BOILER = boiler()
# ---- 煙突（背中）と 炎（見せ所）----
STACK = outline(over(shade(mask(12, 14, [('p', [(0, 0), (12, 0), (10, 4), (9, 14), (3, 14), (2, 4)], '#')]), {'#': 'STU'}, 1, 1, 2),
                     ['YYYYYYYYYYYY', 'OOOOOOOOOOOO']))
FLAME = ['....kk....kk..', '...kYk...kYk..', '..kYOk..kYOk..', '..kYyOk.kYyk.k', '.kYyyOkkYyOkkR', '.kYyyyOYyyOkRk', 'kYyyyyyyyyOkRk', 'kYyyyyyyyyyORk', 'kOYyyyyyyyyOk.', '.kOYyyyyyyOk..', '..kOOYYYOOk...']
FLAME2 = ['..kk.....kk...', '..kYk...kYk...', '...kYk.kYOk.k.', '..kYyOkkYyOkRk', '.kYyyOkYyyOkRk', 'kYyyyyOyyyOkRk', 'kYyyyyyyyyOkk.', 'kYyyyyyyyyyORk', 'kOYyyyyyyyyOk.', '.kOYyyyyyyOk..', '..kOOYYYOOk...']
FLAME_ATK = ['.k..kk...kk..k.', 'kYk.kYk.kYk.kYk', 'kYOkkYOkkYOkYOk', 'kYyOkYyOkYyOYyk', 'kYyyOYyyOyyyyOk', 'kYyyyyyyyyyyyOk', 'kYyyywwwwyyyyOk', 'kYyyyywwyyyyyOk', 'kOYyyyyyyyyyOk.', '.kOYyyyyyyyOk..', '..kOOYYYYYOOk..']
# ---- 車輪の 足（短い 足の 先が 車輪。手前の 2つは 連結棒で つながる）----
def wheel(ph=0, far=False):
    N = 13; g = grid(N, N); c = 6
    ellipse(g, c + .5, c + .5, 6.5, 6.5, 'U'); ellipse(g, c + .5, c + .5, 5, 5, 'T')
    for i in range(4):
        a = math.radians(i * 45 + ph * 22.5)
        pix.line(g, round(c - 4.5 * math.cos(a)), round(c - 4.5 * math.sin(a)), round(c + 4.5 * math.cos(a)), round(c + 4.5 * math.sin(a)), 'U')
    ellipse(g, c + .5, c + .5, 1.6, 1.6, 'Y')
    for y in range(N):                       # 左上の 光
        for x in range(N):
            if g[y][x] == 'U' and ((x - c) ** 2 + (y - c) ** 2) > 30 and x + y < 10: g[y][x] = 'S'
    r = outline(rows_of(g))
    return recolor(r, {'S': 'T', 'T': 'U', 'Y': 'O'}) if far else r
WHEEL = wheel(); WHEEL2 = wheel(1); WHEELF = wheel(0, True); WHEELF2 = wheel(1, True)
LEG = opentop(outline(shade(['######', '######', '.#####', '.####.'], {'#': 'RQP'}, 1, 1, 2)), 2)
ROD = ['kkkkkkkkkkkkkkkkkkkkk', 'kSSTTTTTTTTTTTTTTTTUk', 'kkkkkkkkkkkkkkkkkkkkk']
# ---- しっぽ（鋼の 節）----
TAIL = outline(shade(mask(16, 10, [('p', [(16, 1), (16, 9), (8, 8), (0, 3), (8, 2)], '#')]), {'#': 'STU'}, 1, 2, 2))
# ---- 攻撃：炎の ブレス ----
BREATH = ['......kk..kk.....', '...kkkYYkkYYkk...', 'kkkYYyyyyyyyYYkk.', 'yyyyyyyyyyyyyyyOk', 'kkkYYyyyyyyyYYkk.', '...kkkYYkkYYkk...', '......kk..kk.....']
BREATH2 = ['....kk...kk..k...', '..kkOYk.kYOk.kY..', 'kkYYyyYkYyyYkkYk.', 'yyyyyyyyyyyyyyyyk', 'kkYYyyYkYyyYkkYk.', '..kkOYk.kYOk.kY..', '....kk...kk..k...']

NB = 'atk1|atk2'
WALT = {'walk1|walk3|atk2': WHEEL2}
def layers():
    return [
        dict(n='tail', g='tail', x=1, y=38, rows=TAIL),
        dict(n='wheelHF', g='legB', x=17, y=47, rows=WHEELF, alt={'walk1|walk3|atk2': WHEELF2}),
        dict(n='wheelFF', g='legB', x=38, y=47, rows=WHEELF, alt={'walk1|walk3|atk2': WHEELF2}),
        dict(n='flame', g='flame', x=15, y=8, rows=FLAME, alt={'idle1|idle3|walk1|walk3': FLAME2, 'atk0|' + NB: FLAME_ATK}),
        dict(n='stack', g='body', x=16, y=18, rows=STACK),
        dict(n='neck', g='body', x=36, y=25, rows=NECK),
        dict(n='boiler', g='body', x=10, y=29, rows=BOILER),
        dict(n='legH', g='legA', x=15, y=45, rows=LEG),
        dict(n='legF', g='legA', x=35, y=45, rows=LEG),
        dict(n='wheelH', g='legA', x=11, y=48, rows=WHEEL, alt=WALT),
        dict(n='wheelF', g='legA', x=31, y=48, rows=WHEEL, alt=WALT),
        dict(n='rod', g='rod', x=17, y=53, rows=ROD),
        dict(n='horn', g='head', x=31, y=4, rows=HORN),
        dict(n='head', g='head', x=32, y=7, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=41, y=13, rows=EYE, alt=EYE_ALT),
        dict(n='breath', g='head', x=64, y=20, rows=BREATH, alt={'atk2': BREATH2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1), 'flame': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'flame': (0, -1)}, 'blink': {},
    'walk0': {'body': (0, -1), 'rod': (-1, -1)}, 'walk1': {'body': (0, 0), 'rod': (0, 0)},
    'walk2': {'body': (0, -1), 'rod': (1, -1)}, 'walk3': {'body': (0, 0), 'rod': (0, 1)},
    'atk0': {'body': (-1, 1), 'head': (-2, 0), 'flame': (0, -2)}, 'atk1': {'root': (3, 0), 'head': (1, 0), 'flame': (0, -2)}, 'atk2': {'root': (4, 0), 'head': (1, 0), 'flame': (0, -3)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'flame': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'rod': 'root'}
