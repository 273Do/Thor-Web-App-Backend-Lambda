<p align="center">
<img width="120" src="./imgs/Thor.png">
</p>

# Thor-Web-App-BE

- 本 web アプリは，本研究のアルゴリズムや推定処理を誰でも利用できるようにするとともに，結果を AI を用いてフィードバックできるようにするものである．また，ローカルで解析を行うこともできる．

- 本リポジトリでは，アプリの目に見えない処理の部分を実装しており，基本的には全て AWS 上で動作するようになっている．環境変数さえ用意すればローカルでも動かすことができる．関数単位で細かく処理を分けているため，研究ソースコードよりかなりわかりやすい．

- [フロントエンドリポジトリ](https://github.com/273Do/Thor-Web-App-Frontend)

## 🚚 開発環境・使用技術・ツール

<!-- <H3>x日間(1日あたりy~z時間)</H3> -->

<H3>BE
<div>
<img alt="Python" src="https://img.shields.io/badge/-Python-000?style=flat&logo=Python&logoColor=3776AB" />
 <img alt="Flask" src="https://img.shields.io/badge/-Flask-000?style=flat&logo=flask&logoColor=FFFFFF" />
</div>

<h3>環境，コード管理
<div>
 <img alt="Docker" src="https://img.shields.io/badge/-Docker-000?style=flat&logo=Docker&logoColor=46a2f1" />
 <img alt="GitHub" src="https://img.shields.io/badge/-GitHub-000?style=flat&logo=GitHub&logoColor=FFFFFF" />
<img alt="Git" src="https://img.shields.io/badge/-Git-000?style=flat&logo=Git&logoColor=F05032" />
</div>

<h3>外部サービス
<div>
 <img alt="Google Docs" src="https://img.shields.io/badge/-Google Docs-000?style=flat&logo=googledocs&logoColor=4285F4" />
 <img alt="OpenAI API" src="https://img.shields.io/badge/-OpenAI API-000?style=flat&logo=openai&logoColor=ffffff" />
</div>

<h3>ストレージ，デプロイ
<div>
<img alt="AWS S3" src="https://img.shields.io/badge/-AWS S3-000?style=flat&logo=amazons3&logoColor=569A31" />
  <img alt="AWS Lambda" src="https://img.shields.io/badge/-AWS Lambda-000?style=flat&logo=awslambda&logoColor=FF9900" />
  <img alt="AWS EC2" src="https://img.shields.io/badge/-AWS EC2-000?style=flat&logo=amazonec2&logoColor=FF9900" />
  <img alt="Serverless" src="https://img.shields.io/badge/-Serverless-000?style=flat&logo=serverless&logoColor=FD5750" />
</div>

<h3>ロゴ
<div>
  <img alt="Blender" src="https://img.shields.io/badge/-Blender-000?style=flat&logo=Blender&logoColor=E87D0D" />
  <img alt="Adobe Photoshop" src="https://img.shields.io/badge/-Adobe Photoshop-000?style=flat&logo=Adobe Photoshop&logoColor=31A8FF" />
</div>

## 🚚 システム構成図

<img src="./imgs/system_architecture.png">

## 🚚 動作確認済み端末・OS

- macOS Sequoia 15.0
- AWS Lmabda，AWS EC2

## 🚚 アプリ構築・起動

> 環境構築について記載しています．本番環境でも基本的には同じです．

<details><summary>環境構築</summary>

### 環境構築

1. Git と Docker Desktop をインストールしてください．

2. 任意のディレクトリで`git clone https://github.com/273Do/Thor.git`を実行してください．

3. ルートディレクトリと`thor-web-app-beディレクトリ`に`.env`ファイルを作成し，環境変数を設定してください．(内容については開発者に問い合わせください．)
4. 作成されたプロジェクトの`Dockerfile`が存在するディレクトリで，`docker compose build`でイメージを作成してください．

5. 引き続き，`docker compose up -d`でコンテナを起動してください．

6. `docker exec -it thor_web_app_be /bin/bash`を実行してコンテナの中に入ってください．

7. `aws configure`で aws cli の設定をしてください．

8. 以降はコンテナ内で python3 コマンドを実行していただけます．必要なライブラリは requirements.txt に記載されているものが自動でインストールされますが，必要なライブラリが無いとエラーが吐かれた場合は`pip3`で手動でインストールしてください．

9. コンテナから抜ける場合は`exit`を実行，コンテナを終了させる場合は`docker compose down`を実行してください．
</details>

## 🚚 API 利用手順

> API の利用手順について記載しています．本番では`http://localhost:5000`ではなく正しいエンドポイントを使用してください．

<details><summary>ローカル環境でのアプリの実行</summary>

1.  REST API のテストができるようなツールを導入してください．  
    VSCode の拡張機能版 Postman，Thunder Client などを入れるといいです．

2.  アプリのリクエスト順序通りに API を叩いていきます．

<summary>API 利用手順</summary>

## 1. 署名付き URL を発行

### HTTP リクエスト

| 項目   | 内容                                         |
| ------ | -------------------------------------------- |
| Method | POST                                         |
| URL    | `http://localhost:5000/get_presigned_url`    |
| Header | `Content-Type: application/json`             |
| Body   | [json]`{"file_name": "書き出したデータ.zip"} |

### レスポンス

- UUID とアップロード用の URL が返されます．

---

## 2. 署名付き URL を使用して ZIP を送信

### HTTP リクエスト

| 項目   | 内容                            |
| ------ | ------------------------------- |
| Method | PUT                             |
| URL    | 先ほど取得した URL              |
| Header | `Content-Type: application/zip` |
| Body   | [binary]ZIP ファイル            |

### レスポンス

- アップロードが成功すれば，`200` ステータスが返されます．

---

## 3. 解析処理を要求する

### HTTP リクエスト

| 項目   | 内容                                 |
| ------ | ------------------------------------ |
| Method | POST                                 |
| URL    | `http://localhost:5000/analysis`     |
| Header | `Content-Type: application/json`     |
| Body   | [json]                               |
|        | `{                                   |
|        | "UUID": "先ほど取得した UUID",       |
|        | "file_name": "書き出したデータ.zip", |
|        | "habit": "x",                        |
|        | "bed_answer": "y",                   |
|        | "wake_answer": "z"                   |
|        | }`                                   |

※リクエスト内容

- `habit`: 夜更かししたかどうか (x：`0` or `1`)
- `bed_answer`: アンケート回答 (y：`0〜4`)
- `wake_answer`: アンケート回答 (z：`0〜2`)

### レスポンス

- 解析結果が返されます．

---

</details>
     
</details>

## 🚚 ブランチの説明

`develop`：以下のソースコードまとめてがアップロードされています．  
`feature/#12_only_lambda_functions`：AWS Lambda に搭載するソースコード(署名付き URL の取得)がアップロードされています．  
`feature/#13_only_ec2_functions`：AWS EC2 に搭載するソースコード(解析処理やフィードバック処理)がアップロードされています．

## 🚚 各種関数の説明

実装した関数の解説を記載しています．

### `./App.py`

<details><summary>API関連の関数をまとめている．</summary>

| 関数   | `get_presigned_ur()`                                                 |
| ------ | -------------------------------------------------------------------- |
| 役割   | HTTP リクエストを受け取り，署名付き url を取得してレスポンスを返す． |
| 引数   | なし                                                                 |
| 返り値 | ステータスメッセージ，署名付き URL，UUID                             |

| 関数   | `analyze()`                                                          |
| ------ | -------------------------------------------------------------------- |
| 役割   | HTTP リクエストを受け取り，解析処理を実行してレスポンスを返す．      |
| 引数   | なし                                                                 |
| 返り値 | ステータスメッセージ，睡眠推定結果，歩数クラスタ情報，フィードバック |

</details>

<hr>

### `./src/applehealthdata.py`

<details><summary>applehealthdataを一部改変したもの．</summary>

| 役割     | export.xml から必要なデータを抽出するためのクラス．一部改変している． |
| -------- | --------------------------------------------------------------------- |
| ソース元 | [**applehealthdata**](https://github.com/tdda/applehealthdata)        |

```
extractor = HealthDataExtractor(export_xml)
extractor.extract()

dfs = extractor.get_dataframes()
```

</details>

### `./src/extract_data.py`

<details><summary>applehealthdataを用いてデータを抽出，加工する処理．</summary>

| 関数     | `extract_data(export_xml)`                                                     |
| -------- | ------------------------------------------------------------------------------ |
| 役割     | `export.xml`から必要なデータを抽出して DateFrame にする．                      |
| 第１引数 | `export.xml`のバイナリデータ                                                   |
| 返り値   | 処理が成功したかどうか，エラー文，歩数の DataFrame，正解睡眠データの DateFrame |

</details>

### `./src/open_api_functions.py`

<details><summary>フィードバック生成関連の関数をまとめたもの．</summary>

| 関数     | `generate_feedback(estimate_sleep_df, cluster_stats)`    |
| -------- | -------------------------------------------------------- |
| 役割     | 推定結果から OpenAI API を使用してフィードバックを返す． |
| 第１引数 | 睡眠推定データの DataFrame                               |
| 第２引数 | 歩数クラスタ情報                                         |
| 返り値   | 処理が成功したかどうか，エラー文，フィードバック         |

| 関数   | `get_prompt()`                                       |
| ------ | ---------------------------------------------------- |
| 役割   | Google Docs からプロンプトを取得する．               |
| 引数   | なし                                                 |
| 返り値 | 処理が成功したかどうか，エラー文，各プロンプトの配列 |

</details>

### `./src/s3_functions.py`

<details><summary>S3関連の関数をまとめたもの．</summary>

| 関数     | `issue_presigned_url(tmp_file)`                                         |
| -------- | ----------------------------------------------------------------------- |
| 役割     | S3 の署名付き url を発行する．                                          |
| 第１引数 | UUID と zip ファイル名を組み合わせたもの．S3 に保存されるディレクトリ． |
| 返り値   | 処理が成功したかどうか，エラー文，S3 の署名付き url                     |

| 関数     | `get_fromS3(file_dir)`                                         |
| -------- | -------------------------------------------------------------- |
| 役割     | S3 にアップロードされた zip ファイルを取得する．               |
| 第１引数 | S3 に保存されるている zip ファイルのパス．                     |
| 返り値   | 処理が成功したかどうか，エラー文，zip ファイルのバイナリデータ |

| 関数     | `delete_fromS3(dir)`                                             |
| -------- | ---------------------------------------------------------------- |
| 役割     | S3 にアップロードされた zip ファイルをディレクトリごと削除する． |
| 第１引数 | S3 に保存されるている zip ファイルのディレクトリ(UUID)．         |
| 返り値   | 処理が成功したかどうか，エラー文                                 |

</details>

### `./src/unzip.py`

<details><summary>zipファイルを解凍する処理．</summary>

| 関数     | `unzip(zip_file)`                                              |
| -------- | -------------------------------------------------------------- |
| 役割     | zip ファイルをメモリ上に解凍する．                             |
| 第１引数 | zip ファイルのバイナリデータ                                   |
| 返り値   | 処理が成功したかどうか，エラー文，`export.xml`のバイナリデータ |

</details>

<hr>

## 🚚 クレジット・免責事項

- 開発：273\*
- This source code contains a partially modified version of [**applehealthdata**](https://github.com/tdda/applehealthdata) .
- この作成物および同梱物を使用したことによって生じたすべての障害・損害・不具合等に関しては，私と私の関係者および私の所属するいかなる団体・組織とも，一切の責任を負いません．各自の責任においてご使用ください．
