# all.json と aispr.js を index.html に 入れる（何度でも 実行できる）
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, '..', '..', 'index.html')
data = json.load(open(os.path.join(HERE, 'all.json')))
js = open(os.path.join(HERE, 'aispr.js')).read()
lines = ',\n'.join(f'  {k}: {json.dumps(v, separators=(",", ":"))}' for k, v in data.items())
end = '// ====== ここまで AISPR ======'
js = js.replace(end, f'Object.assign(AISpr.DATA, {{\n{lines},\n}});\n{end}')
s = open(IDX).read()
a = s.find('// ====== ここから AISPR')
if a >= 0:
    b = s.index(end) + len(end) + 1
    s = s[:a] + js + s[b:]
else:
    m = '// ====== ここまで HANDPIX ======\n'
    s = s.replace(m, m + js, 1)
open(IDX, 'w').write(s)
print('spliced', list(data))
