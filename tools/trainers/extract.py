# トレーナーの シート（2人 × 4ポーズ、透過）を ドットに もどす → trainers.json
import json, numpy as np
from PIL import Image
A = np.asarray(Image.open('sheet.webp').convert('RGBA')).astype(int)
fg = A[..., 3] > 100
def bands(v, mn=10):
    out = []; inb = False
    for i, x in enumerate(v):
        if x and not inb: s = i; inb = True
        if not x and inb: out.append((s, i)); inb = False
    if inb: out.append((s, len(v)))
    return [b for b in out if b[1] - b[0] > mn]
def rebuild(sub, s, ox, oy):
    H, W, _ = sub.shape; nx, ny = int((W - ox) / s), int((H - oy) / s); r = max(1, int(s * .3))
    o = np.zeros((ny, nx, 4), int)
    for j in range(ny):
        for i in range(nx):
            cy, cx = int(oy + (j + .5) * s), int(ox + (i + .5) * s)
            b = sub[max(0, cy - r):cy + r + 1, max(0, cx - r):cx + r + 1].reshape(-1, 4)
            if (b[:, 3] > 128).mean() < .5: continue
            b = b[b[:, 3] > 128]; med = np.median(b, 0); o[j, i] = (*b[np.argmin(((b - med) ** 2).sum(1))][:3], 255)
    return o
def best(sub):
    bb = None
    for s in np.arange(7.4, 8.8, .1):
        for ox in np.arange(0, s, 1):
            for oy in np.arange(0, s, 1):
                o = rebuild(sub, s, ox, oy)
                yi = np.clip(((np.arange(sub.shape[0]) - oy) / s).astype(int), 0, o.shape[0] - 1)
                xi = np.clip(((np.arange(sub.shape[1]) - ox) / s).astype(int), 0, o.shape[1] - 1)
                up = o[yi][:, xi]; m = sub[..., 3] > 128
                e = np.abs(up[..., :3] - sub[..., :3])[m].mean() + 60 * np.mean((up[..., 3] > 0) != m)
                if bb is None or e < bb[0]: bb = (e, s, o)
    return bb
rows = bands(fg.any(1))
H = A.shape[0]
rows = [(0, H // 2), (H // 2, H)]   # 2人ぶん
frames = {}
for who, (r0, r1) in zip(['girl', 'boy'], rows):
    cs = bands(fg[r0:r1].any(0), 30)
    print(who, cs)
    for k, (c0, c1) in enumerate(cs[:4]):
        sub = A[r0:r1, max(0, c0 - 4):c1 + 4]
        e, s, o = best(sub)
        ys, xs = np.nonzero(o[..., 3]); o = o[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        frames[f'{who}{k}'] = o; print(who, k, 'grid %.1f err %.1f' % (s, e), o.shape)
# 共通パレット（人ごと）
out = {}
for who in ['girl', 'boy']:
    fs = [frames[f'{who}{k}'] for k in range(4)]
    px = np.concatenate([f[f[..., 3] > 0][:, :3] for f in fs]); cnt = {}
    for c in map(tuple, px): cnt[c] = cnt.get(c, 0) + 1
    pal = []
    for c, _ in sorted(cnt.items(), key=lambda x: -x[1]):
        if not any(sum((p - q) ** 2 for p, q in zip(c, pp)) < 30 ** 2 for pp in pal): pal.append(c)
    P = np.array(pal); Hh = max(f.shape[0] for f in fs)
    feet = [int(np.nonzero(f[-4:, :, 3].any(0))[0].mean()) for f in fs]   # 足もとの まんなか
    L = max(feet); R = max(f.shape[1] - c for f, c in zip(fs, feet)); W = L + R
    out[who] = {'pal': ['#%02x%02x%02x' % c for c in pal], 'w': W, 'h': Hh, 'f': []}
    for f in fs:
        idx = np.argmin(((f[..., None, :3] - P[None, None]) ** 2).sum(-1), -1) + 1; idx[f[..., 3] == 0] = 0
        c = feet[fs.index(f) if False else [id(x) for x in fs].index(id(f))]; full = np.zeros((Hh, W), int); full[Hh - f.shape[0]:, L - c:L - c + f.shape[1]] = idx   # 足もとを そろえる
        out[who]['f'].append(full.tolist())
    print(who, len(pal), 'colors', W, Hh)
json.dump(out, open('trainers.json', 'w'))
# 確認用
Z = 4; S = Image.new('RGB', (sum(out[w]['w'] * Z + 10 for w in out for _ in range(4)), max(out[w]['h'] for w in out) * Z), (200, 205, 215)); x = 0
for w in out:
    pal = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in out[w]['pal']]
    for f in out[w]['f']:
        f = np.array(f); im = Image.new('RGB', (f.shape[1], f.shape[0]), (200, 205, 215))
        for yy, xx in zip(*np.nonzero(f)): im.putpixel((xx, yy), pal[f[yy, xx] - 1])
        S.paste(im.resize((f.shape[1] * Z, f.shape[0] * Z), Image.NEAREST), (x, 0)); x += f.shape[1] * Z + 10
S.save('preview.png')
