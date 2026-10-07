# ノリムスビ（くさ・じめん × おにぎり）手打ち GBA風：無機物＋かわいい
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, rot90, stamp
META = dict(id='norimusubi', name='ノリムスビ', types=['grass', 'ground'], base='おにぎり', size='S')
EYE_BOX = (26, 37, 14, 9)
PAL = {'k': '#16141a', 'l': '#6a4a3a',
       'A': '#fffdf2', 'B': '#ebe2c8', 'C': '#b8aa96',            # ごはん
       'n': '#4e6e52', 'N': '#2a3e34', 'm': '#18241f',            # のり
       'u': '#ff7d86', 'U': '#d6344a', 'v': '#8a1c3a',            # 梅干し
       'g': '#9ad64a', 'G': '#3c8a3a',                            # しその 葉
       'w': '#ffffff', 'p': '#ff9fae', 'e': '#1c1222'}
LIGHT = set('Agw')
KEEP_BLACK = set('we')

def rtri(W, H, pts, r):
    """角の 丸い 三角形（小さい 三角形を r だけ ふくらませる）"""
    def seg(px, py, a, b):
        (x1, y1), (x2, y2) = a, b; dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        return ((px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2) ** .5
    def inside(px, py):
        s = []
        for i in range(3):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 3]; s.append((x2 - x1) * (py - y1) - (y2 - y1) * (px - x1))
        return all(v >= 0 for v in s) or all(v <= 0 for v in s)
    return {(x, y) for y in range(H) for x in range(W)
            if inside(x + .5, y + .5) or min(seg(x + .5, y + .5, pts[i], pts[(i + 1) % 3]) for i in range(3)) <= r}

def shade(g, ramp, lw=1, dw=2):
    L, M, D = ramp; H, W = len(g), len(g[0]); src = [r[:] for r in g]
    inside = lambda y, x: 0 <= y < H and 0 <= x < W and src[y][x] == M
    for y in range(H):
        for x in range(W):
            if src[y][x] != M: continue
            dr = min(next((i for i in range(1, 9) if not inside(y + i, x)), 9), next((i for i in range(1, 9) if not inside(y, x + i)), 9))
            ul = min(next((i for i in range(1, 9) if not inside(y - i, x)), 9), next((i for i in range(1, 9) if not inside(y, x - i)), 9))
            if dr <= dw: g[y][x] = D
            elif ul <= lw: g[y][x] = L
    return g
def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch

# ---- おにぎりの 体：頂点を 少し 右へ ずらした 三角（右向き 3/4）、右下が 厚く 暗い。下に 海苔の 帯 ----
TRI = [(19, 7), (5, 24), (32, 24)]
def body():
    W, H = 39, 31; g = grid(W, H)
    front = rtri(W, H, TRI, 6.5)
    for x, y in front: g[y][x] = 'B'
    shade(g, 'ABC', 1, 2)
    for x, y in front:      # 右の 面（厚み）：右下の ふちを 3ドット 暗く
        if g[y][x] == 'B' and (x + 3, y) not in front and y > 6: g[y][x] = 'C'
    # ごはんつぶ（短い 2ドットの 粒）
    put(g, [(13, 11), (14, 11), (9, 17), (10, 16), (17, 8), (18, 8), (6, 21), (7, 21)], 'A')
    put(g, [(30, 18), (31, 19), (27, 12), (28, 13)], 'B')
    # 海苔：正面の 下 中央を 帯で 包む（右側は 影で 暗い）
    for x, y in front:
        if y >= 20 and 11 <= x <= 28:
            g[y][x] = 'm' if x >= 26 or y >= 29 else 'n' if (x == 11 or y == 20) else 'N'
    put(g, [(14, 23), (15, 23), (16, 24), (17, 25), (18, 26)], 'n')      # 海苔の つや
    # 土の よごれ（ころがった あと）
    put(g, [(4, 25), (5, 25), (5, 26), (6, 26), (8, 27), (9, 27)], 'l')
    return outline(rows_of(g))

# ---- 梅干し（てっぺんに のぞく）としその 葉 ----
def ume():
    g = [list(r) for r in ['..uuuUUU..', '.uwuUUUUU.', 'uuuUUUUvUU', 'uUUvvUUvUU', 'UUUUUvvUUU', '.UUUUUUUv.', '..vvvvvv..']]   # しわしわ
    return outline(rows_of(g))
LEAF0 = ['kk.........', 'kgkk.......', 'kggGkkk....', '.kgggGGkk..', '.kGggGGGGk.', '..kGGgGGGGk', '...kkGGgGkk', '.....kkkkk.']
LEAF1 = ['...........', 'kkk........', 'kggkkk.....', '.kgggGGkk..', '.kGggGGGGk.', '..kGGgGGGGk', '...kkGGgGkk', '.....kkkkk.']
LEAF2 = ['...........', '...........', 'kkkkk......', 'kgggGkkkk..', '.kGgggGGGkk', '..kGGGggGGk', '...kkGGGGkk', '.....kkkkk.']

# ---- 顔：つぶらな 点の 目（光・黒・下に 海苔色）＋ ほっぺ ＋ 口 ----
EN = ['.ee.', 'ewee', 'eeee', 'eNNe', '.ee.']
EF = ['.ee', 'ewe', 'eee', 'eNe', '.e.']
FACES = {
    'open':  (EN, EF, ['eeee', 'evve', '.ee.']),
    'blink': (['....', '....', 'e..e', '.ee.', '....'], ['...', '...', 'e.e', '.e.', '...'], ['eeee', 'evve', '.ee.']),
    'fight': (['ee..', '.eee', 'ewee', 'eeNe', '.ee.'], ['..e', 'ee.', 'wee', 'eNe', '.e.'], ['....', 'eeee', '....']),
    'shout': (['ee..', '.eee', 'ewee', 'eeNe', '.ee.'], ['..e', 'ee.', 'wee', 'eNe', '.e.'], ['eeee', 'evve', 'evve', '.ee.']),
    'pain':  (['e...', '.ee.', '...e', '.ee.', 'e...'], ['..e', 'ee.', 'e..', '.ee', '...'], ['.ee.', 'e..e']),
    'ko':    (['e..e', '.ee.', '.ee.', 'e..e', '....'], ['e.e', '.e.', 'e.e', '...', '...'], ['eeee']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(14, 9)
    stamp(g, ef, 0, 0); stamp(g, en, 9, 0)
    stamp(g, mo, 5, 5)
    if kind in ('open', 'blink'): put(g, [(0, 5), (1, 5)], 'p'); put(g, [(11, 5), (12, 5), (13, 5)], 'p')
    return rows_of(g)

ARM_B = ['.kkk.', 'kBBCk', 'kBCCk', '.kkk.']
ARM_F = ['.kkkk.', 'kABBBk', 'kBBBCk', 'kBCCCk', '.kkkk.']
ARM_UP = ['.kk.', 'kABk', 'kBCk', 'kBCk', '.kk.']
FOOT = ['.kkkk.', 'kBBBCk', 'kBBCCk', 'kBCCCk', '.kkkk.']

# ---- 攻撃：しその 葉が 回って 飛ぶ ＋ 土くれ ----
CLOD = ['.kkk.', 'kCllk', 'kllkk', '.kk..']
SPIN = ['....kk...', '...kggk..', '..kgggGk.', '.kggGGGk.', 'kgGGgGGk.', 'kGGGGgGGk', '.kGGGGGk.', '..kkGGk..', '....kk...']
WIND = ['.gg.....', 'g..gg...', '.....gg.', '......g.']
DUST = ['..CC....', '.C..C.C.', 'C....C.C', '.CC.C...']
STAR = ['..u..', '.uuu.', 'uuuuu', '.uuu.', '..u..']

NA = 'ko'
def layers():
    return [
        dict(n='armB', g='arms', x=7, y=45, rows=ARM_B, alt={'atk0': ARM_UP, 'atk1|atk2': ARM_B}, not_=NA),
        dict(n='leaf', g='leaf', x=18, y=15, rows=LEAF0, alt={'idle1|idle2|walk1|walk3': LEAF1, 'atk1|atk2|hit': LEAF2}, not_=NA),
        dict(n='footB', g='legB', x=37, y=55, rows=FOOT, not_=NA),
        dict(n='footA', g='legA', x=22, y=56, rows=FOOT, not_=NA),
        dict(n='body', g='body', x=11, y=25, rows=body(), not_=NA),
        dict(n='ume', g='top', x=25, y=21, rows=ume(), not_=NA),
        dict(n='face', g='face', x=26, y=37, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='armF', g='arms', x=47, y=45, rows=ARM_F, alt={'atk0': ARM_UP, 'atk1|atk2': ARM_F}, not_=NA),
        dict(n='spin1', g='root', x=55, y=31, rows=SPIN, only='atk1'),
        dict(n='wind1', g='root', x=51, y=27, rows=WIND, only='atk1'),
        dict(n='clod1', g='root', x=56, y=47, rows=CLOD, only='atk1'),
        dict(n='clod1b', g='root', x=61, y=42, rows=CLOD, only='atk1'),
        dict(n='spin1b', g='root', x=63, y=26, rows=SPIN, only='atk1'),
        dict(n='spin2b', g='root', x=69, y=37, rows=SPIN, only='atk2'),
        dict(n='spin2', g='root', x=62, y=25, rows=SPIN, only='atk2'),
        dict(n='wind2', g='root', x=56, y=33, rows=WIND, only='atk2'),
        dict(n='clod2', g='root', x=66, y=42, rows=CLOD, only='atk2'),
        dict(n='clod3', g='root', x=61, y=50, rows=CLOD, only='atk2'),
        dict(n='ko', g='root', x=10, y=24, rows=ko_body(), only='ko'),
        dict(n='kodust', g='root', x=6, y=55, rows=DUST, only='ko'),
        dict(n='koume', g='root', x=50, y=53, rows=ume(), only='ko'),
        dict(n='koleaf', g='root', x=55, y=46, rows=LEAF2[2:], only='ko'),
    ]

def ko_body():
    # 体を 組んで 90度 回す：頂点が 左、海苔が 右に くる 横だおし
    W, H = 43, 33; g = grid(W, H)
    stamp(g, ARM_B, 0, 18); stamp(g, body(), 2, 0); stamp(g, face('ko'), 17, 12)
    rows = rot90(rows_of(g))
    rows = [r[::-1] for r in rows][::-1]            # 反時計回りに
    rows = [r[::-1] for r in rows]                  # 頂点を 左へ
    return [r.rstrip('.') for r in rows]

FRAMES = {
    'idle0': {}, 'idle1': {'leaf': (0, 0)}, 'idle2': {'body': (0, 1), 'arms': (0, 1)}, 'idle3': {'arms': (0, -1)}, 'blink': {},
    'walk0': {'body': (0, -1), 'arms': (0, -1), 'legA': (0, -1)},
    'walk1': {'body': (0, -2), 'arms': (0, -1)},
    'walk2': {'body': (0, -1), 'arms': (0, -2), 'legB': (0, -1)},
    'walk3': {'body': (0, -2), 'arms': (0, -1)},
    'atk0': {'root': (-2, 1), 'arms': (0, -2), 'body': (0, 1)},
    'atk1': {'root': (3, -1), 'arms': (1, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0), 'top': (-1, 0), 'arms': (0, -2)}, 'ko': {},
}
PARENT = {'top': 'body', 'face': 'body', 'leaf': 'top', 'body': 'root', 'arms': 'root', 'legA': 'root', 'legB': 'root'}
