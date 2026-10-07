# マクラン（ノーマル・エスパー × まくら）手打ち GBA風：無機物＋かわいい ライン
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, stamp
META = dict(id='makuran', name='マクラン', types=['normal', 'psychic'], base='まくら', size='M')
EYE_BOX = (25, 35, 22, 5)
PAL = {'k': '#1a1630', 'l': '#6c5698',
       'W': '#fffaf0', 'M': '#e6dcf2', 'D': '#ac9ad6',          # 綿の 布（影は 青紫へ）
       'b': '#9ccaff', 'B': '#5a7fd2',                          # まくらカバーの ふち（パイピング）
       'V': '#dc9cff', 'U': '#8a46d4',                          # ねむけの 念波・ひとみ
       'c': '#261a40', 'w': '#ffffff', 'p': '#ffa6c6'}          # 目の 黒・光・ほっぺ
LIGHT = set('Wwb')
KEEP_BLACK = set('wpcVU')

def put(g, pts, ch):
    for x, y in pts:
        if 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch

# ---- 顔の 部品：ねむそうな 半目（重い まぶた＋下半分の 紫の ひとみ）----
EYES = {
    'open':  (['.ccccc..', 'cMMMMMc.', 'cccccccc', 'cUUUwUc.', '.cVVVc..', '..ccc...'], ['..ccccc.', '.cMMMMMc', 'cccccccc', '.cUwUUUc', '..cVVVc.', '...ccc..']),
    'blink': (['.........', '........c', 'c.....cc.', '.ccccc...', '.........'], ['........', 'c.......', '.cc.....c', '...ccccc.', '........']),
    'fight': (['c......', '.cc....', 'ccccccc', 'cUwwUUc', 'cUVVVUc', '.ccccc.'], ['.....c', '....c.', 'cccccc', 'cwwUUc', 'cVVVUc', '.cccc.']),
    'hypno': (['..ccc..', '.cVVVc.', 'cVUUUVc', 'cVUwUVc', 'cVUUUVc', '.cVVVc.', '..ccc..'], ['..ccc..', '.cVVVc.', 'cVUUUVc', 'cVUwUVc', 'cVUUUVc', '.cVVVc.', '..ccc..']),
    'pain':  (['c......', '.cc....', '...cc..', '.cc....', 'c......'], ['.....c', '...cc.', '.cc...', '...cc.', '.....c']),
    'ko':    (['.c...c.', '..c.c..', '...c...', '..c.c..', '.c...c.'], ['c...c.', '.c.c..', '..c...', '.c.c..', 'c...c.']),
}
MOUTH = {'open': ['.cc.', 'cppc', '.cc.'], 'blink': ['c..c', '.cc.'], 'fight': ['cccc'], 'hypno': ['.cc.', 'cppc', '.cc.'],
         'pain': ['.c.c', 'c.c.'], 'ko': ['.cc.', 'c..c']}

# ---- まくら本体：ふくらんだ 角丸の 四角＋ 4すみの 「耳」。高さの 場から 陰影を 計算 ----
def pillow(W, H, kind='open', ears=True):
    g = grid(W, H); z = [[-1.0] * W for _ in range(H)]
    A, Bh = W / 2 - .5, H / 2 - .5
    for y in range(H):
        for x in range(W):
            px, py = x + .5 - W / 2, y + .5 - H / 2
            a = A - 1.5 - 2.5 * (py / Bh) ** 2              # ふくらんだ ふち（上下・左右とも 外へ ふくらむ）
            bb = Bh - 1.5 - 2 * (px / A) ** 2
            u, v = abs(px) / a, abs(py) / bb
            cu, cv = abs(px) - (A - 5), abs(py) - (Bh - 5)
            tip = cu >= 0 and cv >= 0 and abs(cu - cv) <= (5 - max(cu, cv)) * .7 + .6 and max(cu, cv) <= 4.2
            if u ** 3.2 + v ** 3.2 > 1 and not tip: continue   # すみは 布が つまんだ 「耳」
            u, v = min(u, 1), min(v, 1)
            m = (u ** 3.2 + v ** 3.2)
            z[y][x] = max(0, 1 - m) ** .5
    for y in range(H):
        for x in range(W):
            if z[y][x] < 0: continue
            zl = z[y][x - 1] if x > 0 and z[y][x - 1] >= 0 else 0
            zr = z[y][x + 1] if x < W - 1 and z[y][x + 1] >= 0 else 0
            zu = z[y - 1][x] if y > 0 and z[y - 1][x] >= 0 else 0
            zd = z[y + 1][x] if y < H - 1 and z[y + 1][x] >= 0 else 0
            gx, gy = (zr - zl) * W / 7, (zd - zu) * H / 7
            n = (gx * gx + gy * gy + 1) ** .5
            I = (.5 * gx + .6 * gy + .62) / n
            g[y][x] = 'W' if I > .78 else 'M' if I > .40 else 'D'
    # パイピング：ふちから 2ドット 内側を 1周
    inside = lambda y, x: 0 <= y < H and 0 <= x < W and g[y][x] != '.'
    for y in range(H):
        for x in range(W):
            if not inside(y, x): continue
            d = min(next((i for i in range(1, 9) if not all(inside(y + dy * i, x + dx * i) for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))), 9), 9)
            if d == 3: g[y][x] = 'B' if (x > W * .55 and y > H * .3) or y > H * .75 else 'b'
    # 4すみの しわ（耳の 付け根から 内へ 短い 線）
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        cx, cy = (W - 1) / 2 + sx * (W / 2 - 7), (H - 1) / 2 + sy * (H / 2 - 7)
        for i in range(3):
            put(g, [(round(cx - sx * i * 1.0), round(cy - sy * i * .5))], 'D')
    # 顔（中心より 右に 寄せる＝3/4）
    en, ef = EYES[kind]; mo = MOUTH[kind]
    fx, fy = int(W * .58), int(H * .42)
    eh = len(en)
    stamp(g, ef, fx - 13, fy - eh + 3); stamp(g, en, fx + 3, fy - eh + 3)
    stamp(g, mo, fx - len(mo[0]) // 2 + 1, fy + 5)
    if kind != 'ko': stamp(g, MOON, 6, H - 13)
    if kind in ('open', 'blink', 'hypno'):
        put(g, [(fx - 14, fy + 4), (fx - 13, fy + 4), (fx - 12, fy + 4)], 'p'); put(g, [(fx + 9, fy + 4), (fx + 10, fy + 4), (fx + 11, fy + 4)], 'p')
    return outline(rows_of(g))

MOON = ['.UU.', 'U...', 'U...', 'U...', '.UU.']   # 刺しゅうの 三日月（エスパーの しるし）
# ---- 足：ちょこんと した 布の こぶ ----
FOOT = ['.kkkk.', 'kMMMDk', 'kDDDDk', '.kkkk.']
# ---- ねむけの Z（紫、浮かぶ。はなれているのは 意図的）----
ZBIG = ['kkkkk.', 'kVVVVk', 'kkkVkk', '.kVkk.', 'kVkkkk', 'kVVVVk', 'kkkkk.']
ZSM = ['VVVV', '..U.', '.U..', 'UUUU']
# ---- 念波（ねむけの 波）：同心の 弧 ----
def waves(n=3, r0=4, gap=4):
    H = 2 * (r0 + gap * (n - 1)) + 3; W = r0 + gap * (n - 1) + 3; g = grid(W, H); cy = H // 2
    for i in range(n):
        r = r0 + gap * i
        for y in range(H):
            for x in range(W):
                d = (x * x + (y - cy) ** 2) ** .5
                if r - .6 <= d <= r + .6 and x >= 1: g[y][x] = 'V' if i % 2 == 0 else 'U'
    return rows_of(g)
WAVE1 = waves(3, 4, 4)
WAVE2 = waves(3, 7, 4)
SPARK = ['.V.', 'VwV', '.V.']

NA = 'ko'
def layers():
    return [
        dict(n='footB', g='legB', x=33, y=53, rows=FOOT, not_=NA),
        dict(n='footA', g='legA', x=17, y=53, rows=FOOT, not_=NA),
        dict(n='body', g='body', x=7, y=25, rows=pillow(48, 30), alt={
            'blink': pillow(48, 30, 'blink'), 'atk0': pillow(52, 26, 'fight'), 'atk1|atk2': pillow(46, 32, 'hypno'),
            'hit': pillow(44, 30, 'pain')}, not_=NA),
        dict(n='z1', g='fx', x=52, y=20, rows=ZSM, not_='atk0|atk1|atk2|hit|ko'),
        dict(n='z2', g='fx2', x=56, y=11, rows=ZBIG, only='idle1|idle2|idle3|walk1|walk2'),
        dict(n='wave1', g='root', x=56, y=27, rows=WAVE1, only='atk1'),
        dict(n='wave2', g='root', x=58, y=21, rows=WAVE2, only='atk2'),
        dict(n='spark', g='root', x=4, y=19, rows=SPARK, only='atk0'),
        dict(n='spark2', g='root', x=56, y=20, rows=SPARK, only='atk0'),
        dict(n='ko', g='root', x=4, y=42, rows=pillow(56, 18, 'ko', ears=True), only='ko'),
        dict(n='koz', g='root', x=56, y=33, rows=ZSM, only='ko'),
    ]

FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, 1), 'fx': (0, -1)}, 'idle2': {'body': (0, 1), 'fx': (1, -2), 'fx2': (0, -1)}, 'idle3': {'fx': (1, -1), 'fx2': (1, -2)},
    'blink': {},
    'walk0': {'body': (0, -1), 'legA': (0, -1)}, 'walk1': {'body': (0, -2), 'legA': (1, -2), 'fx': (0, -1)},
    'walk2': {'body': (0, -1), 'legB': (0, -1)}, 'walk3': {'body': (0, -2), 'legB': (1, -2), 'fx': (0, -1)},
    'atk0': {'root': (-3, 0), 'body': (-2, 4)}, 'atk1': {'root': (3, 0), 'body': (1, -2)}, 'atk2': {'root': (2, 0), 'body': (0, -1)},
    'hit': {'root': (-3, 0), 'body': (2, 0)}, 'ko': {},
}
PARENT = {'body': 'root', 'legA': 'root', 'legB': 'root', 'fx': 'body', 'fx2': 'body'}
