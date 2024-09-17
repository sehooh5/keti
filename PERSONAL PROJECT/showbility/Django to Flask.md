# Django to Flask

- Dajngo 프로젝트를 Flask 로 전환

Django에서 Flask로 프로젝트를 변경하려면 몇 가지 주요 부분을 변경해야 합니다. Django와 Flask는 구조적으로 다른 웹 프레임워크이므로, 변경 작업은 Django의 기능을 Flask 스타일로 변환하는 작업이 필요합니다. 다음은 전환을 위한 기본 단계를 안내합니다:

### 1. **프로젝트 구조 변경**
   Django는 기본적으로 프로젝트 구조를 강제하지만, Flask는 매우 유연합니다. 따라서 Flask의 프로젝트 구조는 Django에 비해 간단해집니다.

   **Django 프로젝트 구조**:
   ```
   myproject/
       manage.py
       myproject/
           __init__.py
           settings.py
           urls.py
           wsgi.py
       app1/
           models.py
           views.py
           urls.py
           ...
   ```

   **Flask 프로젝트 구조**:
   ```
   myproject/
       app.py
       config.py
       templates/
       static/
       models.py
       views.py
   ```

   여기서 `app.py`는 Flask 애플리케이션의 진입점이 됩니다. `settings.py`와 같은 구성은 `config.py` 파일로 옮기게 됩니다.

### 2. **설정 변경**
   Django는 설정을 `settings.py`에 저장하고 여러 설정 파일을 나누어 사용하지만, Flask에서는 보통 `config.py`에 설정을 작성합니다.

   - **Django 설정 (settings.py)**:
     ```python
     INSTALLED_APPS = ['app1', 'app2']
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'mydb',
             ...
         }
     }
     ```

   - **Flask 설정 (config.py)**:
     ```python
     class Config:
         SECRET_KEY = 'your-secret-key'
         SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/mydb'
         SQLALCHEMY_TRACK_MODIFICATIONS = False
     ```

### 3. **라우팅 변경**
   Django에서는 URL 패턴을 `urls.py`에서 정의하지만, Flask에서는 각 뷰 함수에 데코레이터로 직접 URL을 매핑합니다.

   - **Django URL 설정**:
     ```python
     # urls.py
     from django.urls import path
     from . import views
     
     urlpatterns = [
         path('home/', views.home, name='home'),
     ]
     ```

   - **Flask 라우팅**:
     ```python
     # app.py
     from flask import Flask, render_template
     
     app = Flask(__name__)
     
     @app.route('/home')
     def home():
         return render_template('home.html')
     ```

### 4. **ORM 전환**
   Django는 자체 ORM을 사용하지만, Flask에서는 SQLAlchemy와 같은 외부 ORM을 사용해야 합니다.

   - **Django 모델**:
     ```python
     from django.db import models
     
     class User(models.Model):
         username = models.CharField(max_length=100)
         email = models.EmailField()
     ```

   - **SQLAlchemy 모델 (Flask)**:
     ```python
     from flask_sqlalchemy import SQLAlchemy
     
     db = SQLAlchemy()
     
     class User(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         username = db.Column(db.String(100))
         email = db.Column(db.String(120), unique=True)
     ```

### 5. **템플릿**
   Django 템플릿을 그대로 사용하면서도 Flask로 쉽게 이전할 수 있습니다. Flask 역시 Jinja2 템플릿 엔진을 사용하므로, Django 템플릿의 대부분은 수정 없이 사용할 수 있습니다.

   - **Django 템플릿 사용**:
     ```html
     <!-- Django -->
     <h1>{{ user.username }}</h1>
     ```

   - **Flask 템플릿 사용**:
     ```html
     <!-- Flask -->
     <h1>{{ user.username }}</h1>
     ```

### 6. **폼 및 기타 기능**
   Django의 Form 시스템은 매우 강력하지만, Flask에서는 `WTForms`와 같은 라이브러리를 사용할 수 있습니다.

### 7. **기타 마이그레이션 고려 사항**
   - 인증, 세션 관리 등은 Flask의 확장을 통해 구현해야 합니다. 예를 들어, `Flask-Login`을 사용하여 로그인 시스템을 구현할 수 있습니다.
   - Django의 강력한 관리 기능은 Flask에서는 따로 구현하거나, 필요시 Flask-Admin을 사용할 수 있습니다.

---

Django에서 Flask로 전환하려면 위의 단계들을 따라 각 기능을 수동으로 변환해야 하며, 필요한 라이브러리와 플러그인을 추가해주는 것이 중요합니다. 프로젝트의 복잡성에 따라 전환 작업은 다소 시간이 걸릴 수 있습니다.







---

---

---









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

