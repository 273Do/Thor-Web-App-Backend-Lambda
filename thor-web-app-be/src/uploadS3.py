import os
import boto3
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
