# Steam で うる ための せってい

PC版（`app/desktop`）は Steam に つながる ように して あります。Steamworks の がめんで いれる ものと、GitHub に いれる ものを まとめます。

## 1. App ID を いれる
- Steamworks で もらった App ID を `app/desktop/steam.json` の `appId` に かく。または GitHub の Secrets に `STEAM_APP_ID` を いれる（ビルドの ときに こちらが つかわれる）
- 480 の あいだは Valve の ためし用（Spacewar）。実績は とれないが、Steam オーバーレイ（Shift+Tab）は ためせる
- Steam が うごいて いない PC でも ゲームは ふつうに あそべる（つながらない だけ）
- 本当の App ID の ときは、Steam の そとから ひらくと Steam から ひらきなおす

## 2. 実績（Steamworks → Stats & Achievements → Achievements）
API 名は この とおりに つくる（ゲームは この 名前で おくる）。あとから はじめた 人も、つぎに セーブした ときに これまでの ぶんが とれる。

| API 名 | とれる とき |
|---|---|
| FIRST_WIN | はじめて バトルに かった |
| FIRST_CATCH | はじめて モンスターを つかまえた |
| BADGE_1 | はじめて バッジを とった |
| BADGE_10 | バッジが 10こ そろった |
| CHAMPION | チャンピオンに なった（でんどういり） |
| ARCADE_CLEAR | アーケードを クリアした |
| DEX_50 | ずかんで 50しゅるい つかまえた |
| DEX_ALL | ずかんを ぜんぶ つかまえた |
| TRAIN_FIRST | 訓練の チュートリアルを おえた |
| ONLINE_WIN | ランク対戦で はじめて かった |

## 3. Steam Cloud（Steamworks → Application → Steam Cloud）
セーブは `PixelMonsterArena/cloud/save.json` にも かいて います。Auto-Cloud で この ファイルを おくる：
- Byte quota：1MB・Number of files：1
- Root Overrides なし で、OS ごとに 1ぎょうずつ：

| OS | Root | Subdirectory | Pattern |
|---|---|---|---|
| Windows | WinAppDataRoaming | PixelMonsterArena/cloud | *.json |
| macOS | MacAppSupport | PixelMonsterArena/cloud | *.json |
| Linux | LinuxXdgConfigHome | PixelMonsterArena/cloud | *.json |

ほかの PC で あそんだ ぶんが あたらしい ときは、ひらいた ときに そちらに いれかわる。

## 4. デポと 起動の せってい（Steamworks → SteamPipe / Installation）
- デポを 3つ つくる：Windows・macOS・Linux（それぞれ OS を えらぶ）
- Launch Options：
  - Windows：`PixelMonsterArena.exe`
  - macOS：`Pixel Monster Arena.app`
  - Linux：`PixelMonsterArena`

## 5. GitHub から アップロード
1. GitHub の Settings → Secrets and variables → Actions に いれる：
   - `STEAM_APP_ID`：App ID
   - `STEAM_USERNAME`：アップロード用の Steam アカウント（Steamworks で ビルドを のせる けんげんを つける。ふだん つかう アカウントと わけると あんしん）
   - `STEAM_CONFIG_VDF`：その アカウントで 1かい steamcmd に ログインして できる `config/config.vdf` を base64 に した もの（Steam Guard を とおす ため。くわしくは game-ci/steam-deploy の README）
   - デポ ID は ワークフローが 自動で つかうので いれなくて よい（App ID＋1・＋2・＋3 の じゅん：Windows・Mac・Linux）。ちがう ばあいは しらせて ください
2. Actions →「PC アプリ（Steam）」→ Run workflow →「Steam に アップロード」に チェック
3. Steamworks の SteamPipe → Builds で のった ビルドを default（または beta）に する

## 6. Mac について
Mac は Apple の しょめい（Developer ID・年 99ドル）と notarization が ないと、ひらく ときに けいこくが でる ことが あります。さいしょは Windows だけ で だす のも あり です。
