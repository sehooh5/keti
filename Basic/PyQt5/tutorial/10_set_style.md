# 10_set_style

- 스타일 꾸미기,  `setStyleSheet()`
- code : 

```python
## Ex 3-10. 스타일 꾸미기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl_red = QLabel('Red')
        lbl_green = QLabel('Green')
        lbl_blue = QLabel('Blue')

        lbl_red.setStyleSheet("color: red;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: #FA8072;"
                             "border-radius: 3px")
        lbl_green.setStyleSheet("color: green;"
                               "background-color: #7FFFD4")
        lbl_blue.setStyleSheet("color: blue;"
                              "background-color: #87CEFA;"
                              "border-style: dashed;"
                              "border-width: 3px;"
                              "border-color: #1E90FF")

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        vbox.addWidget(lbl_blue)

        self.setLayout(vbox)

        self.setWindowTitle('Stylesheet')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - 세 개의 라벨 위젯을 여러 스타일로 꾸미기

  - ```python
    lbl_red = QLabel('Red')
    lbl_green = QLabel('Green')
    lbl_blue = QLabel('Blue')
    ```

    - QLabel 클래스를 이용해서 세 개의 라벨 위젯 생성
    - 라벨 텍스트는 각각 'Red', 'Green', 'Blue'로 설정

  - `lbl_red.setStyleSheet(설정~~)` : 각 라벨 다양하게 설정

  - `vbox = QVBoxLayout()` : Q vertical Layout, 즉 수직 레이아웃 배치

  - `vbox.addWidget()` : 위젯 추가 

