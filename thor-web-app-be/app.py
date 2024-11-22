from flask import Flask, jsonify, request
from src.s3_functions import get_fromS3, delete_fromS3
from src.unzip import unzip
from src.extract_data import extract_data
from src.analysis.main import data_analyze
from src.analysis.open_api_functions import generate_feedback

# FlaskのWebアプリ作成
app = Flask(__name__)

# 解析処理をするエンドポイント


@app.route("/analyze", methods=["POST"])
def analyze():

    # リクエストボディからUUIDを取得
    request_body = request.json
    UUID = request_body.get("UUID")
    file_name = request_body.get("file_name")
    habit = request_body.get("habit")
    bed_answer = request_body.get("bed_answer")
    wake_answer = request_body.get("wake_answer")

    # s3に格納されているデータのディレクトリを指定
    file_dir = f"{UUID}/{file_name}"

    # UUIDが指定されていない場合はエラーを返す
    if not UUID:
        return jsonify({"error": "UUID parameter is required"}), 400
    # ファイル名が指定されていない場合はエラーを返す
    if not file_name:
        return jsonify({"error": "file_name parameter is required"}), 400
    # habitが指定されていない場合はエラーを返す
    if not habit:
        return jsonify({"error": "habit parameter is required"}), 400
    # bed_answerが指定されていない場合はエラーを返す
    if not bed_answer:
        return jsonify({"error": "bed_answer parameter is required"}), 400
    # wake_answerが指定されていない場合はエラーを返す
    if not wake_answer:
        return jsonify({"error": "wake_answer parameter is required"}), 400

    # アンケートの回答を格納
    answer = [int(habit), int(bed_answer), int(wake_answer)]

    # メイン処理
    # s3からファイルを取得
    success, error_message, zip_file = get_fromS3(file_dir)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # 3からディレクトリ(ファイル)を削除
    success, error_message = delete_fromS3(UUID)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # zipファイルを解凍
    success, error_message, export_xml = unzip(zip_file)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # データの抽出
    success, error_message, step_count_df, sleep_analysis_df = extract_data(
        export_xml)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # 解析処理
    success, error_message, analysis_results, cluster_stats = data_analyze(
        step_count_df, sleep_analysis_df, answer)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    # ChatGPTによるフィードバック生成
    success, error_message, feedback = generate_feedback(
        analysis_results, cluster_stats)
    if not success:
        return {"status": "failed", "error_message": error_message}, 500

    print("解析結果")
    print(step_count_df)
    print(analysis_results)
    print(cluster_stats)
    print(feedback)

    return jsonify({"message": "successfully",
                    "body":
                        {
                            "result": analysis_results,
                            # "step_count_df": step_count_df,
                            "cluster_stats": cluster_stats,
                            "feedback": feedback,
                            "UUID": UUID
                        }
                    }), 200
