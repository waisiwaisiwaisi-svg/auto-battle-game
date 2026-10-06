# シダレユウ（ゴースト・くさ × 柳）手打ち GBA風・デフォルメ（2〜3頭身：垂れ髪の 頭は 大きく、幹の 胴は 小さく、根の 足は 短く 太く）
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


META = dict(id='shidareyuu', name='シダレユウ', types=['ghost', 'grass'], base='柳', size='M')
EYE_BOX = (38, 23, 9, 6)
PAL = {
    'k': '#101018', 'l': '#1a3028',
    'E': '#b6eea0', 'F': '#5cb46c', 'D': '#2a664a',      # 柳の 葉（垂れ髪）
    'V': '#dfe8f4', 'U': '#8a9cc0',                      # 幽霊の 顔（青白い）
    'H': '#a88462', 'G': '#6c4c38', 'J': '#3e2a24',      # 幹・根
    'Y': '#f6ff8a', 'O': '#34d07a',                      # 光る 目（黄みどり）
    'r': '#8a1c2a', 'X': '#0c0a14',                      # 黒い 強膜
    'w': '#ffffff',
}
LIGHT = set('EVHYw')
KEEP_BLACK = set('wYOrX')

# ---- 頭：柳の かんむり（丸い ドーム）から 背中へ 垂れる 髪の 束を 1つの かたまりで 描く。前がみの 葉先が 顔に かかる ----
def hairmass(ph=0):
    s = ph
    m = mask(44, 50, [('e', 24, 8, 19, 8, '#'),
                      ('p', [(3, 8), (26, 6), (26, 26), (25, 36 + s), (23, 30), (21, 42 - s), (19, 32), (17, 46 + s), (15, 33), (13, 41 - s), (11, 31), (9, 45 + s), (7, 32), (5, 39 - s), (3, 30), (1, 35 + s), (1, 20)], '#')]
             + [('p', [(x - 2.5, 10), (x + 2.5, 10), (x + s, 17 + (34 - x) // 4)], '#') for x in (26, 30, 34)])
    g = grid_of(shade(m, {'#': 'EFD'}, 2, 2, 2))
    # 垂れる 筋（見せ所の 質感）：3ドットおきに 暗い 線、その 左に 明るい 葉の 点
    for x in range(3, 44, 3):
        for y in range(3, 50):
            if g[y][x] in 'EF' and (y + x) % 7: g[y][x] = 'D' if g[y][x] == 'F' else 'F'
            if g[y][x - 1] == 'F' and (y + x) % 5 == 0: g[y][x - 1] = 'E'
    return outline(rows_of(g))
def bangs(rows):
    """顔の 上に かぶさる ぶぶん（右上）だけ 切りだす"""
    return [''.join(c if (i >= 26 and j <= 21) else '.' for i, c in enumerate(r)) for j, r in enumerate(rows)]
HAIR = hairmass(); HAIR2 = hairmass(1)
BANG = bangs(HAIR); BANG2 = bangs(HAIR2)
FACE = shade(mask(16, 17, [('e', 8, 8.5, 8, 8.5, '#')]), {'#': 'VVU'}, 1, 2, 3)
def face(mode=''):
    f = over(FACE, ['', '', '', '', '',
                    '.......UUUUUUU',
                    '', '', '', '',
                    '........UUUUUU', '', '',
                    '......U'])
    if mode == 'atk':      # 口が 耳まで さける
        f = over(f, [''] * 10 + ['...kkkkkkkkkkkk', '..kwkwkrrrkwkwk', '..krrrrrrrrrrk', '...kwkwrrrkwk', '....kkkkkkkkk'])
    else:                  # にたりと 笑う 口と きば
        f = over(f, [''] * 11 + ['.....kkkkkkkkk', '....kkwkrrrkwk', '......kk.kk.k'])
    return outline(f)
def lock(ph=0):   # 顔の 左に かかる 前がみの 束
    m = mask(6, 22, [('p', [(0, 0), (6, 0), (5, 9), (4, 15 + ph), (3, 21 + ph), (1, 14), (0, 8)], '#')])
    return outline(shade(m, {'#': 'EFD'}, 1, 1, 2))

FRONT = lock(); FRONT2 = lock(1)

# 黒い 強膜（F）：白目の かわりに 真っ黒な 目。中に 白い 光点 1つと みどりの にじみ。下まぶたは 赤く ただれる
EYE = ['kk.......',
       'UkkkkU...',
       'kXXXXkkk.',
       'kXXwOXXXk',
       '.kXOXXXk.',
       '..rkkkr..']
EYE_ALT = {'blink': ['kk.......', 'UkkkkU...', 'VVVVVkkk.', 'kkkkkkkkk', '.UrrrrrU.'],
           'hit': ['kk.......', 'UkkkU....', 'VkXXkkk..', 'VVkXwXXk.', 'VkXXkkk..', '.UkkU....'],       # ぎゅっと しぼむ、光点が ぶれる
           'atk0|atk1|atk2': ['kkk......', 'UkkkkkU..', 'kXXOXXkkk', 'kXOwwOXXk', '.kXOYXXk.', '..rkkkr..'],   # 光点が ふくらむ
           'ko': ['.........', '.kU..Uk..', '..kUUk...', '...kk....', '..kUUk...', '.kU..Uk..']}

# ---- 胴：短い ねじれた 幹（樹皮の すじ）----
TRUNK = outline(over(shade(mask(16, 20, [('e', 8, 9, 7.5, 9, '#'), ('r', 2, 12, 14, 20, '#')]), {'#': 'HGJ'}, 2, 2, 3), [
    '', '', '', '',
    '.....G...J',
    '....G...J',
    '....G..J.....J',
    '...G...J....J',
    '...G..J.....J',
    '....G.J....J',
    '....G..J...J',
    '.....G.J..J',
]))
# ---- 根の 足（短く 太い、3本の 根の 指）----
ROOT_M = ['#######.', '#######.', '.######.', '.#######', '##########', '#.#.##.##', '#..#..#..']
def root(far=False):
    r = opentop(outline(shade(ROOT_M, {'#': 'HGJ'}, 1, 1, 2)), 2)
    return recolor(r, {'H': 'G', 'G': 'J'}) if far else r
ROOT = root(); ROOTF = root(True)
# ---- 腕：枝の 腕と 垂れ枝の 爪（3本の 長い 爪）----
ARM_M = [
    '#####.........',
    '########......',
    '.#########....',
    '...#########..',
    '......######..',
    '.......#####..',
    '.......######.',
    '.......#.#..#.',
    '......#..#..#.',
    '......#..#...#',
    '.....#...#...#',
    '.....#....#...',
]
def arm(far=False, reach=False):
    m = [r for r in ARM_M]
    if reach:   # 前へ つき出して 爪を ひらく
        m = ['####.................', '############.........', '.##################..', '....################.', '.............#######.',
             '.............#.#..#.#.', '.............#..#..#..#', '............#...#...#..#', '............#....#...#..']
    r = outline(shade(m, {'#': 'HGJ'}, 1, 1, 2))
    return recolor(r, {'H': 'G', 'G': 'J'}) if far else r
ARM = arm(); ARMF = arm(True); ARM_R = arm(False, True)
# ---- 攻撃：葉の 爪の ひっかき ----
SLASH = ['.......kk.kk', '.....kkEkkEk', '...kkEEkkEEk', '.kkEFkkEFkk.', 'kEFkkEFkk...', 'kFk.kFk.....', '.k...k......']
SLASH2 = ['........k..k', '......kkEkkEk', '....kkEwkkEwk', '..kkEwkkEwkk.', '.kEwkkEwkk...', 'kEFk.kFk.....', 'kFk..kk......', '.k...........']
WISP = ['..k..', '.kOk.', 'kOYOk', 'kYwYk', 'kOYOk', '.kkk.']   # 漂う 霊火（はなれているのは 意図的）

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='hair', g='hair', x=3, y=5, rows=HAIR, alt={'idle1|idle3|walk1|walk3|hit': HAIR2}),
        dict(n='rootF', g='legB', x=31, y=51, rows=ROOTF),
        dict(n='armF', g='armF', x=16, y=36, rows=pix.flip_h(ARMF)),
        dict(n='trunk', g='body', x=23, y=33, rows=TRUNK),
        dict(n='root', g='legA', x=21, y=52, rows=ROOT),
        dict(n='face', g='head', x=31, y=18, rows=face(), alt={NB: face('atk')}),
        dict(n='eye', g='head', x=38, y=23, rows=EYE, alt=EYE_ALT),
        dict(n='front', g='hair', x=29, y=17, rows=FRONT, alt={'idle1|idle3|walk1|walk3|hit': FRONT2}),
        dict(n='bang', g='hair', x=3, y=5, rows=BANG, alt={'idle1|idle3|walk1|walk3|hit': BANG2}),
        dict(n='arm', g='arm', x=33, y=36, rows=ARM, not_=NB),
        dict(n='armR', g='arm', x=33, y=37, rows=ARM_R, only=NB),
        dict(n='slash', g='arm', x=56, y=38, rows=SLASH, alt={'atk2': SLASH2}, only=NB),
        dict(n='wisp', g='wisp', x=2, y=9, rows=WISP, not_='ko'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'hair': (0, 1), 'wisp': (0, -1)}, 'idle2': {'head': (0, 1), 'hair': (0, 1), 'wisp': (0, -2)}, 'idle3': {'head': (0, 1), 'wisp': (0, -1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'wisp': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'body': (0, 0), 'wisp': (0, 1)},
    'atk0': {'body': (-2, 1), 'arm': (-2, -1), 'hair': (-1, 0)}, 'atk1': {'root': (3, 0), 'arm': (1, 0)}, 'atk2': {'root': (4, 0), 'arm': (2, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'arm': (-1, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'hair': 'head', 'arm': 'body', 'armF': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'wisp': 'root'}
