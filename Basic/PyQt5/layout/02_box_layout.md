# 02_box_layout

- 박스 레이아웃 클래스를 이용하면 훨씬 유연하고 실용적인 레이아웃 가능
- QHBoxLayout, QVBoxLayout 생성자는 수평, 수직의 박스를 하나 만드는데, 다른 레이아웃 박스를 넣을 수도 있고 위젯을 배치할 수 있음
- code : 

```python
## Ex 4-2. 박스 레이아웃.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - 창의 가운데 아래에 두 개의 버튼을 배치

  - 두 개의 버튼은 창의 크기를 변화시켜도 같은 자리에 위치

  - ```python
    okButton = QPushButton('OK')
    cancelButton = QPushButton('Cancel')
    ```

    - 두 개의 버튼 생성

  - ```python
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(okButton)
    hbox.addWidget(cancelButton)
    hbox.addStretch(1)
    ```

    - `QHBoxLayout()` : 수평 박스를 하나 만들고 
    - `addStretch(1)` :  신축성있는 빈 공간을 제공
      - 두 버튼 양쪽의 stretch factor가 1로 같기 때문에 이 두 빈 공간의 크기는 창의 크기가 변화해도 항상 같음(반응형)

  - ```python
    vbox = QVBoxLayout()
    vbox.addStretch(3)
    vbox.addLayout(hbox)
    vbox.addStretch(1)
    ```

    - `QVBoxLayout()` : 수직 박스를 하나 만들고 
    - `vbox.addLayout(hbox)` : 수평 박스(hbox)를 수직 박스(vbox)에 넣어줌
    - `addStretch(3)` : 위 공간을 더 크게주어서 수평박스를 아래로 내려주는 효과

  - `self.setLayout(vbox)` : 최종적으로 수직 박스를 창의 메인 레이아웃으로 설정

