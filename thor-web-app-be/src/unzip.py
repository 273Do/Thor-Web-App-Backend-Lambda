import os
import zipfile
import io

# zipファイルを解凍


def unzip(zip_file):
    try:
        # zipファイルをメモリ上に解凍
        with zipfile.ZipFile(io.BytesIO(zip_file)) as z:
            file_list = z.namelist()

            # apple_health_export/export.xmlが含まれているか確認
            for file_name in file_list:
                if 'apple_health_export/export.xml' in file_name:

                    # export.xmlを取得
                    export_xml = z.read(file_name)
                    return True, None, export_xml
                else:
                    return False, "export.zip not found", None
    except Exception as e:
        return False, str(e), None
