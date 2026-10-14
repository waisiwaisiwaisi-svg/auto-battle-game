# 透過スプライトシート → 1体6コマ（走り4・ため・攻撃）のドット絵に もどす
# usage: proc3.py  (sheets/No.XX.png と req/batches.json を よむ → out/<id>.npz, out/report.json)
import json, sys, numpy as np
from PIL import Image
from scipy import ndimage
D = '/tmp/claude-0/-home-user-auto-battle-game/27abe3ed-76ac-5b94-8383-de41dcf56044/scratchpad/anim/'
import os
BF, PRE, OUTD = os.environ.get('BATCHES', 'req/batches.json'), os.environ.get('PREFIX', 'No.'), os.environ.get('OUTD', 'out')
B = json.load(open(D + BF))
only = set(sys.argv[1:])
def cuts(prof, k):
    """prof を k 個に わける 切れ目（いちばん ひろい すきま から）"""
    n = len(prof); thr = prof.max() * 0.002
    z = prof <= thr; runs = []; s = None
    for i, v in enumerate(z):
        if v and s is None: s = i
        if not v and s is not None: runs.append((s, i)); s = None
    if s is not None: runs.append((s, n))
    nz = np.where(~z)[0]; lo, hi = nz.min(), nz.max()
    inner = [r for r in runs if r[0] > lo and r[1] <= hi]
    inner.sort(key=lambda r: r[1] - r[0], reverse=True)
    cs = sorted((a + b) // 2 for a, b in inner[:k - 1])
    if len(cs) < k - 1:   # すきまが たりない：ちょうど 等分の あたりの 谷で きる
        sm = ndimage.uniform_filter1d(prof.astype(float), 9)
        for j in range(1, k):
            t = lo + (hi - lo) * j // k
            if any(abs(t - c) < (hi - lo) / k / 2 for c in cs): continue
            w = int((hi - lo) / k / 3); cs.append(t - w + int(np.argmin(sm[t - w:t + w])))
        cs = sorted(cs)
    edges = [lo] + cs + [hi + 1]
    return [(edges[i], edges[i + 1]) for i in range(k)]
def fitp(sig, lo=3.5, hi=16):
    # もとの絵の 大きさから 見こんだ はんいの 中で、いちばん つよい 周期
    ps = np.arange(max(3, lo), hi, 0.01); n = np.arange(len(sig))
    amp = np.array([abs((sig * np.exp(2j * np.pi * n / p)).sum()) for p in ps])
    return ps[amp.argmax()]
import base64, io
_d = json.load(open(D + '../sizes/mons.json')); _d = _d if isinstance(_d, list) else _d.get('mons', _d); _d = _d if isinstance(_d, list) else list(_d.values())
OSZ = {m['id']: Image.open(io.BytesIO(base64.b64decode(m['img'].split(',')[1]))).size for m in _d}
def phase(sig, p):
    n = np.arange(len(sig)); return (-np.angle((sig * np.exp(2j * np.pi * n / p)).sum()) / (2 * np.pi) * p) % p
report = {}
for bi, ids in enumerate(B):
    no = f'{bi + 1:02d}' if PRE == 'No.' else str(bi + 1)
    if only and no not in only: continue
    im = np.array(Image.open(D + f'sheets/{PRE}{no}.png').convert('RGBA')).astype(float)
    a = im[..., 3]; fg = a >= 128
    rgbp = im[..., :3] * (a[..., None] / 255)
    gx = np.abs(np.diff(np.concatenate([rgbp, a[..., None]], 2), axis=1)).sum((0, 2)); gy = np.abs(np.diff(np.concatenate([rgbp, a[..., None]], 2), axis=0)).sum((1, 2))
    two = len(ids) <= 2
    nrows = 2 * len(ids) if two else len(ids)
    rows = cuts(fg.sum(1), nrows)
    cells = {}   # id -> [6 cell boxes]
    for ri, (y0, y1) in enumerate(rows):
        k = (4 if ri % 2 == 0 else 2) if two else 6
        cs = cuts(fg[y0:y1].sum(0), k)
        sid = ids[ri // 2] if two else ids[ri]
        cells.setdefault(sid, []).extend((y0, y1, x0, x1) for x0, x1 in cs)
    PX = {}
    for sid, boxes in cells.items():
        # 1ドットの 大きさ ＝ 走りコマの 高さ ÷ もとの絵の 高さ（正方形の ドット）。その ちかくで いちばん つよい 周期に あわせる
        hs = []
        for (y0, y1, x0, x1) in boxes[:4]:
            yy, xx = np.where(fg[y0:y1, x0:x1]); hs.append(yy.max() - yy.min() + 1)
        e = float(np.median(hs)) / OSZ[sid][1]
        sigs = []
        for (y0, y1, x0, x1) in boxes:
            c = im[y0:y1, x0:x1]; cc = np.concatenate([c[..., :3] * (c[..., 3:] / 255), c[..., 3:]], 2)
            sigs.append(np.abs(np.diff(cc, axis=1)).sum((0, 2))); sigs.append(np.abs(np.diff(cc, axis=0)).sum((1, 2)))
        ps = np.arange(e * .9, e * 1.1, 0.01)
        amp = [sum(abs((g * np.exp(2j * np.pi * np.arange(len(g)) / p)).sum()) / (np.abs(g).sum() + 1) for g in sigs) for p in ps]
        PX[sid] = float(ps[int(np.argmax(amp))])
    for sid, boxes in cells.items():
        frames = []
        for (y0, y1, x0, x1) in boxes:
            c = im[y0:y1, x0:x1]; m = fg[y0:y1, x0:x1].copy()
            # となりの コマの はみだし を けす：コマの ふちに かかった 小さい かたまり だけ のぞく
            # （体から はなれて うかぶ 鬼火・泡・火花 などは のこす）
            lab, nl = ndimage.label(ndimage.binary_dilation(m, iterations=int(PX[sid])))
            if nl > 1:
                sizes = ndimage.sum(m, lab, range(1, nl + 1)); keep = 1 + int(np.argmax(sizes))
                edge = set(np.unique(np.concatenate([lab[:, 0], lab[:, -1], lab[0, :], lab[-1, :]]))) - {0}
                drop = [k for k in range(1, nl + 1) if k != keep and k in edge]
                if drop: m &= ~np.isin(lab, drop)
            cc = np.concatenate([c[..., :3] * (c[..., 3:] / 255), c[..., 3:]], 2)
            px = py = PX[sid]
            ox = phase(np.abs(np.diff(cc, axis=1)).sum((0, 2)), px); oy = phase(np.abs(np.diff(cc, axis=0)).sum((1, 2)), py)
            xs = np.arange(ox + .5 + px / 2 - px, c.shape[1], px); ys = np.arange(oy + .5 + py / 2 - py, c.shape[0], py)
            xs = xs[xs >= 0]; ys = ys[ys >= 0]
            g = np.zeros((len(ys), len(xs), 4), np.uint8)
            for j, y in enumerate(ys):
                for i, x in enumerate(xs):
                    ya, yb, xa, xb = int(y - py * .3), int(y + py * .3) + 1, int(x - px * .3), int(x + px * .3) + 1
                    mb = m[max(0, ya):yb, max(0, xa):xb]
                    if mb.size == 0 or mb.mean() < .5: continue
                    blk = c[max(0, ya):yb, max(0, xa):xb][mb]
                    g[j, i, :3] = np.median(blk[:, :3], 0); g[j, i, 3] = 255
            yy, xx = np.where(g[..., 3] > 0); g = g[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
            frames.append(g)
        allpx = np.concatenate([f[f[..., 3] == 255][:, :3] for f in frames])
        pal = np.array(Image.fromarray(allpx[None]).quantize(32, method=Image.Quantize.MEDIANCUT).getpalette()[:96], float).reshape(-1, 3)
        out = []
        for g in frames:
            q = g.copy(); al = g[..., 3] > 0
            d = ((g[..., :3][..., None, :].astype(float) - pal) ** 2).sum(-1); q[..., :3] = pal[d.argmin(-1)]; q[~al] = 0
            out.append(q)
        np.savez_compressed(D + f'{OUTD}/{sid}.npz', *out)
        report[sid] = dict(no=no, px=round(PX[sid], 2), sizes=[list(f.shape[:2]) for f in out], orig=OSZ[sid])
    print(no, [(s, report[s]['px'], report[s]['sizes'][0], OSZ[s]) for s in ids], flush=True)
old = {}
try: old = json.load(open(D + OUTD + '/report.json'))
except Exception: pass
old.update(report); json.dump(old, open(D + OUTD + '/report.json', 'w'), ensure_ascii=False)
