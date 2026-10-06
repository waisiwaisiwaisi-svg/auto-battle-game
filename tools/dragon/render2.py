# GBA風：文字のまま 重ねて → 16色に 変換 → セルアウト → 色をぬる
import sys
from PIL import Image
import dragon as D, gba
PARENT = {'head': 'neck', 'jaw': 'head', 'neck': 'body', 'wing': 'body', 'wing2': 'body', 'tail': 'body', 'body': 'root', 'legA': 'root', 'legB': 'root'}
W, H, OX, OY = 88, 76, 8, 6
def off(g, mot):
    x = y = 0
    while g:
        o = mot.get(g)
        if o: x += o[0]; y += o[1]
        g = PARENT.get(g)
    return x, y
def compose(frame, mot):
    g = [['.'] * W for _ in range(H)]
    for l in D.layers():
        if l.get('only') and frame not in l['only'].split('|'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if frame in k.split('|'): rows = v
        ox, oy = off(l['g'], mot)
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ': continue
                X, Y = l['x'] + i + ox + OX, l['y'] + j + oy + OY
                if 0 <= X < W and 0 <= Y < H: g[Y][X] = ch
    return gba.finish([''.join(r) for r in g])
def paint(rows):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': c = gba.PAL16[ch]; px[x, y] = (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
    return im
if __name__ == '__main__':
    out = sys.argv[1]
    for f, m in D.FRAMES.items(): paint(compose(f, m)).save(out.replace('.png', f'_{f}.png'))
    im = paint(compose('idle0', {}))
    cols = set(c for c in im.getdata() if c[3])
    print('colors', len(cols))
    im.resize((W * 8, H * 8), Image.NEAREST).save(out)
