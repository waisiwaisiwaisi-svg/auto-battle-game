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
    poly(p, [(19, 61), (22, 54), (24, 42), (25, 30), (24, 20), (40, 20), (39, 30), (37, 42), (39, 53), (44, 61)], '1')
    oval(p, 31, 26, 8, 7, '1')
    s = shade(p, RB, r=2)
    # 木の すじ（縦の みぞ）
    for (x0, y0, x1, y1) in ((27, 40, 26, 58), (34, 44, 36, 58), (30, 46, 30, 56)):
        line(s, x0, y0, x1, y1, 'D')
    for (x0, y0, x1, y1) in ((28, 40, 27, 56), (31, 46, 31, 55)):
        line(s, x0, y0, x1, y1, 'A')
    g = ink(s)
    # 口：幹の うろが 裂けて ぎざぎざの 歯
    put(g, 27, 33, ['kkkkkkkkkk', 'kUkUkkUkUk', '.kkrrrrkk.', '.kUkkkUk..', '..kkkkk...'])
    return g
def roots(side):
    p = G()
    if side == 0: tube(p, [(24, 57), (16, 59), (10, 60)], [3, 2, 1], '1'); tube(p, [(23, 59), (18, 61)], [2, 1], '1')
    else: tube(p, [(38, 57), (46, 59), (52, 60)], [3, 2, 1], '1'); tube(p, [(39, 59), (44, 61)], [2, 1], '1')
    return ink(shade(p, RB, r=1, hi=.15, lo=-.2))

# ---------- 垂れ枝の 髪：葉の すじ（左ほど 明るい ふち）----------
CROWN = [(26, 13, 18, 9), (16, 11, 9, 7), (30, 7, 10, 6), (40, 12, 7, 6)]
def crown():
    p = G()
    for c in CROWN: oval(p, *c, '2')
    s = shade(p, RB, r=3, hi=.3, lo=-.25)
    # 葉の 房の 切れこみ（下向きの 暗い v）
    for (x, y) in ((14, 9), (22, 7), (30, 5), (38, 9), (20, 14), (30, 12), (12, 16), (36, 16), (26, 18)):
        dots(s, 'H', [(x, y), (x + 1, y + 1), (x + 2, y)])
        if s[y - 1][x + 1] in 'FH': s[y - 1][x + 1] = 'E'
    return ink(s)
def strands(sway=0, front=False):
    p = G()
    # (x, 下の はし)：顔の 前は 短く、後ろ・左は 長い
    S = [(9, 40), (11, 48), (13, 52), (16, 50), (18, 54), (21, 46), (24, 32)] if not front else [(38, 30), (41, 40), (43, 44), (45, 34)]
    for i, (x, y1) in enumerate(S):
        y0 = 14 if not front else 17
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0)
            xx = x + round(sway * t * t * 2) + (1 if (y // 5 + i) % 3 == 0 else 0)
            w = 2 if t < .7 else 1
            for d in range(w):
                c = 'E' if d == 0 and (y + i) % 3 else 'F'
                if t > .6 and d == 0: c = 'F' if (y + i) % 2 else 'H'
                if 0 <= xx + d < 64: p[y][xx + d] = c
    return ink(p)

# ---------- 見せ所：垂れ枝の 腕と 大きな かぎ爪 ----------
def arm(back=False, reach=0):
    p = G()
    if not back:
        path = [(38, 18), (46, 13), (53, 15), (56, 22 + reach), (57 + reach, 32 + reach)]
        tube(p, path, [3, 2.6, 2.2, 2, 1.8], '1')
    else:
        path = [(14, 20), (8, 22), (5, 30), (5, 38)]
        tube(p, path, [2.6, 2.2, 1.8, 1.6], '1')
    s = shade(p, RB, r=1, hi=.15, lo=-.2)
    # 枝から 垂れる 葉
    if not back:
        for (x, y0, y1) in ((45, 15, 26), (49, 15, 30), (52, 17, 24)):
            for y in range(y0, y1): s[y][x] = 'E' if y % 3 else 'F'
    g = ink(s)
    if back: recol(g, {'A': 'B', 'B': 'D'})
    return g
CLAW = [   # 3本の かぎ爪（下へ 曲がる）
    '..kkkkkk....',
    '.kBBBBBBkk..',
    'kBkkBkkBBBk.',
    'kUkkUkk.kUk.',
    'kUUkkUUk.kUk',
    'kUXk.kUXk.kUk',
    '.kUXk.kUXk.kUk',
    '.kUXk..kUXk.kXk',
    '..kXk...kUXkkXk',
    '..kXk....kXk.kk',
    '...kk....kXk...',
    '..........kk...',
]
CLAW_BACK = [
    '.kkkkk..',
    'kDDDDDk.',
    'kXkXkXk.',
    'kXkkXkXk',
    '.kXk.kXk',
    '.kXk..kk',
    '..kk....',
]
EYE = ['kk.......kk', '.kkk...kkk.', '.kYYk.kYYk.', '..kkk.kkk..']   # つり上がる 光る 目（まゆ つき）
EYE_ALT = {'blink': ['kk.......kk', '.kkk...kkk.', '..kkk.kkk..', '...........'],
           'atk0|atk1|atk2': ['kk.......kk', '.kkk...kkk.', '.kYrk.krYk.', '..kkk.kkk..'],
           'hit': ['...........', 'k.k.....k.k', '.kkk...kkk.', '...........']}
WISP = ['.k.', 'kCk', 'kWk', '.k.']
WISP2 = ['..k', '.kC', 'kWk', '.k.']
SLASH = ['.......C', '......CW', '....CWC.', '..CWC...', '.CW.....', 'C.......']

def full_tree(eye='ko'):
    """ダウン用：木 全体を 1枚に（右へ 倒れる → 90度 回す）"""
    g = G()
    for L in [arm(True), roots(0), roots(1), trunk(), crown(), strands(), arm(), strands(0, True)]:
        stamp(g, rows_of(L), 0, 0)
    stamp(g, CLAW, 51 + 1, 31); stamp(g, CLAW_BACK, 2, 37)
    stamp(g, ['kk...kk..k.k', '.k.k.....k..', '..k.....k.k.'], 28, 26)
    return g

def layers():
    KO = rot90(rows_of(full_tree()))
    KO = [r for r in KO]
    return [
        dict(n='armB', g='armB', x=0, y=0, rows=rows_of(arm(True)), not_='ko'),
        dict(n='clawB', g='armB', x=2, y=37, rows=CLAW_BACK, not_='ko'),
        dict(n='strB', g='hair', x=0, y=0, rows=rows_of(strands()), alt={'idle1|idle2|walk1|walk3|hit': rows_of(strands(-1))}, not_='ko'),
        dict(n='rootL', g='legA', x=0, y=0, rows=rows_of(roots(0)), not_='ko'),
        dict(n='rootR', g='legB', x=0, y=0, rows=rows_of(roots(1)), not_='ko'),
        dict(n='trunk', g='body', x=0, y=0, rows=rows_of(trunk()), not_='ko'),
        dict(n='eye', g='head', x=26, y=24, rows=EYE, alt=EYE_ALT, not_='ko'),
        dict(n='crown', g='head', x=0, y=0, rows=rows_of(crown()), not_='ko'),
        dict(n='arm', g='arm', x=0, y=0, rows=rows_of(arm()), alt={'atk1|atk2': rows_of(arm(False, 3))}, not_='ko'),
        dict(n='claw', g='arm', x=51, y=31, rows=CLAW, alt={'atk1|atk2': CLAW}, not_='ko'),
        dict(n='strF', g='hair', x=0, y=0, rows=rows_of(strands(0, True)), alt={'idle1|idle2|walk1|walk3|hit': rows_of(strands(-1, True))}, not_='ko'),
        dict(n='wisp1', g='fx', x=4, y=6, rows=WISP, alt={'idle1|idle3|walk1|walk3': WISP2}, not_='ko'),
        dict(n='wisp2', g='fx', x=46, y=3, rows=WISP2, alt={'idle1|idle3|walk1|walk3': WISP}, not_='ko'),
        dict(n='slash', g='arm', x=56, y=24, rows=SLASH, only='atk1'),
        dict(n='ko', g='root', x=-4, y=10, rows=KO, only='ko'),
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
