# スナリュウ（ドラゴン・じめん × オオトカゲ）手打ち GBA風・デフォルメ（2〜3頭身：大あごの 頭は 大きく、胴は 小さく 丸く、足は 短く 太く）
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


META = dict(id='sunaryu', name='スナリュウ', types=['dragon', 'ground'], base='オオトカゲ', size='L')
PAL = {
    'k': '#101018', 'l': '#3a2418',
    'F': '#c89a62', 'G': '#8a6240', 'H': '#4e3424',      # うろこ（こげ茶）
    'S': '#fff2c4', 'D': '#ecc47e', 'E': '#c08c4a',      # 砂丘の 背（明・中・暗）
    'N': '#e8c890',                                      # 背の もよう
    'r': '#9a2a2a', 'p': '#e86a6a',                      # 口の 中・舌
    'Y': '#ffd23c', 'O': '#c8501c',                      # 目
    'w': '#ffffff', 'T': '#c8bca4',                      # きば・爪
}
LIGHT = set('FSwY')
KEEP_BLACK = set('wYOT')

# ---- 頭（見せ所＝大あご）：平たく 長い 頭、上下の 太い あごに きばが ならぶ ----
HEAD_M = [
    '......#########...............',
    '....##############............',
    '..##################..........',
    '.######################.......',
    '##########################....',
    '############################..',
    '#############################.',
    '##############################',
    '#############################.',
    '############################..',
    '##########################....',
    '##########################....',
    '##########################....',
    '##############################',
    '##############################',
    '.############################.',
    '..##########################..',
    '...#######################....',
    '.....##################.......',
]
def head(mode=''):
    m = shade(HEAD_M, {'#': 'FGH'}, 2, 2, 2)
    m = over(m, ['', '', '', '',
                 '..........................k',
                 '...H.H....................kk',  # うろこ・鼻の あな
                 '..H.H.H.',
                 '...H.H'])
    # 口：後ろは 細い 線、前へ ゆくほど 開く くさび形。上下に 太い きば（前の 2本は とくに 大きい）
    g = grid_of(m); W = len(g[0])
    up, dn = (3, 8) if mode == 'atk' else (1, 4)
    for x in range(7, W):
        f = (x - 7) / (W - 8)
        t, b_ = round(10 - up * f), round(10 + dn * f)
        for y in range(t, b_ + 1): g[y][x] = 'r' if t < y < b_ else 'k'
        if x >= W - 1:
            for y in range(t + 1, b_): g[y][x] = '.'
    for x, n in ((13, 1), (17, 1), (21, 2), (26, 3)):       # 上の きば（下向き）
        t = round(10 - up * (x - 7) / (W - 8))
        for i in range(1, n + 1):
            g[t + i][x] = 'w'
            if i < n: g[t + i][x + 1] = 'w'
    for x, n in ((15, 1), (19, 1), (24, 2)):                # 下の きば（上向き）
        b_ = round(10 + dn * (x - 7) / (W - 8))
        for i in range(1, n + 1):
            g[b_ - i][x] = 'w'
            if i < n: g[b_ - i][x - 1] = 'w'
    if mode == 'atk':
        for x in range(12, 18): g[11][x] = 'p'              # 舌
    m = rows_of(g)
    return outline(m)
HEAD = head(); HEAD_ATK = head('atk')
# するどい 目：重い まゆの ひさし＋白い 光＋金と 赤の 虹彩＋たての ひとみ＋下まぶた
EYE = ['kkkk.....', 'HkkkkkkH.', 'kwYkYYkkk', 'kYOkOOk..', '.kkkkkk..']
EYE_ALT = {'blink': ['kkkk.....', 'HkkkkkkH.', 'GGGGGGGGG', 'kkkkkkk..', '.HHHHHH..'],
           'hit': ['kkkk.....', 'HkkGGGkk.', 'GGkkkkGG.', 'HkkGGGkk.', '.HHHHHH..'],
           'atk0|atk1|atk2': ['kkkkk....', 'HkwkkkkkH', 'kwYYkYYkk', 'kYOOkOk..', '.kkkkkk..'],
           'ko': ['.........', 'HkGGGGkH.', 'GGkGGkGG.', 'GGGkkGGG.', 'GGkGGkGG.']}

# ---- 胴（小さく 丸い）＋ 背の 砂丘（なだらかな 山の 列、風もんの すじ）----
BODY = outline(over(shade(mask(30, 18, [('e', 15, 10, 14.5, 7.5, '#')]), {'#': 'FGH'}, 2, 2, 3), [
    '', '', '', '', '', '', '',
    '.....N....N.....N',
    '...N....N.....N....N',
    '',
    '..........FFFFFFF',
]))
def dunes(ph=0):
    """砂丘の 背（見せ所の 次）：大小 3つの 山。行ごとに 風もん（すじ）"""
    m = mask(34, 16, [('e', 8, 15, 7, 8, '#'), ('e', 18, 14, 8, 11, '#'), ('e', 28, 15, 6, 8, '#')])
    m = shade(m, {'#': 'SDE'}, 1, 2, 3)
    g = grid_of(m)
    for y in range(3, 16, 2):
        for x in range(34):
            if g[y][x] == 'D' and (x + y + ph) % 6 < 3: g[y][x] = 'E'
    return outline(rows_of(g))
DUNE = dunes(); DUNE2 = dunes(1)
# ---- しっぽ（太く 短く、先も 小さな 砂丘）----
TAIL = outline(over(shade(mask(22, 10, [('p', [(22, 1), (22, 9), (12, 9), (4, 7), (0, 4), (6, 4), (14, 2)], '#'), ('e', 15, 2.5, 4, 2.5, 's')]), {'#': 'FGH', 's': 'SDE'}, 1, 2, 2), [
    '', '', '', '', '.....N...N....N']))
TAIL2 = outline(over(shade(mask(22, 10, [('p', [(22, 1), (22, 9), (12, 9), (4, 8), (0, 7), (6, 5), (14, 2)], '#'), ('e', 15, 2.5, 4, 2.5, 's')]), {'#': 'FGH', 's': 'SDE'}, 1, 2, 2), [
    '', '', '', '', '', '......N...N...N']))
# ---- 足（短く 太く 横へ ふんばる、3本の 大きな 爪）----
LEG_M = ['.#####..', '######..', '.######.', '..#####.', '..######', '.########']
def leg(far=False):
    m = shade(LEG_M, {'#': 'FGH'}, 1, 1, 2)
    m = outline(m)
    m = over(m, ['', '', '', '', '', '', '', '.kTk.kTk.kTk', '.kw.k.w.k.w.', '..k...k...k'])
    r = opentop(m, 2)
    return recolor(r, {'F': 'G', 'G': 'H', 'T': 'H', 'w': 'T'}) if far else r
LEG = leg(); LEGF = leg(True)
# ---- 攻撃：砂けむりの はじけ ----
SAND = ['..k.....k...', '.kSk..kkSk..', 'kSDSkkSDDSk.', '.kDGkSDGGDSk', '..kk.kGGGDk.', '......kkkk..']
SAND2 = ['.k...k....k.', 'kSk.kSk..kSk', '.k.kSDSk..k.', '..kSDGDSk...', 'k..kDGDk..k.', 'Sk..kkk..kSk']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=1, y=40, rows=TAIL, alt={'idle1|idle3|walk1|walk3': TAIL2}),
        dict(n='hlegF', g='legB', x=23, y=49, rows=LEGF),
        dict(n='flegF', g='legA', x=41, y=49, rows=LEGF),
        dict(n='dune', g='body', x=9, y=23, rows=DUNE, alt={'idle1|idle3|walk1|walk3': DUNE2}),
        dict(n='body', g='body', x=14, y=34, rows=BODY),
        dict(n='hleg', g='legA', x=16, y=50, rows=LEG),
        dict(n='fleg', g='legB', x=35, y=50, rows=LEG),
        dict(n='head', g='head', x=34, y=19, rows=HEAD, alt={NB: HEAD_ATK}),
        dict(n='eye', g='head', x=40, y=21, rows=EYE, alt=EYE_ALT),
        dict(n='sand', g='head', x=52, y=46, rows=SAND, alt={'atk2': SAND2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-2, -1), 'legA': (-1, 0), 'tail': (1, 0)},
    'atk1': {'root': (3, 0), 'head': (1, 0)}, 'atk2': {'root': (4, 0), 'head': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)}, 'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
