# シダレユウ（ゴースト・くさ × 柳）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp, ellipse

# ---------- 下書きの 道具（あたり用。陰影の 仕上げ・目・牙は 手で 打つ）----------
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def dots(g, ch, pts):
    for x, y in pts:
        if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def put(g, x0, y0, rows):
    """手で 打った 小さな 絵を 置く（'.' は すける）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < 64 and 0 <= x0 + i < 64: g[y0 + j][x0 + i] = c
def ink(p, keep=None):
    """色の かたまりの まわりに 黒い 輪郭"""
    g = G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
            elif p[y][x] != '.': g[y][x] = p[y][x]
    return g
def light_map(p, r=2):
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    return {(x, y): (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 for y in range(64) for x in range(64) if m[y][x]}
def shade(p, ramps, r=2, hi=.35, lo=-.3):
    """光は 左上：上と 左の ふちは 明、右下は 暗（ramps: 下書き文字 → (明, 中, 暗)）"""
    L = light_map(p, r); out = [row[:] for row in p]
    for (x, y), v in L.items():
        c = p[y][x]
        if c in ramps:
            h, m, d = ramps[c]; out[y][x] = h if v > hi else d if v < lo else m
    return out
def tube(p, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r and 0 <= x < 64 and 0 <= y < 64: p[y][x] = ch
def oval(p, cx, cy, rx, ry, ch): ellipse(p, cx, cy, rx, ry, ch)
def recol(g, mp, box=None):
    x0, y0, x1, y1 = box or (0, 0, 64, 64)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if g[y][x] in mp: g[y][x] = mp[g[y][x]]
def shift(g, dx, dy):
    o = G()
    for y in range(64):
        for x in range(64):
            if g[y][x] != '.' and 0 <= x + dx < 64 and 0 <= y + dy < 64: o[y + dy][x + dx] = g[y][x]
    return o
from pix import rot90

META = dict(id='shidareyuu', name='シダレユウ', types=['ghost', 'grass'], base='柳', size='M')
PAL = {
    'k': '#101018', 'l': '#1c2c26',
    'A': '#a89a86', 'B': '#6c5e54', 'D': '#3a3232',      # 幹（白っぽい 古木）
    'E': '#c4eeb0', 'F': '#74b07a', 'H': '#35604a',      # 垂れ葉（青白い 緑）
    'W': '#effff6', 'C': '#7ef0c4',                      # 霊火
    'Y': '#f4ff6a', 'r': '#e83050',                      # 目
    'U': '#ece4cc', 'X': '#9c9078',                      # 爪
}
LIGHT = set('AEWCYU')
KEEP_BLACK = set('YWCr')
RB = {'1': 'ABD', '2': 'EFH', '3': 'UUX'}

def trunk():
    p = G()
    # 前へ かがむ 幹（上が 右へ ずれる）
    poly(p, [(18, 61), (22, 54), (24, 44), (26, 32), (27, 20), (42, 18), (42, 30), (39, 44), (40, 53), (45, 61)], '1')
    oval(p, 35, 26, 8, 8, '1')
    s = shade(p, RB, r=2)
    for (x0, y0, x1, y1) in ((28, 42, 26, 58), (35, 44, 37, 58), (31, 46, 31, 56)):
        line(s, x0, y0, x1, y1, 'D')
    for (x0, y0, x1, y1) in ((29, 42, 27, 56), (32, 46, 32, 55)):
        line(s, x0, y0, x1, y1, 'A')
    # 顔の くぼみ（暗い うろ）
    for y in range(21, 30):
        for x in range(29, 43):
            if s[y][x] in 'AB' and ((x - 36) / 7.5) ** 2 + ((y - 25) / 4.5) ** 2 < 1: s[y][x] = 'D'
    g = ink(s)
    # 口：幹の 裂け目、ふぞろいの 木の 牙
    put(g, 29, 32, ['kk..........k', '.kkkkkkkkkkkk', '.kUkUkUkkUkUk', '..kkrrrrrrrk.', '..kUkkUkkUkk.', '...kkkkkkkk..'])
    return g
def roots(side):
    p = G()
    if side == 0: tube(p, [(24, 57), (16, 59), (10, 60)], [3, 2, 1], '1'); tube(p, [(23, 59), (18, 61)], [2, 1], '1')
    else: tube(p, [(39, 57), (47, 59), (53, 60)], [3, 2, 1], '1'); tube(p, [(40, 59), (45, 61)], [2, 1], '1')
    return ink(shade(p, RB, r=1, hi=.15, lo=-.2))

# ---------- 垂れ枝の 髪：頭の 上から 長く 垂れる 葉の すじ ----------
CROWN = [(27, 12, 14, 6), (19, 10, 7, 6), (27, 6, 8, 5), (35, 8, 6, 5), (40, 12, 4, 4)]
def crown():
    p = G()
    for c in CROWN: oval(p, *c, '2')
    s = shade(p, RB, r=3, hi=.3, lo=-.25)
    # 頭の 葉の 流れ（後ろへ なでつけた すじ）
    # 頭の てっぺんから 左右へ 流れる 髪の すじ（分け目）
    for (x0, y0, x1, y1) in ((28, 3, 20, 8), (29, 5, 15, 12), (30, 7, 19, 16), (32, 5, 38, 9), (33, 8, 41, 13), (28, 9, 25, 17)):
        line(s, x0, y0, x1, y1, 'H')
    for (x0, y0, x1, y1) in ((27, 4, 19, 9), (27, 9, 21, 13)):
        line(s, x0, y0, x1, y1, 'E')
    return ink(s)
def strands(sway=0, front=False):
    p = G()
    # (x, 上, 下)：後ろ・左は 地面まで 長い 髪、顔の 前は 短い
    S = [(8, 12, 44), (10, 10, 50), (12, 9, 55), (14, 8, 58), (16, 8, 53), (18, 8, 57), (20, 8, 49), (22, 9, 54), (24, 10, 44), (26, 12, 36)] if not front else \
        [(43, 13, 34), (45, 14, 30)]
    for i, (x, y0, y1) in enumerate(S):
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0)
            xx = x - round(t * 3) + round(sway * t * t * 2) + (1 if (y // 6 + i) % 3 == 0 else 0)
            w = 2 if t < .75 else 1
            for d in range(w):
                c = 'E' if d == 0 else 'F'
                if (y + i * 2) % 4 == 0: c = 'F' if d == 0 else 'H'
                if t > .7: c = 'F' if d == 0 and (y + i) % 2 else 'H'
                if 0 <= xx + d < 64: p[y][xx + d] = c
    return ink(p)

# ---------- 見せ所：垂れ枝の 腕と 大きな かぎ爪 ----------
def arm(back=False, reach=0):
    p = G()
    if not back:
        path = [(40, 17), (47, 12), (53, 13), (56, 19 + reach), (57 + reach, 27 + reach)]
        tube(p, path, [3.2, 2.8, 2.4, 2.2, 2.2], '1')
    else:
        path = [(18, 16), (10, 18), (6, 26), (5, 34)]
        tube(p, path, [2.6, 2.2, 1.8, 1.6], '1')
    s = shade(p, RB, r=1, hi=.15, lo=-.2)
    g = ink(s)
    if back: recol(g, {'A': 'B', 'B': 'D'})
    else:
        for (x, y0, y1) in ((46, 15, 24), (50, 14, 27)):   # 枝から 垂れる 葉
            for y in range(y0, y1): g[y][x] = 'E' if y % 3 else 'F'; g[y][x + 1] = 'k'
    return g
CLAW = [   # 3本の 長い かぎ爪（先が 前へ 曲がる）
    '...kkkkkk.......',
    '..kABBBBDkk.....',
    '.kABBBBBBDDk....',
    '.kBBkkBBkkBDk...',
    'kUUk.kUUk.kBDk..',
    'kUUk.kUUk..kUk..',
    'kUXk.kUXk..kUXk.',
    'kUXk.kUXk..kUXk.',
    'kUXk.kUXk..kUXk.',
    '.kUXk.kUXk..kUXk',
    '.kUXk.kUXk..kUXk',
    '..kXk..kUXk..kXk',
    '..kXkk..kXkk.kXk',
    '...kXk...kXk.kk.',
    '....k.....k.....',
]
CLAW_BACK = [
    '.kkkkk..',
    'kDDDDDk.',
    'kXkXkXk.',
    'kXkkXkXk',
    'kXk.kXk.',
    '.kXk.kXk',
    '.kXk..k.',
    '..k.....',
]
EYE = ['kk..........k', '.kkkk.....kkk', '..kWYYkk.kWYk', '...kkYYk.kYk.', '.....kkk..kk.']
EYE_ALT = {'blink': ['kk..........k', '.kkkk.....kkk', '..kkkkkk.kkkk', '.....kkk..kk.', '.............'],
           'atk0|atk1|atk2': ['kk..........k', '.kkkk.....kkk', '..kWYrrk.kWrk', '...kkrrk.krk.', '.....kkk..kk.'],
           'hit': ['.............', 'k...k.....k.k', '.kkkkk....kk.', '.....kk...kk.', '.............']}
WISP = ['.k.', 'kCk', 'kWk', '.k.']
WISP2 = ['..k', '.kC', 'kWk', '.k.']
SLASH = ['........CW', '......CWC.', '....CWC...', '..CWC.....', '.CW.......', 'C.........']

def full_tree(eye='ko'):
    """ダウン用：木 全体を 1枚に（右へ 倒れる → 90度 回す）"""
    g = G()
    for L in [arm(True), roots(0), roots(1), trunk(), crown(), strands(), arm(), strands(0, True)]:
        stamp(g, rows_of(L), 0, 0)
    stamp(g, CLAW, 48, 26); stamp(g, CLAW_BACK, 1, 33)
    stamp(g, ['YkY.....YkY', 'kYk.....kYk', 'YkY.....YkY'], 31, 23)
    return g

def layers():
    KO = rot90(rows_of(full_tree()))
    KO = [r for r in KO]
    return [
        dict(n='armB', g='armB', x=0, y=0, rows=rows_of(arm(True)), not_='ko'),
        dict(n='clawB', g='armB', x=1, y=33, rows=CLAW_BACK, not_='ko'),
        dict(n='strB', g='hair', x=0, y=0, rows=rows_of(strands()), alt={'idle1|idle2|walk1|walk3|hit': rows_of(strands(-1))}, not_='ko'),
        dict(n='rootL', g='legA', x=0, y=0, rows=rows_of(roots(0)), not_='ko'),
        dict(n='rootR', g='legB', x=0, y=0, rows=rows_of(roots(1)), not_='ko'),
        dict(n='trunk', g='body', x=0, y=0, rows=rows_of(trunk()), not_='ko'),
        dict(n='eye', g='head', x=29, y=22, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='crown', g='head', x=0, y=0, rows=rows_of(crown()), not_='ko'),
        dict(n='arm', g='arm', x=0, y=0, rows=rows_of(arm()), alt={'atk1|atk2': rows_of(arm(False, 3))}, not_='ko'),
        dict(n='claw', g='arm', x=48, y=26, rows=CLAW, not_='ko'),
        dict(n='strF', g='hair', x=0, y=0, rows=rows_of(strands(0, True)), alt={'idle1|idle2|walk1|walk3|hit': rows_of(strands(-1, True))}, not_='ko'),
        dict(n='wisp1', g='fx', x=4, y=6, rows=WISP, alt={'idle1|idle3|walk1|walk3': WISP2}, not_='ko'),
        dict(n='wisp2', g='fx', x=46, y=3, rows=WISP2, alt={'idle1|idle3|walk1|walk3': WISP}, not_='ko'),
        dict(n='slash', g='arm', x=56, y=16, rows=SLASH, only='atk1'),
        dict(n='ko', g='root', x=-6, y=6, rows=KO, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'head': (0, 1), 'arm': (0, 1)}, 'idle2': {'head': (0, 1), 'hair': (0, 1), 'fx': (0, -1)}, 'idle3': {'arm': (0, 1), 'fx': (0, -1)},
    'blink': {},
    'walk0': {'legA': (-1, 0), 'body': (1, 0)}, 'walk1': {'body': (1, -1)}, 'walk2': {'legB': (1, 0), 'body': (1, 0)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 0), 'arm': (-2, -3), 'armB': (0, -1)},
    'atk1': {'body': (2, 1), 'arm': (2, 2)},
    'atk2': {'body': (1, 1), 'arm': (1, 3)},
    'hit': {'body': (-3, 0), 'head': (-1, 1), 'arm': (-2, 1), 'fx': (-3, 0)},
    'ko': {},
}
PARENT = {'head': 'body', 'hair': 'head', 'arm': 'head', 'armB': 'head', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
