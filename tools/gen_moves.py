"""ランキング上位100技（PokéAPI のデータで確認済み）をゲーム用データに変換して index.html に埋め込む。
- tools/top100-moves.json : 技の元データ（タイプ・威力・命中・優先度・追加効果）
- DESIGN : リアルタイム戦闘での形（k）と名前。名前はオリジナル。
命中率が100未満の技は「方向・範囲を指定する技」（追尾しない）にして、よける余地を作る。
"""
import json, sys, re, csv, os

HERE = os.path.dirname(__file__)
src = json.load(open(os.path.join(HERE, 'top100-moves.json'), encoding='utf-8'))

# id: (なまえ, 形, 追加パラメータ)
D = {
 'earthquake': ('グランドショック', 'aoe', {'rad': 110}),
 'stealth-rock': ('うかびいし', 'hazard', {'hz': 'rocks'}),
 'taunt': ('あおりたてる', 'ray', {'sp': 'taunt'}),
 'swords-dance': ('とうしのまい', 'self', {}),
 'protect': ('ガードシェル', 'protect', {}),
 'will-o-wisp': ('ひとだまび', 'proj', {'spd': 190, 'r': 9}),
 'close-combat': ('ぜんりょくラッシュ', 'dash', {'len': 150}),
 'flamethrower': ('フレイムブレス', 'beam', {'len': 300, 'wid': 34}),
 'knock-off': ('ひっぱたき', 'melee', {}),
 'encore': ('くりかえしコール', 'ray', {'sp': 'encore'}),
 'calm-mind': ('せいしんとういつ', 'self', {}),
 'u-turn': ('ヒットアンドアウェイ', 'dash', {'len': 170, 'switchOut': 1}),
 'shadow-ball': ('やみだま', 'proj', {'spd': 260, 'r': 11, 'homing': 1.2}),
 'yawn': ('ねむけさそい', 'ray', {'sp': 'yawn'}),
 'ice-beam': ('フロストレイ', 'beam', {'len': 330, 'wid': 22}),
 'sucker-punch': ('だしぬき', 'dash', {'len': 190, 'sucker': 1}),
 'substitute': ('デコイにんぎょう', 'sub', {}),
 'body-press': ('こうらおし', 'dash', {'len': 140, 'useDef': 1}),
 'psychic': ('ねんどうは', 'strike', {'rad': 55}),
 'thunderbolt': ('ハイボルト', 'proj', {'spd': 480, 'r': 8, 'homing': 2}),
 'iron-defense': ('アイアンウォール', 'self', {}),
 'ice-punch': ('こおりのこぶし', 'melee', {}),
 'foul-play': ('てのひらがえし', 'melee', {'useFoeAtk': 1}),
 'volt-switch': ('スパークターン', 'proj', {'spd': 420, 'r': 8, 'homing': 1.5, 'switchOut': 1}),
 'poison-jab': ('ポイズンスタブ', 'melee', {}),
 'focus-blast': ('きはくだん', 'proj', {'spd': 230, 'r': 15}),
 'earth-power': ('ちみゃくのいかり', 'strike', {'rad': 58}),
 'nasty-plot': ('くろいたくらみ', 'self', {}),
 'dazzling-gleam': ('きらめきフラッシュ', 'aoe', {'rad': 100}),
 'stone-edge': ('いわのきっさき', 'beam', {'len': 280, 'wid': 30, 'crit': 1, 'look': 'spikes'}),
 'rock-slide': ('がけくずれ', 'multi', {'rad': 40, 'pattern': 'fan'}),
 'surf': ('ビッグウェーブ', 'aoe', {'rad': 130}),
 'toxic': ('もうどくのしずく', 'proj', {'spd': 230, 'r': 9}),
 'drain-punch': ('すいとりナックル', 'melee', {}),
 'leech-seed': ('きせいのタネ', 'proj', {'spd': 210, 'r': 7}),
 'roost': ('つばさやすめ', 'heal', {}),
 'destiny-bond': ('もろとも', 'dbond', {}),
 'fake-out': ('びっくりてうち', 'dash', {'len': 200, 'fakeout': 1}),
 'giga-drain': ('いのちすい', 'beam', {'len': 260, 'wid': 26}),
 'trick-room': ('さかさまフィールド', 'field', {'fld': 'trickroom'}),
 'rock-tomb': ('いわのおり', 'strike', {'rad': 48}),
 'draco-meteor': ('スターフォール', 'multi', {'rad': 42, 'pattern': 'around'}),
 'mirror-coat': ('はんしゃのまく', 'counter', {'ctr': 'spec', 'mult': 2}),
 'overheat': ('オーバーバーン', 'beam', {'len': 300, 'wid': 44}),
 'dragon-dance': ('てんりゅうのまい', 'self', {}),
 'thunder-punch': ('いなずまパンチ', 'melee', {}),
 'aqua-jet': ('みずのダッシュ', 'dash', {'len': 200}),
 'flash-cannon': ('はがねのほうだん', 'beam', {'len': 320, 'wid': 26}),
 'flare-blitz': ('もえさかるとっしん', 'dash', {'len': 220}),
 'iron-head': ('てつのずつき', 'dash', {'len': 160}),
 'dragon-pulse': ('ドラゴンウェーブ', 'proj', {'spd': 300, 'r': 12, 'homing': 1}),
 'trick': ('いれかえのじゅつ', 'ray', {'sp': 'trick'}),
 'sludge-wave': ('どくのおおなみ', 'aoe', {'rad': 115}),
 'thunder-wave': ('しびれでんぱ', 'proj', {'spd': 360, 'r': 7}),
 'baton-pass': ('うけわたし', 'baton', {}),
 'hyper-voice': ('だいおんせい', 'aoe', {'rad': 115}),
 'quick-attack': ('すばやいいちげき', 'dash', {'len': 200}),
 'recover': ('さいせい', 'heal', {}),
 'ice-shard': ('ひょうのつぶ', 'proj', {'spd': 420, 'r': 6, 'homing': 1.5}),
 'flip-turn': ('すいりゅうターン', 'dash', {'len': 170, 'switchOut': 1}),
 'ice-fang': ('ひょうがのキバ', 'swipe', {'rad': 64}),
 'icy-wind': ('こがらし', 'cone', {'rad': 200, 'half': .5}),
 'dark-pulse': ('やみのなみ', 'aoe', {'rad': 105}),
 'crunch': ('がぶりかみ', 'melee', {}),
 'rapid-spin': ('スピンはらい', 'melee', {'rapidSpin': 1}),
 'psychic-noise': ('ねんぱノイズ', 'proj', {'spd': 300, 'r': 9, 'homing': 1.2, 'healBlock': 1}),
 'draining-kiss': ('すいとりキッス', 'proj', {'spd': 240, 'r': 8, 'homing': 1.5}),
 'bulk-up': ('きんにくきたえ', 'self', {}),
 'fissure': ('だいちのさけめ', 'beam', {'len': 380, 'wid': 20, 'ohko': 1, 'look': 'crack'}),
 'play-rough': ('じゃれあそび', 'swipe', {'rad': 66}),
 'fire-blast': ('だいかえん', 'proj', {'spd': 240, 'r': 18}),
 'hydro-pump': ('すいりゅうほう', 'beam', {'len': 360, 'wid': 34}),
 'body-slam': ('おしつぶし', 'dash', {'len': 160}),
 'gunk-shot': ('どくのかたまり', 'proj', {'spd': 240, 'r': 15}),
 'sludge-bomb': ('どくだま', 'proj', {'spd': 260, 'r': 11, 'homing': 1}),
 'liquidation': ('みずのいちげき', 'melee', {}),
 'toxic-spikes': ('どくのトゲ', 'hazard', {'hz': 'tspikes'}),
 'tailwind': ('せなかのかぜ', 'field', {'fld': 'tailwind'}),
 'curse': ('のろいのぎしき', 'curse', {}),
 'blizzard': ('ブリザード', 'cone', {'rad': 220, 'half': .55}),
 'moonblast': ('つきのちから', 'proj', {'spd': 260, 'r': 12, 'homing': 1}),
 'aura-sphere': ('きこうだん', 'proj', {'spd': 250, 'r': 11, 'homing': 4}),
 'roar': ('とおぼえ', 'ray', {'sp': 'roar'}),
 'triple-axel': ('さんれんスピン', 'swipe', {'rad': 64, 'hits': 3}),
 'energy-ball': ('しぜんのたま', 'proj', {'spd': 260, 'r': 11, 'homing': 1}),
 'metal-burst': ('はがねのしかえし', 'counter', {'ctr': 'any', 'mult': 1.5}),
 'synthesis': ('ひかりのめぐみ', 'heal', {}),
 'psyshock': ('ねんりきだん', 'proj', {'spd': 280, 'r': 9, 'homing': 1.2, 'hitDef': 1}),
 'alluring-voice': ('まどわしのうた', 'aoe', {'rad': 110, 'confuseIfBoosted': 1}),
 'rock-blast': ('いしつぶてれんぱつ', 'proj', {'spd': 330, 'r': 9, 'burst': [2, 5]}),
 'shadow-sneak': ('かげのいちげき', 'strike', {'rad': 30}),
 'poltergeist': ('さわぐかげ', 'strike', {'rad': 50}),
 'leaf-storm': ('このはあらし', 'cone', {'rad': 240, 'half': .45}),
 'freeze-dry': ('しゅんかんとうけつ', 'beam', {'len': 300, 'wid': 24, 'superVsWater': 1}),
 'outrage': ('りゅうのあばれ', 'dash', {'len': 180, 'rampage': 1}),
 'spikes': ('トゲまき', 'hazard', {'hz': 'spikes'}),
 'flame-charge': ('ほのおのダッシュ', 'dash', {'len': 180}),
 'air-slash': ('そらのやいば', 'proj', {'spd': 360, 'r': 10}),
 'brave-bird': ('すてみのはばたき', 'dash', {'len': 230}),
 'slack-off': ('ごろりやすみ', 'heal', {}),
}
assert len(D) == 100, len(D)

TYPE_MAP = {'electric': 'elec', 'flying': 'wind'}
# 初代の 15タイプだけを 使う（あく・はがね・フェアリーは なし）。その タイプの わざは 初代らしい タイプへ
GEN1_DROP = ('dark', 'steel', 'fairy')
GEN1_MOVE = {'taunt': 'normal', 'knock-off': 'normal', 'sucker-punch': 'normal', 'foul-play': 'normal', 'crunch': 'normal',
             'nasty-plot': 'psychic', 'dark-pulse': 'ghost', 'iron-defense': 'normal', 'flash-cannon': 'normal', 'iron-head': 'rock',
             'metal-burst': 'fighting', 'dazzling-gleam': 'psychic', 'draining-kiss': 'grass', 'play-rough': 'normal',
             'moonblast': 'psychic', 'alluring-voice': 'psychic'}
STAT = {'attack': 'atk', 'defense': 'def', 'special-attack': 'spa', 'special-defense': 'spd', 'speed': 'spe'}
AIL = {'burn': 'brn', 'paralysis': 'par', 'poison': 'psn', 'freeze': 'frz'}
SELF_DROP = {'close-combat', 'draco-meteor', 'overheat', 'leaf-storm'}
WIND = {'proj': .3, 'beam': .55, 'strike': .7, 'aoe': .6, 'dash': .35, 'melee': .15, 'swipe': .3, 'cone': .55, 'multi': .75,
        'ray': .3, 'self': .3, 'heal': .4, 'field': .4, 'hazard': .4, 'protect': .03, 'counter': .03, 'sub': .3, 'dbond': .2, 'curse': .4, 'baton': .2}
CD = {'self': 6, 'heal': 9, 'protect': 3.5, 'hazard': 7, 'field': 14, 'ray': 7, 'counter': 5, 'sub': 9, 'dbond': 8, 'curse': 7, 'baton': 6}

out = {}
for o in src:
    mid = o['id']; name, k, p = D[mid]
    t = TYPE_MAP.get(o['type'], o['type'])
    t = GEN1_MOVE.get(mid, t)
    cat = {'physical': 'phys', 'special': 'spec', 'status': 'stat'}[o['dmg']]
    acc = o['acc']  # 0 = 必中（または命中判定なし）
    m = {'n': name, 'ref': mid, 't': t, 'cat': cat, 'k': k, 'power': o['power'], 'acc': acc, 'prio': o['prio']}
    m.update(p)
    # 命中100未満 → 方向・範囲指定（追尾なし）。100/必中 → 相手をねらう（追尾あり）
    m['aim'] = 'dir' if 0 < acc < 100 else 'lock'
    if m['aim'] == 'dir': m.pop('homing', None)
    w = WIND[k]
    if m['aim'] == 'dir': w += (100 - acc) * .012
    if o['prio'] > 0: w = .06
    if mid == 'fissure': w = 1.4
    m['wind'] = round(w, 3)
    if cat == 'stat': m['cd'] = CD.get(k, 7)
    elif o['prio'] > 0: m['cd'] = 2.2
    else: m['cd'] = round(1.4 + o['power'] / 32, 2)
    if mid == 'fissure': m['cd'] = 12
    m['pow'] = round(o['power'] * .2, 1)
    e = {}
    if o['ailment'] in AIL and o['ailment_chance'] > 0: e['st'] = AIL[o['ailment']]; e['stCh'] = o['ailment_chance']
    if mid == 'will-o-wisp': e['st'], e['stCh'] = 'brn', 100
    if mid == 'thunder-wave': e['st'], e['stCh'] = 'par', 100
    if mid == 'toxic': e['st'], e['stCh'] = 'tox', 100
    if mid == 'leech-seed': e['seed'] = 1
    if mid == 'fake-out': e['flinch'] = 100
    elif o['flinch']: e['flinch'] = o['flinch']
    if mid == 'ice-fang': e['flinch'] = 10
    if o['drain'] > 0: e['drain'] = o['drain']
    if o['drain'] < 0: e['recoil'] = -o['drain']
    if o['healing'] > 0: e['heal'] = o['healing']
    if o['stats']:
        ch = {STAT[s]: v for s, v in o['stats']}
        if cat == 'stat' or mid in SELF_DROP or all(v > 0 for v in ch.values()): e['self'] = ch
        else: e['foe'] = ch; e['foeCh'] = o['stat_chance'] or 100
    if mid == 'curse': e.pop('self', None)
    m['e'] = e
    out[mid] = m

# 18タイプのあいしょう（PokéAPI type_efficacy）
csvdir = sys.argv[2] if len(sys.argv) > 2 else None
chart = {}
if csvdir:
    T = {r['id']: TYPE_MAP.get(r['identifier'], r['identifier']) for r in csv.DictReader(open(os.path.join(csvdir, 'types.csv')))}
    for r in csv.DictReader(open(os.path.join(csvdir, 'type_efficacy.csv'))):
        a, b, f = T[r['damage_type_id']], T[r['target_type_id']], int(r['damage_factor'])
        if a in ('stellar', 'shadow', 'unknown') or b in ('stellar', 'shadow', 'unknown'): continue
        if f != 100: chart.setdefault(a, {})[b] = f / 100
    json.dump(chart, open(os.path.join(HERE, 'type-chart.json'), 'w'), indent=0)
else:
    chart = json.load(open(os.path.join(HERE, 'type-chart.json')))

chart = {a: {b: f for b, f in r.items() if b not in GEN1_DROP} for a, r in chart.items() if a not in GEN1_DROP}
js = '/* ---- ここから自動生成（tools/gen_moves.py）---- */\n'
js += 'const CHART = ' + json.dumps(chart, ensure_ascii=False, separators=(',', ':')) + ';\n'
js += 'const MOVES100 = {\n' + ',\n'.join(f'  {json.dumps(k)}: ' + json.dumps(v, ensure_ascii=False, separators=(", ", ": ")) for k, v in out.items()) + '\n};\n'
js += '/* ---- ここまで自動生成 ---- */\n'

html = open(sys.argv[1], encoding='utf-8').read()
pat = re.compile(r'/\* ---- ここから自動生成.*?ここまで自動生成 ---- \*/\n', re.S)
if pat.search(html): html = pat.sub(lambda _: js, html)
else: html = html.replace('/* ==MOVES100== */\n', js)
open(sys.argv[1], 'w', encoding='utf-8').write(html)
print('ok', len(out), 'moves; types', len(chart))

# 対応表（docs/moves.md）
KIND_JA = {'proj': 'とびどうぐ', 'beam': 'ちょくせん', 'aoe': 'じぶんの周囲', 'strike': 'あいての足元', 'dash': 'とっしん', 'melee': 'せっきん', 'swipe': '前方おうぎ（近）', 'cone': '前方おうぎ（遠）', 'multi': '複数の範囲', 'ray': '補助（相手）', 'self': '補助（自分）', 'heal': '回復', 'protect': 'まもる', 'sub': 'デコイ', 'dbond': 'みちづれ', 'counter': 'カウンター', 'curse': 'のろい', 'field': '場', 'hazard': '設置', 'baton': '交代'}
rows = ['# わざ一覧（ランキング上位100）', '',
        '元データ：PChamp DB「技使用率一覧」（上位100件。全角の重複1件をまとめ、存在しない1件は除外して101位を採用）。',
        'わざの内容（タイプ・威力・命中・優先度・追加効果）は PokéAPI のデータで確認しています。ゲーム内の名前はオリジナルです。',
        '', '**命中100未満の わざ（◎）は相手を自動で狙わず、方向・範囲を指定する技**として実装しています（予兆の間に動けば避けられる。命中が低いほど予兆が長い）。',
        '', '| # | ゲーム内の名前 | 参考にした技 | タイプ | 分類 | 威力 | 命中 | 形 | 狙い |', '|---|---|---|---|---|---|---|---|---|']
for i, o in enumerate(src):
    m = out[o['id']]
    rows.append(f"| {i+1} | {m['n']} | {o['ja']} | {m['t']} | {m['cat']} | {o['power'] or '—'} | {o['acc'] or '—'} | {KIND_JA[m['k']]} | {'◎ 方向・範囲' if m['aim'] == 'dir' else '相手'} |")
os.makedirs(os.path.join(HERE, '..', 'docs'), exist_ok=True)
open(os.path.join(HERE, '..', 'docs', 'moves.md'), 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
