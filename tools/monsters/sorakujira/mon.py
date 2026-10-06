# ソラクジラ（かぜ・みず × クジラ）手打ち GBA風・デフォルメ（大きな 頭と 口が 体の 大半、うしろは 短く しぼって 飛行船の 尾翼）
META = dict(id='sorakujira', name='ソラクジラ', types=['wind', 'water'], base='クジラ', size='L')
EYE_BOX = (34, 22, 10, 9)
PAL = {
    'k': '#101018', 'l': '#1c2a50',
    'B': '#94d0f4', 'C': '#4a88cc', 'D': '#28488a',      # 体（空色）
    'V': '#f0f4f8', 'W': '#a4b4cc',                      # 下あご（うね）
    'G': '#ffe070', 'H': '#c0862a',                      # 真ちゅう（帯・プロペラ・目）
    'R': '#d23a52', 'E': '#5a1428',                      # 口の 中
    'A': '#c4f2ff', 'w': '#ffffff',                      # 風・しぶき
    'I': '#5a7cff', 'J': '#1c249c',                      # 目（こい 青の 虹彩 明・暗）
}
KEEP_BLACK = set('wIJ')
LIGHT = set('BVGAw')
import pix
# ---- 下書き用の 小道具（あたりの マスク → 左上 光の 3段階 → 手打ちの 仕上げ → 輪郭）----
def M(W, H, *sh):
    """('e',ch,cx,cy,rx,ry) だ円 / ('p',ch,[(x,y),...]) 多角形 / ('r',ch,x0,y0,x1,y1) 四角。ch='.' で けずる"""
    g = pix.grid(W, H)
    for s in sh:
        if s[0] == 'e': pix.ellipse(g, *s[2:], s[1])
        elif s[0] == 'p': pix.poly(g, s[2], s[1])
        elif s[0] == 'r':
            for y in range(s[3], s[5] + 1):
                for x in range(s[2], s[4] + 1): g[y][x] = s[1]
    return g
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
    """マスクに 陰影 → 手打ちの 上がき（rows, x, y）→ 輪郭"""
    shade(g, ramps, lw, dw)
    for rows, x, y in over: pix.stamp(g, rows, x, y)
    r = pix.rows_of(g)
    return pix.outline(r) if ol else r
def opentop(rows, n=1):
    """体に かさなる 付け根：上の 輪郭を 消して 体の 色と なじませる"""
    return ['.' * len(r) if i < n else r for i, r in enumerate(rows)]
def dark(rows, m): return pix.recolor(rows, m)
def eye(A, B, glow='w'):
    """右向きの つり目（8x5）：まゆ／上まぶたの 線、白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ k、下まぶた"""
    base = ['kkkkk...', 'kww' + A + A + 'kkk', 'kw' + A + B + B + 'k' + A + 'k', '.k' + B * 3 + 'k' + B + 'k', '..kkkkkk']
    alt = {
        'blink': ['kkkkk...', '.kkkkkkk', '..' + '.' * 6, '........', '........'],
        'hit': ['kkkk....', '...kkkk.', '.kkk....', '...kkkk.', '........'],
        'atk0|atk1|atk2': ['kkkkk...', 'kw' + glow * 2 + A + 'kkk', 'kw' + glow + A + A + 'k' + glow + 'k', '.k' + A * 3 + 'k' + A + 'k', '..kkkkkk'],
        'ko': ['.k...k..', '..k.k...', '...k....', '..k.k...', '.k...k..'],
    }
    return base, alt
SKY = {'1': 'BCD', '2': 'VVW'}

# ---- 体（飛行船の だ円 ＝ クジラの 胴）：頭と 口が 前の 大部分 ----
MOUTH = [(18, 32), (30, 27), (55, 21)]
def body(open_=False):
    W, H = 56, 38
    g = M(W, H, ('e', '1', 32, 18, 23.5, 17.5), ('p', '1', [(14, 9), (0, 14), (0, 22), (14, 28)]))
    if not open_: jaw = M(W, H, ('p', '2', [(18, 32), (30, 27), (56, 21), (56, 40), (18, 40)]))
    else: jaw = M(W, H, ('p', '2', [(18, 33), (56, 31), (56, 40), (18, 40)]))
    for y in range(H):
        for x in range(W):
            if g[y][x] == '1' and jaw[y][x] == '2': g[y][x] = '2'
    if open_:   # 口を 大きく 開く：上あごを くさび形に 切りとって 口の 中
        cut = M(W, H, ('p', 'E', [(19, 32), (56, 10), (56, 31), (19, 33)]))
        for y in range(H):
            for x in range(W):
                if cut[y][x] == 'E' and g[y][x] != '.': g[y][x] = 'E'
    shade(g, SKY, lw=3, dw=3)
    # 飛行船の 骨組みの 帯（真ちゅう）と びょう：頭と 胴の さかい
    for x, c in ((18, 'G'), (19, 'H')):
        for y in range(H):
            if g[y][x] in 'BCDVW': g[y][x] = c if 5 < y < 31 else ('G' if y <= 5 else 'H')
    for y in (9, 15, 21, 27):
        if g[y][17] in 'BCD': g[y][17] = 'k'
    # 下あごの うね（ひだ）
    for y in range(30, H, 2):
        for x in range(22, 52):
            if g[y][x] == 'V' and (x + y) % 9 != 0: g[y][x] = 'W'
    if not open_:
        def my(x):
            for (x0, y0), (x1, y1) in zip(MOUTH, MOUTH[1:]):
                if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) // (x1 - x0)
        for x in range(19, 55):                                    # 口：上くちびる k・すき間 E・下くちびる k
            y = my(x)
            for dy, c in ((-1, 'k'), (0, 'E'), (1, 'k')):
                if g[y + dy][x] != '.': g[y + dy][x] = c
        for x in range(22, 53, 3):                                 # 牙
            y = my(x); g[y][x] = 'w'
            if x % 2 and g[y + 1][x] != '.': g[y + 1][x] = 'w'
    else:
        src = [r[:] for r in g]
        for y in range(H):
            for x in range(W):
                if src[y][x] != 'E': continue
                up = src[y - 1][x]; dn = src[y + 1][x] if y + 1 < H else '.'
                if up not in 'E.' and x % 4 == 0: g[y][x] = 'w'; g[y + 1][x] = 'w'
                elif dn in 'VW' and x % 4 == 2: g[y][x] = 'w'; g[y - 1][x] = 'w'
                elif dn in 'VW' or (y + 2 < H and src[y + 2][x] in 'VW'): g[y][x] = 'R'
    # まゆの ほね（目の 上に 張り出す 板）
    pix.line(g, 26, 9, 37, 11, 'D'); pix.line(g, 26, 8, 37, 10, 'D'); pix.line(g, 26, 7, 36, 9, 'B')
    # 光の 三日月
    for (x, y) in ((24, 3), (25, 3), (26, 2), (27, 2), (28, 2), (29, 1), (30, 1), (31, 1), (22, 4), (21, 5)):
        if g[y][x] in 'C': g[y][x] = 'B'
    # 古傷と フジツボ
    for (x, y) in ((44, 8), (45, 9), (46, 10), (8, 15), (9, 15)):
        if g[y][x] in 'BCD': g[y][x] = 'D'
    g[2][36] = 'k'; g[2][37] = 'k'                       # 潮ふき穴
    return pix.outline(pix.rows_of(g))
BODY, BODY_OPEN = body(), body(True)

# ---- 尾：飛行船の 十字の 尾翼 ＝ クジラの 尾びれ（上下に 2枚）----
def tail(ph=0):
    g = M(15, 28, ('p', '1', [(14, 10), (5, 2 - ph), (0, 0 - ph), (2, 6), (6, 13), (2, 21), (0, 27 + ph), (5, 25 + ph), (14, 18)]))
    return P(g, SKY, [(['DD', '.DDD', '..DDDD'], 3, 12)], lw=2, dw=2)
TAIL, TAIL2 = tail(), tail(1)

# ---- むなびれ ＝ プロペラ：うでは 体に 3ドット もぐり、先に ハブと 2枚の 羽 ----
ARM = opentop(P(M(9, 11, ('p', '1', [(3, 0), (9, 0), (6, 8), (3, 11), (1, 9)])), SKY, lw=1, dw=2))
PROP = [   # 縦
    '...kk...',
    '..kGHk..',
    '..kGHk..',
    '..kGHk..',
    '..kkkk..',
    '.kGHHk..',
    '.kHHHk..',
    '..kkkk..',
    '..kGHk..',
    '..kGHk..',
    '..kGHk..',
    '...kk...',
]
PROP2 = [  # ななめ
    'kk......',
    'kGkk....',
    '.kGHk...',
    '..kGHk..',
    '...kkkk.',
    '..kGHHkk',
    '..kHHHkGk',
    '...kkkkHk',
    '.....kGHk',
    '......kHk',
    '.......kk',
    '........',
]
PROP3 = [  # 横
    '............',
    '............',
    '............',
    '..kkkk......',
    'kkkGHkkkkkk.',
    'kGGGHHGGGGHk',
    'kHHHHHHHHHHk',
    'kkkkkkkkkkk.',
    '............',
]
# 目（O 傷の目）：白目＋こい 青の 虹彩（明 I・暗 J）＋丸い ひとみ。古い 傷（白っぽい 線 W）が 目を たてに 切り、
# 上下の まぶたが 傷の ところで 切れて いる。まぶたは 太く 前へ 下がる
EYE = ['......W...', '.....WW...', 'kkkkk.Wkk.', '.kkwIIWkkk', '.kwIJkWJIk', '..kJJJWJk.', '...kkk.k..', '......W...', '......W...']
EYE_ALT = {
    'blink': ['......W...', '.....WW...', 'kkkkk.Wkk.', '.kkkkkWkkk', '..DDDDWDD.', '......W...', '......W...', '......W...', '..........'],
    'hit': ['......W...', '.....WW...', 'kkkk..W...', '...kkkWk..', '.....kWkkk', '...kkkW...', '.kkk..W...', '......W...', '..........'],
    'atk0|atk1|atk2': ['......W...', '.....WW...', 'kkkkk.Wkk.', '.kwwIIWkkk', '.kwIIkWwIk', '..kIJJWIk.', '...kkk.k..', '......W...', '......W...'],
    'ko': ['......W...', '.....WW...', '..k...Wk..', '...k.kW...', '....k.W...', '...k.kW...', '..k...Wk..', '......W...', '..........'],
}
# 潮ふき（みず）：穴から 立つ 水の 柱（付け根は 穴に つながる）
SPOUT = ['.k.kk.k.', 'kAkAAkAk', '.kAwAAk.', '..kAAk..', '..kAwk..', '...kk...']
SPOUT2 = ['..k..k..', '.kAkkAk.', '..kAAk..', '..kwAk..', '...kk...']
# 攻撃：口から 吹きだす 突風（エフェクト）
GUST = [
    '...kkkkkkk....',
    '.kkAAAAAAAkk..',
    'kAAwwwkkkAAAk.',
    '.kk...kAAkkAAk',
    '..kkkkAAk..kAk',
    '.kAAAAAk...kAk',
    'kAwwkkk...kAk.',
    '.kAAAAkkkkAk..',
    '..kkkkAAAAk...',
    '......kkkk....',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='tail', g='tail', x=0, y=15, rows=TAIL, alt={'idle1|idle2|walk1|walk2': TAIL2}),
        dict(n='body', g='body', x=5, y=12, rows=BODY, alt={NB: BODY_OPEN}),
        dict(n='spout', g='spout', x=38, y=8, rows=SPOUT, alt={'idle1|idle3|walk1|walk3': SPOUT2}, not_='ko|hit|atk0'),
        dict(n='eye', g='body', x=34, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='arm', g='fin', x=27, y=44, rows=ARM),
        dict(n='prop', g='fin', x=23, y=52, rows=PROP, alt={'idle1|idle3|walk1|walk3|atk1|hit': PROP2, 'idle2|walk2|atk2': PROP3}),
        dict(n='gust', g='fx', x=60, y=24, rows=GUST, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1)}, 'idle3': {}, 'blink': {},
    'walk0': {'root': (0, 0), 'tail': (0, -1)}, 'walk1': {'root': (1, -1)}, 'walk2': {'root': (1, -2), 'tail': (0, 1)}, 'walk3': {'root': (0, -1)},
    'atk0': {'root': (-3, 1), 'tail': (1, 0)}, 'atk1': {'root': (2, 0), 'fx': (0, 0)}, 'atk2': {'root': (4, 0), 'fx': (1, 0)},
    'hit': {'root': (-4, -1), 'tail': (1, 1)}, 'ko': {'_flip': True},
}
PARENT = {'tail': 'body', 'spout': 'body', 'fin': 'body', 'body': 'root', 'fx': 'root'}
