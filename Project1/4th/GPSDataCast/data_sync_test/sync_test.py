import vlc
import time

def event_callback(event, player):
    if event.type == vlc.EventType.MediaPlayerEndReached:
        print("재시작 합니다")
        player.set_media_list(instance.media_list_new([media]))  # 미디어 리스트 재설정
        player.play()


# 미디어 생성
media = instance.media_new(mp4_path)

# 미디어 리스트 플레이어에 미디어 할당
media_list = instance.media_list_new([media])
media_player.set_media_list(media_list)

# RTP로 스트리밍 설정
media_player.play()  # 재생 시작

# RTP 출력 설정 적용
media.get_mrl()  # 기존의 옵션을 삭제합니다.
media.add_option(rtp_output)  # 새로운 RTP 출력 설정을 추가합니다.

# 루프 및 기타 설정
# media_player.set_fullscreen(True)  # 전체 화면 모드로 설정 (선택적)
media_player.set_playback_mode(vlc.PlaybackMode.loop)  # 루프 설정

# 이벤트 콜백 함수 등록
events = media_player.event_manager()
events.event_attach(vlc.EventType.MediaPlayerEndReached, lambda event: event_callback(event, media_player))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    media_player.stop()