# ハガネハリネズ（はがね × ハリネズミ）手打ち GBA風・デフォルメ（2〜3頭身：頭を 大きく、胴は 小さく 丸く、足は 短く 太く）
META = dict(id='haganeharinezu', name='ハガネハリネズ', types=['steel'], base='ハリネズミ', size='S')
PAL = {
    'k': '#101018', 'l': '#3a1a2c',
    'S': '#f4f6fa', 'T': '#a9b1c0', 'U': '#5a6070', 'C': '#9ef0ff',
    'F': '#c48a8a', 'G': '#8a4a5c', 'H': '#4e2438',
    'R': '#ff2e3e', 'w': '#ffffff',
    'x': '#060608',                                   # ビーズ目の 黒
}
LIGHT = set('SCFw')
KEEP_BLACK = set('wx')
EYE_BOX = (37, 38, 10, 8)   # 目と まゆ（idle0 の 64x64 座標）
import math
from pix import grid, rows_of, outline, ellipse


def _ol(g):
    H, W = len(g), len(g[0]); out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = 'k'
    return out

# ---- 刃の 針：1本ずつ 根もと・先・はばを 決めて、奥から 手前へ 重ねる（1本ごとに 輪郭）----
# 根もとは 胴の 中（背中の 弧）に 3ドット 以上 うめる。見せ所なので 長さは 元の まま
def fan(n, a0, a1, r0, L, cx=27, cy=51, w=3, jit=(0, 2, 1, 3, 0, 2, 1)):
    out = []
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        bx, by = cx + r0 * math.cos(a) * 1.5, cy - r0 * math.sin(a)
        ll = L - jit[i % len(jit)]
        out.append(((round(bx), round(by)), (round(cx + ll * math.cos(a)), round(cy - ll * math.sin(a) * 1.05)), w))
    return out
BLADES = fan(7, 152, 62, 5, 26, cx=28, cy=50) + fan(6, 146, 72, 4, 20, cx=28, cy=50)
FLARE = fan(7, 140, 56, 5, 31, cx=28, cy=50) + fan(6, 134, 66, 4, 24, cx=28, cy=50)
def quills(bl):
    W, H = 64, 64; g = [['.'] * W for _ in range(H)]
    for (bx, by), (tx, ty), w in bl:
        ax, ay = tx - bx, ty - by; L = (ax * ax + ay * ay) ** .5; ux, uy = ax / L, ay / L
        nx, ny = -uy, ux
        if nx + ny > 0: nx, ny = -nx, -ny   # n は 光（左上）の 側
        t = [['.'] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                px, py = x + .5 - bx, y + .5 - by
                a = (px * ux + py * uy) / L; d = px * nx + py * ny
                if not (-.15 <= a <= 1): continue
                hw = w * (1 - a) + .35
                if abs(d) > hw: continue
                s = d / hw
                c = 'S' if s > .3 else ('T' if s > -.35 else 'U')
                if a > .72 and s > -.2: c = 'S'
                if a < .12: c = 'U' if s < .3 else 'T'
                t[y][x] = c
        t = _ol(t)
        for y in range(H):
            for x in range(W):
                if t[y][x] != '.': g[y][x] = t[y][x]
    return g
def quill_rows(bl, k=0):
    g = quills(bl)
    # 刃先の 光：1本おきに 先から 3〜4ドット 手前を 青白く
    for i, ((bx, by), (tx, ty), w) in enumerate(bl):
        if (i + k) % 2: continue
        x, y = round(bx + (tx - bx) * .78), round(by + (ty - by) * .78)
        if g[y][x] in 'ST': g[y][x] = 'C'
    return [''.join(r) for r in g]
QUILL = quill_rows(BLADES)
QUILL2 = quill_rows(BLADES, 1)
QFLARE = quill_rows(FLARE)

# ---- 胴（小さく 丸く）----
def shade(g, ramp, lw=2, dw=3):
    L, M, D = ramp; H, W = len(g), len(g[0]); src = [r[:] for r in g]
    def fill(y, x): return 0 <= y < H and 0 <= x < W and src[y][x] == M
    for y in range(H):
        for x in range(W):
            if src[y][x] != M: continue
            dr = min(next((i for i in range(1, 9) if not fill(y + i, x)), 9), next((i for i in range(1, 9) if not fill(y, x + i)), 9) + 1)
            ul = min(next((i for i in range(1, 9) if not fill(y - i, x)), 9), next((i for i in range(1, 9) if not fill(y, x - i)), 9))
            if dr <= dw: g[y][x] = D
            elif ul <= lw: g[y][x] = L
    return g
def body():
    g = grid(22, 13); ellipse(g, 11, 6.5, 11, 6.5, 'G'); shade(g, 'FGH', 1, 3)
    for x in range(4, 16):                                   # 腹の 明るい 毛
        if g[9][x] != '.': g[10][x] = 'F'
    for (x, y) in ((4, 5), (8, 3), (12, 6), (17, 4), (21, 7)):  # 毛の あと
        if g[y][x] == 'G': g[y][x] = 'H'
    return outline(rows_of(g))
BODY = body()

# ---- 頭（大きく：たて 17 × よこ 22）----
HEAD = [
    '.......kkkkkk.........',
    '.....kkGGGGGGkk.......',
    '...kkGGGGGGGGGGkk.....',
    '..kGGGGGGGGGGGGGGk....',
    '.kGGGGGGGGGGGGGGGGk...',
    '.kGGGFFFFFFFFFFFGGGk..',
    'kGGFFFFFFFFFFFFFFFGGk.',
    'kGFFFFFFFFFFFFFFFFFGGkk',
    'kGFFFFFFFFFFFFFFFFFFGUk',
    'kGFFFFFFFFFGGGGGGGGGkkk',
    'kHGFFFFFFkkkkkkkkkkkk..',
    'kHGFFFFFkwkwkkwkkwk....',
    '.kHGFFGkHkHHHHkwHk.....',
    '.kHHGGGGkkkkkkkkk......',
    '..kHHHGGGHHk...........',
    '...kkHHHHHkk...........',
    '.....kkkkk.............',
]
# 目（S：ビーズ目＋太い まゆ）：小さく 真っ黒な ビーズ目（x）に 強い 白の ハイライト 1点。その 上に 鉄色（S／T／U）の 太い まゆが 前へ ななめに さがって 怖く にらむ
BROW = ['kkk.......', 'kSTTkkk...', '.kUTTTTkkk', '..kkUUUTTk', '....kkkkkk']
EYE = BROW + ['....kwxk..', '....kxxk..', '.....kk...']
EYE_ALT = {
    'blink': BROW + ['..........', '....kkkk..', '..........'],
    'atk0|atk1|atk2': ['..........', 'kkk.......', 'kSTTkkkk..', '.kUTTTTTkk', '..kkkUUUUk', '....kCxk..', '....kxRk..', '.....kk...'],
    'hit': ['kkk.......', 'kSTTkkk...', '.kUTTTkkk.', '..kkkkk...', '....kk....', '......kk..', '....kk....', '..........'],
    'ko': BROW + ['....x.x...', '.....x....', '....x.x...'],
}
LEG = ['.kkkkk.', 'kFGGGHk', 'kGGGGHk', 'kGGGHHk', 'kGHHHHk', 'kHHHHHk', 'kSkSkSk']
DARK = {'F': 'G', 'G': 'H', 'H': 'l', 'S': 'T'}
def dark(rows): return [''.join(DARK.get(c, c) for c in r) for r in rows]
# 飛ばす 刃（攻撃）
SHOT = ['kkk......', 'kSSkkk...', '.kTTSSSkk', '.kTTTTUUk', 'kUUUkkk..', 'kk.......']
STREAK = ['TT.TTT', '......', '.TTT..']

def layers():
    return [
        dict(n='legBF', g='legB', x=19, y=54, rows=dark(LEG)),
        dict(n='legFF', g='legA', x=30, y=54, rows=dark(LEG)),
        dict(n='quill', g='quill', x=0, y=0, rows=QUILL, alt={'idle1|idle3|walk1|walk3': QUILL2, 'atk0|atk1|atk2': QFLARE}),
        dict(n='body', g='body', x=16, y=41, rows=BODY),
        dict(n='legB', g='legA', x=15, y=54, rows=LEG),
        dict(n='legF', g='legB', x=34, y=54, rows=LEG),
        dict(n='head', g='head', x=31, y=37, rows=HEAD),
        dict(n='eye', g='head', x=37, y=38, rows=EYE, alt=EYE_ALT),
        dict(n='shot1', g='fx', x=52, y=30, rows=SHOT, only='atk1|atk2'),
        dict(n='shot2', g='fx2', x=55, y=36, rows=SHOT, only='atk1|atk2'),
        dict(n='streak1', g='fx', x=45, y=31, rows=STREAK, only='atk1'),
        dict(n='streak2', g='fx2', x=48, y=37, rows=STREAK, only='atk1'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'quill': (0, -1)},
    'idle2': {'body': (0, 1)},
    'idle3': {'body': (0, 1), 'quill': (0, -1)},
    'blink': {},
    'walk0': {'legA': (1, -1), 'legB': (-1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (1, -1)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (0, 0)},
    'atk1': {'body': (1, 0), 'fx': (0, 0), 'fx2': (0, 0)},
    'atk2': {'body': (1, 0), 'fx': (8, -2), 'fx2': (6, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'quill': (1, 1)},
    'ko': {'_flip': True},
}
PARENT = {'head': 'body', 'quill': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'root', 'fx2': 'root'}
