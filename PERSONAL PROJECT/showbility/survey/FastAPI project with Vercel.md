# FastAPI project with Vercel

- FastAPI 프로젝트를 Vercel에서 운영할 때 기본 틀 잡기
- DB : turso



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



### 6. 이미지 업로드

1. **이미지를 서버에 업로드**
2. **이미지를 파일 시스템이나 클라우드 스토리지에 저장**
3. **이미지의 경로(URL)을 데이터베이스에 저장**

### 1. **파일 업로드 경로 설정 (FastAPI)**

먼저, FastAPI를 사용하여 클라이언트가 이미지를 업로드할 수 있도록 설정합니다.

```python
from fastapi import FastAPI, File, UploadFile
import shutil
import os

app = FastAPI()

# 이미지 업로드 경로 설정
UPLOAD_DIRECTORY = "./uploaded_images/"

# 업로드 디렉토리가 없을 경우 생성
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    # 파일을 저장할 경로 설정
    file_location = os.path.join(UPLOAD_DIRECTORY, image.filename)
    
    # 파일을 서버에 저장
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {"info": f"file '{image.filename}' saved at '{file_location}'"}
```

### 2. **이미지 경로를 Turso (SQLite) DB에 저장**

이미지가 서버에 저장된 후, 해당 이미지의 경로를 데이터베이스에 저장합니다. 여기서는 SQLAlchemy를 사용하여 Turso와 연동된 데이터베이스에 이미지를 저장하는 모델을 정의합니다.

```python
from sqlalchemy import Column, Integer, String
from database import Base, engine, SessionLocal

# 데이터베이스 모델 정의
class ImageModel(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True)
    filepath = Column(String)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스에 이미지 경로 저장하는 함수
def save_image_to_db(filename: str, filepath: str):
    db = SessionLocal()
    new_image = ImageModel(filename=filename, filepath=filepath)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    db.close()
    return new_image
```

### 3. **파일 업로드 및 DB 저장 통합**

이미지 파일을 업로드하고, 그 경로를 데이터베이스에 저장하는 통합 로직을 만듭니다.

```python
@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, image.filename)
    
    # 이미지 파일 저장
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # 이미지 경로를 데이터베이스에 저장
    image_in_db = save_image_to_db(filename=image.filename, filepath=file_location)
    
    return {"info": f"file '{image.filename}' saved at '{file_location}'", "db_record": image_in_db.id}
```

### 4. **이미지 조회**

이미지를 조회하는 API를 추가하여 저장된 이미지를 서버에서 다시 확인할 수 있도록 합니다.

```python
from fastapi.responses import FileResponse

@app.get("/images/{image_id}")
async def get_image(image_id: int):
    db = SessionLocal()
    image_record = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    
    if image_record:
        return FileResponse(image_record.filepath)
    return {"error": "Image not found"}
```

### 5. **결론**
- **이미지 파일 저장**: 이미지를 서버에 업로드하고 파일 시스템에 저장합니다.
- **이미지 경로를 DB에 저장**: 이미지 파일이 저장된 경로와 파일명을 데이터베이스에 저장하여, 나중에 해당 이미지를 조회할 수 있도록 합니다.
- **이미지 조회**: 저장된 이미지를 URL로 접근하거나 제공할 수 있도록 설정합니다.

### 추가 참고사항:
- **클라우드 스토리지**: 파일 시스템 대신 AWS S3와 같은 클라우드 스토리지에 이미지를 저장하고 URL만 DB에 저장할 수도 있습니다.
- **파일명 중복**: 업로드되는 파일의 파일명을 UUID 등의 방식으로 고유하게 변경하여 중복 문제를 방지하는 것도 고려해야 합니다.