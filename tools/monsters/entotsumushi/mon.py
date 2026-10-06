# エントツムシ（どく・ほのお × イモムシ）手打ち GBA風・デフォルメ（2〜3頭身）
# 見せ所：背中に 立つ 鉄の 煙突。体節と 同じ 輪を 重ねた 形で、毒の 煙を 吐く
import os, math
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kit.py'), encoding='utf-8').read())
from functools import lru_cache

META = dict(id='entotsumushi', name='エントツムシ', types=['poison', 'fire'], base='イモムシ', size='M')
PAL = {
    'k': '#101018', 'l': '#2a1a22',
    'A': '#bce452', 'B': '#6c9c2c', 'D': '#305224',      # 体（黄緑）
    'E': '#f2e2a4',                                      # 腹・いぼ足
    'S': '#a4a4b4', 'T': '#5e5e70', 'U': '#30303e',      # 鉄の 煙突
    'Y': '#ffe466', 'O': '#ff7a22', 'R': '#c4341c',      # 熱・火
    'P': '#c48ae4', 'Q': '#5e367c',                      # 毒の 煙
    'w': '#ffffff',
}
LIGHT = set('AESYPw')
KEEP_BLACK = set('wYOP')
RAMP = {'1': 'ABD', '2': 'STU', '4': 'EEB'}

SEG = [(35, 49, 7.2, 6.6), (27, 48, 7.6, 7.2), (19, 50, 6.6, 6.2), (12.5, 53, 5, 4.6)]
# ---------- 体節（輪が 重なる）＋ いぼ足 ----------
@lru_cache(None)
def seg(i, lift=0):
    cx, cy, rx, ry = SEG[i]; cy -= lift
    def d(g):
        ell(g, cx, cy, rx, ry, '1')
        for Y in range(H):                                                     # 腹（下 1/4）は クリーム
            for X in range(W):
                if g[Y][X] == '1' and Y - MY > cy + ry * .55: g[Y][X] = '4'
        if i < 3:
            poly(g, [(cx - 2, cy + ry - 2), (cx + 2, cy + ry - 2), (cx + 2, 59), (cx - 2.5, 59)], '4')   # いぼ足
    def p(g):
        dots(g, 'O', [(round(cx), round(cy + 1)), (round(cx) + 1, round(cy + 1))])     # 気門（火の 穴）
        put(g, round(cx), round(cy + 2), 'R')
        dots(g, 'P', [(round(cx - 3), round(cy - 3)), (round(cx + 2), round(cy - 4))])  # 毒の 斑
        dots(g, 'Q', [(round(cx - 3), round(cy - 2)), (round(cx + 2), round(cy - 3))])
        if i < 3: dots(g, 'k', [(round(cx - 2), 59), (round(cx), 59), (round(cx + 2), 59)])  # 足の かぎ
    return part(d, RAMP, p, r=2, tilt=.6)

# ---------- 煙突：体節と 同じ 輪を 4段 重ねる。輪の ふちが 赤く 焼ける ----------
@lru_cache(None)
def chimney(hot=0):
    def d(g):
        poly(g, [(20.5, 44), (29.5, 44), (28.5, 30), (21.5, 30)], '2')
        poly(g, [(19.5, 30), (30.5, 30), (30.5, 26), (19.5, 26)], '2')        # 口の かさ
    def p(g):
        for y in (33, 38):                                                 # 輪の つぎ目（焼けて 光る）
            for x in range(19, 32):
                if at(g, x, y) in 'STU': put(g, x, y, 'k')
                if at(g, x, y + 1) in 'STU': put(g, x, y + 1, ('Y' if hot else 'O') if 22 <= x <= 27 else 'R')
        for x in range(20, 31): put(g, x, 26, 'k' if x in (20, 30) else 'U')   # 口の やみ
        for x in range(21, 30): put(g, x, 27, 'R' if not hot else 'O')
        dots(g, 'S', [(21, 35), (21, 36), (21, 40), (21, 41)])
    return part(d, RAMP, p, open=[(17, 40, 33, 46)], r=1, tilt=.3)

# ---------- 毒の 煙（煙突の 口に つながって 立ちのぼる）----------
@lru_cache(None)
def smoke(ph=0, big=False):
    o = (0, 1, -1)[ph]
    t = G()
    cs = [(25, 24, 3), (23 + o, 20, 3.6), (27 - o, 16, 4), (22 + o, 13, 3.2)] if not big else \
         [(25, 23, 4), (22, 18, 5.5), (31, 17, 5), (26, 12, 5.5), (37, 14, 4.5), (17, 12, 3.5)]
    for cx, cy, r in cs: ell(t, cx, cy, r, r * .85, 'P')
    g = G()
    for Y in range(H):
        for X in range(W):
            if t[Y][X] == '.': continue
            e = (t[Y][X + 1] == '.') or (t[Y + 1][X] == '.') or (t[Y + 2][X] == '.' and (X + Y) % 2)
            g[Y][X] = 'Q' if e else 'P'
    if big:
        ell(g, 26, 20, 3, 3, 'O'); ell(g, 26, 20.5, 1.6, 1.6, 'Y')            # 中の 火
    else:
        dots(g, 'Q', [(24 + o, 19), (25 + o, 19), (26 - o, 15)])
    return Part(ink(g))

# ---------- 頭：大きく 丸い。つり目、口の 左右に 大あご ----------
EYES = {
    'open': ['kk......', '.kkkkk..', '..kwYkOk', '..kYOkOk', '...kkkk.'],
    'atk':  ['kk......', '.kkkkk..', '..kwwYYk', '..kYwYOk', '...kkkk.'],
    'blink': ['kk......', '.kkkkk..', '........', '..kkkkkk', '........'],
    'hit':  ['........', '.kk..kk.', '...kk...', '.kk..kk.', '........'],
    'ko':   ['........', '.k...k..', '..k.k...', '...k....', '..k.k...'],
}
@lru_cache(None)
def head(eye='open', bite=False):
    def d(g):
        ell(g, 46.5, 43, 10.5, 10, '1')
        poly(g, [(51, 48), (58, 47), (59, 53), (53, 55)], '1')                 # あご
    def p(g):
        stamp(g, 45, 37, EYES[eye])
        # 口と 大あご（茶色の かぎ ＝ 鉄の 色）
        if bite:
            stamp(g, 53, 46, ['kkkk..', 'kRRRkk', 'kRwwwk', 'kRRRRk', 'kwwwRk', 'kkkkkk'])
            stamp(g, 58, 45, ['kk', 'Sk', 'Tk', '..', 'Tk', 'Sk', 'kk'])
        else:
            stamp(g, 52, 48, ['kkkkkkk', '.kwkwkw', '..kkkkk'])
            stamp(g, 58, 46, ['kkk.', 'kSTk', '.kTk', '..kk'])
        dots(g, 'P', [(41, 40), (40, 45)]); dots(g, 'Q', [(41, 41), (40, 46)])
        dots(g, 'D', [(44, 51), (46, 52)])
    return part(d, RAMP, p, open=[(35, 38, 41, 54)], r=2, tilt=.6)

def frame(f):
    E = {'blink': 'blink', 'hit': 'hit', 'ko': 'ko', 'atk0': 'atk', 'atk1': 'atk', 'atk2': 'atk'}.get(f, 'open')
    lifts = [0, 0, 0, 0]; h = (0, 0); ph = 0; hot = 0; big = False; bite = False; root = (0, 0); ch = (0, 0)
    if f == 'idle1': ph = 1; h = (0, 1)
    if f == 'idle2': ph = 2; lifts = [1, 1, 0, 0]; h = (0, 1)
    if f == 'idle3': ph = 1
    if f == 'walk0': lifts = [0, 1, 2, 1]; ph = 1
    if f == 'walk1': lifts = [1, 2, 1, 0]; ph = 2; h = (1, -1)
    if f == 'walk2': lifts = [2, 1, 0, 0]; ph = 0; h = (1, -1)
    if f == 'walk3': lifts = [1, 0, 0, 1]; ph = 1
    if f == 'atk0': h = (-2, -1); hot = 1; lifts = [1, 1, 0, 0]
    if f == 'atk1': h = (3, 0); hot = 1; big = True; bite = True; root = (2, 0)
    if f == 'atk2': h = (2, 0); hot = 1; big = True; root = (2, 0); ph = 1
    if f == 'hit': root = (-3, 0); h = (-2, -2); lifts = [0, 1, 0, 0]
    ch = (2, -lifts[1])
    R = lambda o: (o[0] + root[0], o[1] + root[1])
    items = [(seg(3, lifts[3]), R((0, 0))), (seg(2, lifts[2]), R((0, 0)))]
    if f not in ('hit', 'ko'): items.append((smoke(ph, big), R(ch)))
    if f != 'ko': items.append((chimney(hot), R(ch)))
    items += [ (seg(1, lifts[1]), R((0, 0))), (seg(0, lifts[0]), R((0, 0))), (head(E, bite), R(h))]
    # 煙突は 2つ目の 体節の 上に 立つ（体節の 後ろに 回るので 根もとを 前に 出し直す）
    g = compose(items)
    return flip_ko(g, 60) if f == 'ko' else g

def layers(): return one_layer({f: frame(f) for f in FR})
FRAMES = {f: {} for f in FR}
PARENT = {}
