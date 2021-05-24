# 04_toggle_tooltip

- 어떤 위젯의 기능을 설명하는 등의 역할을 하는 말풍선 형태의 도움말, 툴팁 나타내기
- 위젯에 있는 모든 구성 요소에 대해서 툴팁(tooltip)이 나타냄
-  setToolTip() 메서드를 이용해서 위젯에 툴팁을 만들기
- code : 

```python
## Ex 3-4. 툴팁 나타내기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QFont


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())

        self.setWindowTitle('Tooltips')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 
  - `QToolTip.setFont(QFont('SansSerif', 10)` : 툴팁 폰트 설정
  - `self.setToolTip('This is a <b>QWidget</b> widget')` : 표시될 텍스트 입력
  - `btn.setToolTip('This is a <b>QPushButton</b> widget')` : 버튼에도 툴팁 달아주기
  - `btn.resize(btn.sizeHint())` : 버튼을 적절한 크기로 설정