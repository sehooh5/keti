# Django-ninja

- Django 프레임워크를 기반으로 한 API 구축 도구
- 빠르고, 간단하며, 효율적인 방식으로 REST API를 생성
- FastAPI와 Pydantic을 사용하여 설계됨
- **Django Ninja는 Flask와 비슷한 구조를 가지고 있고, 기존 코드를 재사용할 수 있어 Django 프로젝트에서 빠르게 API를 확장가능**



### **Django Ninja의 주요 특징**

1. **빠른 속도**:
   - Django Ninja는 FastAPI와 비슷한 방식으로 비동기 처리를 지원하고, 성능이 매우 뛰어납니다. 이는 API 호출 처리에서 속도와 효율성이 중요한 경우 특히 유리합니다.
2. **타입 힌트 기반**:
   - Python의 타입 힌트(type hints)를 적극적으로 활용하여 API 엔드포인트를 정의합니다. 이를 통해 코드의 가독성과 유지보수성을 높이고, 개발 도중 발생할 수 있는 타입 관련 오류를 줄일 수 있습니다.
3. **자동 문서화**:
   - Django Ninja는 **Swagger UI** 및 **Redoc**과 같은 API 문서화 도구를 기본으로 제공합니다. API를 정의하면 자동으로 문서화되고, 이를 통해 개발자와 사용자 간의 API 통신을 더 쉽게 이해할 수 있습니다.
4. **Pydantic 모델 지원**:
   - **Pydantic**을 사용하여 데이터 유효성 검사를 처리하며, JSON 스키마 기반으로 데이터를 검증할 수 있습니다. 이를 통해 API에서 데이터를 안전하게 처리할 수 있습니다.
5. **비동기 처리 지원**:
   - Django Ninja는 비동기 방식(asynchronous)으로 API 요청을 처리할 수 있는 옵션을 제공하여 대규모 트래픽 처리에 유연하게 대응할 수 있습니다.
6. **Django와의 자연스러운 통합**:
   - Django Ninja는 Django 프레임워크와 완벽하게 통합됩니다. 이를 통해 기존 Django 프로젝트에 쉽게 API를 추가할 수 있으며, Django ORM, 미들웨어, 인증 시스템 등과도 자연스럽게 연동됩니다.

### **Django Ninja의 기본 사용 예시**

```
python코드 복사# 설치
pip install django-ninja

# 프로젝트 설정에 앱 추가
# settings.py
INSTALLED_APPS = [
    ...
    'ninja',
    ...
]

# views.py
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello, world!"}

# urls.py
from django.urls import path
from .views import api

urlpatterns = [
    path("api/", api.urls),
]
```

이 간단한 예시는 `/api/hello` 경로에서 GET 요청을 처리하고 "Hello, world!"라는 메시지를 반환하는 API를 정의하는 방법을 보여줍니다.

### **장점**

- **빠른 개발 속도**: 타입 힌트와 자동 문서화를 제공하여 API 개발 속도를 높이고 생산성을 향상시킵니다.
- **성능**: FastAPI와 비슷한 비동기 처리 지원으로 매우 높은 성능을 제공합니다.
- **간편한 통합**: 기존 Django 프로젝트에 쉽게 통합 가능하며, Django의 ORM과 인증 시스템을 그대로 사용할 수 있습니다.

### **사용 예시**

1. **GET 요청과 Query 파라미터 처리**:

   ```
   python코드 복사@api.get("/items")
   def list_items(request, q: str = None):
       return {"query": q}
   ```

2. **POST 요청과 데이터 유효성 검사**:

   ```
   python코드 복사from pydantic import BaseModel
   
   class ItemSchema(BaseModel):
       name: str
       price: float
   
   @api.post("/items")
   def create_item(request, item: ItemSchema):
       return {"item": item.dict()}
   ```

### **결론**

Django Ninja는 Django 환경에서 REST API를 쉽고 효율적으로 만들 수 있는 강력한 도구입니다. FastAPI와 Pydantic의 장점을 결합한 Django Ninja는 뛰어난 성능과 간편한 API 개발 환경을 제공하며, 특히 타입 안정성과 자동 문서화를 통해 개발 경험을 향상시킵니다.











