# ゲームに 入っている 200体の 図鑑ページ（dex.html）を 作る
# 使い方: python3 tools/monsters/_ext/dex_page.py  → tools/monsters/dex.html
import base64, io, json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
AL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
TYPES = {'normal': ('ノーマル', '#d8d0c0'), 'fire': ('ほのお', '#ff8a3d'), 'water': ('みず', '#4aa8ff'), 'grass': ('くさ', '#62d26f'),
         'elec': ('でんき', '#ffd84a'), 'ice': ('こおり', '#9fe8ff'), 'fighting': ('かくとう', '#e0704a'), 'poison': ('どく', '#b86ad8'),
         'ground': ('じめん', '#d8b060'), 'wind': ('かぜ', '#a6ece6'), 'psychic': ('エスパー', '#ff7ab0'), 'bug': ('むし', '#a8c840'),
         'rock': ('いわ', '#c49a6c'), 'ghost': ('ゴースト', '#8a78c8'), 'dragon': ('ドラゴン', '#7a6aff')}
ORDER = ['fire', 'water', 'grass', 'elec', 'ice', 'fighting', 'poison', 'ground', 'wind', 'dragon', 'ghost']

def png(sp, flip=True):
    w, h = sp['w'], sp['h']; pal = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in sp['pal']]
    flat = []; d = sp['d']
    for i in range(0, len(d), 3): flat += [AL.index(d[i])] * int(d[i + 1:i + 3], 36)
    im = Image.new('RGBA', (w, h))
    for k, c in enumerate(flat[:w * h]):
        if c: im.putpixel((k % w, k // w), pal[c - 1] + (255,))
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)   # ゲームと 同じ 右向き
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def main():
    meta = json.load(open(os.path.join(HERE, 'meta.json'))); spr = json.load(open(os.path.join(HERE, 'sprites.json')))
    ids = sorted(meta, key=lambda k: (ORDER.index(meta[k]['types'][0]), meta[k]['h']))
    pre = {}
    for k, m in meta.items():
        if m.get('evo'): pre[m['evo']] = k
    rows = []
    for no, k in enumerate(ids, 1):
        m = meta[k]; s = spr[k]
        rows.append({'no': no, 'id': k, 'n': m['name'], 't': m['types'], 'h': m['h'], 'wt': m['wt'], 'home': m['home'], 'trait': m['trait'],
                     'note': m['note'], 'base': m['base'], 'evo': m.get('evo'), 'pre': pre.get(k), 'fly': m['body'] == 'F', 'rare': m.get('rare', 0),
                     'sz': m['sz'], 'w': s['w'], 'hh': s['h'], 'img': png(s), 'game': 1})
    # 第3弾（_ext3）：図鑑だけ。採用されたら ゲームへ
    import math, sys
    sys.path.insert(0, os.path.join(HERE, '..', '_ext3')); from table import TABLE
    c_spr = json.load(open(os.path.join(HERE, '..', '_ext3', 'all.json')))
    T3 = {'fire': 'fire', 'water': 'water', 'grass': 'grass', 'elec': 'elec', 'ice': 'ice', 'fighting': 'fighting', 'poison': 'poison', 'ground': 'ground', 'wind': 'wind', 'dragon': 'dragon'}
    no = len(rows)
    for line in TABLE.strip().splitlines():
        k, name, t2, base, body, h, wt, home, note, trait = line.split('|')
        t = k[2:].rstrip('0123456789'); num = int(k[2 + len(t):]); s = c_spr[k]; h = float(h)
        u = min(1, max(0, (math.log10(h) - math.log10(.25)) / (math.log10(4) - math.log10(.25))))
        no += 1
        rows.append({'no': no, 'id': k, 'n': name, 't': [T3[t]] + ([t2] if t2 != '-' else []), 'h': h, 'wt': float(wt), 'home': home, 'trait': trait,
                     'note': note, 'base': base, 'evo': None, 'pre': None, 'fly': body == 'F', 'rare': 1 if num == 10 else 0,
                     'sz': round(.72 + .72 * u, 3), 'w': s['w'], 'hh': s['h'], 'img': png(s, False), 'game': 0, 'batch': 3})
    tpl = open(os.path.join(HERE, 'dex_tpl.html')).read()
    out = tpl.replace('/*DATA*/', json.dumps(rows, ensure_ascii=False, separators=(',', ':'))).replace('/*TYPES*/', json.dumps(TYPES, ensure_ascii=False))
    dst = os.path.join(HERE, '..', 'dex.html'); open(dst, 'w').write(out)
    print(len(rows), 'monsters', len(out) // 1024, 'KB ->', os.path.normpath(dst))

if __name__ == '__main__':
    main()
