# マツボリン（くさ・はがね × センザンコウ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：松ぼっくりの 形に 重なる 鉄の うろこ（丸まると 鉄の 松ぼっくり）
META = dict(id='matsuborin', name='マツボリン', types=['grass', 'steel'], base='センザンコウ', size='M')
PAL = {
    'k': '#101018', 'l': '#1c2232',
    'S': '#dce6f2', 'T': '#8c9ab6', 'U': '#4a5572',      # 鉄の うろこ
    'P': '#d0904c', 'p': '#7a4826',                      # 松の 木の 色（うろこの ふち）
    'F': '#ecbe96', 'G': '#b27c5a', 'H': '#6a4434',      # 顔・足の 皮
    'A': '#9ad866', 'B': '#3a7c3a',                      # 松葉
    'Y': '#ffd23c', 'O': '#e0601c',                      # 目
    'w': '#ffffff',
}
LIGHT = set('SPFAYw')
KEEP_BLACK = set('wY')
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
# 鱗片 1まい（手打ち）：上が 光、右下が 影、下の ふちは 木の 色の 線、先は 明るい 木の 色
TILE = ['TSSSTTT', 'SSSTTTU', 'STTTTUU', 'pTTTUUp', '.pTUUp.', '..pPp..']
TILE_S = ['SSSSTT', 'SSTTTU', 'pTTTUp', '.pPPp.']
def scales(g, on='STU', tile=TILE, dx=6, dy=4, ox=0, oy=0):
    """松ぼっくりの 鱗片：屋根がわらの ように 下の 段から 上へ 重ねる（上の 板の ふちが 下の 板に かぶさる）"""
    src = [r[:] for r in g]; DK = {'S': 'T', 'T': 'U', 'U': 'U', 'P': 'p', 'p': 'p'}
    ys = [y for y in range(N) if any(c in on for c in src[y])]
    if not ys: return
    rows = list(range(ys[0] - len(tile) + oy, ys[-1] + 1, dy))
    for r_i, y0 in reversed(list(enumerate(rows))):
        for x0 in range(-dx + ox + (r_i % 2) * (dx // 2), N, dx):
            for j, line_ in enumerate(tile):
                for i, c in enumerate(line_):
                    x, y = x0 + i, y0 + j
                    if c == '.' or not (0 <= x < N and 0 <= y < N) or src[y][x] not in on: continue
                    g[y][x] = DK[c] if src[y][x] == 'U' else c
ST = {'1': 'STU'}; SK = {'2': 'FGH'}; SKD = {'2': 'GHH'}
# ---- しっぽ（太い 鱗の 尾。先に 松葉）----
def tail_d(g):
    P(g, [(19, 40), (13, 38), (8, 41), (5, 47), (7, 53), (10, 50), (13, 46), (19, 50)], '1')
TAIL = part(tail_d, ST, dw=2, post=lambda g: scales(g, tile=TILE_S, dx=5, dy=3))
# ---- 胴＝松ぼっくりの ドーム（鉄の 鱗片）----
def body_d(g):
    E(g, 27, 42, 12, 11.5, '1'); P(g, [(20, 34), (26, 27), (33, 33)], '1')
    for y in range(50, N):
        for x in range(N):
            if g[y][x] == '1': g[y][x] = '2'
def body_p(g):
    scales(g, ox=2, oy=1)
    for x in range(14, 41): dots(g, 'H', [(x, 53)], 'FG')
BODY = part(body_d, {'1': 'STU', '2': 'FGH'}, lw=2, dw=3, post=body_p)
# 背中の 松葉の たてがみ
NEEDLE = ['..k...k...', '.kAk.kAk.k', '.kAkkABkkA', 'kABkABkAB.', '.kBBBBBBk.']
NEEDLE2 = ['...k...k..', '..kAk.kAkk', '.kABkkABkA', 'kABkABkAB.', '.kBBBBBBk.']
# ---- 足（短く 太い。大きな 爪）----
def leg(x, ramp, cut=True):
    def d(g): E(g, x + 3, 51, 4.5, 4, '2'); P(g, [(x + 1, 52), (x + 6, 52), (x + 6, 57), (x + 8, 58), (x + 8, 61), (x - 1, 61), (x, 58)], '2')
    def p(g):
        hand(g, x + 5, 57, ['.w.', 'wTw', 'wT.', '.T.'] if ramp[0] == 'F' else ['.T.', 'TUT', 'TU.', '.U.'])
        dots(g, 'w' if ramp[0] == 'F' else 'T', [(x + 1, 60), (x + 3, 60)])
    return part(d, {'2': ramp}, post=p, cut=((x - 1, 47, x + 7, 50),) if cut else ())
LEG_F = leg(35, 'FGH'); LEG_H = leg(17, 'FGH'); LEG_FF = leg(39, 'GHH', False); LEG_HF = leg(22, 'GHH', False)
# ---- 頭（顔は 皮、頭の 上と 後ろは 鉄の 鱗。とがった 鼻先と 牙）----
def head_d(g):
    E(g, 43, 36, 10, 9, '2'); P(g, [(48, 33), (57, 37), (58, 40), (52, 43), (45, 44)], '2')
    P(g, [(33, 34), (35, 28), (40, 26), (47, 27), (51, 31), (46, 31), (40, 33), (36, 38)], '1')
def head_p(g, open_=False):
    scales(g, tile=TILE_S, dx=5, dy=3, ox=1)
    if not open_:
        hand(g, 46, 40, ['kkkkkkkkkkk', '.wkwk..wkk.', '..w.........'])
    else:
        hand(g, 45, 39, ['kkkkkkkkkkkk', 'kwkwkwkwkk..', 'kHHHHHHHk...', '.kwkwkwk....'])
    dots(g, 'H', [(57, 38), (56, 37)], 'FG')
    for x in range(36, 52): dots(g, 'H', [(x, 45)], 'FG')
HEAD = part(head_d, {'1': 'STU', '2': 'FGH'}, lw=1, dw=2, post=head_p)
HEAD_OPEN = part(head_d, {'1': 'STU', '2': 'FGH'}, lw=1, dw=2, post=lambda g: head_p(g, True))
# ---- 目：白い 光＋金の 虹彩（明 Y・暗 O）＋ひとみ。鉄の ひさしの 下 ----
EYE = ['kkkkk...', '.kkkkkk.', '.kwYYkYk', '..kOOkOk', '...kkkk.']
EYE_ALT = {
    'blink': ['kkkkk...', '.kkkkkk.', '..kkkkkk'],
    'atk0': ['kkkkkk..', '.kkkkkkk', '.kwwYkYk', '..kOOkk.', '...kkk..'],
    'hit': ['kkk.....', '..kk....', '....kkk.', '..kk....'],
    'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
}
# ---- 攻撃：丸まって 鉄の 松ぼっくりに なり 転がる ----
def ball_d(g):
    P(g, [(31, 31), (40, 34), (46, 41), (48, 50), (43, 58), (34, 61), (24, 60), (16, 54), (15, 45), (20, 36)], '1')
def ball_p(g, ph=0):
    scales(g, ox=ph, oy=ph // 2)
    hand(g, 26, 29, NEEDLE)
BALL = part(ball_d, ST, lw=2, dw=3, post=ball_p)
BALL2 = part(ball_d, ST, lw=2, dw=3, post=lambda g: ball_p(g, 3))
DUST = ['...k.k..', '..kGkHk.', '.kGFGk..', 'kGHk....', '.kk.....']

NB = 'atk1|atk2'
def layers():
    return [
        L('legHF', 'legB', LEG_HF, not_=NB),
        L('legFF', 'legA', LEG_FF, not_=NB),
        L('tail', 'tail', TAIL, not_=NB),
        H('needle', 'body', 21, 23, NEEDLE, alt={'idle1|idle3|walk1|walk3': NEEDLE2}, not_=NB),
        L('body', 'body', BODY, not_=NB),
        L('legH', 'legA', LEG_H, not_=NB),
        L('legF', 'legB', LEG_F, not_=NB),
        L('head', 'head', HEAD, not_=NB),
        H('eye', 'head', 40, 30, EYE, alt=EYE_ALT, not_=NB),
        L('ball', 'root', BALL, alt={'atk2': BALL2}, only=NB),
        H('dust', 'root', 10, 56, DUST, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 2), 'head': (-2, 2), 'tail': (1, 0)}, 'atk1': {'root': (6, -1)}, 'atk2': {'root': (12, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
