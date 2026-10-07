# ランプリン（ほのお・はがね × ハリケーンランプ）手打ち GBA風：無機物＋かわいい の 試作
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, rot90
META = dict(id='lampurin', name='ランプリン', types=['fire', 'steel'], base='ハリケーンランプ', size='S')
EYE_BOX = (26, 34, 14, 9)
PAL = {'k': '#141018', 'l': '#5a3418',
       'A': '#ffe9a0', 'B': '#e0a848', 'C': '#96602a',          # 真ちゅう
       'g': '#f2fdff', 'h': '#b4e2ee', 'j': '#6aa2bc',          # ガラス
       'f': '#fffbe0', 'y': '#ffd23c', 'o': '#ff8a24', 'R': '#d8461e',  # 炎
       'w': '#ffffff', 'r': '#7a2810', 's': '#a4a2b4'}
LIGHT = set('Agfyw')
KEEP_BLACK = set('wr')

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

# ---- 取っ手（針金の 輪）----
def handle():
    g = grid(18, 8)
    for x in range(18):
        for y in range(8):
            d = ((x - 8.5) / 8.5) ** 2 + ((y - 7.5) / 7.5) ** 2
            if .62 <= d <= 1.0: g[y][x] = 'B'
    put(g, [(3, 2), (4, 1), (5, 1), (6, 0), (7, 0)], 'A')
    return outline(rows_of(g))

# ---- ふた（丸い 真ちゅうの かさ、てっぺんに つまみ）----
def cap():
    g = grid(22, 8); ellipse(g, 11, 8, 11, 6.5, 'B')
    for x in range(9, 13): g[0][x] = 'B'; g[1][x] = 'B'
    shade(g, 'ABC', 1, 2)
    for x in range(1, 21): g[7][x] = 'C' if g[7][x] != '.' else '.'
    put(g, [(4, 4), (5, 3), (6, 3)], 'A'); put(g, [(10, 0)], 'A')
    for x in (5, 11, 17): put(g, [(x, 6)], 'l')        # 通気の 穴
    return outline(rows_of(g))

# ---- ガラスの ほや（中は 空気色、ふちと 下が 濃い）----
def glass():
    W, H = 26, 22; g = grid(W, H); ellipse(g, 13, 11, 13, 11, 'h')
    shade(g, 'ghj', 1, 2)
    return outline(rows_of(g))

# ---- 炎（顔）：しずく形、中心ほど 明るい。phase で ゆらぐ ----
def flame(phase=0, big=False, small=False):
    W, H = 21, 21; g = grid(W, H)
    cx, cy, rx, ry = 10, 13, 8.5, 7
    if big: rx, ry = 9.5, 7.5
    if small: rx, ry = 5.5, 4.5; cy = 15
    for y in range(H):
        for x in range(W):
            dx, dy = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            tip = cy - ry - (6 if not small else 3)
            if dx * dx + dy * dy <= 1 or (y + .5 < cy and y + .5 >= tip and abs(x + .5 - cx - (phase - 1) * (cy - y) / 10) <= (y + .5 - tip) * .55):
                r = (dx * dx + dy * dy) ** .5 if y + .5 >= cy else abs(x + .5 - cx) / rx + (cy - y) / (ry * 3)
                g[y][x] = 'f' if r < .45 else 'y' if r < .75 else 'o' if r < .95 else 'R'
    return rows_of(g)

# ---- 顔：大きな まるい 目（白い 光・黒・下に 赤茶）＋ 小さな 口 ----
EYE_N = ['.kkk.', 'kwwkk', 'kwkkk', 'kkkkk', 'kkrrk', '.krr.']        # 手前の 目
EYE_F = ['.kk.', 'kwkk', 'kkkk', 'kkkk', 'krrk', '.rr.']              # 奥の 目（少し 小さい）
FACES = {
    'open':  (EYE_N, EYE_F, ['k.k.k', '.k.k.']),
    'blink': (['.....', '.....', 'k...k', '.kkk.', '.....'], ['....', '....', 'k..k', '.kk.', '....'], ['k.k', '.k.']),
    'fight': (['kk...', '.kkk.', 'kwkkk', 'kkkrk', '.krr.'], ['...k', '.kk.', 'kwkk', 'kkrk', '.rr.'], ['kkk', '...']),
    'shout': (['kk...', '.kkk.', 'kwkkk', 'kkkrk', '.krr.'], ['...k', '.kk.', 'kwkk', 'kkrk', '.rr.'], ['.k.', 'krk', '.k.']),
    'pain':  (['k...k', '.k.k.', '..k..', '.k.k.', '.....'], ['k..k', '.kk.', '.kk.', 'k..k', '....'], ['.k.', 'k.k']),
    'ko':    (['k...k', '.k.k.', '..k..', '.k.k.', 'k...k'], ['k..k', '.kk.', '.kk.', 'k..k', '....'], ['kkk']),
}
def face(kind):
    en, ef, mo = FACES[kind]; g = grid(14, 10)
    for j, r in enumerate(ef):
        for i, c in enumerate(r):
            if c != '.': g[j][i] = c
    for j, r in enumerate(en):
        for i, c in enumerate(r):
            if c != '.': g[j][7 + i] = c
    for j, r in enumerate(mo):
        for i, c in enumerate(r):
            if c != '.': g[7 + j][4 + i] = c
    put(g, [(0, 6), (1, 6)], 'R'); put(g, [(12, 6), (13, 6)], 'R') if kind in ('open', 'blink') else None   # ほっぺ
    return rows_of(g)

# ---- ガラスの 映りこみ（炎の 上に 重ねる 白い 弧）と 針金の かご ----
REFLECT = ['..g', '.g.', 'g..', 'g..', 'g..', '.']
def wires():
    g = grid(26, 22)
    for y in range(2, 20):
        for x0 in (4, 21):
            off = 0 if 5 <= y <= 16 else (1 if x0 < 13 else -1)
            g[y][x0 + off] = 'C'
            if g[y][x0 + off + (1 if x0 < 13 else -1)] == '.': pass
    for x in range(3, 23): g[11][x] = '.'
    return rows_of(g)

# ---- 油つぼ（ずんぐりした 胴）と 芯の つまみ ----
def tank():
    W, H = 28, 12; g = grid(W, H); ellipse(g, 14, 7, 14, 7.5, 'B')
    for x in range(1, 27): g[0][x] = '.' if abs(x - 13.5) > 11 else g[0][x]
    shade(g, 'ABC', 1, 2)
    for x in range(2, 26): g[2][x] = 'C' if g[2][x] != '.' else '.'      # 首の 段
    for x in range(3, 25): g[3][x] = 'A' if 3 < x < 18 and g[3][x] != '.' else g[3][x]
    put(g, [(6, 6), (7, 5), (8, 5)], 'A')
    return outline(rows_of(g))
KNOB = ['.kkk.', 'kAABk', 'kABCk', 'kBCCk', '.kkk.']
FOOT = ['kkkkk', 'kBBCk', 'kCCCk', '.kkk.']
SMOKE = ['..ss.', '.s..s', '.s...', '..ss.', '....s', '...s.']

NA = 'ko'
def layers():
    return [
        dict(n='handle', g='top', x=23, y=12, rows=handle(), not_=NA),
        dict(n='footB', g='legB', x=36, y=56, rows=FOOT, not_=NA),
        dict(n='footA', g='legA', x=22, y=56, rows=FOOT, not_=NA),
        dict(n='tank', g='body', x=18, y=45, rows=tank(), not_=NA),
        dict(n='knob', g='body', x=45, y=49, rows=KNOB, not_=NA),
        dict(n='glass', g='body', x=19, y=25, rows=glass(), not_=NA),
        dict(n='flame', g='flame', x=22, y=25, rows=flame(1), alt={'idle1|walk1|walk3': flame(2), 'idle3': flame(0), 'atk0': flame(1, small=True), 'atk1|atk2': flame(1, big=True), 'hit': flame(0, small=True)}, not_=NA),
        dict(n='face', g='flame', x=26, y=34, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='wires', g='body', x=19, y=25, rows=wires(), not_=NA),
        dict(n='reflect', g='body', x=23, y=29, rows=REFLECT, not_=NA),
        dict(n='cap', g='top', x=21, y=19, rows=cap(), not_=NA),
        # 攻撃：ほやの 上から 火の玉
        dict(n='fire1', g='root', x=44, y=22, rows=[r for r in flame(1, small=True)[8:]], only='atk1'),
        dict(n='fire2', g='root', x=50, y=20, rows=[r for r in flame(2, small=True)[8:]], only='atk2'),
        # たおれ：横だおしの ランプ（90度）、火は 消えて けむり
        dict(n='ko', g='root', x=8, y=40, rows=ko_body(), only='ko'),
        dict(n='smoke', g='root', x=47, y=35, rows=SMOKE, only='ko'),
    ]

def ko_body():
    # 立ち姿を 組み立てて 90度 回す（取っ手は 外す）
    W, H = 34, 44; g = grid(W, H)
    def st(rows, x, y):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != '.' and 0 <= y + j < H and 0 <= x + i < W: g[y + j][x + i] = c
    st(FOOT, 6, 37); st(FOOT, 20, 37); st(tank(), 2, 26); st(glass(), 3, 6)
    st(wires(), 3, 6); st(face('ko'), 10, 17); st(cap(), 5, 0)
    rows = rot90(rows_of(g))
    return [r.rstrip('.') for r in rows]

FRAMES = {
    'idle0': {}, 'idle1': {'flame': (0, -1)}, 'idle2': {'body': (0, 1), 'top': (0, 1), 'flame': (0, 1)}, 'idle3': {'top': (0, 0)}, 'blink': {},
    'walk0': {'body': (0, -2), 'top': (0, -2), 'flame': (0, -2), 'legA': (0, -1)}, 'walk1': {'body': (0, -1), 'top': (0, -2), 'flame': (0, -1)},
    'walk2': {'body': (0, -2), 'top': (0, -2), 'flame': (0, -2), 'legB': (0, -1)}, 'walk3': {'body': (0, -1), 'top': (0, -2), 'flame': (0, -1)},
    'atk0': {'root': (-2, 1), 'top': (0, 1)}, 'atk1': {'root': (2, 0), 'top': (0, -2)}, 'atk2': {'root': (1, 0), 'top': (0, -1)},
    'hit': {'root': (-3, 0), 'top': (-1, 1)}, 'ko': {},
}
PARENT = {'top': 'body', 'flame': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
