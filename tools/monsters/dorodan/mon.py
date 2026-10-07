# ドロダン（じめん・フェアリー × 光る 泥だんご）手打ち GBA風：無機物＋かわいい
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, rot90
META = dict(id='dorodan', name='ドロダン', types=['ground', 'fairy'], base='光る 泥だんご', size='S')
EYE_BOX = (31, 36, 12, 5)
PAL = {'k': '#1a1014', 'l': '#52261c',
       'A': '#dc9a5e', 'B': '#a65c36', 'C': '#6a3040',          # みがいた 泥（明・中・暗）
       'g': '#fffaf0', 'h': '#f2cc9c',                          # つやの 光
       'p': '#ff8e9a', 'v': '#b84870',                          # ほっぺ・目の 下の 色
       'Y': '#fff27a', 's': '#ffb6e8',                          # きらきら（フェアリー）
       'u': '#c8a27c', 'm': '#7a5236'}                          # 土ぼこり・泥はね
LIGHT = set('Agh')
KEEP_BLACK = set('gvABC')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
def stamp(g, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c

# ---- 泥だんご：球の 明暗（左上から 光）、右下に 照りかえし、左上に 窓の 映りこみ ----
D = 32
def ball(crack=0, dull=False):
    g = grid(D, D); c = D / 2; r = D / 2
    lx, ly, lz = -.55, -.6, .58
    for y in range(D):
        for x in range(D):
            dx, dy = (x + .5 - c) / r, (y + .5 - c) / r; q = dx * dx + dy * dy
            if q > 1: continue
            dz = math.sqrt(1 - q); i = dx * lx + dy * ly + dz * lz
            ch = 'A' if i > .84 else 'B' if i > .22 else 'C'
            if q > .8 and dy < -.3: ch = 'A' if dx < .5 else 'B'                       # 上の ふち（上を 向く 面）
            if q > .8 and dx < .05 and dy < .72 and dx + dy < .1: ch = 'A'                # 左上の ふち 明
            if q > .8 and dx + dy > .9 and ch == 'C': ch = 'B'               # みがいた ふちの 照りかえし
            g[y][x] = ch
    # 窓の 映りこみ（まるい 四角＋十字の わく）
    WIN = ['..hhh.', '.hggh.', 'hggh..', 'hgh...', 'hh....']
    if not dull:
        stamp(g, WIN, 5, 4); put(g, [(12, 4), (13, 4)], 'h')
        put(g, [(22, 26), (23, 25), (24, 24)], 'h')                              # 下の 照り
    if crack:                                                                 # ひび（被弾・ダウン）
        pts = [(13, 0), (13, 1), (14, 2), (14, 3), (13, 4), (12, 5), (12, 6)] if crack == 1 else \
              [(13, 0), (13, 1), (14, 2), (14, 3), (13, 4), (12, 5), (12, 6), (13, 7), (14, 8), (14, 9), (13, 10), (15, 3), (16, 4), (17, 4)]
        put(g, pts, 'k')
    return outline(rows_of(g))

# ---- 顔：つぶらな 点の 目（光・黒・ばら色）＋ 大きな ほっぺ ----
EYE = ['.kk.', 'kgkk', 'kkkk', 'kkvk', '.kk.']
FACES = {
    'open':  (EYE, EYE, ['k...k', '.kvk.']),
    'blink': (['....', '....', 'kkkk', '.kk.', '....'], ['....', '....', 'kkkk', '.kk.', '....'], ['k...k', '.kvk.']),
    'fight': (['k...', '.kk.', 'kgkk', 'kkvk', '.kk.'], ['...k', '.kk.', 'kgkk', 'kkvk', '.kk.'], ['kkk', '...']),
    'shout': (['k...', '.kk.', 'kgkk', 'kkvk', '.kk.'], ['...k', '.kk.', 'kgkk', 'kkvk', '.kk.'], ['.k.', 'kvk', 'kvk', '.k.']),
    'pain':  (['k...', '.kk.', '...k', '.kk.', 'k...'], ['...k', '.kk.', 'k...', '.kk.', '...k'], ['.k.', 'k.k']),
    'ko':    (['k..k', '.kk.', '.kk.', 'k..k', '....'], ['k..k', '.kk.', '.kk.', 'k..k', '....'], ['kkk']),
}
def face(kind):
    ef, en, mo = FACES[kind]; g = grid(13, 9)
    stamp(g, ef, 0, 0); stamp(g, en, 8, 0); stamp(g, mo, 4 if len(mo[0]) == 5 else 5, 5)
    if kind in ('open', 'blink'): put(g, [(0, 6), (1, 6), (2, 6), (10, 6), (11, 6), (12, 6)], 'p')
    return rows_of(g)

# ---- 足（みじかい 4本）----
LEG_N = ['kABk', 'kABk', 'kBBCk', '.kkk.']
LEG_N = ['kABCk'] * 4 + ['kABCk', 'kBBCk', '.kkk.']
LEG_F = ['kBCCk'] * 4 + ['kCCCk', '.kkk.']

# ---- エフェクト ----
SPARK = ['.Y.', 'YgY', '.Y.']
SPARK2 = ['..s..', '..s..', 'ssgss', '..s..', '..s..']
DUST = ['..kkk..', '.kuuuk.', 'kuuuuuk', '.kkkkk.']
SPLAT = ['.kk', 'kmk', 'kk.']
def roll():
    # ころがり：光は そのまま、顔だけ 90度 回って 下へ（前転）。うしろに 速さの 線・土ぼこり・きらきら
    g = grid(50, 38)
    b = [list(r) for r in ball()]; stamp(b, rot90(face('shout')), 19, 17)
    stamp(g, rows_of(b), 15, 2)
    for y, n, x0 in ((9, 9, 3), (17, 12, 0), (25, 10, 2)):
        for i in range(n): g[y][x0 + i] = 'u' if i < n - 3 else 'h'
    stamp(g, DUSTB, 0, 28); stamp(g, DUST, 8, 31)
    stamp(g, SPARK, 6, 3); stamp(g, ['.s.', 'sgs', '.s.'], 9, 20)
    stamp(g, SPLAT, 46, 30)
    return rows_of(g)
DUSTB = ['...kkkk...', '.kkuuuukk.', 'kuuhhuuuuk', 'kuuuuuuuuk', '.kkkkkkkk.']
BURST = ['....k....', '...kYk...', '.k.kYk.k.', 'kYkYgYkYk', '.kYgggYk.', 'kYkYgYkYk', '.k.kYk.k.', '...kYk...', '....k....']
LEG_S = ['.kkkkk.', 'kAABBCk', 'kBBBCCk', '.kkkkk.']

NA = 'ko'
def layers():
    return [
        dict(n='legFB', g='legB', x=16, y=51, rows=LEG_F, not_=NA + '|atk1'),
        dict(n='legFA', g='legA', x=33, y=53, rows=LEG_F, not_=NA + '|atk1'),
        dict(n='legNA', g='legA', x=21, y=53, rows=LEG_N, not_=NA + '|atk1'),
        dict(n='legNB', g='legB', x=38, y=53, rows=LEG_N, not_=NA + '|atk1'),
        dict(n='ball', g='body', x=14, y=24, rows=ball(), alt={'hit': ball(1)}, not_=NA + '|atk1'),
        dict(n='face', g='face', x=31, y=36, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk2': face('shout'), 'hit': face('pain')}, not_=NA + '|atk1'),
        dict(n='tw1', g='body', x=46, y=24, rows=SPARK, only='idle0|idle1|blink'),
        dict(n='tw2', g='body', x=9, y=44, rows=SPARK, only='idle2|idle3'),
        dict(n='roll', g='root', x=3, y=22, rows=roll(), only='atk1'),
        dict(n='imp', g='root', x=46, y=28, rows=BURST, only='atk2'),
        dict(n='imp2', g='root', x=56, y=24, rows=['..s..', '..s..', 'ssgss', '..s..', '..s..'], only='atk2'),
        dict(n='spl1', g='root', x=48, y=50, rows=SPLAT, only='atk2|hit'),
        dict(n='spl2', g='root', x=55, y=44, rows=SPLAT, only='atk2'),
        dict(n='ko', g='root', x=9, y=24, rows=ko_body(), only='ko'),
    ]

def ko_body():
    # へたりこみ：足を 横に 投げ出し、つやが 消えて ひびが 入る。目は ×
    g = grid(44, 36)
    stamp(g, DUSTB, 32, 26); stamp(g, LEG_S, 4, 30); stamp(g, LEG_S, 33, 30)
    b = [list(r) for r in ball(2, dull=True)]; stamp(b, face('ko'), 16, 14)
    stamp(g, rows_of(b), 5, 2)
    return rows_of(g)

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'face': (0, 0)}, 'idle3': {}, 'blink': {},
    'walk0': {'body': (0, -1), 'legA': (1, -1)}, 'walk1': {'body': (0, 0)},
    'walk2': {'body': (0, -1), 'legB': (1, -1)}, 'walk3': {'body': (0, 0)},
    'atk0': {'root': (-3, 0), 'body': (0, 2), 'legA': (0, 0)}, 'atk1': {'root': (4, 0)}, 'atk2': {'root': (3, 0)},
    'hit': {'root': (-3, 0), 'body': (-1, 0)}, 'ko': {},
}
PARENT = {'face': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
