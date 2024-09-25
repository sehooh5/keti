# FastAPI project with Vercel

- FastAPI 프로젝트를 Vercel에서 운영할 때 기본 틀 잡기
- DB : Supabase



### 1. FastAPI 프로젝트 설정

#### 디렉토리 구조:
```plaintext
instagram-clone/
│
├── app/
│   ├── main.py        # FastAPI 애플리케이션 진입점
│   ├── models.py      # 데이터베이스 모델 정의
│   ├── schemas.py     # 요청 및 응답 스키마
│   ├── crud.py        # 데이터베이스 작업을 수행하는 CRUD 로직
│   ├── deps.py        # 의존성 주입
│   ├── config.py      # 환경 변수 및 설정 관리
│   ├── services/      # 비즈니스 로직
│   └── routers/       # 라우팅을 정의하는 모듈들 (users, posts 등)
│
├── tests/             # 테스트 코드
│
├── .env               # 환경 변수 파일
├── requirements.txt   # 의존성 패키지 목록
├── vercel.json        # Vercel 배포 설정
└── Dockerfile         # (옵션) Docker를 통한 컨테이너화
```

### 2. FastAPI 기본 설정

#### `app/main.py` (FastAPI 진입점)
```python
from fastapi import FastAPI
from app.routers import users, posts  # 사용자와 게시물에 대한 라우터

app = FastAPI()

# 라우터 등록
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Instagram Clone API!"}
```

#### `app/models.py` (Supabase와 연결된 데이터베이스 모델)
Supabase는 PostgreSQL 기반이므로 SQLAlchemy ORM을 사용하여 데이터베이스 모델을 정의

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
```

#### `app/schemas.py` (Pydantic 스키마)
```python
from pydantic import BaseModel
from typing import List

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True
```

#### `app/crud.py` (CRUD 작업)
```python
from sqlalchemy.orm import Session
from app import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
```

#### `app/routers/users.py` (유저 라우터)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
```

### 3. Supabase 연결 설정
Supabase PostgreSQL에 연결하려면 `app/database.py`에 데이터베이스 연결 설정을 추가

#### `app/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Supabase URL을 환경 변수로 관리

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### `.env`
```
DATABASE_URL=postgresql://{supabase_user}:{password}@db.{supabase_host}:{port}/{database_name}
```

### 4. Vercel 배포 설정

#### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    { "src": "app/main.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app/main.py" }
  ]
}
```

#### `requirements.txt`
```plaintext
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
```

#### Vercel 배포
1. Vercel CLI를 설치하고 로그인:
   ```bash
   npm i -g vercel
   vercel login
   ```

2. 프로젝트 배포:
   ```bash
   vercel
   ```

### 5. 실시간 기능 추가
인스타그램 같은 소셜 플랫폼에서는 실시간 알림이나 채팅 기능이 중요한데, Supabase의 실시간 데이터베이스 동기화를 활용하거나, FastAPI의 WebSocket을 이용해 채팅 기능을 구현가능

