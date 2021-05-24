# 01_open_widget

- 그냥 창 띄우기
- 기본 적인 내용들은 코드가 다 구성되어있다
- code : 

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300) # 위치
        self.resize(400, 200) # 창 사이즈
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
```

- 설명
  - 기본적인 UI 구성요소를 제공하는 위젯 (클래스)들은 PyQt5.QtWidgets 모듈에 포함
  - `self.setWindowTitle('')`  : 윈도우의 이름 설정
  - `move()` : 위젯을 x,y 위치로 이동
  - `resize()` : 위젯 크기 설정
  - `show()` : 위젯을 스크린에 보여주기
  - `if __name__ == '__main__':` : '`__name__`'은 현재 모듈의 이름이 저장되는 내장 변수
    - 만약 'moduleA.py'라는 코드를 import해서 예제 코드를 수행하면 `__name__` 은 'moduleA'가 된다.  그렇지 않고 코드를 직접 실행한다면 `__name__` 은 `__main__` . 
    - 이 한 줄의 코드를 통해 프로그램이 직접 실행되는지 혹은 모듈을 통해 실행되는지를 확인
  - `app = QApplication(sys.argv)` : 모든 PyQt5 어플리케이션은 어플리케이션 객체를 생성해야 함