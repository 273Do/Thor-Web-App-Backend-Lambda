from .applehealthdata import HealthDataExtractor


# export.zipからデータを抽出する
# StepCountとSleepAnalysisのデータを抽出する


def extract_data(export_xml):

    # データの抽出処理
    try:
        # バイナリデータを引数として渡してクラスを初期化
        extractor = HealthDataExtractor(export_xml)
        extractor.extract()

        # DataFrame の取得と表示
        dfs = extractor.get_dataframes()
        step_count_df = dfs['StepCount']
        sleep_analysis_df = dfs['SleepAnalysis']

        return True, None, step_count_df, sleep_analysis_df
    except Exception as e:
        return False, str(e), None, None
