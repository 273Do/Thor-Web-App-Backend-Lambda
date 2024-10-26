import pandas as pd


def staying_up_late_model(time_range, df):
    start, end = time_range

    step_sum_count = {}
    for hour in range(start, end):

        start_time_v = pd.to_datetime(f"{hour}:00")
        end_time_v = pd.to_datetime(f"{hour+1}:00")
        print(start_time_v, end_time_v)

        # # 時間範囲を指定
        # range_df = df[(
        #     df["startDate"].dt.time >= start_time_v.time()) & (df["startDate"].dt.time <= end_time_v.time())]
        # step_sum_count[f"sumValue_{hour}_{hour+1}"] = range_df[range_df['startDate'].dt.date == date]['value'].sum(
        # )
        # step_sum_count[f"valueCount_{hour}_{hour+1}"] = range_df[
        #     range_df['startDate'].dt.date == date].shape[0]
    pass
