# Showbility - sehooh5

- Showbility Project 내 오세호 개인 파일
- ssh -i [개인키].pem ubuntu@13.209.10.151
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
- 



#### 0915

- AWS - Dev Server 연동 시작
