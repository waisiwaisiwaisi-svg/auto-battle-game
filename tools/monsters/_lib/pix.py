# 手打ち GBA風 モンスターの 共通エンジン
# - パーツ（文字マップ）を 重ねる → 動き（グループごとの ずらし／差しかえ絵）→ GBA風 仕上げ（内側の 線と 光側の 輪郭を 濃い色に）
# - 検査：16色以内・待機コマが 64x64 に おさまる・14コマ そろっている
# - 出力：コマごとの PNG、GIF、一覧、ゲーム用 JSON（パレット＋ランレングス）
import importlib.util, json, os, sys
from PIL import Image, ImageDraw

FRAMES = ['idle0', 'idle1', 'idle2', 'idle3', 'blink', 'walk0', 'walk1', 'walk2', 'walk3', 'atk0', 'atk1', 'atk2', 'hit', 'ko']
CW, CH, OX, OY = 96, 84, 16, 12   # 作業キャンバス（動きで はみ出しても 切れないよう 余白つき）

# ---------- 描くための 小道具（どれも 文字の 2次元配列を あつかう）----------
def grid(w, h, ch='.'): return [[ch] * w for _ in range(h)]
def rows_of(g): return [''.join(r) for r in g]
def grid_of(rows):
    w = max((len(r) for r in rows), default=0)
    return [list(r.ljust(w, '.')) for r in rows]
def outline(rows, ch='k'):
    """まわりに 1ドットの 輪郭を つける（はばと 高さは 2 ふえる）"""
    g = grid_of(rows); H, W = len(g), len(g[0]) if g else 0
    o = grid(W + 2, H + 2)
    for y in range(H):
        for x in range(W): o[y + 1][x + 1] = g[y][x]
    out = [r[:] for r in o]
    for y in range(H + 2):
        for x in range(W + 2):
            if o[y][x] != '.': continue
            if any(0 <= y + dy < H + 2 and 0 <= x + dx < W + 2 and o[y + dy][x + dx] != '.' for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))): out[y][x] = ch
    return rows_of(out)
def recolor(rows, mapping): return [''.join(mapping.get(c, c) for c in r) for r in rows]
def flip_h(rows): w = max(len(r) for r in rows); return [r.ljust(w, '.')[::-1] for r in rows]
def flip_v(rows): return list(reversed(rows))
def rot90(rows):
    g = grid_of(rows); h, w = len(g), len(g[0]); return [''.join(g[h - 1 - y][x] for y in range(h)) for x in range(w)]
def line(g, x0, y0, x1, y1, ch):
    """ピクセルパーフェクトな 直線（Bresenham）"""
    dx, dy = abs(x1 - x0), -abs(y1 - y0); sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1); e = dx + dy
    while True:
        if 0 <= y0 < len(g) and 0 <= x0 < len(g[0]): g[y0][x0] = ch
        if x0 == x1 and y0 == y1: break
        e2 = 2 * e
        if e2 >= dy: e += dy; x0 += sx
        if e2 <= dx: e += dx; y0 += sy
def poly(g, pts, ch):
    """多角形を ぬる（下書き・あたり用。陰影は 手で 打つ）"""
    for y in range(len(g)):
        for x in range(len(g[0])):
            px, py, c = x + .5, y + .5, False
            for i in range(len(pts)):
                (x1, y1), (x2, y2) = pts[i], pts[i - 1]
                if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
            if c: g[y][x] = ch
def ellipse(g, cx, cy, rx, ry, ch):
    for y in range(len(g)):
        for x in range(len(g[0])):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: g[y][x] = ch
def stamp(g, rows, x0, y0):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != '.' and 0 <= y0 + j < len(g) and 0 <= x0 + i < len(g[0]): g[y0 + j][x0 + i] = c

# ---------- 合成 ----------
def load(path):
    spec = importlib.util.spec_from_file_location('mon_' + os.path.basename(os.path.dirname(path)), path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def _off(M, g, mot):
    x = y = 0; parent = getattr(M, 'PARENT', {})
    while g:
        o = mot.get(g)
        if o: x += o[0]; y += o[1]
        if g == 'root': break
        g = parent.get(g, 'root')
    return x, y
def compose(M, frame):
    mot = M.FRAMES.get(frame, {})
    g = grid(CW, CH)
    for l in M.layers():
        if l.get('only') and frame not in l['only'].split('|'): continue
        if l.get('not_') and frame in l['not_'].split('|'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if frame in k.split('|'): rows = v
        ox, oy = _off(M, l['g'], mot)
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ': continue
                X, Y = l['x'] + i + ox + OX, l['y'] + j + oy + OY
                if 0 <= X < CW and 0 <= Y < CH: g[Y][X] = ch
    if mot.get('_flip'):
        ys = [y for y in range(CH) if any(c != '.' for c in g[y])]
        if ys:
            bottom = ys[-1]; body = [g[y] for y in range(ys[0], bottom + 1)][::-1]
            g = grid(CW, CH)
            for j, r in enumerate(body): g[bottom - len(body) + 1 + j] = r
    return finish(M, g)
def finish(M, g):
    """GBA風：まわりが 全部 色の 黒線は 内側の 線→濃い色。光の 当たる 外側の 輪郭も 濃い色（セルアウト）"""
    if 'l' not in M.PAL: return g
    light = getattr(M, 'LIGHT', set()); keep = getattr(M, 'KEEP_BLACK', set('w'))
    H, W = len(g), len(g[0])
    def at(y, x): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'k': continue
            nb = [at(y + dy, x + dx) for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))]
            if '.' not in nb and not any(c in keep for c in nb): out[y][x] = 'l'
            elif (at(y + 1, x) in light or at(y, x + 1) in light) and (at(y - 1, x) == '.' or at(y, x - 1) == '.'): out[y][x] = 'l'
    return out
def paint(M, g, bg=None):
    im = Image.new('RGBA', (CW, CH), bg or (0, 0, 0, 0)); px = im.load()
    for y in range(CH):
        for x in range(CW):
            c = g[y][x]
            if c != '.':
                h = M.PAL[c]; px[x, y] = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255)
    return im

# ---------- 検査 ----------
def check(M, gs):
    errs = []
    missing = [f for f in FRAMES if f not in M.FRAMES]
    if missing: errs.append(f'コマが たりない: {missing}')
    if len(M.PAL) > 16: errs.append(f'色が 多い: {len(M.PAL)} > 16')
    for f, g in gs.items():
        for r in g:
            for c in r:
                if c != '.' and c not in M.PAL: errs.append(f'{f}: パレットに ない 文字 {c!r}'); break
    g = gs['idle0']; ys = [y for y in range(CH) if any(c != '.' for c in g[y])]; xs = [x for x in range(CW) if any(g[y][x] != '.' for y in range(CH))]
    if ys and (ys[-1] - ys[0] + 1 > 64 or xs[-1] - xs[0] + 1 > 64): errs.append(f'待機コマが 64x64 を こえる: {xs[-1] - xs[0] + 1}x{ys[-1] - ys[0] + 1}')
    return errs, (xs[-1] - xs[0] + 1, ys[-1] - ys[0] + 1) if ys else (0, 0)

# ---------- 出力 ----------
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
def export(M, gs):
    """ゲーム用：全コマ共通の 枠で 切りぬき、パレット番号＋ランレングス"""
    xs = [x for g in gs.values() for y in range(CH) for x in range(CW) if g[y][x] != '.']
    ys = [y for g in gs.values() for y in range(CH) for x in range(CW) if g[y][x] != '.']
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    keys = list(M.PAL); idx = {k: i + 1 for i, k in enumerate(keys)}
    out = {'w': x1 - x0 + 1, 'h': y1 - y0 + 1, 'pal': [M.PAL[k] for k in keys], 'f': {}}
    for f, g in gs.items():
        flat = [idx.get(g[y][x], 0) if g[y][x] != '.' else 0 for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
        s, i = [], 0
        while i < len(flat):
            j = i
            while j < len(flat) and flat[j] == flat[i] and j - i < 1295: j += 1
            n = j - i; s.append(AL[flat[i]] + format(n, 'x').rjust(2, '0') if n < 256 else AL[flat[i]] + '~' + format(n, 'x').rjust(3, '0')); i = j
        out['f'][f] = ''.join(s)
    return out
def build(path, outdir=None, quiet=False):
    M = load(path); d = os.path.dirname(os.path.abspath(path)); outdir = outdir or os.path.join(d, 'out'); os.makedirs(outdir, exist_ok=True)
    gs = {f: compose(M, f) for f in FRAMES if f in M.FRAMES}
    errs, size = check(M, gs)
    ims = {f: paint(M, g) for f, g in gs.items()}
    for f, im in ims.items(): im.save(os.path.join(outdir, f + '.png'))
    Z = 4; BG = (246, 246, 246, 255)
    def big(im): b = Image.new('RGBA', im.size, BG); b.alpha_composite(im); return b.convert('RGB').resize((CW * Z, CH * Z), Image.NEAREST)
    seq = [('idle0', 240), ('idle1', 240), ('idle2', 240), ('idle3', 240), ('idle0', 240), ('blink', 110), ('idle1', 240), ('idle2', 240), ('idle3', 240)] + \
          [('walk0', 130), ('walk1', 130), ('walk2', 130), ('walk3', 130)] * 2 + \
          [('atk0', 380), ('atk1', 150), ('atk2', 260), ('idle0', 300), ('hit', 400), ('idle0', 300), ('ko', 1200)]
    fr = [big(ims[f]) for f, _ in seq if f in ims]
    fr[0].save(os.path.join(d, 'anim.gif'), save_all=True, append_images=fr[1:], duration=[t for f, t in seq if f in ims], loop=0)
    sh = Image.new('RGB', (CW * Z * 7, (CH * Z + 20) * 2), (40, 40, 52)); dr = ImageDraw.Draw(sh)
    for i, f in enumerate(FRAMES):
        if f not in ims: continue
        x, y = (i % 7) * CW * Z, (i // 7) * (CH * Z + 20); sh.paste(big(ims[f]), (x, y + 20)); dr.text((x + 6, y + 4), f, fill='white')
    sh.save(os.path.join(d, 'frames.png'))
    data = export(M, gs); data['meta'] = getattr(M, 'META', {}); data['size'] = size
    json.dump(data, open(os.path.join(d, 'sprite.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    if not quiet: print(os.path.basename(d), 'size', size, 'colors', len(M.PAL), 'OK' if not errs else 'NG', *errs)
    return errs
