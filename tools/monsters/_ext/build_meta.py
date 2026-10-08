# 切りだした 絵（all.json）に 名前・タイプ・説明を つけて ゲーム用の sprites.json / meta.json を 作る
# 使い方: python3 build_meta.py && python3 ../export_ext.py
import json, math
from lore import load as load_lore
LORE = load_lore()
ROW = {'fire': 'fire', 'water': 'water', 'grass': 'grass', 'elec': 'elec', 'ice': 'ice', 'fighting': 'fighting',
       'poison': 'poison', 'ground': 'ground', 'wind': 'wind', 'dragon': 'dragon'}
# 前から 入っている 10体は id を そのまま（セーブが 消えないように）
KEEP = {'b_fire3': 'kamadon', 'b_water2': 'pottoko', 'b_ice4': 'hyoukyuu', 'b_ice7': 'yukidome', 'b_poison1': 'furasukon',
        'b_ground2': 'shoberaa', 'b_wind9': 'sorabune', 'g3': 'noroinui', 'g4': 'kitsunemen', 'g7': 'medamasho'}
# 有名な キャラクターに 似すぎている ものは 入れない
SKIP = {'a_elec1', 'b_elec1', 'b_elec5', 'a_ground1', 'b_water1', 'b_grass5'}
# シートの 番号 | 名前 | 2つめの タイプ | もと | 体型 | ひとこと（大きさは 番号で きまる：1〜3=S 4〜8=M 9〜10=L、10番は レア）
TABLE = '''
a_fire1|コギツネビ|normal|子ギツネ|Q|しっぽの 先に 小さな 火が ともる 子ギツネ
a_fire2|ヒバシリ|-|リス|Q|火の しっぽを 立てて すばしっこく 走りまわる
a_fire3|ホノライ|-|ライオンの 子|Q|燃える たてがみが 生えはじめた 子ライオン
a_fire4|ヒノトリ|wind|火の鳥|F|羽ばたくたびに 火の粉が 舞う
a_fire5|ボッコ|-|火の 小鬼|B|まんまるの 体から 炎が ふきだす
a_fire6|エンジュウ|dark|けもの|Q|黒い 角と 赤い 毛並み。口から 熱い けむりを はく
a_fire7|マグマグマ|rock|クマ|B|溶岩の 毛皮を まとった 大グマ
a_fire8|ホムラギツネ|-|キツネ|Q|三つに 分かれた 炎の しっぽで 敵を まどわす
a_fire9|クロホムラ|dark|オオカミ|Q|黒い 体に 燃える たてがみ。夜の 山を かける
a_fire10|エンリュウオウ|dragon|火竜|F|翼を ひろげると 空が 赤く そまる 炎の 竜
a_water1|アザラコ|normal|アザラシの 子|W|白黒の ふわふわ。水に うかんで ねむる
a_water2|ナミリュー|-|首長竜の 子|S|長い 首で 波の 上を すべる
a_water3|ペンギーノ|ice|ペンギン|B|胸を はって よちよち 歩く。泳ぐと 速い
a_water4|クラゲリン|poison|クラゲ|W|光る かさと 長い 足。さわると ピリッと しびれる
a_water5|サメット|-|サメ|W|小さいけれど するどい 歯で かみつく
a_water6|アオチビ|-|水の 小竜|B|頭の ひれを ふって 水しぶきを とばす
a_water7|ウミヘビオ|dragon|ウミヘビ|S|渦を まいて 船を まきこむ
a_water8|カメッポ|rock|カメ|Q|岩の ような 甲羅に こもって 身を 守る
a_water9|キバザメ|dark|サメ|W|大きな 口で なんでも かみくだく
a_water10|ワダツミ|dragon|海竜|F|海の 底から 現れる 青い 竜。嵐を 呼ぶ
a_grass1|ハッパネコ|-|ネコ|Q|葉っぱの 耳を ぴくぴく 動かす 子ネコ
a_grass2|コノハジカ|-|子ジカ|Q|若葉の 角が 生えた 子ジカ
a_grass3|ハナコロ|fairy|花の 精|B|頭の 花から あまい かおりを 出す
a_grass4|モリガメ|rock|カメ|Q|背中の 森に 小鳥が すむ のんびり ガメ
a_grass5|ハナビラン|fairy|花|P|花びらを くるくる 回して 飛ばす
a_grass6|ツタヘビ|-|ヘビ|S|ツタに まぎれて えものを 待つ
a_grass7|コケゴリラ|fighting|ゴリラ|B|全身 コケだらけ。太い 腕で 木を ひっこぬく
a_grass8|ハッパドリ|wind|オウム|F|葉っぱの 翼で 森の 上を すべる
a_grass9|モリジカ|-|シカ|Q|大きな 枝角に つるが からむ 森の 番人
a_grass10|シンリンオウ|dragon|白いシカ＋竜|Q|森の 奥に すむ 王。つるの 竜を したがえる
a_elec2|デンヒヨ|normal|ヒヨコ|B|ふくらんだ 羽毛に 静電気を ためる
a_elec3|イナズマイヌ|-|イヌ|Q|イナズマ形の しっぽで 電気を はなつ
a_elec4|エレキュウ|steel|電気の たま|W|まるい 体の 輪っかが 光って 回る
a_elec5|ライバット|wind|コウモリ|F|雷雲の 中を 飛びまわる
a_elec6|ライギツネ|-|キツネ|Q|しっぽの 先から 火花が ちる
a_elec7|イナビカリ|-|シカ|Q|長い 足で 稲妻の ように かける
a_elec8|ゴロビリ|rock|コガネムシ|Q|黒い 殻に 電気を ためて 転がる
a_elec9|ライジュウガ|dark|ヒョウ|Q|黒と 金の しま模様。雷の 速さで とびかかる
a_elec10|テンライオウ|dragon|雷獣|Q|全身から 稲妻を はなつ 雷の 王
a_ice1|コオリギツネ|-|子ギツネ|Q|冷たい 息で 草を 白く 凍らせる
a_ice2|ツララグマ|-|クマ|B|背中に つららが 生えた 白い クマ
a_ice3|シロクマル|-|シロクマの 子|B|雪の 上で ころころ 転がって あそぶ
a_ice4|コウテイペン|water|ペンギン|B|氷の 海を まっすぐ 泳ぐ ペンギン
a_ice5|ユキウサ|fairy|ウサギ|Q|長い 耳で 雪の 音を 聞きわける
a_ice6|ヒョウチョウ|wind|鳥|F|氷の 羽を きらきら ちらして 飛ぶ
a_ice7|イエティオ|fighting|雪男|B|大きな 体で 雪山を 守る
a_ice8|ショウケツネ|-|キツネ|Q|背中の 氷の とげを 逆立てて おこる
a_ice9|ユキマンモ|ground|マンモス|Q|分厚い 毛皮と 雪の ずきん
a_ice10|スイショウバ|fairy|天馬|Q|水晶の 翼を もつ 天馬。ふれた ものを 凍らせる
a_fighting1|ケンザル|-|サル|B|小さな こぶしで 毎日 修行する
a_fighting2|ゴリラッシュ|-|ゴリラ|B|胸を たたいて 突進する
a_fighting3|ホノケン|fire|サル|B|燃える こぶしの 拳法家
a_fighting4|クマボクサ|-|クマ|B|重い パンチで 岩を くだく
a_fighting5|レッサパン|-|レッサーパンダ|B|身軽な けりわざが 得意
a_fighting6|パンダイ|dark|パンダ|B|目つきの 悪い 力自慢
a_fighting7|ベニザル|-|サル|B|赤い 毛並みの すばやい 拳士
a_fighting8|シシケンポー|fire|獅子|B|獅子の 頭を もつ 拳法の 達人
a_fighting9|ツノバッファ|ground|バイソン|Q|大きな 角で 何でも はねとばす
a_fighting10|オニゴリラ|dark|鬼＋ゴリラ|B|ツノの ある 赤い 大ザル。地面を なぐって 割る
a_poison1|ドクネコ|dark|ネコ|Q|しっぽの 先に 毒の しずく
a_poison2|ドクヘビ|-|ヘビ|S|紫の うろこ。かまれると しびれる
a_poison3|ヤドクトカゲ|-|トカゲ|Q|あざやかな 色は 毒の しるし
a_poison4|ウイルスン|-|ウイルス|W|とげとげの 体で ふわふわ ただよう
a_poison5|ドクバット|wind|コウモリ|F|夜に 毒の 粉を まきちらす
a_poison7|ドクイカ|water|イカ|W|毒の すみを はく
a_poison8|ドクガエル|grass|カエル|Q|苔の 背中に 毒の いぼ
a_poison9|ドクリュウ|dragon|竜|F|毒の 息を はく 紫の 竜
a_poison10|オニタケ|grass|キノコ|P|大きな かさから 毒の 胞子を ふらせる
a_ground2|イワコロ|rock|アルマジロ|Q|岩の 甲羅で 丸まって 転がる
a_ground3|イノシシン|-|イノシシ|Q|まっすぐ 突進して 地面を えぐる
a_ground5|サイロック|rock|サイ|Q|岩の よろいを 着た サイ
a_ground6|ドロゴーレム|rock|ゴーレム|B|泥と 石で できた 体。ゆっくり だが 力持ち
a_ground7|スナヘビ|-|ヘビ|S|砂の 中を 泳ぐ ように 進む
a_ground8|サソリン|poison|サソリ|M|オレンジの ハサミと 毒の しっぽ
a_ground9|サバクガメ|-|リクガメ|Q|砂漠を 何日も 歩きつづける
a_ground10|ガンセキオウ|rock|岩の 獣|Q|山の ような 体。ふみしめると 地面が ゆれる
a_wind1|ヒヨッコ|normal|ヒヨコ|F|まだ うまく 飛べない 小鳥
a_wind2|ツバメット|-|ツバメ|F|風を きって 低く 飛ぶ
a_wind3|アカツバサ|fire|赤い鳥|F|夕焼け色の 羽で 熱い 風を おこす
a_wind4|フクロン|dark|フクロウ|F|夜の 森を 音も なく 飛ぶ
a_wind6|オウムン|-|オウム|F|聞いた 声を まねして 敵を まどわす
a_wind7|ペリカーン|water|ペリカン|F|大きな くちばしで 水ごと すくう
a_wind8|ヨルコウモリ|dark|コウモリ|F|月の 夜に むれで 飛ぶ
a_wind9|イヌワシオウ|fighting|ワシ|F|するどい 爪で 急降下する
a_wind10|ハクリュウ|dragon|白い竜|F|雲の 上に すむ 白い 竜。羽ばたきで 竜巻を 起こす
a_dragon1|チビドラ|-|竜の 子|B|まだ 小さい 竜の 子。火も 吹けない
a_dragon2|アオドラ|water|竜の 子|B|青い うろこの 元気な 子竜
a_dragon3|ミズチ|water|水の 竜|S|川に すむ 竜。とぐろを まいて ねむる
a_dragon4|シデンリュウ|poison|竜|F|紫の 翼で 毒の 風を 起こす
a_dragon6|ミドリュウ|grass|竜|F|森の 竜。翼の まくは 葉っぱ もよう
a_dragon7|キンリュウ|ground|金の竜|S|金色の うろこで 光を はねかえす
a_dragon8|ヤミドラゴ|dark|竜|F|闇に まぎれて 空から おそう
a_dragon9|ベニリュウ|fire|竜|F|赤い 翼から 熱風を はなつ
a_dragon10|ハクギンリュウ|ice|白銀の竜|F|白銀の うろこ。ふぶきを まとう 竜の 王
b_fire1|ロウソッピ|-|ロウソク|B|頭の 火が 消えると しょんぼり する
b_fire2|タイマツネ|-|キツネ＋たいまつ|Q|しっぽの たいまつで 夜道を 照らす
b_fire3|カマドン|rock|かまど|Q|石を 積んだ かまどの 体。おなかの 火で なんでも 焼く
b_fire4|ヒバトリ|wind|火の鳥|F|炎の 羽を ひろげて 舞う
b_fire5|ツボビ|steel|火の つぼ|W|つぼの 中で 炎が ぐつぐつ 燃える
b_fire6|ホノサンショ|-|サンショウウオ|Q|背中の 炎が 消えないように 雨を さける
b_fire7|ヒノタマン|ghost|火の玉|W|ゆらゆら ゆれる 生きた 炎
b_fire8|チョウチン|ghost|ちょうちん|F|祭りの 夜に ふわりと 浮かぶ
b_fire9|ホノイノシ|ground|イノシシ|Q|燃える 背中で 突っ込んでくる
b_fire10|マグマジン|rock|溶岩の 巨人|B|ひびから 溶岩が あふれる 巨人
b_water2|ポットコ|normal|ティーポット＋タコ|W|ティーポットの 頭を もつ タコ。注ぎ口から 熱い お茶を 飛ばす
b_water3|ミズクラゲ|poison|クラゲ|W|すきとおった 体で 波に ゆられる
b_water4|センスイギョ|steel|潜水艦＋魚|W|深い 海を 探検する 鉄の 魚
b_water5|チョウチンアンコ|elec|アンコウ|W|頭の あかりで えものを さそう
b_water6|イルカン|-|イルカ|W|水から 高く とびあがって あそぶ
b_water7|アワボウ|fairy|あわの 精|B|あわを ぷかぷか 浮かべて 遊ぶ
b_water8|タツノコン|-|タツノオトシゴ|S|しっぽで 海草に つかまって 休む
b_water9|サンゴガメ|rock|カメ＋サンゴ|Q|背中に サンゴの 島を のせた 大ガメ
b_water10|ミズビン|-|水の びん|W|びんの 中の 水が 体。ふたを とると あふれだす
b_grass1|メバエ|-|ふたば|P|頭の ふたばで 日の光を あびる
b_grass2|ヒマワリン|-|ヒマワリ|P|いつも 太陽の ほうを 向いて いる
b_grass3|キボック|-|木|P|年を とった 木に 顔が 生まれた
b_grass4|ハナサキ|fairy|花|P|大きな 花で 虫を 呼びよせる
b_grass6|ツルリュウ|dragon|つるの 竜|S|つるが よりあつまって 竜の 形に なった
b_grass7|トマトガブ|dark|トマト|P|まっかな 実に するどい 歯
b_grass8|ワカバジカ|-|シカ|Q|若葉の 角で 春を 告げる
b_grass9|ハナウサギ|fairy|ウサギ|Q|花の 冠を つけた ウサギ
b_grass10|タイボクオウ|ground|大木|P|千年 生きた 大木。根で 大地を ゆらす
b_elec2|ビリザル|dark|サル|Q|長い しっぽの 先から 電気を とばす
b_elec3|ライジャ|-|ヘビ|S|雷の もようの ヘビ
b_elec4|デンフクロウ|wind|フクロウ|F|大きな 目が 電球の ように 光る
b_elec6|イカヅチネコ|dark|ネコ|Q|毛を 逆立てると 火花が ちる
b_elec7|デンチボット|steel|電池|B|体の 電池で なんでも 動かす ロボ
b_elec8|ライカマキリ|bug|カマキリ|M|雷の カマで 切りさく
b_elec9|スパークボム|steel|機雷|W|さわると バチッと はじける
b_elec10|イカヅチジュウ|dark|雷獣|Q|黒い 毛並みに 金の 稲妻。吠えると 雷が おちる
b_ice1|ユキダルン|-|雪だるま|B|冬の あいだだけ 動きだす 雪だるま
b_ice2|ヒョウロウ|-|オオカミ|Q|氷の たてがみを もつ オオカミ
b_ice3|ユキウサギ|-|ウサギ|Q|まっしろな 毛で 雪に とけこむ
b_ice4|ヒョウキュー|normal|氷の キューブ|Q|四角い 氷の 体。冷たい 角で 体当たりする
b_ice5|ペンギンヌ|water|ペンギン|B|おなかで 氷の 上を すべる
b_ice6|トナカイス|-|トナカイ|Q|氷の 角で 吹雪を 切りひらく
b_ice7|ユキドーム|fairy|スノードーム|W|ガラスの 中に 小さな 家と 雪景色。ふると 吹雪が 起きる
b_ice8|コオリチョウ|fairy|チョウ|F|氷の はねを もつ チョウ
b_ice9|セイウチャン|water|セイウチ|Q|大きな きばで 氷を 割る
b_ice10|ヒョウショウジュウ|rock|氷の 獣|Q|全身が 氷の 結晶で できた 獣
b_fighting1|モクジン|-|木人|B|修行の 相手を して いるうちに 動きだした
b_fighting2|レッサーボクサ|-|レッサーパンダ|B|赤い グローブで 連打する
b_fighting3|ルチャドリ|wind|鳥＋覆面|B|覆面を つけた 空中殺法の 鳥
b_fighting4|ハチマキザル|-|サル|B|はちまきを しめると 本気を 出す
b_fighting5|ツルケン|wind|ツル|B|片足で 立つ 拳法の 構え
b_fighting6|ヨロイジロ|rock|アルマジロ|Q|かたい 背中で 体当たり
b_fighting7|クマグローブ|-|クマ|B|赤い グローブの 力持ち ボクサー
b_fighting8|カマキリケン|bug|カマキリ|M|カマの 両腕で 拳法を つかう
b_fighting9|スモウリキ|rock|力士|B|どっしり 構えて 押し出す
b_fighting10|パンダボクサ|dark|パンダ|B|赤い マフラーの チャンピオン
b_poison1|フラスコン|water|フラスコ|W|毒の 薬が 入った フラスコ。泡を ぶくぶく 飛ばす
b_poison2|ドクモリ|wind|コウモリ|F|洞くつの 奥で 毒の 歌を うたう
b_poison3|キノコヒメ|fairy|キノコ|B|かさを ふると 眠りの 胞子が 舞う
b_poison4|ノラドクネコ|dark|ネコ|Q|毒の けむりを まとった 野良ネコ
b_poison5|ドクマイマイ|-|カタツムリ|M|通った あとに 毒の すじが 残る
b_poison6|ドクグモ|bug|クモ|M|紫の 糸で えものを しばる
b_poison7|ドクガスン|ghost|毒ガス|W|紫の けむりが 集まって 生まれた
b_poison8|パクリソウ|grass|ハエトリソウ|P|大きな 口で なんでも ぱくり
b_poison9|ムラサソリ|ground|サソリ|M|紫の 毒の しっぽを 高く かかげる
b_poison10|ペストガラス|dark|カラス＋ペスト医者|B|くちばしの マスクと シルクハット。毒の 薬を あやつる
b_ground1|モグラン|-|モグラ|Q|大きな 爪で 土を ほりすすむ
b_ground2|ショベラー|steel|ショベルカー|Q|黄色い ショベルカー。アームで 地面ごと すくいあげる
b_ground3|レンガゴーレム|rock|ゴーレム|B|レンガを 積みあげた 体
b_ground4|ハニワウマ|-|はにわの 馬|Q|土で できた 馬。走ると 砂ぼこりが 立つ
b_ground5|スナミミズ|-|ミミズ|S|砂漠の 下を ぐねぐね 進む
b_ground6|トロッコン|steel|トロッコ|Q|鉱石を 積んで 線路を 走る
b_ground7|トゲイワサイ|rock|サイ|Q|岩の とげが びっしり 生えた サイ
b_ground8|ドグウン|psychic|土偶|B|大昔の 土偶。ひとつ目が 光る
b_ground9|コハクハリ|rock|ハリネズミ|Q|背中の コハクの とげが 光る
b_ground10|ドリルモグラ|steel|ドリル＋モグラ|Q|鼻の ドリルで 岩山を つらぬく
b_wind1|アオトリ|-|青い鳥|F|しあわせを 運ぶと いわれる 小鳥
b_wind2|タコギツネ|fire|キツネ＋たこあげ|F|リボンの しっぽで 風に のる
b_wind3|カモメン|water|カモメ|F|海の 上を 風に のって 飛ぶ
b_wind4|フウセンボ|fairy|風船|F|たくさんの 風船で ぷかぷか 浮かぶ
b_wind5|カサドリ|ghost|からかさ＋ツル|F|紙の かさを さした 一本足の 鳥
b_wind6|クモモ|fairy|雲|F|ふわふわの 雲の 子。泣くと 雨が ふる
b_wind7|ライウン|elec|竜＋雷雲|F|雷雲を ひきつれて 飛ぶ
b_wind8|ヘリドリ|steel|ヘリコプター＋鳥|F|頭の プロペラで 空中に 止まる
b_wind9|ソラブネ|steel|飛行船＋マンボウ|F|マンボウの 形の 飛行船。プロペラで 風を 起こす
b_wind10|タカオウ|fighting|タカ|F|空の 王者。大きな 翼で 突風を 起こす
b_dragon1|ヒチビドラ|fire|竜の 子|B|しっぽの 先に 小さな 火
b_dragon2|シャリンリュウ|steel|竜＋車輪|Q|歯車の 体で 走る からくり竜
b_dragon3|スイショウリュウ|ice|水晶の 竜|Q|透きとおった うろこが 光を まげる
b_dragon4|マキモノリュウ|psychic|竜＋巻物|S|巻物に ひみつの 術を 書きしるす
b_dragon5|ホシゾラリュウ|fairy|星空の 竜|B|うろこに 星空が うつる
b_dragon6|ヨロイドラ|steel|竜|Q|鉄の ような うろこで 身を 守る
b_dragon7|マツリュウ|fire|祭りの 竜|S|祭りの 竜の ように 赤い リボンを なびかせる
b_dragon8|ヒスイリュウ|grass|竜|Q|ひすい色の うろこと 金の たてがみ
b_dragon9|シコクリュウ|dark|竜|F|紫黒の 翼で 夜空を おおう
b_dragon10|タカラリュウ|ground|竜＋財宝|Q|金貨の 山に ねそべる 欲ばりな 竜
g1|オニビン|fire|鬼火|W|青白い 炎が ふわふわ ただよう
g2|トウロウ|fire|灯籠|W|夜に なると 紫の 火が ともる
g3|ノロイヌイ|normal|呪いの ぬいぐるみ|B|ボタンの 目の つぎはぎ人形。霊火を まとって 呪う
g4|キツネメン|psychic|狐の お面|F|宙に 浮かぶ 狐の お面。鈴の 音で 心を まどわす
g5|ユウレイネコ|dark|黒ネコ|Q|けむりの しっぽを ゆらす 黒ネコの 霊
g6|ボウレイキシ|steel|よろいの 騎士|B|からっぽの よろいに 青い 霊火が やどる
g7|メダマショ|dark|目玉の 本|F|表紙に 大きな 目玉。ページの 触手で からめとる
g8|タマメダマ|psychic|目玉|W|たくさんの 目で あらゆる ものを 見とおす
g9|シニガミン|dark|死神|F|大きな カマを もつ 死神。霊を 連れさる
g10|ユウレイクラゲ|water|クラゲ|W|夜の 空を ただよう 白い クラゲの 霊
'''

if __name__ == '__main__':
    allv = json.load(open('all.json'))
    meta, spr = {}, {}
    for line in TABLE.strip().splitlines():
        k, name, t2, base, body, note = line.split('|')
        if k in SKIP or k not in allv: print('skip', k); continue
        if k.startswith('g'): t1 = 'ghost'; num = int(k[1:])
        else:
            t = k[2:].rstrip('0123456789'); t1 = ROW[t]; num = int(k[2 + len(t):])
        L = LORE[k]
        size = 'S' if L['h'] < .7 else 'M' if L['h'] < 1.8 else 'L'      # 強さの 合計は 高さで きまる
        rare = 1 if (num == 10 and not k.startswith('g')) or k == 'g9' else 0
        gid = KEEP.get(k, k)
        # ゲーム内の 大きさ：高さ 0.25m 以下 = 0.72倍、4m 以上 = 1.44倍（あいだは 対数で なめらかに）
        u = min(1, max(0, (math.log10(L['h']) - math.log10(.25)) / (math.log10(4) - math.log10(.25))))
        sz = round(.72 + .72 * u, 3)
        meta[gid] = {'name': name, 'types': [t1] + ([t2] if t2 != '-' else []), 'base': base, 'body': body, 'size': size, 'note': note, 'rare': rare, 'src': k,
                     'h': L['h'], 'wt': L['wt'], 'home': L['home'], 'trait': L['trait'], 'evo': KEEP.get(L['evo'], L['evo']) if L['evo'] else None, 'sz': sz}
        v = allv[k]; spr[gid] = {'w': v['w'], 'h': v['h'], 'pal': v['pal'], 'd': v['d'], 'ms': round(76 * sz / max(v['w'], v['h']), 3)}
    for gid, m in meta.items():   # しんか先が 外した モンスターなら 消す
        if m['evo'] and m['evo'] not in meta: m['evo'] = None
    json.dump(meta, open('meta.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(spr, open('sprites.json', 'w'), separators=(',', ':'))
    print(len(meta), 'monsters')
