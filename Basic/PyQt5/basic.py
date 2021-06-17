#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QRadioButton, QLabel, QLineEdit, QGridLayout, QFileDialog, QDialog
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

        # QDialog 설정(로그인)
        self.dialog = QDialog()

        # QMainWindow 추가
        self.setCentralWidget(tabs)
        self.resize(1500, 950)

    # 첫번째 탭 생성함수
    def make_tab1(self):
        # 버튼 객체 만들기
        button1 = QPushButton('Login', self)
        button1.clicked.connect(self.btnLogin_clicked)
        button1_2 = QPushButton('Logout', self)
        button1_2.clicked.connect(self.btnLogout_clicked)

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

        # 파일이름 및 경로 보여주기
        self.path_lbl = QLabel("파일 정보", self)

        # 레이아웃 만들기
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(button1)
        vbox.addWidget(button1_2)
        vbox.addStretch(1)
        vbox.addWidget(button2)
        vbox.addWidget(self.path_lbl)
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

        # 라벨 및 타이핑
        id_lbl = QLabel("ID", self.dialog)
        pwd_lbl = QLabel("Password", self.dialog)
        id_qle = QLineEdit(self.dialog)
        pwd_qle = QLineEdit(self.dialog)
        pwd_qle.setEchoMode(QLineEdit.Password)  # 패스워드 숨김 설정
        id_qle.textChanged[str].connect(self.id_onChanged)
        pwd_qle.textChanged[str].connect(self.pw_onChanged)

        # 위치 설정
        id_lbl.move(60, 25)
        id_qle.move(60, 40)
        pwd_lbl.move(60, 70)
        pwd_qle.move(60, 85)

        # 로그인 버튼 추가
        btnDialog = QPushButton("login", self.dialog)
        btnDialog.move(100, 120)
        btnDialog.clicked.connect(self.dialog_login)

        # QDialog 세팅
        self.dialog.setWindowTitle('Docker Login')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()

    # id 입력
    def id_onChanged(self, text):
        os.environ['id'] = text

    # pw 입력
    def pw_onChanged(self, text):
        os.environ['pwd'] = text

    # Dialog 로그인 닫기 이벤트
    def dialog_login(self):
        docker_id = os.environ['id']
        docker_pwd = os.environ['pwd']
        os.system(f"docker login -u {docker_id} -p {docker_pwd}")
        self.dialog.close()

    def btnLogout_clicked(self):
        os.system("echo Logout button clicked!!")
        os.system("docker logout")

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
                self.path_lbl.setText(fname[0])

    # 도커 이미지 빌드 기능
    def btnBuild_clicked(self):
        os.system("echo Build button clicked!!")

        file_name = os.environ['fname']
        docker_name = os.environ['docker_name']
        os.chdir(os.environ['fpath'])
        print(f"docker build -f {file_name} -t sehooh5/{docker_name}:latest .")
        os.system(
            f"docker build -f {file_name} -t sehooh5/{docker_name}:latest .")

    # 도커 이미지 푸시 기능
    def btnPush_clicked(self):
        os.system("echo Push button clicked!!")

        docker_name = os.environ['docker_name']
        os.system(
            f"docker push sehooh5/{docker_name}:latest")

    # deployment 배포 기능
    def btnApply_clicked(self):
        os.system("echo Apply button clicked!!")

        file_name = os.environ['fname']
        os.chdir(os.environ['fpath'])
        os.system(
            f"kubectl apply -f {file_name}")

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
