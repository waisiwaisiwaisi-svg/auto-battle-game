# ChatGPT に つくってもらった エフェクトの シート（横6コマ×縦4段）を ドットに もどして コマに きる
# usage: python3 tools/anim/gpt_fx.py   → tools/anim/gpt_fx/<key>.png（よこ 1れつ）と meta.json
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'gpt_fx')
SHEETS = {'E1': ['p_fire', 'p_water', 'p_elec', 'p_ice'], 'E2': ['p_grass', 'p_poison', 'p_psychic', 'p_ghost'],
          'E3': ['p_dragon', 'p_fighting', 'p_normal', 'p_bug'], 'E4': ['p_wind', 'p_rock', 'p_hadou', 'p_moon'],
          'E5': ['wave', 'whirl', 'tornado', 'mine'], 'E6': ['fist', 'nail', 'skull', 'web'],
          # じめん・かべ
          'E7': ['fl_poison', 'fl_fire', 'fl_elec', 'fl_honey'], 'E8': ['wall_rock', 'wall_ice', 'wall_thorn', 'pit'],
          'E9': ['hz_rocks', 'hz_spikes', 'hz_tspikes', 'snare'], 'E10': ['hole', 'crater', 'scorch', 'trail'],
          'E11': ['brk_rock', 'brk_ice', 'brk_thorn', 'brk_mirror'], 'E12': ['pit2', 'dirt', 'spark', 'reflect'],
          # ヒット・よびだし・ヤドリギ・ガード
          'H1': ['hit_normal', 'hit_fighting', 'hit_fire', 'hit_water'], 'H2': ['hit_elec', 'hit_grass', 'hit_ice', 'hit_poison'],
          'H3': ['hit_ground', 'hit_rock', 'hit_wind', 'hit_bug'], 'H4': ['hit_psychic', 'hit_ghost', 'hit_dragon', 'hit_crit'],
          'X1': ['sum_circle', 'sum_pillar', 'sum_return', 'sum_swap'], 'X2': ['seed_proj', 'seed_root', 'seed_vine', 'seed_drain'],
          'G1': ['g_open', 'g_hold', 'g_hit', 'g_break'], 'G2': ['ctr_aura', 'ctr_strike', 'mirror', 'psn_barrier'],
          'G3': ['dodge', 'parry', 'iron', 'shellpush']}
HITS = {'hit_' + t for t in ['normal', 'fighting', 'fire', 'water', 'elec', 'grass', 'ice', 'poison', 'ground', 'rock', 'wind', 'bug', 'psychic', 'ghost', 'dragon', 'crit']}
ONCE = {'fist', 'nail', 'skull', 'web', 'brk_rock', 'brk_ice', 'brk_thorn', 'brk_mirror', 'dirt', 'spark', 'reflect', 'wall_rock', 'wall_ice', 'wall_thorn',
        'sum_circle', 'sum_pillar', 'sum_return', 'sum_swap', 'seed_root', 'g_open', 'g_hit', 'g_break', 'ctr_strike', 'dodge', 'parry', 'iron'} | HITS
VAR = {'hole', 'crater', 'scorch'}   # アニメではなく 形ちがい
BOTTOM = {'tornado', 'mine', 'wall_rock', 'wall_ice', 'wall_thorn', 'brk_rock', 'brk_ice', 'brk_thorn', 'brk_mirror', 'hz_rocks', 'hz_spikes', 'hz_tspikes', 'trail', 'dirt', 'sum_pillar', 'seed_root', 'shellpush', 'ctr_aura', 'iron'}   # 足もとが きじゅん
# 1つの エフェクトを なんドットに するか（いちばん ながい へん）。ゲームでは 1ドット＝PIX_D で かく
TARGET = {'p_hadou': 22, 'p_moon': 22, 'wave': 40, 'whirl': 36, 'tornado': 30, 'mine': 16, 'fist': 28, 'nail': 24, 'skull': 20, 'web': 30,
          'fl_poison': 48, 'fl_fire': 48, 'fl_elec': 48, 'fl_honey': 48, 'pit': 48, 'pit2': 48, 'snare': 32, 'hole': 30, 'crater': 30, 'scorch': 30,
          'wall_rock': 18, 'wall_ice': 18, 'wall_thorn': 18, 'brk_rock': 18, 'brk_ice': 18, 'brk_thorn': 18, 'brk_mirror': 18,
          'hz_rocks': 14, 'hz_spikes': 14, 'hz_tspikes': 14, 'trail': 14, 'dirt': 24, 'spark': 22, 'reflect': 24,
          **{k: 26 for k in HITS}, 'hit_crit': 32, 'sum_circle': 40, 'sum_pillar': 40, 'sum_return': 30, 'sum_swap': 28,
          'seed_proj': 12, 'seed_root': 22, 'seed_vine': 30, 'seed_drain': 22, 'g_open': 34, 'g_hold': 34, 'g_hit': 36, 'g_break': 36,
          'ctr_aura': 36, 'ctr_strike': 34, 'mirror': 36, 'psn_barrier': 36, 'dodge': 30, 'parry': 28, 'iron': 36, 'shellpush': 30}
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

def reduce_soft(c, PITCH):
    # すけた エフェクト（ガラス・ひかり）よう：ブロックの 平均の こさを 3だんかいで のこす
    h, w = c.shape[0] // PITCH, c.shape[1] // PITCH
    b = c[:h * PITCH, :w * PITCH].reshape(h, PITCH, w, PITCH, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, PITCH * PITCH, 4).astype(np.float32)
    al = b[..., 3]; ma = al.mean(-1); out = np.zeros((h, w, 4), np.uint8)
    for y in range(h):
        for x in range(w):
            if ma[y, x] < 34: continue
            m = al[y, x] > 60
            if not m.any(): m = al[y, x] > 0
            out[y, x, :3] = np.median(b[y, x][m][:, :3], 0)
            out[y, x, 3] = 255 if ma[y, x] > 170 else 190 if ma[y, x] > 95 else 120
    return out

# python3 gpt_fx.py H1 H2 …：その シートだけ つくりなおす（ほかは meta.json の まま。ゆかは あとで たいらに してある）
ONLY = sys.argv[1:]
meta = json.load(open(f'{D}/meta.json')) if ONLY else {}
for sh, keys in SHEETS.items():
    if ONLY and sh not in ONLY: continue
    a = np.array(Image.open(f'{D}/src/{sh}.png').convert('RGBA'))
    # マスめの 線（ずっと つづく 列・行）を けす
    op = a[:, :, 3] > 40; H_, W_ = op.shape
    for x in np.where(op.sum(0) > H_ * .9)[0]: a[:, max(0, x - 1):x + 2, 3] = 0
    for y in np.where(op.sum(1) > W_ * .9)[0]: a[max(0, y - 1):y + 2, :, 3] = 0
    xs, ys = comp_cells(a) if sh.startswith('E') else ([a.shape[1] * i // COLS for i in range(COLS + 1)], [a.shape[0] * i // ROWS for i in range(ROWS + 1)])
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
            fr.append(reduce(pad, PITCH) if sh.startswith('E') else reduce_soft(pad, PITCH))
        h, w = fr[0].shape[:2]
        strip = Image.fromarray(np.concatenate(fr, 1), 'RGBA')
        # いろを へらす（32しょく）
        q = strip.convert('RGB').quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(strip.getchannel('A'))
        q.save(f'{D}/{k}.png')
        meta[k] = {'n': COLS, 'w': w, 'h': h, 'ms': 70 if k in ONCE else 100, 'loop': k not in ONCE and k not in VAR, 'var': k in VAR,
                   'ax': w / 2, 'ay': h - 1 if k in BOTTOM else h / 2}
        print(sh, k, w, h, 'pitch', PITCH)
json.dump(meta, open(f'{D}/meta.json', 'w'), indent=1)
