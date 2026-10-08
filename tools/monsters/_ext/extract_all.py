# 透過シート（ゴースト 10体・通常 100体・無機物 100体）から 全員を 切りだして ドットに もどす
# 使い方: python3 extract_all.py  → all.json（id → 絵）と 一覧画像 sheet_<名前>.png
import sys, json, numpy as np
from collections import deque
from PIL import Image, ImageDraw
sys.path.insert(0, '.')
from extract import rle
from extract32 import grid_fit
IMG = '/tmp/claude-0/-home-user-auto-battle-game/27abe3ed-76ac-5b94-8383-de41dcf56044/images/'
TYPES = ['fire', 'water', 'grass', 'elec', 'ice', 'fighting', 'poison', 'ground', 'wind', 'dragon']
SHEETS = {  # 名前: (ファイル, ドット 1粒の 大きさの 目安, 左の ラベルの 幅)
    'g': ('13.webp', 8.0, 0),      # ゴースト 2段×5
    'a': ('14.webp', 2.0, 70),     # 通常（いきもの）10段×10
    'b': ('15.webp', 2.0, 70),     # 無機物・どうぐ 10段×10
}

def comps(m):
    H, W = m.shape; lab = np.zeros((H, W), int); out = []; n = 0
    for y in range(H):
        for x in range(W):
            if m[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
                p = np.array(pts); out.append(p)
    return out

def bands(m):
    rows = m.any(1); out = []; inb = False
    for y, v in enumerate(rows):
        if v and not inb: s = y; inb = True
        if not v and inb: out.append((s, y)); inb = False
    if inb: out.append((s, len(rows)))
    return [b for b in out if b[1] - b[0] > 3]

def rebuild(a, s, ox, oy):
    H, W, _ = a.shape; nx, ny = int((W - ox) / s), int((H - oy) / s); r = max(1, int(s * .3))
    out = np.zeros((ny, nx, 4), int)
    for j in range(ny):
        for i in range(nx):
            cy, cx = int(oy + (j + .5) * s), int(ox + (i + .5) * s)
            b = a[max(0, cy - r):cy + r + 1, max(0, cx - r):cx + r + 1].reshape(-1, 4)
            if (b[:, 3] > 128).mean() < .5: continue
            b = b[b[:, 3] > 128]; med = np.median(b, 0); out[j, i] = (*b[np.argmin(((b - med) ** 2).sum(1))][:3], 255)
    return out

def best_grid(a, s0):
    wb = a.copy(); wb[..., :3] = np.where(a[..., 3:] > 128, a[..., :3], 255)
    s, ox, oy = grid_fit(wb[..., :3], s0)
    best = None
    for s_ in sorted({round(s, 2), s0}):
        for ox_ in np.arange(0, s_, .5):
            for oy_ in np.arange(0, s_, .5):
                o = rebuild(a, s_, ox_, oy_); k = int(s_)
                up = np.repeat(np.repeat(o, k, 0), k, 1); sub = a[int(oy_):int(oy_) + up.shape[0], int(ox_):int(ox_) + up.shape[1]]
                up = up[:sub.shape[0], :sub.shape[1]]; m = sub[..., 3] > 128
                if not m.any(): continue
                e = np.abs(up[..., :3] - sub[..., :3])[m].mean() + 40 * np.mean((up[..., 3] > 0) != m)
                if best is None or e < best[0]: best = (e, o)
    return best[1]

def palettize(o, maxd=20):
    m = o[..., 3] > 0; cnt = {}
    for c in map(tuple, o[m][:, :3]): cnt[c] = cnt.get(c, 0) + 1
    pal = []
    for c, _ in sorted(cnt.items(), key=lambda x: -x[1]):
        if not any(sum((p - q) ** 2 for p, q in zip(c, pp)) < maxd ** 2 for pp in pal): pal.append(c)
        if len(pal) >= 60: break
    P = np.array(pal); idx = np.argmin(((o[..., None, :3] - P[None, None]) ** 2).sum(-1), -1) + 1; idx[~m] = 0
    ys, xs = np.nonzero(idx); idx = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return idx, ['#%02x%02x%02x' % tuple(int(v) for v in c) for c in pal]

def extract_sheet(key):
    f, s0, lw = SHEETS[key]
    A = np.asarray(Image.open(IMG + f).convert('RGBA')).astype(int)
    m = A[..., 3] > 60; m[:, :lw] = False
    if key == 'g': m[:220] = False            # 見出し（ゴーストの 帯）を 外す
    bs = bands(m)
    if key == 'g':   # ゴーストは 数字と 絵が くっついているので 範囲を 決めうち
        bs = [(228, 532), (533, 590), (591, 918), (919, 980)]
    pairs = []   # (絵の 帯, 数字の 帯)
    i = 0
    while i < len(bs) - 1:
        if key == 'g' or (bs[i + 1][1] - bs[i + 1][0] < 40 and bs[i][1] - bs[i][0] >= 40): pairs.append((bs[i], bs[i + 1])); i += 2
        else: i += 1
    out = {}
    for row, (sb, db) in enumerate(pairs):
        # 数字の 位置 ＝ 各モンスターの まんなか
        dm = m[db[0]:db[1]]; cs = sorted([(p[:, 1].mean(), p) for p in comps(dm) if len(p) > 6], key=lambda t: t[0])
        centers = []
        for cx, p in cs:
            if centers and cx - centers[-1][-1] < 14: centers[-1].append(cx)
            else: centers.append([cx])
        centers = [np.mean(c) for c in centers]
        if key == 'g': centers = [160, 460, 765, 1063, 1375]
        sm = m[sb[0]:sb[1]]
        if key != 'g' and len(centers) != 10:   # 数字が うまく 読めない 段は 絵どうしの すき間で 分ける
            cl = []
            for p in sorted([p for p in comps(sm) if len(p) >= 4], key=lambda p: p[:, 1].min()):
                a0, a1 = p[:, 1].min(), p[:, 1].max()
                if cl and a0 <= cl[-1][1] + 2: cl[-1][1] = max(cl[-1][1], a1); cl[-1][2] += len(p)
                else: cl.append([a0, a1, len(p)])
            big = [c for c in cl if c[2] >= 80]
            centers = [(c[0] + c[1]) / 2 for c in big]
            print('row', row, 'gap clusters', len(centers), flush=True)
        groups = {k: [] for k in range(len(centers))}
        for p in comps(sm):
            if len(p) < 4: continue
            k = int(np.argmin([abs(p[:, 1].mean() - c) for c in centers])); groups[k].append(p)
        for k, ps in groups.items():
            if not ps: continue
            P = np.concatenate(ps); y0, x0 = P.min(0); y1, x1 = P.max(0)
            sub = np.zeros((y1 - y0 + 1 + 8, x1 - x0 + 1 + 8, 4), int)
            for pp in ps:
                for (yy, xx) in pp: sub[yy - y0 + 4, xx - x0 + 4] = A[sb[0] + yy, xx]
            o = best_grid(sub, s0); idx, pal = palettize(o)
            if key == 'g': nm = 'g%d' % (row * 5 + k + 1)
            else: nm = '%s_%s%d' % (key, TYPES[row], k + 1)
            out[nm] = {'w': int(idx.shape[1]), 'h': int(idx.shape[0]), 'pal': pal, 'd': rle(idx), '_idx': idx}
            print(nm, idx.shape, len(pal), flush=True)
    return out

def contact(data, name, cols=10, Z=4):
    items = list(data.items()); cw = max(v['w'] for _, v in items) * Z + 10; ch = max(v['h'] for _, v in items) * Z + 22
    rows = (len(items) + cols - 1) // cols; S = Image.new('RGB', (cw * cols, ch * rows), (236, 236, 242)); d = ImageDraw.Draw(S)
    for i, (k, v) in enumerate(items):
        idx = v['_idx']; im = Image.new('RGB', (v['w'], v['h']), (236, 236, 242))
        for y in range(v['h']):
            for x in range(v['w']):
                if idx[y, x]: im.putpixel((x, y), tuple(int(v['pal'][idx[y, x] - 1][j:j + 2], 16) for j in (1, 3, 5)))
        im = im.resize((v['w'] * Z, v['h'] * Z), Image.NEAREST); X, Yy = (i % cols) * cw, (i // cols) * ch
        S.paste(im, (X + 5, Yy + ch - 18 - im.height)); d.text((X + 5, Yy + ch - 15), k, fill=(20, 20, 60))
    S.save(name)

if __name__ == '__main__':
    allv = {}
    for key in (sys.argv[1:] or SHEETS):
        d = extract_sheet(key); allv.update(d); contact(d, 'sheet_%s.png' % key)
    import os
    old = json.load(open('all.json')) if os.path.exists('all.json') else {}
    old.update({k: {kk: vv for kk, vv in v.items() if kk != '_idx'} for k, v in allv.items()})
    json.dump(old, open('all.json', 'w'))
