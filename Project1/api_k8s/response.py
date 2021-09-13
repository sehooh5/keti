from flask import jsonify


def message(code):
    if code == '0000':
        res = jsonify(
            code=code,
            message="처리 성공"
        )
        return res
    elif code == '0001':
        res = jsonify(
            code=code,
            message="YES"
        )
        return res
    elif code == '0002':
        res = jsonify(
            code=code,
            message="NO"
        )
        return res
    elif code == '0003':
        res = jsonify(
            code=code,
            message="ID 중복 오류"
        )
        return res
    elif code == '0004':
        res = jsonify(
            code=code,
            message="ID 유효성 오류"
        )
        return res
    elif code == '0005':
        res = jsonify(
            code=code,
            message="패스워드 오류"
        )
        return res
    elif code == '0010':
        res = jsonify(
            code=code,
            message="Parsing 오류"
        )
        return res
    elif code == '0011':
        res = jsonify(
            code=code,
            message="데이터베이스 연결 오류"
        )
        return res
    elif code == '0012':
        res = jsonify(
            code=code,
            message="알 수 없는 오류"
        )
        return res
    elif code == '0013':
        res = jsonify(
            code=code,
            message="Invalid 프로토콜 오류"
        )
        return res
    elif code == '0014':
        res = jsonify(
            code=code,
            message="시스템 연동 오류"
        )
        return res
    elif code == '0015':
        res = jsonify(
            code=code,
            message="필수 파라미터 Missing 오류"
        )
        return res
    elif code == '0016':
        res = jsonify(
            code=code,
            message="길이 초과 오류"
        )
        return res
    elif code == '0017':
        res = jsonify(
            code=code,
            message="규격에 없는 필드 오류"
        )
        return res
    elif code == '0018':
        res = jsonify(
            code=code,
            message="날짜포맷 오류"
        )
        return res
    elif code == '0019':
        res = jsonify(
            code=code,
            message="Invalid 코드 값 오류"
        )
        return res
    elif code == '0020':
        res = jsonify(
            code=code,
            message="데이터 Missing 오류"
        )
        return res
    elif code == '0021':
        res = jsonify(
            code=code,
            message="헤더정보 누락 오류"
        )
        return res
    elif code == '9999':
        res = jsonify(
            code=code,
            message="기타 오류"
        )
        return res
