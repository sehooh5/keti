# 02_add_favicon

- Favicon 추가하기
- code : 

```python
## Ex 3-2. 어플리케이션 아이콘 넣기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      self.setWindowTitle('Icon')
      self.setWindowIcon(QIcon('C://Users/KETI/Desktop/keti/Basic/PyQt5/images/web.png'))
      self.setGeometry(300, 300, 300, 200)
      self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())
```

- 설명 : 
  - `elf.setWindowIcon(QIcon('web.png'))` : 경로와 함께 파비콘 이미지 입력
  - `self.**set**Geometry(300, 300, 300, 200)` : 창의 위치와 크기 설정 동시에

