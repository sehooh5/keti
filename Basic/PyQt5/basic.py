#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QRadioButton, QLabel, QLineEdit, QGridLayout, QFileDialog
from PyQt5.QtCore import Qt

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import os


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
        button1.clicked.connect(self.btnLogin_clicked)

        button2 = QPushButton('File', self)
        button2.clicked.connect(self.btnFile_clicked)

        button3 = QPushButton('Docker Image Build', self)
        button3.clicked.connect(self.btnBuild_clicked)

        button4 = QPushButton('Docker Image push', self)
        button4.clicked.connect(self.btnPush_clicked)

        button5 = QPushButton('Kubernetes Apply', self)
        button5.clicked.connect(self.btnApply_clicked)

        # 도커 이미지 이름
        lbl = QLabel('Docker Image Name : ', self)
        qle = QLineEdit(self)
        qle.textChanged[str].connect(self.onChanged)

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
        edge_lbl1 = QLabel('Worker Edge 1: ', self)
        edge_lbl2 = QLabel('Worker Edge 2: ', self)

        grid = QGridLayout()
        grid.addWidget(edge_lbl1, 0, 0)
        grid.addWidget(edge_lbl2, 2, 0)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(grid)
        hbox.addStretch(5)

        # 위젯에 레이아웃 추가하기
        tab = QWidget()
        tab.setLayout(hbox)
        return tab

    def onChanged(self, text):
        os.environ['docker_name'] = text

    # 도커 로그인 기능
    def btnLogin_clicked(self):
        os.system("echo Login button clicked!!")

    # 파일 오픈 기능
    def btnFile_clicked(self):
        os.system("echo File button clicked!!")
        fname = QFileDialog.getOpenFileName(self, 'Open File', '',
                                            'All File(*);; html File(*.html *.htm)')
        if fname[0]:
            os.environ['fpath'] = os.path.split(fname[0])[0]
            os.environ['fname'] = os.path.split(fname[0])[1]
            print(os.environ['fname'])
            print(os.environ['fpath'])
            f = open(fname[0], 'r', encoding='UTF8')
            with f:
                data = f.read()
                os.environ['data'] = data

    # 도커 이미지 빌드 기능

    def btnBuild_clicked(self):
        os.system("echo Build button clicked!!")

        file_name = os.environ['fname']
        docker_name = os.environ['docker_name']
        os.chdir(os.environ['fpath'])
        os.system(
            f"docker build -f {file_name} -t sehooh5/{docker_name}:latest")

    # 도커 이미지 푸시 기능
    def btnPush_clicked(self):
        os.system("echo Push button clicked!!")

        docker_name = os.environ['docker_name']
        os.chdir(os.environ['fpath'])
        os.system(
            f"docker push sehooh5/{docker_name}:latest")

    # deployment 배포 기능

    def btnApply_clicked(self):
        os.system("echo Apply button clicked!!")

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
