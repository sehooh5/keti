# 02_QLabel

-  텍스트 또는 이미지 라벨을 만들 때
- 사용자와 어떤 상호작용을 제공하지는 않음
- 기본적으로 수평 방향으로는 왼쪽, 수직 방향으로는 가운데 정렬, setAlignment() 메서드를 통해 조절가능
- code : 

```python
## Ex 5-2. QLabel.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel('Second Label', self)
        label2.setAlignment(Qt.AlignVCenter)

        font1 = label1.font()
        font1.setPointSize(20)

        font2 = label2.font()
        font2.setFamily('Times New Roman')
        font2.setBold(True)

        label1.setFont(font1)
        label2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        self.setLayout(layout)

        self.setWindowTitle('QLabel')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - ```python
    label1 = QLabel('First Label', self)
    label1.setAlignment(Qt.AlignCenter)
    ```

    - 생성자에 라벨 텍스트와 부모 위젯을 입력
    - setAlignment() 메서드로 라벨의 배치를 설정
    - Qt.AlignCenter로 설정해주면 수평, 수직 방향 모두 가운데 위치

  

  - ```python
    font1 = label1.font()
    font1.setPointSize(20)
    ```

    - 라벨에 사용될 폰트 만들기
    - setPointSize() 메서드로 폰트의 크기를 설정

  

  - ```python
    label2 = QLabel('Second Label', self)
    label2.setAlignment(Qt.AlignVCenter)
    ```

    -  두번째 라벨 수직 방향으로만 가운데 (Qt.AlignVCenter)로 설정

  

  - ```python
    font2 = label2.font()
    font2.setFamily('Times New Roman')
    font2.setBold(True)
    ```

    - setFamily() 메서드로 폰트의 종류를 'Times New Roman'으로 설정
    - setBold(True)로 폰트를 진하게 설정
    - 폰트의 크기를 설정하지 않았기 때문에 디폴트 크기인 13으로 설정