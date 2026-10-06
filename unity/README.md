# Pixel Monster Arena（Unity 版）

ブラウザ版（リポジトリ直下の `index.html`）と同じゲームを Unity に移植したプロジェクトです。
モンスター・わざ（ランキング上位100を含む）・タイプ表・大会・捕獲・セーブまで、同じ内容で動きます。

- シーンやプレハブを手で作る必要はありません。ドット絵・ステージ・UI はすべて C# のコードから実行時に生成します。
- データは `index.html` から自動生成しています（`Assets/Scripts/PixelMonsterArena/Data.Generated.cs`）。

## ひらきかた

1. **Unity Hub** をインストールし、**Unity 6（6000.0 LTS 以降）** を入れる
   - スマホで遊ぶなら、エディタと一緒に **Android Build Support**（または iOS Build Support）も入れる
2. Unity Hub の「**追加**」→「**ディスクから追加**」で `unity/PixelMonsterArena` フォルダを選ぶ
3. プロジェクトを開く（初回はパッケージの読み込みで数分かかります）
   - 「新しい Input System を有効にしますか？」と聞かれたら **Yes**（どちらでも動きます）
4. 自動で `Assets/Scenes/Main.unity` が作られ、Build Settings に登録されます
   - 作られなかったときは、メニュー「**Pixel Monster Arena → メインシーンを作りなおす**」
5. `Main` シーンを開いて **▶（再生）** を押すと遊べます

## そうさ

- モンスターは自分で動きます。ボタンで わざ（4つ）・こうげき・かわす・こうたい・クリスタル・オート を指示します
- PC：J=こうげき、K・L・U・I=わざ、Space=かわす、C=クリスタル、X=こうたい

## スマホ向けにビルドする

1. **File → Build Profiles**（Unity 6 の場合。旧版は Build Settings）で **Android**（または iOS）を選び「Switch Platform」
2. 縦画面で遊ぶなら **Player Settings → Resolution and Presentation → Default Orientation** を **Portrait** に
3. Android 端末をUSBでつなぎ「**Build And Run**」

## 日本語が □ になるとき

IMGUI の標準フォントは OS のフォントで日本語を表示します。□ になる環境では、
日本語フォント（.ttf / .otf）を `Assets/Resources/JPFont.ttf` という名前で置くと自動で使われます。

## データを更新するとき

ブラウザ版（`index.html`）のモンスターやわざを変えたら、リポジトリ直下で次を実行して C# 側を作りなおします。

```sh
node tools/export-sprites.js index.html unity/PixelMonsterArena/Assets/Resources/Sprites   # ドット絵（アニメ 14コマ × モンスター／トレーナー）
node unity/gen-data.js index.html unity/PixelMonsterArena/Assets/Scripts/PixelMonsterArena/Data.Generated.cs
```

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `Game.cs` | 起動・画面（タイトル／最初の1匹／ハブ／へんせい／バトル）・UI・入力 |
| `Battle.cs` | リアルタイムバトルの中身（わざ・状態異常・AI・捕獲・経験値） |
| `BattleRenderer.cs` / `Painter.cs` | バトル画面の描画（SpriteRenderer を使い回して描く） |
| `Stage.cs` / `PixelArt.cs` | スタジアムとくさむらの背景、ドット絵の読みこみ（`Resources/Sprites` の `{名前}_{コマ}.png`。コマ選びは `BattleRenderer.MonFrame`） |
| `Data.cs` / `Data.Generated.cs` | 型定義と、`index.html` から生成したデータ |
| `SaveData.cs` | セーブ（PlayerPrefs） |
| `InputAdapter.cs` | タッチ・マウス・キーボード（旧 Input Manager／新 Input System 両対応） |
| `Editor/PixelMonsterArenaSetup.cs` | 初回にシーンを作って Build Settings に登録 |
