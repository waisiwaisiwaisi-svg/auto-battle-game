# 32×32 版の シートから ドットを 正確に 復元：粒の 大きさ（約3ピクセル）と 位置を 探して、各マスの 中心の 色を 取る
import sys, json, numpy as np
from collections import deque
from PIL import Image
sys.path.insert(0, '.')
from extract import AL, rle
IMG = '/tmp/claude-0/-home-user-auto-battle-game/27abe3ed-76ac-5b94-8383-de41dcf56044/images/'
PICKS = {
  'kamadon':    ('12.webp', (245, 20, 336, 137)),
  'pottoko':    ('12.webp', (160, 168, 270, 284)),
  'hyoukyuu':   ('12.webp', (345, 652, 430, 750)),
  'yukidome':   ('12.webp', (626, 640, 718, 752)),
  'furasukon':  ('12.webp', (90, 942, 153, 1064)),
  'shoberaa':   ('12.webp', (156, 1098, 256, 1214)),
  'sorabune':   ('12.webp', (816, 1255, 928, 1354)),
  'noroinui':   ('10.webp', (596, 290, 848, 566)),
  'kitsunemen': ('10.webp', (864, 276, 1132, 568)),
  'medamasho':  ('10.webp', (315, 648, 592, 978)),
}
def grid_fit(a, s0):
    """色の さかい目が 格子線に のる 割合で 粒の 大きさを 決める（合う 中で いちばん 大きい 粒）"""
    g = a.mean(-1)
    ex = np.nonzero((np.abs(np.diff(g, axis=1)) > 45).any(0))[0] + 1.0
    ey = np.nonzero((np.abs(np.diff(g, axis=0)) > 45).any(1))[0] + 1.0
    res = []
    for s in np.arange(s0 * .9, s0 * 1.1, .02):
        best = (0, 0, 0)
        for o in np.arange(0, s, .1):
            fx = np.mean(np.minimum((ex - o) % s, s - (ex - o) % s) < .55) if len(ex) else 0
            if fx > best[0]: best = (fx, o, 0)
        bo = best[1]; byy = (0, 0)
        for o in np.arange(0, s, .1):
            fy = np.mean(np.minimum((ey - o) % s, s - (ey - o) % s) < .55) if len(ey) else 0
            if fy > byy[0]: byy = (fy, o)
        res.append(((best[0] + byy[0]) / 2, s, bo, byy[1]))
    f, s, ox, oy = max(res)
    return s, ox, oy
def rebuild(a, s, ox, oy):
    H, W, _ = a.shape; nx = int((W - ox) / s); ny = int((H - oy) / s)
    out = np.zeros((ny, nx, 3), int)
    for j in range(ny):
        for i in range(nx):
            cy, cx = oy + (j + .5) * s, ox + (i + .5) * s
            blk = a[int(cy - s * .25):int(cy + s * .25) + 1, int(cx - s * .25):int(cx + s * .25) + 1].reshape(-1, 3)
            med = np.median(blk, 0); out[j, i] = blk[np.argmin(((blk - med) ** 2).sum(1))]
    return out
def bg_mask(c):
    H, W, _ = c.shape; white = np.abs(c - 255).sum(-1) < 90; bg = np.zeros((H, W), bool); q = deque()
    for y in range(H):
        for x in range(W):
            if (y in (0, H - 1) or x in (0, W - 1)) and white[y, x]: bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and white[ny, nx] and not bg[ny, nx]: bg[ny, nx] = True; q.append((ny, nx))
    # 囲まれた 白い すきま（4マス以上）も 背景
    pure = (np.abs(c - 255).sum(-1) < 30) & ~bg; seen = np.zeros_like(bg)
    for y in range(H):
        for x in range(W):
            if pure[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and pure[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
                if len(pts) >= 6:
                    for p in pts: bg[p] = True
    fg = ~bg
    # 小さな はぐれた かけら（となりの 絵の 切れはし・数字）を 消す
    lab = np.zeros((H, W), int); n = 0; comps = []
    for y in range(H):
        for x in range(W):
            if fg[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; cnt = 0; edge = False
                while q:
                    cy, cx = q.popleft(); cnt += 1; edge |= cy in (0, H - 1) or cx in (0, W - 1)
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and fg[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
                comps.append((cnt, n, edge))
    big = max(comps)[0]; keep = [k for c, k, e in comps if c >= 3 and not (e and c < big * .3)]
    return np.isin(lab, keep)
def quant(c, m, n=15):
    im = Image.fromarray(c.astype(np.uint8), 'RGB'); q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:n * 3]; idx = np.asarray(q).astype(int) + 1; idx[~m] = 0
    used = sorted(set(idx[idx > 0].ravel())); remap = {u: i + 1 for i, u in enumerate(used)}
    idx = np.vectorize(lambda v: remap.get(v, 0))(idx)
    pal = ['#%02x%02x%02x' % tuple(pal[(u - 1) * 3:(u - 1) * 3 + 3]) for u in used]
    ys, xs = np.nonzero(idx); idx = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return idx, pal
if __name__ == '__main__':
    data = {}; sheet = []
    for nm, (f, box) in PICKS.items():
        a = np.asarray(Image.open(IMG + f).convert('RGB').crop(box)).astype(int)
        s, ox, oy = grid_fit(a, {'12.webp': 3.4, '11.webp': 3.2, '10.webp': 7.3}[f]); c = rebuild(a, s, ox, oy); m = bg_mask(c); idx, pal = quant(c, m)
        data[nm] = {'w': int(idx.shape[1]), 'h': int(idx.shape[0]), 'pal': pal, 'd': rle(idx), 'ms': 2.2}
        im = Image.new('RGBA', (idx.shape[1], idx.shape[0]))
        for y in range(idx.shape[0]):
            for x in range(idx.shape[1]):
                if idx[y, x]: im.putpixel((x, y), tuple(int(pal[idx[y, x] - 1][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        sheet.append(im); print(nm, 'grid %.2f' % s, idx.shape, len(pal), flush=True)
    json.dump(data, open('ext32.json', 'w'))
    Z = 8; W = sum(i.width * Z + 12 for i in sheet); H = max(i.height for i in sheet) * Z
    o = Image.new('RGB', (W, H), (236, 236, 242)); x = 0
    for im in sheet:
        b = Image.new('RGBA', im.size, (236, 236, 242, 255)); b.alpha_composite(im); b = b.convert('RGB').resize((im.width * Z, im.height * Z), Image.NEAREST); o.paste(b, (x, H - b.height)); x += b.width + 12
    o.save('ext32_sheet.png')
