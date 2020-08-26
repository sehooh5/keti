# Python 환경구성(Ubuntu)

- Python 3.7.6
- VS Code

## Python 설치

1. python 최신버전 확인

   - 홈페이지 : https://www.python.org/downloads/
   - 현재 2020년 8월 25일 기준 : v 3.8.5

2. 개발 라이브러리 다운

   ```bash
   $ sudo apt-get install build-essential checkinstall
   $ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
       libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
   ```

3. Python 다운로드(안정화 버전 : v 3.7.6)

   ```bash
   $ cd /opt
   $ sudo wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
   $ sudo tar xzf Python-3.7.6.tgz
   ```

4. Python 컴파일

   ```bash
   $ cd Python-3.7.6
   $ sudo ./configure --enable-optimizations
   $ sudo make altinstall
   ```

5. 버전 확인

   ```bash
   $ python3.7 -V
   Python-3.7.6
   ```

6. Python 커맨드의 디폴트로 설정

   - update-alternatives 명령어로 커맨드의 디폴트 경로를 설정해줄 수 있다

   - 설치 경로 찾기 : `whereis python3`

     ```bash
     sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7 6
     ```

7. 설정 후 확인

   ```bash
   $ python -V
   ```



---

## VS Code

1. curl 설치

```bash
$ sudo apt-get install curl
```



2. MS 의  GPG 키 다운로드해 /etc/apt/trusted.gpg.d/ 경로에 복사

```bash
$ sudo sh -c 'curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg'
```



3. 저장소 추가

```bash
$ sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
```



4. 저장소로 부터 패키지 목록 가져오기

```bash
$ sudo apt update
```



5. VS Code 설치

```bash
$ sudo apt install code
```



6. 터미널 또는 데스크톱 환경에서 실행

```bash
$ code
```



7. 만약 git error 뜨면 git 설치

```bash
$ sudo apt-get install git
```



