import pandas as pd
import numpy as np
# import joblib
from models_functions import list_models_in_s3, load_model_from_s3
# from src.analysis.models_functions import list_models_in_s3, load_model_from_s3

# 歩数データから特徴量を作成する関数


def create_feature_value(df, habit, time_range):

    # 特徴量となるデータの時間範囲の指定
    start, end = time_range

    # 日付ごとの結果を保存するためのリスト
    results = []

    # データの日付範囲を設定
    unique_dates = pd.date_range(start=df.head(
        1)["startDate"].values[0], end=df.tail(1)["endDate"].values[0]).date

    # 1日毎に処理を繰り返す
    for date in unique_dates:

        # 指定の日付でデータを絞る
        date_df = df[df['startDate'].dt.date == date]

        # 日付ごとの結果を格納する辞書
        daily_result = {}

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

        # 普段の就寝時刻
        daily_result["habit"] = habit

        # 1日の結果をリストに追加
        results.append(daily_result)

    # リストからデータフレームを作成
    feature_value_df = pd.DataFrame(results)

    # csvに出力
    # feature_value_df.to_csv("./test/feature_value.csv")

    return feature_value_df


# 夜更かし検知処理を行う関数
def sleep_prediction(feature_value_df):

    # 14個の学習済みモデルのロード
    # models = []
    # for i in range(14):
    #     # 学習済みモデルをロード
    #     model = joblib.load(f'./models/model_{i+1}.pkl')
    #     models.append(model)
    # モデル一覧を取得し、ロードする

    model_keys = list_models_in_s3()
    models = [load_model_from_s3(key) for key in model_keys]

    # 各モデルで予測を実行
    predictions = []
    for model in models:
        pred = model.predict(feature_value_df)  # 各モデルで予測
        predictions.append(pred)

    # 最終予測結果の集計（投票ベース）
    # 予測結果を多数決で決定
    final_predictions = np.round(np.mean(predictions, axis=0)).astype(int)

    # final_predictions = []
    # for i in range(len(feature_value_df)):
    #     # 各モデルの i 行目の予測を収集
    #     votes = [pred[i] for pred in predictions]
    #     # 最も多くのモデルが予測したクラスを最終予測とする
    #     majority_vote = max(set(votes), key=votes.count)
    #     final_predictions.append(majority_vote)

    # 結果の表示
    results = pd.DataFrame({
        'staying_up_late_prediction': final_predictions  # 1: 夜更かし, 0: 通常
    })

    return results
