# コンペイトン（フェアリー・エスパー × 金平糖）手打ち GBA風：無機物＋かわいい ライン
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, poly, rot90
META = dict(id='kompeiton', name='コンペイトン', types=['fairy', 'psychic'], base='金平糖（お菓子）', size='S')
EYE_BOX = (26, 31, 14, 10)
PAL = {'k': '#1c1024', 'l': '#8a3470',
       'A': '#fff4f2', 'B': '#ffc4d8', 'C': '#f080b4', 'D': '#a8509e',   # 砂糖（ピンク、影は 紫へ）
       'w': '#ffffff', 'i': '#a070f0', 'e': '#3a1658',                 # 目（白・すみれ・こい紫）
       'r': '#ff5a7a',                                                 # ほっぺ・舌
       'y': '#fff07a', 's': '#ffb830',                                 # 星くず
       'p': '#c890ff'}                                                 # 念力の 波
LIGHT = set('ABwy')
KEEP_BLACK = set('wie')

def despeckle(g, keep='w'):
    # はぐれドットを まわりで いちばん 多い 色に（手で 消す かわり）
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c in '.' + keep: continue
            nb = [src[y + dy][x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx) and 0 <= y + dy < H and 0 <= x + dx < W]
            if c not in nb:
                cs = [n for n in nb if n != '.']
                if cs: g[y][x] = max(set(cs), key=cs.count)
    return g
def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch

# ---- 体：丸い 砂糖の 玉に とげとげ（角）。角ごとに 光の 向きで 3段＋白 ----
L = (-.58, -.6, .55)
def tone(nx, ny, wet=False):
    nz = math.sqrt(max(0, 1 - nx * nx - ny * ny)); d = nx * L[0] + ny * L[1] + nz * L[2]
    return 'A' if d > .86 else 'B' if d > .3 else 'C' if d > -.2 else 'D'
def candy():
    W = H = 32; g = grid(W, H); cx = cy = 16; R = 9.8; rb = 3.1
    angs = [math.radians(a) for a in range(-90, 270, 33)]
    bumps = [(cx + (R + 1.7) * math.cos(a), cy + (R + 1.7) * math.sin(a)) for a in angs]
    for y in range(H):
        for x in range(W):
            px, py = x + .5, y + .5; dc = math.hypot(px - cx, py - cy)
            own = None
            for bx, by in bumps:
                db = math.hypot(px - bx, py - by)
                if db <= rb and dc > R - 1.5:
                    own = ((px - bx) / rb * .75 + (px - cx) / R * .4, (py - by) / rb * .75 + (py - cy) / R * .4)
            if own is None and dc <= R: own = ((px - cx) / (R + 1), (py - cy) / (R + 1))
            if own: g[y][x] = tone(*own)
    despeckle(g)
    # 手打ちの 仕上げ：上と 左の 角に それぞれ つや（2ドット）、胴の 左上に 白い 三日月
    for bx, by in bumps:
        if bx + by < cx + cy - 6:
            X, Y = int(bx - .8), int(by - .9); put(g, [(X, Y), (X + 1, Y)], 'A')
    put(g, [(10, 9), (11, 9), (9, 10), (9, 11)], 'w')
    return outline(rows_of(g))

# ---- 顔：きらきらの 目（すみれ色の ひとみに 白い 光 2つ）＋ ほっぺ ----
EYE_N = ['.kkk.', 'kwwek', 'kweek', 'keeik', 'kiiwk', '.kkk.']
EYE_F = ['.kk.', 'kwek', 'keek', 'keik', '.kk.']
FACES = {
    'open':  (EYE_N, EYE_F, ['e.e', '.e.']),
    'blink': (['.....', '.....', '.....', 'k...k', '.kkk.', '.....'], ['....', '....', 'k..k', '.kk.', '....'], ['e.e', '.e.']),
    'fight': (['...kk', '.kk..', 'kwekk', 'keeik', 'kiiwk', '.kkk.'], ['kk..', '..kk', 'kwek', 'keik', '.kk.'], ['eee', '...']),
    'shout': (['...kk', '.kk..', 'kwekk', 'keeik', 'kiiwk', '.kkk.'], ['kk..', '..kk', 'kwek', 'keik', '.kk.'], ['.e.', 'ere', '.e.']),
    'pain':  (['.....', '...kk', '.kk..', 'k....', '.kk..', '...kk'], ['....', 'kk..', '..kk', '..kk', 'kk..'], ['.e.', 'e.e']),
    'ko':    (['k...k', '.k.k.', '..k..', '.k.k.', 'k...k', '.....'], ['k..k', '.kk.', '.kk.', 'k..k', '....'], ['eee']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(14, 10)
    for j, r in enumerate(ef):
        for i, c in enumerate(r):
            if c != '.': g[j + 1][i] = c
    for j, r in enumerate(en):
        for i, c in enumerate(r):
            if c != '.': g[j][8 + i] = c
    for j, r in enumerate(mo):
        for i, c in enumerate(r):
            if c != '.': g[6 + j][5 + i] = c
    if kind in ('open', 'blink', 'fight', 'shout'):
        put(g, [(0, 7), (1, 7)], 'r'); put(g, [(12, 7), (13, 7)], 'r')     # ほっぺ
    return [r.replace('k', 'e') for r in rows_of(g)]     # 顔の 線は こい紫（体の 線に まぎれない）

# ---- 星くず（フェアリー）：小さな 4方向の きらめき と 5つ角の 星 ----
TW = ['.y.', 'ywy', '.y.']
TW2 = ['..y..', '..y..', 'yywyy', '..y..', '..y..']
def star(r1=4.6, r2=2.0, n=11):
    g = grid(n, n); c = n / 2
    pts = [(c + (r1 if i % 2 == 0 else r2) * math.sin(math.pi * i / 5), c - (r1 if i % 2 == 0 else r2) * math.cos(math.pi * i / 5)) for i in range(10)]
    poly(g, pts, 'y')
    for y in range(n):
        for x in range(n):
            if g[y][x] == 'y' and (x + .5 - c) + (y + .5 - c) > 2.2: g[y][x] = 's'
    g[int(c) - 1][int(c) - 1] = 'w'
    return outline(rows_of(g))
# ---- 念力の 波（エスパー）：前へ ひろがる 弧 ----
def wave(r, h):
    g = grid(r + 1, 2 * h + 1)
    for y in range(2 * h + 1):
        t = (y - h) / h; x = int(round(r * (1 - .55 * t * t)))
        g[y][x] = 'p'
        if abs(t) < .7: g[y][x - 1] = 'p'
    return rows_of(g)
def aura():
    # ため：体の まわりに 紫の 点線の 輪（念力を ためる）
    W = H = 42; g = grid(W, H)
    for k in range(40):
        a = 2 * math.pi * k / 40
        if k % 4 == 3: continue
        x, y = int(21 + 20 * math.cos(a)), int(21 + 19 * math.sin(a))
        g[y][x] = 'p'
    return rows_of(g)
CHIP = ['.kk', 'kBk', 'kCk', '.k.']

NA = 'ko'
def layers():
    body = candy()
    return [
        dict(n='aura', g='root', x=7, y=10, rows=aura(), only='atk0'),
        dict(n='candy', g='body', x=14, y=18, rows=body, not_=NA),
        dict(n='face', g='face', x=26, y=31, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        # きらめき（はなれているのは 意図的な エフェクト）
        dict(n='tw1', g='fx', x=9, y=16, rows=TW, only='idle0|idle1|walk0|walk1|blink'),
        dict(n='tw2', g='fx', x=50, y=22, rows=TW2, only='idle0|idle1|walk2|walk3|blink'),
        dict(n='tw3', g='fx', x=48, y=13, rows=TW, only='idle2|idle3|walk0|walk1'),
        dict(n='tw4', g='fx', x=10, y=44, rows=TW2, only='idle2|idle3|walk2|walk3'),
        # 攻撃：念力の 波に のせて 星くずを 飛ばす
        dict(n='wave1', g='root', x=49, y=23, rows=wave(4, 11), only='atk1'),
        dict(n='star1', g='root', x=53, y=26, rows=star(6.6, 2.8, 15), only='atk1'),
        dict(n='twA', g='root', x=50, y=19, rows=TW2, only='atk1'),
        dict(n='twB', g='root', x=49, y=42, rows=TW, only='atk1'),
        dict(n='trA', g='root', x=46, y=33, rows=['y.y.s'], only='atk1'),
        dict(n='wave2', g='root', x=53, y=20, rows=wave(5, 14), only='atk2'),
        dict(n='star2', g='root', x=62, y=27, rows=star(5.6, 2.4, 13), only='atk2'),
        dict(n='twC', g='root', x=58, y=19, rows=TW2, only='atk2'),
        dict(n='twD', g='root', x=56, y=43, rows=TW, only='atk2'),
        dict(n='trB', g='root', x=50, y=33, rows=['y..y..s.s'], only='atk2'),
        # 被弾：砂糖の かけらが 飛ぶ
        dict(n='chip', g='root', x=50, y=21, rows=CHIP, only='hit'),
        dict(n='chip2', g='root', x=53, y=29, rows=CHIP[:3], only='hit'),
        # たおれ：ころんと 横に 転がって 地面に 落ちる
        dict(n='ko', g='root', x=14, y=27, rows=ko_body(), only='ko'),
        dict(n='kotw', g='root', x=44, y=24, rows=['.pp.', 'p..p', 'p.p.', '.p..'], only='ko'),
    ]

def ko_body():
    g = [list(r) for r in candy()]
    for j, r in enumerate(face('ko')):
        for i, c in enumerate(r):
            if c != '.': g[13 + j][9 + i] = c
    return rot90(rows_of(g))

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1), 'fx': (0, -1)}, 'idle2': {'body': (0, -2), 'fx': (0, 1)}, 'idle3': {'body': (0, -1)}, 'blink': {},
    'walk0': {'body': (1, -2), 'fx': (-1, 0)}, 'walk1': {'body': (1, -3), 'fx': (-1, 0)}, 'walk2': {'body': (1, -2), 'fx': (-2, 0)}, 'walk3': {'body': (1, -1), 'fx': (-2, 0)},
    'atk0': {'root': (-2, 1), 'body': (0, 1)}, 'atk1': {'root': (2, -1)}, 'atk2': {'root': (1, 0)},
    'hit': {'root': (-3, 1), 'face': (-1, 0)}, 'ko': {},
}
PARENT = {'face': 'body', 'body': 'root', 'fx': 'root'}
