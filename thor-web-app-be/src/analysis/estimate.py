from staying_up_late_model import create_feature_value

# 歩数から睡眠を推定する処理


def estimate(step_df, time_range):

    # 夜更かしモデルを使用して夜更かししているかどうかを判定
    feature_value = create_feature_value([0, 12], step_df)
    print(feature_value)

    # その日が夜更かしをしているかどうかを機械学習モデルから推定
    is_staying_up_late = False

    if (is_staying_up_late):
        # 夜更かししている場合の推定処理
        pass
    else:
        # 夜更かししていない場合の推定処理
        pass
    return None
