#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QRadioButton, QLabel, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(50, 50, 100, 100)  # x, y, w, h
        self.setWindowTitle('Basic Application')

        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self.make_tab1(), 'Function')
        tabs.addTab(self.make_tab2(), 'Monitoring')

        # QMainWindow 추가
        self.setCentralWidget(tabs)
        self.resize(1500, 950)

    # 첫번째 탭 생성함수
    def make_tab1(self):
        # 버튼 객체 만들기
        button1 = QPushButton('Login', self)
        button2 = QPushButton('File', self)
        button3 = QPushButton('Docker Image Build', self)
        button4 = QPushButton('Docker Image push', self)
        button5 = QPushButton('Kubernetes Apply', self)

        # 도커 이미지 이름
        lbl = QLabel('Docker Image Name : ', self)
        qle = QLineEdit()

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(button1)
        vbox.addStretch(1)
        vbox.addWidget(button2)
        vbox.addStretch(1)
        vbox.addWidget(lbl)
        vbox.addWidget(qle)
        vbox.addWidget(button3)
        vbox.addStretch(1)
        vbox.addWidget(button4)
        vbox.addStretch(1)
        vbox.addWidget(button5)
        vbox.addStretch(6)

        # test
        lbl2 = QLabel('Docker Image1: ', self)
        lbl3 = QLabel('Docker Image2: ', self)

        grid = QGridLayout()
        grid.addWidget(lbl2, 0, 0)
        grid.addWidget(lbl3, 2, 0)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(grid)
        hbox.addStretch(5)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(hbox)
        return tab

    # 모니터링 탭
    def make_tab2(self):
        # 위젯에 grafana 레이아웃 추가하기
        tab = QWebEngineView()
        tab.setUrl(
            QUrl("https://grafana.com/"))  # 추후에 필요한 그라파나 url 변경해주기
        return tab


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
