from flask_mail import Message
from flask import current_app
from random import randint, getrandbits
from app import mail  # Flask app에서 mail 인스턴스를 가져옴


def send_mail_with_code(recip_list):
    subject = '쇼빌리티 인증 메일입니다.'
    code = randint(100000, 999999)
    message_body = f'인증번호는 {code} 입니다.'

    msg = Message(subject=subject, recipients=recip_list)
    msg.body = message_body
    with current_app.app_context():
        mail.send(msg)

    return code


def generate_random_hash():
    return str(getrandbits(128))
