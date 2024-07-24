import subprocess
import json
import re

# AI update에서 docker image tag 추출하는 부분
def get_image_tags(docker_id, fname):
    # Docker 이미지 정보 추출
    result = subprocess.run(['docker', 'images'], capture_output=True, text=True)
    output_text = result.stdout

    # 정규 표현식 패턴 = 해당 이미지의 태그
    pattern = re.compile(fr'{docker_id}/{fname}\s+(\d+)\s+')

    # 매칭된 결과 중 작은값 가져오기
    matches = pattern.findall(output_text)

    # 매칭된 결과 출력
    return matches

