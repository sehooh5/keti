# APPLE 로그인 기능 구현

------

### **Apple 로그인: 리다이렉트 없이 처리하는 방식**

1. **프론트엔드 처리**:
   - 프론트엔드에서 Apple 로그인 버튼을 사용해 Apple의 인증을 요청.
   - Apple에서 `authorization_code`와 `id_token`을 응답으로 받음.
2. **백엔드 처리**:
   - 프론트엔드가 받은 `authorization_code`와 `id_token`을 백엔드에 전달.
   - 백엔드는 Apple 서버와 통신하여 인증 상태를 확인하고 사용자 정보를 처리.

------

### **백엔드 코드 (FastAPI)**

#### 엔드포인트: Apple 인증 데이터 처리

```python
from fastapi import APIRouter, HTTPException, Request, Depends
from app.core.config import settings
from app.models.users import ExtendUser
from app.crud.users import get_or_create_apple_user
from app.utils.apple import Auth  # 유틸리티 클래스
from app.schemas.users import TokenResponse

router = APIRouter()

@router.post("/social/apple", response_model=TokenResponse)
async def handle_apple_login(request: Request, session: SessionDep):
    # 프론트엔드에서 전달한 데이터
    data = await request.json()
    authorization_code = data.get("authorization_code")
    id_token = data.get("id_token")

    if not authorization_code or not id_token:
        raise HTTPException(status_code=400, detail="Missing authorization_code or id_token.")

    # Apple 서버와 통신하여 토큰 검증
    token_data, verified = Auth.verify_token(authorization_code)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid authorization code.")

    # ID 토큰 디코드
    decoded_token = Auth.decode_jwt_token(id_token)
    sub = decoded_token.get("sub")
    email = decoded_token.get("email")

    if not sub:
        raise HTTPException(status_code=400, detail="Missing user identifier from Apple.")

    # 사용자 생성 또는 로그인 처리
    user = get_or_create_apple_user(session, sub=sub, email=email)
    response_data = login_user(user=user)

    return response_data
```

------

### **Apple 개발자 페이지 설정 방법**

Apple 로그인 기능을 사용하려면 [Apple 개발자 계정](https://developer.apple.com/)에서 앱 설정이 필요합니다.

#### 1. **App ID 생성**

1. Apple Developer Console로 이동: https://developer.apple.com/account/

2. **Certificates, IDs & Profiles** > **Identifiers** > **App IDs**로 이동.

3. `+` 버튼을 클릭해 새 App ID 생성.

4. **Description**: 앱 이름 입력.

5. **Bundle ID**: 앱의 고유 식별자 입력(예: `com.example.myapp`).

6. Capabilities

   :

   - "Sign In with Apple" 활성화.

7. 저장.

#### 2. **Key 생성**

1. **Keys**로 이동.
2. `+` 버튼을 클릭해 새 Key 생성.
3. Key 이름 입력(예: `SignInWithAppleKey`).
4. "Sign In with Apple" 활성화.
5. 저장 후 Key 다운로드 (`.p8` 파일). **이 파일은 한 번만 다운로드 가능**.

#### 3. **Service ID 생성**

1. **Identifiers** > **Service IDs**로 이동.

2. `+` 버튼을 클릭해 새 Service ID 생성.

3. Service ID 이름 입력(예: `SignInWithAppleService`).

4. Identifier 입력(예: `com.example.myapp.service`).

5. Capabilities

   :

   - "Sign In with Apple" 활성화.

6. 저장.

#### 4. **Redirect URI 설정**

1. Service ID를 클릭해 설정 페이지로 이동.

2. Sign In with Apple

    설정에서 

   Return URLs

    입력:

   - 예: `https://your-domain.com/social/apple`.

#### 5. **Client ID 및 Secret 구성**

- `client_id`: Service ID 값.

- ```
  client_secret
  ```

  : 다음과 같은 정보로 생성:

  - Team ID (Apple 개발자 계정에서 확인 가능).
  - Key ID (생성한 Key에서 확인 가능).
  - Private Key (다운로드한 `.p8` 파일).

------

### **결론**

- **리다이렉트 없는 처리**:
  - 프론트엔드에서 `authorization_code`와 `id_token`을 받아 백엔드로 전달.
  - 백엔드에서 Apple 서버와 통신하여 검증 후 사용자 정보 처리.
- **Apple 개발자 설정**:
  - App ID 생성, Key 생성, Service ID 생성.
  - Redirect URI 설정.
  - 클라이언트에서 인증 후 서버로 `authorization_code`와 `id_token` 전달.