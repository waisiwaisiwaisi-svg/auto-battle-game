# フウリン（こおり・かぜ × 風鈴）手打ち GBA風：無機物＋かわいい
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, rot90, stamp
META = dict(id='fuurin', name='フウリン', types=['ice', 'wind'], base='風鈴', size='S')
EYE_BOX = (29, 26, 15, 7)
PAL = {'k': '#141626', 'l': '#2c5a86',
       'g': '#f4fdff', 'h': '#bce6f2', 'j': '#6eaad6',          # ガラス
       'i': '#1e2468', 'c': '#4c84e8',                          # 絵つけ（藍）
       'w': '#ffffff', 'r': '#e2383e', 'R': '#8e1a3a',          # ひも
       't': '#fff0e8', 'T': '#f59cb4', 'U': '#b04a7c'}          # 短冊
LIGHT = set('gwt')
KEEP_BLACK = set('w')

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

# ---- ガラスの 鈴：丸い 屋根＋少し 広がる 口、下に 口の ふち（だ円）----
def bell():
    W, H = 27, 21; g = grid(W, H); cx = 13.5
    for y in range(H):
        for x in range(W):
            px, py = x + .5, y + .5
            if py < 12: ok = ((px - cx) / 12.5) ** 2 + ((py - 12) / 11.5) ** 2 <= 1
            elif py < 18: ok = abs(px - cx) <= 12.5 + (py - 12) * .18
            else: ok = ((px - cx) / 13.5) ** 2 + ((py - 18) / 2.6) ** 2 <= 1
            if ok: g[y][x] = 'h'
    shade(g, 'ghj', 1, 2)
    # 口の 内がわ（奥の ふちが 見える）：濃い 水色、手前の ふちは 明るい 線
    for y in range(H):
        for x in range(W):
            if ((x + .5 - cx) / 11.5) ** 2 + ((y + .5 - 18.3) / 1.5) ** 2 <= 1: g[y][x] = 'j'
    for x in range(4, 23): 
        if g[19][x] in 'jh': g[19][x] = 'g' if x < 12 else 'h'
    # ガラスの 映りこみ（左上の 白い 弧）と 霜の きらめき
    put(g, [(5, 6), (5, 7), (4, 8), (4, 9), (4, 10), (6, 5), (7, 4)], 'w')
    put(g, [(9, 3), (10, 3)], 'g')
    # 絵つけの 雪の 結晶（左下の 面）
    put(g, [(6, 11), (6, 12), (6, 14), (6, 16), (6, 17), (3, 14), (4, 14), (8, 14), (9, 14), (5, 13), (7, 13), (5, 15), (7, 15)], 'c')
    return outline(rows_of(g))

# ---- てっぺんの ひもの 輪 ----
LOOP = ['.rrr.', 'r...r', 'R...r', '.R.r.', '..r..', '..r..', '..R..']
# ---- 舌（ぜつ）：ガラスの 玉と ひも ----
BEAD = ['..R..', '.kkk.', 'kwckk', 'kccik', '.kkk.', '..r..', '..r..']
BEAD_SW = ['.R...', '..kkk', '.kwck', '.kcci', '..kkk', '...r.', '..r..']

# ---- 短冊：ゆれ 具合で 段を ずらす ----
def tanzaku(sw=0):
    rows = ['.kkkkkkk.', 'kttttttTk', 'kttUUttTk', 'ktttUttTk', 'kttUUttTk', 'ktttttTTk', 'kttUttTTk', 'kttUUttTk', 'ktttUttTk', 'ktttttTTk', 'kTTTTTTTk', '.kkkkkkk.']
    out = []
    for j, r in enumerate(rows):
        d = int(round(sw * j / 6))
        out.append('.' * max(0, 3 + d) + r)
    return out
WIND_A = ['..hh....', '.h..hh..', '......h.', '...hh...', '..h.....']
WIND_B = ['....hh..', '..hh..h.', '.h......', '....hh..', '......h.']

# ---- 顔：絵つけの ねむそうな 目（藍の まぶた・青・白い 光）＋ 赤い 口 ----
EN = ['iiiiiii', 'iwccii.', 'icccii.', '.iiii..']
EF = ['iiiii', 'iwcii', 'iccii', '.iii.']
FIGHT_N = ['....iii', '.iiii..', 'iwccii.', 'icccii.', '.iiii..']
FIGHT_F = ['ii...', '.iii.', 'iwcii', 'iccii', '.iii.']
FACES = {
    'open':  (EN, EF, ['r.r.r', '.r.r.'], 4),
    'blink': (['.......', 'iiiiiii', '.iiii..', '.......'], ['.....', 'iiiii', '.iii.', '.....'], ['r.r.r', '.r.r.'], 4),
    'fight': (FIGHT_N, FIGHT_F, ['rrrrr'], 6),
    'shout': (FIGHT_N, FIGHT_F, ['.rrr.', 'rRRRr', '.rrr.'], 5),
    'pain':  (['....ii', '..ii..', 'ii....', '..ii..', '....ii'], ['ii....', '..ii..', '....ii', '..ii..', 'ii....'], ['.rrr.', 'r...r'], 6),
    'ko':    (['i...i.', '.i.i..', '..i...', '.i.i..', 'i...i.'], ['i...i', '.i.i.', '..i..', '.i.i.', 'i...i'], ['rrrrr'], 6),
}
def face(kind):
    en, ef, mo, my = FACES[kind]; g = grid(15, 9)
    stamp(g, ef, 0, 0); stamp(g, en, 9, 0); stamp(g, mo, 5, my)
    if kind in ('open', 'blink'): put(g, [(0, 4), (1, 4)], 'T'); put(g, [(12, 4), (13, 4), (14, 4)], 'T')
    return rows_of(g)

# ---- 攻撃：音の 波 ＋ 冷たい 風と 雪の 結晶 ----
def wave(h):
    """音の 波：右へ ふくらむ 弧（青と 水色の 2本線）"""
    g = grid(6, h); c = (h - 1) / 2
    for y in range(h):
        d = abs(y - c) / c; x = int(round(4 - 4 * d * d))
        g[y][min(5, x + 1)] = 'h'; g[y][x] = 'c'
    return rows_of(g)
FLAKE = ['..h..', 'h.g.h', '.ggg.', 'h.g.h', '..h..']
GUST = ['.hhhhh.....', 'g.....hh...', '........h..', '..hhhhhh.h.', '.g......hh.', '...........', '.....ggggh.']

NA = 'ko'
def layers():
    return [
        dict(n='loop', g='bell', x=30, y=12, rows=LOOP, not_=NA),
        dict(n='str', g='tail', x=31, y=44, rows=['r', 'R'], not_=NA),
        dict(n='tanzaku', g='tail', x=25, y=45, rows=tanzaku(0), alt={'idle1|idle3|walk1|walk3': tanzaku(-1), 'idle2|walk2': tanzaku(-2), 'atk0': tanzaku(2), 'atk1|atk2': tanzaku(-3), 'hit': tanzaku(3)}, not_=NA),
        dict(n='bead', g='bead', x=29, y=38, rows=BEAD, alt={'atk1|atk2': BEAD_SW, 'hit': BEAD_SW}, not_=NA),
        dict(n='bell', g='bell', x=19, y=18, rows=bell(), not_=NA),
        dict(n='face', g='bell', x=29, y=26, rows=face('open'), alt={'blink': face('blink'), 'atk0': face('fight'), 'atk1|atk2': face('shout'), 'hit': face('pain')}, not_=NA),
        dict(n='windA', g='root', x=14, y=46, rows=WIND_A, only='idle0|idle1|walk0|walk1'),
        dict(n='windB', g='root', x=40, y=48, rows=WIND_B, only='idle2|idle3|walk2|walk3'),
        dict(n='wave1', g='root', x=49, y=20, rows=wave(13), only='atk1'),
        dict(n='wave1b', g='root', x=55, y=17, rows=wave(19), only='atk1'),
        dict(n='gust1', g='root', x=50, y=37, rows=GUST, only='atk1'),
        dict(n='flake1', g='root', x=62, y=30, rows=FLAKE, only='atk1'),
        dict(n='wave2', g='root', x=55, y=17, rows=wave(19), only='atk2'),
        dict(n='wave2b', g='root', x=62, y=14, rows=wave(25), only='atk2'),
        dict(n='gust2', g='root', x=56, y=40, rows=GUST, only='atk2'),
        dict(n='flake2', g='root', x=69, y=26, rows=FLAKE, only='atk2'),
        dict(n='flake3', g='root', x=67, y=47, rows=FLAKE, only='atk2'),
        dict(n='ko', g='root', x=8, y=31, rows=ko_body(), only='ko'),
    ]

def ko_body():
    """横だおし（反時計回り 90度：口が 右）。舌の ひもが たれて、短冊は 地面に ぺたり"""
    W, H = 29, 33; g = grid(W, H)
    stamp(g, LOOP, 11, 0); stamp(g, bell(), 0, 6); stamp(g, face('ko'), 10, 13)
    stamp(g, ['..Z..'] + BEAD[1:5], 10, 26)
    r = rows_of(g)
    for _ in range(3): r = rot90(r)
    G = [list(x) for x in r]; h, w = len(G), len(G[0])
    zy, zx = next((y, x) for y in range(h) for x in range(w) if G[y][x] == 'Z'); G[zy][zx] = 'R'
    out = grid(w + 16, h + 2); stamp(out, rows_of(G), 0, 0)
    # ひも：玉から 右へ 出て 地面まで たれる
    pts = [(zx + 1, zy), (zx + 2, zy + 1), (zx + 3, zy + 2), (zx + 3, zy + 3)] + [(zx + 4, y) for y in range(zy + 4, h - 3)]
    for x, y in pts: out[y][x] = 'r'
    tz = [x for x in rot90(tanzaku(0)) if x.strip('.')]
    tz = [x.lstrip('.') if False else x for x in tz]
    stamp(out, [x[::-1].rstrip('.') for x in tz][::-1], zx + 2, h - 8)
    return [''.join(x).rstrip('.') for x in out]

FRAMES = {
    'idle0': {}, 'idle1': {'bell': (0, -1), 'bead': (0, -1)}, 'idle2': {'bell': (0, -1), 'bead': (0, -1), 'tail': (0, -1)}, 'idle3': {'tail': (0, -1)}, 'blink': {},
    'walk0': {'root': (0, -1)}, 'walk1': {'root': (1, -3)}, 'walk2': {'root': (0, -2)}, 'walk3': {'root': (1, -1)},
    'atk0': {'root': (-3, 1)}, 'atk1': {'root': (3, -1), 'bead': (1, 0)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, -1)}, 'ko': {},
}
PARENT = {'bell': 'root', 'bead': 'root', 'tail': 'bead'}
