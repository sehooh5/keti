# file path 및 zip 파일에서 fname 추출하는 방법 테스트
# str = "/home/edge-master-01/monitoring.zip".split('/')[-1]
# if str.find("zip") != -1:
#     str = str.split('.')[0]
#
# print(str)


## /docker/getImageTag AI 수정 부분, docker image tag 추출하는 부분

# import subprocess
# import json
# import re
#
# def get_image_tags(docker_id, fname):
#     # Docker 이미지 정보 추출
#     result = subprocess.run(['docker', 'images'], capture_output=True, text=True)
#     output_text = result.stdout
#
#     # 정규 표현식 패턴 = 해당 이미지의 태그
#     pattern = re.compile(fr'{docker_id}/{fname}\s+(\d+)\s+')
#
#     # 매칭된 결과 중 작은값 가져오기
#     matches = pattern.findall(output_text)
#
#     # 매칭된 결과 출력
#     return matches
#
#
# # 사용 예제
# docker_id = 'sehooh5'
# fname = 'monitoring2'
# tag_list = get_docker_image_tags(docker_id, fname)
#
# print(f"Tag List : {tag_list}")


## get_image_tags() 사용 테스트

# from docker import getImageTag as git
# docker_id = 'sehooh5'
# fname = 'monitoring'
# tag_list = git.get_image_tags(docker_id, fname)
#
# if len(tag_list) >= 1:
#     for tag in tag_list:
#         print(f'{docker_id}/{fname}:{tag}')


## get_selectedClusterInfo 요청 오류 발생 테스트
# import requests
# res = requests.get("http://123.214.186.244:4880/get_selectedClusterInfo?id=655c1e0f8e3c4787585c6836")
#
# print(res)

## zip 파일 풀기 예재
import zipfile
import os

file_path = "/home/edge-master-01"
filename = "monitoring.zip"

zip_file_path = "/home/edge-master-01/monitoring.zip"


try:
    # Zip 파일 열기
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 압축 해제
        zip_ref.extractall('monitoring')
    print(f"Zip file '{zip_file_path}' successfully extracted to '/monitoring'.")
except zipfile.BadZipFile as e:
    print(f"Error: {zip_file_path} is not a valid zip file. {e}")
except Exception as e:
    print(f"Error extracting zip file: {e}")