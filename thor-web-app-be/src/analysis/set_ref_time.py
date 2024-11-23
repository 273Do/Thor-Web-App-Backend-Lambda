import pandas as pd

# 時間帯ごとに睡眠している確率を日毎に配列で指定


def setReferenceTime(weekday_probability, holiday_probability):
    # 結果を格納する配列
    result = []

    # データのパスを指定
    csv_file_path = ["./statistical_data/nhk_investigation_data/sleep_data_weekday.csv",
                     "./statistical_data/nhk_investigation_data/sleep_data_holiday.csv"]

    # 平日/土日の基準/精査先のパーセントに対する時間を設定する処理
    for i, path in enumerate(csv_file_path):

        # 平日/土日の結果を格納する配列
        day_result_list = []

        # CSVファイルを読み込む
        df = pd.read_csv(path, low_memory=False)

        # 入力範囲を知るためパーセントの最大値と最小値を取得

        #  平日/土日の基準/精査先のパーセントを設定
        if (i == 0):
            median_time_probability, edge_time_probability = weekday_probability
        else:
            median_time_probability, edge_time_probability = holiday_probability

        # 基準の%を上回る時間と精査先の%を下回る時間のdfを取得して配列に格納
        median_edge_list = [
            df[df["行為者率(%)"] >= median_time_probability], df[df["行為者率(%)"] <= edge_time_probability]]

        # 基準/精査先ごとに処理を行う
        for (j, data_frame) in enumerate(median_edge_list):

            # 基準/精査先の指定時間を設定
            if (j == 0):
                specified_time = median_time_probability
            else:
                specified_time = edge_time_probability

            # dfの行番号の配列
            median_row_list = list(data_frame.index)

            # 基準/精査先の時間を設定する処理
            for k in range(2):

                if (k == 0):  # 1つ目の基準/精査先のdf
                    standard_percent = data_frame.iloc[0:1]
                    # 基準/精査先の前の時間のdfを取得
                    pre_standard_percent = df.iloc[median_row_list[0] -
                                                   1:median_row_list[0]]
                else:  # 2つ目の基準/精査先のdf
                    standard_percent = data_frame.iloc[len(
                        data_frame)-1:len(data_frame)]
                    # 基準/精査先の後の時間のdfを取得
                    pre_standard_percent = df.iloc[median_row_list[-1] +
                                                   1:median_row_list[-1]+2]

                # 基準/精査先の%と前/後ろの差の絶対値を比較して，値が小さい方を基準値とする
                if (abs(standard_percent["行為者率(%)"].values[0] - specified_time) <= abs(pre_standard_percent["行為者率(%)"].values[0] - specified_time)):
                    set_time = standard_percent["時刻(時間:分)"].values[0]
                else:
                    set_time = pre_standard_percent["時刻(時間:分)"].values[0]

                day_result_list.append(set_time)
        result.append(day_result_list)
    return result


# 処理軽減の為，main関数ではハードコーディングで使用する．
# 平日，休日も94%と4%に範囲を設定
time_range = setReferenceTime([94, 4], [94, 4])
print(time_range)
