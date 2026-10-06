# ドブマスク（あく・どく × ドブネズミ）手打ち GBA風・デフォルメ（2〜3頭身）
META = dict(id='dobumasuku', name='ドブマスク', types=['dark', 'poison'], base='ドブネズミ', size='M')
PAL = {
    'k': '#101018', 'l': '#2e1a36',
    'A': '#8e84a4', 'B': '#5e5474', 'C': '#3a3248',
    'F': '#ecdcae', 'G': '#c0a072', 'H': '#7a5a3a',
    'P': '#ee9cac', 'Q': '#a85870',
    'V': '#d4f46a', 'X': '#74c03c', 'Z': '#2e7438',
    'R': '#ff6a3c', 'D': '#a8182c',
    'w': '#ffffff',
}
LIGHT = set('AFPVw')
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
FUR = {'f': 'ABC'}
DARKER = {'A': 'B', 'B': 'C', 'C': 'l', 'P': 'Q', 'Q': 'l', 'F': 'G', 'G': 'H', 'w': 'G'}
def dark(rows): return recolor(rows, DARKER)


# ---- 胴：小さく 丸い。背中に 逆立つ 毛の とげ ----
def body():
    g = G(24, 21)
    ell(g, 12.5, 11.5, 9.5, 8.5, 'f')
    for x0 in (4, 8, 13):                                     # 背の 逆毛（左上へ とがる）
        pl(g, [(x0 - 2, 6), (x0 - 4, 0 + (x0 == 4) * 2), (x0 + 3, 4)], 'f')
    ell(g, 17, 13, 4.5, 6, 'b')                               # 明るい 腹
    shade(g, {'f': 'ABC', 'b': 'AAB'}, hl=1, dk=3, dr=2)
    at(g, 6, 9, 'B'); at(g, 7, 11, 'BB'); at(g, 5, 14, 'C'); at(g, 9, 15, 'BC')   # 毛並みの すじ（手打ち）
    at(g, 14, 9, 'lll')                                      # 胸の 毛の さかい
    return done(g)

# ---- 足：短く 太い もも＋大きな 足、つめ ----
LEG_M = [
    '..ffffff...',
    '.ffffffff..',
    '.ffffffff..',
    '..ffffff...',
    '..fffff....',
    '..pppppppp.',
    '.pppppppppp',
]
def leg():
    g = [list(r) for r in LEG_M]; shade(g, {'f': 'ABC', 'p': 'PPQ'}, dk=1)
    at(g, 5, 4, 'C')
    r = done(g, open_top=2)
    r[-1] = r[-1][:7] + 'kwkw' + r[-1][11:]                   # つめ
    return r

# ---- 腕：短く、つめの 大きな 手を 前に かまえる ----
ARM = [
    '.kkkk...........',
    'kAAABkkk........',
    'kBBBBBBBkkk.....',
    '.kBBBBBBPPPkk...',
    '..kCBBBPPPPQwk..',
    '...kCCkPQQQQkwk.',
    '....kk.kkQkQkwk.',
    '.......kwkwkwk..',
    '........k.k.k...',
]
def arm(): return ['.' + ARM[0][1:]] + ARM[1:]

# ---- 尾：長い ピンクの 尾が 後ろで 巻く（ふしの 線）----
def tail():
    g = G(18, 20)
    thick(g, [(17, 16), (11, 17), (5, 15), (2, 11), (2, 6), (5, 3), (8, 3), (9, 5)], 'p', 2)
    shade(g, {'p': 'PPQ'}, dk=1)
    for x, y in ((12, 17), (7, 16), (3, 12), (2, 8), (4, 4)): g[y][x] = 'Q' if g[y][x] != '.' else '.'
    return done(g)

# ---- 頭：ネズミの 頭に くちばしの 仮面（見せ所）----
def head(gas=0, ko=False):
    g = G(41, 27)
    ell(g, 14, 4.5, 3.5, 4.5, 'q'); ell(g, 14.5, 5, 1.5, 2.5, 'r')    # 奥の 耳
    ell(g, 10.5, 15, 11, 9.5, 'f')                                 # 頭（大きく 丸い）
    ell(g, 6, 5, 4.5, 5.5, 'e'); ell(g, 6.5, 5.5, 2.5, 3.5, 'p')      # 耳（丸く 大きい、頭の 上に 立つ）
    ell(g, 17, 14, 7, 8, 'm')                                      # 仮面の 顔
    pl(g, [(15, 7), (26, 10), (39, 17), (39.5, 19.5), (28, 21), (15, 23)], 'm')   # くちばし（長い 円すい）
    edge(g, 'qr'); edge(g, 'm'); edge(g, 'e'); edge(g, 'p')
    shade(g, {'f': 'ABC', 'e': 'ABC', 'q': 'BBC', 'r': 'QQl', 'm': 'FGH', 'p': 'PPQ'}, hl=1, dk=3, dr=1)
    line(g, 19, 15, 38, 18, 'H')                                   # くちばしの ぬい目
    for x, y in ((23, 13), (29, 14), (34, 16)): at(g, x, y, 'F')
    for x, y in ((22, 16), (27, 17)): at(g, x, y, 'k')
    at(g, 32, 18, 'kX'); at(g, 35, 19, 'kV')                       # 毒の 霧が もれる 穴
    line(g, 3, 13, 11, 10, 'l'); line(g, 3, 14, 11, 11, 'C')        # 仮面を とめる 革の ベルト
    at(g, 7, 11, 'G')
    at(g, 12, 9, '.HHHHHH', 'H......H', 'H......H', 'H......H', '.HHHHHH')   # レンズの 枠
    if ko: at(g, 13, 10, 'k...k', '.k.k.', '..k..', '.k.k.')
    else: at(g, 13, 9, 'kk', '..kkkk', 'kwRRkDk', 'kRDDkDk', '.kkkkk')       # 目
    at(g, 16, 23, 'kwwk', 'kwGk', '.kk')                           # 出っ歯
    if gas: at(g, 36, 20, 'XX', '.V')
    return done(g)
EYE_BLINK = ['......', '..kkkk', 'kkkkkkk', '.BBBBB', '......']
EYE_HIT = ['k.....', '.kk...', 'kRRkkk', 'kkkkRk', '......']
EYE_ATK = ['kk....', '..kkkk', 'kwwRkVk', 'kRRRkRk', '.kkkkk']

# ---- 毒の 霧（エフェクト：はなれて いるのは 意図的）----
def cloud(big=False):
    w, h = (18, 14) if big else (13, 10)
    g = G(w, h)
    for cx, cy, r in ([(4, 7, 3.5), (9, 5, 4.5), (13, 8, 4), (8, 10, 3.5)] if big else [(3, 5, 3), (7, 4, 3.5), (9, 6, 3)]):
        ell(g, cx, cy, r, r * .9, 'v')
    shade(g, {'v': 'VXZ'}, hl=2, dk=2, dr=2)
    for x, y in ((6, 3), (10, 6)): at(g, x, y, 'Z')
    return done(g)

NB = 'atk1|atk2'
def eye_head(e):
    """頭に 目の 差しかえを 置く"""
    g = [list(r) for r in head(gas=1)]
    at(g, 14, 10, *e)
    return rows_of(g)
H0, H1, HKO = head(), head(gas=1), head(ko=True)
def layers():
    return [
        dict(n='tail', g='tail', x=1, y=33, rows=tail()),
        dict(n='legF', g='legB', x=16, y=52, rows=dark(leg())),
        dict(n='armF', g='armB', x=33, y=40, rows=dark(arm())),
        dict(n='body', g='body', x=14, y=34, rows=body()),
        dict(n='leg', g='legA', x=25, y=52, rows=leg()),
        dict(n='head', g='head', x=19, y=14, rows=H0,
             alt={'idle1|idle2|walk1|walk3': H1, 'blink': eye_head(EYE_BLINK), 'hit': eye_head(EYE_HIT),
                  'atk0|atk1|atk2': eye_head(EYE_ATK), 'ko': HKO}),
        dict(n='arm', g='armA', x=30, y=41, rows=arm()),
        dict(n='cloud', g='fx', x=59, y=29, rows=cloud(), alt={'atk2': cloud(True)}, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1), 'armA': (0, 1)}, 'idle3': {'body': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'armA': (1, 0)}, 'walk1': {'body': (0, -1), 'head': (0, -1), 'armA': (0, -1), 'armB': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'armB': (1, 0)}, 'walk3': {'body': (0, -1), 'armA': (0, -1), 'armB': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'armA': (-3, 1), 'armB': (-2, 1), 'tail': (-1, 0)},
    'atk1': {'root': (3, 0), 'head': (1, 0), 'armA': (3, -2)}, 'atk2': {'root': (4, 0), 'head': (1, 1), 'armA': (4, 0), 'fx': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'armA': (-1, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'armA': 'body', 'armB': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
