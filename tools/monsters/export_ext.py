# 外部の 絵（他の AIの シートから 切りだした もの）を ゲームに 入れる
# 使い方: python3 tools/monsters/export_ext.py   （_ext/sprites.json と _ext/meta.json → index.html の EXTMON 区間）
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_game as E
HERE = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = '// ====== EXTMON（tools/monsters/export_ext.py が 自動生成）======', '// ====== ここまで EXTMON ======'
spr = json.load(open(os.path.join(HERE, '_ext', 'sprites.json'))); meta = json.load(open(os.path.join(HERE, '_ext', 'meta.json')))
# 図鑑で「不採用」に なった ものは 入れない／第3弾（_ext3）の 不採用 以外を 足す
import math
REJ = set(json.load(open(os.path.join(HERE, '_ext', 'rejected.json')))) if os.path.exists(os.path.join(HERE, '_ext', 'rejected.json')) else set()
sys.path.insert(0, os.path.join(HERE, '_ext3')); from table import TABLE
c_spr = json.load(open(os.path.join(HERE, '_ext3', 'all.json')))
for line in TABLE.strip().splitlines():
    k, name, t2, base, body, h, wt, home, note, trait = line.split('|')
    if k in REJ: continue
    t = k[2:].rstrip('0123456789'); num = int(k[2 + len(t):]); h = float(h)
    u = min(1, max(0, (math.log10(h) - math.log10(.25)) / (math.log10(4) - math.log10(.25)))); sz = round(.72 + .72 * u, 3)
    meta[k] = {'name': name, 'types': [t] + ([t2] if t2 != '-' else []), 'base': base, 'body': body, 'size': 'S' if h < .7 else 'M' if h < 1.8 else 'L',
               'note': note, 'rare': 1 if num == 10 else 0, 'h': h, 'wt': float(wt), 'home': home, 'trait': trait, 'evo': None, 'sz': sz}
    v = c_spr[k]; spr[k] = {'w': v['w'], 'h': v['h'], 'pal': v['pal'], 'd': v['d'], 'ms': round(88 * sz / max(v['w'], v['h']), 3)}
meta = {k: m for k, m in meta.items() if k not in REJ}
for m in meta.values():
    if m.get('evo') and m['evo'] not in meta: m['evo'] = None
species, learn = {}, {}
for i, m in meta.items():
    r = dict(m, no=0)
    L = E.learnset(i, r)
    species[i] = {'n': m['name'], 'type': m['types'][0], **({'type2': m['types'][1]} if len(m['types']) > 1 else {}),
                  'base': E.stats(i, r), 'moves': [x for _, x in L[:2]], 'style': E.style(r),
                  'catch': {'S': .5, 'M': .4, 'L': .3}[m['size']], 'rare': m.get('rare', 0), 'desc': m['note'] + '。（もと：' + m['base'] + '）', 'ext': 1, **({'fly': 1} if m.get('body') == 'F' else {}),
                  **({'prof': {'h': m['h'], 'wt': m['wt'], 'home': m['home'], 'trait': m['trait'], 'evo': m.get('evo')}, 'sz': m['sz']} if 'h' in m else {})}
    learn[i] = L
js = BEGIN + '\n// 他の AIで 作った 絵（%d体）。絵は 1枚 → AISpr の 変形で 14コマ（fx:1 ＝ 左向きの 絵を 反転して 右向きに）\n' % len(meta)
js += 'Object.assign(AISpr.DATA, %s);\nObject.assign(SPECIES, %s);\nObject.assign(LEARN, %s);\n' % (
    json.dumps({k: {**spr[k], 'fx': 1} for k in meta}, ensure_ascii=False, separators=(',', ':')), json.dumps(species, ensure_ascii=False, separators=(',', ':')),
    json.dumps(learn, ensure_ascii=False, separators=(',', ':'))) + END
src = open(E.GAME).read()
if BEGIN in src: a = src.index(BEGIN); b = src.index(END) + len(END); src = src[:a] + js + src[b:]
else: k = src.index('// ====== ここまで HANDMON ======') + len('// ====== ここまで HANDMON ======'); src = src[:k] + '\n' + js + src[k:]
open(E.GAME, 'w').write(src); print('extmon', len(meta), len(js) // 1024, 'KB')
