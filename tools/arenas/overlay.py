# 当たり判定の 確認用：python3 overlay.py <名前> [x0 y0 x1 y1] [出力.png]
#   hit/<名前>.json の solid（赤）・low（青）・platforms（紫）を 絵に かさねて、50pxごとの 目もり つきで 出す
#   範囲を 指定すると その部分を 2倍に 拡大して 出す
import json, sys, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
n = sys.argv[1]; box = list(map(int, sys.argv[2:6])) if len(sys.argv) >= 6 else None
out = sys.argv[6] if len(sys.argv) >= 7 else (sys.argv[2] if len(sys.argv) == 3 else os.path.join(HERE, 'hit', n + '_overlay.png'))
h = json.load(open(os.path.join(HERE, 'hit', n + '.json')))
im = Image.open(os.path.join(HERE, 'src', n + '.webp')).convert('RGBA')
L = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
for r in h['solid']: d.rectangle([r[0], r[1], r[2] - 1, r[3] - 1], fill=(255, 0, 0, 100), outline=(255, 0, 0, 255))
for r in h['low']: d.rectangle([r[0], r[1], r[2] - 1, r[3] - 1], fill=(0, 120, 255, 70), outline=(0, 160, 255, 255))
for r in h['platforms']: d.rectangle(r, outline=(200, 0, 255, 255), width=2)
f = h['floor']; d.rectangle(f, outline=(0, 255, 0, 255), width=1)
for x in range(0, im.width, 50): d.line([x, 0, x, im.height], fill=(255, 255, 255, 60 if x % 100 else 130))
for y in range(0, im.height, 50): d.line([0, y, im.width, y], fill=(255, 255, 255, 60 if y % 100 else 130))
im = Image.alpha_composite(im, L); d = ImageDraw.Draw(im)
for x in range(0, im.width, 100): d.text((x + 2, 2), str(x), fill=(255, 255, 0, 255))
for y in range(0, im.height, 100): d.text((2, y + 2), str(y), fill=(255, 255, 0, 255))
if box:
    im = im.crop(box); im = im.resize((im.width * 2, im.height * 2), Image.NEAREST); d = ImageDraw.Draw(im)
    for x in range((box[0] // 50 + 1) * 50, box[2], 50): d.text(((x - box[0]) * 2 + 2, 2), str(x), fill=(255, 255, 0, 255))
    for y in range((box[1] // 50 + 1) * 50, box[3], 50): d.text((2, (y - box[1]) * 2 + 2), str(y), fill=(255, 255, 0, 255))
im.convert('RGB').save(out); print(out)
