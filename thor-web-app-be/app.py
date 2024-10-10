from flask import Flask, jsonify, request
import boto3
import uuid
import os
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()

# s3のバケット名
bucket_name = os.environ['AWS_S3_BUCKET_NAME']

# s3のクライアントを作成
s3 = boto3.client('s3')

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

    # ファイルのアップロード処理
    try:
        # s3へのディレクトリの作成
        tmp_dir = str(uuid.uuid4())
        save_path = tmp_dir + "/" + file.filename

        # s3へのアップロード処理
        s3.upload_fileobj(file, bucket_name, save_path)
        return jsonify(message='File uploaded successfully : ' + save_path), 200

    except Exception as e:
        # エラーが発生した場合はエラーメッセージを返す
        return jsonify({"error": str(e)}), 500
