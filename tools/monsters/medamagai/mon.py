# メダマガイ（みず・エスパー × オウムガイ）手打ち GBA風
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, poly, line, stamp

# ---------- 下書きの 道具（あたりを とって 自動で 3段の 陰影 → 仕上げは 手で 打つ）----------
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
    """光は 左上：ふくらみ（まわりの 量の かたむき）＋ 全体の 斜めの かたむき → 明・中・暗。上と 左の ふちは 明、右下の ふちは 暗"""
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
def ink(p, g=None):
    """まわりに 黒の 輪郭（エンジンが 内側の 線と 光側を 濃い色に する）"""
    g = g or G()
    for y in range(64):
        for x in range(64):
            if p[y][x] == '.' and any(at(p, x + dx, y + dy) != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): g[y][x] = 'k'
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
def L(n, grp, g, **kw): return dict(n=n, g=grp, x=0, y=0, rows=rows_of(g) if isinstance(g[0], list) else g, **kw)

META = dict(id='medamagai', name='メダマガイ', types=['water', 'psychic'], base='オウムガイ', size='M')
EYE_BOX = (32, 20, 19, 20)   # 目の 位置（idle0 の 64x64 座標）
PAL = {
    'k': '#101018', 'l': '#2a1a3e',
    'A': '#f6ecd4', 'B': '#cbb48e', 'C': '#86704e',      # 殻（象牙色）
    'P': '#9a52c0', 'Q': '#52286e',                      # 殻の しま（念の 紫）
    'T': '#74dce0', 'U': '#2e8eac', 'V': '#1a4870',      # 頭巾・触手（深海の 青）
    'Y': '#fff4b8', 'M': '#ff62d4', 'N': '#a8188c',      # 目玉（白目・念の 虹彩）
    'w': '#ffffff', 'Z': '#bff0ff',                      # 光・泡
    'R': '#ffbcec',                                      # 虹彩の 内の 輪（うす桃）
}
LIGHT = set('ATYMwZ')
KEEP_BLACK = set('wYMR')

SC = (22, 30); SR = 15.5          # 殻の 中心と 半径
EC = (41, 30)                     # 目玉（殻口）の 中心

# ---------- 殻：うず巻き＋ 後ろ半分に 念の しま ----------
def shell():
    p = G(); disc(p, SC[0], SC[1], SR, SR, '1')
    s = shade(p, {'1': 'ABC'}, r=3, tilt=.6)
    cx, cy = SC
    for y in range(64):
        for x in range(64):
            if s[y][x] == '.': continue
            dx, dy = x + .5 - cx, y + .5 - cy; rho = math.hypot(dx, dy) / SR
            th = math.degrees(math.atan2(-dy, dx)) % 360        # 0＝右（殻口）、反時計まわり
            if rho < .38 or not (35 < th < 330): continue
            # 中心から 外へ 反って 流れる しま（殻口に 近づくほど 細く 消える）
            k = (th + rho * 70) % 34
            wdt = 13 if th > 110 else 9 if th > 60 else 6
            if th > 290: wdt = 5
            if k < wdt * min(1, (rho - .25) * 2.0):
                s[y][x] = 'Q' if s[y][x] == 'C' or k < 1.5 else 'P'
    g = ink(s)
    # 巻きの すじ（へその うずから 殻口の 上へ）：1ドットずつ
    sp = [(21, 28), (22, 27), (23, 27), (24, 28), (24, 29), (23, 30), (22, 31), (20, 31), (19, 30), (18, 29), (17, 27), (17, 25), (18, 24),
          (19, 23), (21, 22), (23, 22), (25, 22), (27, 23), (28, 24), (29, 25)]
    for a, b in zip(sp, sp[1:]): line(g, a[0], a[1], b[0], b[1], 'k')
    for x, y in sp[8:]: put(g, x - 1 if y < 28 else x, y + 1 if y < 25 else y, 'A') if at(g, x, y + 1) in 'BC' and y < 25 else None
    dots(g, 'C', [(21, 27), (22, 28), (21, 29), (22, 30), (20, 30), (19, 29), (18, 27), (18, 26), (19, 25)])   # うずの くぼみ
    dots(g, 'A', [(20, 24), (21, 23), (22, 23), (17, 23), (18, 22), (16, 25)])
    return g

# ---------- 殻口の ふち（丸の 中に 丸）----------
def lip():
    p = G(); disc(p, EC[0], EC[1], 12, 12.5, '1')
    s = shade(p, {'1': 'ABC'}, r=2, tilt=.8)
    for y in range(64):
        for x in range(64):
            if ((x + .5 - EC[0]) / 9.6) ** 2 + ((y + .5 - EC[1]) / 10.1) ** 2 <= 1: s[y][x] = '.'
    g = ink(s)
    # ふちの 内がわ：暗い 段（深い 穴）
    for y in range(64):
        for x in range(64):
            d = ((x + .5 - EC[0]) / 9.6) ** 2 + ((y + .5 - EC[1]) / 10.1) ** 2
            if 1 < d <= 1.32 and g[y][x] in 'ABC': g[y][x] = 'C' if y < EC[1] + 2 else 'B'
    return g

# ---------- 巨大な 一つ目（手打ち 19×20）----------
EYE = [
    '......kkkkkkk......',
    '....kkYYYYYYYkk....',
    '...kYYYYYYYYYYYk...',
    '..kYYYYNNNNNYYYBk..',
    '.kYYYNNMMMMMNNYYBk.',
    '.kYYNMMMMkMMMMNYBk.',
    'kYYNMMwwMkMMMMMNYBk',
    'kYYNMwwMkkkMMMMNYBk',
    'kYNMMwMMkkkMMMMMNBk',
    'kYNMwwMMkkkMMMMMNBk',
    'kYNMwMMMkkkMMMMMNBk',
    'kYNMMMMMkkkMMMMNNBk',
    'kYYNMMMMkkkMMMMNBBk',
    'kYYNNMMMMkMMMMNNBBk',
    '.kYYNNMMMkMMMNNBBk.',
    '.kYYYNNNNNNNNNBBBk.',
    '..kBYYYNNNNNYBBBk..',
    '...kBBYYYYYBBBBk...',
    '....kkBBBBBBBkk....',
    '......kkkkkkk......',
]
# 目（H：単眼・大目玉）：白目に 血管の 線、虹彩は 桃の 3色の 輪（濃い 紫・桃・うす桃）、まん中に 丸い 黒瞳と 白い 光
VEINS = [(1, 10), (2, 11), (3, 11), (2, 14), (3, 14), (4, 15), (6, 17), (7, 16), (15, 15), (16, 14), (14, 16)]
def eye_draw(pr=2.0, core=False, hot=False):
    e = [list(r) for r in EYE]
    for y in range(20):
        for x in range(19):
            if e[y][x] not in 'YBNMw' and not (e[y][x] == 'k' and 2 < x < 16 and 2 < y < 17): continue
            d = ((x - 9) ** 2 + (y - 9.6) ** 2) ** .5
            if d <= pr: c = 'k'
            elif d <= pr + 1.1: c = 'R' if not hot else 'w'
            elif d <= 4.6: c = 'M'
            elif d <= 5.7: c = 'N'
            else: c = 'B' if (x - 9) * .6 + (y - 9.6) * .8 > 5.2 else 'Y'
            e[y][x] = c
    for (x, y) in VEINS:
        if e[y][x] in 'YB': e[y][x] = 'N'
    for (x, y) in ((6, 9), (7, 8), (8, 7), (12, 12)): e[y][x] = 'w'     # 光（左上に 大、右下に 小）
    if core:
        for (x, y) in ((9, 9), (9, 10)): e[y][x] = 'w'
    return [''.join(r) for r in e]
def eye_var(kind):
    if kind == 'glow': return eye_draw(pr=1.2, hot=True)     # ため：瞳が 点に ちぢみ、内の 輪が 白く 光る
    if kind == 'wide': return eye_draw(pr=2.9, core=True)    # 決め：瞳が 開いて 白く 光る 芯
    return eye_draw()
def eye_shut(kind):
    """まぶた（頭巾と 同じ 色）を とじる。blink＝細い 線、hit＝ゆがむ、ko＝×"""
    rows = []
    for y, r in enumerate(EYE):
        rr = ''
        for x, c in enumerate(r):
            rr += c if c == '.' or c == 'k' and (y in (0, 19) or x in (0, 18) or r[:x].count('k') == 0 or r[x + 1:].count('k') == 0) else ('U' if y < 9 else 'V')
        rows.append(rr)
    e = [list(r) for r in rows]
    for y in range(20):
        for x in range(19):
            if e[y][x] in 'UV' and y < 6: e[y][x] = 'T' if x < 9 else 'U'
    if kind == 'blink':
        for x in range(1, 18): e[10][x] = 'k' if e[10][x] != '.' else '.'
        for x in range(2, 17): e[11][x] = 'V' if e[11][x] != '.' else '.'
    elif kind == 'hit':
        for x, y in ((2, 9), (3, 10), (4, 9), (5, 10), (6, 11), (7, 10), (8, 11), (9, 10), (10, 11), (11, 10), (12, 11), (13, 10), (14, 11), (15, 10), (16, 9)):
            e[y][x] = 'k'
        for x, y in ((6, 12), (7, 12), (8, 12), (12, 12)): e[y][x] = 'Y'
    elif kind == 'ko':
        for i in range(-4, 5):
            e[10 + i][9 + i] = 'k'; e[10 + i][9 - i] = 'k'
        for i in range(-3, 4):
            e[10 + i][10 + i] = 'M'; e[10 + i][8 - i] = 'M'
    return [''.join(r) for r in e]

# ---------- 頭巾（まゆの ひさし）：目の 上に かぶさり 前へ 下がる → にらむ ----------
def hood(dy=0):
    p = G()
    poly(p, [(28, 14 + dy), (36, 10 + dy), (46, 10 + dy), (53, 14 + dy), (56, 21 + dy), (55, 28 + dy), (49, 26 + dy), (42, 22.5 + dy), (35, 20.5 + dy), (28, 20 + dy)], '3')
    s = shade(p, {'3': 'TUV'}, r=2, tilt=.5)
    g = ink(s)
    # 頭巾の いぼ（ごつごつ）と ふちの 影
    dots(g, 'V', [(40, 15 + dy), (44, 16 + dy), (48, 17 + dy), (35, 15 + dy), (51, 20 + dy)])
    dots(g, 'T', [(39, 14 + dy), (43, 15 + dy), (47, 16 + dy), (34, 14 + dy)])
    # ひさしの ふち：にらむ まゆの 稜線（明るい すじ＋下に 影）
    for x in range(30, 55):
        yy = [y for y in range(64) if g[y][x] in 'TUV']
        if yy: g[yy[-1]][x] = 'V'; g[yy[-1] - 1][x] = 'T' if x < 50 else 'U'
    # 前に 突き出す 角（ひさしの 先）
    stamp(g, ['kkk...', 'kTUkk.', '.kUUVk', '..kVVk', '...kk.'], 53, 25 + dy)
    return g

# ---------- 触手：数を 5本に 引いて 太く。先が かぎ爪の ように 巻く ----------
TENT_A = [
    ([(39, 41), (45, 44), (50, 45), (54, 43), (55, 39), (53, 38)], [3, 2.6, 2.2, 1.8, 1.3, 1]),
    ([(42, 42), (46, 47), (50, 51), (54, 52), (56, 49)], [3, 2.6, 2.1, 1.6, 1.1]),
    ([(36, 42), (39, 48), (43, 52), (48, 55), (52, 55)], [3, 2.6, 2.2, 1.6, 1.1]),
]
TENT_B = [
    ([(39, 41), (45, 43), (50, 43), (54, 41), (55, 37), (53, 36)], [3, 2.6, 2.2, 1.8, 1.3, 1]),
    ([(42, 42), (47, 46), (51, 49), (55, 49), (56, 46)], [3, 2.6, 2.1, 1.6, 1.1]),
    ([(36, 42), (40, 48), (44, 51), (49, 53), (53, 52)], [3, 2.6, 2.2, 1.6, 1.1]),
]
TENT_BACK_A = [([(30, 40), (31, 47), (34, 52), (38, 54)], [2.6, 2.2, 1.6, 1.1]), ([(33, 41), (35, 48), (39, 52), (43, 52)], [2.6, 2.2, 1.6, 1.1])]
TENT_BACK_B = [([(30, 40), (30, 46), (32, 51), (36, 54)], [2.6, 2.2, 1.6, 1.1]), ([(33, 41), (36, 47), (40, 51), (44, 50)], [2.6, 2.2, 1.6, 1.1])]
TENT_LIMP = [([(39, 41), (45, 44), (50, 45), (56, 47), (60, 47)], [3, 2.6, 2.1, 1.6, 1.1]),
             ([(42, 42), (46, 47), (50, 49), (56, 51), (60, 52)], [3, 2.6, 2.1, 1.6, 1.1]),
             ([(36, 42), (40, 48), (45, 51), (51, 53), (56, 54)], [3, 2.6, 2.1, 1.6, 1.1])]
def tentacles(spec, back=False):
    p = G()
    for path, rad in spec: tube(p, path, rad, '3')
    s = shade(p, {'3': 'UVV' if back else 'TUV'}, r=1, tilt=.2)
    # 吸いつく すじ（下がわに 明るい 点）
    for y in range(64):
        for x in range(64):
            if s[y][x] == 'V' and at(s, x, y + 1) == '.' and (x + y) % 3 == 0 and not back: s[y][x] = 'Z'
    return ink(s)

# ---------- 念と 水の 演出 ----------
BUB_A = ['.kk.', 'kZwk', 'kZZk', '.kk.', '....', '..kk', '.kZk', '..k.']
BUB_B = ['..kk', '.kZk', '..k.', '....', '.kk.', 'kZwk', 'kZZk', '.kk.']
RING0 = [   # ため：目の まわりに 念の 輪が あつまる
    '..M....M..',
    'M........M',
]
BEAM1 = [
    '.......kk.....kkk......',
    '.....kkMMk...kMMMkk....',
    '....kMMwwMk.kMwwwMMk...',
    '...kMwwMMMkkMwMMMwMMk..',
    'kkkMwMNkkMMMwMNkkNMwMk.',
    'MMMwMNk..kMwMNk..kNMwMk',
    'wwwwwMk...kwMk....kMwMk',
    'MMMwMNk..kMwMNk..kNMwMk',
    'kkkMwMNkkMMMwMNkkNMwMk.',
    '...kMwwMMMkkMwMMMwMMk..',
    '....kMMwwMk.kMwwwMMk...',
    '.....kkMMk...kMMMkk....',
    '.......kk.....kkk......',
]
BEAM2 = [
    '..........kk......',
    '.........kMMk.....',
    '..kk....kMwwMk....',
    '.kMMk..kMwMMwMk...',
    'kMwwMk.kMk..kMk...',
    'kMkkwMkMk....kMk..',
    'kMk.kwMk.....kMk..',
    'kMkkwMkMk....kMk..',
    'kMwwMk.kMk..kMk...',
    '.kMMk..kMwMMwMk...',
    '..kk....kMwwMk....',
    '.........kMMk.....',
    '..........kk......',
]

def wave(radii, core):
    W, H = 34, 34; g = [['.'] * W for _ in range(H)]; cx, cy = -6, 16.5
    for R in radii:
        for y in range(H):
            for x in range(W):
                d = math.hypot(x + .5 - cx, y + .5 - cy); a = abs(math.degrees(math.atan2(y + .5 - cy, x + .5 - cx)))
                if a < 52 and abs(d - R) < 1.6: g[y][x] = 'w' if abs(d - R) < .6 else 'M'
    if core:
        for x in range(0, core):
            for y in (15, 16, 17, 18): g[y][x] = 'w' if y in (16, 17) else 'M'
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + b < H and 0 <= x + a < W and g[y + b][x + a] != '.' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y][x] = 'N'
    return [''.join(r) for r in out]
# 触手の 根もとの くちばし（かぎ形・するどい）
BEAK = ['.kkkk..', 'kTTTUkk', 'kUUUUwk', '.kkUwk.', '...kk..']
BEAK_OPEN = ['.kkkk..', 'kTTTUkk', 'kUUUwwk', 'kkkkkk.', 'kUUwk..', '.kkk...']
def layers():
    SH = shell(); LIP = lip()
    return [
        L('tback', 'tent', tentacles(TENT_BACK_A, True), alt={'idle2|idle3|walk1|walk3|atk1|atk2': rows_of(tentacles(TENT_BACK_B, True)), 'ko': rows_of(tentacles(TENT_BACK_A, True))}),
        L('shell', 'body', SH),
        L('lip', 'body', LIP),
        dict(n='eye', g='eye', x=EC[0] - 9, y=EC[1] - 10, rows=eye_draw(),
             alt={'atk0': eye_var('glow'), 'atk1|atk2': eye_var('wide'), 'blink': eye_shut('blink'), 'hit': eye_shut('hit'), 'ko': eye_shut('ko')}),
        L('hood', 'hood', hood(3), alt={'atk0|atk1|atk2': rows_of(hood(4)), 'hit': rows_of(hood(1))}),
        L('tent', 'tent', tentacles(TENT_A), alt={'idle2|idle3|walk1|walk3|atk1|atk2': rows_of(tentacles(TENT_B)), 'ko': rows_of(tentacles(TENT_LIMP))}),
        dict(n='beak', g='tent', x=EC[0] + 4, y=EC[1] + 9, rows=BEAK, alt={'atk1|atk2': BEAK_OPEN}),
        dict(n='bub', g='fx', x=8, y=4, rows=BUB_A, alt={'idle2|idle3|walk2|walk3': BUB_B}, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='ring0', g='eye', x=EC[0] - 5, y=EC[1] - 14, rows=RING0, only='atk0'),
        dict(n='ring0b', g='eye', x=EC[0] - 5, y=EC[1] + 12, rows=RING0[::-1], only='atk0'),
        dict(n='beam1', g='eye', x=EC[0] + 9, y=EC[1] - 16, rows=wave((12, 19, 26), 30), only='atk1'),
        dict(n='beam2', g='eye', x=EC[0] + 9, y=EC[1] - 16, rows=wave((17, 25, 32), 0), only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'root': (0, -1)}, 'idle2': {'root': (0, -1), 'fx': (0, -2)}, 'idle3': {'root': (0, 0), 'fx': (0, -2)},
    'blink': {},
    'walk0': {'root': (1, 0)}, 'walk1': {'root': (1, -1), 'tent': (-1, 0)}, 'walk2': {'root': (0, -2)}, 'walk3': {'root': (0, -1), 'tent': (-1, 0)},
    'atk0': {'root': (-2, 1), 'tent': (-1, 0)}, 'atk1': {'root': (3, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 1), 'eye': (-1, 0), 'tent': (-1, -1)},
    'ko': {'root': (0, 6), 'hood': (0, 2)},
}
PARENT = {'body': 'root', 'eye': 'body', 'hood': 'body', 'tent': 'body', 'fx': 'root'}
