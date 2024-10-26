from staying_up_late_model import create_feature_value, sleep_prediction

# 歩数から睡眠を推定する処理


def estimate(step_df, time_range):

    # 歩数データから特徴量を作成
    # habit:普段の就寝時刻(事前アンケート)3時以前を０，3時以降を1
    feature_value_df = create_feature_value(step_df, 0, [0, 12])

    # 推定処理の実行(予測の実行)
    staying_up_late_predictions = sleep_prediction(feature_value_df)

    print(staying_up_late_predictions)
    print("予測結果")

    # その日が夜更かしをしているかどうかを機械学習モデルから推定
    is_staying_up_late = False

    if (is_staying_up_late):
        # 夜更かししている場合の推定処理
        pass
    else:
        # 夜更かししていない場合の推定処理
        pass
    return None
