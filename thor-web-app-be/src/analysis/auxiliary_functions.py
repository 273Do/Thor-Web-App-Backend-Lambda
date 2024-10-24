from dateutil.relativedelta import relativedelta

# 補助関数を定義するファイル


# データを最後のレコードから直近のnヶ月前に絞る関数
def narrow_the_data(df, months):

    # データの最後の日の観測時間を取得
    end_date = df.iloc[-1]['startDate']

    # 精査する範囲の最初の日を設定
    start_date = end_date - relativedelta(months=months-1)

    # 精査する初日の時刻を0時に設定
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # 設定した月でデータを絞る
    narrow_df = df[(df["startDate"] >= start_date)
                   & (df["startDate"] <= end_date)]

    return narrow_df


# 抽出対象を指定してフィルタリングする関数


def filter_data(df, target):

    if (target == "step"):
        # 歩数データを抽出
        filter_df = df[df["device"].str.contains("name:iPhone")]
    elif (target == "sleep"):
        # 睡眠データを抽出
        # MEMO: WatchOS 10以降のデータのみを抽出
        filter_df = df[(df["sourceVersion"].str.contains("10")) & (
            df["value"] == "HKCategoryValueSleepAnalysisInBed")]

    # device列を削除
    filter_df['device'] = filter_df['device'].astype(str)
    filter_df = filter_df.drop("device", axis=1)

    return filter_df
