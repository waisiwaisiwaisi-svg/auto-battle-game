# 検査結果を 目で 見る：はぐれドット（赤の 枠）・ダブル（青の 枠）・ピロー影（黄の 枠）を 8倍の idle0 に 重ねる
# 使い方: python3 _lib/lintview.py out.png id
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import pix, lint
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, i = sys.argv[1], sys.argv[2]
M = pix.load(os.path.join(HERE, i, 'mon.py'))
g = pix.finish(M, pix.compose(M, 'idle0')); H, W = len(g), len(g[0])
at = lambda y, x: g[y][x] if 0 <= y < H and 0 <= x < W else '.'
im = pix.paint(M, pix.compose(M, 'idle0')); Z = 8
b = Image.new('RGBA', im.size, (236, 236, 242, 255)); b.alpha_composite(im); b = b.convert('RGB').resize((W * Z, H * Z), Image.NEAREST); d = ImageDraw.Draw(b)
for y in range(H):
    for x in range(W):
        c = g[y][x]
        if c != '.' and c not in 'kl' and all(at(y + dy, x + dx) != c for dy, dx in lint.N8):
            d.rectangle((x * Z, y * Z, x * Z + Z - 1, y * Z + Z - 1), outline=(255, 0, 0))
bb = b.getbbox(); b.save(out)
print(lint.lint(M))
