# ZIPファイルを解凍


def unzip():
    pass

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
