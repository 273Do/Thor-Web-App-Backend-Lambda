import os
import boto3
from botocore.client import Config
import joblib
from io import BytesIO
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()

# s3のバケット名
model_bucket = os.environ['AWS_S3_MODEL_BUCKET_NAME']


# リージョンの設定
region = os.environ['AWS_DEFAULT_REGION']

# s3のクライアントを作成
s3 = boto3.client('s3', region_name=region,
                  config=Config(signature_version='s3v4'))


# S3内のモデル一覧を取得する


def list_models_in_s3():
    response = s3.list_objects_v2(Bucket=model_bucket)
    model_keys = [item['Key'] for item in response.get('Contents', [])]
    return model_keys


# S3からモデルファイルを取得してロードする関数


def load_model_from_s3(model_key):
    # S3からモデルを取得し，BytesIOでメモリに読み込む
    response = s3.get_object(Bucket=model_bucket, Key=model_key)
    model_bytes = response['Body'].read()
    model = joblib.load(BytesIO(model_bytes))  # メモリ上でロード
    return model
