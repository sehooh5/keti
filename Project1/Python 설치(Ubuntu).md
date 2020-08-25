# Python 설치(Ubuntu)

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

   