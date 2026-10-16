# ステージを「床（ステージごと）」「観客席の枠（共通）」「観客」「旗」「置きもの」に わけて index.html に いれる
# 使い方: python3 tools/arenas/build_stage.py
#   stage_src/F1.png 枠（まんなか透明） F2.png 観客 6×2  F3.png 旗 6×5  S01〜S10.png 床  P1〜P5.png 置きもの 4×2
#   座標は 元の 闘技場の 画像（1448×1086）＝ゲームの 世界座標
import base64, io, json, os, re
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'stage_src')
GAME = os.path.join(HERE, '..', '..', 'index.html')
BEGIN, END = '// ====== STAGE（tools/arenas/build_stage.py が 自動生成）======', '// ====== ここまで STAGE ======'
W, H = 1448, 1086
KEYS = ['grass', 'fire', 'water', 'elec', 'ice', 'dragon', 'wind', 'ground', 'poison', 'fighting']
IMG_K = .7   # 画像は 縮めて 保存（カメラで 縮めて うつすので じゅうぶん）

def enc(im, fmt='WEBP', q=88):
    b = io.BytesIO()
    if fmt == 'WEBP': im.save(b, 'WEBP', quality=q, method=6)
    else: im.save(b, 'PNG', optimize=True)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()

def cells(a, cols, rows):
    # マスわり：絵の ない すきまで きる
    op = a[:, :, 3] > 40
    def cuts(prof, n, L):
        out = []
        for k in range(1, n):
            c = L * k // n; lo, hi = c - L // (n * 3), c + L // (n * 3); out.append(lo + int(np.argmin(prof[lo:hi])))
        return [0] + out + [L]
    xs, ys = cuts(op.sum(0), cols, a.shape[1]), cuts(op.sum(1), rows, a.shape[0])
    return [[a[ys[r]:ys[r + 1], xs[c]:xs[c + 1]] for c in range(cols)] for r in range(rows)]

def crop_alpha(c):
    ys, xs = np.where(c[:, :, 3] > 40)
    return Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1], 'RGBA')

# ---- 枠：まんなかの 穴と、みどりの 旗（あとで タイプの 旗を かける）----
fr = np.array(Image.open(f'{SRC}/F1.png').convert('RGBA').resize((W, H), Image.LANCZOS))
al = fr[:, :, 3]; ys, xs = np.where(al[100:1000, 100:1350] < 20); hole = [int(xs.min() + 100), int(ys.min() + 100), int(xs.max() + 101), int(ys.max() + 101)]
r, g, b = [fr[:, :, i].astype(int) for i in range(3)]
green = (g > r + 35) & (g > b + 15) & (g > 70) & (al > 200)
lab, n = ndimage.label(ndimage.binary_closing(green, iterations=2))
slots = []
for i, sl in enumerate(ndimage.find_objects(lab)):
    y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
    if (lab[sl] == i + 1).sum() < 400 or (y1 - y0) < 40 or (y1 - y0) < (x1 - x0): continue   # たてながの 旗だけ
    slots.append([x0, y0, x1, y1])
# 旗の ところを まわりの 色で うめる（あとで 上に タイプの 旗を かく）
mask = np.zeros_like(green)
for x0, y0, x1, y1 in slots: mask[y0 - 3:y1 + 3, x0 - 3:x1 + 3] = True
f = fr[:, :, :3].astype(float); known = ~mask
for _ in range(60):
    if known.all(): break
    acc = np.zeros_like(f); cnt = np.zeros(mask.shape)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sk = np.roll(known, (dy, dx), (0, 1)); sf = np.roll(f, (dy, dx), (0, 1))
        acc += sf * sk[:, :, None]; cnt += sk
    new = (~known) & (cnt > 0); f[new] = acc[new] / cnt[new][:, None]; known = known | new
fr[:, :, :3] = f.clip(0, 255).astype(np.uint8)
frame = Image.fromarray(fr, 'RGBA').resize((int(W * IMG_K), int(H * IMG_K)), Image.LANCZOS)

# ---- 床 ----
hw, hh = hole[2] - hole[0], hole[3] - hole[1]
floors = {}
for i, k in enumerate(KEYS):
    im = Image.open(f'{SRC}/S{i + 1:02d}.png').convert('RGB').resize((int((hw + 16) * IMG_K), int((hh + 16) * IMG_K)), Image.LANCZOS)
    floors[k] = enc(im, q=86)

# ---- 観客 ----
cr = cells(np.array(Image.open(f'{SRC}/F2.png').convert('RGBA')), 6, 2)
CH = 24   # 観客 1人の 高さ（ドット絵を この 高さに）
crowd_img = []
for row in cr:
    for c in row:
        im = crop_alpha(c); s = CH / im.height; crowd_img.append(im.resize((max(1, round(im.width * s)), CH), Image.NEAREST))
cw = max(i.width for i in crowd_img); strip = Image.new('RGBA', (cw * 12, CH))
for j, im in enumerate(crowd_img): strip.paste(im, (j * cw + (cw - im.width) // 2, 0))
crowd = {'src': enc(strip, 'PNG'), 'w': cw, 'h': CH, 'n': 6}

# ---- 旗 ----
bn = cells(np.array(Image.open(f'{SRC}/F3.png').convert('RGBA')), 6, 5)
BH = 64; bimgs = {}
ORDER = [('grass', 'fire'), ('water', 'elec'), ('ice', 'dragon'), ('wind', 'ground'), ('poison', 'fighting')]
bw = 0; tmp = {}
for r_, (ka, kb) in enumerate(ORDER):
    for half, k in enumerate((ka, kb)):
        fr3 = [crop_alpha(bn[r_][half * 3 + j]) for j in range(3)]
        fr3 = [im.resize((max(1, round(im.width * BH / im.height)), BH), Image.LANCZOS) for im in fr3]
        tmp[k] = fr3; bw = max(bw, *[im.width for im in fr3])
banners = {}
for k, fr3 in tmp.items():
    st = Image.new('RGBA', (bw * 3, BH))
    for j, im in enumerate(fr3): st.paste(im, (j * bw + (bw - im.width) // 2, 0))
    banners[k] = enc(st, 'PNG')

# ---- 置きもの：いまの 障害物の ばしょ（四すみ）に おく ----
src = open(GAME, encoding='utf-8').read()
AR = json.loads(re.search(r'ARENAS = (\{.*?\});\n', src, re.S).group(1))
props = {}
for j in range(5):
    pc = cells(np.array(Image.open(f'{SRC}/P{j + 1}.png').convert('RGBA')), 4, 2)
    for rr in range(2):
        k = KEYS[j * 2 + rr]; solid = AR[k]['solid'][10:]   # さいしょの 10こは 台・管・はしらの 柱（枠の 一部）
        out = []
        for q, (qx, qy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):   # 左上・右上・左下・右下
            rs = [s for s in solid if ((s[0] + s[2]) / 2 > W / 2) == bool(qx) and ((s[1] + s[3]) / 2 > H / 2) == bool(qy)]
            if not rs: continue
            x0, y0, x1, y1 = min(s[0] for s in rs), min(s[1] for s in rs), max(s[2] for s in rs), max(s[3] for s in rs)
            im = crop_alpha(pc[rr][q]); dw = (x1 - x0) * 1.12; dh = dw * im.height / im.width
            sv = im.resize((max(1, round(dw * .8)), max(1, round(dh * .8))), Image.LANCZOS)   # 表示の 0.8 倍で 保存
            # あたりはんてい：絵の 列ごとに、した 55% を 足もととして 通れなく する（CELL ごとの 四角に まとめる）
            A = np.array(im.resize((max(1, round(dw)), max(1, round(dh))), Image.LANCZOS))[:, :, 3] > 100
            px0, py0 = (x0 + x1) / 2 - dw / 2, y1 + 6 - dh; CELL = 12; rects = []
            for cx in range(0, A.shape[1], CELL):
                col = A[:, cx:cx + CELL].any(1); ys_ = np.where(col)[0]
                if len(ys_) < 4: continue
                top, bot = ys_.min(), ys_.max(); fy0 = bot - (bot - top) * .55
                if A[:, cx:cx + CELL].sum() < CELL * 3: continue
                rects.append([round(px0 + cx), round(py0 + fy0), round(px0 + min(cx + CELL, A.shape[1])), round(py0 + bot - 4)])
            # となりの 列と おなじ 高さなら つなげる
            mg = []
            for r_ in rects:
                if mg and abs(mg[-1][1] - r_[1]) < 10 and abs(mg[-1][3] - r_[3]) < 10 and mg[-1][2] >= r_[0] - 1: mg[-1] = [mg[-1][0], min(mg[-1][1], r_[1]), r_[2], max(mg[-1][3], r_[3])]
                else: mg.append(r_)
            out.append({'src': enc(sv, 'PNG'), 'x': round((x0 + x1) / 2), 'y': y1 + 6, 'w': round(dw), 'h': round(dh), 'solid': mg})
        props[k] = out

# ---- 観客の 席（上の 観客席）----
seats = []; rng = np.random.default_rng(7)
for y in (14, 28, 42, 56):
    for xa, xb in ((14, 172), (214, 544), (906, 1236), (1278, 1432)):
        x = xa + (y // 14 % 2) * 9
        while x < xb:
            if rng.random() < .8: seats.append([int(x), y + 22, int(rng.integers(0, 6))])
            x += 19 + int(rng.integers(0, 6))

data = {'hole': hole, 'frame': enc(frame, q=88), 'floors': floors, 'crowd': crowd, 'banners': banners, 'bw': bw, 'bh': BH, 'slots': slots, 'props': props, 'seats': seats}
block = BEGIN + '\nconst STAGE = ' + json.dumps(data, separators=(',', ':')) + ';\n' + END
if BEGIN in src: src = re.sub(re.escape(BEGIN) + '.*?' + re.escape(END), lambda m: block, src, flags=re.S)
else: src = src.replace('// ====== ここまで ARENAS ======', '// ====== ここまで ARENAS ======\n' + block, 1)
open(GAME, 'w', encoding='utf-8').write(src)
print('hole', hole, 'slots', len(slots), 'seats', len(seats), 'props', {k: len(v) for k, v in props.items()}, 'bytes', len(block))
