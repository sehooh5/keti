#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow, \
    QApplication, QPushButton, QMessageBox, QLabel, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 420, 320)  # x, y, w, h
        self.setWindowTitle('QFileDialog Example Window')

        # QButton 위젯 생성 - FileDialog 을 띄위기 위한 버튼
        self.button = QPushButton('QFileDialog Open', self)
        self.button.clicked.connect(self.filedialog_open)
        self.button.setGeometry(10, 10, 200, 50)

        # QLabel 설정
        self.pathLabel = QLabel(self)
        self.pathLabel.setGeometry(10, 60, 400, 50)

        # QTextEdit 파일 읽은 내용 표시
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 110, 400, 200)

    def filedialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '',
                                            'All File(*);; html File(*.html *.htm)')
        if fname[0]:
            # 튜플 데이터에서 첫 번째 인자 값이 주소이다.
            self.pathLabel.setText(fname[0])
            print('filepath : ', fname[0])
            print('filesort : ', fname[1])

            # 텍스트 파일 내용 읽기
            f = open(fname[0], 'r', encoding='UTF8')  # Path 정보로 파일을 읽는다.
            with f:
                data = f.read()
                self.textEdit.setText(data)
        else:
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
