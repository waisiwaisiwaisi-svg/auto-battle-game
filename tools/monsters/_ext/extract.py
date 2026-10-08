# シートから 1体ずつ 切りだし → 白背景を 消す → 目標の 大きさへ 多数決で 縮める → 15色に 減色 → 1ドットの 輪郭
import sys, json, numpy as np
from collections import deque
from PIL import Image
IMG = '/tmp/claude-0/-home-user-auto-battle-game/27abe3ed-76ac-5b94-8383-de41dcf56044/images/'
PICKS = {
  'kamadon':    ('8.webp', (245, 20, 336, 137)),
  'pottoko':    ('8.webp', (160, 168, 270, 284)),
  'hyoukyuu':   ('8.webp', (345, 652, 430, 750)),
  'yukidome':   ('8.webp', (626, 640, 718, 752)),
  'furasukon':  ('8.webp', (90, 942, 153, 1064)),
  'shoberaa':   ('8.webp', (156, 1098, 256, 1214)),
  'sorabune':   ('8.webp', (816, 1255, 928, 1354)),
  'noroinui':   ('9.webp', (596, 290, 848, 566)),
  'kitsunemen': ('9.webp', (864, 276, 1132, 568)),
  'medamasho':  ('9.webp', (315, 648, 592, 978)),
}
def clean(a):
    """白背景（ふちから つながる 白っぽい 部分）を 透明に"""
    H, W, _ = a.shape; white = (np.abs(a - 255).sum(-1) < 75)
    bg = np.zeros((H, W), bool); q = deque()
    for y in range(H):
        for x in (0, W - 1):
            if white[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
    for x in range(W):
        for y in (0, H - 1):
            if white[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and white[ny, nx] and not bg[ny, nx]: bg[ny, nx] = True; q.append((ny, nx))
    # 囲まれた 大きな 真っ白の すきま（腕の 内側 など）も 背景に
    pure = (np.abs(a - 255).sum(-1) < 20) & ~bg; seen = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            if pure[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and pure[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
                if len(pts) > 250:
                    for p in pts: bg[p] = True
    fg = ~bg
    # いちばん 大きい かたまりと、その 近くの かけら（炎・きらきら）だけ のこす
    lab = np.zeros((H, W), int); comps = []; n = 0
    for y in range(H):
        for x in range(W):
            if fg[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and fg[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
                comps.append((len(pts), n))
    big = max(comps)[0]
    keep = {k for s, k in comps if s >= max(25, big * .01)}
    # ふちに さわる 小さな かけら（となりの 絵の 切れはし）を 捨てる
    for s, k in comps:
        ys, xs = np.nonzero(lab == k)
        if k in keep and s < big * .2 and (ys.min() == 0 or xs.min() == 0 or ys.max() == H - 1 or xs.max() == W - 1): keep.discard(k)
    return np.isin(lab, list(keep))
def shrink(a, mask, target):
    H, W, _ = a.shape; ys, xs = np.nonzero(mask); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; mask = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    H, W = mask.shape; s = max(H, W) / target; h, w = max(1, round(H / s)), max(1, round(W / s))
    out = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            y0, y1 = int(y * H / h), max(int(y * H / h) + 1, int((y + 1) * H / h)); x0, x1 = int(x * W / w), max(int(x * W / w) + 1, int((x + 1) * W / w))
            m = mask[y0:y1, x0:x1]
            if m.mean() >= .45:
                px = a[y0:y1, x0:x1][m]
                # 中央値に 近い 色（ぼけない ように 実在する 色を 選ぶ）
                med = np.median(px, 0); c = px[np.argmin(((px - med) ** 2).sum(1))]
                out[y, x, :3] = c; out[y, x, 3] = 255
    return out
def quant(rgba, n=14):
    im = Image.fromarray(rgba, 'RGBA'); rgb = im.convert('RGB'); alpha = np.asarray(im)[..., 3]
    q = rgb.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:n * 3]; idx = np.asarray(q).astype(int) + 1; idx[alpha == 0] = 0
    pal = ['#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3]) for i in range(n)]
    # 輪郭：まわりが 透明の ドットの 外側に 1ドット 黒（いちばん 暗い 色を 使う）
    lum = [sum(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in pal]; dark = int(np.argmin(lum)) + 1
    if lum[dark - 1] > 150: pal.append('#1a1022'); dark = len(pal)
    H, W = idx.shape; o = np.zeros((H + 2, W + 2), int); o[1:-1, 1:-1] = idx; res = o.copy()
    for y in range(H + 2):
        for x in range(W + 2):
            if o[y, x] == 0 and any(0 <= y + dy < H + 2 and 0 <= x + dx < W + 2 and o[y + dy, x + dx] > 0 for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))): res[y, x] = dark
    return res, pal
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
def rle(idx):
    flat = idx.ravel(); s = ''; i = 0
    while i < len(flat):
        j = i
        while j < len(flat) and flat[j] == flat[i] and j - i < 1295: j += 1
        n = j - i; s += AL[flat[i]] + (np.base_repr(n, 36).lower().rjust(2, '0')); i = j
    return s
if __name__ == '__main__':
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    data = {}; sheet = []
    for nm, (f, box) in PICKS.items():
        a = np.asarray(Image.open(IMG + f).convert('RGB').crop(box)).astype(int)
        m = clean(a); small = shrink(a, m, target); idx, pal = quant(small)
        data[nm] = {'w': idx.shape[1], 'h': idx.shape[0], 'pal': pal, 'd': rle(idx)}
        im = Image.new('RGBA', (idx.shape[1], idx.shape[0]))
        for y in range(idx.shape[0]):
            for x in range(idx.shape[1]):
                if idx[y, x]: im.putpixel((x, y), tuple(int(pal[idx[y, x] - 1][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        sheet.append(im); print(nm, idx.shape, len(pal))
    json.dump(data, open('ext.json', 'w'))
    Z = 4; W = sum(i.width * Z + 10 for i in sheet); H = max(i.height for i in sheet) * Z
    o = Image.new('RGB', (W, H), (236, 236, 242)); x = 0
    for im in sheet:
        b = Image.new('RGBA', im.size, (236, 236, 242, 255)); b.alpha_composite(im); b = b.convert('RGB').resize((im.width * Z, im.height * Z), Image.NEAREST); o.paste(b, (x, H - b.height)); x += b.width + 10
    o.save('ext_sheet.png')
