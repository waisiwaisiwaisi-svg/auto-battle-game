# ヒョウジンペンギン（こおり・はがね × ペンギン）手打ち GBA風・デフォルメ（2〜3頭身：頭は 大きめ、胴は 小さく 丸く、足は 短く 太く）
# ===KIT=== 下書きの 道具（あたりを とって 3段の 陰影 → 目・牙・模様は 手で 打つ）
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp
def G(): return grid(64, 64)
def at(g, x, y): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
def put(g, x, y, ch):
    if 0 <= y < 64 and 0 <= x < 64: g[y][x] = ch
def dots(g, ch, pts):
    for x, y in pts: put(g, x, y, ch)
def disc(p, cx, cy, rx, ry=None, ch='1'):
    ry = ry or rx
    for y in range(64):
        for x in range(64):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: p[y][x] = ch
def tube(p, path, rad, ch='1'):
    """道すじに そって 丸い 管を ぬる（太さは 点ごとに 指定）"""
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: put(p, x, y, ch)
def shade(p, ramps, r=2, hi=.3, lo=-.3, tilt=.35, rim=True):
    """光は 左上：ふくらみ＋全体の 斜めの かたむき → 明・中・暗。上と 左の ふちは 明、右下の ふちは 暗"""
    m = [[1 if p[y][x] != '.' else 0 for x in range(64)] for y in range(64)]
    pts = [(x, y) for y in range(64) for x in range(64) if p[y][x] in ramps]
    if not pts: return [row[:] for row in p]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    cx, cy, w, h = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(4, max(xs) - min(xs)), max(4, max(ys) - min(ys))
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if 0 <= yy < 64 and 0 <= xx < 64 else 0
        return s / n
    out = [row[:] for row in p]
    for x, y in pts:
        c = p[y][x]; hc, mc, dc = ramps[c]
        v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 - tilt * ((x - cx) / w * 1.2 + (y - cy) / h * 1.6)
        t = hc if v > hi else dc if v < lo else mc
        if rim:
            ul = at(p, x - 1, y) == '.' or at(p, x, y - 1) == '.'
            dr = at(p, x + 1, y) == '.' or at(p, x, y + 1) == '.'
            if ul and not dr and v > lo: t = hc
            elif dr and not ul: t = dc
        out[y][x] = t
    return out
def ink(p, g=None, skip=None):
    """まわりに 黒の 輪郭。skip(x, y) が 真の ところは 線を 引かない（付け根を 胴に なじませる）"""
    g = g or G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                if not (skip and skip(x, y)): g[y][x] = 'k'
    for y in range(64):
        for x in range(64):
            if p[y][x] != '.': g[y][x] = p[y][x]
    return g
def swap(g, mapping, box=None):
    x0, y0, x1, y1 = box or (0, 0, 63, 63)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if g[y][x] in mapping: g[y][x] = mapping[g[y][x]]
    return g
def cut(g, box):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): put(g, x, y, '.')
    return g
def L(n, grp, g, x=0, y=0, **kw): return dict(n=n, g=grp, x=x, y=y, rows=rows_of(g) if isinstance(g[0], list) else g, **kw)
def part(paint_fn, ramps, r=2, tilt=.4, skip=None, **kw):
    p = G(); paint_fn(p); return ink(shade(p, ramps, r=r, tilt=tilt, **kw), skip=skip)
def stack(*gs):
    g = G()
    for h in gs:
        for y in range(64):
            for x in range(64):
                if h[y][x] != '.': g[y][x] = h[y][x]
    return g
def fallen(g, cw=True, ground=61, cx=32):
    """ダウン用：全身を 90度 たおして 地面に のせる（90度 回転は 可）"""
    r = G()
    for y in range(64):
        for x in range(64): r[y][x] = g[63 - x][y] if cw else g[x][63 - y]
    pts = [(x, y) for y in range(64) for x in range(64) if r[y][x] != '.']
    x0, x1, y1 = min(p[0] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)
    out = G(); dx, dy = cx - (x0 + x1) // 2, ground - y1
    for x, y in pts: put(out, x + dx, y + dy, r[y][x])
    return out
# ---- するどい 目（右向き）：まゆ／上まぶたの 線＋白い 光＋虹彩 2色（A 明・B 暗）＋たての ひとみ＋下まぶた ----
EYES = {
    'idle':  ['kk.....', '.kkkkk.', '.kwAkkk', '.kABkBk', '..kkkk.'],
    'atk':   ['kk.....', '.kkkkkk', '.kwwAkA', '.kAABkk', '..kkkk.'],
    'blink': ['kk.....', '.kkkkk.', '.......', '.kkkkkk', '.......'],
    'hit':   ['k......', '.kkk...', '....kkk', '.kkk...', '.......'],
    'ko':    ['.......', '.k...k.', '..k.k..', '...k...', '..k.k..', '.k...k.'],
}
EYES_BIG = {
    'idle':  ['kkk.....', '.kkkkkk.', '.kwAAkkk', '.kAABkBk', '..kBBkk.', '...kkk..'],
    'atk':   ['kkk.....', '.kkkkkkk', '.kwwAAkA', '.kwAABkk', '..kABkk.', '...kkk..'],
    'blink': ['kkk.....', '.kkkkkk.', '........', '.kkkkkkk', '........', '........'],
    'hit':   ['kk......', '.kkkk...', '.....kkk', '..kkkk..', '........', '........'],
    'ko':    ['........', '.k....k.', '..k..k..', '...kk...', '..k..k..', '.k....k.'],
}
def eye(g, x, y, mode='idle', A='Y', B='O', big=False):
    E = (EYES_BIG if big else EYES)[mode]
    for j, r in enumerate(E):
        for i, c in enumerate(r):
            if c == '.': continue
            put(g, x + i, y + j, {'A': A, 'B': B}.get(c, c))
    return g
# 目（O：傷の目）：赤い つり目（白い 光＋だいだい・赤・さび色の 虹彩＋黒い 瞳）を 古傷（うすい 青白の 線）が たてに 切りさき、上下の まぶたの 線が 切れて いる
SCAR_EYE = {
    'idle':  ['..........', '.....V....', 'kkk..Vk...', '.kkkkVkkk.', '.kwOOkOpk.', '..kOpkpRk.', '...kkVkk..', '.....V....', '....V.....', '....V.....'],
    'atk':   ['..........', '.....V....', 'kkk..Vk...', '.kkkkVkkk.', '.kwwwkwOk.', '..kOOkOpk.', '...kkVkk..', '.....V....', '....V.....', '....V.....'],
    'blink': ['..........', '.....V....', 'kkk..V....', '.kkkkVkkk.', '..........', '.....V....', '.....V....', '.....V....', '....V.....', '....V.....'],
    'hit':   ['..........', '.....V....', '.....V....', '.kk..V.kk.', '...kkVk...', '.kk..V.kk.', '.....V....', '.....V....', '....V.....', '....V.....'],
    'ko':    ['..........', '.....V....', '.....V....', '..W..V.W..', '...W.VW...', '....WW....', '...W.VW...', '..W..V.W..', '....V.....', '....V.....'],
}
EYEMODE = {'blink': 'blink', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk', 'hit': 'hit', 'ko': 'ko'}
# ===END KIT===

META = dict(id='hyoujinpengin', name='ヒョウジンペンギン', types=['ice', 'steel'], base='ペンギン', size='M')
PAL = {
    'k': '#101018', 'l': '#1c2440',
    'A': '#5a6ea4', 'B': '#34406c', 'D': '#1e2444',      # 背の 羽（濃い 紺）
    'W': '#eef6ff', 'V': '#a8c2e2',                      # 腹（氷の 白）
    'S': '#f4f8ff', 'T': '#a2acc4', 'U': '#5c6484',      # 鋼の 刃
    'I': '#c6f6ff', 'J': '#4cbcec',                      # 氷の 結晶・目
    'O': '#f29a32', 'R': '#a4501c',                      # 足
    'w': '#ffffff', 'p': '#c8405a',                      # 光／口の 中
}
LIGHT = set('AWSIOw')
KEEP_BLACK = set('wS')
FUR = {'1': 'ABD', '2': 'WVV'}

# ---------- 胴：たまご形。前（右）は 氷の 白い 腹 ----------
def body(lean=0):
    p = G(); disc(p, 30 + lean, 47, 10.5, 9)
    for y in range(64):
        for x in range(64):
            if p[y][x] == '1' and ((x - 34 - lean) / 6.5) ** 2 + ((y - 49) / 8) ** 2 <= 1: p[y][x] = '2'
    s = shade(p, FUR, r=2, tilt=.6)
    g = ink(s)
    for x, y in ((33, 44), (35, 46), (32, 49), (36, 51), (34, 53)):    # 腹の 羽の 模様（氷の うろこ）
        if at(g, x, y) in 'WV': put(g, x, y, 'V'); put(g, x + 1, y, 'J' if x % 2 else 'V')
    return g

# ---------- 足：短く 太い 鋼の かぎ爪 ----------
def leg(x, back, lift=0):
    def f(p):
        tube(p, [(x, 52), (x, 57 - lift)], [3, 2.8])
        disc(p, x + 2, 59 - lift, 4.4, 2.2)
    g = part(f, {'1': ('RRR' if back else 'ORR')}, r=1, tilt=.3, skip=lambda X, Y: Y < 53)
    fx, fy = x + 2, 59 - lift
    dots(g, 'k', [(fx - 1, fy), (fx + 1, fy)]); dots(g, 'T' if back else 'S', [(fx + 5, fy + 1), (fx + 3, fy + 2)])
    return g

# ---------- 頭：大きな 丸。紺の かぶとに 氷の 白い ほお、鋼の くちばし（ぎざぎざの 刃）----------
def head(mode='idle'):
    def f(p):
        disc(p, 32.5, 30, 10, 8.6)
        for y in range(64):
            for x in range(64):
                if p[y][x] == '1' and ((x - 30) / 4.5) ** 2 + ((y - 35) / 3.5) ** 2 <= 1: p[y][x] = '2'
    g = part(f, FUR, r=2, tilt=.5)
    # 鋼の くちばし（上は 長く 下に 曲がる 刃、下は ぎざぎざ）
    if mode == 'atk':
        stamp(g, ['kkkkkkkk.....', 'STTTTTTTkkk..', 'TTTTTTTUUUUk.', 'kkkkkkkkkkUUk', 'pppppkkk..kk.', 'wkwkwkp......', 'TTTTTTk......', 'UUUUkk.......', 'kkkk.........'], 40, 28)
    else:
        stamp(g, ['kkkkkkk.......', 'STTTTTTkkkk...', 'TTTTTTTTTUUkk.', 'UUUUUUUUUUUUk.', 'kwkwkwkwkUUk..', 'TTTTTTTUkkk...', 'UUUUUkkk......', 'kkkkk.........'], 40, 29)
    dots(g, 'S', [(41, 29), (42, 29)])
    for j, r in enumerate(SCAR_EYE[mode]):
        for i, c in enumerate(r):
            if c != '.': put(g, 31 + i, 22 + j, c)
    return g
# 頭の 上の 氷の 結晶の とさか（3本）：付け根は 頭に 3ドット 食いこむ
CREST = [
    '....kk..........',
    '...kIk......kk..',
    '..kIJk..kk.kIk..',
    '..kIJk.kIk.kIJk.',
    '.kIIJkkIJk.kIJk.',
    '.kIJJkIIJkkIJJk.',
    'kIIJJkIJJkIIJk..',
    'kIJJkIIJJkIJJk..',
    '.kkkkkkkkkkkk...',
]

# ---------- ひれ＝スケートの 刃（見せ所）：平たく 細い 鋼の 板、下の ふちが 光る 刃 ----------
def blade(mode='idle', back=False):
    p = G()
    if back:                # 奥の ひれ：後ろ下へ のびる 刃
        poly(p, [(27, 40), (22, 40), (14, 51), (8, 57), (10, 59), (17, 55), (26, 47)], '1')
    elif mode == 'idle':    # 下へ 長く のびる 刃（前へ 反る）
        poly(p, [(33, 39), (38, 38), (49, 48), (57, 55), (58, 58), (53, 58), (44, 52), (33, 45)], '1')
    elif mode == 'up':      # ため：後ろへ ふりかぶる
        poly(p, [(30, 41), (35, 40), (30, 30), (24, 22), (22, 24), (26, 33), (29, 44)], '1')
    else:                   # 攻撃：前へ まっすぐ 突き出す
        poly(p, [(33, 40), (38, 39), (52, 41), (60, 43), (59, 45), (50, 46), (34, 46)], '1')
    s = shade(p, {'1': ('TUU' if back else 'STU')}, r=1, tilt=.8, hi=.05, lo=-.35)
    g = ink(s)
    for y in range(64):                 # 刃の ふち（下と 前）は 白く 光る 線
        for x in range(64):
            if s[y][x] != '.' and at(s, x, y + 1) == '.' and (x > 38 or back): g[y][x] = 'w' if not back else 'S'
    if not back and mode == 'idle':       # 刃の 先の ぎざぎざ（トウピック）
        dots(g, 'k', [(58, 56), (57, 57)]); dots(g, 'T', [(56, 56)])
    j = (24, 42) if back else (35, 42)                         # 付け根の 鋲（胴に 食いこむ 関節）
    dots(g, 'U', [(j[0], j[1]), (j[0] + 1, j[1] + 1), (j[0], j[1] + 1)]); dots(g, 'S', [(j[0] - 1, j[1] - 1)])
    return g
SLASH = [
    '.........kkk',
    '......kkkIIk',
    '....kkIIIJk.',
    '..kkIIJJkk..',
    '.kIIJkk.....',
    'kIJkk.......',
    'kJk.........',
    'kk..........',
]

def ko_pose():
    c = G(); stamp(c, CREST, 24, 15)
    return fallen(stack(blade('idle', True), leg(35, True), body(), leg(28, False), head('ko'), c, blade()), cw=True)
KO = None
def layers():
    global KO
    KO = ko_pose()
    H = {m: rows_of(head(m)) for m in ('idle', 'blink', 'atk', 'hit', 'ko')}
    return [
        L('bladeB', 'finB', blade('idle', True), not_='ko'),
        L('legB', 'legB', leg(35, True), not_='ko'),
        L('body', 'body', body(), not_='ko'),
        L('legA', 'legA', leg(28, False), not_='ko'),
        L('head', 'head', head(), alt={'blink': H['blink'], 'atk0|atk1|atk2': H['atk'], 'hit': H['hit']}, not_='ko'),
        dict(n='crest', g='head', x=24, y=15, rows=CREST, not_='ko'),
        L('blade', 'fin', blade(), alt={'atk1|atk2': rows_of(blade('atk'))}, not_='ko'),
        L('ko', 'root', KO, only='ko'),
        dict(n='slash', g='root', x=50, y=32, rows=SLASH, only='atk1'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'fin': (0, -1)}, 'idle2': {'body': (0, 1)}, 'idle3': {'fin': (0, 1)},
    'blink': {},
    'walk0': {'legA': (0, -2), 'body': (-1, 0)}, 'walk1': {'body': (0, -1)}, 'walk2': {'legB': (0, -2), 'body': (1, 0)}, 'walk3': {'body': (0, -1)},
    'atk0': {'body': (-1, 1), 'head': (-1, 0), 'fin': (-3, 0), 'finB': (-1, -1)},
    'atk1': {'root': (4, 0)},
    'atk2': {'root': (2, 0), 'fin': (1, 1)},
    'hit': {'root': (-3, 0), 'head': (-1, -1), 'fin': (-1, 1)},
    'ko': {},
}
EYE_BOX = (31, 23, 10, 9)
PARENT = {'head': 'body', 'fin': 'body', 'finB': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
