# キババーバー（ノーマル・みず × ビーバー）手打ち GBA風・デフォルメ（2〜3頭身：頭と のみの 歯は そのまま、胴を 小さく 短く）
META = dict(id='kibabeaver', name='キババーバー', types=['normal', 'water'], base='ビーバー', size='M')
PAL = {
    'k': '#101018', 'l': '#42201c',
    'F': '#cc7a4e', 'G': '#8c4630', 'H': '#4e2420',
    'Y': '#ffd47a', 'T': '#f08a22',
    'N': '#b49a72', 'L': '#6e5a42', 'M': '#3e3226',
    'C': '#e6fbff', 'A': '#5cc6f0', 'B': '#2470c0',
    'w': '#ffffff', 'x': '#060608',                      # x＝ビーズ目の 黒
}
LIGHT = set('FYNCw')
KEEP_BLACK = set('wx')
EYE_BOX = (40, 27, 9, 7)   # 目・まゆ・白い 傷（idle0 の 64x64 座標）

def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out
def shade(spans, W, ramp='FGH', lit=1, dk=2):
    H = len(spans); m = [[a <= x <= b for x in range(W)] for (a, b) in spans]
    def ins(y, x): return 0 <= y < H and 0 <= x < W and m[y][x]
    g = [['.'] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            du = next(i for i in range(1, 9) if not ins(y - i, x) or i == 8)
            dl = next(i for i in range(1, 9) if not ins(y, x - i) or i == 8)
            dd = next(i for i in range(1, 9) if not ins(y + i, x) or i == 8)
            dr = next(i for i in range(1, 9) if not ins(y, x + i) or i == 8)
            c = ramp[1]
            if dd <= dk: c = ramp[2]
            elif du <= lit or dl <= 1: c = ramp[0]
            elif dr <= 1: c = ramp[2]
            g[y][x] = c
    return g
def rot90(rows):
    h, w = len(rows), max(len(r) for r in rows); rows = [r.ljust(w, '.') for r in rows]
    return [''.join(rows[h - 1 - y][x] for y in range(h)) for x in range(w)]

# ---- 胴：肩が もり上がった 前のめりの 体（あたりは 多角形）→ ぬれた 毛の たば・筋肉・きずあとは 手で ----
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, poly, outline, rows_of
def run(g, x, y, dx, dy):
    n = 0
    while 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] != '.': n += 1; x += dx; y += dy
    return n
SX, SY = .78, .8   # デフォルメ：胴の はばと 高さを ちぢめる
def X(x): return round(x * SX)
def body():
    W, H = 27, 25; g = grid(W, H)
    poly(g, [(x * SX, y * SY) for x, y in [(0, 16), (2, 9), (7, 5), (13, 3), (19, 0), (25, 1), (30, 6), (33, 13), (33, 22), (30, 28), (20, 26), (14, 29), (4, 29), (0, 23)]], '#')
    # 背中の ぬれた 毛の たば（後ろへ とがる）
    for (x, y) in ((4, 6), (5, 5), (8, 3), (9, 2), (12, 1), (13, 0)):
        if 0 <= y < H: g[y][x] = '#'
    out = grid(W, H)
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.': continue
            up, lf, dn, rt = run(g, x, y, 0, -1), run(g, x, y, -1, 0), run(g, x, y, 0, 1), run(g, x, y, 1, 0)
            c = 'G'
            if dn <= 4 or rt <= 2: c = 'H'
            elif dn == 5 and (x + y) % 2: c = 'H'
            if up <= 2 or (lf <= 2 and dn > 4): c = 'F'
            if x >= 21 and y >= 13 and c == 'G' and (x + y) % 2: c = 'H'      # 頭の 下の 影（ディザ）
            out[y][x] = c
    # 毛の すじ（後ろ下へ ながれる）
    for (x, y) in ((6, 6), (7, 7), (10, 4), (11, 5), (15, 2), (16, 3), (19, 3), (20, 4), (4, 9), (5, 10), (9, 8), (10, 9), (14, 6), (15, 7)):
        if out[y][x] == 'G': out[y][x] = 'H'
        if out[y][x - 1] == 'G': out[y][x - 1] = 'F'
    # ももの 筋肉（大きな 弧）
    for (x, y) in ((8, 11), (7, 12), (6, 13), (6, 14), (6, 15), (7, 16), (8, 17), (9, 18), (10, 19)):
        out[y][x] = 'l'
        if out[y][x + 1] == 'G': out[y][x + 1] = 'F'
    # 肩の きずあと（3本の 爪あと）
    for i in range(3):
        for j in range(5):
            x, y = 15 + i * 2 + j // 2, 5 + j + i
            out[y][x] = 'l'
            if out[y][x - 1] in 'GH': out[y][x - 1] = 'N'
    # 水てき
    for (x, y) in ((7, 4), (12, 2), (3, 8), (20, 3)):
        out[y][x] = 'C'; out[y + 1][x] = 'A'
    return outline(rows_of(out))

# 頭：低く 前へ つき出す。重い まゆの ひさし・きずあと・するどい 目・大きな のみの 歯
HEAD = [
    '..kk..kkkkkk...........',
    '.kFHkkFFFFFFkk.........',
    '.kGHkFGGGGGGFFkk.......',
    'kFGGGGGGGGGGGGGFkk.....',
    'kFGGGGGGGNkkkkkkGFkk...',
    'kGGGGGGGkNlHHHHHkkGFk..',
    'kGGGGGGkHHl......HkGFk.',
    'kGGGGGGGkkkN......GGGFk',
    'kGGGGGGGGGGlNGGGNNNNkkk',
    'kHGGGGGGGGGGlGNNNNNNkkk',
    'kHGGGGGGGGGGGNNNNNNNLLk',
    '.kHGGGGGGGGGGGNNNNLLLk.',
    '.kHHGGGGGGGkkkkkkkkkk..',
    '..kHHGGGGGkYYYkYTk.....',
    '...kkHHHHkYYYYkYTTk....',
    '.....kkkkkYYYTkYTTk....',
    '.........kYYYTkYTTk....',
    '.........kYYTTkTTTk....',
    '.........kYYTTkTTk.....',
    '..........kkkkkkk......',
]
TEETH_GLINT = ['w', 'w', 'w']
# 目（S：ビーズ目＋太い まゆ）：小さく 真っ黒な ビーズ目（x）に 白の ハイライト 1点。上に 太く 前へ さがる まゆ（黒線＋こげ茶 H）。白い 古傷（C）が まゆを 切って ほおへ ななめに 走る
#   （頭の 目の 穴を うめるため、この 層は まゆと 傷の まわりも 描く）
_E0 = ['C........', 'Ckkkkkk..', 'lCHHHHHkk']
EYE = _E0 + ['HHCNkwxkH', 'GGlCkxxkG', '....Ckk..', '.....C...']
EYE_ALT = {'blink': _E0 + ['HHCNHHHkH', 'GGlCkkkkG', '....CGG..', '.....C...'],
           'atk0|atk1|atk2': _E0 + ['HHCNHHHHk', 'GGlCkwxkG', '....Ckk..', '.....C...'],
           'hit': _E0 + ['HHCNkkGkH', 'GGlCGkkGG', '....CGG..', '.....C...'],
           'ko': _E0 + ['HHCNGxGxH', 'GGlCGGxGG', '....CxGx.', '.....C...']}
# 丸太の しっぽ：木の 皮の すじ と 切り口の 年輪
TAIL = [
    '..kkkkkkkkkkkkkk..',
    '.kNkkNLLNNNkLLNLk.',
    'kNkNNkLLLLLkLLLMk.',
    'kNkNYkkLLMLkLLMMk.',
    'kNkNNkLLLLLLkLMMk.',
    'kNNkkLLMLLLLkMMMk.',
    'kLMMMMkMMMMMkMMMk.',
    '.kMMMMMMMMMMMMMk..',
    '..kkkkkkkkkkkkk...',
]
TAIL_UP = rot90(TAIL)
DRIP = ['C.', 'A.', '..', '.A', '.B']
DRIP2 = ['..', 'C.', 'A.', '..', '.A']
FLEG = [
    '.kkkkkkk..',
    'kFGGGGGHk.',
    'kFGGGGGHHk',
    'kFGGGGGHHk',
    '.kFGGGGHHk',
    '.kFGGGGHk.',
    '.kFGGGHHk.',
    '.kFGGGHHk.',
    '.kFGGGGHk.',
    '.kGGGGHHk.',
    '.kFGGGGHHk',
    'kFGGGGGHHk',
    'kGGGlGGlHk',
    'kHHHlHHlHk',
    'kwkkwkkwk.',
]
HLEG = [
    '.kGGGGGHk....',
    'kFGGGGGHHk...',
    'kFGGGGGHHk...',
    '.kFGGGGHHk...',
    '.kFGGGHHHk...',
    '..kFGGHHk....',
    '..kFGGHHk....',
    'kGGGGHHHHkk..',
    'kHHHHHHHHHHk.',
    'kHAAkHAAkHBBk',
    'kkkkkkkkkkkkk',
]
PUDDLE = ['..kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..', '.kAACCAAAAAACCAAAAAACCAAAAAACAABk.', '..kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..']
PUDDLE2 = ['..kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..', '.kAAAACCAAAAAAACCAAAAAACCAAAAAABk.', '..kkkkkkkkkkkkkkkkkkkkkkkkkkkkk..']
# 攻撃：しっぽで たたいて 前へ 走る 大波
WAVE = [
    '.....kkkk.....',
    '...kkCCCAkk...',
    '..kCCAAAAABk..',
    '.kCAAABBkkABk.',
    '.kCAABk...kk..',
    'kCAABBk.......',
    'kAABBBBk......',
    'kABBBBBBkkk...',
    'kkkkkkkkkkk...',
]
WAVE2 = [
    '......kkkk......',
    '....kkCCCAkk....',
    '...kCCAAAAABk...',
    '..kCAAABBkkABk..',
    '.kCAAABk...kABk.',
    '.kCAABBk....kk..',
    'kCAABBBBk.......',
    'kAABBBBBBkk.....',
    'kABBBBBBBBBkkk..',
    'kkkkkkkkkkkkkk..',
]
SPLASH = ['C...A..C', '.A.C..A.', 'A..A.C..', '.C...A.A']
DARK = {'F': 'G', 'G': 'H', 'H': 'l'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]

BODY = body()
def layers():
    L = [
        dict(n='puddle', g='root', x=2, y=58, rows=PUDDLE, alt={'idle1|idle3|walk1|walk3': PUDDLE2}, not_='ko'),
        dict(n='tail', g='tail', x=1, y=42, rows=TAIL, not_='atk0'),
        dict(n='tailup', g='tail', x=6, y=24, rows=TAIL_UP, only='atk0'),
        dict(n='drip', g='tail', x=4, y=51, rows=DRIP, alt={'idle1|idle3|walk1|walk3': DRIP2}, not_='atk0|atk1|atk2|ko'),
        dict(n='splash', g='root', x=1, y=36, rows=SPLASH, only='atk1'),
        dict(n='legHF', g='legB', x=19, y=47, rows=dark(HLEG)),
        dict(n='legFF', g='legA', x=35, y=45, rows=dark(FLEG)),
        dict(n='body', g='body', x=11, y=30, rows=BODY),
        dict(n='legH', g='legA', x=12, y=47, rows=HLEG),
        dict(n='legF', g='legB', x=29, y=45, rows=FLEG),
        dict(n='head', g='head', x=31, y=27, rows=HEAD),
        dict(n='eye', g='head', x=40, y=30, rows=EYE, alt=EYE_ALT),
        dict(n='glint', g='head', x=42, y=41, rows=TEETH_GLINT, only='atk0|atk1'),
        dict(n='wave', g='fx', x=46, y=50, rows=WAVE, alt={'atk2': WAVE2}, only='atk1|atk2'),
    ]
    for l in L:
        if l['n'] not in ('puddle', 'wave') and not l['n'].startswith('leg'): l['y'] -= 3   # 足を 長く 見せる ぶん 体を 上げる
    return L

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1)},
    'idle2': {'body': (0, 1), 'tail': (0, 0)},
    'idle3': {'tail': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'tail': (0, -1)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'tail': (0, 1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, -1), 'head': (-1, -1)},
    'atk1': {'root': (3, 0), 'tail': (0, 2), 'head': (1, 1)},
    'atk2': {'root': (4, 0), 'tail': (0, 2), 'fx': (4, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, -2), 'tail': (0, -1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
