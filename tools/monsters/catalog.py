# モンスター図鑑ページ（catalog.html）を 作る：各フォルダの sprite.json と SETTEI.md を 1枚に まとめる
# 使い方: python3 tools/monsters/catalog.py  → tools/monsters/catalog.html
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = {'normal': ('ノーマル', '#d8d0c0'), 'fire': ('ほのお', '#ff8a3d'), 'water': ('みず', '#4aa8ff'), 'grass': ('くさ', '#62d26f'), 'elec': ('でんき', '#ffd84a'),
         'ice': ('こおり', '#9fe8ff'), 'fighting': ('かくとう', '#e0704a'), 'poison': ('どく', '#b86ad8'), 'ground': ('じめん', '#d8b060'), 'wind': ('かぜ', '#a6ece6'),
         'psychic': ('エスパー', '#ff7ab0'), 'bug': ('むし', '#a8c840'), 'rock': ('いわ', '#c49a6c'), 'ghost': ('ゴースト', '#8a78c8'), 'dragon': ('ドラゴン', '#7a6aff'),
         'dark': ('あく', '#8a7060'), 'steel': ('はがね', '#b8c0d0'), 'fairy': ('フェアリー', '#ffb0e0')}

def md(text):
    """SETTEI.md の かんたんな 変換（見出し・表・箇条書き・太字）"""
    out, rows, lst = [], [], []
    def flush():
        nonlocal rows, lst
        if rows:
            body = ''.join('<tr><th>%s</th><td>%s</td></tr>' % (inline(a), inline(b)) for a, b in rows if a.strip() not in ('項目', '---'))
            out.append('<table>%s</table>' % body); rows = []
        if lst: out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(x) for x in lst)); lst = []
    def inline(s): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(s.strip()))
    for line in text.splitlines():
        if line.startswith('# '): flush(); continue
        if line.startswith('## '): flush(); out.append('<h4>%s</h4>' % inline(line[3:])); continue
        if line.startswith('|'):
            cells = [c for c in line.strip().strip('|').split('|')]
            if len(cells) >= 2 and not set(cells[0].strip()) <= set('-'): rows.append((cells[0], '|'.join(cells[1:])))
            continue
        if line.startswith('- '): lst.append(line[2:]); continue
        flush()
        if line.strip(): out.append('<p>%s</p>' % inline(line))
    flush()
    return ''.join(out)

mons = []
for d in sorted(os.listdir(HERE)):
    p = os.path.join(HERE, d, 'sprite.json')
    if not os.path.isfile(p): continue
    s = json.load(open(p))
    meta = s.get('meta', {})
    settei = open(os.path.join(HERE, d, 'SETTEI.md')).read() if os.path.isfile(os.path.join(HERE, d, 'SETTEI.md')) else ''
    mons.append({'id': d, 'name': meta.get('name', d), 'types': meta.get('types', []), 'base': meta.get('base', ''), 'size': meta.get('size', ''),
                 'w': s['w'], 'h': s['h'], 'pal': s['pal'], 'f': s['f'], 'doc': md(settei)})
# 図鑑の 並び：ROSTER.md の 番号順
order = re.findall(r'^\| (\d+) \| (\w+) \|', open(os.path.join(HERE, 'ROSTER.md')).read(), re.M)
rank = {i: int(n) for n, i in order}
mons.sort(key=lambda m: rank.get(m['id'], 999))
for m in mons: m['no'] = rank.get(m['id'], 0)

tpl = open(os.path.join(HERE, '_lib', 'catalog_tpl.html')).read()
page = tpl.replace('/*DATA*/null', json.dumps(mons, ensure_ascii=False, separators=(',', ':'))).replace('/*TYPES*/null', json.dumps(TYPES, ensure_ascii=False))
open(os.path.join(HERE, 'catalog.html'), 'w').write(page)
print('catalog', len(mons), 'monsters', len(page) // 1024, 'KB')
