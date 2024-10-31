import pandas as pd

# 歩数から睡眠を推定する処理


def estimate_sleep_from_step(df, time_range, staying_up_late_predictions_df):

    # time_range = [["3:00", "4:15", "12:00", "21:00"],
    #               ["3:00", "4:45", "12:45", "20:45"]]

    # データの日付範囲を設定
    unique_dates = pd.date_range(
        start=df["startDate"].iloc[0].date(), end=df["startDate"].iloc[-1].date()).date

    # 1日毎に処理を繰り返す
    for i, date in enumerate(unique_dates):
        # MEMO: 睡眠の定義
        # どこからどこまでをその日の睡眠と定義するか
        # -> 前日の21時(5 %)から翌日の21時まで

        # レコードの最初の日はスキップする
        if (i == 0):
            continue

        # その日が夜更かしをしているかどうかを判断するフラグ
        is_staying_up_late = staying_up_late_predictions_df[
            staying_up_late_predictions_df["date"].dt.date == date]["staying_up_late_prediction"].item()

        print(i, date)

        # 歩数から睡眠を推定
        if (is_staying_up_late):
            # 夜更かししている場合の推定処理
            print("夜更かししている")
            pass
        else:
            print("夜更かししていない")
            # 夜更かししていない場合の推定処理
            pass

        # 補正処理
