import pandas as pd
from datetime import datetime, timedelta, time

# 精査範囲(平日，休日)
# 関数setReferenceTimeから取得可能
time_range_list = [["3:00", "4:15", "12:00", "21:00"],
                   ["3:00", "4:45", "12:45", "20:45"]]


# 歩数から睡眠を推定する処理


def estimate_sleep_from_step(df, staying_up_late_predictions_df):

    # データの日付範囲を設定
    unique_dates = pd.date_range(
        start=df["startDate"].iloc[0].date(), end=df["startDate"].iloc[-1].date()).date

    # 結果格納用の辞書
    result = {}

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

        # その日が平日かどうかを判断するフラグ
        is_weekday = date.weekday() < 5
        if (is_weekday):
            # 平日の場合
            print(i, date, "平日")
            time_range = time_range_list[0]

        else:
            # 休日の場合
            print(i, date, "休日")
            time_range = time_range_list[1]

        # 歩数から睡眠を推定
        if (is_staying_up_late):
            # 夜更かししている場合の推定処理

            # その日の歩数データを取得
            day_step_count_df = df[(df["startDate"].dt.date == date)].sort_values(
                "startDate")
            sleep_detail = staying_up_late_sleep_estimation(
                day_step_count_df, time_range, 1)
            # print(sleep_detail)
            result[date.strftime('%Y/%m/%d')] = sleep_detail
            print(sleep_detail)

        else:
            # 夜更かししていない場合の推定処理
            sleep_detail = normal_sleep_estimation()

    # 補正処理


# 夜更かししている場合の推定処理


def staying_up_late_sleep_estimation(df, time_range, cluster_id):

    # print("---夜更かししている")

    # 精査するデータの時間範囲の指定
    start, *_, end = time_range[0], time_range[3]

    # 精査範囲のデータを取得
    df = df[(df["endDate"].dt.time >= pd.to_datetime(f"{start}:00").time()) &
            (df["startDate"].dt.time <= pd.to_datetime(f"{end}:00").time())]

    # print(start, end)

    # 初期値
    pre_endDate = pd.to_datetime(f"{start}:00").time()
    tmp = timedelta()  # 初期値は0秒

    # 結果格納用の辞書
    result = {}

    # その日の歩数データごとに処理を繰り返す
    for _, row in df.iterrows():
        # print(row["startDate"].time(), row["endDate"].time(), row["cluster"])

        # pre_endDate > 現在の startDate の場合はスキップ（複数端末への対応）
        if pre_endDate > row["startDate"].time():
            # print("スキップ")
            continue

        # pre_endDate と startDate の時間差を計算
        pre_end_datetime = datetime.combine(datetime.today(), pre_endDate)
        start_datetime = datetime.combine(
            datetime.today(), row["startDate"].time())
        current_diff = start_datetime - pre_end_datetime

        # print(pre_end_datetime.time(), start_datetime.time())

        # 現在の時間差が最大の時間差より大きい場合は更新
        if current_diff > tmp:
            # print("更新")
            tmp = current_diff

            # timedelta を datetime.time に変換
            total_seconds = int(tmp.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            # datetime.time オブジェクトを作成
            converted_tmp = time(hours, minutes, seconds)

            # 最新の睡眠時間を格納
            result = {
                "bed_time": pre_end_datetime.time(),
                "wake_time": start_datetime.time(),
                "sleep_time": converted_tmp
            }

        # endDate を更新
        pre_endDate = row["endDate"].time()

        # デバッグ情報の出力
        # print(current_diff)
        # print(f"Updated tmp: {tmp}, Updated pre_endDate: {pre_endDate}")
        # print("-----")

        # 外出検知の場合はスキップ
        if row["cluster"] == cluster_id:
            # print("外出検知")
            break

    result["staying_up_late"] = True
    result["data_count"] = len(df)

    # print("結果")
    # print(result)

    return result

# 夜更かししていない場合の推定処理


def normal_sleep_estimation():
    print("夜更かししていない")
