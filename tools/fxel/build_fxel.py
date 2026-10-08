# FXEL（https://takayustudio.jp/fxel/ ・作成物は商用利用OK）で 書き出した ドットの スプライトシート（48px×32コマ、8列）を
# うごいている コマだけ 切りだして よこ一列に ならべ、index.html の「FXEL」区間に 書きこむ
#   python3 tools/fxel/build_fxel.py
import base64, io, json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); GAME = os.path.join(HERE, '..', '..', 'index.html')
BEGIN, END = '// ====== FXEL（tools/fxel/build_fxel.py が 自動生成）======', '// ====== ここまで FXEL ======'
# ゲームの キー → FXEL の サンプル（src の ファイル名）, 最大コマ数
USE = {
    'normal': ('ヒット_ヒット', 20), 'fighting': ('ヒット_火花', 14), 'crit': ('ヒット_クリティカル', 20),
    'fire': ('爆発_小爆発', 16), 'water': ('氷_水_水しぶき', 18), 'ice': ('ヒット_ヒット_氷', 16), 'elec': ('雷_落雷', 16),
    'grass': ('闇_自然_木の葉', 16), 'poison': ('ヒット_はじける毒', 18), 'ground': ('爆発_ブロック崩し_土', 18), 'rock': ('闇_自然_岩槍', 18),
    'ghost': ('ヒット_ヒット_闇', 16), 'psychic': ('ヒット_はじける魔力', 18), 'dragon': ('ヒット_ヒット_六角', 16), 'wind': ('闇_自然_竜巻', 16),
    'bug': ('闇_自然_種', 16), 'boom': ('爆発_爆発', 20), 'heal': ('回復_強化_回復', 20), 'buff': ('回復_強化_強化', 20),
}
out = {}
for k, (fn, mx) in USE.items():
    im = Image.open(os.path.join(HERE, 'src', fn + '.png')).convert('RGBA')
    fr = [im.crop(((i % 8) * 48, (i // 8) * 48, (i % 8) * 48 + 48, (i // 8) * 48 + 48)) for i in range(32)]
    on = [bool(x.getbbox()) for x in fr]; a = on.index(True); b = a
    while b + 1 < 32 and b + 1 - a < mx and any(on[b + 1:b + 4]): b += 1   # はじめに うごいている ひとつづき（2コマまでの すきまは つなぐ）
    use = fr[a:b + 1]; S = Image.new('RGBA', (48 * len(use), 48))
    for i, x in enumerate(use): S.paste(x, (i * 48, 0))
    buf = io.BytesIO(); S.save(buf, 'PNG', optimize=True)
    out[k] = {'n': len(use), 'src': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()}
    print(k, fn, len(use), len(buf.getvalue()))
js = BEGIN + '\n// FXEL で 作った ドットの エフェクト（48×48 の コマを よこに ならべた もの）\nconst FXEL = %s;\nfor (const k in FXEL) { const im = new Image(); im.src = FXEL[k].src; FXEL[k].img = im; }\n' % json.dumps(out, separators=(',', ':')) + END
src = open(GAME, encoding='utf-8').read()
if BEGIN in src: i = src.index(BEGIN); j = src.index(END) + len(END); src = src[:i] + js + src[j:]
else: k = src.index('const FX_STYLE = {'); src = src[:k] + js + '\n' + src[k:]
open(GAME, 'w', encoding='utf-8').write(src)
