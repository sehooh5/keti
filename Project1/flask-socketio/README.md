# flask-socketio 를 사용한 실시간 통신

- flask-socketio  라이브러리를 사용하여 실시간으로 상호작용 할 수 있게 한다
- [참고](https://bokyeong-kim.github.io/python/flask/2020/05/09/flask(1).html)





## 기본 개념

### Flask?

- 파이썬으로 작성된 마이크로 웹 프레임워크
- 두개의 외부 라이브러리에 의존
  - Jinja2 템플릿 엔진
  - Werkzeug WSGI 툴킷



### Socket?

- 한 컴퓨터가 다른 컴퓨터와 상호 작용할 수 있는 경로를 설정
- 게이트가 열려있을 때, 즉 소켓이 열려있는 경우에만 통신을 가능하게 한다
- 채팅 기능을 만들 때 소켓은 필수적이다



### SocketIO

- 실제 전송 프로토콜에서 <u>클라이언트 응용 프로그램을 추상화</u>하는 브라우저 간 **Javascript 기반** 라이브러리
- SocketIO Javascript 라이브러리에 의해 노출 된 메시지 전달 프로토콜을 구현함
- SocketIO 를 사용하면 **브라우저**가 **응용 프로그램에 연결**할 수 있다



---



## flask에서 socket 만들기

- flask-socketIO 를 사용하면 <u>플라스크 응용프로그램</u>이 <u>**클라이언트**와 **서버**간의 양방향 통신</u>에 액세스 할 수 있다.

- 실행 전 pip 로 flask-socketIO 를 설치해 준다

  ```
  pip install flask-socketio
  ```

- 전체 코드를 먼저 작성 후 세부 내용을 정리하겠다



### 전체 코드

- **Server**(main.py)

  ```python
  from flask import Flask, render_template
  from flask_socketio import SocketIO
  
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
  socketio = SocketIO(app)
  
  
  @app.route('/')
  def sessions():
      return render_template('session.html')
  
  
  def messageReceived(methods=['GET', 'POST']):
      print('message was received!!!')
  
  
  @socketio.on('my event')
  def handle_my_custom_event(json, methods=['GET', 'POST']):
      print('received my event: ' + str(json))
      socketio.emit('my response', json, callback=messageReceived)
  
  
  if __name__ == '__main__':
      socketio.run(app, host='0.0.0.0', port=5001, debug=True)
  
  ```

- **Client**(session.html)

  ```php+HTML
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>Flask_Chat_App</title>
    </head>
    <body>
      <h3 style="color: #ccc; font-size: 30px">No message yet..</h3>
      <div class="message_holder"></div>
  
      <form action="" method="POST">
        <input type="text" class="username" placeholder="User Name" />
        <input type="text" class="message" placeholder="Messages" />
        <input type="submit" />
      </form>
  
      <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js"></script>
      <script type="text/javascript">
        var socket = io.connect("http://0.0.0.0:5001");
  
        socket.on("connect", function () {
          socket.emit("my event", {
            data: "User Connected",
          });
          var form = $("form").on("submit", function (e) {
            e.preventDefault();
            let user_name = $("input.username").val();
            let user_input = $("input.message").val();
            socket.emit("my event", {
              user_name: user_name,
              message: user_input,
            });
            $("input.message").val("").focus();
          });
        });
        socket.on("my response", function (msg) {
          console.log(msg);
          if (typeof msg.user_name !== "undefined") {
            $("h3").remove();
            $("div.message_holder").append(
              '<div><b style="color: #000">' +
                msg.user_name +
                "</b> " +
                msg.message +
                "</div>"
            );
          }
        });
      </script>
    </body>
  </html>
  
  ```

  



### 해석

#### Server

##### 기본코드

```python
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seho'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, debug=True) # host,port 임의 지정 가능
```

- Flask를 배치하여 app이라는 변수를 만든다.
- 암호화를 활성화하기 위해 SECRET_KEY를 환경변수에 선언.
- SocketIO는 ‘app’에 적용되고 있으며, 나중에 애플리케이션을 실행할 때 app 대신 socketio를 사용할 수 있도록 socketio 변수에 저장된다 (app -> socketio)
- **socketio는 웹 서버를 캡슐화**한다.
- run() 메소드는 기본적으로 Flask의 개발 웹 서버와 같은 localhost:5000에서 대기한다.
- debug = True를 사용하면 쉽게 오류를 정렬 할 수 있다.(필수는 아님)



##### + flask view

```python
@app.route('/')
def sessions():
    return render_template('session.html')
```

- app.route 로 URL 경로가 ('/') 일때 'templates' 폴더의 'session.html' 이 렌더링 되게 해준다

- 잘 렌더링 되는지 확인하고 싶으면 아래처럼 'session.html'을 간이로 작성한 뒤, 'main.py '를 실행시켜본다

  - ```html
    <html>
        <head>
            <title>Session</title>
        </head>
        <body>
            <p>Hello</p>
        </body>
    </html>
    ```

  - 잘 된다면 Hello 라는 문자열이 해당 서버주소와 포트번호 호출 시 브라우저에 나타난다



##### + flask socket Handling

```python
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
```

- 서버에서 클라이언트가 보낸 메시지를 받는 방법, 클라이언트의 메시지를 확인하는 방법
- **@socketio.on()** : 이벤트 핸들러 데코레이터, 클라이언트에서 WebSocket 메시지를 수신하기 위함
- **send()** 및 **emit()** 함수를 사용하여 연결된 클라이언트에 응답 메시지를 보낼 수 있다.
- ‘my event’ 를 트리거할 때 ‘handle_my_custom_event’ 함수는 먼저 json 객체를 수신하여 print 한 후, 나중에 ‘my response’ 이벤트로 전송한다. callback(콜백)은 서버에 의해 메시지가 수신되는지 여부를 알 수 있도록 도와주는 디버깅 기법의 일종이다.(위의 경우 messageRecevied함수를 불러옴)





#### Client

##### 채팅 타이핑 하는 부분

```html
<form action="" method="POST">
      <input type="text" class="username" style='font-size:15px;' placeholder="User Name"/>
      <input type="text" class="message" style='font-size:15px;' placeholder="Messages"/>
      <input type="submit"/>
</form>
```



##### jquery 와 socket.js 사용할 수 있게 script 가져오기

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js"></script>
```



##### io.connect 로 해당 서버와 연결

```javascript
var socket = io.connect('http://' + document.domain + ':' + location.port);
```

- 연결 설정 및 세션 생성에 **io.connect()**를 사용
- 두 사용자 모두를 http://127.0.1:5000이라는 동일한 URL에 연결하여 세션 생성
- 아래 코드의 **document.domain**은 작업 중인 컴퓨터의 IP 주소를 나타낸다.
- **location.port**는 포트를 나타내며, 기본값은 5000 (flask)



##### 발생 이벤트 처리

```javascript
socket.on( 'connect', function() {
  socket.emit( 'my event', {
    data: 'User Connected'
  })
  var form = $( 'form' ).on( 'submit', function( e ) {
    e.preventDefault()
    let user_name = $( 'input.username' ).val()
    let user_input = $( 'input.message' ).val()
    socket.emit( 'my event', {
      user_name : user_name,
      message : user_input
    })
    $( 'input.message' ).val( '' ).focus()
  })
})
```

- socket.on()에 대한 첫 번째 인수는 이벤트 이름
  - ‘connect’, ‘disconnect’, ‘message’, ‘json’은 socketIO에 의해 생성된 특수 **이벤트**.
  - 다른 모든 이벤트 이름은 사용자 정의 이벤트로 간주된다.
    - ‘message’ : 형식 문자열의 페이로드(payload)를 전달
    - ‘json’ : json 사용자 정의 이벤트는 파이썬 사전의 형태로 JSON 페이로드(payload)를 전달
- 이벤트를 보내기 위해 flask server는 flask socketIO에서 제공하는 send(), emit() 기능을 사용할 수 있다.
- send() 함수는 문자열 또는 JSON 유형의 표준 메시지를 클라이언트로 보낸다.
- emit() 함수는 데이터와 함께 사용자 정의 이벤트 이름(위 코드에서는 ‘my event’)으로 메시지를 전송한다.
- POST 메소드를 호출한 후 이벤트 ‘e’가 인수로 전달되며, 여기서 preventDefault() 메서드가 호출되어 전달이 금지된다. 그리고 나중에 입력 필드, 사용자 이름 및 메시지에서 값을 가져온다.
- 그런 다음 emit()을 통해 이전에 ‘main.py’에서 정의한 ‘my event’로 전달된다.
- 그 후 메시지 필드에는 전달했던 값이 사라지고 빈칸으로 변경된다.(focus()사용)



##### 응답 온 부분 처리

```javascript
socket.on( 'my response', function( msg ) {
  console.log( msg )
  if( typeof msg.user_name !== 'undefined' ) {
    $( 'h3' ).remove()
    $( 'div.message_holder' ).append('<div><b style="color:#000">'+msg.user_name+'</b>'+msg.message+'</div>' )
  }
})
```

- 일단 메시지를 이벤트를 통해 보내면, 수신된 메시지를 HTML 페이지에 렌더링해야 한다.
- 응답으로 메시지가 수신되는 즉시 메시지를 “message_holder” 클래스 (h3 태그의 텍스트 (“No message yet”)가 제거됨)로 전달한다. 여기서 메시지는 이전 메시지에 추가된다.