from dateutil.relativedelta import relativedelta

# 補助関数を定義するファイル


# データを最後のレコードから直近のnヶ月前に絞る関数
def narrow_the_data(df, months):

    # データの最後の日の観測時間を取得
    end_date = df.iloc[-1]['startDate']

    # 精査する範囲の最初の日を設定
    start_date = end_date - relativedelta(months=months-1)

    # 設定した月でデータを絞る
    narrow_df = df[(df["startDate"] >= start_date)
                   & (df["startDate"] <= end_date)]

    return narrow_df
