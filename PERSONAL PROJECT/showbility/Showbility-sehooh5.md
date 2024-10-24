# Showbility - sehooh5

- Showbility Project 내 오세호 개인 파일

- ssh -i [개인키].pem ubuntu@13.209.10.151

  - ```
    ssh -i ShowbilityServer05.pem ubuntu@13.209.10.151

- 개인 일정 및 진행방향 공유

- PORT
  - nginx : 80
  - uwsgi : http = 0.0.0.0:8080        
  - DB : 3306
  
- **서버 켜는법**
  - nginx + uwsgi로 작동함
    1. `nginx` 켜져 있는지 확인
       1. `sudo service nginx status`
       2. 안켜져 있으면 켜기 `sudo service nginx start````
    2. `uWSGI` 로 장고 서버 띄우기
       1. `sudo uwsgi --ini uwsgi.ini`
  
- **작동 안하는 가짜 설정파일들**
  - apache → 사용 안함
  - 관련 설정이 있는지 nginx가 죽으면 그 자리를 빼앗아(?) 시작됨
  - TODO: 지워두기
  - `run_with_env.sh` 이전에 테스트용으로 만들어둔 파일인듯
  - 작동 자체는 하긴 함 
  - 이걸 쓰면 80 포트에 파이썬 프로세스가 바로 붙는데, 권장되는 방법은 아님
  - nginx 에서 static 파일 serving을 하도록 설정되어 있는데, 파이썬을 바로 쓰는 경우 이게 작동 안해서 이미지 안보임



## Setting

- python 3.9.6

  - packages : 

    ```
    pip3 install 
    
    fastapi uvicorn sqlalchemy databases python-dotenv libsql-experimental
    sqlalchemy-libsql passlib aiosqlite
    
    # poetry add
    poetry add fastapi uvicorn qlalchemy databases alembic pyjwt httpx jinja2 python-dotenv passlib[bcrypt]
    ```



- DB

  - Turso

    - Download : 

      ```
      # Mac
      brew install tursodatabase/tap/turso
      
      # Window
      curl -sSfL https://get.tur.so/install.sh | bash
      
      ```



- 



## Study or Survey

### Backend

#### Django - Flask 협업툴

- Django-ninja
  - 참고 페이지 : https://django-ninja.dev/
- FastAPI
- Vercel using Python
  - https://vercel.com/docs/functions/runtimes/python
- nginx
- wsgi



### Planning

#### 화해 플랫폼

- 가입 부분에 있어서 email 등 인증 관련한 부분 기획 참고





## Daily

#### 0905

- AWS 책 보고 공부
- AWS EC2 내 테스트서버 구축
  - 인스턴스를 추가할지
    - [쇼빌 인스턴스 정봅](https://showbility.notion.site/EC2-e2a8e40604fe4d1aa29739330011e254)
  - 아니면 한 개의 인스턴스 내 테스트서버도 구축할지[(링크)](https://hou27.tistory.com/entry/%ED%95%98%EB%82%98%EC%9D%98-EC2-%EC%95%88%EC%97%90-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%84%9C%EB%B2%84%EA%B9%8C%EC%A7%80-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0-feat-AWS)



- 질문사항
  - 인스턴스, 볼륨이 두개로 나누어져있는데 차이점?



#### 0908

- AWS 접속
- 로그인, 가입, 게시물 오류 디버깅
  - 데이터베이스 연결 문제:
    - DB 서버가 다운되었거나 연결 문제가 있을 수 있습니다.
    - 연결 문자열이 변경되었거나 잘못되었을 수 있습니다.
  - 서버 리소스 부족:
    - CPU, 메모리, 디스크 공간 등이 부족할 수 있습니다.
  - ~~애플리케이션 코드 오류:~~
    - ~~최근 배포된 코드에 버그가 있을 수 있습니다.~~
  - 외부 서비스 의존성 문제:
    - 이메일 검증, 인증 등 외부 서비스에 문제가 있을 수 있습니다.
  - 캐시 문제:
    - 잘못된 데이터가 캐시되어 있을 수 있습니다.
  - 네트워크 문제:
    - 방화벽, 프록시 설정 등에 문제가 있을 수 있습니다.
  - 결국 서버꺼져서 다시 키는방향



#### 0909

- Survey 할것들 대충 공부해놓기 - 1시간

<<<<<<< HEAD
- 테스트서버 구축하기

  - ### **1. Nginx 설정 변경**

    Nginx에서 테스트 서버용으로 별도의 포트를 할당해야 합니다. 예를 들어, 프로덕션 서버는 포트 80을 사용하고, 테스트 서버는 포트 8080을 사용하도록 설정할 수 있습니다.

    #### 1.1. **Nginx 설정 파일 복제**

    현재 프로덕션 서버에 대한 설정 파일을 복제하여 테스트 서버용 설정을 만듭니다.

    ```
    bash
    
    
    코드 복사
    sudo cp /etc/nginx/sites-available/your_site_config /etc/nginx/sites-available/your_dev_site_config
    ```

    #### 1.2. **테스트 서버 포트 변경**

    복제한 설정 파일을 열고, 프로덕션 포트(예: `80`)를 테스트용 포트(예: `8080`)으로 변경합니다.

    ```
    bash
    
    
    코드 복사
    sudo nano /etc/nginx/sites-available/your_dev_site_config
    ```

    다음과 같이 `listen` 지시어를 수정합니다.

    ```
    nginx
    
    
    코드 복사
    server {
        listen 8080;
        server_name your_test_domain_or_ip;
    
        location / {
            proxy_pass http://127.0.0.1:8001;  # uWSGI에서 실행 중인 Django 서버의 포트
            ...
        }
    }
    ```

    #### 1.3. **사이트 활성화**

    테스트 서버 설정 파일을 활성화하려면 `sites-enabled` 디렉토리에 심볼릭 링크를 생성합니다.

    ```
    bash
    
    
    코드 복사
    sudo ln -s /etc/nginx/sites-available/your_dev_site_config /etc/nginx/sites-enabled/
    ```

    #### 1.4. **Nginx 설정 테스트 및 재시작**

    Nginx 설정을 테스트하고 문제가 없으면 재시작합니다.

    ```
    bash
    
    
    코드 복사
    sudo nginx -t
    sudo service nginx restart
    ```

    ### **2. uWSGI 설정 변경**

    uWSGI는 테스트 서버를 위한 별도의 포트에서 Django 애플리케이션을 실행해야 합니다. 테스트 서버에서는 예를 들어 `8001` 포트를 사용할 수 있습니다.

    #### 2.1. **uWSGI 설정 파일 복제**

    현재 `uwsgi.ini` 파일을 복제하여 테스트용 설정 파일을 만듭니다.

    ```
    bash
    
    
    코드 복사
    sudo cp /path/to/your/uwsgi.ini /path/to/your/uwsgi_dev.ini
    ```

    #### 2.2. **테스트 서버용 포트 변경**

    복제한 `uwsgi_dev.ini` 파일을 열어, 포트를 테스트 서버용으로 변경합니다.

    ```
    bash
    
    
    코드 복사
    sudo nano /path/to/your/uwsgi_dev.ini
    ```

    설정 파일에서 `http-socket` 또는 `socket` 항목을 수정하여 다른 포트(예: `8001`)에서 서버가 실행되도록 합니다.

    ```
    ini
    
    
    코드 복사
    [uwsgi]
    http-socket = 127.0.0.1:8001  # 테스트 서버용 포트
    module = your_project.wsgi:application
    master = true
    processes = 5
    ```

    #### 2.3. **테스트 서버 실행**

    테스트 서버를 실행하려면 `uwsgi_dev.ini` 파일을 사용하여 uWSGI를 실행합니다.

    ```
    bash
    
    
    코드 복사
    sudo uwsgi --ini /path/to/your/uwsgi_dev.ini
    ```

    ### **3. 보안 그룹에서 포트 열기**

    AWS EC2의 보안 그룹에서 새로운 포트(예: `8080`)를 열어야 외부에서 접근할 수 있습니다.

    1. AWS Management Console에 접속하여 EC2 인스턴스의 보안 그룹 설정으로 이동합니다.

    2. 인바운드 규칙

       에서 포트 

       ```
       8080
       ```

       을 허용하는 규칙을 추가합니다.

       - **타입**: Custom TCP
       - **포트 범위**: 8080
       - **소스**: 0.0.0.0/0 (또는 필요한 IP 범위)

    ### **4. 테스트 서버 확인**

    브라우저에서 EC2 인스턴스의 퍼블릭 IP 주소 또는 도메인 뒤에 테스트용 포트를 추가하여 접속합니다.

    ```
    bash
    
    
    코드 복사
    http://your-ec2-ip:8080
    ```

    ### **결론**

    1. **Nginx 설정**에서 테스트용 포트(예: `8080`)를 추가하고, uWSGI가 다른 포트에서 테스트 서버를 실행하도록 설정합니다.
    2. **uWSGI 설정 파일**을 복제하고 포트 번호를 수정하여 테스트 서버용 설정을 적용합니다.
    3. **보안 그룹**에서 새로운 포트를 열고, Nginx와 uWSGI를 재시작하여 테스트 서버를 실행합니다.

    이렇게 하면 동일한 EC2 인스턴스에서 프로덕션과 테스트 서버를 각기 다른 포트에서 운영할 수 있습니다.
=======


#### 0910

- Vercel 서버 이전 서베이
  - 비용
  - 유지/보수
  - 운영방법
  - 이전방법



- 인증번호 이메일 서베이
  - 구글 Gmail API
    - 사용 흐름
      1. 사용자가 회원가입/비밀번호 찾기 화면에서 [이메일 주소]를 입력 후 인증번호를 요청하면 [인증번호]를 생성해서 입력한 [이메일 주소]로 전송
      2. 사용자는 이메일로 받은 [인증번호]를 입력
      3. 입력한 [인증번호]를 실제 생성된 인증번호와 비교해서 맞는지 확인
         - 일치 : 통과
         - 불일치 : 에러메시지,  
    - 에러 처리
      - 이메일 전송 실패 시 : 사용자에게 전송 실패 메시지
      - 인증번호 유효기간 만료 시 : 인증 X, 유효기간이 지났음을 알리는 메시지



#### 0911

- Vercel 적용방법 자세히
- Django to Flask



#### 0914

- Django -> Flask 시작



#### 0915

- AWS - Dev Server 연동 시작



#### 0917

- AWS 연동 잘 안되는거 진행하기



#### 0923

- routes 옮기기 시작
- models 옮기기 시작
  - customusermanager 옴겨야함 완료
  - 나머지 옮기기 시작



#### 0924

- models 
  - ExtendUser 이후 옮기기 시작



#### 0925

- fastapi 변경으로 다시 시작
- poertry
- DB 고려해보기
  - turso
  - neon
  - **supabase** : 유력
  - drizzle

#### 0926

- fastapi로 변경중
  - urls.py 옮기는중
    - 라우터 설정은 거의 끝났고 로직 부분 정의하면 될듯



#### 0930

- 라우터 로직 다시 시작



#### 1001

- model 변경 완료
- pedantic - schema 시작



#### 1002

- 오늘은 쇼빌 위주로 진행
  - 전체적으로 어떻게 전환하면 좋을지 다시 확인해서 진행



#### 1004

- DB 변경
  - supabase -> turso



#### 1005

- model, schema, crud 검토
- views 전환중
  - crud : db 
  - schema - 어떤 원리인지? 기본주터 다시 알아야할듯



#### 1006

- view 계속 진행중
  - user part

#### 1008

- views
  - my, serializer, permission 진행



#### 1010

- 기본세팅 후 버셀에 올리기
  - config부분 완료
    - config, prod_config만 사용예정
  - 이후 
    - 기본 틀 main과 env 에 필요한 것들 업로드
    - turso 업데이트



#### 1012

- vercel 기본 세팅 완료
  - DB 세팅한거 다시 커밋, 푸시 필요
- 깃헙 
  - draft
    - merge 할 pr작업중일 때 열어두는 느낌
  - branch
- pipenv install 사용 



#### 1013

- 기본 fastsapi 예제대로 파일 구성하기
  - 기초 참고하기 : https://velog.io/@crosstar1228/FastapiSQLAlchemy-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-DB%EC%99%80-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0
- DB 세팅 완료
- 이제 현재 옮기고 있던 router, model, crud, schema 옮기기
  - user -------> 순호님 풀리퀘 후 feat 만든 후 다시 진행
    - 현재 create_user만 구성중
      - jwt_handler.py : 적합하게 수정해줘야함
      - 이미지 파일처리 어떻게 해야할지 정확하게 수정해야함



#### 1014

- pr : DB 세팅
  - Annotated 확인
  - schema users
    - orm 부분 삭제 필요
  - 환경 별 변수 나누기
    - local - dev -prod 나누어서 한번 적용해보겠습니다.
    - os.environ였나로 가져오는것보다, 세팅도 pydantic 통해서 관리하고 validate할수 있는데 적용해보기[docs.pydantic.dev/latest/concepts/pydantic_settings#usage](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage)
- 이제 현재 옮기고 있던 router, model, crud, schema 옮기기
  - user -------> 순호님 풀리퀘 후 feat 만든 후 다시 진행
    - 현재 create_user만 구성중
      - 이미지 파일처리 어떻게 해야할지 정확하게 수정해야함



#### 1015

- 현재 비동기 때문에 에러나는중
- 공식문서 보고 다시 구성해보기
  - https://fastapi.tiangolo.com/ko/tutorial/sql-databases/#create-database-tables-on-startup



#### 1016

- 기존 dev에서 수정할 부분만 수정
  - pydantic으로 on.environ 세팅
    - [docs.pydantic.dev/latest/concepts/pydantic_settings#usage](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage)
  - annotated 

- turso 연동

  - async -> 동기 엔진으로 변경 완료 실행되는지 확인 with turso

- env 환경설정 -> 추후 진행(AWS)

  - 기존 내용 옴기기

    ```
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    APPLE_MEMBER_ID
    APPLE_KEY_ID
    APPLE_CERT_KEY_PATH
    ```

    

- 환경 나누어서 실행하는 방법 



#### 1017

- 동기엔진 turso와 연동되는지 확인하기
  - 연동 완료
  - dev  브랜치 머지 후
  
- User 기능 구현 시작

  - feat/user branch 에서 작업 진행

  - r-m-s 한번 정리 완료

  - deps 검토 완료

  - -> 이미지 관리 부분 시작해야함

    - 어느정도 완성
- 테스트중인데 swagger UI (/docs)로 진행하면됨
  
  
  

#### 

- feat

  - **User**

    - r-m-s 한번 정리 완료
    - deps 검토 완료
    - -> ~~이미지 관리 부분 시작해야함~~
      - ~~어느정도 완성~~
    - 테스트중인데 swagger UI (/docs)로 진행하면됨

    - create 완료
      - **프로필 사진 파일 없을때 처리방법 보완해야함** 
    - delete : postman으로 완료
      - **사진까지 지워지게끔 해야함** 
    - login 기능 완성 
      - token 반환 - 업데이트
    - update : 사용자 정보 변경 완료
      - 태그 추가부분 완료
    - auth : verify 부분 추가<mark>(테스트 필요)</mark>
      - crud, model, router / relationship with user model
      - 이메일 인증요청/인증 완료
      - 비밀번호 재설정 완료
      - **나머지 두개 진행하면 됨**
    - 소셜 로그인 완료<mark>(테스트 필요)</mark>

  

  - **Content**
    - 시작하면 됨

  

  2410JJM25

  

#### 쇼빌리티 방향성

- v2
- 그룹
- 페어 참가
- 특수적인 기능
  - 채용
  - 거래
  - 포트폴리오 AI 제작





#### 전환 일정

-  fastapi 전환
  - **User** 
    - 코드 작성 완료
    - 테스트 필요
  - **Content**
    - 시작 1022



- 일정
  - **Content(게시물)**: 게시물 생성, 조회, 수정, 삭제 기능을 추가.
  - **이미지 처리**: 이미지 업로드 및 썸네일 생성 로직, 관련된 경로 설정.
  - **태그 및 카테고리**: 게시물과 태그 및 카테고리를 연결하고, 조회 및 필터링 기능.
  - **좋아요 기능**: 사용자가 게시물에 좋아요를 누르거나 취소할 수 있는 기능 구현.















