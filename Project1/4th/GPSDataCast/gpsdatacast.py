import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QProcess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.process = None
        self.video_files = ['blackbox_01.avi', 'blackbox_02.avi', 'blackbox_03.avi',
                            'blackbox_04.avi', 'blackbox_05.avi', 'blackbox_06.avi', 'blackbox_07.avi']
        self.start_port = 5001
        self.current_index = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('VLC Command')

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.startVLC)
        self.start_button.setGeometry(30, 30, 70, 30)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stopVLC)
        self.stop_button.setGeometry(110, 30, 70, 30)
        self.stop_button.setEnabled(False)

        self.show()

    def startVLC(self):
        if not self.process:
            video_file = self.video_files[self.current_index]
            dst_port = self.start_port + self.current_index

            command = [
                'cvlc',
                '-vvv',
                f'/media/keti-laptop/T7/{video_file}',
                f'--sout',
                f'#rtp{{dst=123.214.186.162,port={dst_port},mux=ts}}',
                '--loop',
                '--no-sout-all'
            ]

            self.process = QProcess(self)
            self.process.start(command[0], command[1:])

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            self.current_index += 1
            if self.current_index >= len(self.video_files):
                self.current_index = 0

    def stopVLC(self):
        if self.process:
            self.process.terminate()
            self.process = None

            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())