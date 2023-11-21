
# AI 수정 부분, docker image tag 추출하는 부분
import subprocess
import json
import re

def get_docker_image_tags(docker_id, fname):
    # Docker 이미지 정보 추출
    result = subprocess.run(['docker', 'images'], capture_output=True, text=True)
    output_text = result.stdout

    # 정규 표현식 패턴 = 해당 이미지의 태그
    pattern = re.compile(fr'{docker_id}/{fname}\s+(\d+)\s+')

    # 매칭된 결과 중 작은값 가져오기
    matches = pattern.findall(output_text)

    # 매칭된 결과 출력
    print(matches)

    # JSON 문자열을 파이썬 객체로 파싱
    try:
        tags = json.loads(result.stdout)
        return tags
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None

# 사용 예제
docker_id = 'sehooh5'
fname = 'monitoring'
tags = get_docker_image_tags(docker_id, fname)

if tags:
    print(f"Tags for image '{image_name}': {tags}")
else:
    print(f"Failed to retrieve tags for image '{image_name}'.")