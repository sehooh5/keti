# 01_QPushButton

- 푸시 버튼(push button) 은 사용자가 프로그램에 명령을 내려서 어떤 동작을 하도록 할 때 사용되는 버튼이며, GUI 프로그래밍에서 가장 흔하게 사용되고 중요한 위젯

- **자주 쓰이는 메서드**

  | 메서드         | 설명                                                     |
  | :------------- | :------------------------------------------------------- |
  | setCheckable() | True 설정 시, 누른 상태와 그렇지 않은 상태를 구분합니다. |
  | toggle()       | 상태를 바꿉니다.                                         |
  | setIcon()      | 버튼의 아이콘을 설정합니다.                              |
  | setEnabled()   | False 설정 시, 버튼을 사용할 수 없습니다.                |
  | isChecked()    | 버튼의 선택 여부를 반환합니다.                           |
  | setText()      | 버튼에 표시될 텍스트를 설정합니다.                       |
  | text()         | 버튼에 표시된 텍스트를 반환합니다.                       |


  **자주 쓰이는 시그널**

  | 시그널     | 설명                              |
  | :--------- | :-------------------------------- |
  | clicked()  | 버튼을 클릭할 때 발생합니다.      |
  | pressed()  | 버튼이 눌렸을 때 발생합니다.      |
  | released() | 버튼을 눌렀다 뗄 때 발생합니다.   |
  | toggled()  | 버튼의 상태가 바뀔 때 발생합니다. |

- code : 

```python
## Ex 5-1. QPushButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('&Button1', self)
        btn1.setCheckable(True)
        btn1.toggle()

        btn2 = QPushButton(self)
        btn2.setText('Button&2')

        btn3 = QPushButton('Button3', self)
        btn3.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        self.setLayout(vbox)
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - ```python
    btn1 = QPushButton('&Button1', self)
    btn1.setCheckable(True)
    btn1.toggle()
    ```

    - QPushButton 클래스로 푸시 버튼을 하나 만듬.
    - 첫 번째 파라미터로는 버튼에 나타날 텍스트 지정
    - 두 번째는 버튼이 속할 부모 클래스를 지정
    - 버튼에 단축키(shortcut)를 지정하고 싶으면 아래와 같이 해당 문자 앞에 ampersand('&')를 넣기
    - setCheckable()을 True로 설정해주면, 선택되거나 선택되지 않은 상태를 유지
    - toggle() 메서드를 호출하면 버튼의 상태가 바뀜

  

  - ```python
    btn2 = QPushButton(self)
    btn2.setText('Button&2')
    ```

    -  단축키는 'Alt+2'

  

  - ```python
    btn3 = QPushButton('Button3', self)
    btn3.setEnabled(False)
    ```

    - btn3.setEnabled(False) 버튼 사용 불가