# Ubuntu

- Version : 18.04

### Ubuntu 설치파일 다운로드 및 설치용 USB 만들기

- Rutus 사용하여 설치용 USB 만들어서 사용



### USB 플러그인 후 재부팅 시 설치

- `delete` 키로 설치모드로 연결



### [문제] ifcofig 입력 시 찾을수 없다고 뜸

- 아래 명령어로 툴 설치

```bash
sudo apt-get install net-tools
```

- 서버 문제로 `Software&Update` 에서 서버를 변경(한국 서버가 다운 많이 된다함)



### Ubuntu 이더넷 연결 가능하게 네트워크 설정



### 우분투 방화벽(UFW) 설정

```bash
# check
sudo ufw status verbose

# active 
sudo ufw enable

# inactive
sudo ufw disable
```



### 이더넷 연결 가능하게 네트워크 설정 [(참고)](https://webdir.tistory.com/188)

- `ifconfig`  로 해당 네트워크 환경 확인

- **GUI : `Network` 환경 설정 검색 후 변경 가능**(이거 사용했음)

  CLI : 아래 처럼 수정해줘야 함

  ```bash
  sudo vi /etc/network/interfaces 
  # This file describes the network interfaces available on your system 
  # and how to activate them. For more information, see interfaces(5). 
  
  # The loopback network interface 
  
  auto lo iface lo 
  inet loopback 
  
  # The primary network interface 
  # auto eth0 
  # iface eth0 inet dhcp 
  
  # menual 
  auto eth0 
  iface eth0 inet static 
  address 192.168.100.5
  netmask 255.255.255.0 
  netwrok 192.168.0.1
  broadcast 192.168.0.255
  gateway 192.168.100.1 
  
  dns-nameservers 168.126.63.1 168.126.63.2 8.8.8.8
  
  ```

- 네트워크 재시작

```bash
sudo /etc/init.d/networking restart
```



### apt-get update 명령 시 주소를 못찾아올 때

- 패키지 다운로드 서버를 변경해준다

- `sources.list` 안에 내용 변경

  ```bash
  sudo vi /etc/apt/sources.list
  ```

- 내용 변경하는 명령어 `:`를 입력한 후에

  ```bash
  %s/kr.archive.ubuntu.com/ftp.daumkakao.com
  ```

  명령어 치면 변경이 몇개 되었는지 나오고 `:wq`로 저장하고 빠져나오기

- 나는 wifi 연결이 아니라 이더넷으로 연결되어있어서 온라인이 아니어서 오류났었던것