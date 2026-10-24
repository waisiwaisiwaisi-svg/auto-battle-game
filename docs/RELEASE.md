# ピクセルモンスターアリーナ　アプリ版リリース手順

ゲーム本体は `index.html` の1ファイルのまま。`app/` が iOS / Android アプリの入れ物（Capacitor）です。
`app/` でビルドすると、`index.html` を `app/www/` にコピーし、オンライン機能を Firebase につなぐ部品（`app/src/backend.js`）を差しこみます。claude.ai 版はそのまま動きます。

---

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
1. アプリを作成：名前「ピクセルモンスターアリーナ」、ゲーム、無料。
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

---

## 5. ストア掲載文の例

- **名前**：ピクセルモンスターアリーナ
- **サブタイトル／簡単な説明（80字以内）**：ドット絵モンスターを育てて、リアルタイムで対戦！ランク戦・ギルドで全国のトレーナーと競おう
- **説明**：
  ```
  ドット絵のモンスターたちが、リアルタイムでぶつかりあう！
  ・173種類のモンスターをくさむらでつかまえて、自分だけのチームに
  ・技の相性と性格を見きわめる、オートバトル＋指示のハイブリッド対戦
  ・オンライン対戦でレートを上げて、ブロンズからマスターを目指そう
  ・ギルドに入ってみんなでポイントを集め、週間ランキングで競争
  ・アーケードでジムを巡ってバッジを集め、チャンピオンリーグへ
  ・トレーナーとモンスターをドット絵で自作できるメイキング機能
  ```
- **キーワード（iOS）**：モンスター,ドット絵,対戦,育成,オートバトル,ランク戦,ギルド,レトロ,RPG

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

- **似ている作品との関係**：モンスターを捕まえる・ジム・バッジ・殿堂入りなど、有名作品に近い用語や仕組みがあります。名前・絵・用語が既存作品と同じにならないよう確認してください（似すぎると著作権・商標で削除や却下の対象になります）。
- **ユーザー生成コンテンツ**（名前・ギルド名・チャット）：NGワードの伏せ字、通報、ブロック、連絡先の掲載が必要です（アプリ内に実装済み。連絡先は7章）。
- **最低限の機能**（Apple 4.2）：Web をそのまま包んだだけのアプリは却下されやすいですが、本作はオフラインで遊べるゲームなので問題ありません。
