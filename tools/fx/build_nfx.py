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

js = '// ====== NFX（effects/ の 納品エフェクト：tools/fx/build_nfx.py が 自動生成。PLFX の おなじ キーは 上書き）======\nconst NFX = ' + json.dumps(out, separators=(',', ':')) + ';\nObject.assign(PLFX, NFX);\n// ====== ここまで NFX ======\n'
html = (ROOT / 'index.html').read_text(encoding='utf-8')
html = re.sub(r'// ====== NFX.*?// ====== ここまで NFX ======\n', '', html, flags=re.S)
anchor = '// ====== ここまで PLFX ======\n'
assert html.count(anchor) == 1
html = html.replace(anchor, anchor + js)
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print(len(out), 'sheets,', len(js) // 1024, 'KB')
