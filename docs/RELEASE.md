# マジックギアアリーナ　アプリ版リリース手順

ゲーム本体は `index.html` の1ファイルのまま。`app/` が iOS / Android アプリの入れ物（Capacitor）です。
`app/` でビルドすると、`index.html` を `app/www/` にコピーし、オンライン機能を Firebase につなぐ部品（`app/src/backend.js`）を差しこみます。claude.ai 版はそのまま動きます。

---

## いまの状態と、のこりの作業（2026/11/11）

- アプリの中身：最終テスト済み（全画面×日英中×スマホ・タブレット・PC、通しプレイ、データの確認）
- Capacitor 8：Android は targetSdk・compileSdk 36（Google Play の いまの 条件）、最低 Android 7（minSdk 24）。iOS は 15.0 から
- バージョン：1.0.0（Android の versionCode・iOS のビルド番号は GitHub Actions の実行番号が自動で入る）
- はじめての ときの ことばは 端末（Steam 版は Steam）の ことばに あわせる。日本語・中国語 いがいは English
- **のこり（あなたが やること）**
  1. Firebase の設定を GitHub Secrets の `FIREBASE_CONFIG_JS` に入れる（1章・6章）
  2. 署名：Android（`ANDROID_KEYSTORE_BASE64` ほか）・iOS（`IOS_P12_BASE64`・`ASC_KEY_P8` ほか）・Steam（`STEAM_APP_ID`・`STEAM_USERNAME`・`STEAM_CONFIG_VDF`）を GitHub Secrets に入れる（6章・STEAM.md）
  3. プライバシーポリシー（`docs/privacy.html`）の「お問い合わせ」に連絡先を書く（7章）
  4. 各ストアで アプリを作って、5章の文と `promo/store/` の画像を入れる
  5. Google Play は クローズドテスト 12人×14日（0章の注意）
  6. 人型ステージ（キングエイト ツバキ）の絵が とどいたら さしかえる（いまは かくとうの ステージで 代用）

## 0. 必要なもの

| もの | 費用 | 用途 |
|---|---|---|
| Firebase プロジェクト | 無料（Spark プラン）で開始可 | オンライン対戦・ランキング・ギルドのサーバー |
| Google Play Console アカウント | 登録料 25ドル（1回だけ） | Android 版の公開 |
| Apple Developer Program | 年 99ドル | iOS 版の公開 |
| Mac（Xcode） | — | iOS のビルド。Mac がなければ GitHub Actions（macOS）で代用（6章） |

> **Google Play の注意**：2023年11月以降に作った個人の開発者アカウントは、本番公開の前に「クローズドテストを 12人以上で 14日間」行う必要があります。早めにテスターを集めてください。

---

## 1. Firebase の準備（オンライン機能）

1. <https://console.firebase.google.com/> でプロジェクトを作る（Google アナリティクスは不要）。
2. **Authentication** → 「始める」→ ログイン方法で **匿名** を有効にする。
3. **Firestore Database** → 作成 → 本番モード、場所は `asia-northeast1（東京）`。
4. **Realtime Database** → 作成 → 場所は `asia-southeast1（シンガポール）`、ロックモード。
5. プロジェクトの設定 → マイアプリ → **ウェブアプリ（</>）を追加** → 表示された設定をコピー。
6. `app/firebase-config.example.js` を `app/firebase-config.js` にコピーして、5の値を貼る。
   `databaseURL`（Realtime Database の URL）も必ず入れる。
7. ルールをアップロード：
   ```sh
   cd app
   npx firebase login
   npx firebase use --add          # 作ったプロジェクトを選ぶ
   npx firebase deploy --only firestore,database
   ```
   ルールの中身：`app/firebase/firestore.rules`・`app/firebase/database.rules.json`
   （読むのはログインした人全員、書けるのは自分のデータだけ。通報は書くだけで読めない）
4. **いまは むりょう プラン（Spark）で うごかす**：ゲームの `SRV_FN_ON = false` で サーバーの しごとは つかわない。
   レート・せんせき（`ranks` の r・w・l）と ギルドポイント（`gmembers` の pts・tot・wk）は ゲームが かき、`firestore.rules` で かわりかたを せいげん する
   （1かいの かきこみで しあいは 1つ・レートの かわりは ±32 まで・しあいの あいだは 15びょう／ギルドは 1かい +3 まで・10びょう）。
   ルールを かえたら `npx firebase deploy --only firestore:rules,database`（むりょう プランでも できる）。
   むりょう プランの うえかぎり：Realtime Database の どうじ せつぞく 100・Firestore の よみ 1日 5まん／かき 2まん。こえた ひは オンラインが とまる（せいきゅう は されない）。
   Blaze に したら `SRV_FN_ON = true` に して、下の サーバーの しごと と ルール（r・w・l は サーバーだけ）に もどす。
5. **サーバーの しごと（Cloud Functions：Blaze プランに したら）**：レート・せんせき・ギルドポイント・日替わりの むりょう を サーバーで きめる（チート たいさく）。
   Firebase を **Blaze プラン**（従量課金）に して から：
   ```sh
   cd app/functions && npm install && cd ..
   npx firebase deploy --only functions,firestore,database
   ```
   - `matchStart`／`matchReport`：へやの ようすを サーバーが よんで 試合を きろく → ふたりの けっかが あえば レートと ギルドポイントを つける。くいちがいは どちらにも つけず `flags/{uid}.disp` に かぞえる
   - `matchSweep`（5ふん ごと）：10ぷん たっても かたほう だけ の 試合（とちゅうで ぬけた）を のこった ほうの もうしでで きめる
   - `guildWin1`：ふつうの バトルの かち +1（30びょうに 1かい・1日 60かい まで）／`claimDaily`：むりょう（日本時間の 1日 1かい）
   - `ranks` の r・w・l・h と `gmembers` の pts・tot・wk は ルールで クライアントからは かけない（サーバーだけ）
   - **さいげんで たしかめる（matchLog → matchVerify）**：ホストは 試合の きろく（シード・チーム・そうさ）を おくる。サーバーは ヘッドレス Chromium で ゲームを うごかして ほんとうの かちまけを きめる（`functions/game/index.html` は deploy の まえに じどうで つくられる）。メモリ 2GiB の 関数に なる
   - ゲームは どの 端末でも おなじ けいさんに なる ように して ある（三角関数などは じぶんで けいさん・たたかいの らんすうは シードつき・1/60びょう きざみ）。**バトルの しくみを かえた ときは、アプリと サーバーを いっしょに 出す**（GAME_VER が ちがう 試合は さいげん しないで ふたりの もうしでで きめる）
   - flags/{uid}：n（試合）・disp（くいちがい）・cheat（してない かちを いった）・div（ホストの がめんが さいげんと ちがった）。おおい 人は ranks.hide＝true（ランキングに ださない・レート／ギルドに いれない）
   - おなじ ふたりの 試合は 1日 3かい まで レートを うごかす（なれあい たいさく）
   - **セーブも サーバー（saves/{uid}）**：ジェム・ボックス・どうぐ・ワザステッカー・ブラインドボックス・モンスター・すすみぐあい は サーバーの セーブが ただしい（`act`／`saveGet`）。
     ショップ・はこ・どうぐ・きょうか・ワザステッカー・にがす は サーバーで ゲームの コードを うごかして から 端末でも おなじ ように うごく。たたかいは はじまりで チケット（あいて・シード）を つくり、
     おわったら サーバーが そうさの きろくで さいげん して ごほうびを つける。オンライン対戦の チームは サーバーの セーブに いる モンスター だけ（ちがえば その 試合は なし・cheat）。
     アプリ版は オンラインが ひつよう（claude.ai 版は いままで どおり 端末で）。さいしょの ながれが おわった とき、端末の データから あたらしい プロフィールとして つくる（ジェム 50・ボックス 20・モンスター 3たい まで。のうりょくは サーバーで きめなおす）。
     **いま アプリを ためして いる 人の データは、この しくみに なった とき あたらしく なる**。べつの 端末へは ふっかつコードで（`saveClaim`：サーバーの セーブを うつす）
   - `act`・`saveGet`・`matchVerify` は ゲームの ページを ひらく ので さいしょの 1かいは 数びょう かかる。にぎやかに なったら `minInstances: 1` を おすすめ（すこし お金が かかる）
   - ためす：`npx firebase emulators:start --config firebase.emu.json --only auth,firestore,database,functions --project demo-pma`
   - 配信用の ビルド（`npm run build`）は テスト用の `window.__game` を はずす（のこす ときは `PMA_DEBUG=1`）
   - **ゲームを かえたら サーバーも くばりなおす**：さいげんは サーバーに おいた ゲーム（`functions/game/index.html`）で うごく ので、ちがう 版だと「ちがう バージョン」で たしかめられない。`SRV_FN_ON = true` に して、リポジトリの Secrets に `FIREBASE_SERVICE_ACCOUNT`（サービスアカウントの JSON）と `FIREBASE_PROJECT_ID` を いれて おくと、本番に あげる たびに `.github/workflows/functions.yml` が じどうで くばりなおす

`firebase-config.js` がない／中身が `YOUR_...` のままだと、アプリはオフライン専用で動きます（1人用の遊びは全部できます）。

---

## 2. 手元でビルドして動かす

```sh
cd app
npm install
npm run sync            # index.html → www/ にコピー ＋ android/ios に反映
npx cap open android    # Android Studio が開く → ▶ で実機/エミュレータ
npx cap open ios        # Xcode が開く（Mac のみ。初回は CocoaPods が必要：brew install cocoapods）
```

`index.html` を直したら、毎回 `npm run sync` をしてからビルドします。

アイコン・スプラッシュを作り直すとき：`app/assets/` の画像を差し替えて `npm run assets`。

---

## 3. Android（Google Play）

### 3-1. 署名かぎを作る（1回だけ・なくすと更新できなくなるので厳重に保管）
```sh
keytool -genkey -v -keystore pma-release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias pma
```
`app/android/keystore.properties` を作る（git には入りません）：
```
storeFile=/絶対パス/pma-release.jks
storePassword=かぎのパスワード
keyAlias=pma
keyPassword=かぎのパスワード
```

### 3-2. AAB を作る
```sh
cd app && npm run sync
cd android && ./gradlew bundleRelease
# → app/android/app/build/outputs/bundle/release/app-release.aab
```
バージョンは環境変数で指定できます：`PMA_VERSION_CODE=2 PMA_VERSION_NAME=1.0.1 ./gradlew bundleRelease`
（versionCode は毎回 1 ずつ上げる）

### 3-3. Play Console
1. アプリを作成：名前「マジックギアアリーナ」、ゲーム、無料。
2. **アプリのコンテンツ**をすべて埋める：
   - プライバシーポリシー：`https://waisiwaisiwaisi-svg.github.io/auto-battle-game/privacy.html`（7章で公開）
   - 広告：なし
   - コンテンツのレーティング：アンケートに回答（ユーザー同士のやりとり＝ギルドチャットあり、と答える）
   - ターゲット年齢：13歳以上を推奨（それ未満を含めるとファミリー向けの追加審査がある）
   - **データセーフティ**：
     - 収集：ユーザーID（匿名ID）、ユーザー名（プレイヤー名）、アプリ内メッセージ（ギルドチャット）、ゲームの進行（レート・勝敗）
     - 目的：アプリの機能。第三者と共有：しない。転送時の暗号化：する。
     - 削除のリクエスト：アプリ内（せってい →「オンラインの データを けす」）
3. **テスト → クローズドテスト**に AAB をアップロード（Play App Signing を有効のまま）→ テスターを招待。
4. 条件（12人×14日）を満たしたら **本番** へ。

---

## 4. iOS（App Store）

1. <https://developer.apple.com/account> → Identifiers で Bundle ID `com.waisi.pixelmonsterarena` を登録。
2. <https://appstoreconnect.apple.com/> → マイApp → 新規 App（名前・プライマリ言語：日本語・Bundle ID・SKU は任意）。
3. Mac で：
   ```sh
   cd app && npm run sync && npx cap open ios
   ```
   Xcode → App ターゲット → Signing & Capabilities → Team を選ぶ（自動署名）。
   Product → Archive → Distribute App → App Store Connect → アップロード。
4. App Store Connect で：
   - **App のプライバシー**：収集するデータ＝ユーザーID・名前（ユーザー名）・その他のユーザーコンテンツ（チャット）・ゲームプレイの内容。すべて「App の機能」、トラッキングなし、ユーザーに紐づく。
   - プライバシーポリシー URL（3-3 と同じ）
   - 年齢制限指定：アンケートに回答（ユーザー生成コンテンツあり）
   - スクリーンショット：6.9インチ（1320×2868 など）と 13インチ iPad（iPad 対応のまま出す場合）
   - 審査メモ：「オンライン機能は匿名ログインで自動的に使えます。ギルドのチャットは、名前をタップして通報・ブロックできます。」
5. TestFlight で動作確認 → 審査に提出。

輸出コンプライアンス（暗号化）の質問は `Info.plist` に「使っていない」と設定済みなので出ません。
プライバシーマニフェスト（`app/ios/App/App/PrivacyInfo.xcprivacy`）も入れてあります：トラッキングなし、集めるのは ユーザーID（匿名）・その他のユーザーコンテンツ（名前・チャット）・ゲームプレイの内容 で、どれも「App の機能」だけに使う。App Store Connect の「App のプライバシー」も同じ内容で答えてください。

---

## 5. ストア掲載文（日本語・English・简体中文）

スクリーンショットは `promo/store/` にあります（言語_サイズ_場面.png）。
- `iphone69`：1320×2868（App Store 6.9インチ）・`ipad13`：2752×2064（App Store 13インチ iPad・よこ向き）
- `android`：1080×2400（Google Play スマホ）・`steam`：1920×1080（Steam）
- 場面：1battle（キングエイト戦）・2home（ホームの街）・3train（訓練）・4team（編成）・5wild（空き地で捕獲）

### 日本語
- **名前**：マジックギアアリーナ
- **サブタイトル（30字以内・iOS）**：育てて、教えて、リアルタイム対戦
- **簡単な説明（80字以内・Google Play）**：ドット絵のマギアを捕まえて訓練し、リアルタイムで戦わせよう！ギルド・キングエイト・オンライン対戦
- **説明**：
  ```
  ドット絵のマギアたちが、リアルタイムでぶつかりあう！
  ・191種類のマギアを空き地で捕まえて、自分だけのチームに
  ・「訓練」で技の順番・条件・撃ち方を教えると、その通りに戦うオートバトル
  ・8つのギルドを巡ってタグを集め、キングエイトとキングに挑もう
  ・アリーナでタワー・ドラフトバトル・10連戦に挑戦
  ・オンライン対戦でレートを上げて、ブロンズからマスターを目指そう
  ・チームに入って仲間と協力、週間ランキングで競争
  ・オフラインでも1人用モードはすべて遊べます
  ```
- **キーワード（iOS・100字以内）**：モンスター,ドット絵,対戦,育成,オートバトル,ランク戦,レトロ,RPG,捕獲,ギルド

### English
- **Name**: Magic Gear Arena
- **Subtitle (iOS, 30 chars)**: Catch, train, battle in real time
- **Short description (Google Play, 80 chars)**: Catch pixel Magia, train their moves, and battle in real time!
- **Description**:
  ```
  Pixel-art Magia clash in real-time battles!
  - Catch 191 kinds of Magia in the Vacant Lot and build your own team
  - Use Training to teach move order, conditions and positioning - then watch them fight exactly as taught
  - Visit 8 Guilds to collect Tags, then challenge the King Eight and the King
  - Take on the Battle Tower, Draft Battles and 10-battle runs in the Arena
  - Climb from Bronze to Master in online ranked battles
  - Join a Team with friends and compete on the weekly ranking
  - All single-player modes work offline
  ```
- **Keywords (iOS)**: monster,pixel,retro,battle,auto battler,trainer,rpg,pvp,strategy,collect

### 简体中文
- **名称**：魔法齿轮竞技场
- **副标题（iOS）**：捕捉、训练、实时对战
- **简短说明（Google Play）**：捕捉像素魔机，训练招式，实时对战！公会・王者八人・在线对战
- **说明**：
  ```
  像素风格的魔机们，在实时战斗中激烈碰撞！
  ・在空地捕捉191种魔机，组成属于你的队伍
  ・通过“训练”教会招式顺序、条件和走位，它们会照着你教的方式战斗
  ・巡游8个公会收集标签，挑战王者八人与王者
  ・在竞技场挑战塔、轮抽对战与10连战
  ・在线对战提升积分，从青铜一路冲向大师
  ・加入队伍与伙伴合作，在每周排行榜上竞争
  ・单人模式全部可离线游玩
  ```
- **关键词（iOS）**：怪兽,像素,复古,对战,自动战斗,养成,RPG,策略,收集

---

## 6. GitHub Actions で自動ビルド（Mac がなくても iOS をビルドできる）

`index.html` か `app/` を push すると動きます（`.github/workflows/app-android.yml`・`app-ios.yml`）。
リポジトリの Settings → Secrets and variables → Actions に登録：

| シークレット | 中身 |
|---|---|
| `FIREBASE_CONFIG_JS` | `firebase-config.js` の中身まるごと |
| `ANDROID_KEYSTORE_BASE64` | `base64 -w0 pma-release.jks` の結果 |
| `ANDROID_KEYSTORE_PASSWORD` / `ANDROID_KEY_ALIAS` / `ANDROID_KEY_PASSWORD` | 3-1 の値 |
| `IOS_P12_BASE64` / `IOS_P12_PASSWORD` | Apple Distribution 証明書（.p12）を base64 にしたもの・そのパスワード |
| `IOS_PROFILE_BASE64` / `IOS_PROFILE_NAME` | App Store 用プロビジョニングプロファイル（.mobileprovision）を base64・その名前 |
| `IOS_TEAM_ID` | Apple の Team ID（10文字） |
| `ASC_KEY_ID` / `ASC_ISSUER_ID` / `ASC_KEY_P8` | App Store Connect API キー（ユーザとアクセス → 統合 → キー） |

- 署名のシークレットがないとき：Android はテスト用 APK、iOS はシミュレータ用ビルド（確認だけ）。
- そろっているとき：Android は Play 用 AAB、iOS は TestFlight へ自動アップロード。
- できたファイルは Actions の実行結果の「Artifacts」からダウンロード。

---

## 7. プライバシーポリシーの公開

`docs/privacy.html` を GitHub Pages で公開します：リポジトリの Settings → Pages → Branch を `main`、フォルダを `/docs` に。
公開前に、ページ下の「お問い合わせ」に連絡先メールアドレスを書いてください。

---

## 8. 審査で気をつけること

- **似ている作品との関係**：モンスターを捕まえて育てる仕組みは有名作品に近いので、用語はギルド・タグ・キングエイト・キングなど独自のものにしています。名前・絵・用語が既存作品と同じにならないよう確認してください（似すぎると著作権・商標で削除や却下の対象になります）。
- **ユーザー生成コンテンツ**（名前・ギルド名・チャット）：NGワードの伏せ字、通報、ブロック、連絡先の掲載が必要です（アプリ内に実装済み。連絡先は7章）。
- **最低限の機能**（Apple 4.2）：Web をそのまま包んだだけのアプリは却下されやすいですが、本作はオフラインで遊べるゲームなので問題ありません。


## PC版（Steam）

`app/desktop/` は ゲーム（`app/www`）を Electron の まどで うごかす PC版です。

- ためす：`cd app/desktop && npm install && npm start`（F11 か Alt+Enter で ぜんがめん）
- つくる：`npm run dist:win`／`dist:mac`／`dist:linux` → `app/desktop/dist/` に できる。GitHub の「PC アプリ（Steam）」ワークフローでも 3つ とも つくれる（Firebase の 設定は Android と おなじ シークレット `FIREBASE_CONFIG_JS`）
- Steam に のせる：Steamworks で アプリを つくり、SteamPipe（steamcmd）で `dist/win-unpacked` などを アップロード。起動ファイルは `PixelMonsterArena.exe`（Mac は `.app`、Linux は `PixelMonsterArena`）
- Mac で 配るときは Apple の 署名・公証（notarize）が いる（electron-builder の `mac.identity` と `notarize` を せってい）
- Firebase の API キーに「HTTP リファラーの せいげん」を かけて いる ときは、PC版（`app://game`）からも つかえる ように する
- セーブは PC の ユーザーフォルダ（Electron の userData）に のこる。2つ いっぺんには ひらけない
