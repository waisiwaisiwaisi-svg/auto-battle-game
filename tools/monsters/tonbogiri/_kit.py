# 下書き・仕上げの 小道具（このフォルダ 専用。mon.py から exec で 読む）
# 座標は すべて 64x64 の 画面座標（左上 0,0／足もと y=60 前後）。動きで はみ出せる よう 余白つきの 紙に 描く
from pix import grid, rows_of
MX, MY = 12, 10
W, H = 64 + 2 * MX, 64 + 2 * MY
def G(): return grid(W, H)
def _in(x, y): return 0 <= x < W and 0 <= y < H
def at(g, x, y):
    X, Y = x + MX, y + MY
    return g[Y][X] if _in(X, Y) else '.'
def put(g, x, y, ch):
    X, Y = x + MX, y + MY
    if _in(X, Y): g[Y][X] = ch
def dots(g, ch, pts):
    for x, y in pts: put(g, x, y, ch)
def ell(g, cx, cy, rx, ry, ch):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: put(g, x, y, ch)
def poly(g, pts, ch):
    ys = [p[1] for p in pts]; xs = [p[0] for p in pts]
    for y in range(int(min(ys)) - 1, int(max(ys)) + 2):
        for x in range(int(min(xs)) - 1, int(max(xs)) + 2):
            px, py, c = x + .5, y + .5, False
            for i in range(len(pts)):
                (x1, y1), (x2, y2) = pts[i], pts[i - 1]
                if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
            if c: put(g, x, y, ch)
def tube(g, path, rad, ch):
    for i in range(len(path) - 1):
        (x0, y0), (x1, y1) = path[i], path[i + 1]; r0, r1 = rad[i], rad[i + 1]
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for j in range(n + 1):
            t = j / n; cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
            for y in range(int(cy - r - 1), int(cy + r + 2)):
                for x in range(int(cx - r - 1), int(cx + r + 2)):
                    if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r: put(g, x, y, ch)
def stamp(g, x0, y0, rows):
    """手打ちの 絵を 置く（'.' は すきとおる）"""
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c not in '. ': put(g, x0 + i, y0 + j, c)
def recol(g, mp, box=None):
    for Y in range(H):
        for X in range(W):
            x, y = X - MX, Y - MY
            if box and not (box[0] <= x <= box[2] and box[1] <= y <= box[3]): continue
            if g[Y][X] in mp: g[Y][X] = mp[g[Y][X]]
def shade(g, ramps, r=2, hi=.3, lo=-.25, tilt=.5, rim=True):
    """光は 左上：ふちの 向き（まわりの ぬりの かたより）＋上ほど 明るい。上・左の ふち 1ドットは 明、右下の ふちは 暗"""
    m = [[1 if g[y][x] != '.' else 0 for x in range(W)] for y in range(H)]
    ys = [y for y in range(H) if any(m[y])]
    if not ys: return g
    y0, y1 = ys[0], ys[-1]
    def B(x, y):
        s = n = 0
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                n += 1; s += m[yy][xx] if _in(xx, yy) else 0
        return s / n
    def M(x, y): return m[y][x] if _in(x, y) else 0
    out = [row[:] for row in g]
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c not in ramps: continue
            v = (B(x + 1, y) - B(x - 1, y)) * 1.6 + (B(x, y + 1) - B(x, y - 1)) * 2.5 + tilt * (.45 - (y - y0) / max(1, y1 - y0))
            h, md, d = ramps[c]
            o = h if v > hi else d if v < lo else md
            if rim:
                if not M(x, y + 1) or not M(x + 1, y): o = d
                elif (not M(x, y - 1) or not M(x - 1, y)) and v > lo: o = h
            out[y][x] = o
    return out
def ink(g, ch='k'):
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(_in(x + dx, y + dy) and g[y + dy][x + dx] != '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y][x] = ch
    return out
class Part:
    def __init__(s, g, open=None): s.g = g; s.open = open or []
def part(draw, ramps=None, paint=None, open=None, **kw):
    g = G(); draw(g)
    if ramps: g = shade(g, ramps, **kw)
    if paint: paint(g)
    return Part(ink(g), open)
def compose(items):
    """items: [(Part, (dx, dy)), ...] 奥から 手前。open の 箱の 中では 輪郭を 下の 色に とかす（付け根を なじませる）"""
    out = G()
    for p, (dx, dy) in items:
        for Y in range(H):
            for X in range(W):
                c = p.g[Y][X]
                if c == '.': continue
                Xo, Yo = X + dx, Y + dy
                if not _in(Xo, Yo): continue
                if c == 'k' and out[Yo][Xo] not in '.k':
                    x, y = X - MX, Y - MY
                    if any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in p.open): continue
                out[Yo][Xo] = c
    return out
def flip_ko(g, ground=60):
    """ひっくり かえって たおれる（上下 反転して 地面に おとす）"""
    ys = [y for y in range(H) if any(c != '.' for c in g[y])]
    band = [g[y] for y in range(ys[0], ys[-1] + 1)][::-1]
    out = G(); b = ground + MY
    for j, r in enumerate(band):
        Y = b - len(band) + 1 + j
        if 0 <= Y < H: out[Y] = r[:]
    return out
def shift(g, dx, dy):
    out = G()
    for Y in range(H):
        for X in range(W):
            if g[Y][X] != '.' and _in(X + dx, Y + dy): out[Y + dy][X + dx] = g[Y][X]
    return out
def over(base, top):
    out = [r[:] for r in base]
    for Y in range(H):
        for X in range(W):
            if top[Y][X] != '.': out[Y][X] = top[Y][X]
    return out
FR = ['idle0', 'idle1', 'idle2', 'idle3', 'blink', 'walk0', 'walk1', 'walk2', 'walk3', 'atk0', 'atk1', 'atk2', 'hit', 'ko']
def one_layer(frames):
    """コマごとに 組んだ 絵を 1枚の 差しかえ レイヤーに する"""
    rs = {f: rows_of(frames[f]) for f in FR}
    return [dict(n='all', g='root', x=-MX, y=-MY, rows=rs['idle0'], alt={f: rs[f] for f in FR})]
