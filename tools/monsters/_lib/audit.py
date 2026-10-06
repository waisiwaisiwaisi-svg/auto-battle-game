# 検査：コマの 中で 体から はなれた かたまり（手足の うき）を 数える
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import pix
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def comps(g):
    H, W = len(g), len(g[0]); seen = [[0] * W for _ in range(H)]; out = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' or seen[y][x]: continue
            st = [(y, x)]; seen[y][x] = 1; n = 0; xs = []; ys = []
            while st:
                cy, cx = st.pop(); n += 1; xs.append(cx); ys.append(cy)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and not seen[ny][nx] and g[ny][nx] != '.': seen[ny][nx] = 1; st.append((ny, nx))
            out.append((n, min(xs), min(ys), max(xs), max(ys)))
    return sorted(out, reverse=True)
ids = sys.argv[1:] or sorted(d for d in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, d, 'mon.py')))
for i in ids:
    try:
        M = pix.load(os.path.join(HERE, i, 'mon.py'))
        bad = {}
        for f in ('idle0', 'walk0', 'walk2', 'hit'):
            c = comps(pix.compose(M, f))
            big = [x for x in c[1:] if x[0] >= 12]
            if big: bad[f] = [(n, (x0 - pix.OX, y0 - pix.OY)) for n, x0, y0, _, _ in big]
        if bad: print(i, bad)
    except Exception as e: print(i, 'ERR', e)
