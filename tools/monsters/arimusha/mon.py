# アリムシャ（むし・かくとう × アリ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と こぶしの 大あご、胴と 腹は 小さく、2本足で 立つ）
META = dict(id='arimusha', name='アリムシャ', types=['bug', 'fighting'], base='アリ', size='M')
PAL = {
    'k': '#101018', 'l': '#3c1418',
    'C': '#e47c4c', 'D': '#a83a2a', 'E': '#58181e',      # 赤アリの 殻
    'F': '#ffe4a4', 'G': '#d69a50', 'H': '#80502c',      # 大あご（こぶし）・前立て
    'Y': '#dcff6c', 'Z': '#62a42a',                      # 目（明・暗）
    'V': '#b4bccc', 'w': '#ffffff',                      # さらし（包帯）
}
LIGHT = set('CFYw')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
    return g
def shade(g, ramps, lw=2, dw=2):
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, c):
        n = 1
        while 0 <= y + dy * n < H and 0 <= x + dx * n < W and src[y + dy * n][x + dx * n] == c: n += 1
        return n
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c not in ramps: continue
            hi, mid, lo = ramps[c]
            if run(y, x, 1, 0, c) <= dw or run(y, x, 0, 1, c) <= dw: g[y][x] = lo
            elif run(y, x, -1, 0, c) <= lw or run(y, x, 0, -1, c) <= 1: g[y][x] = hi
            else: g[y][x] = mid
    return g
def P(g, ramps, over=(), lw=2, dw=2, ol=True):
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def opentop(rows, n=1):
    """体に かさなる 付け根：上の 輪郭を 消して 体の 色と なじませる"""
    return ['.' * len(r) if i < n else r for i, r in enumerate(rows)]
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '..' + '.' * 6, '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
SHELL = {'1': 'CDE'}; FIST = {'1': 'FGH'}
DK = {'C': 'D', 'D': 'E', 'E': 'l', 'F': 'G', 'G': 'H', 'H': 'l', 'w': 'V', 'V': 'D'}
def openleft(rows, ys):
    return [('.' + r[1:]) if i in ys and r[:1] == 'k' else r for i, r in enumerate(rows)]

# ---- 頭（大きく 丸い）：かぶとの ような 殻、額に 金の 前立て、目の 上に かぶとの ひさし ----
HEAD = P(M(24, 21, ('e', '1', 12, 10, 12, 10), ('e', '1', 15, 14, 9, 7)), SHELL, [
    (['..CCCC', '.C', 'C'], 3, 2),                        # 光の 三日月
    (['EEEEEEEEEEEEEE', '..CCCCCCCCCCCCC'], 1, 7),         # かぶとの ひさしの さかい
    (['......EE', '....EE', '..EE', 'EE'], 1, 14),          # ほおの 殻の さかい
    (['GG.....', '.FGG...', '..FFGG.', '....FF'], 15, 0),   # 前立て（三日月の 金具）
], lw=2, dw=3)
EYE, EYE_ALT = eye('Y', 'Z')
MOUTH = ['kkkkk', 'kwkwk', '.k.k.']                             # 口の 牙

# ---- 触角：くの字に 折れて 後ろへ（かぶとの 角飾り）、先は こぶ ----
ANT = [
    '.kkk.........',
    'kCCDk........',
    'kDDDEkk......',
    '.kkkCDDkk....',
    '....kkCDDk...',
    '......kCDk...',
    '......kCDk...',
    '.......kCDk..',
    '........kCDk.',
    '.........kCDk',
    '..........kkk',
]
ANT2 = ['.........', '.kkk.........', 'kCCDk........', 'kDDDEkkk.....', '.kkkkCDDk....'] + ANT[5:]

# ---- 大あご ＝ こぶし（見せ所）：口から 生えた 太い あごの 先が にぎりこぶし（指の 節が 横に 並ぶ）----
FIST = [
    '..........kkkkkkkk......',
    '........kkFFFFFFFFkk....',
    '.......kFFFGGGGkFFFGk...',
    '......kFFGGGGGGkGGGGGHk.',
    'kkkkkkFGGGGGGGkkkkkkkkkk',
    'FFFFFFGGGGGGGkFFFFFFGGwk',
    'GGGGGGGGGGGGkFGGGGGGHHHk',
    'GGGGGGGGGGGkkkkkkkkkkkkk',
    'HHHHHHGGGGGkFFFFFFGGGwk.',
    'kkkkkkHGGGGkGGGGGGHHHHk.',
    '......kHGGGkkkkkkkkkkkk.',
    '......kHHGGkFFFFFGGHHk..',
    '.......kHHHkGGGGHHHHk...',
    '........kkkkkkkkkkkk....',
]
FIST_N = FIST; FIST_F = dark(FIST, DK)

# ---- 胴（たてに 立つ 胸）と 腹（後ろ下へ たれる だ円、節の すじ）----
THORAX = P(M(13, 16, ('e', '1', 6.5, 8, 6.5, 8)), SHELL, [(['CC', 'C', 'C'], 3, 2), (['EEE'], 5, 9)], lw=2, dw=3)
GASTER = P(M(20, 15, ('e', '1', 10, 7.5, 10, 7.5)), SHELL, [
    (['.E', 'E.', 'E.', 'E.', 'E.', '.E'], 8, 4),
    (['.E', 'E.', 'E.', 'E.', 'E.', '.E'], 13, 4),
    (['CC', 'C'], 3, 3),
], lw=2, dw=3)

# ---- 足（2本だけ）：短く 太く、すねに さらし ----
LEG = [
    '..kkkkkk..',
    '.kCCCDDDk.',
    'kCCCDDDEk.',
    'kCCDDDEEk.',
    '.kwwwVVk..',
    '.kVwwwVk..',
    '.kwwVVwk..',
    '.kCCDDEk..',
    'kCCCDDDEkk',
    'kCDDDDDDEk',
    'kwkkwkkwkk',
]
LEG_N = opentop(LEG); LEG_F = dark(LEG, DK)

POW = [
    '...k...k...',
    '..kFk.kFk..',
    'kk.kFkFk.kk',
    'kFkkFwFkkFk',
    '.kFFwwwFFk.',
    'kFkkFwFkkFk',
    'kk.kFkFk.kk',
    '..kFk.kFk..',
    '...k...k...',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='ant2', g='ant', x=21, y=8, rows=dark(ANT, DK), alt={'idle1|idle3|walk1|walk3': dark(ANT2, DK)}),
        dict(n='legF', g='legB', x=23, y=50, rows=LEG_F),
        dict(n='gaster', g='gaster', x=8, y=37, rows=GASTER),
        dict(n='fistF', g='fistF', x=38, y=19, rows=FIST_F),
        dict(n='thorax', g='body', x=24, y=34, rows=THORAX),
        dict(n='legN', g='legA', x=29, y=50, rows=LEG_N),
        dict(n='ant', g='ant', x=26, y=6, rows=ANT, alt={'idle1|idle3|walk1|walk3': ANT2}),
        dict(n='head', g='head', x=24, y=15, rows=HEAD),
        dict(n='eye', g='head', x=36, y=24, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=42, y=30, rows=MOUTH),
        dict(n='fistN', g='fistN', x=36, y=29, rows=FIST_N),
        dict(n='pow', g='fistN', x=60, y=31, rows=POW, only='atk1'),
        dict(n='pow2', g='fistF', x=62, y=21, rows=POW, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'fistN': (0, -1)}, 'idle3': {'fistF': (0, -1)}, 'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'fistN': (1, 0)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'body': (0, -1)}, 'walk3': {'fistF': (1, 0)},
    'atk0': {'body': (-2, 1), 'fistN': (-2, 0), 'fistF': (-2, 0), 'gaster': (1, -1)},
    'atk1': {'root': (3, 0), 'fistN': (3, 0), 'fistF': (-2, 0)}, 'atk2': {'root': (4, 0), 'fistF': (3, 2), 'fistN': (-1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'fistN': (-1, 1), 'fistF': (-1, 0)}, 'ko': {'_flip': True},
}
PARENT = {'ant': 'head', 'fistN': 'head', 'fistF': 'head', 'head': 'body', 'gaster': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
