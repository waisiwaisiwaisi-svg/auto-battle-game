# 候補の 一覧（id ごとに 1行）
import sys, glob, os
from PIL import Image, ImageDraw
ids = sys.argv[2:]; rows = []
for i in ids:
    fs = sorted(glob.glob(f'raw/{i}_*.png'), key=lambda p: int(p.rsplit('_', 1)[1][:-4]))
    rows.append(fs)
n = max(len(r) for r in rows); S = 200
im = Image.new('RGB', (S * n, S * len(rows)), 'white'); d = ImageDraw.Draw(im)
for y, r in enumerate(rows):
    for x, p in enumerate(r):
        im.paste(Image.open(p).resize((S, S)), (x * S, y * S)); d.text((x * S + 4, y * S + 4), os.path.basename(p)[:-4], fill='red')
im.save(sys.argv[1])
