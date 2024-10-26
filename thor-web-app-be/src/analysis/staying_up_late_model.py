import pandas as pd

# 歩数データから特徴量を作成する関数


def create_feature_value(time_range, df):

    # 特徴量となるデータの時間範囲の指定
    start, end = time_range

    # 日付ごとの結果を保存するためのリスト
    results = []

    # データの日付範囲を設定
    unique_dates = pd.date_range(start=df.head(
        1)["startDate"].values[0], end=df.tail(1)["endDate"].values[0]).date

    # 1日毎に処理を繰り返す
    for i, date in enumerate(unique_dates):

        # 指定の日付でデータを絞る
        date_df = df[df['startDate'].dt.date == date]

        # 日付ごとの結果を格納する辞書
        daily_result = {"date": date}

        # 1時間毎に処理を繰り返す
        for hour in range(start, end):

            start_time = pd.to_datetime(f"{hour}:00")
            end_time = pd.to_datetime(f"{hour+1}:00")

            # 指定の時間範囲でデータを絞る
            hour_df = date_df[(date_df['startDate'].dt.time >= start_time.time()) &
                              (date_df['startDate'].dt.time <= end_time.time())]

            # 1時間の歩数の合計とデータ数を取得
            sum_value = hour_df["value"].sum()
            count_value = hour_df.shape[0]

            # 結果を辞書に格納（キーの名前は sumValue_*_* と valueCount_*_*）
            daily_result[f"sumValue_{hour}_{hour + 1}"] = sum_value
            daily_result[f"valueCount_{hour}_{hour + 1}"] = count_value

        # 1日の結果をリストに追加
        results.append(daily_result)

    # リストからデータフレームを作成
    feature_value_df = pd.DataFrame(results)

    # csvに出力
    feature_value_df.to_csv("./test/feature_value.csv")

    return feature_value_df


# 夜更かし検知処理を行う関数
