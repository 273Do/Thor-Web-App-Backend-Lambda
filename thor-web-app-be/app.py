from flask import Flask, jsonify, request
import uuid
import json
from src.s3_functions import uploadS3

# FlaskのWebアプリ作成
app = Flask(__name__)


# POSTリクエストとエンドポイントの設定
@app.route("/get_presigned_url", methods=['POST'])
def main():

    # リクエストにファイルが含まれているか確認
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    # ファイルの取得
    file_name = request.files['file']
    # ファイル名が空か確認
    if file_name.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 一時ファイル名を生成
    UUID = str(uuid.uuid4())  # uuidを生成
    tmp_file = f"{UUID}/{file_name.filename}"

    # s3のプリサインドurlの発行
    success, error_message, presigned_url = uploadS3(tmp_file)
    if success:
        print(presigned_url)
        return jsonify({
            'message': 'successfully',
            'body': json.dumps(
                {
                    'PUT_URL': presigned_url,
                    'UUID': UUID
                }
            )}), 200
    else:
        return {"status": "failed", "error_message": error_message}, 500
