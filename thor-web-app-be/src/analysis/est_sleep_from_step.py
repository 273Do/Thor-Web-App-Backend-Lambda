import pandas as pd

# 歩数から睡眠を推定する処理


def estimate_sleep_from_step(df, time_range, staying_up_late_predictions):

    # time_range = [["3:00", "4:15", "12:00", "21:00"],
    #               ["3:00", "4:45", "12:45", "20:45"]]

    # データの日付範囲を設定
    unique_dates = pd.date_range(
        start=df["startDate"].iloc[0], end=df["startDate"].iloc[-1]).date

    # 1日毎に処理を繰り返す
    for date in unique_dates:
        print(date)

        # その日が夜更かしをしているかどうかを判断するフラグ
        is_staying_up_late = False

        if (is_staying_up_late):
            # 夜更かししている場合の推定処理
            pass
        else:
            # 夜更かししていない場合の推定処理
            pass
