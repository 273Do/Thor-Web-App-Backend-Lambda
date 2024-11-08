import pandas as pd
# MEMO: コンテナ内で実行する場合は以下のパスを使用
from auxiliary_functions import narrow_the_data, filter_data
from ML.clustering import clustering
from estimate.estimate import estimate
# from src.analysis.auxiliary_functions import narrow_the_data, filter_data
# from src.analysis.ML.clustering import clustering
# from src.analysis.estimate.estimate import estimate


# データ解析用のメイン関数


def data_analyze(step_count_df, sleep_analysis_df, answer):

    # "startDate" と "endDate" の列を datetime 型に変換
    for df in [step_count_df, sleep_analysis_df]:
        df["startDate"] = pd.to_datetime(df["startDate"])
        df["endDate"] = pd.to_datetime(df["endDate"])

    # step_count_dfの "value" カラムを数値型に変換（変換できない値は NaN にする）
    step_count_df["value"] = pd.to_numeric(
        step_count_df["value"], errors="coerce")

    # 歩数データと睡眠データを直近3ヶ月間に絞る
    step_count_df = narrow_the_data(step_count_df, 3)
    sleep_analysis_df = narrow_the_data(sleep_analysis_df, 3)

    # 抽出対象を指定してフィルタリング
    step_count_df = filter_data(step_count_df, "step")
    sleep_analysis_df = filter_data(sleep_analysis_df, "sleep")

    # 正解データがあるかどうかのフラグ
    hasActSleep = True
    if sleep_analysis_df.empty:
        hasActSleep = False

    # 歩数のクラスタリング処理
    step_count_df, cluster_stats = clustering(step_count_df)
    print(cluster_stats)
    print(step_count_df)

    # 睡眠推定処理
    # habit:普段の就寝時刻(事前アンケート)3時以前を０，3時以降を1
    estimate_sleep_df = estimate(step_count_df, answer)

    print("推定結果")
    print(estimate_sleep_df)

    return True, None, None


# テスト用のデータを読み込む
# CSVファイルを読み込む

# MEMO: コンテナ内で実行する場合は以下の2列のパスを使用
sc_df = pd.read_csv("./test/StepCountCP.csv", low_memory=False)
sa_df = pd.read_csv("./test/SleepAnalysisCP.csv", low_memory=False)
# sc_df = pd.read_csv(
#     "./thor-web-app-be/src/analysis/test/SleepAnalysisCP.csv", low_memory=False)
# sa_df = pd.read_csv(
#     "./thor-web-app-be/src/analysis/test/SleepAnalysisCP.csv", low_memory=False)

# 必要な列だけを抽出する
sc_df = sc_df[["sourceVersion", "device", "startDate", "endDate", "value"]]
sa_df = sa_df[["sourceVersion", "device", "startDate", "endDate", "value"]]

data_analyze(sc_df, sa_df, [0, 3, 0])
