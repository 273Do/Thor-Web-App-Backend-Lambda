# ベースイメージとして，PythonとNode.jsがインストールされた公式のDebianイメージをdockerhubから使用
FROM debian:bullseye

# パッケージの更新と基本ツールのインストール
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    unzip

# Node.jsの最新バージョンをインストール（オプション）
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# AWS CLIのインストール
RUN pip3 install awscli --upgrade

# Werkzeugのインストール
RUN pip3 install werkzeug

# virtualenvのインストール
RUN pip3 install virtualenv

# Serverless Frameworkのインストール
RUN npm install -g serverless serverless-plugin-existing-s3

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# PythonおよびNode.js、AWS CLIのバージョン確認
RUN python3 --version && pip3 --version && node -v && npm -v && aws --version

# 必要なパッケージをインストールするためのrequirements.txtとpackage.jsonをコピー
COPY requirements.txt ./
COPY package.json ./

# Pythonパッケージをインストール
RUN pip3 install --no-cache-dir -r requirements.txt

# Node.jsパッケージをインストール
RUN npm install

# アプリケーションのエントリーポイント（必要に応じて変更）
CMD ["bash"]
