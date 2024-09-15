# Django to Flask

- Dajngo 프로젝트를 Flask 로 전환



### Flask로 전환 및 배포 절차
1. **Flask 프로젝트 생성**
   - Django 프로젝트를 Flask 프로젝트로 전환하려면 먼저 Flask 애플리케이션을 생성해야 합니다. Flask는 `pip`로 설치할 수 있습니다.
   ```bash
   pip install Flask
   ```

   이후 기본적인 Flask 애플리케이션을 설정합니다.
   ```python
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def home():
       return "Hello Flask"
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

2. **Django의 기능을 Flask로 옮기기**
   Django에서 사용한 URL 라우팅, 뷰, 모델 등의 기능을 Flask로 옮겨야 합니다.

   - **URL 라우팅**: Django의 `urls.py`를 Flask의 `@app.route`로 변경.
   - **뷰(Views)**: Django의 `views.py`에서 사용한 함수나 클래스를 Flask의 뷰로 변경.
   - **ORM**: Django의 ORM 대신 SQLAlchemy나 Flask-SQLAlchemy를 사용해 데이터베이스와의 연결을 처리할 수 있습니다.
     ```bash
     pip install Flask-SQLAlchemy
     ```

     이후 모델을 SQLAlchemy로 마이그레이션합니다.
     ```python
     from flask_sqlalchemy import SQLAlchemy
     
     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/db_name'
     db = SQLAlchemy(app)
     
     class User(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         username = db.Column(db.String(80), unique=True, nullable=False)
     ```

3. **React Native (Expo)와의 통신 유지**
   React Native 앱이 Django 백엔드와 통신하고 있었다면, Flask에서도 동일한 API 경로와 동작을 제공해야 합니다.

   - API 라우트는 Flask의 `@app.route`로 정의합니다.
   - **CORS 설정**: React Native와 Flask가 서로 다른 출처에 있을 경우 CORS(Cross-Origin Resource Sharing)를 처리해야 합니다. 이를 위해 `flask-cors` 패키지를 사용합니다.
     ```bash
     pip install flask-cors
     ```

     이후 설정 추가:
     ```python
     from flask_cors import CORS
     CORS(app)
     ```

4. **Django-specific 코드 및 패키지 제거**
   - Django의 기본적인 패키지, 설정 파일 등을 모두 제거하고 Flask에 맞는 패키지로 교체합니다.
   - Django가 제공하는 미들웨어, 인증 기능 등을 Flask에서 직접 구현하거나 Flask의 확장을 사용하여 대체합니다.

5. **백엔드 배포**
   Flask 애플리케이션을 배포하기 위해서는 기존 Django 서버와 동일한 환경에서 Flask 서버를 구동할 수 있습니다. AWS EC2 같은 서버에서 Nginx와 uWSGI를 통해 Flask 애플리케이션을 실행할 수 있습니다.
   - **uWSGI 설정**: Flask를 uWSGI로 실행하도록 설정.
   - **Nginx 설정**: 기존의 Nginx 설정을 Flask 애플리케이션에 맞게 수정합니다.

6. **배포 후 Expo에서 통신 테스트**
   - Flask로 전환한 후 Expo 앱에서 백엔드와의 통신을 테스트합니다.
   - API 경로가 동일하다면 큰 수정 없이 작동할 수 있으며, 경로 변경이 있을 경우 React Native의 API 요청 경로를 수정해야 합니다.

### 장단점
- **장점**: Flask는 가벼운 프레임워크로, Django보다 더 간단하고 유연하게 프로젝트를 관리할 수 있습니다.
- **단점**: Django의 기본 제공 기능들(예: Admin 패널, 인증 시스템 등)을 직접 구현해야 하는 부담이 있습니다.

배포는 충분히 가능하며, Flask는 EC2와 같은 환경에서도 잘 작동합니다.