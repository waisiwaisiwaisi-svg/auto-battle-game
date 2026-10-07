# クルリン（かぜ・フェアリー × 紙の 風車）手打ち GBA風：無機物＋かわいい
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, rot90
META = dict(id='kururin', name='クルリン', types=['wind', 'fairy'], base='風車（おもちゃ）', size='S')
EYE_BOX = (27, 28, 11, 5)
PAL = {'k': '#16121e', 'l': '#5a2a5a',
       'a': '#ffb4c8', 'b': '#f05a86', 'c': '#a8285e',          # もも色の 紙
       'd': '#b8f4ff', 'e': '#48b4e8', 'f': '#2c5ca8',          # 水色の 紙
       'Y': '#fffbe0', 'y': '#ffd85c', 'o': '#d48a34',          # まん中の 留め具（顔）
       'p': '#eec48a', 'n': '#9a5a3a',                          # 木の 棒
       'w': '#ffffff', 'v': '#7a48c8'}                          # 目の 光・ひとみ
LIGHT = set('adYpw')
KEEP_BLACK = set('wvbY')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def stamp(g, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c

# ---- 羽根：4枚の 紙（もも・水色 交互）。theta で 回る。各羽根は 折り返し（明）と 面（中）、右下の ふちは 暗 ----
R = 16.2
RAMP = ('abc', 'def')
def wheel(theta):
    W = H = 34; cx = cy = 17; g = grid(W, H); part = {}
    for y in range(H):
        for x in range(W):
            dx, dy = x + .5 - cx, y + .5 - cy; r = math.hypot(dx, dy)
            a = (math.degrees(math.atan2(dy, dx)) - theta) % 360
            i = int(a // 90); f = (a % 90) / 90
            if r > R * (.46 + .54 * f ** .8): continue
            L, M, D = RAMP[i % 2]
            mid = (i * 90 + 70 + theta) % 360     # 羽根の 向き
            lit = math.cos(math.radians(mid - 225))  # 左上なら +1
            curl = f > .5 and r > R * .4
            c = (L if lit > -.3 else M) if curl else (M if lit > -.75 else D)
            if not curl and lit < .4 and r > R * (.46 + .54 * f ** .8) - 1.6: c = D       # 右下の ふち
            if curl and abs(f - .5) < .06 and r > 4: c = D                                  # 折り目
            g[y][x] = c
    return outline(rows_of(g))

def smear():
    # 高速回転：もも・水色の 輪が まざった 円盤＋白い すじ
    W = H = 34; cx = cy = 17; g = grid(W, H)
    for y in range(H):
        for x in range(W):
            dx, dy = x + .5 - cx, y + .5 - cy; r = math.hypot(dx, dy)
            if r > R - .5: continue
            band = int(r / 2.6) % 2
            ang = math.degrees(math.atan2(dy, dx))
            c = 'b' if band else 'e'
            if math.cos(math.radians(ang - 225)) > .35: c = 'a' if band else 'd'
            elif math.cos(math.radians(ang - 225)) < -.6: c = 'c' if band else 'f'
            g[y][x] = c
    for a0 in (200, 20):
        for t in range(0, 70, 3):
            a = math.radians(a0 + t); rr = R - 3
            put(g, [(int(cx + rr * math.cos(a)), int(cy + rr * math.sin(a)))], 'w')
    return outline(rows_of(g))

# ---- まん中の 留め具（クリーム色の まるい ボタン）＝顔の 台 ----
def hub():
    g = grid(15, 14); ellipse(g, 7.5, 7, 7.5, 7, 'Y')
    for y in range(14):
        for x in range(15):
            if g[y][x] == '.': continue
            d = ((x + .5 - 7.5) / 7.5) ** 2 + ((y + .5 - 7) / 7) ** 2
            if d > .55 and (x - 7.5) + (y - 7) > 4: g[y][x] = 'y'
            if d > .7 and (x - 7.5) + (y - 7) > 6: g[y][x] = 'o'
    return outline(rows_of(g))

# ---- 顔：きらきら目（白い 光 2つ・むらさきの ひとみ・黒）＋ ほっぺ＋小さな 口 ----
EYE_N = ['.kkk.', 'kwwvk', 'kwvvk', 'kvvwk', '.kkk.']
EYE_F = ['.kk.', 'kwvk', 'kvvk', 'kvwk', '.kk.']
FACES = {
    'open':  (EYE_N, EYE_F, ['kkk', 'kbk', '.k.']),
    'blink': (['.....', '.....', '.kkk.', 'k...k', '.....'], ['....', '....', '.kk.', 'k..k', '....'], ['k.k', '.k.']),
    'fight': (['...kk', '.kk..', 'kwvvk', 'kvvwk', '.kkk.'], ['kk..', '..kk', 'kwvk', 'kvwk', '.kk.'], ['kkk', '...']),
    'shout': (['...kk', '.kk..', 'kwvvk', 'kvvwk', '.kkk.'], ['kk..', '..kk', 'kwvk', 'kvwk', '.kk.'], ['kkk', 'kbk', 'kbk', '.k.']),
    'pain':  (['k....', '.kk..', '...kk', '.kk..', 'k....'], ['...k', '.kk.', 'k...', '.kk.', '...k'], ['.k.', 'k.k']),
    'ko':    (['k...k', '.k.k.', '..k..', '.k.k.', 'k...k'], ['k..k', '.kk.', '.kk.', 'k..k', '....'], ['kkk']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(12, 10)
    stamp(g, ef, 0, 0); stamp(g, en, 6, 0); stamp(g, mo, 4, 6)
    if kind in ('open', 'blink'): put(g, [(0, 6), (1, 6), (10, 6), (11, 6)], 'a')
    return rows_of(g)

# ---- 木の 棒・リボン・足 ----
STICK = ['kppnk'] * 9
BOW = ['.kk...kk.',
       'kddkkkeek',
       'kdddkeeek',
       'kddkkkffk',
       '.kk...kk.']
BEAD = ['.kkkkk.', 'kpppnnk', 'kppnnnk', '.kkkkk.']
FOOT = ['.kkk.', 'kppnk', 'kpnnk', '.kkk.']

# ---- 風（攻撃）：三日月の 風の 刃＋きらきら ----
def crescent(H=17, big=False):
    W = H // 2 + 3; g = grid(W, H); r = H / 2; cy = H / 2
    for y in range(H):
        for x in range(W):
            d1 = math.hypot(x + .5 - (W - r - .5), y + .5 - cy); d2 = math.hypot(x + .5 - (W - r - 4.5), y + .5 - cy)
            if d1 <= r and d2 > r - .6:
                g[y][x] = 'd' if y < cy - 2 else 'e' if y < cy + 3 else 'f'
    for y in range(H):
        xs = [x for x in range(W) if g[y][x] != '.']
        if xs and y < cy + 2: g[y][xs[-1] - (1 if len(xs) > 2 else 0)] = 'w' if y < cy - 1 else g[y][xs[-1]]
    return outline(rows_of(g))
SPARK = ['.y.', 'yYy', '.y.']
def gust(big=False):
    g = grid(22, 26)
    stamp(g, crescent(21 if big else 17), 8 if big else 5, 1 if big else 3)
    for (x, y, n) in ((0, 7, 7), (1, 13, 9), (0, 18, 6)):          # 風の すじ
        for i in range(n): g[y][x + i] = 'e' if i < n - 3 else 'd'
    stamp(g, SPARK, 2, 1); stamp(g, SPARK, 4, 21)
    if big: stamp(g, SPARK, 19, 10)
    return rows_of(g)
WIND = ['kkkkk..', '.....kk', 'kkk...k', '...k..k', '..k...']

NA = 'ko'
def layers():
    return [
        dict(n='footB', g='legB', x=34, y=56, rows=FOOT, not_=NA),
        dict(n='footA', g='legA', x=28, y=56, rows=FOOT, not_=NA),
        dict(n='stick', g='body', x=31, y=48, rows=STICK, not_=NA),
        dict(n='wheel', g='head', x=15, y=15, rows=wheel(0),
             alt={'idle1|walk1|walk3': wheel(45), 'idle2|walk2': wheel(90), 'idle3': wheel(135), 'atk0|hit': wheel(20), 'atk1|atk2': smear()}, not_=NA),
        dict(n='hub', g='head', x=25, y=25, rows=hub(), not_=NA),
        dict(n='face', g='face', x=27, y=28, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='bow', g='body', x=29, y=48, rows=BOW, not_=NA),
        dict(n='tw1', g='head', x=15, y=18, rows=SPARK, only='idle0|idle2|blink'),
        dict(n='tw2', g='head', x=50, y=44, rows=SPARK, only='idle1|idle3'),
        dict(n='gust1', g='root', x=48, y=21, rows=gust(), only='atk1'),
        dict(n='gust2', g='root', x=50, y=19, rows=gust(True), only='atk2'),
        dict(n='ko', g='root', x=8, y=25, rows=ko_body(), only='ko'),
    ]

def ko_body():
    W, H = 36, 47; g = grid(W, H)
    stamp(g, FOOT, 13, 42); stamp(g, FOOT, 19, 42); stamp(g, STICK, 16, 34)
    stamp(g, wheel(30), 0, 0); stamp(g, BOW, 14, 33)
    g2 = [list(r) for r in rot90(rows_of(g))]
    stamp(g2, hub(), 21, 10); stamp(g2, face('ko'), 23, 13)
    return [''.join(r).rstrip('.') for r in g2]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, -1)}, 'idle2': {'head': (0, 0)}, 'idle3': {'head': (0, 1), 'body': (0, 0)}, 'blink': {},
    'walk0': {'body': (0, -1), 'legA': (0, -1)}, 'walk1': {'head': (0, 1)},
    'walk2': {'body': (0, -1), 'legB': (0, -1)}, 'walk3': {'head': (0, 1)},
    'atk0': {'root': (-2, 1), 'head': (-1, 0)}, 'atk1': {'root': (2, 0), 'head': (1, -1)}, 'atk2': {'root': (1, 0)},
    'hit': {'root': (-3, 0), 'head': (-1, 1)}, 'ko': {},
}
PARENT = {'face': 'head', 'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
