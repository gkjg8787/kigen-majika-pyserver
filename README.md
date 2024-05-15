# kigen-majika-pyserver

## 概要

- 消費期限を管理するための WEB サーバアプリケーション。
- API がメインですが HTML での一覧の表示・追加・編集も可能です。
- アイテム登録時に足りない情報取得（商品名、カテゴリー、メーカー）に以下のサイト様から情報を取得しています。
  `https://www.janken.jp/gadgets/jan/JanSyohinKensaku.php`
  <br>settings.py でオンラインの情報取得を OFF にすることもできます。

### 対応するデータベース

- sqlite3
- 非同期のみ対応(aiosqlite)

### docker で動かす

0. 前提：docker をインストール済み
1. ダウンロードしたディレクトリ内の Dockerfile がある場所で以下のコマンドを実行しイメージを作成します。<br>
   `docker build -t kigen-majika-pyserver:test .`
2. 次のコマンドでイメージを実行<br>
   `docker run -d --init -p 8010:8010 --name kigen-majika-pyserver -it kigen-majika-pyserver:test`
3. 実行できたら URL にアクセスしてください。<br>
   `http://localhost:8010/items`

[TOP](#kigen-majika-pyserver)

### 使い方

#### API で使用する

- 仕様は以下で確認。細かいパラメータチェック等はありません。
  `http://localhost:8010/docs`

[TOP](#kigen-majika-pyserver)

#### HTML で WEB アプリケーションとして使用する

- `http://localhost:8010/items`にアクセスして管理したいアイテムを追加するだけ。
- 追加したアイテムを更新したい場合は登録後の横の編集ボタンから変更できます。

[TOP](#kigen-majika-pyserver)

### 設定

- settings.py で設定を変更することができます。

#### オンラインからの情報取得

- オンラインからの情報取得の ON/OFF を設定できます。
  `GET_INFO_ONLINE = True`

| 設定名          | 説明                              | 値            | デフォルト |
| --------------- | --------------------------------- | ------------- | ---------- |
| GET_INFO_ONLINE | オンラインからの情報取得の ON/OFF | True of False | True       |

[TOP](#kigen-majika-pyserver)

#### アイテム一覧表示における注意度の日にち設定

- HTML によるアイテム一覧表示の注意度の判定に使用する日にちを設定できます。

```
ATTENTION_DISPLAY_FOR_HTML = {
    "DANGEROUS": 0,
    "CAUTION": 30,
    "SOMEWHAT_CAUTION": 183,
}
```

| 設定名           | 説明                     | 値   | デフォルト |
| ---------------- | ------------------------ | ---- | ---------- |
| DANGEROUS        | 危険と表示する残日数     | 数値 | 0          |
| CAUTION          | 注意と表示する残日数     | 数値 | 30         |
| SOMEWHAT_CAUTION | やや注意と表示する残日数 | 数値 | 183        |

[TOP](#kigen-majika-pyserver)
