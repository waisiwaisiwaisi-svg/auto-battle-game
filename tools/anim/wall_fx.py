# W1（わざの かべ・1まいもの）を きる：6れつ（よこ きれい・よこ ヒビ・たて きれい・たて ヒビ・ななめ きれい・ななめ ヒビ）× 4だん（いわ・こおり・いばら・はんしゃ）
# コマごとに 絵の はんいが ちがうので、コマごとに きりだして 下ぞろえ・まんなかぞろえ で 同じ 大きさの わくに いれる。fb＝コマごとの 絵の はんい
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'gpt_fx')
P = 4   # 1ドット＝4ピクセル（たのんだ 大きさ）
ROWS = ['wl_rock', 'wl_ice', 'wl_thorn', 'wl_mirror']

def reduce_soft(c, P):
    h, w = -(-c.shape[0] // P), -(-c.shape[1] // P); pad = np.zeros((h * P, w * P, 4), np.uint8); pad[:c.shape[0], :c.shape[1]] = c
    b = pad.reshape(h, P, w, P, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, P * P, 4).astype(np.float32); al = b[..., 3]; ma = al.mean(-1); out = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            if ma[y, x] < 60: continue
            m = al[y, x] > 100
            if not m.any(): m = al[y, x] > 0
            out[y, x, :3] = np.median(b[y, x][m][:, :3], 0); out[y, x, 3] = 255 if ma[y, x] > 170 else 200
    return out

a = np.array(Image.open(f'{D}/src/W1.png').convert('RGBA')); H, W = a.shape[:2]
op = a[:, :, 3] > 40
# マスは 等分（256×256）
meta = json.load(open(f'{D}/meta.json'))
for r, key in enumerate(ROWS):
    frs = []
    for c in range(6):
        cell = a[H * r // 4:H * (r + 1) // 4, W * c // 6:W * (c + 1) // 6]; p_ = np.argwhere(cell[:, :, 3] > 40)
        cl = cell.copy(); lab, nl = ndimage.label(cl[:, :, 3] > 40); sz = ndimage.sum(np.ones_like(lab), lab, range(1, nl + 1)); big = sz.max()
        for k in range(nl):
            if sz[k] < big * .04: cl[lab == k + 1] = 0   # となりの マスの はみだし・ちいさな ごみを けす
        p_ = np.argwhere(cl[:, :, 3] > 40); crop = cl[p_[:, 0].min():p_[:, 0].max() + 1, p_[:, 1].min():p_[:, 1].max() + 1]; frs.append(reduce_soft(crop, P))
    fw = max(f.shape[1] for f in frs); fh = max(f.shape[0] for f in frs); strip = np.zeros((fh, fw * 6, 4), np.uint8); fb = []
    for i, f in enumerate(frs):
        ox = i * fw + (fw - f.shape[1]) // 2; oy = fh - f.shape[0]; strip[oy:, ox:ox + f.shape[1]] = f; fb.append([ox - i * fw, oy, ox - i * fw + f.shape[1], fh])
    im = Image.fromarray(strip, 'RGBA'); q = im.convert('RGB').quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(im.getchannel('A')); q.save(f'{D}/{key}.png')
    meta[key] = {'n': 6, 'w': fw, 'h': fh, 'ms': 100, 'loop': False, 'var': True, 'ax': fw / 2, 'ay': fh - 1, 'fb': fb}
    print(key, fw, fh, fb)
json.dump(meta, open(f'{D}/meta.json', 'w'), indent=1)
