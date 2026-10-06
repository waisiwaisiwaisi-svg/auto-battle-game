# ドット絵を 10倍に して 5ドットごとの 目盛り（座標の 確認用）
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('RGBA'); S = 10
bg = Image.new('RGBA', (im.width * S + 30, im.height * S + 30), (70, 120, 70, 255))
bg.paste(im.resize((im.width * S, im.height * S), Image.NEAREST), (30, 30), im.resize((im.width * S, im.height * S), Image.NEAREST))
d = ImageDraw.Draw(bg)
for x in range(0, im.width + 1, 5):
    d.line([(30 + x * S, 30), (30 + x * S, 30 + im.height * S)], fill=(255, 255, 255, 90) if x % 10 else (255, 255, 0, 160)); d.text((30 + x * S - 4, 4 if x % 10 == 0 else 16), str(x), fill='white')
for y in range(0, im.height + 1, 5):
    d.line([(30, 30 + y * S), (30 + im.width * S, 30 + y * S)], fill=(255, 255, 255, 90) if y % 10 else (255, 255, 0, 160)); d.text((2, 30 + y * S - 6), str(y), fill='white')
bg.save(sys.argv[2])
