# 追加トレーナーの シート（2人 × 4ポーズ、透過）を ドットに もどして trainers.json に 足す
#   python3 extract_more.py   … sheets/*.webp を SHEETS の ならびで 読む
import json, os, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
# シート → [上の人, 下の人]
SHEETS = {
    's30.webp': ['researcher', 'ranger'],
    's31.webp': ['gamer', 'camera'],
    's32.webp': ['vet', 'barista'],
    's33.webp': ['florist', 'mechanic'],
    's34.webp': ['firefighter', 'chef'],
}

def bands(v, mn=10):
    out = []; inb = False
    for i, x in enumerate(v):
        if x and not inb: s = i; inb = True
        if not x and inb: out.append((s, i)); inb = False
    if inb: out.append((s, len(v)))
    return [b for b in out if b[1] - b[0] > mn]

def rebuild(sub, s, ox, oy):
    # セルの まんなか ふきんの ピクセルから 代表色（中央値に いちばん ちかい 色）を えらぶ
    H, W, _ = sub.shape; nx, ny = int((W - ox) / s), int((H - oy) / s); r = max(1, int(s * .3))
    cy = (oy + (np.arange(ny) + .5) * s).astype(int); cx = (ox + (np.arange(nx) + .5) * s).astype(int)
    d = np.arange(-r, r + 1)
    yy = np.clip(cy[:, None, None, None] + d[None, None, :, None], 0, H - 1)
    xx = np.clip(cx[None, :, None, None] + d[None, None, None, :], 0, W - 1)
    blk = sub[yy, xx].reshape(ny, nx, -1, 4).astype(float)
    op = blk[..., 3] > 128
    keep = op.mean(-1) >= .5
    rgb = np.where(op[..., None], blk[..., :3], np.nan)
    med = np.nanmedian(np.where(keep[..., None, None], rgb, 0), 2)
    dist = np.nansum((rgb - med[:, :, None]) ** 2, -1); dist[~op] = 1e18
    pick = np.take_along_axis(blk[..., :3], dist.argmin(-1)[..., None, None].repeat(3, -1), 2)[:, :, 0]
    o = np.zeros((ny, nx, 4), int); o[..., :3] = pick.astype(int); o[..., 3] = np.where(keep, 255, 0)
    return o

def err(sub, s, ox, oy, o):
    yi = np.clip(((np.arange(sub.shape[0]) - oy) / s).astype(int), 0, o.shape[0] - 1)
    xi = np.clip(((np.arange(sub.shape[1]) - ox) / s).astype(int), 0, o.shape[1] - 1)
    up = o[yi][:, xi]; m = sub[..., 3] > 128
    return np.abs(up[..., :3] - sub[..., :3])[m].mean() + 60 * np.mean((up[..., 3] > 0) != m)

def best(sub, scales):
    bb = None
    for s in scales:
        for ox in np.arange(0, s, 1):
            for oy in np.arange(0, s, 1):
                o = rebuild(sub, s, ox, oy); e = err(sub, s, ox, oy, o)
                if bb is None or e < bb[0]: bb = (e, s, o)
    return bb

T = json.load(open(os.path.join(HERE, 'trainers.json')))
for sheet, names in SHEETS.items():
    A = np.asarray(Image.open(os.path.join(HERE, 'sheets', sheet)).convert('RGBA')).astype(int)
    A[A[..., 3] <= 100] = 0
    fg = A[..., 3] > 100; H = A.shape[0]
    for who, (r0, r1) in zip(names, [(0, H // 2), (H // 2, H)]):
        cs = bands(fg[r0:r1].any(0), 30)[:4]
        frames = []; scale = None
        for k, (c0, c1) in enumerate(cs):
            rr = bands(fg[r0:r1, c0:c1].any(1), 10); y0, y1 = r0 + rr[0][0], r0 + rr[-1][1]
            sub = A[max(0, y0 - 4):y1 + 4, max(0, c0 - 4):c1 + 4]
            e, s, o = best(sub, np.arange(7.0, 9.6, .1) if scale is None else [scale])
            scale = s
            ys, xs = np.nonzero(o[..., 3]); o = o[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            frames.append(o); print(who, k, 'grid %.1f err %.1f' % (s, e), o.shape)
        # 共通パレット（人ごと）
        px = np.concatenate([f[f[..., 3] > 0][:, :3] for f in frames]); cnt = {}
        for c in map(tuple, px): cnt[c] = cnt.get(c, 0) + 1
        pal = []
        for c, _ in sorted(cnt.items(), key=lambda x: -x[1]):
            if not any(sum((p - q) ** 2 for p, q in zip(c, pp)) < 26 ** 2 for pp in pal): pal.append(c)
            if len(pal) >= 63: break
        P = np.array(pal); Hh = max(f.shape[0] for f in frames)
        feet = [int(np.nonzero(f[-4:, :, 3].any(0))[0].mean()) for f in frames]   # 足もとの まんなか
        L = max(feet); R = max(f.shape[1] - c for f, c in zip(frames, feet)); W = L + R
        T[who] = {'pal': ['#%02x%02x%02x' % tuple(int(v) for v in c) for c in pal], 'w': W, 'h': Hh, 'f': []}
        for f, c in zip(frames, feet):
            idx = np.argmin(((f[..., None, :3] - P[None, None]) ** 2).sum(-1), -1) + 1; idx[f[..., 3] == 0] = 0
            full = np.zeros((Hh, W), int); full[Hh - f.shape[0]:, L - c:L - c + f.shape[1]] = idx   # 足もとを そろえる
            T[who]['f'].append(full.tolist())
        print(who, len(pal), 'colors', W, Hh)
json.dump(T, open(os.path.join(HERE, 'trainers.json'), 'w'))
# 確認用
Z = 3; keys = list(T); rows = []
for w in keys:
    pal = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in T[w]['pal']]; ims = []
    for f in T[w]['f']:
        f = np.array(f); im = np.full((f.shape[0], f.shape[1], 3), (200, 205, 215), np.uint8)
        for v in range(1, f.max() + 1): im[f == v] = pal[v - 1]
        ims.append(Image.fromarray(im).resize((f.shape[1] * Z, f.shape[0] * Z), Image.NEAREST))
    rows.append(ims)
Wd = max(sum(i.width + 8 for i in r) for r in rows); S = Image.new('RGB', (Wd * 2, (max(i.height for r in rows for i in r) + 8) * ((len(rows) + 1) // 2)), (200, 205, 215))
for n, r in enumerate(rows):
    x = (n % 2) * Wd; y = (n // 2) * (max(i.height for r in rows for i in r) + 8)
    for i in r: S.paste(i, (x, y)); x += i.width + 8
S.save(os.path.join(HERE, 'preview.png'))
