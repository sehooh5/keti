# README

- 이번 프로젝트에서 카메라 제어 및 화면 제어 시 이용하는 방법 중 한 가지인 REST API 활용
- REST API를 사용하여 워커 노드의 카메라 url 값을 전달하고 화면을 제어한다





## REST API?

- **REpresentational State Transfer**의 약자
- HTTP기반으로 필요한 자원에 접근하는 방식을 정해놓은 아키텍쳐
- 저장된 데이터(DBMS)는 물론, 이미지/동영상/문서(pdf 등)와 같은 파일, 서비스(이메일 전송, 푸쉬 메시지 등)를 모두 포함



### 속성

1. 서버에 있는 모든 resource는 각 resource 당 클라이언트가 바로 접근 할 수 있는 고유 URI가 존재
2. 모든 요청은 클라이언트가 요청할 때마다 필요한 정보를 주기 때문에 서버에서는 세션 정보를 보관할 필요가 없음, 그렇기 때문에 서비스에 자유도가 높아지고 유연한 아키텍쳐 적응이 가능
3. HTTP 메소드를 사용. 모든 resource는 일반적으로 http 인터페이스인 GET, POST, PUT, DELETE 4개의 메소드로 접근 되어야한다
4. 서비스 내에 하나의 resource가 주변에 연관 된 리소스들과 연결되어 표현이 되어야 한다



### 구성요소

- resource, method, message



#### resource

- REST에서는 자원에 접근할 때 URI 로 하게 된다



#### method

- **GET, POST**, PUT, DELETE 등의 HTTP메소드를 사용한다



#### message

- HTTP header 와 body, 응답상태 코드로 구성되어 있고, header 와 body 에 포함된 메시지는 메시지를 처리하기 위한 충분한 정보를 포함한다
- body : 자원에 대한 정보를 전달 (format : JSON / XML / 사용자 정의 포맷)
- header : body에 어떤 포맷으로 데이터가 담겼는지 정의 ( 요청 : Accept / 응답 : Contente-type)



---



## 우리가 사용할 방식

1. Manager App 에서는 Viewer App 에 URL 값만 보내준다
2. Viewer App 은 해당 URL 값을 받아 해당 영상을 스트리밍 해준다
3. Viewer App 은 노드별로 각각 다른 NodePort 번호를 갖고 있다

4. SSE (Server-Sent Events)



## ~~SSE 를 이용한 실시간 웹앱~~

- ~~서버가  HTTP 연결을 열린 상태로 유지하고 필요할 때 마다 클라이언트에게 데이터를 줄 수 있게 해주는 서버 푸시 기술~~
- ~~[sse 예제 : 기본 시간 문자열이 브라우저에 갱신됨](http://tcpschool.com/html/html5_api_sse)~~ 



## Flask_socketio 사용 -> 폴더 이동

- [원본 예제](https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d)
- [원본 예제 사용한 한글 예제](https://1532468.github.io/bucket/AS_Flask_2_Socket/)



