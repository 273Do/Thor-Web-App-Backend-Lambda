from flask import Flask, jsonify, request
import uuid
import json
from src.s3_functions import issue_presigned_url

# FlaskのWebアプリ作成
app = Flask(__name__)


# 署名付きurlを発行するエンドポイント


@app.route("/get_presigned_url", methods=['GET'])
def get_presigned_url():

    # クエリパラメータからファイル名を取得
    file_name = request.args.get('file_name')

    # ファイル名が指定されていない場合はエラーを返す
    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # 一時ファイル名を生成
    UUID = str(uuid.uuid4())  # uuidを生成
    tmp_file = f"{UUID}/{file_name}"

    # s3のプリサインドurlの発行
    success, error_message, presigned_url = issue_presigned_url(tmp_file)
    if success:
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
