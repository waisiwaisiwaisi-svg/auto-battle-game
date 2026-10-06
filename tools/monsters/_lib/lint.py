# ドット絵の 検査（PIXELART.md の ✔ 項目）：idle0 の 完成絵（輪郭 仕上げ後）を 数える
# 使い方: python3 tools/monsters/_lib/lint.py [id ...]   → 1行に 1体、最後に 悪い 順
import colorsys, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); import pix
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N4 = ((0, 1), (0, -1), (1, 0), (-1, 0)); N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))

def hsv(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)); return colorsys.rgb_to_hsv(r, g, b)

def lint(M):
    g = pix.finish(M, pix.compose(M, 'idle0')); H, W = len(g), len(g[0])
    at = lambda y, x: g[y][x] if 0 <= y < H and 0 <= x < W else '.'
    dark = set('kl')
    body = [(y, x) for y in range(H) for x in range(W) if g[y][x] != '.']
    area = max(1, len(body))
    # はぐれドット：内側の 色ドットで、8方向 全部が ちがう 色（輪郭・透明を ふくむ）
    orphan = sum(1 for y, x in body if g[y][x] not in dark and all(at(y + dy, x + dx) != g[y][x] for dy, dx in N8))
    # ダブル：外側の 輪郭ドットで、L字の 角に なって いて 消しても つながりが 切れない もの
    outer = {(y, x) for y, x in body if g[y][x] in dark and any(at(y + dy, x + dx) == '.' for dy, dx in N4)}
    double = 0
    for y, x in outer:
        for (ay, ax), (by, bx) in (((0, 1), (1, 0)), ((0, 1), (-1, 0)), ((0, -1), (1, 0)), ((0, -1), (-1, 0))):
            if (y + ay, x + ax) in outer and (y + by, x + bx) in outer and (y + ay + by, x + ax + bx) not in outer \
               and at(y + ay + by, x + ax + bx) != '.' and sum((y + dy, x + dx) in outer for dy, dx in N4) == 2:
                double += 1; break
    # ピロー影：輪郭の すぐ内側の ドットのうち、光の 当たる 側（上・左が 透明）で いちばん 暗い 段に なって いる 割合
    pal = {c: hsv(v) for c, v in M.PAL.items()}
    lit_edge = [(y, x) for y, x in body if g[y][x] not in dark and (at(y - 1, x) in dark or at(y, x - 1) in dark)
                and (at(y - 2, x) == '.' or at(y, x - 2) == '.')]
    vals = sorted(v[2] for c, v in pal.items() if c not in dark)
    lowv = vals[len(vals) // 3] if vals else 0
    pillow = sum(1 for y, x in lit_edge if pal[g[y][x]][2] <= lowv) / max(1, len(lit_edge))
    # 色相の ずれ：似た 色相（±35度）で 明るさ ちがいの 組で、色相が 4度 以上 ずれて いる 割合
    cs = [v for c, v in pal.items() if c not in dark and v[1] > .12]
    pairs = shift = 0
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            a, b = cs[i], cs[j]; dh = abs(a[0] - b[0]); dh = min(dh, 1 - dh) * 360
            if dh <= 35 and abs(a[2] - b[2]) > .12:
                pairs += 1; shift += dh >= 4
    hue = shift / pairs if pairs else 1.0
    # 灰色の 影：彩度 0.08 未満で 暗い（明るさ 0.5 未満）色が 体に しめる 割合
    grey = sum(1 for y, x in body if g[y][x] not in dark and pal[g[y][x]][1] < .08 and pal[g[y][x]][2] < .5) / area
    return dict(orphan=orphan, double=double, pillow=round(pillow, 2), hueshift=round(hue, 2), grey=round(grey, 2), area=area)

def score(r):   # 大きいほど 悪い
    return r['orphan'] * 2 + r['double'] * 3 + max(0, r['pillow'] - .3) * 40 + max(0, .5 - r['hueshift']) * 30 + r['grey'] * 40

if __name__ == '__main__':
    ids = sys.argv[1:]
    if not ids:
        ids = [i for _, i in re.findall(r'^\| (\d+) \| (\w+) \|', open(os.path.join(HERE, 'ROSTER.md')).read(), re.M)
               if os.path.isfile(os.path.join(HERE, i, 'mon.py'))]
    res = []
    for i in ids:
        try: r = lint(pix.load(os.path.join(HERE, i, 'mon.py')))
        except Exception as e: print(i, 'ERR', e); continue
        res.append((score(r), i, r)); print('%-16s' % i, ' '.join('%s=%s' % kv for kv in r.items()), ' score=%.0f' % score(r))
    if len(res) > 1:
        res.sort(reverse=True)
        print('\n悪い 順:', ', '.join('%s(%.0f)' % (i, s) for s, i, _ in res[:20]))
        import statistics as st
        for k in ('orphan', 'double', 'pillow', 'hueshift', 'grey'):
            print('  %-8s 平均 %.2f' % (k, st.mean(r[k] for _, _, r in res)))
