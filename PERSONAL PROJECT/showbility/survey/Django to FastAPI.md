# Django to FastAPI



## 쇼빌 프로젝트에 적용

### 1. 루트 파일들

- manage.py

  : FastAPI에는 관리 명령어를 위한 manage.py가 없지만, 주로 실행 스크립트가 

  ```
  main.py
  ```

  로 대체됩니다.

  - **변환**: `main.py`로 FastAPI 앱을 실행하는 스크립트를 작성합니다.

- requirements.txt

  : FastAPI와 관련된 의존성들을 추가해야 합니다.

  - **추가**: `fastapi`, `uvicorn`, `SQLAlchemy`, `asyncpg` (Supabase 사용 시)

### 2. `ShowbilityBackend`

#### `asgi.py`, `wsgi.py`

- ASGI/WAGI 서버

  : FastAPI는 ASGI 서버를 사용합니다. 

  ```
  uvicorn
  ```

  을 통해 FastAPI 앱을 실행합니다.

  - **변환**: `main.py` 파일에서 FastAPI 앱을 정의하고, `uvicorn.run()`으로 실행합니다.

#### `urls.py`

- 변환

  : Django의 URL 패턴은 FastAPI의 

  ```
  APIRouter
  ```

  로 대체됩니다.

  - **변환**: 기존 URL 패턴들을 FastAPI의 `router`로 정의하고, `main.py`에서 `app.include_router(router)`로 추가합니다.

#### `settings/`

- base.py, local.py, prod.py

  : Django의 설정 파일들은 FastAPI에서는 단일 환경 파일로 대체할 수 있습니다. 환경 설정은 

  ```
  .env
  ```

   파일이나 Pydantic 설정을 사용합니다.

  - **변환**: FastAPI에서는 `pydantic`을 사용해 환경 변수를 로드하고 `settings.py`로 대체할 수 있습니다.

### 3. `backend/`

#### `models.py`

- 변환

  : Django ORM에서 SQLAlchemy ORM으로 변환합니다.

  - **Supabase**: SQLAlchemy ORM과 PostgreSQL을 연동하여 Supabase와 통신합니다. 각 모델을 SQLAlchemy로 재작성합니다.

#### `serializers.py`

- 변환

  : Django의 시리얼라이저는 FastAPI의 Pydantic 모델로 대체됩니다.

  - **변환**: 각 데이터 검증 및 직렬화 기능을 Pydantic 모델로 변환해 `schemas.py` 파일로 작성합니다.

#### `views.py`

- 변환

  : FastAPI에서는 각 뷰 함수가 API 엔드포인트가 됩니다.

  - **변환**: `views.py`에 있는 함수들을 FastAPI의 엔드포인트로 변환하고 `@app.get`, `@app.post` 등을 사용해 라우팅합니다.

#### `managers.py`

- 변환

  : Django의 커스텀 매니저 로직은 FastAPI에서는 서비스 계층이나 CRUD 로직으로 전환합니다.

  - **변환**: SQLAlchemy 쿼리와 함께 서비스 계층이나 함수로 옮깁니다.

#### `auth/`

- 변환

  : 인증 관련 로직은 FastAPI의 OAuth2 또는 JWT 인증 모듈로 대체할 수 있습니다.

  - **변환**: Apple 로그인 등 OAuth2 관련 코드를 FastAPI에서 사용할 수 있도록 수정합니다.

### 4. `migrations/`

- 대체

  : FastAPI에서는 

  ```
  alembic
  ```

  을 사용해 데이터베이스 마이그레이션을 처리합니다.

  - **변환**: Supabase를 사용할 경우, 직접 SQLAlchemy 모델을 기반으로 마이그레이션을 설정합니다.

### 5. `utils/`

- 유틸리티 코드

  : 이메일, 예외 처리, 슬랙 웹훅 등의 유틸리티 함수들은 FastAPI에서도 유사하게 사용할 수 있습니다.

  - **변환**: 각 유틸리티 코드를 FastAPI 프로젝트의 유틸리티 폴더로 이동하여 사용합니다.

### 예시 구조 (전환 후)

```
bash코드 복사project_root/
│  main.py
│  .env
│  requirements.txt
├─app/
│  ├─routers/
│  │      auth.py
│  │      category.py
│  ├─models/
│  │      user.py
│  ├─schemas/
│  │      user.py
│  ├─crud/
│  │      user.py
│  └─utils/
│         email.py
│         exceptionhandler.py
│         slack_webhook.py
└─migrations/
       env.py
```

이렇게 파일들을 FastAPI 구조로 변환한 후, Supabase와 연결하여 배포 준비를 진행할 수 있습니다.





---



### 1. **프로젝트 구조 재설정**

- FastAPI는 Django와 달리 MVC 패턴을 따르지 않으며, 경량화된 웹 프레임워크입니다. 먼저 기존 Django 프로젝트 구조를 FastAPI의 디렉토리 구조로 변경해야 합니다. 주요 디렉토리는 다음과 같습니다:
  - `main.py`: FastAPI 애플리케이션이 정의되는 곳.
  - `models.py`: 데이터베이스 모델을 정의.
  - `routers/`: API 경로들을 모듈화하여 저장.
  - `schemas.py`: Pydantic을 사용한 데이터 검증 및 직렬화 정의.

### 2. **Django ORM에서 SQLAlchemy로 마이그레이션**

Django는 ORM을 기본으로 사용하지만, FastAPI는 SQLAlchemy와 같은 외부 ORM을 사용합니다.

- Django의 `models.py`에서 SQLAlchemy를 사용하는 방식으로 변환.
- Django에서 사용하던 모델 필드를 SQLAlchemy의 필드로 바꿔야 하며, 이를 위해 기존 모델을 분석하고 새로운 모델로 작성합니다.

```
python코드 복사from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
```

### 3. **Django Forms 및 Validators 대체**

Django의 `forms.py`에서 사용하는 폼 및 유효성 검사 기능을 FastAPI의 Pydantic 모델로 대체합니다.

- Pydantic은 FastAPI에서 데이터를 검증하고 직렬화하는 역할을 합니다.

```
python코드 복사from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
```

### 4. **Django Views에서 FastAPI 경로로 전환**

- Django의 뷰 함수와 클래스 기반 뷰를 FastAPI의 엔드포인트로 변환합니다.
- FastAPI에서는 경로를 `@app.get`, `@app.post` 등의 데코레이터로 정의합니다.

```
python코드 복사from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}
```

### 5. **템플릿 및 정적 파일 처리**

- Django 템플릿 시스템은 Jinja2로 변환이 가능합니다.
- FastAPI는 Jinja2를 쉽게 사용할 수 있으므로, 템플릿 폴더 구조를 유지한 채 Jinja2 설정을 추가합니다.
- Django의 `STATIC_URL`과 `MEDIA_URL` 처리 방식을 FastAPI의 `StaticFiles`를 사용하여 구현할 수 있습니다.

```
python코드 복사from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 6. **사용자 인증 및 권한 관리**

- Django에서 제공하는 기본 인증 시스템(로그인, 로그아웃, 인증 미들웨어 등)을 FastAPI로 마이그레이션합니다.
- FastAPI에서는 OAuth2, JWT를 이용하여 인증 기능을 구현할 수 있습니다.
- Flask-JWT-Extended, FastAPI의 `OAuth2PasswordBearer` 등을 사용하여 인증 및 권한 관리를 구축할 수 있습니다.

```
python코드 복사from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

### 7. **마이그레이션과 데이터베이스 연결**

- Django에서 사용하는 마이그레이션 툴인 `makemigrations`, `migrate` 대신, FastAPI에서는 Alembic을 사용하여 데이터베이스 스키마 변경을 관리합니다.

```
bash


코드 복사
alembic init alembic
```

### 8. **테스트 및 디버깅**

- 전환 후 각 기능별로 테스트 코드를 작성하고, FastAPI의 자체 문서화 기능(Swagger)을 통해 API 테스트 및 디버깅을 진행합니다.

### 9. **배포 준비**

- FastAPI 프로젝트를 Uvicorn과 같은 ASGI 서버로 배포합니다.
- 기존 Django에서 배포에 사용된 방법(예: Nginx, uWSGI)도 FastAPI로 적용 가능하지만, Uvicorn과 함께 Nginx를 사용하는 것이 더 적합할 수 있습니다.