from flask import Flask, jsonify, request
import uuid
import os
from src.unzip import unzip
from src.uploadS3 import uploadS3

# FlaskのWebアプリ作成
app = Flask(__name__)


# POSTリクエストとエンドポイントの設定
@app.route("/", methods=['POST'])
def main():
    # リクエストにファイルが含まれているか確認
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    # ファイルの取得
    file = request.files['file']
    # ファイル名が空か確認
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # メイン処理
    # s3へのディレクトリの作成
    tmp_dir = str(uuid.uuid4())
    save_path = tmp_dir + "/" + file.filename

    # s3へのアップロード処理
    success, error_message = uploadS3(file, save_path)
    if not success:
        return jsonify({"error": error_message}), 500
    else:
        return jsonify({"message": "Success"}), 200
