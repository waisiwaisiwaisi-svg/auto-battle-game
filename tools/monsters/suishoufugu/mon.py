# スイショウフグ（エスパー・いわ × ハリセンボン）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：ふくらむと のびる 水晶の とげ（ハリセンボンの とげ ⇔ 水晶の 柱）
META = dict(id='suishoufugu', name='スイショウフグ', types=['psychic', 'rock'], base='ハリセンボン', size='S')
EYE_BOX = (31, 26, 9, 8)
PAL = {
    'k': '#101018', 'l': '#26193c',
    'F': '#ecdcb4', 'G': '#b0946a', 'H': '#665240',      # 岩の 皮
    'V': '#f6e0ff', 'P': '#c27cff', 'p': '#6a30aa',      # 水晶
    'C': '#e49cff', 'c': '#8a2ad0',                      # 目（魚の 目の 細い 虹彩の 輪・むらさき）
    'w': '#ffffff', 'r': '#a01c34', 'K': '#060608',     # K＝魚の 目の 平たい ひとみ
}
LIGHT = set('FVCw')
KEEP_BLACK = set('wCc')
# ---------- 下書きの 道具（あたり → 左上光の 3段 → 輪郭。目・牙・模様・線は 手で 打つ）----------
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_lib'))
from pix import grid, rows_of, outline, ellipse, poly, line
N = 64
def G(): return grid(N, N)
def at(g, x, y): return g[y][x] if 0 <= y < N and 0 <= x < N else '.'
def E(g, cx, cy, rx, ry, ch='1'): ellipse(g, cx, cy, rx, ry, ch)
def P(g, pts, ch='1'): poly(g, pts, ch)
def Ln(g, x0, y0, x1, y1, ch): line(g, x0, y0, x1, y1, ch)
def dots(g, ch, pts, on=None):
    """手で 1ドットずつ 打つ（on を 指定すると その 色の 上だけ）"""
    for x, y in pts:
        if 0 <= x < N and 0 <= y < N and (on is None or g[y][x] in on): g[y][x] = ch
def hand(g, x, y, rows):
    """手打ちの 絵（文字の 行）を はりつける。'.' は すける"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= x + i < N and 0 <= y + j < N: g[y + j][x + i] = c
def shade(g, ramps, lw=1, dw=2):
    """マスクに 光（左上）：上・左の ふち lw は 明、下・右の ふち dw は 暗"""
    src = [r[:] for r in g]
    for y in range(N):
        for x in range(N):
            m = src[y][x]
            if m not in ramps: continue
            Lc, Mc, Dc = ramps[m]
            def run(dy, dx):
                i = 1
                while i < 9 and at(src, x + dx * i, y + dy * i) == m: i += 1
                return i
            dr = min(run(1, 0), run(0, 1) + 1); ul = min(run(-1, 0), run(0, -1))
            g[y][x] = Dc if dr <= dw else Lc if ul <= lw else Mc
def part(draw, ramps, lw=1, dw=2, post=None, cut=()):
    """1つの パーツ：draw で 形 → 陰影 → post で 手打ち → 輪郭。cut の 四角では 輪郭を 開けて 体と つなぐ"""
    g = G(); draw(g); shade(g, ramps, lw, dw)
    if post: post(g)
    rows = [list(r) for r in outline(rows_of(g))]
    for (x0, y0, x1, y1) in cut:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if rows[y + 1][x + 1] == 'k' and at(g, x, y) == '.': rows[y + 1][x + 1] = '.'
    return [''.join(r) for r in rows]
def L(n, gr, rows, **kw): return dict(n=n, g=gr, x=-1, y=-1, rows=rows, **kw)
def H(n, gr, x, y, rows, **kw): return dict(n=n, g=gr, x=x, y=y, rows=rows, **kw)
import math
CX, CY, RX, RY = 30, 36, 11.5, 10.5
# ---- 水晶の とげ（胴の 後ろから 放射に のびる 柱。左上の 面は 明るく、右下の 面は 暗い）----
ANG = (200, 225, 250, 275, 300, 325, 350, 115, 140, 165, 90, 65)
def crystals(ln=6, wd=2.2, angs=ANG):
    def d(g):
        for a in angs:
            r = math.radians(a); ux, uy = math.cos(r), math.sin(r); nx, ny = -uy, ux
            bx, by = CX + RX * .8 * ux, CY + RY * .8 * uy
            tx, ty = CX + (RX + ln) * ux, CY + (RY + ln) * uy
            P(g, [(bx + nx * wd, by + ny * wd), (bx + ux * (ln * .6) + nx * wd * .9, by + uy * (ln * .6) + ny * wd * .9), (tx, ty),
                  (bx + ux * (ln * .6) - nx * wd * .9, by + uy * (ln * .6) - ny * wd * .9), (bx - nx * wd, by - ny * wd)], '3')
    def p(g):
        src = [r[:] for r in g]
        for y in range(N):
            for x in range(N):
                if src[y][x] == '.': continue
                # いちばん 近い 柱の 軸で 面を わける
                a = math.degrees(math.atan2(y + .5 - CY, x + .5 - CX)) % 360
                a0 = min(angs, key=lambda q: min(abs(a - q), 360 - abs(a - q)))
                r = math.radians(a0); ux, uy = math.cos(r), math.sin(r)
                side = (x + .5 - CX) * -uy + (y + .5 - CY) * ux
                lit = (-uy * -.6 + ux * -.8) * (1 if side > 0 else -1)   # その 面が 左上を 向いて いるか
                g[y][x] = 'V' if abs(side) < .7 else ('P' if lit > 0 else 'p')
    return part(d, {}, post=p)
CRY = crystals(8, 2.4); CRY_BIG = crystals(12, 2.8); CRY_MID = crystals(10, 2.6)
# ---- 胴＝頭（丸い 岩の フグ。はらは 明るく、背に 斑点）----
def body_d(g, rx=RX, ry=RY): E(g, CX, CY, rx, ry, '1')
def body_p(g, open_=False):
    for y in range(N):
        for x in range(N):
            if g[y][x] in 'FG' and y > CY + 2 and x > CX - 9: g[y][x] = 'F' if y < CY + RY - 2 else 'G'
            if g[y][x] == 'F' and y == CY + 2: g[y][x] = 'G'
    for (x, y) in ((24, 28), (29, 26), (22, 33), (27, 31), (20, 38)):
        dots(g, 'H', [(x, y), (x + 1, y)], 'FG'); dots(g, 'G', [(x, y + 1)], 'F')
    # くちばし（くっついた 歯の 板）
    if not open_:
        hand(g, 38, 36, ['..kkkk..', '.kwwwwk.', 'kGwwwkkk', 'kkkkkkk.', 'kGwwwk..', '.kkkkk..'])
    else:
        hand(g, 38, 35, ['..kkkk..', '.kwwwwk.', 'kGwwwkk.', 'krrrrk..', 'krrrrk..', 'kGwwwk..', '.kkkkk..'])
    # えらの 線
    Ln(g, 31, 33, 30, 41, 'G')
BODY = part(body_d, {'1': 'FGH'}, lw=2, dw=3, post=body_p)
BODY_OPEN = part(body_d, {'1': 'FGH'}, lw=2, dw=3, post=lambda g: body_p(g, True))
# ---- ひれ（水晶の 板の ひれ。つけ根は 胴に もぐる）----
def tail_d(g, up=0): P(g, [(19, 34), (9, 27 - up), (11, 36), (8, 46 + up), (19, 40)], '2')
def tail_p(g): Ln(g, 18, 37, 11, 30, 'V'); Ln(g, 18, 38, 11, 43, 'p')
TAIL = part(tail_d, {'2': 'VPp'}, post=tail_p); TAIL2 = part(lambda g: tail_d(g, 2), {'2': 'VPp'}, post=tail_p)
def fin_d(g, dn=0): P(g, [(30, 40), (25, 45 + dn), (28, 48 + dn), (33, 44)], '2')
FIN = part(fin_d, {'2': 'VPp'}); FIN2 = part(lambda g: fin_d(g, 1), {'2': 'VPp'})
# ---- 目（K 魚の 目）：まぶたの ない 丸い 目。平たく 大きい 黒い ひとみ＋むらさきの 細い 輪（明 C・暗 c）。岩の 骨の ふちが まわりを かこむ ----
EYE = ['.HHHH....',
       'HFFkkkHH.',
       'FHkCCCkH.',
       'HkCwKKckH',
       'HkCKKKckH',
       '.kcKKKck.',
       '.Hkcccc..',
       '..HkkkH..']
EYE_ALT = {
    # まぶたが ないので 灰色の 膜（瞬膜）が 下から かぶさる
    'blink': ['.HHHH....', 'HFFkkkHH.', 'FHkCCCkH.', 'HkCwKKckH', 'HkkkkkkkH', '.kFFFFGk.', '.HkGGGk..', '..HkkkH..'],
    # ため・攻撃：ひとみが 点に しぼり、むらさきの 輪が ひろがって 光る
    'atk0|atk1|atk2': ['.HHHH....', 'HFFkkkHH.', 'FHkCCCkH.', 'HkCwCCckH', 'HkCCKcckH', '.kccccck.', '.Hkcccc..', '..HkkkH..'],
    # 被弾：ひとみが ちぢんで 上へ ずれる
    'hit': ['.HHHH....', 'HFFkkkHH.', 'FHkCKCkH.', 'HkCCCCckH', 'HkCCCcckH', '.kcccccK.', '.HkcccK..', '..HkkkH..'],
    'ko': ['.HHHH....', 'HFFkkkHH.', 'FHKCCCKH.', 'HkcKCKckH', 'HkCcKcckH', '.kcKcKck.', '.HKcccK..', '..HkkkH..'],
}
# ---- 攻撃：水晶の かけらを 四方に 飛ばす（はなれた エフェクト＝意図的）----
SHARD = ['..k...', '.kVk..', 'kVPpk.', '.kPpk.', '..kpk.', '...k..']
SHARD2 = ['.kk.', 'kVPk', 'kPpk', '.kk.']

def layers():
    return [
        L('tail', 'tail', TAIL, alt={'idle1|idle2|walk1|walk3|atk1': TAIL2}),
        L('cry', 'body', CRY, alt={'atk1': CRY_BIG, 'atk2|hit': CRY_MID}),
        L('body', 'body', BODY, alt={'atk1|atk2': BODY_OPEN}),
        L('fin', 'body', FIN, alt={'idle2|idle3|walk0|walk2': FIN2}),
        H('eye', 'body', 31, 26, EYE, alt=EYE_ALT),
        H('sh1', 'root', 55, 20, SHARD, only='atk1'), H('sh2', 'root', 56, 46, SHARD, only='atk1'),
        H('sh3', 'root', 57, 28, SHARD2, only='atk2'), H('sh4', 'root', 58, 42, SHARD2, only='atk2'),
    ]
FRAMES = {
    'idle0': {}, 'idle1': {'body': (0, -1)}, 'idle2': {'root': (0, -1)}, 'idle3': {'body': (0, 1)},
    'blink': {},
    'walk0': {'root': (0, -1)}, 'walk1': {'root': (1, -2), 'tail': (1, 0)}, 'walk2': {'root': (0, -1)}, 'walk3': {'root': (1, 0), 'tail': (1, 0)},
    'atk0': {'root': (-2, 1)}, 'atk1': {'root': (3, -1)}, 'atk2': {'root': (2, 0)},
    'hit': {'root': (-3, 0)},
    'ko': {'_flip': True, 'root': (0, 8)},
}
PARENT = {'body': 'root', 'tail': 'body'}
