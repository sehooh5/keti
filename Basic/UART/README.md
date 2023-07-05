# UART 

- UART 통신, GPS 를 사용하면서 정리한 기초 자료



### UART 통신

- UART 통신이랑 Serial 통신으로, 데이터 전송 혹은 수신 핀이 하나인 통신이다

- 한 번에 1byte씩 보내고 각 bit는 차례(직렬)로 전송된다

  - bit : 메모리에 있는 이진수(binary)의 한 자리
  - byte : 8개의 bit, 256가지의 표현이 가능

- 데이터를 보내는 쪽과 받는 쪽의 데이터 전송 속도가 올일 해야하는데 이때의 통신 속도를 **baudrate**라 한다

  - baudrate 범위 : 115200, 57600, 9600 등

- 실제 데이터를 보낼 때 1byte 이상의 데이터를 전송해야하는데, 보내고 받는 데이터의 형실을 명시해주고 받아야 한다. 간단한 패킷의 구조는 아래와 같다.

  ![image](https://github.com/sehooh5/keti/assets/58541635/d1f17ad5-2747-4411-b503-485cf9158287)

  - 처음 2byte는 데이터의 시작을 알리는 Header로 고정한다. 그 후 Data+Check sum의 수를 알려주는 1byte를 보내고 Data, Check sum 순으로 보낸다. 
  - Header는 약속된 0~255 사이의 숫자이고
  - Check sum 은 앞의 데이터가 중간에 깨지지 않고 잘 갔는지 확인하기 위한 byte이다.