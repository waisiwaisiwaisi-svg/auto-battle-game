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
        elif s[0] == 't':   # 太い 線（関節で 曲がる 足など）
            for (ax, ay), (bx, by) in zip(s[1], s[1][1:]):
                for i in range(17):
                    t = i / 16; cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
                    for yy in range(H):
                        for xx in range(W):
                            if (xx + .5 - cx) ** 2 + (yy + .5 - cy) ** 2 <= s[2] ** 2: g[yy][xx] = s[3]
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
EYE_BOX = (42, 20, 9, 6)
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
# 三白眼（C）：白目が 多く、小さな 氷色の 瞳が 前上に 寄って にらむ。下まぶたの 線が 太く 濃い
EYE = ['kkk......',
       'UkkkkkkkU',
       'kwwwCCwwk',
       'kwwwBkwk.',
       '.kwwwwk..',
       '.Nkkkkk..']
EYE_ALT = {'blink': ['kkk......', 'UkkkkkkkU', 'VVVVVVVVk', 'kkkkkkkk.', '.UNNNNk..', '.........'],
           'hit': ['kkk......', 'Ukkkk....', 'VVkwkkk..', 'VVVkwwBk.', 'VVkwkkk..', '.Ukkk....'],   # 白目が つぶれ、瞳が 下に はずれる
           'atk0|atk1|atk2': ['kkkk.....', 'UkkkkkkkU', 'kwwwwCBwk', 'kwwwwBkwk', '.kwwwwwk.', '.Nkkkkk..'],   # 見開いて 瞳が さらに 小さく 前へ
           'ko': ['.........', 'UkVVVkU..', 'VVkVkVV..', 'VVVkVVV..', 'VVkVkVV..', '.........']}

# ---- 胴＋しっぽ（ひとつながり）：胸は 深く 前が 高い、腹は 引きしまり、腰から 先は 細く なって 吹雪の しっぽに ほどける ----
def body(ph=0):
    d = 1 if ph else 0
    m = mask(44, 26, [('p', [(44, 9), (44, 17), (41, 23), (34, 23), (27, 20), (20, 19), (15, 17), (10, 17), (5, 17 + d), (0, 19 + d), (5, 13), (0, 12 - d), (6, 10), (1, 5 - d), (8, 7), (4, 0 + d), (11, 4), (15, 7), (20, 6), (30, 4), (38, 3)], '#')])
    m = shade(zone(m, lambda x, y: y > 15 - (x > 33) * 4 + (x < 22) * 9), {'#': DFUR, 'o': LFUR}, 2, 2, 2)
    m = over(m, [
        '', '', '', '', '',
        '......P',
        '.....W.......',
        '..PPP....WW.......UUUU......UUU',
        '.......WW...............UUUU',
        '...WWW.........UUU......',
        '.........PP..........UUUUU',
        '..PPPP..WW.......UUU.......',
        '.......PPP',
        '...WW.......',
        '.....PPP',
    ])
    return outline(m)
BODY = body(); BODY2 = body(1)
# ---- 首の ふさ毛（頭と 胴を つなぐ。毛先は 後ろ下へ 流れる）----
RUFF = outline(shade(mask(16, 14, [('p', [(4, 0), (15, 0), (16, 10), (12, 13), (10, 9), (7, 12), (6, 8), (2, 10), (3, 5), (0, 6)], '#')]), {'#': 'WVU'}, 2, 2, 2))
# ---- 吹雪に 溶ける 後ろ半身：横に 流れる 雪の 筋（根もとは 胴に 食いこむ）----
def storm(ph=0):
    """ふさふさの しっぽが 腰から 後ろ上へ のび、先は 横に 流れる 吹雪の 筋に ほどける"""
    d = 1 if ph else 0
    m = mask(22, 16, [
        ('p', [(22, 9), (17, 4), (11, 2), (6, 3 + d), (2, 1), (5, 6), (0, 7 + d), (7, 9), (2, 11 - d), (9, 12), (16, 14), (22, 15)], '#'),
    ])
    m = shade(zone(m, lambda x, y: y >= 10), {'#': DFUR, 'o': LFUR}, 1, 1, 0)
    m = over(m, ['', '', '', '......PPP', '...PP', '', '.....PPPP', '', '...PPP'])
    return outline(m)
STORM = storm(); STORM2 = storm(1)
FLAKES = ['k......k....', '......kck...', '.......k.k..', '.........kck', '..k.......k.', '.kck........', '..k.....k...', '........kck.', '.........k..']
FLAKES2 = ['....k.......', '...kck....k.', '....k....kck', '..........k.', '.k..........', 'kck....k....', '.k....kck...', '.......k....', '............']

# ---- 足（短く 太いが ちゃんと 曲がる）：前足＝ひじ → 手首 → 前を 向く 足先、後ろ足＝太もも → 後ろへ 曲がる かかと → 足先 ----
def fleg(far=False):
    m = mask(12, 15, [('t', [(3.5, 1), (5, 6), (5.5, 10)], 2.4, '#'), ('e', 7.5, 12, 4, 2.6, '#')])
    m = over(shade(m, {'#': 'WVU'}, 1, 1, 2), ['', '', '', '', '', '', '', '', '', '', '', '', '', '....w.w.w'])
    m = over(m, ['', '', '', '', '', '', '', '', '', '...U'])          # 手首の くびれ
    r = opentop(outline(m), 3)
    return recolor(r, {'W': 'V', 'V': 'U', 'U': 'N'}) if far else r
def hleg(far=False):
    m = mask(13, 16, [('e', 7, 4.5, 5.5, 4.5, '#'), ('t', [(6, 7), (3, 10.5)], 2.3, '#'), ('t', [(3, 10.5), (4.5, 13)], 1.8, '#'), ('e', 6.5, 13.5, 3.8, 2.2, '#')])
    m = over(shade(m, {'#': 'VUN'}, 1, 1, 2), ['', '', '..PP', '.P', '', '', '', '', '', '', '', '', '', '', '', '....w.w.w'])
    r = opentop(outline(m), 4)
    return recolor(r, {'V': 'U', 'U': 'N', 'W': 'V'}) if far else r
LEG = fleg(); LEGF = fleg(True); HLEG = hleg(); HLEGF = hleg(True)

# ---- 攻撃：氷の かみつき（はじける 氷片）----
BITE = ['...k....k...', '..kck..kck..', '.kcCBkkcCBk.', 'kcCBBBBBCBBk', '.kBBkkkkBBk.', '..kk....kk..']
BITE2 = ['k...k..k...k', 'ck.kck.kck.k', '.kcCBkkcCBk.', '..kBBkkBBk..', '.kck....kck.', '..k......k..']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='flakes', g='storm', x=1, y=17, rows=FLAKES, alt={'idle1|idle3|walk1|walk3|atk2': FLAKES2}, not_='ko'),
        dict(n='hlegF', g='legB', x=19, y=44, rows=HLEGF),
        dict(n='flegF', g='legA', x=37, y=46, rows=LEGF),
        dict(n='body', g='body', x=0, y=25, rows=BODY, alt={'idle1|idle3|walk1|walk3|atk2': BODY2}),
        dict(n='ruff', g='body', x=31, y=27, rows=RUFF),
        dict(n='hleg', g='legA', x=15, y=44, rows=HLEG),
        dict(n='fleg', g='legB', x=33, y=46, rows=LEG),
        dict(n='head', g='head', x=31, y=13, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=42, y=20, rows=EYE, alt=EYE_ALT),
        dict(n='fang', g='head', x=47, y=28, rows=FANG, alt={NB: FANG_ATK}),
        dict(n='bite', g='head', x=58, y=30, rows=BITE, alt={'atk2': BITE2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'legA': (-1, 0)},
    'atk1': {'root': (4, 0), 'head': (1, 1)}, 'atk2': {'root': (5, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'storm': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
