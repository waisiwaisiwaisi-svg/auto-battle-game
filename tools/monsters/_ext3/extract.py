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
# 番号の 行（各段の 見出しの 下はし付近）と 列の まんなか
NUM = [(lb - 3, lb + 11) for lt, lb in ROWS]
nb = m[ROWS[0][1] - 2:ROWS[0][1] + 10]
ncs = sorted(p[:, 1].mean() for p in comps(nb) if len(p) >= 8); CEN = []
for c in ncs:
    if CEN and c - CEN[-1][-1] < 14: CEN[-1].append(c)
    else: CEN.append([c])
CEN = np.array([np.mean(c) for c in CEN]); assert len(CEN) == 10
mm = m.copy()
mm[:, :54] = False   # 左の タイプ見出し（光の にじみ を ふくめ x 50 まで）
for q in comps(m[:, :70]):
    if q[:, 1].min() <= 2:
        for yy, xx in q: mm[yy, xx] = False
# 番号の 文字を 消す：各段の 番号の 行で、列の まんなか ±9 の 白っぽい／灰色の ドット
# （白い 体が 番号の 行まで のびている モンスターは のぞく）
KEEP_WHITE = {(9, 1)}   # ホネリュウ（ドラゴン2）
rgb = A[..., :3]; sat = rgb.max(-1) - rgb.min(-1)
for r, (lt, lb) in enumerate(ROWS):
    for k, c in enumerate(CEN):
        if (r, k) in KEEP_WHITE:
            y0_, y1_ = lb + 4, lb + 15   # 数字の 下半分だけ（足と かさならない ところ）
        else:
            y0_, y1_ = lb - 3, lb + 15
        x0_, x1_ = int(c - 9), int(c + 10)
        box = mm[y0_:y1_, x0_:x1_]; box[sat[y0_:y1_, x0_:x1_] < 40] = False
allc = [p for p in comps(mm) if len(p) >= 4 and (p[:, 1] < 47).mean() < .5]   # 左の 見出しの アイコンは のぞく
def is_num(p):   # 番号の 文字：小さくて 番号の 行に おさまる
    y0, y1 = p[:, 0].min(), p[:, 0].max()
    return len(p) < 170 and any(a <= y0 and y1 <= b for a, b in NUM) and (y1 - y0) <= 13
cells = {}
for p in allc:
    if is_num(p): continue
    row = np.searchsorted(np.array([b for a, b in NUM]), p[:, 0] + 0)   # 番号の 行より 上なら その段
    row = np.clip(row, 0, 9)
    col = np.argmin(np.abs(p[:, 1:2] - CEN[None]), 1)
    cell = row * 10 + col
    us, cn = np.unique(cell, return_counts=True)
    own = us[cn >= cn.max() * .3]   # いちばん 多い 列の 3割 以上 ある 列が もちぬし
    if len(own) <= 1: cells.setdefault(int(us[np.argmax(cn)]), []).append(p); continue
    # くっついた 2体以上：それぞれの 体の まんなかから 同時に 広げて 分ける（黒い 輪郭は 越えにくい）
    import heapq
    orow, ocol = own // 10, own % 10
    pos = {(int(y), int(x)): i for i, (y, x) in enumerate(p)}
    lum = A[p[:, 0], p[:, 1], :3].mean(-1)
    dist = np.full(len(p), 1e9); lab = np.full(len(p), -1); hq = []
    for j, o in enumerate(own):
        sel = np.nonzero(cell == o)[0]
        # 種：その マスの 中で 列の まんなかに 近い ドット
        cx = CEN[ocol[j]]; d0 = np.abs(p[sel, 1] - cx); seeds = sel[d0 <= np.percentile(d0, 15)]
        for i in seeds: dist[i] = 0; lab[i] = j; heapq.heappush(hq, (0., i, j))
    while hq:
        dd, i, j = heapq.heappop(hq)
        if dd > dist[i] or lab[i] != j: continue
        y, x = p[i]
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            n = pos.get((y + dy, x + dx))
            if n is None: continue
            c = (1.4 if dy and dx else 1.) * (1 + 6 * (lum[n] < 70))
            if dd + c < dist[n]: dist[n] = dd + c; lab[n] = j; heapq.heappush(hq, (dd + c, n, j))
    for j, o in enumerate(own): cells.setdefault(int(o), []).append(p[lab == j])
# ホネリュウ（ドラゴン2）の 白い 翼が となりの ニチリンリュウ（ドラゴン3）に 入りこんでいるので、白っぽい ドットと その 輪郭を もどす
if 91 in cells and 92 in cells:
    q3 = np.concatenate(cells[92]); rgb_ = A[q3[:, 0], q3[:, 1], :3]
    sat_ = rgb_.max(1) - rgb_.min(1); lum_ = rgb_.mean(1)
    bone = (sat_ < 55) & (lum_ > 95)
    bset = {(int(y), int(x)) for y, x in q3[bone]}
    near = np.array([any((y + dy, x + dx) in bset for dy in (-1, 0, 1) for dx in (-1, 0, 1)) and s_ < 55 for (y, x), s_ in zip(q3, sat_)])
    mv = (bone | near) & (q3[:, 1] < CEN[2] - 22)   # ニチリンリュウの 体より 左だけ
    q2 = np.concatenate(cells[91]); r2 = A[q2[:, 0], q2[:, 1], :3]
    red = (r2[:, 0] - r2[:, 2] > 40) & (r2.max(1) - r2.min(1) > 50)   # 翼に まじった 赤い かけらは ニチリンリュウへ
    cells[91] = [q2[~red]]; cells[92] = [np.concatenate([q3, q2[red]])]; q3 = cells[92][0]
    rgb_ = A[q3[:, 0], q3[:, 1], :3]; sat_ = rgb_.max(1) - rgb_.min(1); lum_ = rgb_.mean(1)
    bone = (sat_ < 55) & (lum_ > 95); bset = {(int(y), int(x)) for y, x in q3[bone]}
    near = np.array([any((y + dy, x + dx) in bset for dy in (-1, 0, 1) for dx in (-1, 0, 1)) and s_ < 55 for (y, x), s_ in zip(q3, sat_)])
    notred = (rgb_[:, 0] - rgb_[:, 2] < 70) | (sat_ < 70)
    mv = ((bone | near) | notred) & (q3[:, 1] < CEN[2] - 14)
    cells[91].append(q3[mv]); cells[92] = [q3[~mv]]
    q2 = np.concatenate(cells[91]); r2 = A[q2[:, 0], q2[:, 1], :3]
    tint = (r2[:, 0] - r2[:, 2] > 45) & (r2[:, 0] > 1.8 * r2[:, 1] + 10) & (q2[:, 1] > 132)   # 右はしに まざった 赤っぽい ドットは ニチリンリュウへ
    cells[91] = [q2[~tint]]; cells[92].append(q2[tint])
    q2 = cells[91][0]; keep = np.zeros(len(q2), bool); B = np.zeros(A.shape[:2], bool); B[q2[:, 0], q2[:, 1]] = True
    big = max(comps(B[:, :200]), key=len); bs = {(int(y), int(x)) for y, x in big}
    keep = np.array([(int(y), int(x)) in bs for y, x in q2]); cells[91] = [q2[keep]]   # 本体と つながらない かけらを 消す
for r, t in enumerate(TYPES):
    groups = {k: [] for k in range(10)}
    y0 = 0
    for k in range(10):
        ps = cells.get(r * 10 + k, [])
        if not ps: continue
        big = max(len(q) for q in ps)
        mainq = max(ps, key=len); bot = mainq[:, 0].max()
        groups[k] = [q for q in ps if len(q) >= max(6, big * .015) and not (len(q) < big * .06 and q[:, 0].min() > bot - 4)]   # 下に はなれた 小さな かけらは 消す
    for k, ps in groups.items():
        if not ps: print('missing', t, k + 1); continue
        P = np.concatenate(ps); ya, xa = P.min(0); yb, xb = P.max(0)
        sub = np.zeros((yb - ya + 1, xb - xa + 1, 4), int)
        for pp in ps:
            for yy, xx in pp: sub[yy - ya, xx - xa] = A[yy, xx]
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
