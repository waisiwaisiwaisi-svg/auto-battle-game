# モンスターの ドット絵を 画像生成AIで 作る 道具

CPU だけで 動きます（1枚 約10秒）。

```sh
python3 -m venv sd && sd/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
sd/bin/pip install diffusers transformers accelerate safetensors pillow "rembg[cpu]"

sd/bin/python batch.py < ids.txt      # 候補を raw/<id>_<seed>.png に 生成（プロンプトは batch.py）
sd/bin/python contact.py c.png <id>…  # 候補の 一覧を 見て えらぶ
sd/bin/python pix.py raw/<id>_<seed>.png out/p.png <高さ>   # ためしに ドット絵化
sd/bin/python grid.py out/p.png g.png                  # 目の 座標を しらべる
#   → picks.json に { src, h, colors, eyes:[[x, y, 'big'|'mid'|'small', 虹彩色, 虹彩の影色]] }
sd/bin/python make.py                 # all.json を 作る（目を 手描きの ドットに おきかえ、まばたき用の 範囲も 記録）
node prev.js all.json pv.png          # 14コマの 一覧
python3 splice.py                     # index.html の AISPR ブロックを 更新
node ../export-sprites.js ../../index.html ../../unity/PixelMonsterArena/Assets/Resources/Sprites   # Unity 用
```

`src/` に 採用した 下絵（生成そのまま）を 置いています。
モデル: stabilityai/sdxl-turbo（Stability AI Community License）。
