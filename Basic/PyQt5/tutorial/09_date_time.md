# 09_date_time

- QtCore 모듈의 **QDate**, **QTime**, **QDateTime** 클래스를 이용해서 어플리케이션에 날짜와 시간을 표시
- code : 

```python
## Ex 3-9. 날짜와 시간 표시하기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, Qt


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
```

- 설명 : 

  - **Date** : 

    ```python
    from PyQt5.QtCore import QDate, Qt
    
    now = QDate.currentDate()
    print(now.toString('d.M.yy'))					# 2.1.19
    print(now.toString('dd.MM.yyyy'))				# 02.01.2019
    print(now.toString('ddd.MMMM.yyyy'))			# 수.1월.2019
    print(now.toString(Qt.ISODate))					# 2019-01-02
    print(now.toString(Qt.DefaultLocaleLongDate))	# 2019년 1월 2일 수요일
    
    ### 결과 값 ###
    
    02.01.2019
    수.1월.2019
    2019-01-02
    2019년 1월 2일 수요일
    ```

    - **currentDate()** 메서드는 현재 날짜를 반환
    - **toString()** 메서드를 통해 현재 날짜를 문자열로 출력

  - **Time** : 

    ```python
    from PyQt5.QtCore import QTime, Qt
    
    time = QTime.currentTime()
    print(time.toString('h.m.s'))						# 16.2.3
    print(time.toString('hh.mm.ss'))					# 16.02.03
    print(time.toString('hh.mm.ss.zzz'))				# 16.02.03.610
    print(time.toString(Qt.DefaultLocaleLongDate))		# 오후 4:02:03
    print(time.toString(Qt.DefaultLocaleShortDate))		# 오후 4:02
    ```

  - **DateTime** : 

    ```python
    from PyQt5.QtCore import QDateTime, Qt
    
    datetime = QDateTime.currentDateTime()
    print(datetime.toString('d.M.yy hh:mm:ss'))
    print(datetime.toString('dd.MM.yyyy, hh:mm:ss'))
    print(datetime.toString(Qt.DefaultLocaleLongDate))
    print(datetime.toString(Qt.DefaultLocaleShortDate))
    ```

    