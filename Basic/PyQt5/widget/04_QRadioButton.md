# 04_QRadioButton

- 사용자가 선택할 수 있는 버튼을 만들 때 사용
- 한 번에 여러 버튼을 선택할 수 있도록 하려면 setAutoExclusive() 메서드에 False를 입력
- 한 위젯 안에 여러 개의 exclusive 버튼 그룹을 배치하고 싶다면 QButtonGroup() 메서드를 사용
- 박스와 마찬가지로 버튼의 상태가 바뀔 때, toggled() 시그널이 발생
- 특정 버튼의 상태를 가져오고 싶을 때, isChecked() 메서드를 사용

- 자주 쓰이는 메서드

| 메서드       | 설명                               |
| :----------- | :--------------------------------- |
| text()       | 버튼의 텍스트를 반환합니다.        |
| setText()    | 라벨에 들어갈 텍스트를 설정합니다. |
| setChecked() | 버튼의 선택 여부를 설정합니다.     |
| isChecked()  | 버튼의 선택 여부를 반환합니다.     |
| toggle()     | 버튼의 상태를 변경합니다.          |



- 자주 쓰이는 메서드

| 메서드     | 설명                                     |
| :--------- | :--------------------------------------- |
| pressed()  | 버튼을 누를 때 신호를 발생합니다.        |
| released() | 버튼에서 뗄 때 신호를 발생합니다.        |
| clicked()  | 버튼을 클릭할 때 신호를 발생합니다.      |
| toggled()  | 버튼의 상태가 바뀔 때 신호를 발생합니다. |

- code : 

```python
## Ex 5-4. QRadioButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        rbtn1 = QRadioButton('First Button', self)
        rbtn1.move(50, 50)
        rbtn1.setChecked(True)

        rbtn2 = QRadioButton(self)
        rbtn2.move(50, 70)
        rbtn2.setText('Second Button')

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QRadioButton')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - ```python
    rbtn1 = QRadioButton('First Button', self)
    ```

    - QRadioButton을 하나 만듬

  

  - ```python
    rbtn1.setChecked(True)
    ```

    - True로 설정하면 프로그램이 실행될 때 버튼이 선택되어 표시

  

  - ```python
    rbtn2.setText('Second Button')
    ```

    - setText() 메서드를 통해서도 라벨의 텍스트를 설정