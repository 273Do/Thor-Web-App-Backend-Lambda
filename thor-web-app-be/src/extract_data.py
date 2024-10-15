# from .applehealthdata import HealthDataExtractor
import pandas as pd

# export.zipからデータを抽出する
# StepCountとSleepAnalysisのデータを抽出する


def extract_data(export_xml):

    # DataFrameの初期化
    step_count_df = pd.DataFrame()
    sleep_analysis_df = pd.DataFrame()

    # データの抽出処理
    try:
        # print(str(export_xml.decode('utf-8')))
        # print(str(type(export_xml)))
        # print(str(type(export_xml.decode('utf-8'))))

        # postmanの容量制限でエラーが出る
        # data = HealthDataExtractor(export_xml.decode('utf-8'))
        # data.report_stats()
        # data.extract()
        # データの抽出処理
        # ここにデータの抽出処理を追加する

        return True, None, step_count_df, sleep_analysis_df
    except Exception as e:
        return False, str(e), None, None
