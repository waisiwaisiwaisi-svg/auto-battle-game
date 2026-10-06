# フブキオオカミ（こおり・ゴースト × オオカミ）手打ち GBA風・デフォルメ（2〜3頭身：頭と 氷の 牙は 大きく、胴は 小さく、足は 短く 太く）
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


META = dict(id='fubukiookami', name='フブキオオカミ', types=['ice', 'ghost'], base='オオカミ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c2650',
    'W': '#f2f8ff', 'V': '#a8c4e8', 'U': '#5a72a8', 'N': '#34407a',   # 毛皮（白〜青）
    'c': '#e0fcff', 'C': '#7ee0ff', 'B': '#2f8cc8',                    # 氷
    'P': '#9a7ae0',                                                    # 霊気（吹雪の 中の むらさき）
    'r': '#7a1e3a', 'w': '#ffffff',
}
LIGHT = set('Wcw')
KEEP_BLACK = set('wcCB')

# ---- 頭（大きく、耳は とがり、鼻づらは 長い。ほおの 毛は 後ろへ 流れる）----
HEAD_M = [
    '.....#.....#.................',
    '.....##...##.................',
    '....###..###.................',
    '....####.####................',
    '....##########...............',
    '...#############.............',
    '..################...........',
    '.###################.........',
    '######################.......',
    '#########################....',
    '###########################..',
    '############################.',
    '############################.',
    '.##########################..',
    '##########################...',
    '#######################......',
    '.######################......',
    '###########.#########........',
    '.####.####...........',
    '..##..##.............',
]
def zone(rows, fn, ch='o'):
    """毛の 色わけ：fn(x, y) が 真の ところを 明るい 毛（o）に"""
    return [''.join(ch if c == '#' and fn(x, y) else c for x, c in enumerate(r)) for y, r in enumerate(rows)]
DFUR = 'VUN'; LFUR = 'WWV'
def head(mode=''):
    m = shade(zone(HEAD_M, lambda x, y: y * 2 + x * .7 > 21), {'#': DFUR, 'o': LFUR}, 2, 2, 2)
    m = over(m, [
        '.....V.....V',
        '.....UV....UV',
        '.....UU....UU',
        '',
        '',
        '',
        '',
        '',
        '.U.......................',
        '..UU......................kk',
        '....U.....................kk',
        '..UU.......................k',
        '.U.UU',
        '...U',
        '..U.U',
        '...U',
    ])
    if mode == 'atk':   # 大口を 開く
        m = over(m, [''] * 13 + [
            '..............kkkkkkkkkkkkkk',
            '.............krrrrrrrrrrrrk.',
            '............krrrrrrrrrrrrk..',
            '............krrrrrrrrrrk....',
            '.............kwkwrrrkwk.....',
            '..............kkkkkkkk......',
        ])
    else:
        m = over(m, [''] * 14 + ['.............kkkkkkkkkkkkk', '..............kwkUUUUkwk'])
    return outline(m)
HEAD = head(); HEAD_ATK = head('atk')
# 氷の 牙（見せ所）：上あごから 下へ 大きく はみ出す 2本の 結晶
FANG = ['kkkkkk.kkkk', 'kccCBk.kcBk', 'kcCCBk.kcBk', '.kcCBk.kCBk', '.kcCBk..kk.', '..kCBk.....', '..kCk......', '...k.......']
FANG_ATK = ['kkkkk..kkkk', 'kcCBk..kcBk', '.kcBk..kCBk', '.kCk....kk.', '..k........']
# するどい 目：まゆ＋白い 光＋氷色の 虹彩 2色＋たての ひとみ＋下まぶた
EYE = ['kkk.....', 'UkkkkkU.', 'kwCkCkkk', 'kCBkBBk.', '.kkkkk..']
EYE_ALT = {'blink': ['kkk.....', 'UkkkkkU.', 'VVVVVVVV', 'kkkkkkk.', '.UUUUU..'],
           'hit': ['kkk.....', 'UkkVVkk.', 'VVkkkVV.', 'UkkVVkk.', '.UUUUU..'],
           'atk0|atk1|atk2': ['kkkk....', 'UkwkkkkU', 'kwccCkCk', 'kCCBkBk.', '.kkkkk..'],
           'ko': ['........', 'UkVVVkU.', 'VVkVkVV.', 'VVVkVVV.', 'VVkVkVV.']}

# ---- 胴（小さく 丸い。毛並みは 横に 流れる 筋）----
BODY = outline(over(shade(zone(mask(30, 18, [('e', 15, 9, 14.5, 8.5, '#')]), lambda x, y: y > 8 + (x < 8)), {'#': DFUR, 'o': LFUR}, 2, 2, 3), [
    '', '', '',
    '.....UUUU......UUU',
    '...........UUUU',
    '..UUU......',
    '........UUUUU....UU',
    '.....UUU.......UUU',
    '..UU......UUUU',
    '..........',
]))
# ---- 首の ふさ毛（頭と 胴を つなぐ。毛先は 後ろ下へ 流れる）----
RUFF = outline(shade(mask(16, 14, [('p', [(4, 0), (15, 0), (16, 10), (12, 13), (10, 9), (7, 12), (6, 8), (2, 10), (3, 5), (0, 6)], '#')]), {'#': 'WVU'}, 2, 2, 2))
# ---- 吹雪に 溶ける 後ろ半身：横に 流れる 雪の 筋（根もとは 胴に 食いこむ）----
STORM_M = [
    '..............###########.',
    '......##################..',
    '.............############.',
    '#########################.',
    '.....####################.',
    '...........##############.',
    '..#######################.',
    '.........###############..',
    '................#######...',
]
def storm(ph=0):
    """ふさふさの しっぽ が 後ろへ 流れ、先が 吹雪の 筋に ほどける"""
    m = [(r[7:] + '..') if ph and j % 2 == 0 else r[5:] for j, r in enumerate(STORM_M)]
    m = shade(zone(m, lambda x, y: y >= 4), {'#': DFUR, 'o': LFUR}, 1, 1, 0)
    m = over(m, ['', '', '', 'PP', '', '', '.PP'])
    return outline(m)
STORM = storm(); STORM2 = storm(1)
FLAKES = ['k......k....', '......kck...', '.......k.k..', '.........kck', '..k.......k.', '.kck........', '..k.....k...', '........kck.', '.........k..']
FLAKES2 = ['....k.......', '...kck....k.', '....k....kck', '..........k.', '.k..........', 'kck....k....', '.k....kck...', '.......k....', '............']

# ---- 足（短く 太い、白い 爪）----
LEG_M = ['######', '######', '######', '.#####', '.#####', '.#####', '######', '#######']
def leg(far=False):
    m = over(shade(LEG_M, {'#': 'WVU'}, 1, 1, 2), ['', '', '', '', '', '', '', 'w.w.w'])
    r = opentop(outline(m), 2)
    return recolor(r, {'W': 'V', 'V': 'U', 'U': 'N'}) if far else r
LEG = leg(); LEGF = leg(True)
# 後ろ足：吹雪に 半分 溶けた 足（上が 霊気の むらさき）
HLEG = opentop(outline(over(shade(LEG_M, {'#': 'VUN'}, 1, 1, 2), ['.P.P.', 'P.P.P', '.P.P', '', '', '', '', 'w.w.w'])), 2)

# ---- 攻撃：氷の かみつき（はじける 氷片）----
BITE = ['...k....k...', '..kck..kck..', '.kcCBkkcCBk.', 'kcCBBBBBCBBk', '.kBBkkkkBBk.', '..kk....kk..']
BITE2 = ['k...k..k...k', 'ck.kck.kck.k', '.kcCBkkcCBk.', '..kBBkkBBk..', '.kck....kck.', '..k......k..']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='flakes', g='storm', x=5, y=27, rows=FLAKES, alt={'idle1|idle3|walk1|walk3|atk2': FLAKES2}, not_='ko'),
        dict(n='hlegF', g='legB', x=20, y=51, rows=recolor(HLEG, {'V': 'U', 'U': 'N'})),
        dict(n='flegF', g='legA', x=38, y=51, rows=LEGF),
        dict(n='storm', g='storm', x=5, y=34, rows=STORM, alt={'idle1|idle3|walk1|walk3|atk2': STORM2}),
        dict(n='body', g='body', x=14, y=34, rows=BODY),
        dict(n='ruff', g='body', x=32, y=28, rows=RUFF),
        dict(n='hleg', g='legA', x=16, y=52, rows=HLEG),
        dict(n='fleg', g='legB', x=34, y=52, rows=LEG),
        dict(n='head', g='head', x=31, y=15, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=43, y=23, rows=EYE, alt=EYE_ALT),
        dict(n='fang', g='head', x=47, y=30, rows=FANG, alt={NB: FANG_ATK}),
        dict(n='bite', g='head', x=58, y=32, rows=BITE, alt={'atk2': BITE2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'storm': (-1, 0)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'legA': (-1, 0), 'storm': (-1, 0)},
    'atk1': {'root': (4, 0), 'head': (1, 1)}, 'atk2': {'root': (5, 0), 'head': (1, 1), 'storm': (-2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'storm': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
