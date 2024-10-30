from flask import Flask, jsonify, request
import json
from src.s3_functions import get_fromS3
from src.unzip import unzip
from src.extract_data import extract_data
from src.analysis.main import data_analyze

# FlaskのWebアプリ作成
app = Flask(__name__)

# 解析処理をするエンドポイント


@app.route("/analyze", methods=['POST'])
def analyze():

    # リクエストボディからUUIDを取得
    request_body = request.json
    UUID = request_body.get('UUID')
    file_name = request_body.get('file_name')
    # s3に格納されているデータのディレクトリを指定
    file_dir = f"{UUID}/{file_name}"

    # UUIDが指定されていない場合はエラーを返す
    if not UUID:
        return jsonify({"error": "UUID parameter is required"}), 400
    # ファイル名が指定されていない場合はエラーを返す
    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400

    # メイン処理
    # s3からファイルを取得
    success, error_message, zip_file = get_fromS3(file_dir)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # zipファイルを解凍
    success, error_message, export_xml = unzip(zip_file)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # 3からファイルを削除
    # ここに削除処理を追加する

    # データの抽出
    success, error_message, step_count_df, sleep_analysis_df = extract_data(
        export_xml)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # 解析処理
    success, error_message, analysis_results = data_analyze(
        step_count_df, sleep_analysis_df)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    return jsonify({'message': 'successfully',
                    'body': json.dumps(
                        {
                            'UUID': UUID
                        }
                    )}), 200
