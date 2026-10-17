# PixelLab で つくった エフェクト（tools/anim/pl_hand）を index.html の PLFX に いれる
#   1れつの よこながの PNG に ならべなおして base64 で うめこむ（コマの 時間は json の duration）
import json, base64, io, os, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, 'tools/anim/pl_hand')
USE_PIXELLAB = ['p_fire', 'p_water', 'p_elec', 'p_ice', 'p_grass', 'p_poison', 'p_psychic', 'p_ghost', 'p_dragon', 'p_fighting', 'p_normal', 'p_bug', 'p_wind', 'p_rock',
       'p_hadou', 'p_moon', 'tornado', 'whirl', 'mine', 'web']
USE = []   # PixelLab 版は しつが ひくいので いまは つかわない（てがきに もどす）
out = {}
G = os.path.join(ROOT, 'tools/anim/gpt_fx'); META = json.load(open(f'{G}/meta.json'))   # ChatGPT 版（tools/anim/gpt_fx.py で つくる）
for k, m in META.items():
    if k == 'fx_ghost': continue   # のこりかげは モンスターの 形で かく（人の 形の 絵は つかわない）
    b = io.BytesIO(); Image.open(f'{G}/{k}.png').save(b, 'PNG', optimize=True)
    out[k] = {'n': m['n'], 'w': m['w'], 'h': m['h'], 'ms': m['ms'], 'ax': m['ax'], 'ay': m['ay'], **({'fb': m['fb']} if 'fb' in m else {}), 'src': 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()}
for k in USE:   # PixelLab 版（いまは つかわない）
    js = json.load(open(f'{D}/{k}.json')); fr = js['frames']; im = Image.open(f'{D}/{k}.png').convert('RGBA')
    w, h = fr[0]['frame']['w'], fr[0]['frame']['h']
    st = Image.new('RGBA', (w * len(fr), h))
    for i, f in enumerate(fr): st.paste(im.crop((f['frame']['x'], f['frame']['y'], f['frame']['x'] + w, f['frame']['y'] + h)), (i * w, 0))
    b = io.BytesIO(); st.save(b, 'PNG', optimize=True)
    out[k] = {'n': len(fr), 'w': w, 'h': h, 'ms': fr[0]['duration'], 'src': 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()}
p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
block = '// ====== PLFX（ChatGPT／PixelLab の エフェクト：tools/anim/build_plfx.py）======\nconst PLFX = ' + json.dumps(out, separators=(',', ':')) + ';\n// ====== ここまで PLFX ======'
if '// ====== PLFX' in s: s = re.sub(r'// ====== PLFX.*?// ====== ここまで PLFX ======', lambda m: block, s, flags=re.S)
else: s = s.replace('// ====== ここまで FXEL ======', '// ====== ここまで FXEL ======\n' + block, 1)
open(p, 'w', encoding='utf-8').write(s); print(len(block), 'bytes')
