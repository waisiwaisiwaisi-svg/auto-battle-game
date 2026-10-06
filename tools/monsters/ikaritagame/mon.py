# イカリタガメ（むし・みず × タガメ）手打ち GBA風・デフォルメ（2〜3頭身：大きめの くさび形の 頭、平たい だ円の 背、胸から 生えた 前脚の ひざが 錨の 輪 → 錨の かぎ）
META = dict(id='ikaritagame', name='イカリタガメ', types=['bug', 'water'], base='タガメ', size='M')
EYE_BOX = (37, 21, 9, 8)
PAL = {
    'k': '#101018', 'l': '#2c2618',
    'B': '#dcc47c', 'C': '#96793e', 'D': '#4e3a1e',      # 体（どろ色）
    'I': '#d4dce8', 'J': '#828ca0', 'K': '#40465c',      # 鉄の 錨
    'A': '#a8eaff', 'W': '#3e94d4',                      # 水
    'Y': '#ffd25a', 'O': '#d08420', 'Q': '#7a3a12',     # 目（琥珀の 複眼 明・中・暗）
    'w': '#ffffff',
}
LIGHT = set('BIAYw')
KEEP_BLACK = set('wYOQ')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角 / ('t',ch,r,[(x,y),...]) 太い 線。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
        elif s[0] == 't':
            r, pts = s[2], s[3]
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                n = int(max(abs(bx - ax), abs(by - ay)) * 2) + 1
                for i in range(n + 1):
                    t = i / n; pix.ellipse(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, r, s[1]) if False else _disc(g, ax + (bx - ax) * t, ay + (by - ay) * t, r, s[1])
    return g
def _disc(g, cx, cy, r, ch):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= y < len(g) and 0 <= x < len(g[0]) and (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: g[y][x] = ch
def shade(g, ramps, lw=2, dw=2):
    H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def run(y, x, dy, dx, c):
        n = 1
        while 0 <= y + dy * n < H and 0 <= x + dx * n < W and src[y + dy * n][x + dx * n] == c: n += 1
        return n
    for y in range(H):
        for x in range(W):
            c = src[y][x]
            if c not in ramps: continue
            hi, mid, lo = ramps[c]
            if run(y, x, 1, 0, c) <= dw or run(y, x, 0, 1, c) <= dw: g[y][x] = lo
            elif run(y, x, -1, 0, c) <= lw or run(y, x, 0, -1, c) <= 1: g[y][x] = hi
            else: g[y][x] = mid
    return g
def P(g, ramps, over=(), lw=2, dw=2, ol=True):
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭（輪郭の ぶん 左上へ 1 ずれる）"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '........', '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
BUG = {'1': 'BCD'}; STEEL = {'1': 'IJK'}
DK = {'B': 'C', 'C': 'D', 'D': 'l', 'I': 'J', 'J': 'K', 'K': 'l', 'A': 'W', 'w': 'J'}

import math
def tilt(cx, cy, rx, ry, deg):
    a = math.radians(deg); return [(cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a), cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a)) for t in [i * math.pi / 24 for i in range(48)]]
# ---- 背（平たい だ円の 葉っぱ形、前を 上げて 立つ）：前に 胸の たて、羽は X字に 重なる ----
BODY = P(M(36, 26, ('p', '1', tilt(18, 13, 17.5, 8, -24))), BUG, [
    (['.....AAAA', '...AA', '.AA', 'A'], 5, 7),                         # 水に ぬれた つや
    (['..........DD', '........DD', '......DD', '....DD', '..DD', 'DD'], 9, 8),    # 羽の 重なり（X字）
    (['DD', '..DD', '....DD', '......DD', '........DD'], 11, 8),
    (['.......D', '.....DD', '...DD', '.DD', 'D'], 21, 4),             # 胸の たてと 羽の さかい
    (['BB', 'B'], 26, 3),
], lw=2, dw=3)
SIPHON = ['kkkkkk.', 'kCCCDDk', '.kkkkkk']

# ---- 頭（くさび形、前へ とがる）：大きな 目、下に 針の くちばし ----
HEAD = P(M(19, 16, ('p', '1', [(0, 6), (7, 0), (14, 1), (19, 7), (15, 12), (5, 16), (0, 12)])), BUG, [
    (['..BBB', '.B', 'B'], 2, 3),
], lw=2, dw=3)
# 目（D 複眼）：琥珀の 丸い ドーム。ななめの あみ目の すじ（暗い 色の 線）と たての 白い 反射の 帯。ひとみは ない。
# 上に 前へ 下がる 太い まゆの 線
def ceye(mode=''):
    rows = ['kk.......', '.kkkkk...', '.kwYYOkkk', 'kYwYOYOQk', 'kOwOYOQOk', 'kQOQOQOQk', '.kQOQOQk.', '..kkkkk..']
    if mode == 'atk': rows = ['k........', 'kkkkk....', '.kwwYYkkk', 'kYwwYYYOk', 'kYwYwYOYk', 'kOYOYOYOk', '.kOQOQOk.', '..kkkkk..']
    if mode == 'hit': rows = ['.........', '..kkkk...', 'kk.kwYk..', 'kYwYkOOk.', 'kOkOYkQOk', 'kQOkOQkQk', '.kQOQkQk.', '..kkkkk..']
    if mode == 'blink': rows = ['kk.......', '.kkkkk...', '.kDDDDkkk', 'kkkkkkkkk', 'kOQOQOQOk', 'kQOQOQOQk', '.kQOQOQk.', '..kkkkk..']
    if mode == 'ko': rows = ['kk.......', '.kkkkk...', '.kQOQOkkk', 'kQkQOkOQk', 'kOQkkOQOk', 'kQkOQkOQk', '.kQOQOkk.', '..kkkkk..']
    return rows
EYE = ceye()
EYE_ALT = {'blink': ceye('blink'), 'hit': ceye('hit'), 'atk0|atk1|atk2': ceye('atk'), 'ko': ceye('ko')}
BEAK = ['kkk...', 'kCCkk.', '.kCDDk', '..kDwk', '...kwk', '....kk']

# ---- 前脚（見せ所）：胸から 生えた 太い もも → ひざ ＝ 錨の 輪 → 錨の 柄（すね）→ 2本の かぎ爪 ----
ANCHOR = [
    '.....kkkkk.....',
    '....kIIIJJk....',
    '...kIIkkkJJk...',
    '...kIk...kJk...',
    '...kIJkkkJKk...',
    '....kIJJJKk....',
    '.kkkkkIJJkkkkk.',
    'kIIIIIIIJJJJJKk',
    '.kkkkkIJKkkkkk.',
    '.....kIJKk.....',
    '.....kIJKk.....',
    '.....kIJKk.....',
    '.....kIJKk.....',
    'kk...kIJKk...kk',
    'kwk..kIJKk..kwk',
    'kIJk.kIJKk.kJKk',
    'kIJKkkIJKkkJKKk',
    '.kIJJkIJKkJJKk.',
    '..kIJJIJJJJKk..',
    '...kkIJJJKkk...',
    '.....kkkkk.....',
]
ANCHOR_SWING = pix.rot90(pix.rot90(pix.rot90(ANCHOR)))   # 前へ ふり出す（90度）
def femur(tip):
    g = M(22, 13, ('t', '1', 3.2, [(3.5, 9), tip]))
    return P(g, BUG, [(['.BBB', 'BB'], 5, 5), (['D.D.D'], 8, 9)], lw=1, dw=2)     # ももの 下に とげの すじ
FEMUR = femur((18.5, 4)); FEMUR_FWD = femur((18.5, 8.5))
JOINT = ['.kkk.', 'kBCDk', 'kCCDk', '.kkk.']                      # 胸の 付け根の 関節

# ---- 泳ぐ 足（4本 → 2本に まとめる）：短く 太く、すその 毛は 水色 ----
LEG = [
    '.kkkk....',
    'kBCCCk...',
    'kBCCDk...',
    '.kBCDk...',
    '..kBCDk..',
    '..kBCDk..',
    '..kBCDk..',
    '.kBCDk...',
    '.kBCDk...',
    'kACCAk...',
    'kAkAkAk..',
    'kkkkkkk..',
]
LEG_F = dark(LEG, DK)
SPLASH = ['....k.....k...', '...kAk...kAk..', '.k..kAk.kAk..k', 'kAkk.kAkAk.kAk', '.kAAkkWAWkkAk.', '..kAWWwWWWAk..', '...kkkkkkkk...']
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='anchorF', g='armF', x=40, y=26, rows=dark(ANCHOR, DK), not_=NB),
        dict(n='femurF', g='armF', x=30, y=23, rows=dark(FEMUR, DK), not_=NB),
        dict(n='legF', g='legB', x=13, y=48, rows=LEG_F),
        dict(n='siphon', g='body', x=1, y=50, rows=SIPHON),
        dict(n='body', g='body', x=3, y=30, rows=BODY),
        dict(n='legN', g='legA', x=20, y=48, rows=LEG),
        dict(n='head', g='head', x=31, y=19, rows=HEAD),
        dict(n='eye', g='head', x=37, y=21, rows=EYE, alt=EYE_ALT),
        dict(n='beak', g='head', x=46, y=30, rows=BEAK),
        dict(n='femur', g='arm', x=32, y=29, rows=FEMUR, alt={NB: FEMUR_FWD}),
        dict(n='joint', g='body', x=33, y=37, rows=JOINT),
        dict(n='anchor', g='arm', x=44, y=30, rows=ANCHOR, not_=NB),
        dict(n='anchorS', g='arm', x=48, y=27, rows=ANCHOR_SWING, only=NB),
        dict(n='splash', g='arm', x=52, y=48, rows=SPLASH, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1)}, 'idle2': {'body': (0, 1), 'arm': (0, 1)}, 'idle3': {'arm': (0, 1)}, 'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0), 'body': (0, -1)}, 'walk1': {'body': (0, -1), 'arm': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1), 'body': (0, -1)}, 'walk3': {'arm': (0, -1)},
    'atk0': {'body': (-1, 1), 'arm': (-1, -2), 'armF': (-1, -2)}, 'atk1': {'root': (2, 0)}, 'atk2': {'root': (3, 0), 'arm': (0, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'arm': (0, 1)}, 'ko': {'_flip': True},
}
PARENT = {'arm': 'body', 'armF': 'body', 'head': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
