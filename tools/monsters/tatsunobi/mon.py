# タツノビ（ドラゴン・ほのお × タツノオトシゴ）手打ち GBA風・デフォルメ（2〜3頭身：竜の 頭は 大きく、腹は 小さく 丸く、炎の うず尾は 大きく）
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
META = dict(id='tatsunobi', name='タツノビ', types=['dragon', 'fire'], base='タツノオトシゴ', size='M')
EYE_BOX = (30, 10, 9, 6)
PAL = {
    'k': '#101018', 'l': '#4a1420',
    'F': '#ff9c5a', 'G': '#d8442c', 'H': '#7c1c30',      # うろこ
    'Y': '#ffe27a', 'O': '#d88c34',                      # 腹の 節
    'Q': '#ff9a1a', 'y': '#fff8c8',                      # 炎（＋Y／G）
    'S': '#f2e8d2', 'T': '#a89478',                      # 竜の 角
    'C': '#b6f45a', 'B': '#2e9a3a',                      # 目（みどり）
    'w': '#ffffff',
}
LIGHT = set('FYySw')
KEEP_BLACK = set('wCByY')

# ---- 頭：竜の 頭に 長い 筒の 口（タツノオトシゴの 口）。前へ 少し うつむく ----
HEAD_M = [
    '........######...............',
    '......##########.............',
    '....##############...........',
    '...################..........',
    '..##################.........',
    '..###################........',
    '.#####################.......',
    '.######################......',
    '.#######################.....',
    '.############################',
    '#############################',
    '#############################',
    '#############################',
    '.###########################.',
    '.################.....',
    '..##############......',
    '..#############.......',
    '...###########........',
    '....#########.........',
    '.....#######..........',
]
def head(mode=''):
    m = shade(HEAD_M, {'#': 'FGH'}, 2, 2, 2)
    m = over(m, [
        '', '', '', '', '', '',
        '',
        '',
        '',
        '',
        '..H.....................',
        '...H...................kk',     # ほおの うろこ・鼻の あな
        '..H.H',
        '...H.H',
        '..H.H',
        '...H',
    ])
    if mode == 'atk':   # 筒の 口を 開いて 火を ふく
        m = over(m, [''] * 11 + [
                     '...............kkkkkkkkkkkkkk',
                     '..............kwkwQQQQQQQQQQQ',
                     '...............kwkwkkkkkkkkkk'])
    else:               # 閉じた 口：きば
        m = over(m, [''] * 12 + ['...............kkkkkkkkkkkkkk', '................kwkk.kwkk.kwk'])
    return outline(m)
HEAD = head(); HEAD_ATK = head('atk')
# 竜の 角（後ろへ 反る 2本）
HORN = ['kk..........', 'kSkk........', 'kSSSkk......', '.kTSSSkk....', '..kTTSSSkkk.', '...kkTTTSSSk', '.....kkTTTTk', '.......kkkk.']
HORN2 = ['.kk.........', '.kSkk.......', '.kSSSkk.....', '..kTSSSkk...', '..kTTSSSkk..', '...kkTTTSSk.', '.....kkTTTk.', '.......kkk..']
# 爬虫類の つり目（A）：白目なし。みどりの 虹彩（明・暗）に 細い たての スリット。上まぶたは 太い 黒、下まぶたは 細い 赤茶
EYE = ['kkk......',
       'HkkkkkkkH',
       'kCwCkCCBk',
       '.BCCkCBH.',
       '..HBkBH..',
       '...HHH...']
EYE_ALT = {'blink': ['kkk......', 'HkkkkkkkH', 'GGGGGGGGk', '.GGGGGHH.', '..HHHH...', '.........'],
           'hit': ['kkk......', 'HkkkkkH..', 'GkCkBkkk.', '.GHBkH...', '..GHH....', '.........'],      # 細めて ゆがむ
           'atk0|atk1|atk2': ['kkkk.....', 'HkkkkkkkH', 'kCwCkCCBk', 'kCCCkCCBk', '.BCCkCBH.', '..HHHHH..'],   # 見開き、スリットが のびる
           'ko': ['.........', 'HkGGGkH..', 'GGkGkGG..', 'GGGkGGG..', 'GGkGkGG..', '.........']}

# ---- 胴：小さく 丸い 腹（節の ある 腹板）----
def body():
    m = mask(22, 22, [('e', 11, 11, 10, 10.5, '#'), ('e', 15, 13, 6, 8, 'b')])
    m = shade(m, {'#': 'FGH', 'b': 'YYO'}, 2, 2, 3)
    g = grid_of(m)
    for y in range(6, 22, 3):           # 腹の 節（横の 線）
        for x in range(22):
            if g[y][x] in 'YO': g[y][x] = 'O'
    return outline(rows_of(g))
BODY = body()
# ---- 背びれ：炎の ひれ ----
FIN = ['.....kk.......', '....kYk...kk..', '...kYQk..kYk..', '..kYQQk.kYQk.k', '.kYQGQkkYQGkkQk', 'kYQGGQkQGGGkQGk', 'kQGGGQQGGGGQQGk', '.kGGGGGGGGGGGk.']
FIN2 = ['...kk.........', '...kYk..kk....', '....kYk.kYk..k.', '..kYQQkkYQk.kQk', '.kYQGQkkYQGkkQk', 'kYQGGQkQGGGkQGk', 'kQGGGQQGGGGQQGk', '.kGGGGGGGGGGGk.']
# ---- 小さな 竜の 腕（3本の 爪）----
ARM = opentop(outline(over(shade(['####...', '#####..', '.#####.', '..#####', '...####'], {'#': 'FGH'}, 1, 1, 1), ['', '', '', '', '...w.w'])), 1)

# ---- 炎の うず尾（見せ所）：うろこの 尾が 先へ ゆくほど 炎に なり、くるりと 巻く ----
def spiral(ph=0):
    W, H = 34, 30; g = grid(W, H)
    cx, cy, R0 = 15, 13, 11
    def pt(t):
        th = math.radians(-37 + 430 * t + ph * 14); r = R0 * (1 - .7 * t)
        return cx + r * math.cos(th), cy + r * math.sin(th), th
    # 外がわへ 立つ 炎の 舌（先は 尾の 流れと 逆へ なびく）
    for t in (.36, .5, .64):
        x, y, th = pt(t); ox, oy = math.cos(th), math.sin(th); tx, ty = -oy, ox
        poly(g, [(x - tx * 2.5, y - ty * 2.5), (x + tx * 2.5, y + ty * 2.5), (x + ox * 6 + tx * 3, y + oy * 6 + ty * 3)], 'f')
    N = 70
    for i in range(N + 1):
        t = i / N; x, y, _ = pt(t)
        w = 3.6 - 2.3 * t
        ellipse(g, x, y, w, w, '#' if t < .3 else 'f')
    m = shade(rows_of(g), {'#': 'FGH', 'f': 'yYQ'}, 1, 1, 2)
    return outline(m)
TAIL = spiral(); TAIL2 = spiral(1)
SPARK = ['..k..', '.kYk.', 'kYyYk', '.kYk.', '..k..']   # 尾の 火の粉（はなれているのは 意図的）

# ---- 攻撃：長い 炎の ブレス ----
BREATH = [
    '........kk..kkk.....',
    '.....kkkQQkkYYQkk...',
    'kkkkkQQYYYYQyyYYQkk.',
    'yyyyyyyyyyyyyyyyyYQk',
    'kkkkkQQYYYYQyyYYQkk.',
    '.....kkkQQkkYYQkk...',
    '........kk..kkk.....',
]
BREATH2 = [
    '.....kk....kkk.......',
    '...kkQQk..kYYQk..k...',
    'kkkQYYYQkkQyyYQkkQk..',
    'yyyyyyyyyyyyyyyyYYQQk',
    'kkkQYYYQkkQyyYQkkQk..',
    '...kkQQk..kYYQk..k...',
    '.....kk....kkk.......',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=1, y=34, rows=TAIL, alt={'idle1|idle3|walk1|walk3|atk2': TAIL2}),
        dict(n='spark', g='tail', x=0, y=34, rows=SPARK, only='idle1|idle3|walk1|walk3'),
        dict(n='fin', g='fin', x=10, y=24, rows=FIN, alt={'idle1|idle3|walk1|walk3|atk2': FIN2}),
        dict(n='body', g='body', x=17, y=25, rows=BODY),
        dict(n='head', g='head', x=20, y=5, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='horn', g='head', x=14, y=5, rows=HORN, alt={'idle1|idle3|walk1|walk3': HORN2}),
        dict(n='eye', g='head', x=30, y=10, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='arm', x=35, y=35, rows=ARM),
        dict(n='breath', g='head', x=50, y=14, rows=BREATH, alt={'atk2': BREATH2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -2), 'tail': (0, 1)}, 'idle3': {'root': (0, -1)}, 'blink': {},
    'walk0': {'root': (1, -1), 'tail': (-1, 0)}, 'walk1': {'root': (1, -2), 'head': (0, 1)},
    'walk2': {'root': (0, -1), 'tail': (1, 0)}, 'walk3': {'root': (0, 0), 'head': (0, -1)},
    'atk0': {'head': (-2, 1), 'fin': (-1, 0), 'arm': (-1, 0), 'body': (-1, 0)}, 'atk1': {'root': (3, 0), 'head': (1, 0)}, 'atk2': {'root': (4, 0), 'head': (1, 0)},
    'hit': {'root': (-3, -1), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'fin': 'body', 'arm': 'body', 'tail': 'body', 'body': 'root'}
