#!/usr/bin/env python3
"""ことば（英語・中国語）を index.html に うめこむ。
tools/i18n/dict.json（{ 日本語: [English, 简体中文] }）と tools/i18n/runtime.js から I18N ブロックを つくって、window.__game の まえに 入れる。
つかいかた: python3 tools/i18n/build_i18n.py  （リポジトリの 一番上で）
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
D = json.loads((ROOT / 'tools/i18n/dict.json').read_text(encoding='utf-8'))
rt = (ROOT / 'tools/i18n/runtime.js').read_text(encoding='utf-8').replace('__I18N_DICT__', json.dumps(D, ensure_ascii=False, separators=(',', ':')))
html = (ROOT / 'index.html').read_text(encoding='utf-8')
a, b = '// ====== I18N', '// ====== ここまで I18N ======\n'
if a in html:
    i = html.index(a); j = html.index(b, i) + len(b); html = html[:i] + html[j:]
anchor = 'window.__game = {\n'
assert html.count(anchor) == 1
html = html.replace(anchor, rt + anchor)
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print(len(D), 'entries')
