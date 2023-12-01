import vlc
import time

def event_callback(event, player):
    if event.type == vlc.EventType.MediaPlayerEndReached:
        print("재시작 합니다")
        player.set_media(instance.media_new(media_path))
        player.play()

# VLC 초기화
instance = vlc.Instance("--no-xlib")  # X11 출력을 비활성화합니다.
player = instance.media_player_new()

# RTP 출력 설정
rtp_output = "#rtp{mux=ts,dst=192.168.0.14,port=5008} --no-sout-all"

# MP4 파일 경로
media_path = "/home/edge-worker-01/blackbox_osan/blackbox_08.mp4"

# 미디어 생성
media = instance.media_new(media_path)

# 미디어 플레이어에 미디어 할당
player.set_media(media)

# RTP로 스트리밍 설정
player.play()  # 재생 시작

# RTP 출력 설정 적용
player.video_set_outputs([rtp_output])

# 이벤트 콜백 함수 등록
events = player.event_manager()
events.event_attach(vlc.EventType.MediaPlayerEndReached, lambda event: event_callback(event, player))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    player.stop()
