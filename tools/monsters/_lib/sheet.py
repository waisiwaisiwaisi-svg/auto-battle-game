# 確認用：指定 id の 待機と 攻撃コマを 並べる（3倍）
import sys, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ids = sys.argv[2:]; S = 3; fr = ['idle0', 'atk1', 'ko']
cw, ch = 96 * S, 84 * S
sh = Image.new('RGB', (cw * len(fr), (ch + 16) * len(ids)), (246, 246, 246)); d = ImageDraw.Draw(sh)
for r, i in enumerate(ids):
    for c, f in enumerate(fr):
        p = os.path.join(HERE, i, 'out', f + '.png')
        if not os.path.exists(p): continue
        im = Image.open(p); b = im.resize((im.width * S, im.height * S), Image.NEAREST)
        sh.paste(b, (c * cw, r * (ch + 16) + 16), b)
    d.text((4, r * (ch + 16) + 2), i, fill='black')
sh.save(sys.argv[1])
