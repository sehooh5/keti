# 03_close_window

- 프로그래밍으로 창 닫기
- signal, slot 다뤄보기
- code : 

```python
## Ex 3-3. 창 닫기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication # 새롭게 추가


class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      btn = QPushButton('Quit', self)
      btn.move(50, 50)
      btn.resize(btn.sizeHint())
      btn.clicked.connect(QCoreApplication.instance().quit)

      self.setWindowTitle('Quit Button')
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 
  - `from PyQt5.QtCore import QCoreApplication` : QCoreApplication 클래스 불러오기
  - `btn = QPushButton('Quit', self)` : 
    - 푸시버튼 생성
    - 첫 번째 파라미터에는 버튼에 표시될 텍스트, 두 번째 파라미터에는 버튼이 위치할 부모 위젯 입력
  - `btn.clicked.connect(QCoreApplication.instance().quit)` :
    - PyQt5 에서의 이벤트 처리는 Signal 과 Slot 메커니즘으로 이루어짐
    - `btn` 을 클릭하면 'clicked' 시그널이 만들어짐
    - `instance()` 메서드는 현재 인스턴스를 반환
    - 'clicked' 시그널은 어플리케이션을 종료하는 `quit()` 메서드에 연결
    - 이렇게 Sender와 Receiver, 두 객체 간에 커뮤니케이션이 이루어짐
    - Sender(btn) - Receiver(app)

