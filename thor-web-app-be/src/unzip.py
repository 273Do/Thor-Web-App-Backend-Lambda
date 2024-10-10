from flask import jsonify
import zipfile
import os
import boto3
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()


# zipファイルを解凍し，export.xmlのみをs3にアップロード


def unzip(file, save_path):
    # zipファイルを開く
    with zipfile.ZipFile(file) as existing_zip:
        # zip内のファイルリストを取得
        file_list = existing_zip.namelist()

        if 'export.xml' in file_list:
            # export.xml を解凍

            # existing_zip.extract('export.xml', path=extract_to_directory)

            return True
        else:
            return False
