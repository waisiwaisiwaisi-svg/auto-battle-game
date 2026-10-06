# サボトカゲ（くさ・じめん × トゲトカゲ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：サボテンの とげの 背中（体の とげ ⇔ サボテンの とげ）
EYE_BOX = (39, 28, 9, 7)
META = dict(id='sabotokage', name='サボトカゲ', types=['grass', 'ground'], base='トゲトカゲ', size='M')
PAL = {
    'k': '#101018', 'l': '#1e2c16',
    'A': '#b0e070', 'B': '#5c9e3e', 'D': '#2e5e2c',      # サボテン（みどり）
    'S': '#f2d898', 'T': '#c69a58', 'U': '#7a5630',      # 砂の 皮
    'R': '#ff5a6a', 'r': '#b01c3c', 'Y': '#ffe066', 'O': '#e0861e',   # 花・目
    'q': '#9a3e12',                                      # 目の 虹彩の 暗い 橙
    'w': '#ffffff',
}
LIGHT = set('ASYw')
KEEP_BLACK = set('wYO')
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
CA = {'1': 'ABD'}; SA = {'2': 'STU'}; SAD = {'2': 'TUU'}
def thorns(g, m, xs, ln=3):
    """とげ（マスクの 段階で 足す）：上の ふちから 外へ のびる 細い 三角。左の はしは 左上へ"""
    for x in xs:
        ys = [y for y in range(N) if g[y][x] == m]
        if not ys: continue
        y = ys[0]; dx = -1 if x < xs[len(xs) // 3] else (1 if x > xs[-len(xs) // 3] else 0)
        for i in range(1, ln + 1):
            dots(g, '3', [(x + dx * i, y - i)])
            if i == 1: dots(g, '3', [(x - 1, y), (x + 1, y)])
def spikes(g, pts, on):
    """とげ：ふちから 外へ 2ドット（白い 先）"""
    for (x, y, dx, dy) in pts:
        if at(g, x, y) in on:
            dots(g, 'T', [(x + dx, y + dy)]); dots(g, 'w', [(x + 2 * dx, y + 2 * dy), (x + 3 * dx, y + 3 * dy)])
# ---- しっぽ（太く 短い サボテンの 節）----
def tail_d(g):
    P(g, [(18, 42), (11, 40), (7, 35), (5, 37), (8, 43), (13, 48), (19, 50)], '1')
    thorns(g, '1', [7, 10, 14], 2)
def tail_p(g):
    spikes(g, [(7, 41, -1, 0), (10, 46, -1, 1)], 'ABD')
    Ln(g, 8, 38, 17, 45, 'D')
TAIL = part(tail_d, {'1': 'ABD', '3': 'wSS'}, post=tail_p)
# ---- 胴（小さく 丸い 砂の 腹）＋ 背中の サボテン（見せ所：たての すじ と とげ）----
def body_d(g):
    E(g, 26, 46, 10, 7, '2')
def body_p(g):
    for x in range(18, 36): dots(g, 'U', [(x, 52)], 'ST')
BODY = part(body_d, SA, dw=2, post=body_p)
def back_d(g):
    E(g, 26, 40, 12, 9, '1')
    for y in range(44, N):
        for x in range(N):
            if g[y][x] == '1' and y > 46: g[y][x] = '.'
    thorns(g, '1', [16, 20, 24, 28, 32, 36])
def back_p(g, flower=False):
    # サボテンの たての すじ（ふくらみ）
    for x0 in (19, 25, 31):
        for y in range(31, 47):
            x = x0 + (y - 39) // 6 * 0
            if at(g, x, y) in 'ABD': g[y][x] = 'D'
            if at(g, x - 1, y) in 'BD' and y < 40: g[y][x - 1] = 'A'
    # すじの 上の とげの つぶ（白）
    for x0 in (19, 25, 31):
        for y in range(34, 46, 5):
            dots(g, 'w', [(x0, y)], 'D'); dots(g, 'A', [(x0 - 1, y), (x0 + 1, y), (x0, y - 1)], 'ABD')
    # ふちの 大きな とげ（外へ）
    dots(g, 'D', [(x, 46) for x in range(14, 39)], 'AB')
BACK = part(back_d, {'1': 'ABD', '3': 'wSS'}, lw=2, dw=2, post=back_p)
# ---- 足（短く 太い。砂の 皮＋つめ）----
def leg(x, ramp, cut=True):
    def d(g): E(g, x + 3, 51, 4.5, 4, '2'); P(g, [(x + 1, 52), (x + 6, 52), (x + 6, 57), (x + 8, 58), (x + 8, 61), (x - 1, 61), (x, 58)], '2')
    def p(g): dots(g, 'w', [(x + 3, 60), (x + 6, 60), (x + 8, 60)]); dots(g, 'U', [(x + 2, 52), (x + 3, 52)])
    return part(d, {'2': ramp}, post=p, cut=((x - 1, 47, x + 7, 50),) if cut else ())
LEG_F = leg(33, 'STU'); LEG_H = leg(17, 'STU'); LEG_FF = leg(37, 'TUU', False); LEG_HF = leg(22, 'TUU', False)
# ---- 頭（大きく、目の 上に とげの 角。頭の 上は サボテン）----
def head_d(g):
    E(g, 42, 35, 11, 9.5, '2'); P(g, [(46, 29), (56, 33), (58, 38), (54, 42), (44, 44)], '2')
    E(g, 40, 29, 10, 5.5, '1')
    thorns(g, '1', [33, 38, 44], 3)
def head_p(g, open_=False):
    # 頭の サボテン部分の すじと とげ
    for x in (36, 42): Ln(g, x, 25, x + 1, 32, 'D')
    for x in (36, 42): dots(g, 'w', [(x, 27)]); dots(g, 'A', [(x - 1, 27), (x + 1, 27)], 'ABD')
    # ほおの いぼ（とげの 根）
    dots(g, 'T', [(37, 40), (39, 41), (35, 38)], 'S')
    if not open_:
        hand(g, 46, 38, ['kkkkkkkkkkkk', '.wk.wk.wk.wk'])
    else:
        hand(g, 45, 37, ['kkkkkkkkkkkk', 'kwkwkwkwkwk.', 'krrrrrrrrk..', 'kwkwkwkwk...', '.kkkkkkkk...'])
    dots(g, 'U', [(56, 35), (57, 36)], 'ST')          # 鼻の 穴
    for x in range(34, 52): dots(g, 'U', [(x, 44)], 'ST')
HEAD = part(head_d, {'1': 'ABD', '2': 'STU', '3': 'wSS'}, lw=1, dw=2, post=head_p)
HEAD_OPEN = part(head_d, {'1': 'ABD', '2': 'STU', '3': 'wSS'}, lw=1, dw=2, post=lambda g: head_p(g, True))
# 目の 上の 角（後ろへ 反る とげ）
HORN = ['kk.....', 'kwkk...', '.kATkk.', '..kATBk', '...kBDk', '....kk.']
# 頭の 赤い 花（サボテンの 花）
FLOWER = ['..kk.kk..', '.kRRkRRk.', 'kRRRkRRrk', 'kRRYYYRrk', '.kRYYYrk.', 'kRrRYrRrk', '.kkrrrkk.', '...kBk...', '...kDk...']
FLOWER2 = ['.........', '..kk.kk..', '.kRRkRRk.', 'kRRRYRRrk', 'kRRYYYrrk', '.krRYrRk.', '..kkrkk..', '...kBk...', '...kDk...']
# ---- 目：爬虫類の つり目（A）。丸みの ある 大きめの トカゲの 目。2段の 太い 上まぶた（k＋サボテンの 影 D）、細い 下まぶた。
#      白目なし、橙の 虹彩（上 Y → O → 下 q）を 長い たての スリットが 上から 下まで 割る ----
EYE = ['.kkkkkkk.', 'kDDDDDDkk', 'kkwYYkYYk', 'kYOOOkOOk', 'kOOqqkqOk', '.kqqqkqk.', '..kkkkk..']
EYE_ALT = {
    'blink': ['.kkkkkkk.', 'kDDDDDDkk', 'kDDDDDDDk', 'kDDDDDDDk', 'kkkkkkkkk', '.kTTTTTk.', '..kkkkk..'],
    'atk0|atk1|atk2': ['.kkkkkkk.', 'kkYYYkYkk', 'kYYYYkYYk', 'kYOOOkOOk', 'kOOOqkqOk', '.kqqqkqk.', '..kkkkk..'],
    'hit': ['.kkkkkkk.', 'kDDDDDDkk', 'kDDDDDDDk', 'kkkkkkkkk', 'kOOkkkkOk', '.kkqqqkk.', '..kkkkk..'],
    'ko': ['.kkkkkkk.', 'kDDDDDDkk', 'kkYYYYYkk', 'kOkOOOkOk', 'kOOkOkOOk', '.kqqkqqk.', '..kkkkk..'],
}
# ---- 攻撃：背中の とげを 前へ 飛ばす（はなれた エフェクト＝意図的）----
NEEDLES = ['kkkk.......', 'TTTwwk.....', 'kkkk..kkkk.', '......TTTww', '..kkkkkkkk.', '..TTTTTwwk.', '..kkkk.....']
DUST = ['..k.k.', '.kTkUk', 'kTSTk.', '.kkk..']

def layers():
    return [
        L('legHF', 'legB', LEG_HF),
        L('legFF', 'legA', LEG_FF),
        L('tail', 'tail', TAIL),
        L('body', 'body', BODY),
        L('back', 'body', BACK),
        L('legH', 'legA', LEG_H),
        L('legF', 'legB', LEG_F),
        H('flower', 'head', 35, 16, FLOWER, alt={'idle1|idle2|walk1|walk3': FLOWER2}),
        L('head', 'head', HEAD, alt={'atk1|atk2': HEAD_OPEN}),
        H('horn', 'head', 31, 25, HORN),
        H('eye', 'head', 39, 28, EYE, alt=EYE_ALT),
        H('ndl', 'root', 60, 29, NEEDLES, only='atk1'),
        H('dust', 'root', 6, 56, DUST, only='atk0'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'head': (0, 1)}, 'idle3': {'head': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'head': (0, -1)}, 'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'head': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-2, 2), 'tail': (0, -1)}, 'atk1': {'root': (4, 0), 'head': (1, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'head': (-2, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
