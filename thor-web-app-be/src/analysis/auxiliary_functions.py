import pandas as pd

# 補助関数を定義するファイル


# データを最後のレコードから直近の月数に絞る関数
def narrow_the_data(df, months):

    # 開始月と終了月を初期化
    start_month = 0
    end_month = 0

    # 指定の日付範囲でフィルタリング
    # df = df[(df["startDate"] >= time["time"]["start_date"])
    #         & (df["endDate"] <= time["time"]["end_date"])]

    # データの最後を取得
    df_last = df.iloc[-1]

    print(df_last['startDate'])
    print(type(df_last['startDate']))

    # 最後のデータの月を取得
    end_month = df_last['startDate'].month

    print(end_month)

    # 精査するデータの範囲を月単位で設定
    if (end_month - months) < 0:
        start_month = end_month - months + 13
    else:
        start_month = end_month - months + 1

    print(start_month, end_month)

    # 設定した月でデータを絞る

    pass
