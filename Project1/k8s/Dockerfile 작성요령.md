# Dockerfile 작성요령

- [참고 페이지](https://subicura.com/2017/02/10/docker-guide-for-beginners-create-image-and-deploy.html)

Dockerfile의 명령은 위에서 아래로 차례대로 실행한다.

·     FROM : 생성할 이미지의 베이스 이미지를 입력한다. 이미지가 로컬에 없다면 자동으로 도커허브에서 pull 한다.

·     LABEL : “키:값” 형태로 이미지에 메타데이터 추가. 추가된 메타 데이터는 docker inspect 명령어로 확인가능.

·     WORKDIR : 명령어를 실행할 디렉터리를 나타냄. Bash에서 cd 명령과 동일한 기능이다.

·     COPY : 로컬 디렉터리의 파일을 이미지에 복사하는 역할. ADD와 다른 점은 COPY는 로컬 디렉터리만 가능하고 ADD는 외부 URL및 tar 파일도 추가 가능하다.

·     RUN : 이미지를 만들기 위해 컨테이너 내부에서 명령어를 실행.

·     EXPOSE : Dockerfile의 빌드로 생성된 이미지에서 노출할 포트를 설정

·     CMD : 컨테이너가 시작될 때마다 실행할 명령어(커맨드)를 설정, Dockerfile에서 한번만 사용할 수 있다.

[출처](https://sungwookkang.com/1303)



---

## 도커 이미지 만들기

[자료](https://suwoni-codelab.com/docker/2018/06/11/Docker-Dockerfile/)



---

### 도커 이름없는 이미지 지우기

```
$ docker rmi -f $(docker images -f "dangling=true" -a)
```

