import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()

# s3のバケット名
bucket_name = os.environ['AWS_S3_BUCKET_NAME']

# プリサインドurlの有効期間
duration_seconds = int(os.environ['DURATION_SECONDS'])

# リージョンの設定
region = os.environ['AWS_DEFAULT_REGION']

# s3のクライアントを作成
s3 = boto3.client('s3', region_name=region,
                  config=Config(signature_version='s3v4'))

# s3のプリサインドurlの発行処理


def uploadS3(save_path):
    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': save_path,
                'ContentType': 'application/zip'
            },
            ExpiresIn=duration_seconds,
            HttpMethod='PUT'
        )
        return True, None, presigned_url
    except Exception as e:
        return False, str(e), None


# s3にアップロードされたzipファイルを取得して解凍する処理
def unzipS3():
    print("unzipS3")
