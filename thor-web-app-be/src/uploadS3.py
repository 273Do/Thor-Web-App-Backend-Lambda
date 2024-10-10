import shutil
import os
import boto3
import zipfile
import os
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()

# s3のクライアントを作成
s3 = boto3.client('s3')

# s3のバケット名
bucket_name = os.environ['AWS_S3_BUCKET_NAME']

# s3へアップロードする関数


def uploadS3(file, save_path):
    try:
        # s3へのアップロード処理
        s3.upload_fileobj(file, bucket_name, save_path)
        return True, None
    except Exception as e:
        return False, str(e)

# s3でzipファイルを解凍する関数


def unzipS3():
    try:
        # s3へのアップロード処理
        extract_to_path = os.path.dirname(os.path.abspath(__file__))
        print(extract_to_path)
    except Exception as e:
        return False, str(e)


def uploadS3_2(file, save_path):
    try:
        extract_to_path = os.path.dirname(os.path.abspath(__file__))
        # s3へのアップロード処理
        s3.upload_file(file, bucket_name, save_path + "/export.xml")
        # ローカルのファイルを削除
        shutil.rmtree(extract_to_path + "/tmp/" + save_path +
                      "/apple_health_export")

        return True, None
    except Exception as e:
        return False, str(e)
