# 目の 見くらべ用：各 mon.py の EYE_BOX=(x, y, w, h)（idle0 の 64x64 座標）の まわりを 拡大して 並べる
# 使い方: python3 _lib/eyes.py out.png [id ...]
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__)); import pix
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]; ids = sys.argv[2:]
if not ids:
    order = re.findall(r'^\| (\d+) \| (\w+) \|', open(os.path.join(HERE, 'ROSTER.md')).read(), re.M)
    ids = [i for _, i in order if os.path.isfile(os.path.join(HERE, i, 'mon.py'))]
Z, C, COLS = 6, 20, 10   # 拡大率・切り出し 20x20・1行の 数
cells = []
for i in ids:
    M = pix.load(os.path.join(HERE, i, 'mon.py'))
    box = getattr(M, 'EYE_BOX', None)
    row = []
    for f in ('idle0', 'atk1', 'hit'):
        im = pix.paint(M, pix.compose(M, f))
        if box:
            cx, cy = pix.OX + box[0] + box[2] // 2, pix.OY + box[1] + box[3] // 2
        else:
            cx, cy = pix.OX + 48, pix.OY + 30
        b = Image.new('RGBA', im.size, (236, 236, 242, 255)); b.alpha_composite(im)
        row.append(b.crop((cx - C // 2, cy - C // 2, cx + C // 2, cy + C // 2)).convert('RGB').resize((C * Z, C * Z), Image.NEAREST))
    cells.append((i, row, box is None))
W = C * Z * 3 + 8; H = C * Z + 18
cols = min(COLS // 3 * 1 + 2, 4)
sh = Image.new('RGB', (W * cols, H * ((len(cells) + cols - 1) // cols)), (40, 40, 52)); d = ImageDraw.Draw(sh)
for n, (i, row, nobox) in enumerate(cells):
    x, y = (n % cols) * W, (n // cols) * H
    for k, im in enumerate(row): sh.paste(im, (x + k * C * Z, y + 16))
    d.text((x + 4, y + 2), i + ('  (EYE_BOX なし)' if nobox else ''), fill='white')
sh.save(out)
