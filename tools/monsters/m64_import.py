# ChatGPT に 64×64 で 描き直して もらった モンスターの シート（monsters64/Mxx_k.png）を ゲームの AISpr.ANIM（full）に する
#   1まい＝1たい、横6×たて2 の 12コマ（1マス 256px・1ドット 4px）
#   上：たいき4・ため・攻撃 ／ 下：走り4・ダメージ・たおれる
# usage: python3 tools/monsters/m64_import.py <シートの フォルダ> <mons.json（依頼シートの じゅんばん）> <out.json>
import sys, os, json, glob, re
import numpy as np
from PIL import Image
from scipy import ndimage
SRC, MONS, OUT = sys.argv[1:4]
L = json.load(open(MONS))
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
P = 4


def rle(idx):
    f = idx.ravel(); s = []; i = 0
    while i < len(f):
        j = i
        while j < len(f) and f[j] == f[i] and j - i < 1295: j += 1
        s.append(AL[f[i]] + np.base_repr(j - i, 36).lower().rjust(2, '0')); i = j
    return ''.join(s)


def phase(a):   # ドットの さかいめ（0〜3 ずれ）：ブロックの 中が いちばん そろう ずれ
    op = a[..., 3] > 128; best = None
    for oy in range(P):
        for ox in range(P):
            b = a[oy:oy + (a.shape[0] - oy) // P * P, ox:ox + (a.shape[1] - ox) // P * P, :3].astype(int)
            h, w = b.shape[0] // P, b.shape[1] // P
            v = b.reshape(h, P, w, P, 3).std(axis=(1, 3)).sum()
            if best is None or v < best[0]: best = (v, oy, ox)
    return best[1:]


def reduce(a, oy, ox):
    b = a[oy:oy + (a.shape[0] - oy) // P * P, ox:ox + (a.shape[1] - ox) // P * P]
    h, w = b.shape[0] // P, b.shape[1] // P
    blk = b.reshape(h, P, w, P, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, P * P, 4)
    out = np.zeros((h, w, 4), np.uint8)
    al = blk[..., 3] > 128
    out[..., 3] = np.where(al.sum(-1) > P * P // 2, 255, 0)
    c = blk[:, :, P + 1, :3]; c2 = blk[:, :, 2 * P + 2, :3]   # まんなか ふきんの 画素（ふちの にじみを さける）
    out[..., :3] = np.where((blk[:, :, P + 1, 3] > 128)[..., None], c, c2)
    return out


out = {}
for f in sorted(glob.glob(os.path.join(SRC, 'M*_*.png'))):
    m = re.match(r'M(\d+)_(\d)\.png', os.path.basename(f)); card, k = int(m.group(1)), int(m.group(2))
    sid = L[(card - 1) * 2 + (k - 1)]['id']
    a = np.array(Image.open(f).convert('RGBA'))
    H, W = a.shape[:2]; cw, ch = W // 6, H // 2
    oy, ox = phase(a[:ch, :cw])
    g = reduce(a, oy, ox); gh, gw = g.shape[:2]; CW, CH = cw // P, ch // P   # ドットの マス目（1コマ＝64×64）
    # はみ出した 絵：マス目で きらず、つながった かたまりごとに「まんなかが ある コマ」に いれる（となりの コマの きれはしは のぞく）
    lab, nl = ndimage.label(g[..., 3] > 0, structure=np.ones((3, 3)))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, nl + 1)); cms = ndimage.center_of_mass(np.ones_like(lab), lab, range(1, nl + 1))
    owner = {}
    for n, ((cy, cx), sz) in enumerate(zip(cms, sizes), 1):
        r, c = min(1, int(cy // CH)), min(5, int(cx // CW)); owner[n] = (r * 6 + c, sz)
    # 小さい かたまりは「いちばん ちかい コマの 本体」に つける（となりの コマの しっぽ・つの などが まぎれこまない ように）
    main = {}
    for n, (k2, sz) in owner.items():
        if k2 not in main or sz > owner[main[k2]][1]: main[k2] = n
    dist = {k2: ndimage.distance_transform_edt(lab != n) for k2, n in main.items()}
    for n, (k2, sz) in list(owner.items()):
        if main.get(k2) == n: continue
        m = lab == n; ys, xs = np.where(m)
        edge = min(np.abs(((xs + CW / 2) % CW) - CW / 2).min(), np.abs(ys - CH).min())   # コマの さかいめまでの きょり
        if edge <= 6: owner[n] = (-1, sz); continue   # さかいめ ちかくの はなれた かけら＝となりの コマから はみ出した きれはし → すてる
        best = min(dist, key=lambda kk: dist[kk][m].min()); dd = dist[best][m].min()
        owner[n] = (best if dd <= 14 else -1, sz)
    biggest = {k2: owner[n][1] for k2, n in main.items()}
    fr = []; M = 16   # となりへ はみ出して よい はば（ドット）
    for k2 in range(12):
        r, c = divmod(k2, 6); y0, x0 = r * CH - M, c * CW - M
        cell = np.zeros((CH + 2 * M, CW + 2 * M, 4), np.uint8)
        keep = [n for n, (kk, sz) in owner.items() if kk == k2 and sz >= 2]
        mask = np.isin(lab, keep)
        ys, xs = np.where(mask)
        for yy, xx in zip(ys, xs):
            ty, tx = yy - y0, xx - x0
            if 0 <= ty < cell.shape[0] and 0 <= tx < cell.shape[1]: cell[ty, tx] = g[yy, xx]
        fr.append(cell)
    # 12コマ ぜんぶ おなじ わくで きる（コマどうしの いちを たもつ）
    al = np.any([x[..., 3] > 0 for x in fr], axis=0); yy, xx = np.where(al)
    y0, y1, x0, x1 = yy.min(), yy.max() + 1, xx.min(), xx.max() + 1
    fr = [x[y0:y1, x0:x1] for x in fr]
    strip = np.concatenate(fr, axis=1)
    q = Image.fromarray(strip[..., :3]).quantize(63, method=Image.Quantize.MEDIANCUT, dither=0)
    pal = q.getpalette()[:63 * 3]; qi = np.array(q) + 1; qi[strip[..., 3] == 0] = 0
    used = sorted(set(qi.ravel()) - {0}); remap = {o: n + 1 for n, o in enumerate(used)}
    qi = np.vectorize(lambda v: remap.get(v, 0))(qi)
    palhex = ['#%02x%02x%02x' % tuple(pal[(o - 1) * 3:(o - 1) * 3 + 3]) for o in used]
    w = x1 - x0; F = []
    for i in range(12):
        F.append(dict(w=int(w), h=int(y1 - y0), x=0, d=rle(qi[:, i * w:(i + 1) * w])))
    out[sid] = dict(pal=palhex, f=F, full=1)
    print(sid, L[(card - 1) * 2 + (k - 1)]['n'], w, y1 - y0, len(palhex))
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
print(len(out), os.path.getsize(OUT) // 1024, 'KB')
