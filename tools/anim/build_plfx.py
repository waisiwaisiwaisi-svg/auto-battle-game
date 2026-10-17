# ChatGPT に つくって もらった エフェクト（tools/anim/gpt_fx）を index.html の PLFX に いれる
#   1れつの よこながの PNG に ならべなおして base64 で うめこむ（コマの 時間は json の duration）
import json, base64, io, os, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out = {}
G = os.path.join(ROOT, 'tools/anim/gpt_fx'); META = json.load(open(f'{G}/meta.json'))   # ChatGPT 版（tools/anim/gpt_fx.py で つくる）
for k, m in META.items():
    if k == 'fx_ghost': continue   # のこりかげは モンスターの 形で かく（人の 形の 絵は つかわない）
    b = io.BytesIO(); Image.open(f'{G}/{k}.png').save(b, 'PNG', optimize=True)
    out[k] = {'n': m['n'], 'w': m['w'], 'h': m['h'], 'ms': m['ms'], 'ax': m['ax'], 'ay': m['ay'], **({'fb': m['fb']} if 'fb' in m else {}), 'src': 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()}
p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf-8').read()
block = '// ====== PLFX（ChatGPT の エフェクト：tools/anim/build_plfx.py）======\nconst PLFX = ' + json.dumps(out, separators=(',', ':')) + ';\n// ====== ここまで PLFX ======'
if '// ====== PLFX' in s: s = re.sub(r'// ====== PLFX.*?// ====== ここまで PLFX ======', lambda m: block, s, flags=re.S)
else: s = s.replace('// ====== ここまで FXEL ======', '// ====== ここまで FXEL ======\n' + block, 1)
open(p, 'w', encoding='utf-8').write(s); print(len(block), 'bytes')
