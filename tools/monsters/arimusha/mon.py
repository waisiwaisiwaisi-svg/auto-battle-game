# アリムシャ（むし・かくとう × アリ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭＋こぶしの 大あご、細い くびれで 胸・腹に わかれ、2本足で 立つ）
META = dict(id='arimusha', name='アリムシャ', types=['bug', 'fighting'], base='アリ', size='M')
EYE_BOX = (34, 19, 8, 6)
PAL = {
    'k': '#101018', 'l': '#3c1418',
    'C': '#e47c4c', 'D': '#a83a2a', 'E': '#58181e',      # 赤アリの 殻
    'F': '#ffe4a4', 'G': '#d69a50', 'H': '#80502c',      # 大あご（こぶし）・前立て
    'Y': '#b4c4ec', 'Z': '#3c4058', 'X': '#141420',     # 目（黒い 複眼：光の 帯・あみ目・地）
    'V': '#b4bccc', 'w': '#ffffff',                      # さらし（包帯）
}
LIGHT = set('CFYw')
KEEP_BLACK = set('wYZX')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角 / ('t',ch,r,[(x,y),...]) 太い 線。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
        elif s[0] == 't':
            r, pts = s[2], s[3]
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                n = int(max(abs(bx - ax), abs(by - ay)) * 2) + 1
                for i in range(n + 1):
                    t = i / n; pix.ellipse(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, r, s[1]) if False else _disc(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, s[1])
    return g
def _disc(g, cx, cy, r, ch):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= y < len(g) and 0 <= x < len(g[0]) and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: g[y][x] = ch
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
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭（輪郭の ぶん 左上へ 1 ずれる）"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '........', '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
SHELL = {'1': 'CDE'}; GOLD = {'1': 'FGH'}
DK = {'C': 'D', 'D': 'E', 'E': 'l', 'F': 'G', 'G': 'H', 'H': 'l', 'w': 'V', 'V': 'D'}

# ---- 頭（大きく、アリらしい 角ばった ハート形）：ほおが ふくらみ、額に 金の 前立て ----
HEAD = P(M(23, 20, ('e', '1', 11.5, 9, 11.5, 9), ('r', '1', 3, 9, 20, 15), ('e', '1', 12, 15, 9, 5)), SHELL, [
    (['..CCCC', '.CC', 'C'], 3, 1),
    (['......EE', '....EE', '..EE'], 2, 14),                # ほおの さかい
    (['EEEEE'], 13, 18),                                     # あごの 下
], lw=2, dw=3)
CREST = ['kk......', 'kFkk....', '.kFGkk..', '..kFGGk.', '...kGGHk', '....kkk.']
# 目（D 複眼）：黒い だ円の ドーム。あみ目の 点（Z）と 左上から ななめに 走る 光の 帯（Y・w）。ひとみは ない。
# 上を かぶとの ひさし（まゆ）が 前へ 下がって 切る
EYE = ['.kkkkkk.', 'kXwXXZXk', 'kZXwXXXk', 'kXXZYXZk', 'kXZXXYXk', '.kXXZXk.']
EYE_ALT = {
    'blink': ['.kkkkkk.', 'kEEEEEEk', 'kkkkkkkk', 'kXXZYXZk', 'kXZXXYXk', '.kXXZXk.'],     # まゆ（ひさし）が 下がる
    'hit': ['.kkkkkk.', 'kXwXkZXk', 'kZXkXXXk', 'kXkZXkZk', 'kXZXkYXk', '.kXXZXk.'],        # 光の 帯が 割れる
    'atk0|atk1|atk2': ['.kkkkkk.', 'kwwYXZXk', 'kYwwYXXk', 'kXYwwYZk', 'kXZYwwYk', '.kXXYwk.'],
    'ko': ['.kkkkkk.', 'kXXXXZXk', 'kZkXXkXk', 'kXXkkXZk', 'kXkXXkXk', '.kXXZXk.'],
}
BROW = ['kkkkkkkkk', '.EEEEEEEk']                           # かぶとの ひさし（つり上がった まゆ）

# ---- 触角：くの字（ひじ）に 折れて 前へ。付け根は 頭に 2ドット もぐる ----
ANT = [
    '..........kkk',
    '.........kCCk',
    '........kCDk.',
    '.......kCDk..',
    '..kk..kCDk...',
    '.kCDkkCDk....',
    '.kCDCDDk.....',
    '..kCDDk......',
    '...kCDk......',
    '....kCDk.....',
    '.....kDk.....',
    '.....kk......',
]
ANT2 = ['.'] + ANT[:3] + ['.......kCDk..', '..kk..kCDk...', '.kCDkkCDk....', '.kCDCDDk.....', '..kCDDk......', '...kCDk......', '....kDk.....', '....kk......']
# ---- 大あご ＝ こぶし（見せ所）：口の 両わきから 太い あごが 前へ のび、先が にぎりこぶし（指の 節 3本＋親指）----
def fist():
    return pix.outline([
        '.........FFFFFFF..',
        '.......FFFGGGGGGF.',
        'FFFF..FFGGGGGGGGGw',
        'FGGGFFGGGGGGGHHHHH',
        'GGGGGGGGGGGGGGGGGw',
        'GGGGGGGGGGGGGHHHHH',
        'HGGGGGGGGGGGGGGGGw',
        '.HHHGGGGGGGGGHHHHH',
        '....HGFFFFFGGGGGGH',
        '....HGGGGGGGGGGGH.',
        '.....HHHHHHHHHHHH.',
    ])
FIST = fist(); FIST_F = dark(FIST, DK)
JAW = ['.kkkk.', 'kFGGHk', 'kGGHHk', '.kkkk.']
FANG = ['kwkwk', '.k.k.']

# ---- くび（細い くびれ）・胸（たてに 立つ 小さな 豆形）・腹柄（節の こぶ）・腹（後ろ下へ つき出る たまご）----
NECK = P(M(6, 6, ('e', '1', 3, 3, 3, 3)), SHELL, lw=1, dw=2)
THORAX = P(M(12, 13, ('e', '1', 6, 6.5, 6, 6.5)), SHELL, [(['CC', 'C', 'C'], 2, 2), (['EEE', '..E'], 6, 8)], lw=2, dw=3)
NODE = P(M(6, 6, ('e', '1', 3, 3, 3, 3)), SHELL, lw=1, dw=2)
GASTER = P(M(21, 15, ('e', '1', 10.5, 7.5, 10.5, 7.2), ('p', '1', [(0, 9), (5, 6), (6, 13)])), SHELL, [
    (['.EE', 'E..', 'E..', 'E..', 'E..', 'E..', '.E.', '..E'], 7, 2),     # 節の すじ（たまごに そって 弧）
    (['.EE', 'E..', 'E..', 'E..', 'E..', 'E..', 'E..', '.E.', '..E'], 12, 2),
    (['CCC', 'C', 'C'], 3, 3),
], lw=2, dw=3)

# ---- 足（2本だけ）：ふともも → ひざ → すね（さらし）→ とがった 足先。上は 胸に 3ドット もぐる ----
def leg(knee=0):
    g = M(12, 19, ('t', '1', 2.6, [(3.5, 2.5), (8, 7.5)]), ('t', '1', 2.0, [(8, 7.5), (5, 14.5)]), ('p', '1', [(2.5, 14), (7.5, 14), (11, 18.5), (1.5, 18.5)]))
    return P(g, SHELL, [(['wwV', 'VwV', 'wVV'], 4, 10), (['C'], 3, 3), (['CC', 'CE'], 7, 6)], lw=1, dw=2)
LEG = leg(); LEG_F = dark(leg(), DK)

POW = ['...k...k...', '..kFk.kFk..', 'kk.kFkFk.kk', 'kFkkFwFkkFk', '.kFFwwwFFk.', 'kFkkFwFkkFk', 'kk.kFkFk.kk', '..kFk.kFk..', '...k...k...']
def layers():
    return [
        dict(n='antF', g='ant', x=17, y=4, rows=dark(ANT, DK), alt={'idle1|idle3|walk1|walk3': dark(ANT2, DK)}),
        dict(n='legF', g='legB', x=22, y=42, rows=LEG_F),
        dict(n='fistF', g='fistF', x=37, y=17, rows=FIST_F),
        dict(n='gaster', g='gaster', x=4, y=36, rows=GASTER),
        dict(n='node', g='body', x=20, y=40, rows=NODE),
        dict(n='thorax', g='body', x=23, y=32, rows=THORAX),
        dict(n='neck', g='body', x=28, y=29, rows=NECK),
        dict(n='legN', g='legA', x=27, y=42, rows=LEG),
        dict(n='head', g='head', x=21, y=12, rows=HEAD),
        dict(n='ant', g='ant', x=27, y=2, rows=ANT, alt={'idle1|idle3|walk1|walk3': ANT2}),
        dict(n='brow', g='head', x=33, y=17, rows=BROW),
        dict(n='eye', g='head', x=34, y=19, rows=EYE, alt=EYE_ALT),
        dict(n='fang', g='head', x=39, y=30, rows=FANG),
        dict(n='jaw', g='head', x=38, y=25, rows=JAW),
        dict(n='fistN', g='fistN', x=37, y=24, rows=FIST),
        dict(n='pow', g='fistN', x=56, y=25, rows=POW, only='atk1'),
        dict(n='pow2', g='fistF', x=56, y=18, rows=POW, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'fistN': (0, -1)}, 'idle3': {'fistF': (0, -1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'fistN': (1, 0)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'fistF': (1, 0)},
    'atk0': {'body': (-1, 1), 'fistN': (-2, 0), 'fistF': (-2, 0), 'gaster': (1, -1)},
    'atk1': {'root': (3, 0), 'fistN': (3, 0), 'fistF': (-1, 0)}, 'atk2': {'root': (4, 0), 'fistF': (3, 2), 'fistN': (-1, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'fistN': (-1, 1), 'fistF': (-1, 0)}, 'ko': {'_flip': True},
}
PARENT = {'ant': 'head', 'fistN': 'head', 'fistF': 'head', 'head': 'body', 'gaster': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
