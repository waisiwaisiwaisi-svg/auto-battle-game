# ChatGPT に つくってもらった エフェクトの シート（横6コマ×縦4段）を ドットに もどして コマに きる
# usage: python3 tools/anim/gpt_fx.py   → tools/anim/gpt_fx/<key>.png（よこ 1れつ）と meta.json
import json, os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'gpt_fx')
SHEETS = {'E1': ['p_fire', 'p_water', 'p_elec', 'p_ice'], 'E2': ['p_grass', 'p_poison', 'p_psychic', 'p_ghost'],
          'E3': ['p_dragon', 'p_fighting', 'p_normal', 'p_bug'], 'E4': ['p_wind', 'p_rock', 'p_hadou', 'p_moon'],
          'E5': ['wave', 'whirl', 'tornado', 'mine'], 'E6': ['fist', 'nail', 'skull', 'web']}
ONCE = {'fist', 'nail', 'skull', 'web'}
BOTTOM = {'tornado', 'mine'}   # 足もとが きじゅん
# 1つの エフェクトを なんドットに するか（いちばん ながい へん）。ゲームでは 1ドット＝PIX_D で かく
TARGET = {'p_hadou': 22, 'p_moon': 22, 'wave': 40, 'whirl': 36, 'tornado': 30, 'mine': 16, 'fist': 28, 'nail': 24, 'skull': 20, 'web': 30}
TDEF = 20
COLS, ROWS = 6, 4

def comp_cells(a):
    # マスわり：絵が ない 列・行の すきまで きる（なければ 等分）
    H, W = a.shape[:2]; op = a[:, :, 3] > 40
    def cuts(prof, n, L):
        out = []
        for k in range(1, n):
            c = L * k // n; lo, hi = c - L // (n * 3), c + L // (n * 3)
            seg = prof[lo:hi]; out.append(lo + int(np.argmin(seg)))
        return [0] + out + [L]
    return cuts(op.sum(0), COLS, W), cuts(op.sum(1), ROWS, H)

def reduce(c, PITCH):
    # PITCH ごとの ブロックで：不透明が はんぶん いじょうなら その ブロックの 不透明画素の 中央値の いろ
    h, w = c.shape[0] // PITCH, c.shape[1] // PITCH
    b = c[:h * PITCH, :w * PITCH].reshape(h, PITCH, w, PITCH, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, PITCH * PITCH, 4)
    op = b[..., 3] > 128; out = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            m = op[y, x]
            if m.sum() * 2 >= PITCH * PITCH * .8:
                out[y, x, :3] = np.median(b[y, x][m][:, :3], 0); out[y, x, 3] = 255
    return out

meta = {}
for sh, keys in SHEETS.items():
    a = np.array(Image.open(f'{D}/src/{sh}.png').convert('RGBA'))
    xs, ys = comp_cells(a)
    for r, k in enumerate(keys):
        cells = [a[ys[r]:ys[r + 1], xs[c]:xs[c + 1]] for c in range(COLS)]
        # 6コマ ぶんの 絵の はんいを あわせる（コマごとに ずれない ように）
        bb = [np.argwhere(c[:, :, 3] > 40) for c in cells]
        y0 = min(b[:, 0].min() for b in bb if len(b)); y1 = max(b[:, 0].max() for b in bb if len(b)) + 1
        x0 = min(b[:, 1].min() for b in bb if len(b)); x1 = max(b[:, 1].max() for b in bb if len(b)) + 1
        PITCH = max(2, round(max(y1 - y0, x1 - x0) / TARGET.get(k, TDEF)))
        hh, ww = y1 - y0, x1 - x0; hh += (-hh) % PITCH; ww += (-ww) % PITCH
        fr = []
        for c in cells:
            pad = np.zeros((hh, ww, 4), np.uint8); s = c[y0:y0 + hh, x0:x0 + ww]; pad[:s.shape[0], :s.shape[1]] = s
            fr.append(reduce(pad, PITCH))
        h, w = fr[0].shape[:2]
        strip = Image.fromarray(np.concatenate(fr, 1), 'RGBA')
        # いろを へらす（32しょく）
        q = strip.convert('RGB').quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(strip.getchannel('A'))
        q.save(f'{D}/{k}.png')
        meta[k] = {'n': COLS, 'w': w, 'h': h, 'ms': 70 if k in ONCE else 100, 'loop': k not in ONCE,
                   'ax': w / 2, 'ay': h - 1 if k in BOTTOM else h / 2}
        print(sh, k, w, h, 'pitch', PITCH)
json.dump(meta, open(f'{D}/meta.json', 'w'), indent=1)
