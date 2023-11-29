import zipfile
import os

file_path = "/home/edge-master-01"
filename = "monitoring.zip"

zip_file_path = "/home/edge-master-01/monitoring.zip"


try:
    # Zip 파일 열기
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 압축 해제
        zip_ref.extractall('/monitoring')
    print(f"Zip file '{zip_file_path}' successfully extracted to '{extract_path}'.")
except zipfile.BadZipFile as e:
    print(f"Error: {zip_file_path} is not a valid zip file. {e}")
except Exception as e:
    print(f"Error extracting zip file: {e}")