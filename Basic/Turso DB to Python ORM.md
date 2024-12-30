# Turso DB to Python ORM

Turso DB에서 생성된 데이터베이스 모델을 Python 코드로 자동 생성하려면, 데이터베이스 스키마를 읽어 Python ORM 모델로 변환하는 도구를 사용해야 합니다. SQLAlchemy와 같은 Python ORM에서는 이러한 작업을 지원하는 **sqlacodegen** 같은 도구를 사용할 수 있습니다.

### 1. **Turso DB와 연결**

Turso는 SQLite 기반의 분산형 데이터베이스입니다. 따라서 SQLite와 호환됩니다. Turso CLI를 사용해 데이터베이스 URL을 확인한 뒤 Python에서 연결하면 됩니다.

#### 예시:

```bash
turso db show <database-name>
```

이 명령으로 SQLite URL을 확인할 수 있습니다.

------

### 2. **모델 자동 생성**

`sqlacodegen`을 사용하면 데이터베이스 스키마를 Python ORM 모델로 자동 변환할 수 있습니다.

#### `sqlacodegen` 설치:

```bash
pip install sqlacodegen
```

#### 자동 생성 명령:

```bash
sqlacodegen sqlite:///path/to/turso.db --outfile models.py
```

위 명령은 Turso DB의 스키마를 기반으로 SQLAlchemy 모델 클래스를 생성하고, 결과를 `models.py`에 저장합니다.

------

### 3. **`sqlacodegen`으로 생성된 모델 예시**

예를 들어, Turso DB에 아래와 같은 테이블이 있다고 가정합니다:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
```

`sqlacodegen`은 다음과 같은 Python 코드를 생성합니다:

```python
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
```

------

### 4. **직접 SQLAlchemy Reflection 사용**

Turso DB를 Python 프로젝트에서 동적으로 사용하려면 Reflection 기능을 사용할 수도 있습니다. Reflection은 테이블 스키마를 코드에 명시적으로 작성하지 않고 데이터베이스에서 읽어옵니다.

#### Reflection 예시:

```python
from sqlalchemy import create_engine, MetaData, Table

# Turso DB 연결
engine = create_engine("sqlite:///path/to/turso.db")
metadata = MetaData()

# Reflection으로 모든 테이블 로드
metadata.reflect(bind=engine)

# 특정 테이블 참조
users_table = metadata.tables['users']
print(users_table.columns.keys())
```

------

### 5. **Turso DB와 SQLAlchemy 통합**

Turso DB는 SQLite 기반이기 때문에 SQLAlchemy에서 표준 SQLite 드라이버를 사용하여 쉽게 통합할 수 있습니다:

```python
from sqlalchemy import create_engine

# Turso DB URL
engine = create_engine("sqlite:///path/to/turso.db")
```

------

### 결론

Turso DB 모델을 Python에서 사용하려면:

1. **sqlacodegen**을 사용하여 Turso 스키마 기반으로 SQLAlchemy 모델을 자동 생성합니다.
2. 또는 SQLAlchemy의 **Reflection** 기능을 사용하여 런타임에 데이터베이스 스키마를 동적으로 읽어옵니다.

`sqlacodegen`은 스키마가 비교적 고정되어 있는 경우 유용하며, Reflection은 동적으로 테이블을 관리하거나 스키마 변경이 빈번한 경우 적합합니다.