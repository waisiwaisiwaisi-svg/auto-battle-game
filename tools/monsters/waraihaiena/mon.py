# ワライハイエナ（あく・ノーマル × ハイエナ）手打ち GBA風・デフォルメ（2〜3頭身：仮面の 顔は 大きく、胴は 小さく、足は 短く 太く）
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


META = dict(id='waraihaiena', name='ワライハイエナ', types=['dark', 'normal'], base='ハイエナ', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1a2a',
    'F': '#d8b47e', 'G': '#9a7650', 'H': '#56402e',      # 毛皮（はい茶）
    'M': '#7a4a9a', 'P': '#3a2250',                      # たてがみ（あくの むらさき。明＝M）
    'S': '#f6f0e2', 'T': '#b4a8c0',                      # 笑いの 仮面
    'r': '#8a1a3a',
    'Y': '#ffe03a', 'O': '#e0402a',                      # 目
    'w': '#ffffff', 'q': '#c890e8',
}
LIGHT = set('FSwYq')
KEEP_BLACK = set('wYOr')

# ---- 頭：まるい 耳、太い あたま。顔の 前は 白い 仮面で、口は 三日月に さける（見せ所）----
HEAD_M = [
    '...##.....##.................',
    '..####...####................',
    '..####...####................',
    '..#####.#####................',
    '...################..........',
    '..###################........',
    '.######################......',
    '.########################....',
    '########################.....',
    '##########################...',
    '############################.',
    '#############################',
    '#############################',
    '#############################',
    '.###########################.',
    '.##########################..',
    '..########################...',
    '...######################....',
    '....###################......',
    '......#############..........',
]
def head(mode=''):
    g = grid_of(HEAD_M)
    # 仮面：顔の 前半分（だ円）
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == '#' and ((x - 20) / 10.5) ** 2 + ((y - 11.5) / 8.5) ** 2 <= 1: g[y][x] = 'm'
    m = shade(rows_of(g), {'#': 'FGH', 'm': 'SST'}, 2, 2, 2)
    m = over(m, ['', '.....G....G', '....GH...GH', '....H....H', '', '', '',
                 '', '', '', '', '', '', '............................k', '...........................kk'])   # 耳の 中・鼻
    # 三日月の 口：ほおから ほおへ 大きく 笑う（上の 線と 下の 線の あいだに きば）
    if mode == 'atk':
        top = {x: 12 - (1 if 14 <= x <= 25 else 0) for x in range(10, 28)}
        bot = {x: 13 + round(5 * (1 - ((x - 19) / 9) ** 2)) for x in range(10, 28)}
    else:
        top = {x: 12 + round(2.0 * (1 - ((x - 19) / 9) ** 2)) for x in range(10, 28)}
        bot = {x: 13 + round(4.5 * (1 - ((x - 19) / 9) ** 2)) for x in range(10, 28)}
    G2 = grid_of(m)
    for y in range(len(G2)):          # 仮面の ふち（顔の 毛との さかい）に 細い 影の 線
        for x in range(1, len(G2[0])):
            if G2[y][x] in 'ST' and G2[y][x - 1] in 'FGH': G2[y][x] = 'T'
    for x, y in ((12, 10), (13, 11), (23, 10), (24, 9)):   # 仮面の もよう（ほおの むらさきの すじ）
        G2[y][x] = 'M'
    for x in range(10, 28):
        t, b = top[x] - (1 if x in (10, 27) else 0), bot[x]
        for y in range(t, b + 1): G2[y][x] = 'k' if y in (t, b) else 'r'
        if b - t >= 3:
            if x % 2: G2[t + 1][x] = 'w'
            else: G2[b - 1][x] = 'w'
    return outline(rows_of(G2))
HEAD = head(); HEAD_ATK = head('atk')
# するどい 目：仮面の 目あなの ふち＋白い 光＋金と 赤の 虹彩＋たての ひとみ（笑っているのに 目は 笑わない）
EYE = ['kk......', 'TkkkkkT.', 'kwYkYkkk', 'kYOkOOk.', '.kkkkk..']
EYE_ALT = {'blink': ['kk......', 'TkkkkkT.', 'SSSSSSSS', 'kkkkkkk.', '.TTTTT..'],
           'hit': ['kk......', 'TkkSSkk.', 'SSkkkSS.', 'TkkSSkk.', '.TTTTT..'],
           'atk0|atk1|atk2': ['kkk.....', 'TkwkkkkT', 'kwYYkYkk', 'kYOOkOk.', '.kkkkk..'],
           'ko': ['........', 'TkSSSkT.', 'SSkSkSS.', 'SSSkSSS.', 'SSkSkSS.']}

# ---- たてがみ：首から 背へ さか立つ むらさきの とげ毛 ----
def mane(ph=0):
    m = mask(26, 16, [('p', [(26, 16), (24, 2), (21, 8), (19, 0 + ph), (16, 7), (13, 2 + ph), (11, 9), (8, 5), (6, 11), (3, 9), (0, 16)], '#')])
    return outline(shade(m, {'#': 'qMP'}, 1, 2, 2))
MANE = mane(); MANE2 = mane(1)
# ---- 胴（小さく 丸い。肩が 高く 腰が 低い ハイエナの 背。はんてん）----
BODY = outline(over(shade(mask(30, 18, [('e', 15, 10, 14.5, 7.5, '#'), ('e', 21, 8, 8, 8, '#')]), {'#': 'FGH'}, 2, 2, 3), [
    '', '', '', '', '',
    '.....H....H......H',
    '..H....H.....H',
    '......H....H.....H',
    '...H.......',
]))
# ---- 足（前足は 太く 長め、後ろ足は 短い。黒い 爪）----
FLEG_M = ['######', '######', '######', '.#####', '.#####', '.#####', '.#####', '#######']
HLEG_M = ['#######', '#######', '.######', '..####', '..####', '.######']
def leg(rows, far=False):
    m = shade(rows, {'#': 'FGH'}, 1, 1, 2)
    m = over(m, [''] * (len(rows) - 1) + ['.' * (len(rows[-1]) - 5) + 'H.H.H'])
    r = opentop(outline(m), 2)
    return recolor(r, {'F': 'G', 'G': 'H', 'H': 'l'}) if far else r
FLEG = leg(FLEG_M); FLEGF = leg(FLEG_M, True); HLEG = leg(HLEG_M); HLEGF = leg(HLEG_M, True)
# ---- しっぽ（短く、先は むらさきの ふさ）----
TAIL = outline(shade(mask(12, 10, [('p', [(12, 1), (12, 4), (6, 5), (4, 4)], '#'), ('e', 3.5, 5.5, 3.5, 4, 'm')]), {'#': 'FGH', 'm': 'qMP'}, 1, 1, 1))
TAIL2 = outline(shade(mask(12, 10, [('p', [(12, 1), (12, 4), (6, 4), (4, 2)], '#'), ('e', 3.5, 3, 3.5, 3.2, 'm')]), {'#': 'FGH', 'm': 'qMP'}, 1, 1, 1))
# ---- 攻撃：三日月の やみの 爪あと ----
SLASH = ['......kkk', '....kkqMk', '...kqMPk.', '..kqMPk..', '.kqMPk...', '.kqMk....', 'kqMPk....', 'kqMk.....', '.kqMk....', '..kkk....']
SLASH2 = ['.....kkk..', '...kkqqMk.', '..kqMMPk..', '.kqMPkk...', '.kqMk.....', 'kqMPk.....', 'kqMk......', 'kqMPk.....', '.kqMMk....', '..kkkk....']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=7, y=33, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='hlegF', g='legB', x=19, y=48, rows=HLEGF),
        dict(n='flegF', g='legA', x=38, y=46, rows=FLEGF),
        dict(n='mane', g='mane', x=16, y=20, rows=MANE, alt={'idle1|idle3|walk1|walk3|atk2': MANE2}),
        dict(n='body', g='body', x=13, y=31, rows=BODY),
        dict(n='hleg', g='legA', x=14, y=49, rows=HLEG),
        dict(n='fleg', g='legB', x=33, y=47, rows=FLEG),
        dict(n='head', g='head', x=32, y=10, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=45, y=16, rows=EYE, alt=EYE_ALT),
        dict(n='slash', g='head', x=59, y=20, rows=SLASH, alt={'atk2': SLASH2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'mane': (0, -1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-2, 1), 'legA': (-1, 0), 'mane': (0, -1)},
    'atk1': {'root': (4, 0), 'head': (1, 0)}, 'atk2': {'root': (5, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'mane': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
