import os
import boto3
import zipfile
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


def uploadS3(tmp_file):
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


# s3にアップロードされたzipファイルを取得して解凍する処理


def unzipS3(UUID, file_name):
    try:
        # テスト用のUUIDを取得
        UUID = os.environ['TEST_UUID']

        # s3に格納されているデータのディレクトリを指定
        file_dir = f"{UUID}/{file_name}"

        print("file_dir", file_dir)

        # s3からzipファイルを取得
        s3_object = s3.get_object(Bucket=bucket_name, Key=file_dir)
        zip_content = s3_object['Body'].read()

        # ZIPファイルを解凍
        # with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as z:
        #     file_list = z.namelist()
        #     print(file_list)

        #     export_xml_path = None
        #     for file_name in file_list:
        #         if file_name.endswith('export.xml'):
        #             export_xml_path = file_name
        #             break

        #     if export_xml_path:
        #         with z.open(export_xml_path) as xml_file:
        #             file_content = io.BytesIO(xml_file.read())
        #             file_content.seek(0)
        #             return True, None, file_content.read()
        #     else:
        #         return False, "export.xml not found", None
        return True, None, UUID
    except Exception as e:
        return False, str(e), None
