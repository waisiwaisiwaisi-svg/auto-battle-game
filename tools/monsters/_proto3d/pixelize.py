# 4倍の イラスト → 1倍の ドット（色は パレットへ、かたまりは 多数決、輪郭は 1ドット）
import numpy as np
from PIL import Image
def pixelize(img, ss, pal):
    a = np.asarray(img.convert('RGBA'), float); H, W = a.shape[0] // ss, a.shape[1] // ss
    cols = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal], float)
    d = ((a[..., None, :3] - cols[None, None]) ** 2).sum(-1); idx = np.argmin(d, -1); idx[a[..., 3] < 128] = -1
    out = np.full((H, W), -1, int)
    for y in range(H):
        for x in range(W):
            b = idx[y * ss:(y + 1) * ss, x * ss:(x + 1) * ss].ravel(); c = b[b >= 0]
            if len(c) * 2 >= ss * ss:
                v, n = np.unique(c, return_counts=True)
                # 黒（輪郭）が 1/4 以上 あれば 黒を 優先（線が 消えない ように）
                if 0 in v and n[list(v).index(0)] * 4 >= ss * ss: out[y, x] = 0
                else: out[y, x] = v[np.argmax(n)]
    return out
def to_img(out, pal, Z=8, bg=(236, 236, 242)):
    H, W = out.shape; im = Image.new('RGB', (W, H), bg)
    for y in range(H):
        for x in range(W):
            if out[y, x] >= 0: im.putpixel((x, y), tuple(int(pal[out[y, x]][i:i + 2], 16) for i in (1, 3, 5)))
    return im.resize((W * Z, H * Z), Image.NEAREST)
if __name__ == '__main__':
    import lion_svg as L
    pal = ['#140e18'] + L.FUR + L.FURF[3:] + L.CREAM + L.FIRE + L.STEEL + ['#ffffff', '#ffd23a', '#c0281c', '#8a1c28']
    out = pixelize(Image.open('lion_hi.png'), 4, pal); to_img(out, pal).save('lion_px.png'); print(len(pal))
