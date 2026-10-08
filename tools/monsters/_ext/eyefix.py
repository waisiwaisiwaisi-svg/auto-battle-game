# 目が 黒1ドットだけの モンスターを 見つけて「白い ハイライト＋黒い ひとみ」の 2色に する
# build_meta.py から 呼ばれる（all.json の 元データは 書きかえない）
import numpy as np
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'

def decode(v):
    flat = []; d = v['d']
    for i in range(0, len(d), 3): flat += [AL.index(d[i])] * int(d[i + 1:i + 3], 36)
    return np.array(flat[:v['w'] * v['h']]).reshape(v['h'], v['w'])

def encode(idx):
    flat = idx.ravel(); s = ''; i = 0
    while i < len(flat):
        j = i
        while j < len(flat) and flat[j] == flat[i] and j - i < 1295: j += 1
        s += AL[flat[i]] + np.base_repr(j - i, 36).lower().rjust(2, '0'); i = j
    return s

def lum(c): return .3 * int(c[1:3], 16) + .59 * int(c[3:5], 16) + .11 * int(c[5:7], 16)

def find_eyes(v):
    """目：とても 暗い 色の 小さな かたまり（1〜6ドット、上 6割）で、まわりが ほぼ 明るい 体の 色。
    中や すぐ となりに 白っぽい ハイライトが もう ある 目は のぞく。かえすのは かたまりごとの ドットの リスト"""
    idx = decode(v); H, W = idx.shape; L = [0] + [lum(c) for c in v['pal']]
    dk = (idx > 0) & (np.array(L)[idx] < 50)
    seen = np.zeros_like(dk); out = []
    for y0 in range(H):
        for x0 in range(W):
            if not dk[y0, x0] or seen[y0, x0]: continue
            q = [(y0, x0)]; seen[y0, x0] = True; pts = []
            while q:
                y, x = q.pop(); pts.append((x, y))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and dk[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
            if not (1 <= len(pts) <= 6) or max(p[1] for p in pts) > H * .62: continue
            ps = set(pts); ring = set()
            for x, y in pts:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        r = (x + dx, y + dy)
                        if r not in ps: ring.add(r)
            vals = [idx[y, x] if 0 <= y < H and 0 <= x < W else 0 for x, y in ring]
            light = [c for c in vals if c and L[c] >= 75]
            if len(light) < len(vals) * .7: continue                  # 輪郭の 一部などは のぞく
            if any(L[c] > 200 for c in light): continue               # もう ハイライトが ある
            if sum(L[c] for c in light) / len(light) < 95: continue   # 暗い 体の 上の 点は 目と みなさない
            out.append(sorted(pts, key=lambda p: (p[1], p[0])))
    return idx, out

def fix(v):
    """目の かたまりの 左上の ドットを 白に（1ドットの 目は 上の ドットを 白に して 2ドットに）"""
    idx, eyes = find_eyes(v)
    if not eyes: return v, 0
    pal = list(v['pal'])
    if '#ffffff' not in pal: pal.append('#ffffff')
    white = pal.index('#ffffff') + 1
    for pts in eyes:
        if len(pts) == 1: x, y = pts[0]; idx[y - 1, x] = white
        else: x, y = pts[0]; idx[y, x] = white
    return {**v, 'pal': pal, 'd': encode(idx)}, len(eyes)
