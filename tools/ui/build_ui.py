# ChatGPT に つくってもらった UI の シート（U1〜U3・U6・U7）を ドットに もどして index.html に うめこむ
# usage: python3 tools/ui/build_ui.py   → index.html の「UIA」ブロックを かきかえる（プレビュー：tools/ui/out/*.png）
# U4・U5（アニメ）は tools/anim/gpt_fx.py で つくる
import base64, io, json, os, re
import numpy as np
from scipy import ndimage
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
# シート: (よこ, たて, なまえ（None は つかわない）, いちばん ながい へんの ドット数)
SHEETS = {
    'U1': (6, 4, ['pill', 'bell', 'leaf', 'stone', 'crystal', 'chest',
                  'trophy', 'medal', 'crown', 'badge', 'gem', 'star',
                  'hand_down', 'hand_up', 'hand', 'warn', 'ban', 'arrow_down',
                  'pencil', 'lr', 'undo', 'rotate', 'note', 'pause'], 18),
    'U2': (4, 3, ['emb_shield', 'emb_sword', 'emb_fire', 'emb_drop', 'emb_leaf', 'emb_bolt', 'emb_snow', 'emb_dragon', 'emb_moon', 'emb_star', 'emb_crown', 'emb_skull'], 24),
    'U3': (8, 3, ['d0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'plus', 'minus', 'excl', 'ques', 'times', 'pct',
                  'z', 'up', 'down', 'dstar', 'dnote', 'heart', 'dot', None], 11),
    'U6': (4, 3, ['btn_blue', 'btn_gold', 'btn_red', 'btn_grey', 'pnl_navy', 'pnl_gold', 'pinch', 'frame',
                  'band_blue', 'band_red', 'vs', 'shadow'], 40),
    'U7': (1, 1, ['logo'], 150),
}
# もとの 絵の 1ドットの 大きさ（画素）：いろが おなじ はばの でやすい 長さから はかった
NATIVE = {'U1': 10.7, 'U2': 8, 'U3': 14.5, 'U6': 11, 'U7': 14.7}

def bbox(c):
    p = np.argwhere(c[:, :, 3] > 40)
    if not len(p): return None
    return p[:, 0].min(), p[:, 0].max() + 1, p[:, 1].min(), p[:, 1].max() + 1

def reduce(c, P):
    # P×P の ブロックごと：こさは 平均（3だんかい）、いろは こい 画素の 中央値
    H, W = c.shape[:2]; h, w = -(-H // P), -(-W // P)
    pad = np.zeros((h * P, w * P, 4), np.uint8); pad[:H, :W] = c
    b = pad.reshape(h, P, w, P, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, P * P, 4).astype(np.float32)
    al = b[..., 3]; ma = al.mean(-1); out = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            if ma[y, x] < 60: continue
            m = al[y, x] > 100
            if not m.any(): m = al[y, x] > 0
            out[y, x, :3] = np.median(b[y, x][m][:, :3], 0)
            out[y, x, 3] = 255 if ma[y, x] > 150 else 150
    return out

UIA = {}
for sh, (C, R, names, T) in SHEETS.items():
    a = np.array(Image.open(f'{HERE}/src/{sh}.png').convert('RGBA'))
    H, W = a.shape[:2]; cells = []
    for i, n in enumerate(names):
        if not n: continue
        r, c = divmod(i, C); cell = a[H * r // R:H * (r + 1) // R, W * c // C:W * (c + 1) // C]
        # となりの マスに はみでた 絵を ひろい、まんなかが この マスに ある かたまりだけ のこす
        y0, y1, x0, x1 = H * r // R, H * (r + 1) // R, W * c // C, W * (c + 1) // C; my, mx = (y1 - y0) // 4, (x1 - x0) // 4
        Y0, Y1, X0, X1 = max(0, y0 - my), min(H, y1 + my), max(0, x0 - mx), min(W, x1 + mx); win = a[Y0:Y1, X0:X1].copy()
        lab, nl = ndimage.label(win[:, :, 3] > 40); keep = np.zeros(nl + 1, bool)
        for k, (cy, cx) in enumerate(ndimage.center_of_mass(np.ones_like(lab), lab, range(1, nl + 1)), 1):
            keep[k] = y0 <= cy + Y0 < y1 and x0 <= cx + X0 < x1
        win[~keep[lab]] = 0; bb = bbox(win)
        if bb: cells.append((n, win[bb[0]:bb[1], bb[2]:bb[3]]))
    for n, x in cells:
        f8 = 8 / NATIVE[sh]; im0 = Image.fromarray(x, 'RGBA'); x = np.array(im0.resize((max(1, round(im0.width * f8)), max(1, round(im0.height * f8))), Image.LANCZOS)); p = 8
        d = reduce(x, p); bb = bbox(d)
        if bb: d = d[bb[0]:bb[1], bb[2]:bb[3]]
        im = Image.fromarray(d, 'RGBA'); q = im.convert('RGB').quantize(24, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(im.getchannel('A'))
        q.save(f'{OUT}/{n}.png'); bio = io.BytesIO(); q.save(bio, 'PNG', optimize=True)
        UIA[n] = {'w': q.width, 'h': q.height, 'src': 'data:image/png;base64,' + base64.b64encode(bio.getvalue()).decode()}
        print(sh, n, q.width, q.height, 'pitch', p)

H0, H1 = '// ====== UIA（ChatGPT の UI の 絵：tools/ui/build_ui.py）======', '// ====== ここまで UIA ======'
f = os.path.join(ROOT, 'index.html'); s = open(f, encoding='utf-8').read()
blk = f'{H0}\nconst UIA = {json.dumps(UIA, separators=(",", ":"))};\n{H1}'
if H0 in s: s = re.sub(re.escape(H0) + r'.*?' + re.escape(H1), lambda _: blk, s, flags=re.S)
else: s = s.replace('const ICONS = {', blk + '\nconst ICONS = {', 1)
open(f, 'w', encoding='utf-8').write(s); print(len(blk), 'bytes')
