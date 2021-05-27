# 05_statusBar

- 상태바 만들기 

- 상태바는 어플리케이션의 상태를 알려주기 위해 하단에 위치하는 위젯

- Main Window 는 메뉴바, 툴바, 상태바를 갖는 전형적인 어플리케이션 창

  ![image](https://user-images.githubusercontent.com/58541635/119779656-e869ff80-bf03-11eb-885b-8f36da9ec20c.png)

-  QMenuBar, QToolBar, QDockWidget, QStatusBar를 위한 고유의 레이아웃을 갖고 있음

- 가운데 Central Widget 을 위한 영역이 있는데 여기에는 어떠한 위젯도 들어올 수 있음

- code : 

```python
## Ex 3-5. 상태바 만들기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready', 1000) 

        self.setWindowTitle('Statusbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 
  - `self.statusBar().showMessage('Ready', 1000)` : 
    - 상태바는 QMainWindow 클래스의 statusBar() 메서드를 이용해서 만듬
    - `showMessage()` 메서드를 통해 상태바에 보여질 메세지를 설정
    - 두 번째 인자는 int(micro seconds)
    - 텍스트가 사라지게 하고 싶으면 : 
      - `clearMessage()` 메서드를 사용
      - `showMessage()` 메서드에 텍스트가 표시되는 시간을 설정