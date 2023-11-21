# file path 및 zip 파일에서 fname 추출하는 방법 테스트
# str = "/home/edge-master-01/monitoring.zip".split('/')[-1]
# if str.find("zip") != -1:
#     str = str.split('.')[0]
#
# print(str)


# AI 수정 부분, docker image tag 추출하는 부분

import subprocess
import json

def get_docker_image_tags(image_name):
    # Docker 이미지 정보를 JSON 형식으로 얻기
    result = subprocess.run(['docker', 'image', 'inspect', '--format', '{{json .RepoTags}}', image_name], capture_output=True, text=True)

    # JSON 문자열을 파이썬 객체로 파싱
    try:
        tags = json.loads(result.stdout)
        return tags
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None

# 사용 예제
image_name = 'sehooh5/monitoring'
tags = get_docker_image_tags(image_name)

if tags:
    print(f"Tags for image '{image_name}': {tags}")
else:
    print(f"Failed to retrieve tags for image '{image_name}'.")