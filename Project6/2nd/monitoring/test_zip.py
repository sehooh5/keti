import zipfile
import os

file_path = "/home/edge-master-01"
filename = "monitoring.zip"

with zipfile.ZipFile(f"{file_path}/{filename}", "r") as zip_ref:
    for file_info in zip_ref.infolist():
        # 파일이름
        file_name = file_info.filename

        # 압축 해제할 경로 및 파일 경로
        extract_path = os.path.join(file_path, file_name)

        # 이미 파일이 존재하면 덮어쓰기
        if os.path.exists(extract_path):
            os.remove(extract_path)

        # 파일 압축 해제
        zip_ref.extract(file_info, file_path)

print("압축 해제 완료")