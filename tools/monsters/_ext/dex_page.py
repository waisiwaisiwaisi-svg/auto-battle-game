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

def png(sp):
    w, h = sp['w'], sp['h']; pal = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in sp['pal']]
    flat = []; d = sp['d']
    for i in range(0, len(d), 3): flat += [AL.index(d[i])] * int(d[i + 1:i + 3], 36)
    im = Image.new('RGBA', (w, h))
    for k, c in enumerate(flat[:w * h]):
        if c: im.putpixel((k % w, k // w), pal[c - 1] + (255,))
    im = im.transpose(Image.FLIP_LEFT_RIGHT)   # ゲームと 同じ 右向き
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
                     'sz': m['sz'], 'w': s['w'], 'hh': s['h'], 'img': png(s)})
    tpl = open(os.path.join(HERE, 'dex_tpl.html')).read()
    out = tpl.replace('/*DATA*/', json.dumps(rows, ensure_ascii=False, separators=(',', ':'))).replace('/*TYPES*/', json.dumps(TYPES, ensure_ascii=False))
    dst = os.path.join(HERE, '..', 'dex.html'); open(dst, 'w').write(out)
    print(len(rows), 'monsters', len(out) // 1024, 'KB ->', os.path.normpath(dst))

if __name__ == '__main__':
    main()
