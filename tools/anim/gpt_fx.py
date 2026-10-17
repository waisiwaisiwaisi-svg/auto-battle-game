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
          'H1': ['hit_normal', 'hit_fighting', 'hit_fire', 'hit_water'], 'H2': ['hit_elec', 'hit_grass_old', 'hit_ice', 'hit_poison'],
          'H3': ['hit_ground', 'hit_rock', 'hit_wind', 'hit_bug'], 'H4': ['hit_psychic', 'hit_ghost', 'hit_dragon', 'hit_crit'],
          'X1': ['sum_circle', 'sum_pillar', 'sum_return', 'sum_swap'], 'X2': ['seed_proj', 'seed_root', 'seed_vine', 'seed_drain'],
          'G1': ['g_open', 'g_hold', 'g_hit', 'g_break'], 'G2': ['ctr_aura', 'ctr_strike', 'mirror', 'psn_barrier'],
          'G3': ['dodge', 'parry', 'iron', 'shellpush'],
          # じょうたいの しるし・クリスタル
          'U4': ['st_sleep', 'st_yawn', 'st_dbond', 'st_gravity'], 'U5': ['cap_throw', 'cap_shake', 'cap_caught', 'cap_break'],
          # わざの かべ（ブロック：せりあがり3・完成・ヒビ2）・ステージの 障害物が こわれる
          'W1b': ['wb_rock', 'wb_ice', 'wb_thorn', 'wb_mirror'], 'W2': ['pb_stone', 'pb_bush', 'pb_tree', 'rubble'],
          'W3': ['palm_fly', 'palm_hit', 'palm_charge', 'palm_trail'],
          # とっしん・くさの ヒット（作りなおし：1段目を つかう）
          'D1': ['d_front', 'd_dust', 'd_hit', 'd_lines'], 'D2': ['d_fire', 'd_elec', 'd_water', 'd_dragon'], 'H5': ['hit_grass5', 'hit_grass6', 'hit_grass7', 'hit_grass8'],
          'D3': ['dig_in', 'dig_mound', 'dig_out', 'dig_trail'],
          # コードで かいていた エフェクトの ドット絵（B1・C1〜C6）と タイプの つぶ（P1〜P4：形ちがい 6しゅるい）
          'B1': ['b_upring', 'b_downring', 'b_uparrow', 'b_downarrow'],
          'C1': ['fx_flash', 'fx_impact', 'fx_ring', 'fx_shock'], 'C2': ['fx_pillar', 'fx_ghost', 'fx_beam', 'fx_beamIn'],
          'C3': ['fx_ray', 'fx_blade', 'fx_whip', 'fx_shield'], 'C4': ['fx_glint', 'fx_smoke', 'fx_vortex', 'fx_nail'],
          'C5': ['fx_drain', 'fx_sound', 'fx_swap', 'fx_gust'], 'C6': ['fx_room', 'fx_roots', 'fx_toss', 'fx_rockIn'],
          'P1': ['tp_normal', 'tp_fire', 'tp_water', 'tp_grass'], 'P2': ['tp_elec', 'tp_ice', 'tp_fighting', 'tp_poison'],
          'P3': ['tp_ground', 'tp_wind', 'tp_psychic', 'tp_bug'], 'P4': ['tp_rock', 'tp_ghost', 'tp_dragon']}
HITS = {'hit_' + t for t in ['normal', 'fighting', 'fire', 'water', 'elec', 'grass', 'ice', 'poison', 'ground', 'rock', 'wind', 'bug', 'psychic', 'ghost', 'dragon', 'crit']}
ONCE = {'fist', 'nail', 'skull', 'web', 'brk_rock', 'brk_ice', 'brk_thorn', 'brk_mirror', 'dirt', 'spark', 'reflect', 'wall_rock', 'wall_ice', 'wall_thorn',
        'sum_circle', 'sum_pillar', 'sum_return', 'sum_swap', 'seed_root', 'g_open', 'g_hit', 'g_break', 'ctr_strike', 'dodge', 'parry', 'iron', 'cap_caught', 'cap_break', 'pb_stone', 'pb_bush', 'pb_tree', 'palm_hit', 'palm_trail', 'd_dust', 'd_hit', 'hit_grass5', 'hit_grass6', 'hit_grass7', 'hit_grass8', 'hit_grass_old', 'dig_in', 'dig_out',
        'b_upring', 'b_downring', 'b_uparrow', 'b_downarrow', 'fx_flash', 'fx_impact', 'fx_ring', 'fx_shock', 'fx_pillar', 'fx_ghost', 'fx_beam', 'fx_ray', 'fx_whip', 'fx_shield',
        'fx_glint', 'fx_smoke', 'fx_vortex', 'fx_nail', 'fx_roots', 'fx_toss', 'fx_rockIn'} | HITS
TP = {'tp_' + t for t in ['normal', 'fire', 'water', 'grass', 'elec', 'ice', 'fighting', 'poison', 'ground', 'wind', 'psychic', 'bug', 'rock', 'ghost', 'dragon']}
VAR = TP | {'hole', 'crater', 'scorch', 'rubble', 'dig_trail', 'wb_rock', 'wb_ice', 'wb_thorn', 'wb_mirror'}   # アニメではなく 形ちがい
BOTTOM = {'tornado', 'mine', 'wall_rock', 'wall_ice', 'wall_thorn', 'brk_rock', 'brk_ice', 'brk_thorn', 'brk_mirror', 'hz_rocks', 'hz_spikes', 'hz_tspikes', 'trail', 'dirt', 'sum_pillar', 'seed_root', 'shellpush', 'ctr_aura', 'iron', 'st_gravity', 'wb_rock', 'wb_ice', 'wb_thorn', 'wb_mirror', 'pb_stone', 'pb_bush', 'pb_tree', 'rubble', 'dig_in', 'dig_mound', 'dig_out', 'dig_trail', 'b_upring', 'b_downring', 'fx_pillar', 'fx_roots', 'fx_rockIn'}   # 足もとが きじゅん
# 1つの エフェクトを なんドットに するか（いちばん ながい へん）。ゲームでは 1ドット＝PIX_D で かく
TARGET = {'p_hadou': 22, 'p_moon': 22, 'wave': 40, 'whirl': 36, 'tornado': 30, 'mine': 16, 'fist': 28, 'nail': 24, 'skull': 20, 'web': 30,
          'fl_poison': 48, 'fl_fire': 48, 'fl_elec': 48, 'fl_honey': 48, 'pit': 48, 'pit2': 48, 'snare': 32, 'hole': 30, 'crater': 30, 'scorch': 30,
          'wall_rock': 18, 'wall_ice': 18, 'wall_thorn': 18, 'brk_rock': 18, 'brk_ice': 18, 'brk_thorn': 18, 'brk_mirror': 18,
          'hz_rocks': 14, 'hz_spikes': 14, 'hz_tspikes': 14, 'trail': 14, 'dirt': 24, 'spark': 22, 'reflect': 24,
          **{k: 26 for k in HITS}, 'hit_crit': 32, 'sum_circle': 40, 'sum_pillar': 40, 'sum_return': 30, 'sum_swap': 28,
          'seed_proj': 12, 'seed_root': 22, 'seed_vine': 30, 'seed_drain': 22, 'g_open': 34, 'g_hold': 34, 'g_hit': 36, 'g_break': 36,
          'ctr_aura': 36, 'ctr_strike': 34, 'mirror': 36, 'psn_barrier': 36, 'dodge': 30, 'parry': 28, 'iron': 36, 'shellpush': 30,
          'st_sleep': 16, 'st_yawn': 16, 'st_dbond': 24, 'st_gravity': 40, 'cap_throw': 18, 'cap_shake': 18, 'cap_caught': 22, 'cap_break': 20,
          'wb_rock': 24, 'wb_ice': 24, 'wb_thorn': 24, 'wb_mirror': 24, 'pb_stone': 64, 'pb_bush': 64, 'pb_tree': 64, 'rubble': 56, 'palm_fly': 34, 'palm_hit': 34, 'palm_charge': 30, 'palm_trail': 34,
          'd_front': 30, 'd_dust': 34, 'd_hit': 36, 'd_lines': 40, 'd_fire': 40, 'd_elec': 40, 'd_water': 40, 'd_dragon': 40,
          'hit_grass5': 26, 'hit_grass6': 26, 'hit_grass7': 26, 'hit_grass8': 26,
          'dig_in': 30, 'dig_mound': 26, 'dig_out': 32, 'dig_trail': 24,
          'b_upring': 40, 'b_downring': 40, 'b_uparrow': 20, 'b_downarrow': 20,
          'fx_flash': 28, 'fx_impact': 36, 'fx_ring': 36, 'fx_shock': 44, 'fx_pillar': 40, 'fx_ghost': 32, 'fx_beam': 56, 'fx_beamIn': 56,
          'fx_ray': 56, 'fx_blade': 22, 'fx_whip': 36, 'fx_shield': 40, 'fx_glint': 24, 'fx_smoke': 32, 'fx_vortex': 32, 'fx_nail': 26,
          'fx_drain': 56, 'fx_sound': 32, 'fx_swap': 32, 'fx_gust': 40, 'fx_room': 56, 'fx_roots': 36, 'fx_toss': 48, 'fx_rockIn': 32, **{k: 10 for k in TP}}
TDEF = 20
FIXP = {'P1': 8, 'P2': 8, 'P3': 8, 'P4': 8}   # ドットの 大きさが きまって いる シート（つぶ：もとの 1ドット＝8px）
COLS = 6
GRID = {'G3'}
ROWY = {'D3': [0, 412, 569, 854, 1024]}   # 段の さかいめ（すきまの まんなか）   # マスめの 線が 描かれて いる シート

def comp_cells(a, ROWS):
    # マスわり：絵が ない 列・行の すきまで きる（なければ 等分）
    H, W = a.shape[:2]; op = a[:, :, 3] > 40
    def cuts(prof, n, L):
        out = []
        for k in range(1, n):
            c = L * k // n; lo, hi = c - L // (n * 3), c + L // (n * 3)
            seg = prof[lo:hi]; out.append(lo + int(np.argmin(seg)))
        return [0] + out + [L]
    return cuts(op.sum(0), COLS, W), cuts(op.sum(1), ROWS, H)

CLEAN = {'B1', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'P1', 'P2', 'P3', 'P4'}
def clean(c):
    # となりの 段・コマから はみ出して きた きれはし（マスの ふちに ふれて いて、まんなかが ふちの ちかく）を けす
    from scipy import ndimage
    c = c.copy(); H, W = c.shape[:2]; lab, n = ndimage.label(c[:, :, 3] > 40, structure=np.ones((3, 3)))
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        ys, xs = sl; edge = ys.start == 0 or ys.stop == H or xs.start == 0 or xs.stop == W
        if not edge: continue
        cy, cx = (ys.start + ys.stop) / 2, (xs.start + xs.stop) / 2
        if min(cy, H - cy, cx, W - cx) < min(H, W) * .2: c[lab == i, 3] = 0
    return c

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
    if sh not in GRID: op[:] = False   # マスめの 線が ある シート だけ（ほかは 草むらなどを 線と まちがえる）
    for x in np.where(op.sum(0) > H_ * .9)[0]: a[:, max(0, x - 1):x + 2, 3] = 0
    for y in np.where(op.sum(1) > W_ * .9)[0]: a[max(0, y - 1):y + 2, :, 3] = 0
    ROWS = len(keys)
    xs, ys = comp_cells(a, ROWS) if sh.startswith('E') or sh in ('W1b', 'W2', 'W3', 'D1', 'D2', 'H5') or sh in CLEAN else ([a.shape[1] * i // COLS for i in range(COLS + 1)], [a.shape[0] * i // ROWS for i in range(ROWS + 1)])
    if sh in ROWY: ys = ROWY[sh]   # 段の 高さが そろって いない シート
    for r, k in enumerate(keys):
        cells = [a[ys[r]:ys[r + 1], xs[c]:xs[c + 1]] for c in range(COLS)]
        if sh in CLEAN: cells = [clean(c) for c in cells]
        # 6コマ ぶんの 絵の はんいを あわせる（コマごとに ずれない ように）
        bb = [np.argwhere(c[:, :, 3] > 40) for c in cells]
        y0 = min(b[:, 0].min() for b in bb if len(b)); y1 = max(b[:, 0].max() for b in bb if len(b)) + 1
        x0 = min(b[:, 1].min() for b in bb if len(b)); x1 = max(b[:, 1].max() for b in bb if len(b)) + 1
        PITCH = FIXP.get(sh) or max(2, round(max(y1 - y0, x1 - x0) / TARGET.get(k, TDEF)))
        hh, ww = y1 - y0, x1 - x0; hh += (-hh) % PITCH; ww += (-ww) % PITCH
        fr = []
        for c in cells:
            pad = np.zeros((hh, ww, 4), np.uint8); s = c[y0:y0 + hh, x0:x0 + ww]; pad[:s.shape[0], :s.shape[1]] = s
            fr.append(reduce(pad, PITCH) if sh.startswith('E') else reduce_soft(pad, PITCH))
        if k in TP: fr = [x for x in fr if (x[..., 3] > 0).sum() >= 4]   # つぶ：からっぽの コマ（小さすぎて きえた もの）は のぞく
        h, w = fr[0].shape[:2]
        strip = Image.fromarray(np.concatenate(fr, 1), 'RGBA')
        # いろを へらす（32しょく）
        q = strip.convert('RGB').quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB'); q.putalpha(strip.getchannel('A'))
        q.save(f'{D}/{k}.png')
        meta[k] = {'n': len(fr), 'w': w, 'h': h, 'ms': 70 if k in ONCE else 100, 'loop': k not in ONCE and k not in VAR, 'var': k in VAR,
                   'ax': w / 2, 'ay': h - 1 if k in BOTTOM else h / 2}
        print(sh, k, w, h, 'pitch', PITCH)
json.dump(meta, open(f'{D}/meta.json', 'w'), indent=1)
