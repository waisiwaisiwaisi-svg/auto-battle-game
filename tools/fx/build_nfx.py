#!/usr/bin/env python3
"""effects/ の 納品エフェクトを index.html の NFX ブロックに うめこむ。
NFX の キーは PLFX と おなじ 名前（同じ キーは 上書き）＋ 新しい キー（a_charge_* など）。
つかいかた: python3 tools/fx/build_nfx.py  （リポジトリの 一番上で）
"""
import base64, io, json, re, struct, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FX = ROOT / 'effects'
TYPES = ['normal', 'fire', 'water', 'grass', 'elec', 'ice', 'fighting', 'poison', 'ground', 'wind', 'psychic', 'bug', 'rock', 'ghost', 'dragon']

def png(im):
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def sheet(path, n, ms, ax=None, ay=None, frames=None):
    im = Image.open(path).convert('RGBA'); w = im.width // n; h = im.height
    if frames is not None:   # コマを ぬきだす
        out = Image.new('RGBA', (w * len(frames), h))
        for i, f in enumerate(frames): out.paste(im.crop((f * w, 0, f * w + w, h)), (i * w, 0))
        im, n = out, len(frames)
    return {'n': n, 'w': w, 'h': h, 'ms': ms, 'ax': w / 2 if ax is None else ax, 'ay': h / 2 if ay is None else ay, 'src': png(im)}

def f(name): return next(FX.glob('*/' + name + '_*f.png'))
def nf(p): return int(re.search(r'_(\d+)f\.png$', p.name).group(1))

out = {}
def add(key, name, ms, **kw):
    p = f(name); out[key] = sheet(p, nf(p), ms, **kw)

for t in TYPES:
    add('p_' + t, 'A_shot_' + t, 100)            # とぶ たま（みぎむき）
    add('hit_' + t, 'A_hit_' + t, 70)            # あたった しゅんかん
    add('a_charge_' + t, 'A_charge_' + t, 100)   # ため（くりかえし）
    p = f('A_burst_' + t); out['a_burst_' + t] = sheet(p, nf(p), 80, ay=47)   # あしもとの ばくはつ：下の まんなかが きじゅん
add('fx_beam', 'B_beam_body', 70, ax=0)
add('n_beam_start', 'B_beam_start', 70)
add('n_beam_tip', 'B_beam_tip', 70)
add('n_fan', 'B_fan', 70, ax=0)                  # おうぎ：口もと（ひだりはし）が きじゅん
add('fx_shock', 'B_ring', 70)
add('n_slash', 'B_slash', 70)
add('fist', 'B_fist', 70)
add('n_heal', 'B_heal', 80)
p = f('B_up'); out['n_up'] = sheet(p, nf(p), 80, ay=47)
p = f('B_down'); out['n_down'] = sheet(p, nf(p), 80, ay=47)
add('g_open', 'B_shield_on', 70)
p = f('B_shield_on'); out['g_hold'] = sheet(p, nf(p), 100, frames=[nf(p) - 1])   # はりつづける あいだは さいごの コマ
add('g_hit', 'B_shield_hit', 70)
add('hit_crit', 'D_crit', 70)
add('dodge', 'D_dodge', 70)
add('parry', 'D_parry', 70)
add('n_ko', 'D_down', 90)
add('sum_swap', 'D_switch', 70)
add('sum_return', 'D_switch', 70)
add('cap_throw', 'D_orb_throw', 100)
add('cap_shake', 'D_orb_shake', 100)
add('cap_caught', 'D_capture_ok', 80)
add('cap_break', 'D_capture_ng', 70)
add('n_capin', 'D_capture_in', 75)
# ---- 優先度B（2回目の 納品）----
add('wave', 'B_bigwave', 100)                    # 大波（白い 絵を 水の 色に）
add('n_claw', 'B_claw', 70)
add('d_hit', 'B_dash_hit', 70)
add('d_dust', 'B_dash_trail', 70)
add('n_field', 'B_field', 120)                   # 床（専用の 絵が ない タイプ）
add('g_break', 'B_shield_break', 70)
add('tornado', 'B_tornado', 90)
p = f('B_wall_break'); out['n_wall_break'] = sheet(p, nf(p), 80, ay=63)
p = f('B_wall_up'); out['n_wall_up'] = sheet(p, nf(p), 70, ay=63)
add('n_warp', 'B_warp', 70)
add('n_st_brn', 'C_burn', 120); add('n_st_par', 'C_par', 120); add('n_st_psn', 'C_psn', 140); add('n_st_slp', 'C_slp', 160)
add('n_frz', 'C_frz', 140)
add('pb_bush', 'D_break_bush', 80)
add('pb_stone', 'D_break_stone', 80)
add('n_guardbreak', 'D_guardbreak', 70)
add('n_ambush_blink', 'E_ambush_blink', 60)
add('n_ambush', 'E_ambush_stance', 100)
p = f('E_fly_land'); out['n_fly_land'] = sheet(p, nf(p), 70, ay=40)
p = f('E_fly_up'); out['n_fly_up'] = sheet(p, nf(p), 70, ay=40)
add('n_leaves', 'E_leaf_storm', 90)
add('n_roar', 'E_roar', 70, ax=4)
p = f('E_shadow_strike'); out['n_shadow'] = sheet(p, nf(p), 70, ay=44)
# ---- 4回目の 納品 ----
add('n_dive_wind', 'B_dive_wind', 80); add('n_dive_dragon', 'B_dive_dragon', 80)   # 落下攻撃：体を かくす
add('n_roll', 'B_roll', 70)                      # ごろごろアタック：体を かくす 玉
add('n_dbreath', 'E_dragon_breath', 70, ax=0)   # りゅうのためいき（口もとが きじゅん）
p = f('E_stone_edge'); out['n_stone_edge'] = sheet(p, nf(p), 70, ay=46)   # いわのきっさき系：地面から つきでる 岩

# ---- Gグループ（大技の 専用）：キーは g_ ＋ なまえ ----
BOTTOM = {'bolt', 'thunder', 'future_pillar', 'starfall_hit', 'shadow_hands', 'sludge_hit', 'earth_rift', 'rock_blade', 'flame_vortex'}
for p in sorted(FX.glob('G/G_*_*f.png')):
    nm = re.sub(r'^G_|_\d+f\.png$', '', p.name); n = nf(p)
    kw = {}
    if nm in BOTTOM: kw['ay'] = Image.open(p).height - 2
    if nm.endswith('_body') or nm == 'psy_thread': kw['ax'] = 0
    if nm == 'dragon_head': kw['ax'] = Image.open(p).width // n * .7
    out['g_' + nm] = sheet(p, n, 90 if nm.endswith(('_body', 'thread', 'idle', 'mark')) else 75, **kw)
# ---- アイコン（UIA に 上書き・追加）----
UI = {}
def icons(name, keys):
    p = next(FX.glob('F/' + name + '.png')); im = Image.open(p).convert('RGBA'); n = len(keys); w = im.width // n
    for i, k in enumerate(keys):
        if k: UI[k] = {'w': w, 'h': im.height, 'src': png(im.crop((i * w, 0, i * w + w, im.height)))}
# icons('F_tab_5', ['ic_tab_shop', 'ic_tab_team', 'ic_tab_home', 'ic_tab_train', 'ic_tab_guild'])
# icons('F_homebtn_7', ['ic_help', 'ic_book', 'ic_chart', 'rotate', 'spk_on', 'spk_off', 'ic_gear'])
# icons('F_mode_5', ['ic_mode_online', 'ic_flag', 'ic_mode_cup', 'ic_bush', 'ic_globe'])
# icons('F_resource_4', ['ic_trophy', 'ic_res_orb', 'ic_gem', 'ic_res_chest'])
icons('F_emblem_3', ['emb_sword', 'emb_bow', 'emb_shield'])
uijs = '// ====== NUI（effects/F の 納品アイコン：tools/fx/build_nfx.py が 自動生成。UIA の おなじ キーは 上書き）======\nObject.assign(UIA, ' + json.dumps(UI, separators=(',', ':')) + ');\n// ====== ここまで NUI ======\n'
js = '// ====== NFX（effects/ の 納品エフェクト：tools/fx/build_nfx.py が 自動生成。PLFX の おなじ キーは 上書き）======\nconst NFX = ' + json.dumps(out, separators=(',', ':')) + ';\nObject.assign(PLFX, NFX);\n// ====== ここまで NFX ======\n'
html = (ROOT / 'index.html').read_text(encoding='utf-8')
html = re.sub(r'// ====== NFX.*?// ====== ここまで NFX ======\n', '', html, flags=re.S)
html = re.sub(r'// ====== NUI.*?// ====== ここまで NUI ======\n', '', html, flags=re.S)
anchor = '// ====== ここまで PLFX ======\n'
assert html.count(anchor) == 1
html = html.replace(anchor, anchor + js)
ua = 'UIA.emb_bow = {'   # 古い 弓の 紋章の すぐ あと（UIA の 定義の あと）に 入れる
i = html.index(ua); i = html.index('\n', i) + 1
html = html[:i] + uijs + html[i:]
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print(len(out), 'sheets,', len(js) // 1024, 'KB')
