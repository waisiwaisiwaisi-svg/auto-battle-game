# デンタマ（でんき・エスパー × 電球）手打ち GBA風：無機物＋かわいい ライン
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, poly, rot90, recolor
META = dict(id='dentama', name='デンタマ', types=['elec', 'psychic'], base='電球', size='S')
EYE_BOX = (26, 24, 15, 10)
PAL = {'k': '#18121c', 'l': '#7a4a1c',
       'g': '#fffef0', 'h': '#fff0a4', 'j': '#e6b450',                  # ともった ガラス（白〜黄〜こがね）
       'A': '#eef2ff', 'B': '#a4aecc', 'C': '#586084',                  # 口金（銀、影は 青むらさき）／消えた ガラス
       'n': '#7a2c10', 'o': '#ff8a1c', 'y': '#ffe03a', 'w': '#ffffff',  # フィラメント（線・赤橙・黄・白）
       'r': '#ff8aa0', 'p': '#c47cff', 's': '#9c98b0'}                  # ほっぺ・念力・けむり
LIGHT = set('gAwy')
KEEP_BLACK = set('wnoy')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def stamp(g, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c
def despeckle(g, keep='w'):
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

# ---- ガラスの 玉：まるい 頭 ＋ すぼまる 首。光は 左上、右下の ふちが こがね色 ----
GW, GH = 27, 28
def glass(lit=True, flash=False):
    g = grid(GW, GH); cx, cy, R = 13.5, 12.5, 12.6
    poly(g, [(7, 20), (20, 20), (18.5, 27), (8.5, 27)], 'h')
    for y in range(GH):
        for x in range(GW):
            px, py = x + .5, y + .5
            d = math.hypot(px - cx, py - cy) / R
            if d <= 1 or g[y][x] == 'h':
                nx, ny = (px - cx) / R, (py - cy) / R
                t = nx * .62 + ny * .78 if d <= 1 else (px - 13.5) / 6 + .2
                g[y][x] = 'g' if t < -.62 else 'h' if t < .48 else 'j'
    # フィラメントの まわりが いちばん 明るい（顔の うしろの 光）
    for y in range(GH):
        for x in range(GW):
            d = ((x + .5 - 15.5) / 8.2) ** 2 + ((y + .5 - 13) / 6.8) ** 2
            if d <= 1 and g[y][x] != '.': g[y][x] = 'g' if d < .62 else ('h' if g[y][x] == 'j' else g[y][x])
    despeckle(g)
    # つや：左上の 白い 弧（手打ち）
    put(g, [(6, 5), (5, 6), (4, 7), (4, 8), (3, 9), (3, 10), (7, 4), (8, 4)], 'w')
    put(g, [(5, 12), (5, 13)], 'g')
    # ガラスの 中の 支え（ステム）：首の 中に 小さな 台
    stamp(g, ['..j..', '.jhj.', '.jhj.', 'jhhhj'], 11, 21)
    if not lit: g = [[{'g': 'B', 'h': 'B', 'j': 'C', 'w': 'A'}.get(c, c) for c in r] for r in g]
    if flash: g = [[{'h': 'g', 'j': 'h'}.get(c, c) for c in r] for r in g]     # ぴかっ！
    return outline(rows_of(g))

# ---- 口金：ねじの 山（ななめの 帯）と 先の 接点 ----
def base():
    # ねじの 山：3本の 帯（明るい 山・中・暗い みぞ）が 右へ 1ドット 下がる
    W, H = 13, 9; g = grid(W, H)
    for y in range(H):
        for x in range(W):
            if y >= 7 and (x < 2 + (y - 7) * 2 or x > W - 3 - (y - 7) * 2): continue
            ramp = 'ABC' if x < 3 else 'BBC' if x < 9 else 'BCC'
            ph = (y - (1 if x >= 7 else 0)) % 3                 # 0=山の 上 1=山 2=みぞ
            g[y][x] = ramp[0] if ph == 0 else ramp[1] if ph == 1 else 'C'
            if y >= 7: g[y][x] = 'C' if x > 4 else 'B'
    return outline(rows_of(g))
TIP = ['.kkk.', 'knnnk', '.kkk.']

# ---- 顔：フィラメントの 目（光る 輪の 中に こげ茶の ひとみ）＋ 光る 線の 口 ----
EYE_N = ['.nnnn.', 'nwwyyn', 'nwynnn', 'nyynnn', 'noyyon', '.nnnn.']
EYE_F = ['.nn.', 'nwyn', 'nynn', 'noyn', '.nn.']
FACES = {
    'open':  (EYE_N, EYE_F, ['o...o', '.oyo.']),
    'blink': (['......', '......', '......', 'n....n', '.nnnn.', '......'], ['....', '....', 'n..n', '.nn.', '....'], ['o...o', '.oyo.']),
    'fight': (['nn....', '.nnn..', 'nwynnn', 'nyynnn', 'noyyon', '.nnnn.'], ['..nn', '.nn.', 'nynn', 'noyn', '.nn.'], ['.....', 'ooooo']),
    'shout': (['nn....', '.nnn..', 'nwynnn', 'nyynnn', 'noyyon', '.nnnn.'], ['..nn', '.nn.', 'nynn', 'noyn', '.nn.'], ['.ooo.', 'oyyyo', '.ooo.']),
    'pain':  (['......', 'nn....', '..nn..', '....n.', '..nn..', 'nn....'], ['....', '...n', '.nn.', 'n...', '.nn.'], ['.o.o.', 'o.o.o']),
    'ko':    (['......', 'n...n.', '.n.n..', '..n...', '.n.n..', 'n...n.'], ['....', 'n..n', '.nn.', '.nn.', 'n..n'], ['nnnnn']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(15, 15)
    stamp(g, ef, 0, 1); stamp(g, en, 8, 0); stamp(g, mo, 4, 7)
    # 導線：口（フィラメント）の 両はしから ステムへ おりる 2本の 線
    put(g, [(4, 9), (4, 10), (5, 11), (5, 12), (6, 13), (6, 14)], 'B')
    put(g, [(8, 9), (8, 10), (8, 11), (7, 12), (7, 13), (7, 14)], 'B')
    if kind in ('open', 'blink'): put(g, [(1, 6), (2, 6)], 'r'); put(g, [(13, 7), (14, 7)], 'r')
    return rows_of(g)

# ---- 電気（でんき）：ジグザグの 火花、念力（エスパー）：むらさきの 輪 ----
SPARK1 = ['.y..', '..y.', '.y..', 'y...']
SPARK2 = ['..y', '.y.', 'yw.', '.y.']
BOLT = ['.....kkkk', '....kwyyk', '...kwyyk.', '..kwyyk..', '.kwyyykkk', 'kyyyyyyyk', 'kkkkyyyk.', '...kyyk..', '..kyyk...', '..kyk....', '.kyk.....', '.kk......']
BOLTS = ['...kkk', '..kyyk', '.kyyk.', 'kyyykk', 'kkyyyk', '.kyyk.', '.kyk..', 'kk....']
def rays(r1, r2, n=8):
    W = H = 2 * r2 + 3; g = grid(W, H); c = W // 2
    for k in range(n):
        a = 2 * math.pi * k / n + .2
        for t in range(r1, r2 + 1):
            x, y = int(round(c + t * math.cos(a))), int(round(c + t * math.sin(a)))
            g[y][x] = 'y' if t < r2 else 'w'
    return rows_of(g)
def ring(r):
    W = H = 2 * r + 3; g = grid(W, H); c = W / 2
    for k in range(64):
        a = 2 * math.pi * k / 64
        if k % 8 in (3, 4): continue
        g[int(c + r * math.sin(a))][int(c + r * math.cos(a))] = 'p'
    return rows_of(g)
SMOKE = ['..ss.', '.s..s', '.s...', '..ss.', '....s', '...s.']

NA = 'ko'
def layers():
    return [
        dict(n='ring', g='root', x=12, y=10, rows=ring(19), only='atk0'),
        dict(n='rays', g='root', x=8, y=6, rows=rays(16, 19, 12), only='atk1'),
        dict(n='base', g='body', x=25, y=42, rows=base(), not_=NA),
        dict(n='tip', g='body', x=29, y=52, rows=TIP, not_=NA),
        dict(n='glass', g='body', x=17, y=15, rows=glass(), alt={'atk1': glass(flash=True)}, not_=NA),
        dict(n='face', g='face', x=26, y=24, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        # 火花（はなれているのは 意図的な エフェクト）
        dict(n='sp1', g='fx', x=46, y=20, rows=SPARK1, only='idle0|idle1|blink|walk0|walk1'),
        dict(n='sp2', g='fx', x=14, y=36, rows=SPARK2, only='idle0|idle1|blink|walk2|walk3'),
        dict(n='sp3', g='fx', x=15, y=14, rows=SPARK1, only='idle2|idle3|walk2|walk3'),
        dict(n='sp4', g='fx', x=45, y=38, rows=['.p.', 'pwp', '.p.'], only='idle2|idle3|walk0|walk1'),
        dict(n='spk', g='fx', x=30, y=56, rows=['y.y', '.y.'], not_='ko|hit'),
        # 攻撃：ぴかっと 光って いなずまを 飛ばす
        dict(n='bolt1', g='root', x=49, y=22, rows=BOLT, only='atk1'),
        dict(n='bolt2', g='root', x=57, y=24, rows=BOLT, only='atk2'),
        dict(n='bolt2b', g='root', x=50, y=32, rows=BOLTS, only='atk2'),
        dict(n='pw', g='root', x=47, y=19, rows=['..p', '.p.', 'p..', 'p..', 'p..', '.p.', '..p'], only='atk2'),
        dict(n='hitsp', g='root', x=46, y=18, rows=SPARK2, only='hit'),
        # たおれ：横だおし、光が 消えて けむり
        dict(n='ko', g='root', x=13, y=34, rows=ko_body(), only='ko'),
        dict(n='smoke', g='root', x=49, y=31, rows=SMOKE, only='ko'),
    ]

def ko_body():
    W, H = 30, 44; g = grid(W, H)
    stamp(g, glass(False), 0, 0); stamp(g, face('ko'), 7, 11); stamp(g, base(), 8, 27); stamp(g, TIP, 12, 37)
    rows = rot90(rows_of(g))
    return [r.rstrip('.') for r in rows if r.strip('.')]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1), 'fx': (0, -1)}, 'idle2': {'body': (0, -2), 'fx': (1, 0)}, 'idle3': {'body': (0, -1)}, 'blink': {},
    'walk0': {'body': (1, -2)}, 'walk1': {'body': (1, -3)}, 'walk2': {'body': (1, -2)}, 'walk3': {'body': (1, -1)},
    'atk0': {'root': (-2, 1)}, 'atk1': {'root': (2, -1)}, 'atk2': {'root': (1, 0)},
    'hit': {'root': (-3, 1), 'face': (-1, 0)}, 'ko': {},
}
PARENT = {'face': 'body', 'body': 'root', 'fx': 'root'}
