# 第3弾シート（10タイプ × 10体、透過）を 1体ずつ 切りだす → all.json と 確認用 sheet.png
import json, sys, numpy as np
from collections import deque
from PIL import Image, ImageDraw
sys.path.insert(0, '../_ext')
from extract import rle
A = np.asarray(Image.open('sheet.webp').convert('RGBA')).astype(int)
H, W, _ = A.shape
m = A[..., 3] > 60; m[:, :48] = False
TYPES = ['fire', 'water', 'grass', 'elec', 'ice', 'fighting', 'poison', 'ground', 'wind', 'dragon']
ROWS = [(13, 76), (88, 154), (171, 238), (255, 323), (341, 408), (428, 494), (515, 581), (599, 664), (679, 745), (757, 823)]   # 左の 見出しの 位置
X0, PX = 44, 51.4
def comps(mask):
    h, w = mask.shape; lab = np.zeros((h, w), int); out = []; n = 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
                out.append(np.array(pts))
    return out
out = {}
prev_end = 0
for r, t in enumerate(TYPES):
    lt, lb = ROWS[r]
    # 番号の 文字（見出しの 下はしの すぐ 下）から 各モンスターの まんなかを 知る
    nb = m[lb - 2:lb + 10]
    ncs = sorted(p[:, 1].mean() for p in comps(nb) if len(p) >= 8)
    cen = []
    for c in ncs:
        if cen and c - cen[-1][-1] < 14: cen[-1].append(c)
        else: cen.append([c])
    cen = [np.mean(c) for c in cen]
    if len(cen) != 10: cen = CEN0   # 番号が うまく 読めない 段は 1段目の 位置を つかう（同じ 格子に ならんでいる）
    if r == 0: CEN0 = cen; print('centers', [round(c) for c in cen])
    edges = [0] + [(cen[k] + cen[k + 1]) / 2 for k in range(9)] + [W]
    y0 = max(prev_end, lt - 14); y1 = lb - 3; prev_end = lb + 10
    groups = {k: [] for k in range(10)}
    for k in range(10):
        x0, x1 = int(edges[k]), int(edges[k + 1])
        tile = m[y0:y1, x0:x1].copy(); tile[:, :max(0, 53 - x0)] = False
        cs = [p for p in comps(tile) if len(p) >= 4]
        if not cs: continue
        big = max(len(p) for p in cs); tw = x1 - x0
        for p in cs:
            edge = p[:, 1].min() == 0 or p[:, 1].max() == tw - 1
            if edge and len(p) < big * .3 and len(p) != big: continue   # となりから はみ出した 切れはし
            if len(p) < big * .02: continue
            if p[:, 0].min() == 0 and len(p) < big * .12: continue   # 上の 段の 番号の かけら
            if edge and len(p) < big * .45 and abs(p[:, 1].mean() - (cen[k] - x0)) > tw * .38: continue   # 列の はしに よった はみ出し
            groups[k].append(p + [0, x0])
    for k, ps in groups.items():
        if not ps: print('missing', t, k + 1); continue
        P = np.concatenate(ps); ya, xa = P.min(0); yb, xb = P.max(0)
        sub = np.zeros((yb - ya + 1, xb - xa + 1, 4), int)
        for pp in ps:
            for yy, xx in pp: sub[yy - ya, xx - xa] = A[y0 + yy, xx]
        # 半透明の ふちは 消す／色を まとめる
        on = sub[..., 3] > 110
        rgb = Image.fromarray(sub[..., :3].astype(np.uint8)).quantize(48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pal = rgb.getpalette()[:48 * 3]; idx = np.asarray(rgb).astype(int) + 1; idx[~on] = 0
        used = sorted(set(idx[idx > 0].ravel())); rm = {u: i + 1 for i, u in enumerate(used)}
        idx = np.vectorize(lambda v: rm.get(v, 0))(idx)
        ys, xs = np.nonzero(idx); idx = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        nm = 'c_%s%d' % (t, k + 1)
        out[nm] = {'w': int(idx.shape[1]), 'h': int(idx.shape[0]), 'pal': ['#%02x%02x%02x' % tuple(pal[(u - 1) * 3:(u - 1) * 3 + 3]) for u in used], 'd': rle(idx)}
json.dump(out, open('all.json', 'w')); print(len(out))
# 確認
Z = 3; S = Image.new('RGB', (10 * 60 * Z, 10 * 80 * Z), (230, 230, 238)); d = ImageDraw.Draw(S)
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
for i, (k, v) in enumerate(out.items()):
    flat = []; dd = v['d']
    for j in range(0, len(dd), 3): flat += [AL.index(dd[j])] * int(dd[j + 1:j + 3], 36)
    im = Image.new('RGBA', (v['w'], v['h']))
    pal = [tuple(int(c[q:q + 2], 16) for q in (1, 3, 5)) for c in v['pal']]
    for n, c in enumerate(flat):
        if c: im.putpixel((n % v['w'], n // v['w']), pal[c - 1] + (255,))
    im = im.resize((v['w'] * Z, v['h'] * Z), Image.NEAREST)
    r_, c_ = divmod(TYPES.index(k[2:].rstrip('0123456789')), 1)[0], int(k[2 + len(k[2:].rstrip('0123456789')):]) - 1
    S.paste(im, (c_ * 60 * Z, r_ * 80 * Z), im); d.text((c_ * 60 * Z, r_ * 80 * Z + 72 * Z), k, fill=(0, 0, 0))
S.save('check.png')
