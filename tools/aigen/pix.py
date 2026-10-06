# 生成画像 → ゲーム用ドット絵（背景を ぬく → 高さを そろえて 縮小 → 減色 → 輪郭 → 掃除）
# 使い方: ../sd/bin/python pix.py raw/hinokon_12.png out/hinokon.png 52 [flip]
import sys, os, numpy as np
from PIL import Image
from rembg import remove, new_session

_session = None
def cutout(im):
    global _session
    if _session is None: _session = new_session('isnet-general-use')
    return remove(im, session=_session)

def flood_bg(im, tol=34):
    """ふちから 背景色に 近い ところを ぬりつぶして 背景と みなす"""
    a = np.asarray(im).astype(int); H, W = a.shape[:2]
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, 0)
    near = np.abs(a - bg).sum(2) < tol * 3
    seen = np.zeros((H, W), bool); st = [(y, x) for y in (0, H - 1) for x in range(W)] + [(y, x) for x in (0, W - 1) for y in range(H)]
    while st:
        y, x = st.pop()
        if seen[y, x] or not near[y, x]: continue
        seen[y, x] = True
        if y > 0: st.append((y - 1, x))
        if y < H - 1: st.append((y + 1, x))
        if x > 0: st.append((y, x - 1))
        if x < W - 1: st.append((y, x + 1))
    return ~seen

def to_pixel(src, height, flip=False, colors=16, outline=(26, 16, 34), linew=3.0, method='lanczos', bg='rembg'):
    im = Image.open(src).convert('RGB')
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if bg == 'rembg':
        rgba = cutout(im)
    else:
        fg = flood_bg(im)
        if bg == 'union': fg |= np.asarray(cutout(im))[..., 3] > 128
        rgba = im.convert('RGBA'); arr = np.asarray(rgba).copy(); arr[..., 3] = np.where(fg, 255, 0); rgba = Image.fromarray(arr)
    a = np.asarray(rgba)[..., 3]
    ys, xs = np.nonzero(a > 128)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    rgba = rgba.crop(box)
    w, h = rgba.size
    th = height; tw = max(1, round(w * th / h))
    if tw > 84: tw = 84; th = round(h * tw / w)
    if method == 'lanczos':
        # なめらかに 縮小してから 減色（線は うすく 残る → 減色で 濃い色に よる）
        arr = np.asarray(rgba).astype(float); m = arr[..., 3] > 128
        fill = arr[m][:, :3].mean(0)
        rgb = arr[..., :3].copy(); rgb[~m] = fill
        small = Image.fromarray(rgb.astype(np.uint8)).resize((tw, th), Image.LANCZOS)
        al = np.asarray(rgba.split()[3].resize((tw, th), Image.BOX)) > 128
        # 少し コントラストを 上げてから 減色
        sm = np.asarray(small).astype(float); sm = np.clip((sm - 128) * 1.12 + 128, 0, 255).astype(np.uint8)
        q = Image.fromarray(sm).quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        px = np.asarray(q.convert('RGB')).copy()
    else:
        # 先に 大きいまま 減色 → ブロックごとの 最頻色で 縮小（にごらない）
        al_full = np.asarray(rgba.split()[3]) > 128
        rgb = Image.new('RGB', rgba.size, (255, 255, 255)); rgb.paste(rgba, mask=rgba.split()[3])
        pal_im = rgb.quantize(colors=colors, method=Image.Quantize.KMEANS if hasattr(Image.Quantize, 'KMEANS') else Image.Quantize.MEDIANCUT, kmeans=3, dither=Image.Dither.NONE)
        idx = np.asarray(pal_im); pal = np.array(pal_im.getpalette()[:colors * 3]).reshape(-1, 3)
        lum = pal @ np.array([.3, .59, .11]); dark = lum < 70
        px = np.zeros((th, tw, 3), np.uint8); al = np.zeros((th, tw), bool)
        sy, sx = h / th, w / tw
        for y in range(th):
            for x in range(tw):
                y0, y1 = int(y * sy), max(int(y * sy) + 1, int((y + 1) * sy)); x0, x1 = int(x * sx), max(int(x * sx) + 1, int((x + 1) * sx))
                m = al_full[y0:y1, x0:x1]
                if m.mean() < .5: continue
                # 中央よりの 画素を 重く
                v = idx[y0:y1, x0:x1][m]
                c = np.bincount(v, minlength=colors).astype(float)
                # 線（暗い色）は 細くて 消えやすいので ひいきする
                c[dark] *= linew
                px[y, x] = pal[int(np.argmax(c))]; al[y, x] = True

    # いちばん 大きい かたまり（＋ある程度 大きい もの）だけ のこす
    lab = np.zeros((th, tw), int); comps = []
    for y in range(th):
        for x in range(tw):
            if al[y, x] and not lab[y, x]:
                st = [(y, x)]; lab[y, x] = len(comps) + 1; n = 0
                while st:
                    cy, cx = st.pop(); n += 1
                    for yy, xx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= yy < th and 0 <= xx < tw and al[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = len(comps) + 1; st.append((yy, xx))
                comps.append(n)
    if comps:
        big = max(comps)
        for i, n in enumerate(comps):
            if n < max(12, big * .08): al[lab == i + 1] = False
    # ひとりぼっちの ドットを 消す
    al2 = al.copy()
    for y in range(th):
        for x in range(tw):
            if al[y, x]:
                n = sum(al[yy, xx] for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)) if 0 <= yy < th and 0 <= xx < tw)
                if n <= 1: al2[y, x] = False
    al = al2
    # 1ドットの 余白を つけて 外側に 輪郭
    H, W = th + 2, tw + 2
    out = np.zeros((H, W, 4), np.uint8)
    out[1:-1, 1:-1, :3] = px; out[1:-1, 1:-1, 3] = np.where(al, 255, 0)
    A = out[..., 3] > 0
    res = out.copy()
    for y in range(H):
        for x in range(W):
            if A[y, x]: continue
            if any(0 <= yy < H and 0 <= xx < W and A[yy, xx] for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))):
                res[y, x, :3] = outline; res[y, x, 3] = 255
    return Image.fromarray(res)

if __name__ == '__main__':
    src, dst, h = sys.argv[1], sys.argv[2], int(sys.argv[3])
    flip = 'flip' in sys.argv[4:]
    method = 'mode' if 'mode' in sys.argv[4:] else 'lanczos'
    bgm = 'flood' if 'flood' in sys.argv[4:] else 'union' if 'union' in sys.argv[4:] else 'rembg'
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    im = to_pixel(src, h, flip, method=method, colors=int(os.environ.get('COLORS', 16)), bg=bgm); im.save(dst)
    im.resize((im.width * 8, im.height * 8), Image.NEAREST).save(dst.replace('.png', '_x8.png'))
    print(dst, im.size)
