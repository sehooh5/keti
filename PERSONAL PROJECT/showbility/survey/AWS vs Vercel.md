# AWS vs Vercel

- 호스팅 플랫폼 AWS 와 Vercel 차이점



|              | AWS                             | Vercel                      |
| ------------ | ------------------------------- | --------------------------- |
| 특징         | 백엔드, 프론트엔드 모두 운용    | 프론트엔드 중심 배포 플랫폼 |
| 백엔드       | 다양한옵션                      | 제한적(서버리스 함수 중심)  |
| 데이터베이스 | 다양한 관리형 서비스            | 제한적                      |
| 복잡성       | 높음(다양한 서비스, 설정)       | 낮음(간단한 설정)           |
| 확장성       | 높음                            | AWS보다 제한적              |
| 사용 사례    | 모든 규모의 복잡한 애플리케이션 | 정적 사이트, 애플리케이션   |



### Shobility 적용시

#### 장점

- 초기 비용 절감 가능(트래픽 기반)
- 배포, 운영/관리가 직관적이며 더 용이함



#### 단점

- 백엔드 전환기간 소요
  - Django -> Flask or FastAPI 로 전환이 필요
  - DB 또한 MySQL 지원하지 않고 전환한다면 MongoDB Atlas 로 변경예정
- 정적 사이트에 적합
  - 보통 Uber, Twitch 등 회사에서 프론트엔드 배포에 적용하고 백엔드는 AWS에서 관리하는 경우가 많음
  - 지속적인 연결이 필요한 작업에는 적합하지 않음
- 확장성
  - 대규모 트래픽이나 복잡한 로직 처리에 단점(Showbility는 아직 해당되지 않는듯)



#### 프로젝트 적용에 관한 개인적 의견

- 백엔드 전환기간이 소요되더라도 개인적으로 익숙한 Flask로 전체 프레임워크를 변경해도 좋을 것 같다고 생각합니다. 그리고 배포, 운영/관리 측면에서도 Vercel이 강점은 있다고 생각하구요.
- 다만, 걱정되는 부분은 서비스가 성장함에 따라 백엔드나 DB를 분리하여 사용해야하지 않을까 라는 생각이 듭니다.
- AWS 비용 절감에 있어서 참고할만한 것이 하나 더 있는데 AWS Lightsail 이라고 있던데 한번 같이 의견 나누면 좋을 것 같습니다.(https://library.gabia.com/contents/aws-contents/13171/)