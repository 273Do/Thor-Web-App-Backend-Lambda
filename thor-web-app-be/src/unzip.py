import os
import zipfile
from io import BytesIO

# zipファイルを解凍し，export.xmlのみをs3にアップロード


def unzip(file):
    try:
        # zipファイルを開く
        with zipfile.ZipFile(file) as upload_zip:
            # zip内のファイルリストを取得
            file_list = upload_zip.namelist()
            print(file_list)

            export_xml_path = None
            for file_name in file_list:
                if file_name.endswith('export.xml'):  # パス内にexport.xmlが含まれているか
                    export_xml_path = file_name
                    break

            # export.xml が見つかれば，そのファイルのデータを返す
            if export_xml_path:
                with upload_zip.open(export_xml_path) as xml_file:
                    # print("export.xml found")
                    # print(xml_file.read())
                    file_content = BytesIO(xml_file.read())
                    file_content.seek(0)
                    # print(file_content)
                    return True, None, file_content.read()  # うまくいかない
            else:
                return False, "export.xml not found", None

            # export.xml が存在するかチェック
            # if '*/export.xml' in file_list:
            #     # export.xml のデータをメモリ上で取得
            #     with upload_zip.open('export.xml') as xml_file:
            # return True, None, xml_file.read()  # ファイルの内容をバイト形式で返す
            # else:
            #     return False, "export.xml not found", None
    except Exception as e:
        return False, str(e), None

# zipファイルを解凍し，export.xmlのみを抽出しローカルに保存


def unzip_local(file, save_path):
    extract_to_path = os.path.dirname(os.path.abspath(__file__))
    try:
        # zipファイルを開く
        with zipfile.ZipFile(file) as upload_zip:

            for item in upload_zip.namelist():

                # .csvファイルのみを解凍
                if item.endswith('.xml'):

                    # ファイルを一時保存するディレクトリを作成
                    upload_zip.extract(
                        item, extract_to_path + "/tmp/" + save_path)

                    return True, None, extract_to_path + "/tmp/" + save_path + "/" + item
            else:
                return False, "export.xml not found", None

    except Exception as e:
        return False, str(e), None
