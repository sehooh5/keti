# Installed : Flask-SQLAlchemy, Flask-Mail, Flask-JWT-Extended

import os
import datetime


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key')

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'Asia/Seoul'

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    PERSONAL_IMAGE_PATH = "personal/images/"
    CONTENT_IMAGE_PATH = "content/images/"
    CATEGORY_IMAGE_PATH = "category/images/"
    GROUP_IMAGE_PATH = "group/images/"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SOCIAL_AUTH_CONFIG = {
        'KAKAO_REST_API_KEY': os.environ.get('KAKAO_REST_API_KEY', '6b8d1e6614938f7ca9726eb568445228'),
        'KAKAO_REDIRECT_URI': 'http://127.0.0.1:5000/user/social_callback',
        'KAKAO_GET_AUTH_URL': 'https://kauth.kakao.com/oauth/authorize',
        'KAKAO_GET_TOKEN_URL': 'https://kauth.kakao.com/oauth/token',
        'KAKAO_AGREED_INFO_URL': 'https://kapi.kakao.com/v2/user/scopes',
        'KAKAO_USER_INFO_URL': 'https://kapi.kakao.com/v2/user/me',
        'KAKAO_DISCONNECT_URL': 'https://kapi.kakao.com/v1/user/unlink'
    }

    STATIC_FOLDER = "/home/ubuntu/static/"

    # Flask에서는 ALLOWED_HOSTS가 필요 없지만, 보안을 위해 추가 설정이 필요할 수 있음

## 해당 부분은 Slack 으로 예외처리 메시지 보내는 부분인데 일단 안함
    # Slack setting for exception
#    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'ShowbilityBackend.backend.utils.exceptionhandler.custom_exception_handler'

    # DB : Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('DJANGO_DB_USER')}:{os.environ.get('DJANGO_DB_PASSWORD')}@localhost/{os.environ.get('DJANGO_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 이메일 설정
## 추가적으로 Flask-email 설치 후 핸들링해줘야함
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_HOST_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_MAIL_SENDER = MAIL_USERNAME

    # JWT 설정 (Flask-JWT-Extended)
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # 로깅 설정
    LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs/flask.log')
    LOG_FILE_ACCESS = os.path.join(os.path.dirname(__file__), 'logs/access/access.log')

    @staticmethod
    def init_app(app):
        # 로깅 설정을 추가
        import logging
        from logging.handlers import RotatingFileHandler

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

        # 콘솔 로깅
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

        # 파일 로깅
        file_handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        access_file_handler = RotatingFileHandler(Config.LOG_FILE_ACCESS, maxBytes=1024 * 1024 * 5, backupCount=5)
        access_file_handler.setLevel(logging.INFO)
        access_file_handler.setFormatter(formatter)
        app.logger.addHandler(access_file_handler)


# Apple 인증 설정
APPLE_MEMBER_ID = os.environ.get('APPLE_MEMBER_ID')
APPLE_KEY_ID = os.environ.get('APPLE_KEY_ID')
APPLE_CERT_KEY_PATH = os.environ.get('APPLE_CERT_KEY_PATH')

with open(APPLE_CERT_KEY_PATH) as key_file:
    APPLE_CERT_KEY = ''.join(key_file.readlines())

APPLE_CONFIG = {
    "client_id": "com.showbility.app.Showbility",
    "secret": APPLE_KEY_ID,
    "key": APPLE_MEMBER_ID,
    "certificate_key": APPLE_CERT_KEY
}



class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
