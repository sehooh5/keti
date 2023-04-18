import subprocess
import psutill
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class VideoStream(QWidget):
    def __init__(self):
        super().__init__()

        # GUI 초기화
        self.setWindowTitle("Video Stream")
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_stream)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_stream)
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # VLC 명령어 및 프로세스 초기화
        self.vlc_cmd = "cvlc -vvv rtsp://192.168.1.101:554/h264 --sout=\"#rtp{dst=123.214.186.162,port=5005,mux=ts}\" --no-sout-all --sout-keep"
        self.vlc_process = None

    def start_stream(self):
        # VLC 프로세스 시작
        if self.vlc_process is None:
            self.vlc_process = subprocess.Popen(self.vlc_cmd, shell=True)

    def stop_stream(self):
        # VLC 프로세스 종료
        if self.vlc_process is not None:
            for child in psutil.Process(self.vlc_process.pid).children(recursive=True):
                child.kill()
            self.vlc_process.kill()
            self.vlc_process = None

if __name__ == '__main__':
    app = QApplication([])
    window = VideoStream()
    window.show()
    app.exec_()