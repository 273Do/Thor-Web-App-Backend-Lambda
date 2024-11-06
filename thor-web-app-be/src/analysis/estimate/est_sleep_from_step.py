import pandas as pd
from datetime import datetime, timedelta
from auxiliary_functions import convert_timedelta_to_time

# 精査範囲(平日，休日)
# 関数setReferenceTimeから取得可能
time_range_list = [["3:00", "4:15", "12:00", "21:00"],
                   ["3:00", "4:45", "12:45", "20:45"]]


# MEMO: 歩数から睡眠を推定する処理


def estimate_sleep_from_step(df, staying_up_late_predictions_df):

    # データの日付範囲を設定
    unique_dates = pd.date_range(
        start=df["startDate"].iloc[0].date(), end=df["startDate"].iloc[-1].date()).date

    # 結果格納用の辞書
    result = {}

    # 1日毎に処理を繰り返す
    for i, date in enumerate(unique_dates):
        # NOTE: 睡眠の定義
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

            # 推定処理を実行して結果を取得
            sleep_detail = staying_up_late_sleep_estimation(
                day_step_count_df, time_range, 1)

            # print(sleep_detail)

        else:
            # 夜更かししていない場合の推定処理

            # その日と前日の歩数データを取得
            day_step_count_df = df[(df["startDate"].dt.date == date) |
                                   (df["startDate"].dt.date == (date - timedelta(days=1)))].sort_values("startDate")

            # 推定処理を実行して結果を取得
            sleep_detail = normal_sleep_estimation(
                day_step_count_df, time_range)
            # print(sleep_detail)

        # 結果を格納
        result[date.strftime('%Y/%m/%d')] = sleep_detail


# MEMO: 夜更かししている場合の推定処理


def staying_up_late_sleep_estimation(df, time_range, cluster_id):

    # 精査するデータの時間範囲の指定
    start, *_, end = time_range[0], time_range[3]

    # 精査範囲のデータを取得
    df = df[(df["endDate"].dt.time >= pd.to_datetime(f"{start}:00").time()) &
            (df["startDate"].dt.time <= pd.to_datetime(f"{end}:00").time())]

    # 初期値
    pre_endDate = pd.to_datetime(f"{start}:00").time()
    tmp = timedelta()  # 初期値は0秒

    # 結果格納用の辞書
    result = {}

    # その日の歩数データごとに処理を繰り返す
    for _, row in df.iterrows():

        # pre_endDate > 現在の startDate の場合はスキップ（複数端末への対応）
        if pre_endDate > row["startDate"].time():
            continue

        # pre_endDate と startDate の時間差(睡眠時間)を計算
        pre_end_datetime = datetime.combine(datetime.today(), pre_endDate)
        start_datetime = datetime.combine(
            datetime.today(), row["startDate"].time())
        current_sleep = start_datetime - pre_end_datetime

        # 現在の時間差が最大の時間差より大きい場合は更新
        if current_sleep > tmp:
            tmp = current_sleep

            # timedelta を datetime.time に変換
            converted_tmp = convert_timedelta_to_time(tmp)

            # 最新の睡眠時間を格納
            result = {
                "bed_time": pre_end_datetime.time(),
                "wake_time": start_datetime.time(),
                "sleep_time": converted_tmp
            }

        # endDate を更新
        pre_endDate = row["endDate"].time()

        # 外出検知の場合はスキップ
        if row["cluster"] == cluster_id:
            break

    # 夜更かししているフラグとデータ数を格納
    result["staying_up_late"] = True
    result["data_count"] = len(df)

    return result


# MEMO: 夜更かししていない場合の推定処理


def normal_sleep_estimation(df, time_range):

    # 前日，当日の取得
    unique_dates = df["startDate"].dt.date.unique()

    # 精査するデータの時間範囲の指定
    bed_end, wake_start, wake_end, bed_start = time_range

    # 精査範囲のデータを取得
    # 就寝時刻の精査データは前日から当日のデータ
    bed_df = df[((df["startDate"] >= pd.Timestamp(unique_dates[0].isoformat() + f" {bed_start}:00+09:00")) &
                 (df["startDate"] <= pd.Timestamp(unique_dates[1].isoformat() + f" {bed_end}:00+09:00")))]

    # 起床時刻の精査データは当日のデータ
    wake_df = df[((df["startDate"] >= pd.Timestamp(unique_dates[1].isoformat() + f" {wake_start}:00+09:00")) &
                 (df["startDate"] <= pd.Timestamp(unique_dates[1].isoformat() + f" {wake_end}:00+09:00")))]

    # 就寝時刻の推定
    if bed_df.empty:
        bed_time = pd.to_datetime(f"{bed_end}:00").time()
    else:
        bed_time = bed_df["endDate"].max().time()

    # 起床時刻の推定
    if wake_df.empty:
        wake_time = pd.to_datetime(f"{wake_start}:00").time()
    else:
        wake_time = wake_df["startDate"].min().time()

    # 睡眠時間の計算
    if bed_time > wake_time:

        # 日を跨がない場合は24時間を足して差分を計算
        current_sleep = datetime.combine(
            datetime.today(), wake_time) - datetime.combine(datetime.today(), bed_time) + timedelta(days=1)
    else:

        # 日を跨ぐ場合はそのまま差分を計算
        current_sleep = datetime.combine(
            datetime.today(), wake_time) - datetime.combine(datetime.today(), bed_time)
    converted_sleep = convert_timedelta_to_time(current_sleep)

    # 結果を辞書に格納
    result = {
        "bed_time": bed_time,
        "wake_time": wake_time,
        "sleep_time": converted_sleep,
        "staying_up_late": False,
        "data_count": len(df)
    }

    return result
