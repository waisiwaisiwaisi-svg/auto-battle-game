# ヌケガラゼミ（むし・ゴースト × セミ）手打ち GBA風・デフォルメ（2〜3頭身：大きな 頭と 目、腹は 小さく 丸く、背の 裂け目から 霊火の 翅）
META = dict(id='nukegarazemi', name='ヌケガラゼミ', types=['bug', 'ghost'], base='セミ', size='M')
PAL = {
    'k': '#101018', 'l': '#3e2414',
    'F': '#f6ca78', 'G': '#c47e36', 'H': '#6c3c1c',      # 抜け殻（こはく色）
    'P': '#d4f6ff', 'Q': '#7cc6f4', 'U': '#5a58d0',      # 霊火（明・中・ふち）
    'E': '#24122e',                                      # 殻の 中の からっぽの 闇
    'R': '#ff6a7a', 'S': '#a81a48',                      # 目（明・暗）
    'w': '#ffffff',
}
LIGHT = set('FPw')
KEEP_BLACK = set('wPQU')
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
AMBER = {'1': 'FGH'}
DK = {'F': 'G', 'G': 'H', 'H': 'l', 'w': 'G'}

def flame(W, H, polys):
    """霊火：舌の 形を 重ね、ふち U → Q → 芯 P"""
    g = pix.grid(W, H)
    for pts in polys:
        m = pix.grid(W, H); pix.poly(m, pts, '#')
        for y in range(H):
            for x in range(W):
                if m[y][x] != '#': continue
                r = 9
                for d in range(1, 4):
                    if any(not (0 <= y + dy < H and 0 <= x + dx < W) or m[y + dy][x + dx] != '#' for dy in range(-d, d + 1) for dx in range(-d, d + 1) if max(abs(dy), abs(dx)) == d):
                        r = d; break
                g[y][x] = 'U' if r == 1 else 'Q' if r == 2 else 'P'
    return pix.outline(pix.rows_of(g))

# ---- 背の 裂け目から 立ちのぼる 霊火の 翅（見せ所）：うしろ上へ なびく 3枚の 炎 ----
FIRE = [
    '.k........................',
    'kUk.......k...............',
    'kQUk.....kUk..............',
    '.kQUk...kQUk.......k......',
    '.kPQUk..kQQUk.....kUk.....',
    '..kPQUk.kPQUk....kQUk.....',
    '..kPPQUkkPQQUk..kQQUk.....',
    '...kPPQUkPPQUk.kQPQUk.....',
    '...kPPPQkPPQQUkkQPQUk.....',
    '..kQPPPQQPPPQUkQPPQUk.....',
    '.kQPPPPPQPPPQQkQPPQUk.....',
    '.kQPPPPPPPPPPQQQPPQUk.....',
    'kQPPPwPPPPPPPPQPPPQUk.....',
    'kQPPwPPPPPPPPPPPPPQUk.....',
    'kQPPPPPPPPPPPPPPPQUk......',
    '.kQPPPPPPPPPPPPPQUk.......',
    '.kQQPPPPPPPPPPPQUk........',
    '..kUQQPPPPPPPQQUk.........',
    '...kUUQQQQQQQUUk..........',
    '....kkUUUUUUUkk...........',
    '......kkkkkkk.............',
]
def sway(rows, n, d):
    """上の n 行を d ドット ずらして ゆらす"""
    return [('.' * d + r) if i < n else r for i, r in enumerate(rows)] if d > 0 else [r[-d:] + '..' if i < n else r for i, r in enumerate(rows)]
def grow(rows, keep=3):
    """炎を 大きく：輪郭を はずして 3ドットごとに 1ドット ふやし、輪郭を つけ直す"""
    g = [r.replace('k', '.') for r in rows]
    g = [''.join(c * (2 if i % keep == 1 else 1) for i, c in enumerate(r)) for r in g]
    out = []
    for j, r in enumerate(g): out += [r] * (2 if j % keep == 1 else 1)
    w = max(len(r) for r in out); out = [r.ljust(w, '.') for r in out]
    return pix.outline([r.strip('.') and r for r in out])[1:]
FIRE = grow(FIRE)
WINGS = FIRE
WINGS2 = sway(sway(FIRE, 6, -1), 3, -1)
WINGS_BIG = FIRE[:1] + [FIRE[1]] + FIRE[1:4] + FIRE[3:6] + FIRE[6:]   # 炎が 高く 立つ
# 裂け目の 手前に こぼれる 霊火（頭の 上に かさなる）
WISP = ['..k.....k..', '.kPk..kkQk.', '.kPQkkPQk..', 'kQPPQPPQk..', 'kQPPPPQk...', '.kkkkkk....']
WISP2 = ['.k.....k...', 'kQk..kkPk..', '.kPkkPQk...', 'kQPPQPPQk..', 'kQPPPPQk...', '.kkkkkk....']

# ---- 頭（大きい）：前は 平たい 顔に 横すじ、上に 目の ふくらみ、背に ぎざぎざの 裂け目 ----
HEAD = P(M(24, 21, ('e', '1', 12, 11, 12, 10), ('r', '1', 12, 6, 23, 19), ('e', '1', 15, 5, 7, 5)), AMBER, [
    (['..FFF', '.F', 'F'], 4, 3),
    (['H', 'H.', 'H', 'H.', 'H', 'H.'], 21, 11),            # 顔の 横すじ（セミの 顔）
    (['HH', '.', 'HH', '.', 'HH'], 22, 11),
    (['EEEE.', 'EEEEEE', '.EEEEEE.', '..EEEEEE', '...E.EEE', '.....E.E'], 0, 2),   # 背の 裂け目（中は からっぽの 闇）
], lw=2, dw=3)
EYE, EYE_ALT = eye('R', 'S')
MOUTH = ['kk', 'kwk', '.kwk', '..kk']                          # 口の 針（ストロー）

# ---- 腹（小さく 丸い 殻、節の 輪、裂け目が 続く）----
ABD = P(M(22, 17, ('e', '1', 12, 8.5, 10, 8.5), ('p', '1', [(4, 4), (0, 9), (4, 14)])), AMBER, [
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 6, 4),
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 11, 3),
    (['.H', 'H.', 'H.', 'H.', 'H.', 'H.', '.H'], 16, 4),
    (['...EEEEE', '.EEEEEE', 'EEEE.E', '.E'], 12, 0),
], lw=2, dw=3)

# ---- 前足：ほり返す ための 大きな かぎ爪（ももの 下に とげ）----
CLAW = [
    'kkkkk...........',
    'FFFFFkkkk.......',
    'FFFFFFFFFkkk....',
    'GGGFFFFFFFFFkk..',
    'kkkGGGGGGFFFFFk.',
    '...kwkwkkGGGGFk.',
    '....k.k..kkGGFk.',
    '..........kGFk..',
    '.........kGGFk..',
    '........kwGGk...',
    '.......kwwGk....',
    '.......kwwk.....',
    '........kk......',
]
CLAW_UP = [
    '.........kk.....',
    'kkkkk...kwwk....',
    'FFFFFkkkkwwk....',
    'FFFFFFFFkGwk....',
    'GGGFFFFFkGGk....',
    'kkkGGGGFFGk.....',
    '...kwkwkGGk.....',
    '....k.k.kk......',
]
CLAW_N = CLAW; CLAW_F = dark(CLAW, DK)
SLEG = ['kGGk', '.kGk', '.kGk', '..kGk', '..kHk', '...kk']
SLASH = [
    '..........kk',
    '........kkPk',
    '......kkPQk.',
    '....kkPQUk..',
    '..kkPQUkk...',
    'kkPQUkk.....',
    'kPUkk.......',
    'kkk.........',
]
NB = 'atk1|atk2'
def layers():
    return [
        dict(n='wings', g='wings', x=9, y=-1, rows=WINGS, alt={'idle1|idle3|walk1|walk3|atk2': WINGS2, 'atk0|atk1': WINGS_BIG}),
        dict(n='slegF', g='legB', x=13, y=46, rows=dark(SLEG, DK)),
        dict(n='clawF', g='clawF', x=37, y=36, rows=CLAW_F),
        dict(n='abd', g='body', x=7, y=30, rows=ABD),
        dict(n='sleg', g='legA', x=20, y=46, rows=SLEG),
        dict(n='head', g='head', x=27, y=18, rows=HEAD),
        dict(n='wisp', g='head', x=27, y=15, rows=WISP, alt={'idle1|idle3|walk1|walk3|atk2': WISP2}),
        dict(n='eye', g='head', x=40, y=22, rows=EYE, alt=EYE_ALT),
        dict(n='mouth', g='head', x=49, y=37, rows=MOUTH),
        dict(n='clawN', g='clawN', x=41, y=37, rows=CLAW_N, alt={'atk0': CLAW_UP}),
        dict(n='slash', g='clawN', x=55, y=28, rows=SLASH, only=NB),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -2), 'clawN': (0, 1)}, 'idle3': {'root': (0, -1)}, 'blink': {},
    'walk0': {'root': (1, 0), 'legA': (1, 0)}, 'walk1': {'root': (1, -2)}, 'walk2': {'root': (1, -3), 'legB': (1, 0)}, 'walk3': {'root': (1, -1)},
    'atk0': {'wings': (0, -3), 'root': (-2, -1), 'clawN': (-1, -6), 'clawF': (-1, -1)}, 'atk1': {'wings': (0, -3), 'root': (4, 1), 'clawN': (2, 0)}, 'atk2': {'root': (6, 1), 'clawN': (3, 1), 'clawF': (2, 0)},
    'hit': {'root': (-3, -1), 'head': (-2, -1), 'clawN': (-1, 0)}, 'ko': {'_flip': True},
}
PARENT = {'wings': 'body', 'head': 'body', 'clawN': 'head', 'clawF': 'head', 'body': 'root', 'legA': 'body', 'legB': 'body'}
