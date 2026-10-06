# カマイタチ（かぜ・はがね × イタチの 妖怪）手打ち GBA風
import pix
META = dict(id='kamaitachi', name='カマイタチ', types=['wind', 'steel'], base='イタチ（妖怪）', size='M')
PAL = {
    'k': '#101018', 'l': '#4a2418',
    'A': '#f2a456', 'B': '#bc662e', 'C': '#6c3420',
    'W': '#fff0c8',
    'S': '#f6faff', 'T': '#a6b2ca', 'U': '#566080',
    'V': '#c4fff2', 'X': '#3ebcb4',
    'E': '#ff2848',
}
LIGHT = set('AWSV')

def shade(rows, ramps, low=99):
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); o = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            m = g[y][x]
            if m not in ramps: continue
            hi, mid, lo = ramps[m]
            def e(dy, dx):
                yy, xx = y + dy, x + dx
                return not (0 <= yy < H and 0 <= xx < W) or g[yy][xx] != m
            a = e(-1, 0) or e(-2, 0) or (e(0, -1) and y < low)
            b = e(1, 0) or e(0, 1) or e(1, 1) or e(0, 2)
            c = lo if y >= low else mid
            if a and not b: c = hi
            elif b and not a: c = lo
            o[y][x] = c
    return pix.rows_of(o)
def put(base, over, x=0, y=0):
    g = pix.grid_of(base); w = max(len(r) for r in over) + x; h = len(over) + y
    if w > len(g[0]): g = [r + ['.'] * (w - len(r)) for r in g]
    while len(g) < h: g.append(['.'] * len(g[0]))
    pix.stamp(g, over, x, y); return pix.rows_of(g)
DARK = {'A': 'B', 'B': 'C', 'C': 'l', 'W': 'A', 'S': 'T', 'T': 'U', 'U': 'l'}
def dark(rows): return pix.recolor(rows, DARK)
def notop(r): return ['.' * len(r[0])] + r[1:]

# ---- 胴：細長く しなやか。腹は クリーム色 ----
BODY_M = [
    '..........###########.............',
    '.......#################..........',
    '.....#######################......',
    '...############################...',
    '..##############################..',
    '.################################.',
    '.#################################',
    '##################################',
    '##################################',
    '.%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##',
    '..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#..',
    '....%%%%%%%%%%...........%%%%%....',
]
BODY = pix.outline(put(shade(BODY_M, {'#': 'ABC', '%': 'WWB'}), [
    '', '', '',
    '........C......C......C',
    '.......C......C......C',
    '......C......C......C',
]))
NECK_M = [
    '.....#####.',
    '....######.',
    '....######.',
    '...######..',
    '...######..',
    '..######...',
    '..#####%%..',
    '.#####%%%..',
    '.####%%%%%.',
    '####%%%%%%.',
    '###%%%%%%%%',
    '##%%%%%%%%%',
]
NECK = notop(pix.outline(shade(NECK_M, {'#': 'ABC', '%': 'WWB'})))

HLEG_M = [
    '..#####..',
    '.#######.',
    '#########',
    '#########',
    '#########',
    '.#######.',
    '..#####..',
    '..####...',
    '..###....',
    '..###....',
    '..###....',
    '.#####...',
]
HLEG = notop(pix.outline(put(shade(HLEG_M, {'#': 'ABC'}), ['', '', '', '', '', '', '', '', '', '', '', '.k.k.'])))

# ---- 頭（手打ち）：黒い くまどりの 中に 赤い 目、細い 牙 ----
HEAD = [
    '..kk............',
    '.kAAkkkkkk......',
    '.kAABBBBBBkkk...',
    'kAABBBBBBBBBBkk.',
    'kABkkkkkkBBBBBBk',
    'kABCCCCCkkBBBBBk',
    'kBBBCCCBBBBBBkkk',
    'kBBBBBWWWWWWkSk.',
    '.kBBWWWWWWWWkk..',
    '..kkWWWWWWWk....',
    '....kkkkkkk.....',
]
HEAD_OPEN = HEAD[:6] + [
    'kBBBCCCBBBBBBkkk',
    'kBBBBBWWWWkSkSk.',
    '.kBBWWWWWkllll..',
    '..kkWWWWWWkSkSk.',
    '....kkkkkkkkk...',
]
EYE = ['kEEk']
EYE_ALT = {'blink': ['kkkk'], 'hit': ['kCkC'], 'atk0|atk1|atk2': ['EEEE'], 'ko': ['CkCk']}

# ---- 鎌の 腕：毛の 前腕から 三日月の 刃（上が 刃、下が みね）----
ARM = [
    '.......................kk.',
    '......................kSk.',
    '.....................kSTk.',
    '....................kSTk..',
    '...................kSTUk..',
    '..................kSTUk...',
    '................kkSTUk....',
    '..............kkSSTUk.....',
    '...........kkkSSTTUk......',
    '.kkkk...kkkSSSTTUUk.......',
    'kAABBkkkSSSSTTUUkk........',
    'kABBCkSSSSTTUUkk..........',
    'kBBCCkTTTUUUkk............',
    '.kBCkkUUkkkk..............',
    '.kBCk.kk..................',
    '.kkk......................',
]
# ふりおろした 鎌（攻撃）
ARM_SWING = [
    '.kkkk................',
    'kAABBk...............',
    'kABBCk...............',
    'kBBCCkkkkkkk.........',
    '.kBCkSSSSSSSkkkk.....',
    '.kBCkTTTTTTSSSSSkkk..',
    '..kkkUUUUUTTTTTTSSSk.',
    '.....kkkkkUUUUUTTTTk.',
    '..........kkkkkUUUk..',
    '...............kkk...',
]
# 地面に つき立てた 奥の 鎌
FAR_ARM = [
    '.kkkk.....',
    'kBBBCk....',
    'kBBCCk....',
    '.kBCk.....',
    '.kBCk.....',
    '.kTTkk....',
    '.kTTUk....',
    '..kTUk....',
    '..kTUUk...',
    '...kTUk...',
    '...kTUUk..',
    '....kUUk..',
    '.....kk...',
]
EAR = ['k....', 'kAk..', 'kABk.', 'kABBk', '.kkk.']
# 背の 鋼の ひれ（小さな 鎌）
FIN = [
    'kk.....',
    'kSkk...',
    'kSTTkk.',
    '.kSTTUk',
    '.kSTUUk',
    '..kTUUk',
]

# ---- しっぽ：太い 房が 後ろから 上へ 弧を 描き、先に 小さな 竜巻 ----
def tail():
    import math
    W, H = 18, 26; g = pix.grid(W, H)
    for i in range(120):
        t = i / 119; th = math.pi * (0.5 + 1.25 * t)
        cx, cy, r = 10, 13, 9.5
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        w = 4.4 - 1.8 * t
        for y in range(H):
            for x in range(W):
                if (x + .5 - px) ** 2 + (y + .5 - py) ** 2 <= w * w: g[y][x] = '#'
    s = pix.grid_of(shade(pix.rows_of(g), {'#': 'ABC'}))
    for (x, y) in ((3, 12), (4, 8), (6, 5), (2, 16), (5, 19)):
        if s[y][x] == 'B': s[y][x] = 'C'
    return pix.outline(pix.rows_of(s))
TAIL = tail()
SWIRL = [
    '.kkkkkkkkkk.',
    'kVVVVXXVVVVk',
    '.kXXVVVVXXk.',
    '..kVVXXVVk..',
    '...kXVVXk...',
    '....kVXk....',
    '.....kk.....',
]
SWIRL2 = [
    '.kkkkkkkkkk.',
    'kXXVVVVXXVVk',
    '.kVVXXVVVVk.',
    '..kXVVVXXk..',
    '...kVXVVk...',
    '....kXVk....',
    '.....kk.....',
]
# 体の まわりの 風の すじ
GUST = ['..kkkkk....', '.kVVVVVkk..', 'kXXkkkVVVk.', '.kk...kXXXk', '.......kkk.']
GUST2 = ['....kkkk...', '.kkkVVVVk..', 'kVVVkkXXVk.', '.kXXk..kXk.', '..kk....k..']

# ---- 風の 刃（攻撃）：大きな 三日月 ----
def slash(r1=11, r2=8, cut=0):
    W, H = 18, 26; g = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            d1 = ((x + .5 - 2) ** 2 + (y + .5 - 13) ** 2) ** .5
            d2 = ((x + .5 + 2) ** 2 + (y + .5 - 13) ** 2) ** .5
            if d1 <= r1 + 3 and d2 > r2 + 3 and y >= cut: g[y][x] = 'V' if d1 < r1 + 1.5 else 'X'
    return pix.outline(pix.rows_of(g))
SLASH = slash(); SLASH2 = slash(11, 10, 6)

NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=2, y=17, rows=TAIL),
        dict(n='swirl', g='tail', x=14, y=13, rows=SWIRL, alt={'idle1|idle3|walk1|walk3|atk1': SWIRL2}),
        dict(n='hlegF', g='legB', x=18, y=47, rows=dark(HLEG), not_='ko'),
        dict(n='farm', g='legB', x=43, y=47, rows=dark(FAR_ARM), not_='ko'),
        dict(n='fin1', g='body', x=17, y=31, rows=FIN),
        dict(n='fin2', g='body', x=24, y=30, rows=FIN),
        dict(n='fin3', g='body', x=31, y=31, rows=FIN),
        dict(n='body', g='body', x=9, y=35, rows=BODY),
        dict(n='hleg', g='legA', x=10, y=47, rows=HLEG, not_='ko'),
        dict(n='neck', g='head', x=36, y=26, rows=NECK),
        dict(n='ear', g='head', x=41, y=14, rows=EAR),
        dict(n='head', g='head', x=42, y=17, rows=HEAD, alt={NB: HEAD_OPEN}),
        dict(n='eye', g='head', x=46, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='arm', x=40, y=31, rows=ARM, alt={NB: ARM_SWING}, not_='ko'),
        dict(n='slash', g='arm', x=58, y=22, rows=SLASH, alt={'atk2': SLASH2}, only=NB),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'arm': (0, -1)},
    'idle2': {'body': (0, 1)},
    'idle3': {'body': (0, 0), 'arm': (0, 1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'root': (-2, 0), 'body': (0, 1), 'head': (-1, 1), 'arm': (-3, -4)},
    'atk1': {'root': (4, 0), 'arm': (3, 6), 'head': (1, 0)},
    'atk2': {'root': (6, 0), 'arm': (3, 8)},
    'hit': {'root': (-3, 0), 'head': (-2, -1), 'arm': (-3, -1)},
    'ko': {'body': (0, 12), 'head': (2, 4), 'tail': (0, 0)},
}
PARENT = {'head': 'body', 'arm': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root'}
