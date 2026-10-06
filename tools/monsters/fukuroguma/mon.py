# フクログマ（ノーマル・かくとう × オウルベア）手打ち GBA風
import pix
META = dict(id='fukuroguma', name='フクログマ', types=['normal', 'fighting'], base='オウルベア', size='L')
PAL = {
    'k': '#101018', 'l': '#3a2216',
    'F': '#dcaa72', 'G': '#9c6a40', 'H': '#5a3824',
    'D': '#f6e8ca', 'E': '#c6a87e',
    'C': '#f4d26c', 'c': '#ac7428',
    'O': '#ff9a1e', 'Y': '#fff27a',
    'R': '#e2483a', 'r': '#8c2430',
    'w': '#ffffff',
}
LIGHT = set('FDCYRw')
KEEP_BLACK = set('wOY')   # 目の まわりの まゆは 黒の まま

def make_head():
    """あたり：まるい 頭（円）＋ 顔の 皿（だ円）を 計算で 置き、まゆ・くちばし・羽角は 手で 打った 部品を はる"""
    import pix
    W, H = 32, 28; g = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            dx, dy = (x + .5 - 14) / 12.5, (y + .5 - 16) / 11.5
            if dx * dx + dy * dy > 1: continue
            l = -dx * .6 - dy * .8
            g[y][x] = 'F' if l > .35 else 'H' if l < -.5 else 'G'
    for y in range(H):
        for x in range(W):
            dx, dy = (x + .5 - 18) / 9.5, (y + .5 - 17.5) / 9
            r = dx * dx + dy * dy
            if g[y][x] == '.': continue
            if r <= 1: g[y][x] = 'D' if (dx * .6 + dy * .8 < -.15) else 'E'
            elif r <= 1.28: g[y][x] = 'H'
    # 顔の 皿の 羽の すじ（手で：くちばしから 外へ 放射）
    for (x, y) in ((11, 20), (10, 21), (12, 22), (13, 24), (21, 23), (22, 24), (24, 21), (25, 22), (9, 18), (26, 19)): g[y][x] = 'H' if g[y][x] == 'E' else g[y][x]
    for (x, y) in ((11, 15), (12, 16), (10, 16), (24, 15)): g[y][x] = 'D' if g[y][x] == 'E' else g[y][x]
    pix.stamp(g, TUFT_B, 1, 0); pix.stamp(g, TUFT_F, 20, 0)
    pix.stamp(g, BROW, 6, 8)
    pix.stamp(g, BEAK, 14, 13)
    return pix.outline(pix.rows_of(g))[1:]
# 羽角（うしろへ 反った つの のような 羽）
TUFT_B = ['k.......', 'Gk......', 'GGk.....', 'FGGk....', 'kFGGk...', '.kFGGk..', '..kFFGk.']
TUFT_F = ['......kk', '.....kGk', '....kGHk', '...kFGHk', '..kFGHk.', '.kFGHk..']
# V字の まゆ：外側が 高く、くちばしの 根もとへ 下がる。黒い 羽の ひさし
BROW = [
    'Hk...................kH',
    'kkkH...............Hkkk',
    '.kkkkH...........Hkkkk.',
    '..Hkkkkk.......kkkkkH..',
    '....Hkkkkk...kkkkkH....',
    '......kkkkk.kkkkk......',
    '........kkkkkkk........',
]
# 大きな かぎくちばし（右下へ 曲がって とがる）
BEAK = [
    '..kkkk....',
    '.kCCCCkk..',
    'kCCCCCCCk.',
    'kCCCCCCcck',
    'kcCCCCcccck',
    '.kcCCccccck',
    '.kkcCccccck',
    '..kkcCcccck',
    '...kkcccck.',
    '....kkccck.',
    '......kcck.',
    '.......kk..',
]
HEAD = make_head()
def fur(rows, seed=0):
    """毛の 陰影：茶色の 面を 光（左上）と 影（右下）で ぬり分け、毛束の V字を 手で 打つ 代わりに 規則で 置いて から 手直し"""
    g = pix.grid_of(rows); H, W = len(g), len(g[0]); B = set('FGH')
    def run(x, y, dx, dy):
        n = 0
        while 0 <= x < W and 0 <= y < H and g[y][x] not in '.k': x += dx; y += dy; n += 1
        return n
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] not in B: continue
            u, lf, rt, dn = run(x, y, 0, -1), run(x, y, -1, 0), run(x, y, 1, 0), run(x, y, 0, 1)
            c = 'G'
            if rt <= 2 or dn <= 2 or (rt <= 4 and dn <= 6): c = 'H'
            elif u <= 2 or lf <= 2 or (u <= 4 and lf <= 5): c = 'F'
            out[y][x] = c
    for y in range(3, H - 3, 5):   # 毛の すじ（ななめ 2ドット＋ 光の 1ドット）
        for x in range((y // 5 * 4 + seed) % 7 + 2, W - 2, 7):
            if out[y][x] == 'G' and out[y + 1][x + 1] == 'G':
                out[y][x] = 'H'; out[y + 1][x + 1] = 'H'
                if out[y][x - 1] == 'G': out[y][x - 1] = 'F'
    return pix.rows_of(out)

BODY = [
    '.....kkkkkkkkkkkkk..........',
    '...kkFFFFFFFFFFFFFkkk.......',
    '..kFFFFFFFFFFFFFFFFFFk......',
    '.kFFFFFFFFFFFFFFFFFFFFk.....',
    'kFFFFFFGGGGGGGGGGGGFFFk.....',
    'kFFFFGGGGFGGGGGGGGGGGEEk....',
    'kFFFGGGGGGFGGGGGGGGGEEEk....',
    'kFFGGGFGGGGGGGGGGGGEEDEk....',
    'kFGGGGGFGGGGGGGGGGEEEEEEk...',
    'kFGGGGGGGGGGGGHGGGEEDEEDk...',
    '.kGGGGGGGGGGGGGHGEEEEEEEk...',
    '.kGGGGGGFGGGGGGGGEEDEEDEk...',
    '.kGGGGGGGFGGGGGGGEEEEEEEk...',
    '..kGGGGGGGGGGGGHGDEDEEDEk...',
    '..kGGGGGGGGGGGGGHDEEEEEDk...',
    '..kGGGGGGGGGGGGGHDDEDEEDk...',
    '...kGGGGGGGGGGHGHDDEEEEDk...',
    '...kGGGGGGGGGGGHHDDDEDDk....',
    '...kHGGGGGGGGGGHHDDDDDDk....',
    '...kHGGGGGGGGGHHHHDDDDDk....',
    '...kHHGGGGGGGHHHHHHDDDk.....',
    '...kHHGGGGGGHHHHHHHHHHk.....',
    '...kHHHGGGHHHHHHHHHHHHk.....',
    '....kkHHHHHHHHHHHHHHkk......',
    '......kkkkkkkkkkkkkk........',
]
RUFF = [  # 首の 羽の えりまき：肩の 毛に とけこむ ぎざぎざ
    '....kkkk...........kk...',
    '..kkFFGGkk.......kkGHk..',
    '.kFFGGGkDDkk...kkDDGHk..',
    'kFFGGkDDDEDDkkkDDEDkHHk.',
    'kFGGkDDEDDEDDEDDEDEkGHk.',
    '.kGkDDkEDkDEkDDkEDkEkHk.',
    '.kkDk.kDk.kEk.kEk.kEkk..',
    '..kk...kk..k...k...k....',
]
ARM_F = [
    '....kkkkkkk.............',
    '..kkFFFFFFFkk...........',
    '.kFFFFFFFFFFGk..........',
    'kFFFFFFFFFFGGGk.........',
    'kFFFFFFFFFGGGGHk........',
    'kFFFFFFFGGGGGGHk........',
    'kFFFFFGGGGGGGHHk........',
    '.kFFGGGGGGGGGHHk........',
    '.kFGGGGGGGGGHHHk........',
    '..kGGGGGGGGGHHHk........',
    '..kGGGGGGGGHHHk.........',
    '...kGGGGGGGHHHk.........',
    '...kFGGGGGGHHHHk........',
    '...kFGGGGGGGHHHk........',
    '....kFGGGGGGHHHHk.......',
    '....kRRRRRRRRrrrk.......',
    '....kRrRRRRRRrrrrk......',
    '....kRRRRRRRRrrrrk......',
    '.....kRrRRRRRRrrrk......',
    '.....kRRRRRRRrrrrrk.....',
    '.....kkFFFGGGGGGHHk.....',
    '....kFFFFGGGGGGGHHHk....',
    '....kFFFGGGGGGGGGHHHk...',
    '...kFFGGGGGGGGGGGHHHk...',
    '...kFGGGGkGGGGkGGGHHHk..',
    '...kGGGGGkGGGGkGGGGHHk..',
    '...kGGGGkGGGGkGGGGHHHk..',
    '....kHHkkHHHkkHHHkHHk...',
    '....kwwk.kwwk.kwwk.kwk..',
    '.....kwk..kwk..kwk..kk..',
    '.....kwk..kwk..kwk......',
    '......k....k....k.......',
]
ARM_B = [
    '.k...k...k......',
    'kwk.kwk.kwk.....',
    'kwk.kwk.kwk.k...',
    'kwkkkwkkkwkkwk..',
    'kGHkGHkGHkkwk...',
    'kGGkGGkGGHkHk...',
    'kGGGGGGGGHHHk...',
    '.kGGGGGGGHHHk...',
    '.kRRRRRrrrrk....',
    '.kRrRRRrrrrk....',
    '.kRRRRRrrrrk....',
    '..kGGGGHHHHk....',
    '..kGGGGHHHHk....',
    '...kGGGHHHHHk...',
    '...kGGGHHHHHk...',
    '....kGGGHHHHHk..',
    '....kGGGHHHHHk..',
    '.....kGGGHHHHHk.',
    '.....kGGGHHHHHk.',
    '......kGGHHHHHk.',
    '......kGGHHHHHHk',
    '.......kkkkkkkk.',
]
LEG = [
    '..kkkkkkkk....',
    '.kFFGGGGGHk...',
    'kFFGGGGGGHHk..',
    'kFGGGGGGGHHHk.',
    'kFGGGGGGGHHHk.',
    'kGGGGGGGGHHHk.',
    '.kGGGGGGHHHk..',
    '..kGGGGGHHk...',
    '..kGGGGGHHk...',
    '..kFGGGGHHk...',
    '..kFGGGGHHHk..',
    '.kFGGGGGHHHk..',
    '.kFGGGGGGHHHkk',
    'kFGGGGGGGGHHHk',
    'kGGGGGGGGGHHHk',
    'kwkkwkkwkkwkk.',
    '.k..k..k..k...',
]
LEG = fur(LEG, 1)
DLEG = [r.replace('F', 'G') for r in LEG]
def hump(rows):
    """胴の 左上の 角を まるく 落として 熊の 背中の こぶに する（あたり）"""
    g = [[c if c not in 'k' else '.' for c in r] for r in pix.grid_of(rows)]
    g = [r[1:-1] for r in g[1:-1]]
    for y in range(len(g)):
        for x in range(len(g[0])):
            if x < 12 and y < 10 and ((x - 12) / 12) ** 2 + ((y - 10) / 10) ** 2 > 1: g[y][x] = '.'
    return pix.outline(pix.rows_of(g))
BODY = fur(hump(BODY))
ARM_F = fur(ARM_F, 3)
ARM_B = fur(ARM_B, 2)

EYEN = ['OYYYO', 'YYkOO', 'kOOOk']
EYEN_ALT = {
    'blink': ['kkkkk', 'EEEEE', 'kEEEk'],
    'atk0|atk1|atk2': ['YwwwY', 'wwkYY', 'kYYYk'],
    'hit': ['kkkkk', 'kOkOk', 'kkOkk'],
    'ko': ['wkkkw', 'kwkwk', 'kkwkk'],
}
EYEF = ['OYO', 'kOk']
EYEF_ALT = {'blink': ['kkk', 'EEE'], 'atk0|atk1|atk2': ['YwY', 'kYk'], 'hit': ['kkk', 'kOk'], 'ko': ['wkw', 'kwk']}
# 攻撃：まっすぐの 正拳（腕を 前へ）
PUNCH = [
    '..kkkkkkk.........................',
    '.kFFFFFFGkkkkkkkkkkk....kkkkkkk....',
    'kFFFFFFGGGGGGGGGGGGGkkkkFFFFFFGkk..',
    'kFFFFFGGGGGGGGGGGGGGkRRRkFFFFGGGHk.',
    'kFFFFGGGGGGGGGGGGGGHkRrRkFFGGGGGHk.',
    'kFFFGGGGGGGGGGGGGHHHkRRRkFGGGGGHHHk',
    '.kFGGGGGGGGGGGHHHHHHkRrRkkkkGGkGHHk',
    '.kGGGGGGGGGHHHHHHHHHkRRRkGGGkGGkHHk',
    '..kGGGGGGHHHHHHHHHHHkRrRkkkkGGkGHHk',
    '...kHHHHHHHHHHHHHHHHkRRRkGGGkGkHHHk',
    '....kkkkkkkkkkkkkkkkkkkkkHHHHHHHHk.',
    '........................kkkkkkkkk..',
]
IMPACT = [
    '.....k......',
    '....kYk...k.',
    'k...kYk..kYk',
    'kYk.kwYk.kYk',
    '.kYkkwwYkYk.',
    '..kYwwwwwYk.',
    'kkYwwwwwwYkk',
    '..kYwwwwYk..',
    '.kYkYwwkYYk.',
    'kYk.kwYk.kYk',
    'k...kYk...k.',
    '....kYk.....',
    '.....k......',
]
RAKE = [
    'kk......kk......kk......',
    'kwk.....kwk.....kwk.....',
    '.kwk.....kwk.....kwk....',
    '..kwk.....kwk.....kwk...',
    '...kwk.....kwk.....kwk..',
    '....kYk.....kYk.....kYk.',
    '.....kYk.....kYk.....kYk',
    '......kk......kk......kk',
]

# ---- ダウン：うつぶせに たおれて、あごを 地面に つける（目は ×）----
def lying(W, H):
    g = pix.grid(W, H)
    for y in range(H):
        for x in range(W):
            if ((x + .5 - W / 2) / (W / 2)) ** 2 + ((y + .5 - H) / H) ** 2 <= 1: g[y][x] = 'G'
    return pix.outline(pix.rows_of(g))
def head_ko():
    g = pix.grid_of(HEAD)
    pix.stamp(g, EYEN_ALT['ko'], 9, 12); pix.stamp(g, EYEF_ALT['ko'], 22, 12)
    return pix.rows_of(g)
PAW_KO = fur(ARM_F[20:], 1)
PUNCH = fur(PUNCH, 4)
LEG_KO = fur(pix.rot90(DLEG), 2)
def ko_layers():
    hk = head_ko(); hb = max(i for i, r in enumerate(hk) if r.strip('.'))
    return [
        dict(n='ko_leg', g='root', x=0, y=61 - len(LEG_KO), rows=LEG_KO),
        dict(n='ko_body', g='root', x=6, y=43, rows=fur(lying(38, 17))),
        dict(n='ko_head', g='root', x=33, y=60 - hb, rows=hk),
        dict(n='ko_ruff', g='root', x=31, y=60 - hb + 20, rows=RUFF[:6]),
        dict(n='ko_paw', g='root', x=21, y=61 - len(PAW_KO), rows=PAW_KO),
    ]

def layers():
    L = base_layers()
    for l in L: l['not_'] = (l['not_'] + '|ko') if l.get('not_') else 'ko'
    return L + [dict(l, only='ko') for l in ko_layers()]
def base_layers():
    return [
        dict(n='armB', g='armB', x=6, y=4, rows=ARM_B, not_='ko'),
        dict(n='legB', g='legB', x=18, y=44, rows=DLEG),
        dict(n='body', g='body', x=15, y=19, rows=BODY),
        dict(n='legA', g='legA', x=30, y=44, rows=LEG),
        dict(n='head', g='head', x=28, y=0, rows=HEAD),
        dict(n='eyeN', g='head', x=37, y=12, rows=EYEN, alt=EYEN_ALT),
        dict(n='eyeF', g='head', x=50, y=12, rows=EYEF, alt=EYEF_ALT),
        dict(n='armF', g='armF', x=36, y=22, rows=ARM_F, not_='atk1'),
        dict(n='ruff', g='head', x=29, y=20, rows=RUFF),
        dict(n='punch', g='armF', x=36, y=22, rows=PUNCH, only='atk1'),
        dict(n='impact', g='fx', x=66, y=20, rows=IMPACT, only='atk1'),
        dict(n='rake', g='fx', x=55, y=28, rows=RAKE, only='atk2'),
    ]

FRAMES = {
    'idle0': {},
    'idle1': {'body': (0, 1), 'armB': (0, 0)},
    'idle2': {'body': (0, 1), 'head': (0, 1), 'armB': (0, -1)},
    'idle3': {'body': (0, 0), 'armB': (0, -1)},
    'blink': {},
    'walk0': {'legA': (2, -1), 'legB': (-1, 0), 'armF': (1, 0)},
    'walk1': {'body': (0, -1)},
    'walk2': {'legA': (-1, 0), 'legB': (2, -1), 'armF': (-1, 0)},
    'walk3': {'body': (0, -1)},
    'atk0': {'body': (-2, 1), 'head': (-1, 1), 'armF': (-4, -2), 'armB': (1, 2)},
    'atk1': {'root': (5, 0), 'body': (1, 0), 'legA': (2, 0)},
    'atk2': {'root': (7, 1), 'armF': (3, -2), 'armB': (3, 3)},
    'hit': {'root': (-3, 0), 'body': (-1, 0), 'head': (-2, -1), 'armF': (-2, 1), 'armB': (-2, 2)},
    'ko': {},
}
PARENT = {'fx': 'root', 'head': 'body', 'armF': 'body', 'armB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
