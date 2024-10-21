import pandas as pd

# 補助関数を定義するファイル


# データを最後のレコードから直近の月数に絞る関数
def narrow_the_data(df, months):

    # 開始と終了を初期化
    start_date = 0
    end_date = 0

    # 指定の日付範囲でフィルタリング
    # df = df[(df["startDate"] >= time["time"]["start_date"])
    #         & (df["endDate"] <= time["time"]["end_date"])]

    # データの最後を取得
    df_last = df.iloc[-1]

    print(df_last['startDate'])

    # 最後のデータの月を取得
    end_date = df_last['startDate']

    print(end_date)

    # 精査するデータの範囲を月単位で設定
    # if (end_date.month - months) < 0:
    #     start_date = end_date - months + 13
    # else:
    #     start_date = end_date - months + 1

    if (end_date.month - months) < 0:
        start_date = 0

    print(start_date, end_date)

    # 設定した月でデータを絞る

    narrow_df = df[(df["startDate"] >= start_date)]
    #    & (df["startDate"] <= end_date)]
    print(narrow_df.head())
    print(narrow_df.tail())

    pass
