# ジシャクギュウ（はがね・でんき × 牛）手打ち GBA風・デフォルメ（2〜3頭身）
EYE_BOX = (38, 26, 10, 7)
META = dict(id='jishakugyu', name='ジシャクギュウ', types=['steel', 'elec'], base='牛', size='L')
PAL = {
    'k': '#101018', 'l': '#1e2030',
    'A': '#8e98b2', 'B': '#5a6280', 'C': '#343a52',
    'S': '#eef2fa', 'T': '#a0aac2',
    'R': '#f24444', 'D': '#9c1c2a',
    'E': '#5aaaff', 'F': '#2454b4',
    'Y': '#fff27a', 'O': '#f0a820',
    'P': '#c4a2ae',
    'w': '#ffffff',
}
LIGHT = set('ASREYPw')
import pix
from pix import grid, rows_of, outline, ellipse, poly, line, recolor


# ---- 下書きの 道具（あたりは 図形で、仕上げは 手で 打つ）----
def G(w, h): return grid(w, h)
def ell(g, cx, cy, rx, ry, ch): ellipse(g, cx, cy, rx, ry, ch); return g
def pl(g, pts, ch): poly(g, pts, ch); return g
def thick(g, pts, ch, w=2):
    """太い 線（尾・首などの あたり）"""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for dx in range(w):
            for dy in range(w): line(g, x0 + dx, y0 + dy, x1 + dx, y1 + dy, ch)
    return g
def edge(g, mats, ch='k'):
    """素材の さかい目に 内側の 線（あとで エンジンが 濃い色に する）"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if src[y][x] not in mats: continue
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and src[yy][xx] not in mats and src[yy][xx] not in '.k': g[y][x] = ch; break
    return g
def shade(g, ramps, hl=1, dk=2, dr=1):
    """光は 左上：上・左の ふち hl ドットは 明、下の ふち dk・右の ふち dr ドットは 暗"""
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, m):
        n = 0
        while n < 9 and 0 <= y + dy * (n + 1) < H and 0 <= x + dx * (n + 1) < W and src[y + dy * (n + 1)][x + dx * (n + 1)] == m: n += 1
        return n
    for y in range(H):
        for x in range(W):
            m = src[y][x]
            if m not in ramps: continue
            L, M, D = ramps[m]
            u, l, d, r = run(y, x, -1, 0, m), run(y, x, 0, -1, m), run(y, x, 1, 0, m), run(y, x, 0, 1, m)
            c = M
            if d < dk or r < dr: c = D
            elif u < hl or l < hl: c = L
            g[y][x] = c
    return g
def at(g, x, y, *rows):
    """手打ち：( x, y ) から 文字を 置く（空白と '.' は そのまま）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c not in ' .' and 0 <= y + j < len(g) and 0 <= x + i < len(g[y + j]): g[y + j][x + i] = c
    return g
def done(g, open_top=0, open_left=0):
    """輪郭を つける。付け根側の 輪郭を 開けて 体に なじませる"""
    rows = [list(r) for r in outline(rows_of(g))]
    for y in range(open_top): rows[y] = ['.' if c == 'k' else c for c in rows[y]]
    for r in rows:
        for x in range(open_left):
            if r[x] == 'k': r[x] = '.'
    return [''.join(r) for r in rows]
RAMP = {'h': 'ABC', 's': 'STT', 'r': 'RRD', 'b': 'EEF', 'm': 'PPB', 'y': 'YYO', 'f': 'BCC'}
DARKER = {'A': 'B', 'B': 'C', 'C': 'l', 'S': 'T', 'P': 'B', 'w': 'T'}
def dark(rows): return recolor(rows, DARKER)


# ---- 角（見せ所）：2本で 大きな U字磁石。前の 先は 赤、後ろの 先は 青 ----
def horns(arc=0):
    W, H = 40, 29; g = G(W, H)
    thick(g, [(10, 28), (5, 22), (3, 15), (3, 9), (5, 4), (9, 1)], 's', 5)       # 後ろの 角
    thick(g, [(25, 28), (30, 22), (32, 15), (32, 9), (30, 4), (26, 1)], 's', 5)  # 前の 角
    for y in range(H):
        for x in range(W):
            if g[y][x] == 's' and y <= 8: g[y][x] = 'b' if x < 19 else 'r'
    edge(g, 'b'); edge(g, 'r')
    shade(g, RAMP, hl=1, dk=1, dr=1)
    for y in (9, 10):                                               # 磁石の 色の さかいの 白い 帯
        for x in range(W):
            if g[y][x] in 'ST': g[y][x] = 'S' if g[y][x] == 'T' else 'w'
    # 先と 先の 間に 走る 稲妻（角に つながって いる）
    if arc == 1: at(g, 14, 2, 'kYk.....kk', '.kYk..kYYk', '..kYkkYk..', '...kYYk...')
    elif arc == 2: at(g, 14, 3, '.kk...kYk.', 'kYYk.kYk..', '...kYYk...', '....kk....')
    elif arc == 3: at(g, 14, 1, 'kkkk...kkk', 'YYYYkkkYYY', 'kkkYYYYkkk', '...kkkk...')
    return done(g)

# ---- 頭：大きく 重い。まゆの ひさし、鼻に 鉄の 輪 ----
def head(eye=None, ko=False, mouth=0):
    g = G(29, 24)
    ell(g, 12, 10, 11.5, 9.5, 'h')
    ell(g, 21, 15, 7, 6, 'm')                                       # 鼻づら
    ell(g, 2, 8, 3, 2, 'h')                                         # 耳（横へ）
    edge(g, 'm')
    shade(g, RAMP, hl=1, dk=3, dr=1)
    at(g, 4, 12, 'B'); at(g, 5, 14, 'BC'); at(g, 7, 16, 'C')         # ほおの 筋
    at(g, 24, 13, 'kk'); at(g, 23, 14, 'k')                         # 鼻の あな
    if mouth: at(g, 15, 18, 'kkkkkkkkkkk', 'kDDDDDDDDk', '.kwkkkkkk')
    else: at(g, 16, 19, 'kkkkkkkkk')
    at(g, 21, 19, 'kSSk', 'kTPTk', '.kSTk', '..kk')                  # 鉄の 鼻輪
    at(g, 9, 4, *(EYE_KO if ko else (eye or EYE)))                  # 目（C 三白眼）と まゆの ひさし
    return done(g)
# 三白眼（C）：大きな 白目の 前上の すみに 小さな 赤い 瞳が 寄り、横目で にらむ。前へ 下がる 重い まゆの ひさしと 太い 下まぶた
EYE = ['kkkk......',
       'BkkkkkkC..',
       '.kTwwwkkkk',
       'kTwwwwwRkk',
       '.kTwwwwDRk',
       '..kkkkkkk.',
       '...CCCCC..']
EYE_BLINK = ['kkkk......', 'BkkkkkkC..', '.kBBBBkkkk', 'kBBBBBBBkk', '.kkkkkkkkk', '..CCCCCC..', '..........']
EYE_HIT = ['kkkk......', 'BkkkkC....', '.kkkkkkk..', 'kTwRkwwkk.', '.kkkkkkk..', '..CCCC....', '..........']    # 目を ゆがめ、瞳が 下へ はずれる
EYE_ATK = ['kkkkk.....', 'BkkkkkkkC.', '.kkTwwwkkk', 'kTwwwwwwRk', '.kTwwwwRDk', '..kkkkkkk.', '...CCCCC..']   # まゆが 下がり、瞳が さらに 小さく 前へ
EYE_KO = ['kkkk......', 'BkkkkkkC..', '.kBkBBBkB.', '..BBkBkBB.', '..BBBkBBB.', '..BBkBkBB.', '...CCCCC..']

# ---- 胴：小さく ずんぐり、鋼の 板と 稲妻の もよう ----
def body():
    g = G(30, 22)
    ell(g, 15, 12, 14.5, 9.5, 'h')
    ell(g, 21, 7, 8, 6, 'h')                                        # 肩の こぶ
    shade(g, RAMP, hl=1, dk=3, dr=2)
    thick(g, [(6, 5), (9, 10), (7, 12), (11, 17)], 'Y', 1)          # 稲妻の もよう
    at(g, 10, 5, 'O'); at(g, 12, 15, 'O')
    line(g, 15, 3, 15, 19, 'C'); line(g, 16, 3, 16, 19, 'A')        # 鋼の 板の つぎ目
    for y in (6, 11, 16): at(g, 17, y, 'S')                         # 鋲
    return done(g)

LEG_M = ['.hhhhhh.', 'hhhhhhhh', 'hhhhhhhh', '.hhhhhh.', '.hhhhhh.', '.hhhhhh.', '.ffffff.', 'ffffffff']
def leg():
    g = pix.grid_of(LEG_M); shade(g, RAMP, dk=1)
    at(g, 4, 3, 'C')
    r = done(g, open_top=2)
    return r
def tail(ph=0):
    g = G(10, 14)
    thick(g, [(9, 1), (5, 3), (3, 7), (2, 10)], 'h', 1)
    shade(g, RAMP, dk=1)
    at(g, 0, 9, 'kYk', 'YOYk', 'kYOY', '.kYk') if not ph else at(g, 0, 9, '.Yk', 'kYOY', 'YOYk', 'kY..')
    return done(g)

# ---- 電げき（エフェクト：はなれて いるのは 意図的）----
BOLT = ['....kk.....', '...kYk.....', '..kYOk.kk..', '.kYYYkkYk..', 'kYOYYYYYk..', '.kkkYYOk...', '...kYYk....', '..kYOk.....', '..kYk......', '...k.......']
BOLT2 = ['..kk...kk..', '.kYYk.kYk..', 'kYOYYkYk.k.', '.kkYYYYkkYk', '...kYOYYYOk', '..kYYkkkkk.', '.kYOk......', 'kYYk.......', '.kk........']

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=34, rows=tail(), alt={'idle1|idle3|walk1|walk3|atk1': tail(1)}),
        dict(n='legHF', g='legB', x=12, y=50, rows=dark(leg())),
        dict(n='legFF', g='legB', x=31, y=50, rows=dark(leg())),
        dict(n='body', g='body', x=6, y=31, rows=body()),
        dict(n='legH', g='legA', x=8, y=51, rows=leg()),
        dict(n='legF', g='legA', x=26, y=51, rows=leg()),
        dict(n='horns', g='head', x=21, y=1, rows=horns(), alt={'idle1|walk1|atk0': horns(1), 'idle3|walk3': horns(2), NB: horns(3)}),
        dict(n='head', g='head', x=28, y=21, rows=head(),
             alt={'blink': head(EYE_BLINK), 'hit': head(EYE_HIT), 'atk0': head(EYE_ATK), NB: head(EYE_ATK, mouth=1), 'ko': head(ko=True)}),
        dict(n='bolt', g='fx', x=59, y=38, rows=BOLT, alt={'atk2': BOLT2}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1), 'tail': (0, 1)}, 'idle3': {'body': (0, 1), 'tail': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'head': (0, -1), 'tail': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'tail': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 3), 'tail': (-2, 0), 'legA': (-1, 0)},
    'atk1': {'root': (4, 0), 'head': (2, 3)}, 'atk2': {'root': (6, 0), 'head': (2, 2), 'fx': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
