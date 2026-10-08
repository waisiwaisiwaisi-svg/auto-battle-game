# ChatGPT が 作った 8コマの シート（2段×4）を ドットに もどして GIF に する
import numpy as np, math
from PIL import Image
SRC = Image.open('sheet.webp').convert('RGBA'); A = np.asarray(SRC).astype(int)
S = 4                     # ドット 1粒 = 4ピクセル
CW, CH = SRC.width / 4, SRC.height / 2
def rebuild(sub, ox, oy):
    H, W, _ = sub.shape; nx, ny = int((W - ox) / S), int((H - oy) / S)
    out = np.zeros((ny, nx, 4), int)
    for j in range(ny):
        for i in range(nx):
            cy, cx = int(oy + (j + .5) * S), int(ox + (i + .5) * S)
            b = sub[cy - 1:cy + 2, cx - 1:cx + 2].reshape(-1, 4)
            if (b[:, 3] > 128).mean() < .5: continue
            b = b[b[:, 3] > 128]; med = np.median(b, 0); out[j, i] = (*b[np.argmin(((b - med) ** 2).sum(1))][:3], 255)
    return out
def err(sub, o):
    up = np.repeat(np.repeat(o, S, 0), S, 1); return up
frames = []
for r in range(2):
    for c in range(4):
        x0, y0 = int(c * CW), int(r * CH); sub = A[y0:int(y0 + CH), x0:int(x0 + CW)]
        best = None
        for ox in np.arange(0, S, .5):
            for oy in np.arange(0, S, .5):
                o = rebuild(sub, ox, oy); up = np.repeat(np.repeat(o, S, 0), S, 1)
                s2 = sub[int(oy):int(oy) + up.shape[0], int(ox):int(ox) + up.shape[1]]; m = s2[..., 3] > 128
                e = np.abs(up[:s2.shape[0], :s2.shape[1], :3] - s2[..., :3])[m].mean()
                if best is None or e < best[0]: best = (e, o, ox, oy)
        e, o, ox, oy = best; ys, xs = np.nonzero(o[..., 3])
        frames.append(dict(o=o, x=round((x0 + ox) / S), bottom=ys.max(), y=round((y0 + oy) / S)))
        print(r, c, 'err %.1f' % e, o.shape)
# 色を まとめる（全コマ 共通）
px = np.concatenate([f['o'][f['o'][..., 3] > 0][:, :3] for f in frames]); cnt = {}
for cc in map(tuple, px): cnt[cc] = cnt.get(cc, 0) + 1
pal = []
for cc, _ in sorted(cnt.items(), key=lambda x: -x[1]):
    if not any(sum((a - b) ** 2 for a, b in zip(cc, p)) < 26 ** 2 for p in pal): pal.append(cc)
P = np.array(pal); print('colors', len(pal))
# 足もとを そろえて 同じ キャンバスに 置く（横は 後ろ足の 先＝地面に ついた ままの 足で そろえる）
for f in frames:
    o = f['o']; ys, xs = np.nonzero(o[..., 3]); low = ys >= ys.max() - 5; f['foot'] = xs[low].max()
FOOT = max(f['foot'] for f in frames)
L = min(f['o'].shape[1] for f in frames)
Wc = max(f['o'].shape[1] for f in frames) + 8; base = max(f['bottom'] for f in frames) + 2; Hc = base + 4
out = []
for k, f in enumerate(frames):
    o = f['o']; idx = np.argmin(((o[..., None, :3] - P[None, None]) ** 2).sum(-1), -1)
    q = np.zeros_like(o); q[..., :3] = P[idx]; q[..., 3] = o[..., 3]
    F = np.zeros((Hc, Wc, 4), np.uint8); dy = base - f['bottom']
    dx = FOOT - f['foot'] + 2; print('frame', k, 'dx', dx)
    for y, x in zip(*np.nonzero(q[..., 3])):
        if 0 <= y + dy < Hc and 0 <= x + dx < Wc: F[y + dy, x + dx] = q[y, x]
    out.append(Image.fromarray(F, 'RGBA'))
def gif(fr, durs, name, z=5, bg=(34, 38, 58)):
    o = []
    for f in fr:
        g = Image.new('RGBA', f.size, bg + (255,)); g.alpha_composite(f); o.append(g.convert('RGB').resize((f.width * z, f.height * z), Image.NEAREST))
    o[0].save(name, save_all=True, append_images=o[1:], duration=durs, loop=0)
gif(out, [160, 140, 160, 90, 80, 110, 130, 220], 'gpt_attack.gif')
for k, f in enumerate(out): f.save('f%d.png' % k)
z = 4; sheet = Image.new('RGB', (Wc * z * 4, Hc * z * 2), (34, 38, 58))
for k, f in enumerate(out):
    g = Image.new('RGBA', f.size, (34, 38, 58, 255)); g.alpha_composite(f); sheet.paste(g.convert('RGB').resize((Wc * z, Hc * z), Image.NEAREST), ((k % 4) * Wc * z, (k // 4) * Hc * z))
sheet.save('gpt_frames.png')
