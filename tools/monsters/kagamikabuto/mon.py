# カガミカブト（エスパー・はがね × カブトガニ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：銅鏡の 甲羅（丸く 平らな 板）。鏡の まん中の 鈕（つまみ）が 第三の 目
META = dict(id='kagamikabuto', name='カガミカブト', types=['psychic', 'steel'], base='カブトガニ', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1c22',
    'Y': '#f2d488', 'O': '#c08a3a', 'o': '#6e4a20',      # 銅（ふち・頭）
    'S': '#eaf6ff', 'C': '#9cc6e0', 'c': '#56789c',      # 鏡の 面
    'V': '#e08cff', 'v': '#8a30b8',                      # 念力・第三の 目
    'A': '#b4bed6', 'B': '#68729a', 'D': '#363c5c',      # 鋼の 脚・尾剣
    'w': '#ffffff', 'r': '#a01c34',
}
LIGHT = set('YSAVw')
KEEP_BLACK = set('wV')
# ---------- 下書きの 道具（あたり → 左上光の 3段 → 輪郭。目・牙・模様・線は 手で 打つ）----------
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, poly, line
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def E(g, cx, cy, rx, ry, ch='1'): ellipse(g, cx, cy, rx, ry, ch)
def P(g, pts, ch='1'): poly(g, pts, ch)
def Ln(g, x0, y0, x1, y1, ch): line(g, x0, y0, x1, y1, ch)
def dots(g, ch, pts, on=None):
    """手で 1ドットずつ 打つ（on を 指定すると その 色の 上だけ）"""
    for x, y in pts:
        if 0 <= x < N and 0 <= y < N and (on is None or g[y][x] in on): g[y][x] = ch
def hand(g, x, y, rows):
    """手打ちの 絵（文字の 行）を はりつける。'.' は すける"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= x + i < N and 0 <= y + j < N: g[y + j][x + i] = c
def shade(g, ramps, lw=1, dw=2):
    """マスクに 光（左上）：上・左の ふち lw は 明、下・右の ふち dw は 暗"""
    src = [r[:] for r in g]
    for y in range(N):
        for x in range(N):
            m = src[y][x]
            if m not in ramps: continue
            Lc, Mc, Dc = ramps[m]
            def run(dy, dx):
                i = 1
                while i < 9 and at(src, x + dx * i, y + dy * i) == m: i += 1
                return i
            dr = min(run(1, 0), run(0, 1) + 1); ul = min(run(-1, 0), run(0, -1))
            g[y][x] = Dc if dr <= dw else Lc if ul <= lw else Mc
def part(draw, ramps, lw=1, dw=2, post=None, cut=()):
    """1つの パーツ：draw で 形 → 陰影 → post で 手打ち → 輪郭。cut の 四角では 輪郭を 開けて 体と つなぐ"""
    g = G(); draw(g); shade(g, ramps, lw, dw)
    if post: post(g)
    rows = [list(r) for r in outline(rows_of(g))]
    for (x0, y0, x1, y1) in cut:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if rows[y + 1][x + 1] == 'k' and at(g, x, y) == '.': rows[y + 1][x + 1] = '.'
    return [''.join(r) for r in rows]
def L(n, gr, rows, **kw): return dict(n=n, g=gr, x=-1, y=-1, rows=rows, **kw)
def H(n, gr, x, y, rows, **kw): return dict(n=n, g=gr, x=x, y=y, rows=rows, **kw)
import math
# ---- 尾剣（鋼の 長い とげ。つけ根は 腹に もぐる）----
def tail_d(g): P(g, [(14, 40), (4, 48), (3, 50), (6, 50), (15, 45)], '1')
def tail_p(g): Ln(g, 5, 49, 13, 43, 'w')
TAIL = part(tail_d, {'1': 'ABD'}, post=tail_p)
TAIL2 = part(lambda g: P(g, [(14, 40), (4, 46), (3, 48), (6, 48), (15, 44)], '1'), {'1': 'ABD'}, post=lambda g: Ln(g, 5, 47, 13, 42, 'w'))
# ---- 腹（小さい 六角の 板。ふちに とげ）----
def abd_d(g):
    P(g, [(19, 35), (12, 37), (9, 41), (12, 47), (20, 48)], '1')
    for (x, y) in ((11, 38), (9, 42), (10, 46)): P(g, [(x, y), (x - 3, y + 1), (x, y + 2)], '1')
def abd_p(g):
    Ln(g, 13, 40, 19, 40, 'D'); Ln(g, 13, 44, 19, 44, 'D')
    dots(g, 'w', [(13, 38), (14, 38)])
ABD = part(abd_d, {'1': 'ABD'}, post=abd_p)
# ---- 脚（短い 鋼の とがった 脚。つけ根は 甲羅の 下に もぐる）----
def legs(xs, ramp):
    """短い 鋼の 脚：ひざで 外へ まがり、先は とがる（前の 脚は 前へ、後ろの 脚は 後ろへ）"""
    def d(g):
        for x in xs:
            s_ = 1 if x > 30 else -1
            P(g, [(x, 46), (x + 5, 46), (x + 5 + 2 * s_, 53), (x + 3 + 3 * s_, 60), (x + 2 + 3 * s_, 60), (x + 1 + s_, 54)], '1')
    def p(g):
        for x in xs:
            s_ = 1 if x > 30 else -1
            dots(g, 'D', [(x + 1 + s_ + i, 53) for i in range(5)], 'ABD'); dots(g, 'w', [(x + 2 + 3 * s_, 59)])
    return part(d, {'1': ramp}, post=p)
LEG_A = legs((20, 35), 'ABD'); LEG_B = legs((25, 40), 'BDD')
# ---- 頭（銅の 前の 板。つり目と はさみ牙）----
def head_d(g):
    E(g, 43, 38, 10, 7, '2')
    P(g, [(36, 33), (46, 31), (53, 34), (56, 40), (54, 45), (40, 46)], '2')
    for y in range(45, N):
        for x in range(N):
            if g[y][x] == '2' and y > 45: g[y][x] = '.'
def head_p(g, open_=False):
    # 頭の 板の ふち（前に 3本の とげ）と 光の すじ
    # 馬てい形の ふち（前で 下に まがる）と 中の すじ
    Ln(g, 38, 41, 52, 41, 'o'); Ln(g, 52, 41, 55, 44, 'o'); dots(g, 'Y', [(x, 40) for x in range(39, 52)], 'O')
    Ln(g, 40, 33, 48, 33, 'Y')
    if not open_:
        hand(g, 47, 43, ['kkkkkkkk', '.wkw.wkk', '..w...w.'])
    else:
        hand(g, 46, 42, ['kkkkkkkkk', 'kwkrrrkwk', 'krrrrrrk.', '.wk.wk...'])
    for x in range(36, 53): dots(g, 'o', [(x, 45)], 'YO')
HEAD = part(head_d, {'2': 'YOo'}, lw=1, dw=2, post=head_p)
HEAD_OPEN = part(head_d, {'2': 'YOo'}, lw=1, dw=2, post=lambda g: head_p(g, True))
# 鋏角（前の 小さな はさみ。頭の 下に もぐる）
CLAW = ['.kkk..', 'kABk..', 'kBkkk.', 'kBBwk.', '.kkBk.', '..kwk.', '...k..']
# ---- 銅鏡の 甲羅（見せ所）：銅の ふち＋鏡の 面＋光の すじ＋鈕の 第三の 目 ----
def mirror(glow=False):
    cx, cy, rx, ry = 27, 32, 14.5, 13.5
    def d(g): E(g, cx, cy, rx, ry, '3')
    def p(g):
        for y in range(N):
            for x in range(N):
                if g[y][x] == '.': continue
                ex, ey = (x + .5 - cx) / rx, (y + .5 - cy) / ry; d_ = math.hypot(ex, ey); lit = -ex * .6 - ey * .8
                if d_ > .78:                                       # 銅の ふち（3段）
                    g[y][x] = 'Y' if lit > .3 else ('o' if lit < -.35 else 'O')
                elif d_ > .72: g[y][x] = 'o' if lit > 0 else 'Y'   # ふちの 内がわの 段
                else:                                              # 鏡の 面
                    t = ex + ey
                    g[y][x] = 'S' if abs(t + .55) < .1 or abs(t + .2) < .04 else ('C' if lit > -.15 else 'c')
                    if glow and d_ < .6 and (x + y) % 3 == 0: g[y][x] = 'V'
        # ふちの 模様（銅鏡の きざみ）
        for i in range(24):
            a = math.radians(i * 15); x, y = round(cx - .5 + rx * .87 * math.cos(a)), round(cy - .5 + ry * .87 * math.sin(a))
            dots(g, 'l' if i % 2 else 'Y', [(x, y)], 'YOo')
    return part(d, {}, post=p)
MIRROR = mirror(); MIRROR_GLOW = mirror(True)
# 鈕＝第三の 目（白い 光＋むらさきの 虹彩 明 V・暗 v＋たての ひとみ。まぶたの 銅の 輪で かこむ）
EYE3 = ['..kkkkk..', '.kOYYYOk.', 'kOkkkkkOk', 'kkwVVkVkk', 'kkVvvkvkk', 'kOkkkkkOk', '.kOooOok.', '..kkkkk..']
EYE3_ALT = {
    'blink': ['..kkkkk..', '.kOYYYOk.', 'kOYYYYYOk', 'kOkkkkkOk', 'kOOOOOOOk', 'kOoooooOk', '.kooooook.', '..kkkkk..'],
    'atk0|atk1|atk2': ['..kkkkk..', '.kOYYYOk.', 'kOkkkkkOk', 'kkwwVkVkk', 'kkVwVkvkk', 'kOkkkkkOk', '.kOooOok.', '..kkkkk..'],
    'hit': ['..kkkkk..', '.kOYYYOk.', 'kOkkkkkOk', 'kkkkkkkkk', 'kOOOkOOOk', 'kOkkkkkOk', '.kOooOok.', '..kkkkk..'],
    'ko': ['..kkkkk..', '.kOYYYOk.', 'kOkOOOkOk', 'kOOkOkOOk', 'kOOOkOOOk', 'kOOkOkOOk', '.kkoooOkk.', '..kkkkk..'],
}
# 顔の 目（白い 光＋むらさきの 虹彩＋ひとみ。銅の まゆ）
EYE = ['kkkk...', '.kkkkkk', '.kwVkVk', '..kvkvk', '...kkk.']
EYE_ALT = {
    'blink': ['kkkk...', '.kkkkkk', '..kkkkk'],
    'atk0|atk1|atk2': ['kkkkk..', '.kkkkkk', '.kwwVkk', '..kvkk.', '...kk..'],
    'hit': ['kk.....', '..kk...', '....kk.', '..kk...'],
    'ko': ['k...k', '.k.k.', '..k..', '.k.k.', 'k...k'],
}
# ---- 念力の 光線（鏡から 前へ。はなれた エフェクト＝意図的）----
BEAM = [
    '..............kk......kk',
    'kkkkkkkkkkkkkkVVk...kkVk',
    'VVVVVVVVVVVVVVVVVkkkVVVk',
    'wwwwwwwwwwwwwwwwwwVVwwwV',
    'wwwwwwwwwwwwwwwwwwwwwwwV',
    'VVVVVVVVVVVVVVVVVkkkVVVk',
    'kkkkkkkkkkkkkkVVk...kkVk',
    '..............kk......kk',
]
RING = ['..kkk..', '.kV.Vk.', 'kV...Vk', 'kV...Vk', '.kV.Vk.', '..kkk..']
SPARK = ['.k.', 'kwk', '.k.']

def layers():
    out = _layers()
    for d in out:
        if not d['n'].startswith('leg'): d['y'] += 3
    return out
def _layers():
    return [
        L('legB', 'legB', LEG_B),
        L('tail', 'tail', TAIL, alt={'idle1|idle2|walk1|walk3': TAIL2}),
        L('abd', 'body', ABD),
        H('claw', 'head', 48, 44, CLAW, not_='ko'),
        L('mirror', 'body', MIRROR, alt={'atk0|atk1|atk2': MIRROR_GLOW}),
        H('eye3', 'body', 23, 28, EYE3, alt=EYE3_ALT),
        H('spk', 'body', 17, 23, SPARK, only='idle1|idle2|walk1'),
        L('head', 'head', HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        H('eye', 'head', 43, 35, EYE, alt=EYE_ALT),
        L('legA', 'legA', LEG_A),
        H('beam', 'body', 38, 28, BEAM, only='atk1'),
        H('ring', 'body', 56, 29, RING, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'body': (0, -1), 'head': (0, -1)}, 'idle3': {'head': (0, 0)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)}, 'walk1': {'body': (0, -1), 'head': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)}, 'walk3': {'body': (0, -1), 'head': (0, -1)},
    'atk0': {'body': (-1, -1), 'head': (-1, 0), 'tail': (1, -1)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'root', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
