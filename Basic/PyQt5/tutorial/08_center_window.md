# 08_center_window

- 창을 화면 가운데로
- code : 

```python
## Ex 3-8. 창을 화면의 가운데로.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 
  - `self.center()` : 창이 화면 가운데 위치하는 메서드 생성
  - `qr = self.frameGeometry()` : `frameGeometry()` 메서드로 창의 위치와 크기정보 가져오기
  - `cp = QDesktopWidget().availableGeometry().center()` : 모니터 화면의 가운데 위치를 파악
  - `qr.moveCenter(cp)` : 창의 직사각형 위치를 화면의 중심의 위치로 이동
  - `self.move(qr.topLeft())` : 
    - 현재 창을, 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동
    - 결과적으로 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데에 나타나게 됨

