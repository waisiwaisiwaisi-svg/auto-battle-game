# まんなかの 障害物を 絵から けす（くさの とうぎじょう：まんなかの 木）
#   木の ある まるい ところを、まわりの しばふ と 十字の みち を のばして ぬりつぶす
#   使い方: python3 tools/arenas/clear_center.py → src/grass.webp を かきかえ（もとは src/grass_orig.webp）
import os
from PIL import Image
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(HERE, 'src', 'grass_orig.webp')).convert('RGB')
a = np.asarray(src).astype(np.int16).copy(); H, W = a.shape[:2]
cx, cy, rx, ry = 728, 530, 162, 158        # まるい 植えこみ（木と ランプを ふくむ）
VB = (697, 754)                             # たての みち の はば（x）
HB = (502, 553)                             # よこの みち の はば（y）
ys, xs = np.mgrid[0:H, 0:W]
mask = ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2 <= 1
out = a.copy()
SH = 2 * rx + 12                            # よこに ずらして もってくる きょり
GP, GW, GH = (445, 580), 130, 75               # なにも ない しばふ（お手本）
PV = 50                                     # みちの もようの くりかえし
for y, x in zip(*np.nonzero(mask)):
    inV, inH = VB[0] <= x < VB[1], HB[0] <= y < HB[1]
    if inV and not inH:   # たての みち：すぐ うえ（した）の みちを くりかえす
        top, bot = int(cy - ry) - 4, int(cy + ry) + 4
        sy = top - PV + ((y - top) % PV) if y < cy else bot + ((y - bot) % PV)
        out[y, x] = a[sy, x]
    elif inH:             # よこの みち・こうさてん：ひだり（か みぎ）から
        sx = x - SH if x < cx else x + SH; out[y, x] = a[y, sx]
    else:                 # しばふ：きれいな しばふを かがみ うつしで しきつめる
        px, py = (x - GP[0]) % (2 * GW), (y - GP[1]) % (2 * GH)
        px = px if px < GW else 2 * GW - 1 - px; py = py if py < GH else 2 * GH - 1 - py
        out[y, x] = a[GP[1] + py, GP[0] + px]
# いろあわせ：まわりの わ と ぬった ところの ふちの へいきんを そろえる（しばふ だけ）
e = ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2
ring = (e > 1.0) & (e < 1.25); edge = (e > .7) & (e <= 1.0)
path = ((xs >= VB[0]) & (xs < VB[1])) | ((ys >= HB[0]) & (ys < HB[1]))
d = (np.median(a[ring & ~path], 0) - np.median(out[edge & ~path], 0)) * .6
out[mask & ~path] = (out[mask & ~path] + d).clip(0, 255)
# さかいめを なじませる（マスクの ふち 3px を まぜる）
from PIL import ImageFilter
m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))
mf = np.asarray(m).astype(np.float32)[..., None] / 255
res = (out * mf + a * (1 - mf)).clip(0, 255).astype(np.uint8)
Image.fromarray(res).save(os.path.join(HERE, 'src', 'grass.webp'), quality=95)
print('ok')
