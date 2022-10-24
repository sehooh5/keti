# Dockerfile 작성요령

- [참고 페이지](https://subicura.com/2017/02/10/docker-guide-for-beginners-create-image-and-deploy.html)

### 작성요령

Dockerfile의 명령은 위에서 아래로 차례대로 실행한다. [출처](https://sungwookkang.com/1303)

- FROM : 생성할 이미지의 베이스 이미지를 입력한다. 이미지가 로컬에 없다면 자동으로 도커허브에서 pull 한다.

- LABEL : “키:값” 형태로 이미지에 메타데이터 추가. 추가된 메타 데이터는 docker inspect 명령어로 확인가능.

- WORKDIR : 명령어를 실행할 디렉터리를 나타냄. Bash에서 cd 명령과 동일한 기능이다.

- COPY : 로컬 디렉터리의 파일을 이미지에 복사하는 역할. ADD와 다른 점은 COPY는 로컬 디렉터리만 가능하고 ADD는 외부 URL및 tar 파일도 추가 가능하다.

- RUN : 이미지를 만들기 위해 컨테이너 내부에서 명령어를 실행.

- EXPOSE : Dockerfile의 빌드로 생성된 이미지에서 노출할 포트를 설정

- CMD : 컨테이너가 시작될 때마다 실행할 명령어(커맨드)를 설정, Dockerfile에서 한번만 사용할 수 있다.



### Dockerfile 예시

```dockerfile
FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install click Flask itsdangerous Jinja2 MarkupSafe Werkzeug numpy

RUN mkdir /app
WORKDIR /app
ADD ./video-streaming /app/
ENV OPENCV_VERSION="4.1.0"
RUN pip install opencv-python
RUN ln -s \
  /usr/local/python/cv2/python-3.7/cv2.cpython-37m-x86_64-linux-gnu.so \
  /usr/local/lib/python3.7/site-packages/cv2.so

EXPOSE 5058
CMD ["python", "/app/app.py"]
```

#### RUN 1 

- 리눅스 패키지 업데이트 및 인스톨
- 패키지 종류
  - build-essential :  개발에 필요한 기본 라이브러리와 헤더파일등을 가지고 있음
  - cmake : 운영체제에 관계없이 하나의 코드만으로 실행 파일을 생성해주는 크로스 컴파일러 프로그램
  - wget : 웹 서버로부터 콘텐츠를 가져오는 컴퓨터 프로그램. HTTP, HTTPS, FTP를 통해 내려받기지원
  - unzip : zip으로 압축된 파일을 푸는 명령어
  - yasm : 어셈블리 컴파일러로 ffmpeg는 빌드 시 Yasm을 사용한다
  - pkg-config : 소스 코드로부터 소프트웨어를 컴파일할 목적으로 설치된, <u>라이브러리를 조회</u>하기 위해 통일된 인터페이스를 제공하는 컴퓨터 소프트웨어
  - -dev 패키지들 : 컴파일을 위한 헤더 및 라이브러리 패키지, 다른 프로그램들을 위한 라이브러리 역할과 소스코드 컴파일



