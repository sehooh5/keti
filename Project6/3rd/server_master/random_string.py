import random
import string

def generate(length):
    # 숫자와 알파벳(대소문자)을 포함한 모든 문자 집합을 생성
    characters = string.ascii_letters + string.digits
    # 랜덤하게 4개의 문자를 선택하여 문자열을 생성
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string