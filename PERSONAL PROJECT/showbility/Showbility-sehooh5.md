# Showbility - sehooh5

- Showbility Project 내 오세호 개인 파일

- ssh -i [개인키].pem ubuntu@13.209.10.151

  - ```
    ssh -i ShowbilityServer05.pem ubuntu@13.209.10.151
    ```

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

    

  - Turso Local

    - 로컬 개발 환경에서 Turso DB 실행

    ```
    turso dev --db-file local.db
    
    # 기본적으로 임시 데이터베이스를 생성하기 때문에, 서버를 종료하면 데이터가 사라짐. 데이터 저장이 필요하다면 SQLite 파일을 지정하여 실행
    ```

    - ​	이 명령어는 **로컬에서 Turso의 libSQL 서버**를 실행하고 임시 데이터베이스를 만듬
  
- 서버는 기본적으로 `http://127.0.0.1:8080` 주소에서 실행
  
- Python SDK를 사용하여 데이터베이스 연결
  
      ```
      from libsql_client import create_client
      
      client = create_client({
          "url": "http://127.0.0.1:8080"
      })
  ```
    
      - 로컬 libSQL 서버에 연결
  ```



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
    - auth : verify 부분 추가
      - crud, model, router / relationship with user model
      - 이메일 인증요청/인증 완료
      - 비밀번호 재설정 완료
      - 이메일 닉네임 중복확인 완료
    - 소셜 로그인 완료
      - 카카오 완료
      - 애플
        - <mark>(테스트 필요)</mark> : 프론트와 연동 필요

  

  - **Content**
    
    - 일정 : 
    
      - 일단 전체적으로 옴기고
      - 이미지 처리, 태그, 카테고리 등등 설정해주기
    
    - 기능
    
      - 기본 : 완료
      - Like : 완료
    
    -  <mark>(테스트 중)</mark>
    
      - create : 
    
        - image folder명 잘 들어가나 확인필요
    
        - category, tag 들어가나 확인 필요-고치는중
    
          - ## **category, tag 테이블 이용해서 저장하는 방식으로 다시 다 재검토하기, 끝난 후 update 기능 수정 필요**

  

  - **Category, Tag, Comment**
    - 일단 완료 <mark>(테스트 중)</mark>
    - Category
      - read : 완료
    - 

  

  - ##### **Image**

    - Content에서 처리하는데 꼭 필요한지?
    - <mark>(확인 필요)</mark> 

  

  - **Follow**
    - 완료 <mark>(테스트 필요)</mark>

  

  - **Group**
    - 아직 안하고 회의후 진행해볼것!

  

  #### 1031

  - 일단 db 리셋, Router 추가 완료했으니 처음부터 테스트 시작!
  - 적용하기
    - ~~환경변수 개수 줄여보기~~
    - local turso 적용할 수있으면 적용해보기 - local 환경 나누기 >>> 이후에 진행
      - :8080
    - vercel 환경변수 입력하기
      - env 파일 직접 올릴수있음
    - static file 관리 -> 기본 API 만들고 진행 >>> 이후 진행
      - s3
      - uploadthing
      - blob

  

  #### 1102

  - 오늘 진행
    - ~~vercel 환경변수 입력하기~~
      - ~~env 파일 직접 올릴수있음~~
      - 세팅 완료
        - static, media 세팅은 일단 보류함
        - 나중에 관리하는거 정해지면 진행
    - user, content 
      - 권한설정
        - 설계서 보고 고칠거있으면 ㄱㄱ
      - 파일부분 일단 보류해두기
        - 보류 완료, 테스트 진행하면 될듯?

  

  

  #### 1104

  - db, fs 백업

    - fs(static, media)

      - ```
        # 프로젝트 전체 압축/저장
        tar -czvf ~/backup/static_backup.tar.gz ubuntu
        
        # 전체파일 복사/전송
        scp -i ShowbilityServer05.pem ubuntu@13.209.10.151:~/Volumes/T7/showbility/backup
        ```

  

  #### 1120

  - **Torso - dev 환경에서 fs 없는 api 테스트 시작**

    - **User**
      
      - ~~이용약관 추가 필요~~ 
        - 기존 약관은 node.js에서 처리
      - 카카오
        - agree 부분 수정했는데 테스트 필요
        - 테스트, 401 에러 발생하면서 잘 안되는중!!
      - 애플
        - 카카오와 동일한데, 테스트 아직 해본적 없음
    - 카테고리 추가하는 부분 추가 필요(구닥 참고)
      - update
        - ~~tag가 아닌 category임...모델부터 바꿔야할듯~~ - 변경완료

        - 카테고리 추가하는 부분이 현재 string 으로 입력값을 받아서 처리해주고있음
          
          - 입력값 1,2,3
          
        - 현재 카테고리가 입력되어있는 user 가 에러가 발생중

      - 카테고리, 태그들 데이터 추가완료
    - my get error(프로필 조회)
      
      - ~~프로필에 카테고리가 들어가잇을때 에러가 생김~~
        - tag 객체가 아닌 int 입력으로 해결 완료

  

  - kakao test
    - vercel 보안때매 안되는거였음...
    - 현재는 #error 내용 고치면 됨, user 모델 필수값 입력이안되서그럼




  #### 1121

  - User 부분 테스트 완료

    - 카테고리 추가부분 수정중

      - 기존에는 다같이 처리함

      - 바뀐버전

        1. 카테고리 이외 정보만 수정하고

        2. 카테고리 추가는 라우터 따로 만듬
           - **수정중에 있음**
             - category 추가는 완료
             - userupdate에서 분리하는 작업 필요
           - 수정 후에 1번기능에서 카테고리도 빼줘야함

  

  #### 1122

  - content 업데이트부분 하는중
    - 되긴되는데 중복된 태그 입력하면 오류나는중 고치기! 

  

  #### 1125

  - comment 
    - 쓰기 완료
    - 지우기 완료
    - 읽기 - 오류
      - 완료
- tag
  - category 가 안나오는데 확인
  - 입력값 str 도 확인해야함
  - 완료



#### 1126

- DB 연동 시간 지연되는것 개선
  - comments : 완료
  - tag : 완료
  - follow : 완료
  - category : 완료
  - auth : 완료
  - contents : 일단 완료
  - users : 고칠거 없음

#### 1127

- content filter = 검색기능인데 한번 확인해봐야함
  - list int로 받음...전체적으로 어떻게 받을지 정하면 좋음



#### 1205

- 애플 로그인 구현 
  
- 프론트와 연동필요
  
- #### 파일 시스템 도입

- User 로그인 부분에서 소셜로그인에서 이메일 입력 시 

  - 이메일이 있으면(일단 완료)
    - 어떤 플랫폼(애플, 카카오, 이메일)으로 로그인했는지 알려주는 메시지가 필요함
      - 카카오 완료
      - 애플은 나중에 연동하면서 고고

- #### 동기를 비동기로 바꿔야함

  - g500 에러가 가끔 날때가 있음 - 이 문제인듯?
  - 비동기 작업중 ----> push 하면 안됨 다음에 다같이 push
    - user는 완료했는데 라우터 다 막고 user만 테스트해보기? 1206







#### 1204

- 소셜 로그인
  - 카카오 - 기존처럼 accessToken 바로 받는 형식으로 변경해야함
  - 애플 - 카카오와 동일하게



#### 1210

- ~~env 변경~~
  - sqlite+libsql: 기존
- 일단 비동기화 사용하지 않고, 파일 데이터 사용하는 파트 진행하기
- ~~카카오 register 를 create_user 부분과 합치되 구분하는 로직 필요~~
  - 카카오 로그인 일단 완료
- 이미지, 파일 어떻게 처리할지 구상 시작
  - Vercel blob 사용중인데 api 잘 안됨



#### 1211

- Vercel blob 조금 더 디깅
  - 되는데 이제 엮으면 될듯



#### 1212

- 로그인/회원가입 파트 다시 로직, 라우터 구성해보기 효율적으로
  - 패스워드가 필수값이 아니면 될듯?
- 파일 시스템 엮는 부분 빨리 진행해보기



#### 1213

- 콘텐츠, init_db, engine, main 
  - async로 전환했음 
  - 테스트 해봐야함
- turso..libsql이 async 사용이 안되서  일단 미사용하게 해놨음
  - contents, async_deps 등등

#### 1215

- contents 
  - create 부분 추가함 되는지 git push 하고 확인하기



#### 1216

- git push 완료
- ~~현재 DB 연동이 잘 안되고있는데 점심먹고 확인 필요~~
  - 확인 완료
- content db 확인 완료
- create 부분 테스트 해보기



#### 1217

- auth
  - signup email
    - 완료
  - validate
    - 완료



#### 1218

- 타임아웃 에러
  - **콜드 스타트 최적화**  해보기
- user 
  - 약관, 광고 수신 동의 static 내용 추가해야함
    - 약관 주소 : `TERMS_URL` 추가 완료
  - 소셜 로그인
    - 카카오 로그인
      - id 값으로 로그인하는 예제 찾기 및 진행
    - 애플 로그인
      - 로직 구성하기

#### 1219

- 타임아웃/레이턴시 에러

  - **SQLAlchemy Core로 전환**: ORM 대신 SQLAlchemy Core를 사용해 명시적으로 쿼리를 작성하여 성능 최적화.

  - Connection Pool 설정 강화

    ```python
    engine = create_engine(
        str(settings.DATABASE_URI),
        pool_size=10,  # 최대 연결 수
        max_overflow=5,  # 추가 연결 허용 수
        pool_recycle=1800,  # 연결 재활용 시간
        pool_pre_ping=True  # 연결 체크 활성화
    )
    ```

  - 서버리스 환경에서 연결 유지

    ```python
    from threading import Thread
    import time
    
    def keep_connection_alive():
        while True:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            time.sleep(600)  # 10분마다 핑
            
    Thread(target=keep_connection_alive, daemon=True).start()
    ```



### 1221

- user -> **로그인 파트 STOP**
  - 카카오 로그인
    - 로직 변경함 - 토큰 해석 한번만함
  - 애플 로그인
    - 로직 구성중
  - update
    - 이미지 첨부 추가
- 서버 안정화
  - startup : python 시작할때 db 마이그레이션이 돌가는지 체크해보기
  - sqlalchemy orm : n+1 query -> 쿼리를 바꿔야할 수 도 있고, 스키마를 바꿔야 할 수도있다
  - db -server 간 계속 왔다갔다하는경우
  - connection pooling - sqlalchemy.pool — connction은 한개
  - 내 생각 : response data 만드는거 없애야할듯
  - 측정해보면서 진행하기
    - vercel latency 측정기



#### 1223

- 프로필 업데이트



#### 1224

- 로그인/기획 변화에 따른 api 변경



```json
db 연동하는데 있어서 시간을 줄이고 싶어 해당 코드에서 중복되는 쿼리나 시간이 지연될것같은 코드가 있으면 성능을 높히고 최적화 시켜줘
```

#### 확인 필요

1. [중요] List API의 느린속도 - 원인파악 및 해결 필요
   - sqlalchemy → n+1 query 문제일수도
   - 서버 - db 커넥션 pooling
     - (torso app에서 쿼리사용해보고 속도차이확인)
   - api startup time - vercel 서버리스 어떻게 동작하는지?
2. API 오류
   - 연동중 오류 생기면 공유
   - 조치

3. API Schema 싱크 맞추기
   - User에게 받지 않아도되는 입력값 등
   - Front - Back 요청 시 Schema 싱크 맞추기 각 API 마다 필요할듯

4. Image 업로드
   - 로그인 연동 후 Content 의 Image 파트 먼저 진행예정
   - 저장공간 확정 필요



  - commit - 중요내용 삭제해야함
    - 4b4b432
    - f00fbbc
      - rebase해봣는데 안됨..

  

  - 카테고리, 태그 입력

    ```
    # category, tag 태그명으로 관계형성
    INSERT INTO category_tags (category_id, tag_id)
    SELECT 3, id
    FROM tags
    WHERE name IN ('졸업작품', '패턴', '캐릭터', '포스터', '인물', '패션', '거리예술', '매거진', '회화', '3D')
    AND NOT EXISTS (
        SELECT 1 
        FROM category_tags 
        WHERE category_id = 3 AND tag_id = tags.id
    );
    
    # tag id 찾기
    SELECT id, name
    FROM tags
    WHERE name IN (
        '졸업작품',
        '캠페인',
        '패키지',
        '제품',
        '공간',
        '브랜드',
        '서비스',
        '포스터',
        '로고 디자인'
    );
    
    ```

    

  

  

  

  - 이후 진행
    - 검색
      - 작가 별명, 작품 제목, 작품 내용
        - 각 항목을 체크해서 검색할껀지? 아니면 통합해서 검색하는건지?
      - 카테고리, 태그
      - 전체적으로 and? or?
    - turso db 구조 변경시 migration 하는 방법 알아보기
    - static file 관리 -> 기본 API 만들고 진행 >>> 이후 진행
      - s3
      - uploadthing
      - blob
    - tag
      - 태그 입력(저장) 가능해야함
      - disassemble 테이블 필요할듯
      - 졸ㅈ -> 같은 경우  [ㅈㅗㄹㅈㅏㄱ] 으로 저장해야 검색이 가능
    - local turso 적용할 수있으면 적용해보기 - local 환경 나누기
    - :8080

  

  

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















