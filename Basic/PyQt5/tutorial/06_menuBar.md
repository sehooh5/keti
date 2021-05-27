# 06_menuBar

- 메뉴바 만들기
- code : 

```python
## Ex 3-6. 메뉴바 만들기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - 메뉴 한개 설정, 종료하는 기능, 단축기 사용 가능

  - ```python
    exitAction = QAction(QIcon('exit.png'), 'Exit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    ```

    - 이 세 줄의 코드가 하나의 동작을 만듬
    - 첫 째 줄 : action 정의, Icon 그림 설정(사용 안해도됨), 'Exit' 이름 설정
    - 둘 째 줄 : Shortcut 지정
    - 셋 째 줄 : toggle, 즉 툴팁 설정(status bar 에서 보여짐)

  - `exitAction.triggered.connect(qApp.quit)` : 

    - 이 동작을 선택하면, 생성된 (triggered) 시그널이 QApplication 위젯의 quit() 메서드에 연결되고, 어플리케이션을 종료

  - ```python
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)
    ```

    - `menuBar()` : 메뉴바를 생성
    - `fileMenu = menubar.addMenu('&File')` : 
      - 'File'  메뉴 생성 
      - &(앰퍼샌드)는 간편하게 단축키를 설정하도록해줌...(F 앞에 & = `Alt+F`)
    - `fileMenu.addAction(exitAction)` : 'exitAction' 동작 추가