# Ubuntu

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



### 이더넷 연결 가능하게 네트워크 설정 [(참고)](https://webdir.tistory.com/188)

- `ifconfig`  로 해당 네트워크 환경 확인

- GUI : `Network` 환경 설정 검색 후 변경 가능

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

  

