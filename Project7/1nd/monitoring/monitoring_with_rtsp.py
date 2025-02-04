import sys
import json
import cv2
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CCTVStreamApp(QWidget):
    def __init__(self, rtsp_url="rtsp://admin:wonwoo0!23@192.168.0.34:554/stream0", api_url="http://192.168.0.14:6432/usage"):
        super().__init__()

        self.setWindowTitle("CCTV Streaming with Metadata")
        self.setGeometry(100, 100, 800, 600)

        # UI 요소 설정
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        self.metadata_text = QTextEdit(self)
        self.metadata_text.setReadOnly(True)
        self.metadata_text.setPlainText("데이터 없음")  # 기본값 설정

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.metadata_text)
        self.setLayout(layout)

        # OpenCV 스트림 설정
        self.capture = cv2.VideoCapture(rtsp_url)

        # 타이머 설정 (30ms마다 프레임 업데이트)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # API 요청을 위한 타이머 (1초마다 메타데이터 요청)
        self.api_url = api_url
        self.timer_metadata = QTimer()
        self.timer_metadata.timeout.connect(self.update_metadata)
        self.timer_metadata.start(1000)  # 1초마다 갱신

    def update_frame(self):
        """CCTV 영상 프레임을 PyQt에 표시"""
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

    def update_metadata(self):
        """HTTP API에서 JSON 데이터를 가져와 UI에 표시, 데이터 없을 때 '데이터 없음' 처리"""
        try:
            response = requests.get(self.api_url, timeout=2)  # 2초 타임아웃 설정
            if response.status_code == 200:
                data = response.json()
                if data:
                    metadata = (
                        f"CPU: {data.get('cpu')}%\n"
                        f"Memory: {data.get('memory')}%\n"
                        f"User: {data.get('username')}\n"
                        f"Status: {data.get('message')}"
                    )
                else:
                    metadata = "데이터 없음"
            else:
                metadata = "데이터 없음"
        except Exception:
            metadata = "데이터 없음"

        self.metadata_text.setPlainText(metadata)

    def closeEvent(self, event):
        """앱 종료 시 리소스 해제"""
        self.capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCTVStreamApp("rtsp://your_cctv_stream_url", "http://192.168.0.14:6432/usage")
    window.show()
    sys.exit(app.exec())