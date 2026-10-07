# ツミキン（いわ・フェアリー × 積み木）手打ち GBA風：無機物＋かわいい ライン
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, stamp, poly
META = dict(id='tsumikin', name='ツミキン', types=['rock', 'fairy'], base='積み木', size='M')
EYE_BOX = (21, 27, 17, 6)
PAL = {'k': '#18141e', 'l': '#5a2e3a',
       'Y': '#fff2c4', 'X': '#eac078', 'Z': '#b07a4c',          # 白木（頭の 立方体）
       'R': '#ff8e6e', 'S': '#e0443e', 'T': '#9c2448',          # 赤い 積み木（胴）
       'b': '#82d0ff', 'B': '#3c7ce0', 'N': '#2c3a9c',          # 青い 積み木（足・腕）
       'g': '#b4f070', 'G': '#4cbc4c', 'H': '#1e7a5c',          # 緑の 三角（屋根）
       'w': '#ffffff', 'p': '#ff9ad2'}                          # 光・妖精の ピンク
LIGHT = set('YRbgw')
KEEP_BLACK = set('wpB')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch

# ---- 立方体（正面＋上面＋右側面）：上面＝明、正面＝中、右側面＝暗。光は 左上 ----
def box(w, h, d, ramp, front_hl=True):
    L, M, D = ramp; W, H = w + d, h + d; g = grid(W, H)
    for j in range(d):                                   # 上面（右上へ 奥行き）
        for i in range(w):
            g[j][d - j + i - 1 + 1 - 1 + 0] = L
    for j in range(h):                                   # 正面
        for i in range(w): g[d + j][i] = M
    for i in range(d):                                   # 右側面
        for j in range(h): g[d - i + j][w + i] = D
    # 上面の 右端と 側面の 上を つなぐ
    for j in range(d): g[j][w + d - 1 - j] = L if j == 0 else g[j][w + d - 1 - j]
    if front_hl:
        for i in range(w - 1): g[d][i] = L if i < w - 3 else M      # 正面の 上の ふち（光）
        for j in range(h - 1): g[d + j][0] = L if j < h - 3 else M  # 左の ふち
    return g

# ---- 頭：白木の 立方体。正面に 描いた 顔 ----
FACES = {
    #        奥の 目（左）           手前の 目（右）            口
    'open':  (['.k.', 'kwk', 'kBk', 'kBk', '.k.'], ['.kk.', 'kwkk', 'kwBk', 'kBBk', '.kk.'], ['k...k', 'kSSSk', '.kkk.']),
    'blink': (['...', '...', 'k.k', '.k.', '...'], ['....', '....', 'k..k', '.kk.', '....'], ['k...k', '.kkk.']),
    'fight': (['kk..', '.kkk', 'kwk.', 'kBk.', '.k..'], ['.kkk', 'kkk.', 'kwkk', 'kBBk', '.kk.'], ['.kkk.', 'k...k']),
    'shout': (['kk..', '.kkk', 'kwk.', 'kBk.', '.k..'], ['.kkk', 'kkk.', 'kwkk', 'kBBk', '.kk.'], ['.kkk.', 'kSSSk', 'kSRSk', '.kkk.']),
    'pain':  (['k..', '.k.', '..k', '.k.', 'k..'], ['...k', '..k.', '.k..', '..k.', '...k'], ['.k.k.', 'k.k.k']),
    'ko':    (['...', 'k.k', '.k.', 'k.k', '...'], ['....', 'k..k', '.kk.', 'k..k', '....'], ['kkkkk']),
}
def head(kind='open'):
    g = box(20, 18, 5, 'YXZ')
    # 木目（正面に 薄い すじ）
    for x in (3, 4, 5, 6): put(g, [(x, 21)], 'X')
    for x in range(12, 17): put(g, [(x, 8)], 'X')
    for j in range(3, 9): put(g, [(22, 5 + j + (j // 3))], 'Z')
    ef, en, mo = FACES[kind]
    stamp(g, ef, 4, 10); stamp(g, en, 12, 10); stamp(g, mo, 7, 16)
    if kind in ('open', 'blink'): put(g, [(2, 15), (3, 15)], 'p'); put(g, [(17, 15), (18, 15)], 'p')
    return outline(rows_of(g))

# ---- 屋根：緑の 三角柱（正面の 三角＋右へ のびる 斜面）----
def roof():
    w, h, d = 20, 10, 5; g = grid(w + d, h + d); a = w // 2
    poly(g, [(0, d + h), (a, d), (a + d, 0), (d, h)], 'g')          # 左の 斜面（上を 向く＝明）
    poly(g, [(a, d), (a + d, 0), (w + d, h), (w, d + h)], 'H')      # 右の 斜面（影）
    poly(g, [(0, d + h), (a, d), (w, d + h)], 'G')                  # 正面の 三角
    for y in range(h + d):                                          # 右の 斜面の 上の ふちは 空の 光を 受ける
        for x in range(w + d - 1, -1, -1):
            if g[y][x] == 'H':
                if y < h and (y == 0 or g[y - 1][x] == '.'): g[y][x] = 'G'
                break
    for y in range(h + d):                                          # 正面の 左の ふちに 光（2ドット）
        xs = [x for x in range(w + d) if g[y][x] != '.']
        if xs and g[y][xs[0]] == 'G':
            g[y][xs[0]] = 'g'
            if y > d + 3 and g[y][xs[0] + 1] == 'G': g[y][xs[0] + 1] = 'g'
    return outline(rows_of(g))

# ---- 胴：赤い 直方体。正面に 妖精の 星を ペイント ----
STAR = ['..w..', '.wpw.', 'wpppw', '.pwp.', 'p...p']
STAR = ['...p...', '..ppp..', 'ppppppp', '.ppwpp.', '..ppp..', '.pp.pp.', 'p.....p']
def torso():
    g = box(18, 11, 4, 'RST')
    stamp(g, ['..p..', '.ppp.', 'ppwpp', '.ppp.', 'p...p'], 7, 7)
    return outline(rows_of(g))

# ---- 足・腕：青い 小さな 積み木 ----
def foot(): return outline(rows_of(box(7, 5, 2, 'bBN')))
def arm(): return outline(rows_of(box(5, 5, 2, 'bBN')))

# ---- 妖精の きらめき（はなれているのは 意図的）----
SPK = ['.p.', 'pwp', '.p.']
SPK2 = ['..p..', '..p..', 'ppwpp', '..p..', '..p..']
PEB = outline(rows_of(box(5, 5, 2, 'gGH', False)))         # 投げる 小さな 積み木
PEB2 = outline(rows_of(box(4, 4, 2, 'bBN', False)))
PEB3 = outline(rows_of(box(4, 4, 2, 'YXZ', False)))
DUST = outline(['..XX....', '.XYYXX..', 'XYYYYXX.', 'XXYXXXZX', '.XXXZZZ.'])
TRAIL = ['pppp...', '.......', '..ppppp', '.......', 'ppp....']

def ko_pile():
    W, H = 70, 34; g = grid(W, H)
    stamp(g, foot(), 0, 22); stamp(g, foot(), 40, 23); stamp(g, arm(), 58, 22)
    stamp(g, torso(), 4, 13)                               # 胴は 左に 落ちる
    stamp(g, roof(), 44, 13)                               # 屋根は 右に ころがる
    stamp(g, head('ko'), 18, 4)                            # 頭は 胴に よりかかる
    return [x.rstrip('.') for x in rows_of(g)]

NA = 'ko'
def layers():
    return [
        dict(n='armB', g='armA', x=15, y=42, rows=arm(), not_=NA),
        dict(n='footB', g='legB', x=31, y=50, rows=foot(), not_=NA),
        dict(n='footA', g='legA', x=17, y=51, rows=foot(), not_=NA),
        dict(n='torso', g='body', x=17, y=37, rows=torso(), not_=NA),
        dict(n='armF', g='armB', x=40, y=42, rows=arm(), not_=NA),
        dict(n='head', g='head', x=18, y=17, rows=head(), alt={'blink': head('blink'), 'atk0': head('fight'), 'atk1|atk2': head('shout'), 'hit': head('pain')}, not_=NA),
        dict(n='roof', g='roof', x=18, y=5, rows=roof(), not_=NA),
        dict(n='spk1', g='fx', x=10, y=12, rows=SPK, alt={'idle2|idle3|walk2|walk3': SPK2}, not_='atk1|atk2|hit|ko'),
        dict(n='spk2', g='fx2', x=50, y=16, rows=SPK2, alt={'idle2|idle3|walk2|walk3': SPK}, not_='atk1|atk2|hit|ko'),
        dict(n='trl', g='root', x=47, y=29, rows=TRAIL, only='atk1'),
        dict(n='peb1', g='root', x=52, y=24, rows=PEB, only='atk1'),
        dict(n='peb2', g='root', x=58, y=35, rows=PEB2, only='atk1'),
        dict(n='peb4', g='root', x=50, y=36, rows=PEB3, only='atk1'),
        dict(n='spkA', g='root', x=63, y=21, rows=SPK2, only='atk1|atk2'),
        dict(n='dust', g='root', x=62, y=38, rows=DUST, only='atk2'),
        dict(n='peb3', g='root', x=63, y=28, rows=PEB, only='atk2'),
        dict(n='peb5', g='root', x=70, y=34, rows=PEB3, only='atk2'),
        dict(n='spkB', g='root', x=58, y=46, rows=SPK, only='atk2'),
        dict(n='ko', g='root', x=0, y=29, rows=ko_pile(), only='ko'),
        dict(n='koS', g='root', x=12, y=28, rows=SPK, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'fx': (0, -1)}, 'idle2': {'head': (0, 1), 'roof': (0, -1), 'fx2': (0, 1)}, 'idle3': {'roof': (0, 0), 'fx': (0, 1)},
    'blink': {},
    'walk0': {'body': (0, -1), 'legA': (1, -2)}, 'walk1': {'body': (0, -1), 'head': (1, 0)},
    'walk2': {'body': (0, -1), 'legB': (1, -2)}, 'walk3': {'body': (0, -1), 'head': (-1, 0)},
    'atk0': {'root': (-3, 1), 'head': (-1, 1), 'roof': (-1, 1), 'armB': (-2, -1)},
    'atk1': {'root': (3, 0), 'head': (2, -1), 'roof': (1, -2), 'armB': (3, -3)}, 'atk2': {'root': (2, 0), 'head': (1, 0), 'roof': (1, -1), 'armB': (2, -1)},
    'hit': {'root': (-3, 0), 'head': (-2, 0), 'roof': (-2, -2), 'armB': (0, 1)}, 'ko': {},
}
PARENT = {'body': 'root', 'armA': 'body', 'armB': 'body', 'head': 'body', 'roof': 'head', 'legA': 'root', 'legB': 'root', 'fx': 'root', 'fx2': 'root'}
