# 03_grid_layout

- 가장 일반적인 레이아웃 클래스
- 위젯의 공간을 행 (row)과 열 (column)로 구분
- QGridLayout 클래스를 사용
- code : 

```python
## Ex 4-3. 그리드 레이아웃.

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Title:'), 0, 0)
        grid.addWidget(QLabel('Author:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - 세 개의 라벨, 두 개의 라인 에디터, 하나의 텍스트 에디터를 그리드 형태로 배치

  - ```python
    grid = QGridLayout()
    self.setLayout(grid)
    ```

    - QGridLayout을 만들고, 어플리케이션 창의 레이아웃으로 설정

  - ```python
    grid.addWidget(QLabel('Title:'), 0, 0)
    grid.addWidget(QLabel('Author:'), 1, 0)
    grid.addWidget(QLabel('Review:'), 2, 0)
    ```

    - ` addWidget()` 메서드의 첫 번째 위젯은 추가할 위젯, 두, 세 번째 위젯은 각각 행과 열 번호를 입력
    - 세 개의 라벨을 첫 번째 열에 수직으로 배치

  - ```python
    grid.addWidget(QTextEdit(), 2, 1)
    ```

    - `QTextEdit()` 위젯 : `QLineEdit()` 위젯과 달리 여러 줄의 텍스트를 수정할 수 있는 위젯.
    - 세 번째 행, 두 번째 열에 배치