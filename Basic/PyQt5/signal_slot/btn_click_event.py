import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # form
        self.setWindowTitle('Hello Bryan')
        self.center()  # self.move(500,200)    # 창 위치
        self.resize(500, 200)   # 창 크기

        # 버튼 정의
        btnRun = QPushButton("Run", self)  # 버튼 텍스트
        btnRun.move(20, 20)  # 버튼 위치
        btnRun.clicked.connect(self.btnRun_clicked)  # 클릭 시 실행할 function

    def btnRun_clicked(self):
        QMessageBox.about(self, "message", "clicked")

    '''
    화면의 가운데로 띄우기
    '''

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec_()
