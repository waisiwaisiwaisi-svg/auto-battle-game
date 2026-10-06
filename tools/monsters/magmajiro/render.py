# 文字マップを 重ねて GBA風に 仕上げる（内側の 黒線→濃い色、光側の 輪郭→濃い色）
import sys, importlib, os
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
M = importlib.import_module(sys.argv[1])
W, H, OX, OY = 84, 70, 6, 4
def off(g, mot):
    x = y = 0
    while g:
        o = mot.get(g)
        if o: x += o[0]; y += o[1]
        g = M.PARENT.get(g)
    return x, y
def compose(frame, mot):
    g = [['.'] * W for _ in range(H)]
    for l in M.layers():
        if l.get('only') and frame not in l['only'].split('|'): continue
        if l.get('not_') and frame in l['not_'].split('|'): continue
        rows = l['rows']
        for k, v in (l.get('alt') or {}).items():
            if frame in k.split('|'): rows = v
        ox, oy = off(l['g'], mot)
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ': continue
                X, Y = l['x'] + i + ox + OX, l['y'] + j + oy + OY
                if 0 <= X < W and 0 <= Y < H: g[Y][X] = ch
    if mot.get('_flip'):
        rows = [r for r in g if any(c != '.' for c in r)]
        g = [['.'] * W for _ in range(H - len(rows))] + rows[::-1]
    return finish(g)
def finish(g):
    def at(y, x): return g[y][x] if 0 <= y < H and 0 <= x < W else '.'
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != 'k': continue
            nb = [at(y + dy, x + dx) for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))]
            if '.' not in nb and 'w' not in nb: out[y][x] = 'l'
            elif (at(y + 1, x) in M.LIGHT or at(y, x + 1) in M.LIGHT) and (at(y - 1, x) == '.' or at(y, x - 1) == '.'): out[y][x] = 'l'
    return out
def paint(g):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); px = im.load()
    for y in range(H):
        for x in range(W):
            ch = g[y][x]
            if ch != '.': c = M.PAL[ch]; px[x, y] = (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
    return im
if __name__ == '__main__':
    out = sys.argv[2]; Z = 6
    ims = {f: paint(compose(f, m)) for f, m in M.FRAMES.items()}
    for f, im in ims.items(): im.save(out.replace('.png', f'_{f}.png'))
    sh = Image.new('RGB', (W * Z * 7, H * Z * 2), (248, 248, 248))
    for i, (f, im) in enumerate(ims.items()):
        b = im.resize((W * Z, H * Z), Image.NEAREST); sh.paste(b, ((i % 7) * W * Z, (i // 7) * H * Z), b)
    sh.save(out)
    print('colors', len(set(c for c in ims['idle0'].getdata() if c[3])))
