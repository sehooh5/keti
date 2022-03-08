# 리눅스 환경을 원격으로 사용하기

- Ubuntu 
- 윈도우에서 우분투 환경을 사용하기 위한 방법
- xrdp, xfce4 설치 후 사용
  - xrdp 는 기본적으로 원격을 사용하기 위한
  - xfce4 는 좀더 가볍게 사용하기 위함



## 설치과정



### 1. xrdp 설치

- 터미널을 열고 xrdp 설치 시작

  ```c
  sudo apt-get install xrdp
  ```



### 2. xfce4 설치

- xrdp 가 지원하는 환경인 xfce4 를 설치(조금 오래걸림)

  ```
  sudo apt-get update
  sudo apt-get install xfce4
  ```



### 3. xrdp에 xfce4를 연결하기

- xfce4의 Gnome 환경으로 연결(이 작업으로 인해서 UI가 다르고 독립적임)

  ```
  echo "xfce4-session">~/.xsession
  
  # 확인
  cat .xsession
  ```



### 4. xrdp 재시작해주기

- 접속 전에 xrdp 재시작해주고 로그아웃

  ```
  sudo service xrdp restart
  ```





---



## 후기



### 문제점

- **빈 화면만 뜰 때**, xfce4, xorg 등등 설치하면 됨
- **너무 느릴 때, **해상도를 낮추고 사용
- **xfce4 설치 후 튕길 때,** 위에 3번으로 xfce4를 기본 세션으로 작동하게끔
- keti1, keti2 서버는 작동이 가능한데, keti0이 작동이 안됨..