# ジョウロン（くさ・ノーマル × じょうろ）手打ち GBA風：無機物＋かわいい ライン
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, line, rot90
META = dict(id='jouron', name='ジョウロン', types=['grass', 'normal'], base='じょうろ', size='S')
EYE_BOX = (21, 39, 15, 15)
PAL = {'k': '#1a1216', 'l': '#6a2a24',
       'A': '#ffd2a0', 'B': '#e48a52', 'C': '#a84a3c', 'w': '#fff8ea',   # 銅（明るい 方は 黄、影は 赤紫へ）
       'G': '#c8f070', 'g': '#5cbc44', 'd': '#23784c',                   # 芽（黄緑〜青緑）
       'u': '#d4f4ff', 'v': '#4aa6ec',                                   # 水
       'r': '#ff7a7a', 'e': '#2a1214'}                                   # ほっぺ・顔の 線
LIGHT = set('AwGu')
KEEP_BLACK = set('wgdre')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def stamp(g, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c

# ---- 胴：銅の つつ（3/4 で 上の 口が だ円に 見える）。縦の 帯で 円柱の 陰影 ----
BW, BH = 25, 23
def can_body():
    g = grid(BW, BH)
    for y in range(BH):
        for x in range(BW):
            inside = True
            if y >= BH - 3:                       # 下の 角を 丸く
                k = y - (BH - 3)
                if x < [0, 1, 2][k] or x > BW - 1 - [0, 1, 2][k]: inside = False
            if inside:
                t = x / (BW - 1)
                g[y][x] = 'A' if t < .2 else 'B' if t < .64 else 'C'
    for y in range(4): g[y] = ['.'] * BW
    ellipse(g, BW / 2, 3.6, BW / 2, 3.6, 'A')                       # 上の ふち（明）
    ellipse(g, BW / 2 + .4, 3.4, BW / 2 - 2.6, 2.1, 'l')            # 口の 中（暗い 穴）
    for x in range(8, BW - 3):
        if g[4][x] == 'l': g[4][x] = 'C'                            # 穴の 手前は 少し 明るい
    for x in range(BW):                                             # ふちの 下の 段（巻きの つなぎ目）
        if g[7][x] != '.': g[7][x] = 'C' if x > 3 else 'B'
    for x in range(BW):                                             # すその 巻き（足の うしろ）
        if g[BH - 3][x] != '.': g[BH - 3][x] = 'C' if x > 4 else 'B'
    for y in range(7, BH - 6):                                      # 金属の つや（縦の 白い すじ）
        put(g, [(2, y)], 'w')
    put(g, [(3, 8), (3, 9)], 'w')
    return outline(rows_of(g))

# ---- 取っ手：うしろの 弓なりの 輪 ----
def handle():
    g = grid(12, 20)
    for y in range(20):
        for x in range(12):
            d = ((x - 11.5) / 11) ** 2 + ((y - 10) / 9.6) ** 2
            if .6 <= d <= 1.0: g[y][x] = 'B'
    for y in range(20):
        for x in range(12):
            if g[y][x] == 'B' and (x == 0 or g[y][x - 1] == '.' or y == 0 or g[y - 1][x] == '.'): g[y][x] = 'A'
            elif g[y][x] == 'B' and (y < 19 and g[y + 1][x] == '.'): g[y][x] = 'C'
    return outline(rows_of(g))

# ---- 注ぎ口（＝鼻）：顔の まん中から 右上へ 細くなる 管。先に はす口 ----
def spout():
    W, H = 27, 14; g = grid(W, H); y0 = 9.6
    yc = lambda i: y0 - max(0, i - 8) * .62
    for i in range(2, 21):
        ht = 1.9 - i * .03
        for y in range(H):
            d = y + .5 - yc(i)
            if abs(d) <= ht: g[y][i] = 'A' if d < -ht * .35 else 'B' if d < ht * .45 else 'C'
    # 付け根の まるい つば（鼻の あたま）
    for y in range(H):
        for x in range(7):
            dx, dy = (x + .5 - 3) / 3, (y + .5 - y0) / 3.1
            if dx * dx + dy * dy <= 1: g[y][x] = 'A' if dx + dy < -.55 else 'B' if dx + dy < .45 else 'C'
    # はす口：右上へ 開いた ラッパ形
    hx, hy = 22.4, 2.8
    for y in range(H):
        for x in range(18, W):
            if ((x + .5 - hx) / 3.2) ** 2 + ((y + .5 - hy) / 2.8) ** 2 <= 1 and x - 18.5 >= abs(y + .5 - hy) * .7 - .6:
                g[y][x] = 'A' if x < 22 else 'B' if x < 24 else 'C'
    put(g, [(24, 1), (24, 3), (23, 2)], 'v')
    return outline(rows_of(g))
# ---- 芽：口から 出た 双葉。phase で ゆれる ----
def sprout(phase=0, droop=False):
    g = grid(16, 15)
    if droop:
        stamp(g, ['..ddd...', '.dggd...', 'dgGgd...', 'dgggd.d.', '.ddd.dgd', '....dggd', '.....dd.'], 4, 4)
        put(g, [(7, y) for y in range(9, 15)], 'g')
        return outline(rows_of(g))
    s = phase - 1
    put(g, [(7, y) for y in range(6, 15)], 'g')
    put(g, [(8, y) for y in range(7, 15)], 'd')
    stamp(g, ['..GGG.', '.GGgg.', 'GGggd.', '.ggdd.', '...dd.'], 2 + s, 2 + (1 if s < 0 else 0))   # 左の 葉
    stamp(g, ['.GGg..', 'Gggdd.', 'gggdd.', '.gdd..'], 8 + s, 3 + (1 if s > 0 else 0))        # 右の 葉
    put(g, [(7, 5)], 'G')
    return outline(rows_of(g))

# ---- 顔：ぬりの 目（白い 光＋緑の ひとみ 2段）＋ ほっぺ ＋ 口 ----
EYE_N = ['.ee.', 'ewde', 'ewde', 'egde', 'egge', '.ee.']
EYE_F = ['.e.', 'ewe', 'ede', 'ege', '.e.']
FACES = {
    'open':  (EYE_N, EYE_F, ['e...e', '.eee.']),
    'blink': (['....', '....', '....', 'e..e', '.ee.', '....'], ['...', '...', 'e.e', '.e.', '...'], ['e...e', '.eee.']),
    'fight': (['...e', '.ee.', 'ewde', 'egde', 'egge', '.ee.'], ['e..', '.e.', 'ewe', 'ege', '.e.'], ['.eee.', '.....']),
    'shout': (['...e', '.ee.', 'ewde', 'egde', 'egge', '.ee.'], ['e..', '.e.', 'ewe', 'ege', '.e.'], ['.eee.', '.ere.']),
    'pain':  (['....', '...e', '.ee.', 'e...', '.ee.', '...e'], ['...', 'e..', '.ee', 'e..', '...'], ['.e.e.', 'e.e.e']),
    'ko':    (['....', 'e..e', '.ee.', '.ee.', 'e..e', '....'], ['...', 'e.e', '.e.', 'e.e', '...'], ['.eee.']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(15, 15)
    stamp(g, ef, 1, 1); stamp(g, en, 10, 0); stamp(g, mo, 3, 13)
    if kind in ('open', 'blink'): put(g, [(0, 6), (1, 6)], 'r')
    return rows_of(g)

FOOT = ['kkkkk', 'kBBCk', 'kCCCk', '.kkk.']
# ---- 水しぶき（攻撃）と 水たまり（ダウン）----
SPRAY1 = ['......u.......', '..u.....v.....', '.....v....u...', 'u..v...u...v..', '..u...v..u...v', '.v..u....v....', '....v..u....u.', '.......v......']
SPRAY2 = ['.........u.....', '....u......v...', '.u....v.......u', '...v....u..v...', '......v....u...', '..u.......v....', '.....v.u.....v.', '...........u...', '........v......']
LEAF = ['.kk.', 'kGgk', 'kgdk', '.kk.']
BUD = ['.k.k.', 'kGkgk', '.kgk.', '..k..']
DROP = ['.k.', 'kuk', 'kvk', '.k.']
PUDDLE = ['.kkkkkkkk.', 'kuuvvvvvvk', '.kkkkkkkk.']

NA = 'ko'
def layers():
    return [
        dict(n='handle', g='body', x=5, y=32, rows=handle(), not_=NA),
        dict(n='footB', g='legB', x=31, y=55, rows=FOOT, not_=NA),
        dict(n='footA', g='legA', x=17, y=55, rows=FOOT, not_=NA),
        dict(n='can', g='body', x=13, y=33, rows=can_body(), not_=NA),
        dict(n='sprout', g='top', x=13, y=23, rows=sprout(1), alt={'idle1|idle2|walk1|walk3': sprout(2), 'atk0|hit': sprout(0), 'atk1|atk2': sprout(2)}, not_=NA),
        dict(n='face', g='face', x=21, y=39, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='spout', g='nose', x=22, y=38, rows=spout(), not_=NA),
        # 攻撃：はす口から 水を まき、種が 芽を 出す（はなれているのは 意図的な エフェクト）
        dict(n='spray1', g='root', x=52, y=35, rows=SPRAY1, only='atk1'),
        dict(n='leaf1', g='root', x=58, y=31, rows=LEAF, only='atk1'),
        dict(n='spray2', g='root', x=53, y=39, rows=SPRAY2, only='atk2'),
        dict(n='bud1', g='root', x=60, y=54, rows=BUD, only='atk2'),
        dict(n='bud2', g='root', x=66, y=55, rows=BUD, only='atk2'),
        dict(n='drop', g='root', x=10, y=27, rows=DROP, only='hit'),
        dict(n='drop2', g='root', x=31, y=24, rows=DROP, only='hit'),
        # たおれ：あおむけに ころがり、水が こぼれる
        dict(n='puddle', g='root', x=10, y=57, rows=PUDDLE, only='ko'),
        dict(n='ko', g='root', x=18, y=15, rows=ko_body(), only='ko'),
    ]

def ko_body():
    # 立ち姿を 組んで 左へ 90度（反時計回り）回す：あおむけ、注ぎ口が 上を 向く
    W, H = 52, 40; g = grid(W, H); ox, oy = 5, 23
    for rows, x, y in ((handle(), 5, 32), (sprout(droop=True), 13, 23), (FOOT, 31, 55), (FOOT, 17, 55), (can_body(), 13, 33), (face('ko'), 21, 39), (spout(), 22, 38)):
        stamp(g, rows, x - ox, y - oy)
    rows = rot90(rot90(rot90(rows_of(g))))
    ys = [y for y, r in enumerate(rows) if r.strip('.')]; xs = [x for x in range(len(rows[0])) if any(r[x] != '.' for r in rows)]
    return [r[xs[0]:xs[-1] + 1] for r in rows[ys[0]:ys[-1] + 1]]

FRAMES = {
    'idle0': {}, 'idle1': {'top': (0, -1)}, 'idle2': {'body': (0, 1), 'face': (0, 0)}, 'idle3': {}, 'blink': {},
    'walk0': {'body': (0, -2), 'legA': (0, -1)}, 'walk1': {'body': (0, -1)}, 'walk2': {'body': (0, -2), 'legB': (0, -1)}, 'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'nose': (0, -1)}, 'atk1': {'root': (2, 0), 'nose': (1, 1)}, 'atk2': {'root': (1, 0), 'nose': (1, 1)},
    'hit': {'root': (-3, 0), 'body': (0, 1)}, 'ko': {},
}
PARENT = {'top': 'body', 'face': 'body', 'nose': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
