# 07_toolBar

- 툴바 만들기
- 툴바(toolbar)는 자주 사용하는 명령들을 더 편리하게 사용할 수 있도록 해줌
- code : 

```python
## Ex 3-7. 툴바 만들기.

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

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.setWindowTitle('Toolbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - ```python
    self.toolbar = self.addToolBar('Exit')
    self.toolbar.addAction(exitAction)
    ```

    - `self.toolbar = self.addToolBar('Exit')` : Exit 라는 toolbar 생성
    - `self.toolbar.addAction(exitAction)` : exitAction 동작 추가

