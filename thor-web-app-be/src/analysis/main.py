import pandas as pd

# データ解析用のメイン関数


def data_analyze(step_count_df, sleep_analysis_df):

    print(step_count_df.head())
    print(sleep_analysis_df.head())

    return True, None, None


# テスト用のデータを読み込む
# CSVファイルを読み込む
sc_df = pd.read_csv('./test/StepCountCP.csv')
sa_df = pd.read_csv('./test/SleepAnalysisCP.csv')

data_analyze(sc_df, sa_df)
