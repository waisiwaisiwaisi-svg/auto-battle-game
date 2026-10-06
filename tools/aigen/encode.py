# ドット絵 PNG → {w,h,pal,d}（d は ランレングス：1文字の 色番号 ＋ 2桁 36進の 長さ）
import sys, json
import numpy as np
from PIL import Image
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
def encode(path):
    im = np.asarray(Image.open(path).convert('RGBA'))
    h, w = im.shape[:2]; pal = []; idx = np.zeros((h, w), int)
    key = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = im[y, x]
            if a < 128: continue
            k = '#%02x%02x%02x' % (r, g, b)
            if k not in key: key[k] = len(pal) + 1; pal.append(k)
            idx[y, x] = key[k]
    assert len(pal) < len(AL), len(pal)
    flat = idx.flatten(); out = []; i = 0
    while i < len(flat):
        j = i
        while j < len(flat) and flat[j] == flat[i] and j - i < 1295: j += 1
        n = j - i; out.append(AL[flat[i]] + np.base_repr(n, 36).lower().rjust(2, '0')); i = j
    return {'w': w, 'h': h, 'pal': pal, 'd': ''.join(out)}
if __name__ == '__main__':
    print(json.dumps(encode(sys.argv[1])))
