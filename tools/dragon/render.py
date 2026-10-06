# パーツを 重ねて 1コマ ずつ 描く。動きは パーツ（グループ）ごとの 1ドット ずらし＋差しかえ絵
import sys, importlib
from PIL import Image
sys.path.insert(0, __import__('os').path.dirname(__file__))
mod = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].endswith('.png') else 'dragon')
PARENT = {'head': 'neck', 'jaw': 'head', 'neck': 'body', 'wing': 'body', 'wing2': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
# eye の 差しかえは frame 名で 決まる
S = 64
def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def off(g, mot):
    x = y = 0
    while g:
        o = mot.get(g)
        if o: x += o[0]; y += o[1]
        g = PARENT.get(g)
    return x, y
def render(frame, mot):
    im = Image.new('RGBA', (S + 24, S + 12), (0, 0, 0, 0)); px = im.load()
    for l in mod.layers():
        if l.get('only') and frame not in l['only'].split('|'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if frame in k.split('|'): rows = v
        ox, oy = off(l['g'], mot)
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ': continue
                X, Y = l['x'] + i + ox + 8, l['y'] + j + oy + 6
                if 0 <= X < im.width and 0 <= Y < im.height: px[X, Y] = hexrgb(mod.PAL[ch]) + (255,)
    return im
if __name__ == '__main__':
    frames = getattr(mod, 'FRAMES', {'idle0': {}})
    out = sys.argv[-1] if sys.argv[-1].endswith('.png') else 'out.png'
    Z = 6; ims = [render(f, m) for f, m in frames.items()]
    sheet = Image.new('RGB', (ims[0].width * Z * len(ims), ims[0].height * Z), (78, 120, 84))
    for i, f in enumerate(ims):
        b = f.resize((f.width * Z, f.height * Z), Image.NEAREST); sheet.paste(b, (i * f.width * Z, 0), b)
    sheet.save(out)
    for f, im in zip(frames, ims): im.save(out.replace('.png', f'_{f}.png'))
