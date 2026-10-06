# クビナシバ（ゴースト・あく × 馬）手打ち GBA風・デフォルメ（2〜3頭身：霊火の 頭は 大きく、胴は 小さく 丸く、足は 短く 太く）
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


META = dict(id='kubinashiba', name='クビナシバ', types=['ghost', 'dark'], base='馬', size='L')
PAL = {
    'k': '#101018', 'l': '#2a1a3c',
    'R': '#7a6e9a', 'Q': '#463a60', 'P': '#261e36',      # 胴（夜の 黒馬）
    'S': '#c4b2e2', 'T': '#7e5eaa',                      # 黒煙の たてがみ（暗＝P）
    'C': '#dafff6', 'B': '#5ee0d2', 'A': '#2a8aa0',      # 霊火の 頭
    'Y': '#ffe45a', 'O': '#ff4a30',                      # 目
    'H': '#d0c094', 'G': '#7c6a4c',                      # ひづめ
    'w': '#ffffff',
}
LIGHT = set('RSCYHw')
KEEP_BLACK = set('wYOCB')

# ---- 胴（小さく 丸い たる型、胸と しりが 少し 出る）＋太く 短い 首 ----
BODY = outline(over(shade(mask(36, 24, [
    ('e', 15, 15, 14, 8, '#'), ('e', 23, 14, 8, 8, '#'), ('e', 8, 13, 7, 7, '#'),
    ('p', [(20, 10), (25, 1), (32, 0), (34, 6), (31, 16), (22, 18)], '#'),
]), {'#': 'RQP'}, 2, 2, 3), [
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '..R..........Q',
    '..R.........P',
    '.....Q.....QQ',
    '......QQQQQ',
]))
# ---- 黒煙の たてがみ：首すじから もくもく 立ちのぼり、後ろへ 流れて うずを 巻く ----
MANE_M = [
    '....##....................',
    '...###.......##...........',
    '..###.......###...........',
    '..##.......###............',
    '..##......####............',
    '..###....#####.....##.....',
    '...####.######....###.....',
    '....##########...####.....',
    '.....#########..#####.....',
    '......#########.#####.....',
    '.......###############....',
    '........##############....',
    '.##......##############...',
    '###.......#############...',
    '##........##############..',
    '##.......###############..',
    '###.....################..',
    '.####..#################..',
    '..######################..',
    '...######################.',
    '....#####################.',
    '......###################.',
    '.........################.',
    '............#############.',
    '..............###########.',
    '................#########.',
    '..................#######.',
]
def wave(rows, ph):
    """煙の ゆらぎ：上の 行ほど 左右に ずらす"""
    if not ph: return rows
    return [('.' + r[:-1]) if j < 9 and (j // 3) % 2 == 0 else r for j, r in enumerate(rows)]
def mane(ph=0):
    m = shade(wave(MANE_M, ph), {'#': 'STP'}, 1, 2, 1)
    m = over(m, ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '...........T', '..........T', '.........T', '........T........T', '.......T........T', '...............T', '..............T'])
    return outline(m)
MANE = mane(); MANE2 = mane(1)

# ---- 霊火の 頭（見せ所）：馬の 頭の 形に 燃える 青い 炎。耳の 先と ひたいが 炎 ----
HEAD_M = [
    '.......#.....#.......#........',
    '......##....##......##........',
    '......###..###.....##.........',
    '.....####.####....###.........',
    '.....##########..###..........',
    '....#################.........',
    '...##################.........',
    '...###################........',
    '..#####################.......',
    '..######################......',
    '.########################.....',
    '.#########################....',
    '###########################...',
    '############################..',
    '#############################.',
    '#############################.',
    '.############################.',
    '.############################.',
    '..###########################.',
    '...#########################..',
    '....##########.....########...',
    '.....#######..................',
    '......####....................',
]
def head(mode=''):
    m = shade(HEAD_M, {'#': 'CBA'}, 1, 2, 2)
    m = over(m, [
        '.......C.....C.......C',
        '......CB....CB......CB',
        '.......B.....B.....CB',
        '..................CB',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '..........A',
        '...........A',
        '............A',
        '............A',
        '...........A',
        '..........A',
        '.......AAA',
        '........................kkA',     # 鼻の あな
        '........................kA',
    ])
    if mode == 'atk':   # 口を 大きく 開く（上下の きば）
        m = over(m, [''] * 17 + [
            '...............kkkkkkkkkkkkkk',
            '..............kwkwOOOOOOkwkwk',
            '.............kOOOOOOOOOOOOOk.',
            '.............kOOOOOOOOOOOOk..',
            '..............kwkwOOOOkwk....',
            '...............kkkkkkkkkk....',
        ])
    else:               # 閉じた 口：さけ目と はみ出す きば
        m = over(m, [''] * 19 + [
            '..............kkkkkkkkkkkkkkk',
            '..............kwkAAkwkAAkwkk.',
            '...............k.kk.k.kk.kk..',
        ])
    return outline(m)
HEAD = head(); HEAD_ATK = head('atk')
# するどい 目：まゆの ひさし（黒）＋白い 光＋黄と 赤の 虹彩＋たての ひとみ＋下まぶた
EYE = ['kk......', 'AkkkkkB.', 'AkwYkYkk', 'AkYOkOOk', '.Akkkkk.']
EYE_ALT = {'blink': ['kk......', 'AkkkkkB.', 'ABBBBBBB', 'Akkkkkkk', '.ABBBBB.'],
           'hit': ['kk......', 'AkkBBkkB', 'ABkkkkBB', 'AkkBBkkB', '.ABBBBB.'],
           'atk0|atk1|atk2': ['kkk.....', 'AkwkkkkB', 'AkwYYkYk', 'AkYOOkOk', '.Akkkkk.'],
           'ko': ['........', 'AkBBBkB.', 'ABkBkBB.', 'ABBkBBB.', 'ABkBkBB.']}

# ---- 足（短く 太い、ひざが 少し くびれ、白っぽい ひづめ）----
LEG_M = ['#######', '#######', '.######', '.#####.', '.####..', '.#####.', 'hhhhhh.', 'hhhhhh.', 'hhhhhh.']
def leg(far=False):
    m = shade(LEG_M, {'#': 'RQP', 'h': 'HHG'}, 1, 1, 2)
    r = opentop(outline(m), 2)
    return recolor(r, {'R': 'Q', 'Q': 'P', 'H': 'G'}) if far else r
LEG = leg(); LEGF = leg(True)

# ---- 黒煙の しっぽ（立ちのぼる）----
TAIL_M = [
    '..####..........',
    '.######.........',
    '###..###........',
    '##....###.......',
    '###...####......',
    '.##...#####.....',
    '......######....',
    '.......######...',
    '........######..',
    '.........######.',
    '..........######',
    '...........#####',
    '............####',
]
def tail(ph=0):
    return outline(shade(wave(TAIL_M, ph), {'#': 'STP'}, 1, 2, 1))
TAIL = tail(); TAIL2 = tail(1)

# ---- 攻撃：霊火の ブレス ----
BREATH = [
    '.......kk.....kk......',
    '....kkkBBkk.kkCBk.....',
    '.kkkBBCCCCBkkCCCBkkk..',
    'kBBCCCwwwwCCCwwCCBBBk.',
    'kBCCwwwwwwwwwwwwCCCBBk',
    'kBBCCCwwwwCCCwwCCBBBk.',
    '.kkkBBCCCCBkkCCCBkkk..',
    '....kkkBBkk.kkCBk.....',
    '.......kk.....kk......',
]
BREATH2 = [
    '......k......k........',
    '.....kBk..k.kBk..k....',
    '..kk.kCk.kBk.kk.kBk...',
    '.kBCkkBkkkCkk..kkCk...',
    'kBCCCBBCCCCBkkBCCBk.k.',
    '.kBCkkBkkkCkk..kkCk.kBk',
    '..kk.kCk.kBk.kk.kBk..k.',
    '.....kBk..k.kBk..k.....',
    '......k......k.........',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=27, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='legHF', g='legB', x=16, y=50, rows=LEGF),
        dict(n='legFF', g='legA', x=35, y=50, rows=LEGF),
        dict(n='mane', g='mane', x=12, y=6, rows=MANE, alt={'idle1|idle3|walk1|walk3|atk2': MANE2}),
        dict(n='body', g='body', x=8, y=29, rows=BODY),
        dict(n='legH', g='legA', x=11, y=51, rows=LEG),
        dict(n='legF', g='legB', x=30, y=51, rows=LEG),
        dict(n='head', g='head', x=33, y=4, rows=HEAD, alt={'atk1|atk2': HEAD_ATK}),
        dict(n='eye', g='head', x=44, y=13, rows=EYE, alt=EYE_ALT),
        dict(n='breath', g='head', x=63, y=23, rows=BREATH, alt={'atk2': BREATH2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 0), 'mane': (0, -1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-2, 1), 'legA': (-1, 0), 'tail': (1, 0)},
    'atk1': {'root': (3, 0), 'head': (1, 1)}, 'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'mane': (0, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'mane': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
