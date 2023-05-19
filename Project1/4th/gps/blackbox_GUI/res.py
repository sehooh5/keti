import json

def msg(code):

    if code == 0000:
        msg = {
            "code": "0000",
            "message": "처리 성공"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0001:
        msg = {
            "code": "0001",
            "message": "YES"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0002:
        msg = {
            "code": "0002",
            "message": "NO"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0003:
        msg = {
            "code": "0003",
            "message": "ID 중복 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0004:
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
    elif code == 0010:
        msg = {
            "code": "0010",
            "message": "Parsing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0011:
        msg = {
            "code": "0011",
            "message": "데이터베이스 연결 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0012:
        msg = {
            "code": "0012",
            "message": "알 수 없는 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0013:
        msg = {
            "code": "0013",
            "message": "Invalid 프로토콜 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0014:
        msg = {
            "code": "0014",
            "message": "시스템 연동 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0015:
        msg = {
            "code": "0015",
            "message": "필수 파라미터 Missing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0016:
        msg = {
            "code": "0016",
            "message": "길이 초과 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0017:
        msg = {
            "code": "0017",
            "message": "규격에 없는 필드 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0018:
        msg = {
            "code": "0018",
            "message": "날짜포맷 "
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0019:
        msg = {
            "code": "0019",
            "message": "Invalid 코드 값 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0020:
        msg = {
            "code": "0020",
            "message": "데이터 Missing 오류"
        }
        msg_json = json.dumps(msg)
        return msg_json
    elif code == 0021:
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