import json

def msg(code):

    if code == 0000:
        msg = {
            "code": "0000",
            "message": "처리 성공"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o01:
        msg = {
            "code": "0001",
            "message": "YES"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o02:
        msg = {
            "code": "0002",
            "message": "NO"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o03:
        msg = {
            "code": "0003",
            "message": "ID 중복 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o04:
        msg = {
            "code": "0004",
            "message": "ID 유효성 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0005:
        msg = {
            "code": "0005",
            "message": "패스워드 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o10:
        msg = {
            "code": "0010",
            "message": "Parsing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o11:
        msg = {
            "code": "0011",
            "message": "데이터베이스 연결 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o12:
        msg = {
            "code": "0012",
            "message": "알 수 없는 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o13:
        msg = {
            "code": "0013",
            "message": "Invalid 프로토콜 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o14:
        msg = {
            "code": "0014",
            "message": "시스템 연동 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o15:
        msg = {
            "code": "0015",
            "message": "필수 파라미터 Missing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o16:
        msg = {
            "code": "0016",
            "message": "길이 초과 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o17:
        msg = {
            "code": "0017",
            "message": "규격에 없는 필드 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o18:
        msg = {
            "code": "0018",
            "message": "날짜포맷 "
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o19:
        msg = {
            "code": "0019",
            "message": "Invalid 코드 값 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o20:
        msg = {
            "code": "0020",
            "message": "데이터 Missing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0o21:
        msg = {
            "code": "0021",
            "message": "헤더정보 누락 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 9999:
        msg = {
            "code": "9999",
            "message": "기타 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json