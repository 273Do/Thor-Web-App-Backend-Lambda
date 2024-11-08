from dateutil.relativedelta import relativedelta
from datetime import time
import pandas as pd

# 補助関数を定義するファイル


# データを最後のレコードから直近のnヶ月前に絞る関数


def narrow_the_data(df, months):

    # データの最後の日の観測時間を取得
    end_date = df.iloc[-1]["startDate"]

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
        # WatchOS 10以降のデータのみを抽出
        filter_df = df[(df["sourceVersion"].str.contains("10")) & (
            df["value"] == "HKCategoryValueSleepAnalysisInBed")]

    # device列を削除
    filter_df["device"] = filter_df["device"].astype(str)
    filter_df = filter_df.drop("device", axis=1)

    # 最新バージョンのみのレコードを残す
    # filter_df['sourceVersion'] = filter_df['sourceVersion'].apply(
    #     lambda x: int(x.split('.')[0]))  # マイナーバージョンを消してメジャーバージョンのみを取得
    # latest_version = filter_df["sourceVersion"].max()  # 最新のバージョンを取得
    # filter_df = filter_df[filter_df["sourceVersion"] == latest_version]

    return filter_df


# 時間型のデータをjsonに変換する関数


def custom_converter(obj):
    if isinstance(obj, time):
        return obj.strftime("%H:%M:%S")
    raise TypeError(f"Type {type(obj)} not serializable")
# 使い方
# print(json.dumps(result, default=custom_converter, indent=4))


# timedelta を datetime.time に変換する関数


def convert_timedelta_to_time(s):

    total_seconds = int(s.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    converted_time = time(hours, minutes, seconds)

    return converted_time


# 回答から補正値を取得する関数
def get_correction_value(bed_answer, wake_answer):

    # 就寝時の補正値
    bed_cor_list = [56, 104, 90, 99, 102]

    # 起床時の補正値
    wake_cor_list = [57, 90, 66]

    # 選択した補正値を取得
    bed_minutes = bed_cor_list[bed_answer]
    wake_minutes = wake_cor_list[wake_answer]

    # 補正値を取得
    bed_time = pd.to_timedelta(bed_minutes, unit='m')
    wake_time = pd.to_timedelta(wake_minutes, unit='m')

    return [bed_time, wake_time]
