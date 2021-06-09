#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QTabWidget, QVBoxLayout, QPushButton, QCheckBox, QRadioButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(50, 50, 100, 100)  # x, y, w, h
        self.setWindowTitle('Status Window')

        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self.make_tab1(), 'One')
        tabs.addTab(self.make_tab2(), 'Two')

        # QMainWindow 추가
        self.setCentralWidget(tabs)
        self.resize(1500, 950)

    # 첫번째 탭 생성함수
    def make_tab1(self):
        # 버튼 객체 만들기
        button1 = QPushButton('버튼1', self)
        button2 = QPushButton('버튼2', self)
        button3 = QPushButton('버튼3', self)

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(vbox)
        return tab

    def make_tab2(self):
        # 버튼 객체 만들기
        check1 = QCheckBox('체크버튼1', self)
        check2 = QCheckBox('체크버튼2', self)
        check3 = QCheckBox('체트버튼3', self)

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addWidget(check1)
        vbox.addWidget(check2)
        vbox.addWidget(check3)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(vbox)
        return tab


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
