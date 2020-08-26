# OpenCV

## 참고

- [참고1](https://m.blog.naver.com/samsjang/220498694383)
- 



## Basic

- 실시간 비전을 목적으로 한 프로그래밍 라이브러리
- 실시간 이미지 프로세싱에 중점을 둔 라이브러리
- 조금이라도 영상처리가 들어간다면 필수적으로 사용하게 되는 라이브러리



## 설치방법

### 1. 설치된 OpenCV 제거

- 버전 확인

```bash
$ pkg-config --modversion opencv
```



- 여기서 버전 확인되면 설치되어있는것, 아니면 다음 단계로 넘어가도 된다
- 다음 명령으로 OpenCV 라이브러리 설정 파일을 포함해서 기존에 설치된 OpenCV 패키지를 삭제하고 진행한다

```bash
$ sudo apt-get purge libopencv* python-opencv
$ sudo apt-get autoremove
```



