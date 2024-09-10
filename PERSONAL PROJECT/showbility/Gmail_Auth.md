# Gmail API 사용한 인증번호 확인

- Gmail API를 사용하여 회원가입 시 인증번호를 전송하고 인증 확인



### 1. **Google Cloud에서 Gmail API 설정**

#### 1-1. Google Cloud에서 API 활성화
1. [Google Cloud Console](https://console.cloud.google.com/)에 로그인합니다.
2. **새 프로젝트**를 생성하거나 기존 프로젝트를 선택합니다.
3. 왼쪽 사이드바에서 **API 및 서비스** > **사용자 인증 정보**로 이동합니다.
4. **+ 사용자 인증 정보 만들기** 버튼 클릭 후 **OAuth 2.0 클라이언트 ID**를 선택합니다.
5. OAuth 동의를 설정합니다.
   - 애플리케이션 이름 및 승인된 이메일을 설정.
6. **OAuth 2.0 클라이언트 ID**를 생성할 때, 애플리케이션 유형으로 **데스크톱 앱**을 선택.
7. 생성된 **클라이언트 ID 및 비밀 키**를 다운로드합니다.

#### 1-2. Gmail API 활성화
1. [API 라이브러리](https://console.cloud.google.com/apis/library)로 이동하여 **Gmail API**를 검색하고 활성화합니다.

### 2. **Python으로 Gmail API 사용 준비**

#### 2-1. Python 패키지 설치

Gmail API를 사용하려면 필요한 라이브러리를 설치합니다. 주로 Google의 `google-api-python-client` 및 `oauth2client` 라이브러리를 사용합니다.

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### 2-2. OAuth 2.0 인증 설정

`credentials.json` 파일은 Google Cloud Console에서 다운로드한 클라이언트 ID 파일입니다. 해당 파일을 프로젝트 폴더에 저장해야 합니다.

```python
import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# OAuth2.0 인증 범위 설정
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    # 토큰 파일이 있으면 불러오기
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # 토큰이 없거나 만료되었으면 다시 인증 진행
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 새 토큰 저장
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Gmail API 서비스 빌드
    service = build('gmail', 'v1', credentials=creds)
    return service
```

### 3. **인증번호 이메일 전송 코드**

#### 3-1. 이메일 전송 함수
Gmail API를 통해 인증번호가 포함된 이메일을 전송합니다. `MIMEText`를 사용하여 이메일 메시지를 구성합니다.

```python
# 이메일 메시지 구성
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

# 이메일 전송 함수
def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print(f"Message Id: {message['id']}")
        return message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

# 인증번호 이메일 전송
def send_verification_email(email, code):
    service = gmail_authenticate()
    sender_email = "your-email@gmail.com"  # 발신자 이메일 주소
    subject = "회원가입 인증번호"
    message_text = f"인증번호는 {code}입니다."
    
    message = create_message(sender_email, email, subject, message_text)
    send_message(service, "me", message)
```

#### 3-2. 인증번호 생성

회원가입을 시도한 사용자에게 발송할 인증번호를 생성하는 함수입니다. 간단한 6자리 랜덤 숫자로 설정할 수 있습니다.

```python
import random

# 6자리 인증번호 생성
def generate_verification_code():
    return random.randint(100000, 999999)
```

#### 3-3. 이메일 발송 및 인증 처리 흐름

회원가입 요청이 발생할 때, 인증번호를 생성하고 사용자 이메일로 전송하는 절차입니다.

```python
# 회원가입 시 인증번호 발송
def signup_user(email):
    code = generate_verification_code()
    send_verification_email(email, code)
    # 생성된 인증번호를 데이터베이스에 저장하거나 세션에 기록 (인증 확인 시 필요)
    return code  # 예시: 반환값으로 인증번호 리턴 (실제로는 세션 또는 DB에 저장)

# 인증번호 확인
def verify_code(input_code, actual_code):
    if input_code == actual_code:
        return True
    return False
```

### 4. **사용 흐름**

1. 사용자가 회원가입을 요청하면 `signup_user(email)` 함수가 호출되어 인증번호를 생성하고, 이메일로 전송합니다.
2. 사용자는 이메일로 받은 인증번호를 입력합니다.
3. 입력한 인증번호를 `verify_code()` 함수에서 실제로 생성된 인증번호와 비교하여 확인합니다.

### 5. **추가 고려 사항**
- **보안**: 인증번호의 유효 기간을 설정하여 일정 시간이 지나면 만료되도록 해야 합니다.
- **에러 처리**: 이메일 전송 실패 시 사용자가 알 수 있도록 에러 처리를 추가해야 합니다.
- **두 번째 이메일 발송 시**: 인증번호 요청 시, 기존에 발송한 인증번호를 덮어쓰거나 새로 생성된 번호로 업데이트합니다.

### 요약
- **Google Cloud Console**에서 Gmail API를 활성화하고 클라이언트 인증 정보를 다운로드합니다.
- Python에서 `google-api-python-client`를 사용하여 이메일 발송 및 인증번호 전송 로직을 구현합니다.
- 회원가입 요청 시 인증번호를 생성하고, 이메일을 통해 사용자의 입력을 확인합니다.

이 방법을 통해 간단한 이메일 기반 인증 시스템을 구현할 수 있습니다.