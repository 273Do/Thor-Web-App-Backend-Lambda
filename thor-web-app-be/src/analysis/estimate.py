# MEMO: コンテナ内で実行する場合は以下のパスを使用
# from ML.staying_up_late_model import create_feature_value, staying_up_late_prediction
# from est_sleep_from_step import estimate_sleep_from_step
from src.analysis.ML.staying_up_late_model import create_feature_value, staying_up_late_prediction
from src.analysis.est_sleep_from_step import estimate_sleep_from_step

# 歩数から睡眠を推定するメイン処理


def estimate(step_df, time_range, habit):

    # 歩数データから特徴量を作成
    feature_value_df = create_feature_value(step_df, habit, [0, 12])

    # 推定処理の実行(予測の実行)
    # その日が夜更かしをしているかどうかを機械学習モデルから推定
    staying_up_late_predictions = staying_up_late_prediction(feature_value_df)

    print(step_df[["startDate", "cluster"]])
    print(staying_up_late_predictions)

    # 歩数から睡眠を推定する処理
    estimate_sleep_from_step(step_df, time_range, staying_up_late_predictions)

    # その日が夜更かしをしているかどうかを判断するフラグ
    is_staying_up_late = False

    if (is_staying_up_late):
        # 夜更かししている場合の推定処理
        pass
    else:
        # 夜更かししていない場合の推定処理
        pass
    return None
