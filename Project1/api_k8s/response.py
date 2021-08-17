
def response_message(code):
    if code == '0000':
        return "처리성공"
    elif code == '0001':
        return "YES"
    elif code == '0002':
        return "NO"
    elif code == '0003':
        return "ID 중복 오류"
    elif code == '0004':
        return "ID 유효성 오류"
    elif code == '0005':
        return "패스워드 오류"
    elif code == '0010':
        return "Parsing 오류"
    elif code == '0011':
        return "데이터베이스 연결 오류"
    elif code == '0012':
        return "알 수 없는 오류"
    elif code == '0013':
        return "Invalid 프로토콜 오류"
    elif code == '0014':
        return "시스템 연동 오류"
    elif code == '0015':
        return "필수 파라미터 Missing 오류"
    elif code == '0016':
        return "길이 초과 오류"
    elif code == '0017':
        return "규격에 없는 필드 오류"
    elif code == '0018':
        return "날짜포맷 오류"
    elif code == '0019':
        return "Invalid 코드 값 오류"
    elif code == '0020':
        return "데이터 Missing 오류"
    elif code == '0021':
        return "헤더정보 누락 오류"
    elif code == '9999':
        return "기타 오류"
