# Django to FastAPI

Django 프로젝트를 FastAPI와 Turso로 마이그레이션하는 과정은 여러 단계로 나눌 수 있습니다. 다음은 파일 변경 순서와 방법에 대한 가이드입니다:

### 1단계: 프로젝트 구조 설정

1. **FastAPI 프로젝트 초기화**  
   - 새로운 FastAPI 프로젝트를 생성합니다.
   - 필요한 라이브러리를 설치합니다:
     ```bash
     pip install fastapi uvicorn sqlalchemy turso
     ```

2. **디렉토리 구조 설정**  
   ```plaintext
   your_project/
   ├── app/
   │   ├── main.py
   │   ├── models.py
   │   ├── crud.py
   │   ├── routers/
   │   ├── schemas/
   │   ├── config.py
   │   └── utils.py
   └── requirements.txt
   ```

### 2단계: 모델 정의

3. **Django 모델을 SQLAlchemy 모델로 변환**  
   - 기존 Django 모델을 SQLAlchemy 모델로 변환합니다.
   - `models.py` 파일에 SQLAlchemy ORM을 사용하여 모델을 정의합니다.
   ```python
   from sqlalchemy import Column, Integer, String, DateTime
   from sqlalchemy.ext.declarative import declarative_base
   
   Base = declarative_base()
   
   class User(Base):
       __tablename__ = 'users'
   
       id = Column(Integer, primary_key=True, index=True)
       username = Column(String, unique=True, index=True)
       email = Column(String, unique=True, index=True)
       # 필요한 다른 필드 추가
   ```

### 3단계: CRUD 기능 구현

4. **CRUD 함수 정의**  
   - `crud.py` 파일에 CRUD 기능을 구현합니다.
   ```python
   from sqlalchemy.orm import Session
   from .models import User
   from .schemas import UserCreate
   
   def create_user(db: Session, user: UserCreate):
       db_user = User(**user.dict())
       db.add(db_user)
       db.commit()
       db.refresh(db_user)
       return db_user
   
   def get_user(db: Session, user_id: int):
       return db.query(User).filter(User.id == user_id).first()
   ```

### 4단계: 스키마 정의

5. **Pydantic 스키마 정의**  
   - `schemas.py` 파일에 Pydantic 스키마를 정의합니다.
   ```python
   from pydantic import BaseModel
   
   class UserBase(BaseModel):
       username: str
       email: str
   
   class UserCreate(UserBase):
       password: str
   
   class User(UserBase):
       id: int
   
       class Config:
           orm_mode = True
   ```

### 5단계: 라우터 설정

6. **라우터 설정**  
   - `routers` 폴더에 사용자 라우터를 생성합니다.
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from .. import crud, models, schemas
   from ..database import get_db
   
   router = APIRouter()
   
   @router.post("/users/", response_model=schemas.User)
   def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
       return crud.create_user(db=db, user=user)
   ```

### 6단계: 데이터베이스 설정

7. **Turso 데이터베이스 설정**  
   - `config.py` 파일에 Turso 데이터베이스 연결 설정을 추가합니다.
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   
   SQLALCHEMY_DATABASE_URL = "turso://<YOUR_TURSO_DATABASE_URL>"
   engine = create_engine(SQLALCHEMY_DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   ```

### 7단계: 의존성 주입

8. **데이터베이스 세션 관리**  
   - `utils.py` 파일에 데이터베이스 세션 관리 함수를 추가합니다.
   ```python
   from sqlalchemy.orm import Session
   from .database import SessionLocal
   
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```

### 8단계: FastAPI 앱 설정

9. **FastAPI 애플리케이션 설정**  
   - `main.py` 파일에서 FastAPI 애플리케이션을 설정합니다.
   ```python
   from fastapi import FastAPI
   from .routers import user
   
   app = FastAPI()
   
   app.include_router(user.router)
   ```

### 9단계: 배포 준비

10. **애플리케이션 실행**  
   - FastAPI 애플리케이션을 실행하여 모든 것이 제대로 작동하는지 확인합니다.
   ```bash
   uvicorn app.main:app --reload
   ```

### 10단계: 추가 기능 구현

11. **기타 기능 이식**  
   - Django에서 사용하던 나머지 기능 (인증, 소셜 로그인 등)을 FastAPI로 이식합니다. 이를 위해 FastAPI의 보안 모듈을 활용할 수 있습니다.

### 마무리

이 단계들을 따라 기존 Django 프로젝트를 FastAPI와 Turso로 마이그레이션할 수 있습니다. 각 단계에서는 코드와 문서화를 잘 유지하여, 필요에 따라 리팩토링할 수 있도록 해주세요. 추가적인 질문이 있다면 언제든지 물어보세요!





---



Django 프로젝트를 FastAPI로 전환하는 단계는 다음과 같습니다.

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
from sqlalchemy import Column, Integer, String
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
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
```

### 4. **Django Views에서 FastAPI 경로로 전환**

- Django의 뷰 함수와 클래스 기반 뷰를 FastAPI의 엔드포인트로 변환합니다.
- FastAPI에서는 경로를 `@app.get`, `@app.post` 등의 데코레이터로 정의합니다.

```
from fastapi import FastAPI

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
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 6. **사용자 인증 및 권한 관리**

- Django에서 제공하는 기본 인증 시스템(로그인, 로그아웃, 인증 미들웨어 등)을 FastAPI로 마이그레이션합니다.
- FastAPI에서는 OAuth2, JWT를 이용하여 인증 기능을 구현할 수 있습니다.
- Flask-JWT-Extended, FastAPI의 `OAuth2PasswordBearer` 등을 사용하여 인증 및 권한 관리를 구축할 수 있습니다.

```
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

### 7. **마이그레이션과 데이터베이스 연결**

- Django에서 사용하는 마이그레이션 툴인 `makemigrations`, `migrate` 대신, FastAPI에서는 Alembic을 사용하여 데이터베이스 스키마 변경을 관리합니다.

```
bash


alembic init alembic
```

### 8. **테스트 및 디버깅**

- 전환 후 각 기능별로 테스트 코드를 작성하고, FastAPI의 자체 문서화 기능(Swagger)을 통해 API 테스트 및 디버깅을 진행합니다.

### 9. **배포 준비**

- FastAPI 프로젝트를 Uvicorn과 같은 ASGI 서버로 배포합니다.
- 기존 Django에서 배포에 사용된 방법(예: Nginx, uWSGI)도 FastAPI로 적용 가능하지만, Uvicorn과 함께 Nginx를 사용하는 것이 더 적합할 수 있습니다.