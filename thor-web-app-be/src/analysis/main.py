import pandas as pd
# MEMO: コンテナ内で実行する場合は以下のパスを使用
from auxiliary_functions import narrow_the_data
# from src.analysis.auxiliary_functions import narrow_the_data

# データ解析用のメイン関数


def data_analyze(step_count_df, sleep_analysis_df):

    # "startDate" と "endDate" の列を datetime 型に変換
    for df in [step_count_df, sleep_analysis_df]:
        df['startDate'] = pd.to_datetime(df['startDate'])
        df['endDate'] = pd.to_datetime(df['endDate'])

    # 歩数データを直近3ヶ月間に絞る
    step_count_df = narrow_the_data(step_count_df, 3)

    print(step_count_df.head())
    print(step_count_df.tail())

    # narrow_the_data(sleep_analysis_df, 3)

    return True, None, None


# テスト用のデータを読み込む
# CSVファイルを読み込む

# MEMO: コンテナ内で実行する場合は以下の2列のパスを使用
sc_df = pd.read_csv('./test/StepCountCP.csv', low_memory=False)
sa_df = pd.read_csv(
    './test/SleepAnalysisCP.csv', low_memory=False)
# sc_df = pd.read_csv(
#     './thor-web-app-be/src/analysis/test/SleepAnalysisCP.csv', low_memory=False)
# sa_df = pd.read_csv(
#     './thor-web-app-be/src/analysis/test/SleepAnalysisCP.csv', low_memory=False)

# 必要な列だけを抽出する
sc_df = sc_df[["sourceVersion", "startDate", "endDate", "value"]]
sa_df = sa_df[["sourceVersion", "startDate", "endDate", "value"]]

data_analyze(sc_df, sa_df)
