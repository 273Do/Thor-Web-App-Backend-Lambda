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


def issue_presigned_url(tmp_file):
    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': tmp_file,
                'ContentType': 'application/zip'
            },
            ExpiresIn=duration_seconds,
            HttpMethod='PUT'
        )
        return True, None, presigned_url
    except Exception as e:
        return False, str(e), None


# s3にアップロードされたzipファイルを取得


def get_fromS3(UUID, file_name):
    try:
        # テスト用のUUIDを取得
        UUID = os.environ['TEST_UUID']

        # s3に格納されているデータのディレクトリを指定
        file_dir = f"{UUID}/{file_name}"

        # s3からzipファイルを取得
        s3_object = s3.get_object(Bucket=bucket_name, Key=file_dir)
        zip_file = s3_object['Body'].read()

        return True, None, zip_file
    except Exception as e:
        return False, str(e), None
