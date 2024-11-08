# MEMO: コンテナ内で実行する場合は以下のパスを使用
from ML.staying_up_late_model import create_feature_value, staying_up_late_prediction
from estimate.est_sleep_from_step import estimate_sleep_from_step
# from src.analysis.ML.staying_up_late_model import create_feature_value, staying_up_late_prediction
# from src.analysis.estimate.est_sleep_from_step import estimate_sleep_from_step

# 歩数から睡眠を推定するメイン処理


def estimate(step_count_df, answer):

    # アンケートの回答を取得
    habit, bed_answer, wake_answer = answer

    # 歩数データから特徴量を作成
    feature_value_df = create_feature_value(step_count_df, habit, [0, 12])

    # 推定処理の実行(予測の実行)
    # その日が夜更かしをしているかどうかを機械学習モデルから推定
    staying_up_late_predictions_df = staying_up_late_prediction(
        feature_value_df)

    # 歩数から睡眠を推定する処理
    estimate_sleep_df = estimate_sleep_from_step(
        step_count_df, staying_up_late_predictions_df, bed_answer, wake_answer)

    return estimate_sleep_df
