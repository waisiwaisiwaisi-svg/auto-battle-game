# picks.json の 設定で ドット絵を 作り、目を 手で 描きなおして all.json に まとめる
# picks.json: { id: { src, h, flip?, colors?, eyes: [[cx, cy, style]], skin?: [x, y] } }
import json, os, sys
import numpy as np
from PIL import Image
from pix import to_pixel
from encode import encode
HERE = os.path.dirname(os.path.abspath(__file__))
EYE = {
    # k=ふち e=白 g/G=虹彩（明/暗） p=ひとみ
    'big': ['..kkkkk..', '.kggggGk.', 'kgeeggGGk', 'kgeepppGk', 'kggppppGk', 'kggppppGk', 'kGgppppGk', '.kGGGGGk.', '..kkkkk..'],
    'mid': ['.kkkkk.', 'kgeegGk', 'kgeppGk', 'kgpppGk', 'kGpppGk', '.kGGGk.', '..kkk..'],
    'small': ['.kkk.', 'keegk', 'kepGk', 'kgpGk', '.kkk.'],
    'dot': ['kkk', 'kek', 'kkk'],
}
def hexrgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
def make(id, c):
    im = to_pixel(os.path.join(HERE, c['src']), c['h'], c.get('flip', False), colors=c.get('colors', 16), bg=c.get('bg', 'rembg'), holes=c.get('holes', False), clip_y=c.get('clip_y'))
    a = np.array(im)
    if c.get('erase'):
        # 指定の 四角を けして 輪郭を 引きなおす（足もとの 草など）
        OL = np.array([26, 16, 34])
        for (x0, y0, x1, y1) in c['erase']: a[y0:y1, x0:x1, 3] = 0
        body = (a[..., 3] > 0) & ~np.all(a[..., :3] == OL, -1)
        H, W = body.shape; out = np.zeros_like(a); out[body] = a[body]
        for y in range(H):
            for x in range(W):
                if body[y, x]: continue
                if any(0 <= yy < H and 0 <= xx < W and body[yy, xx] for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))):
                    out[y, x, :3] = OL; out[y, x, 3] = 255
        a = out
    blinks = []
    for (cx, cy, style, *col) in c.get('eyes', []):
        rows = EYE[style]; h = len(rows); w = len(rows[0])
        g, G = (col[0] if col else '#5ad04a'), (col[1] if len(col) > 1 else '#1e7a3a')
        pal = {'k': '#1a1022', 'e': '#ffffff', 'g': g, 'G': G, 'p': '#1a1022'}
        x0, y0 = cx - w // 2 + 1, cy - h // 2 + 1  # +1 は 輪郭の 余白
        # まぶたの 色は 目の まわり（2ドット外側）で いちばん 多い 明るい色
        from collections import Counter
        cnt = Counter()
        for yy in range(y0 - 3, y0 + h + 3):
            for xx in range(x0 - 3, x0 + w + 3):
                if x0 <= xx < x0 + w and y0 <= yy < y0 + h: continue
                if not (0 <= yy < a.shape[0] and 0 <= xx < a.shape[1]) or a[yy, xx, 3] == 0: continue
                c = tuple(int(v) for v in a[yy, xx, :3])
                if c[0] * .3 + c[1] * .59 + c[2] * .11 > 85: cnt[c] += 1
        lid = list(cnt.most_common(1)[0][0]) if cnt else a[y0 - 1, x0 + w // 2, :3].tolist()
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch == '.': continue
                a[y0 + j, x0 + i, :3] = hexrgb(pal[ch]); a[y0 + j, x0 + i, 3] = 255
        blinks.append((x0, y0, w, h, lid))
    out = Image.fromarray(a); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    p = os.path.join(HERE, 'out', id + '.png'); out.save(p)
    d = encode(p)
    lk = '#1a1022'
    if blinks and lk not in d['pal']: d['pal'].append(lk)
    d['eyes'] = []
    for (x0, y0, w, h, lid) in blinks:
        key = '#%02x%02x%02x' % tuple(lid)
        if key not in d['pal']: d['pal'].append(key)
        d['eyes'].append([x0, y0, w, h - 1, d['pal'].index(key) + 1, d['pal'].index(lk) + 1])
    return d
if __name__ == '__main__':
    picks = json.load(open(os.path.join(HERE, 'picks.json')))
    allp = os.path.join(HERE, 'all.json')
    data = json.load(open(allp)) if os.path.exists(allp) else {}
    for id in (sys.argv[1:] or picks):
        data[id] = make(id, picks[id]); print(id, data[id]['w'], data[id]['h'], len(data[id]['pal']), len(data[id]['d']))
    json.dump(data, open(allp, 'w'))
