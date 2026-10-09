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
    # わざの かたち
    'slash': ('斬撃_斬撃', 16), 'claw': ('斬撃_爪', 16), 'dash': ('軌跡_移動_ダッシュ', 16), 'charge': ('爆発_集まる光', 20),
    'flamer': ('炎_火炎放射', 16), 'blizzard': ('氷_水_吹雪', 16), 'magicshot': ('魔法_魔弾', 16),
    # まわり（aoe）
    'aoe_fire': ('炎_炎の輪', 16), 'aoe_ground': ('闇_自然_地割れ', 16), 'aoe_elec': ('雷_雷の結界', 16), 'aoe_water': ('氷_水_渦潮', 16),
    'aoe_ice': ('氷_水_氷柱の輪', 20), 'aoe_psychic': ('魔法_魔法陣', 16), 'aoe_ghost': ('闇_自然_闇の渦', 16), 'shockwave': ('ヒット_衝撃波', 16),
    'slam': ('ヒット_地面たたき', 16), 'aoe_grass': ('闇_自然_キノコの胞子', 16), 'aoe_poison': ('炎_毒の床', 16),
    # 足もと（strike）
    'st_fire': ('炎_火柱', 18), 'st_rock': ('爆発_隕石落下', 24), 'st_ice': ('爆発_氷塊落下', 24), 'st_psychic': ('魔法_光の柱', 20),
    'st_ghost': ('闇_自然_影から出る', 18), 'st_ground': ('闇_自然_地面から出る', 18), 'st_dragon': ('爆発_魔石落下', 24),
    # 補助・状態
    'barrier': ('回復_強化_バリア', 20), 'poof': ('爆発_ポン', 14), 'curse': ('闇_自然_呪い', 18), 'counter': ('ヒット_カウンター', 16),
    'timestop': ('魔法_時間停止', 20), 'speed': ('回復_強化_スピードアップ', 18), 'debuff': ('魔法_拘束', 16),
    'par': ('雷_帯電', 16), 'freeze': ('氷_水_凍結', 18), 'sleep': ('キラキラ_またたき', 16), 'psn': ('闇_自然_毒', 16),
    # 交代・たおれる・つかまえる
    'summon': ('魔法_召喚', 20), 'teleport': ('魔法_テレポート', 18), 'ko': ('爆発_星爆発', 18), 'confetti': ('キラキラ_紙吹雪', 24),
    # ゆか（くりかえし）
    'floor_fire': ('炎_火炎の床', 32), 'floor_poison': ('炎_毒の床', 32), 'floor_elec': ('雷_電撃の床', 32), 'floor_ground': ('闇_自然_砂嵐', 32),
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
