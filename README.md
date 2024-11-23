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

1. Git と Docker Desktop をインストールしてください．

2. 任意のディレクトリで`git clone https://github.com/273Do/Thor.git`を実行してください．
3. 作成されたプロジェクトの`Dockerfile`が存在するディレクトリで，`docker compose build`を実行してください．

4. 引き続き，`docker compose up -d`を実行してください．

5. `docker exec -it thor_web_app_be /bin/bash`を実行してコンテナの中に入ってください．以降はコンテナ内で python3 コマンドを実行していただけます．必要なライブラリは requirements.txt に記載されているものが自動でインストールされますが，必要なライブラリが無いとエラーが吐かれた場合は`pip3`で手動でインストールしてください．

6. コンテナから抜ける場合は`exit`を実行，コンテナを終了させる場合は`docker compose down`を実行してください．

## 🚚 各種関数の説明

## 🚚 免責事項

この作成物および同梱物を使用したことによって生じたすべての障害・損害・不具合等に関しては，私と私の関係者および私の所属するいかなる団体・組織とも，一切の責任を負いません．各自の責任においてご使用ください．
