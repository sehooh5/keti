# MongoDB

- MongoDB 설치 및 실행





## 개발 환경

- Ubuntu 20.04 LTS 





## 설치

- Ubuntu 환경에서 MongoDB 설치 및 실행



### MongoDB 설치



#### gnupg 및 curl 설치 여부 확인 및 설치

```
# 설치 안되어있으면

sudo apt-get install gnupg curl
```



#### 공개 키 가져오기

```
# 20240820

curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```



#### MongoDB용 목록 파일 생성

```
# Ubuntu 20.04(Focal)용 /etc/apt/sources.list.d/mongodb-org-7.0.list 파일 생성

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```



#### 로컬 패키지 데이터베이스 불러오기

```
sudo apt-get update
```



#### MongoDB 패키지 설치

```
# 최신 스테이블 버전 설치

sudo apt-get install -y mongodb-org
```



---

### MongoDB 실행



#### MongoDB 시작

```
sudo systemctl start mongod
```



#### MongoDB 실행 확인

```
sudo systemctl status mongod

```



#### MongoDB 중지

```
sudo systemctl stop mongod
```



#### MongoDB 재시작

```
sudo systemctl restart mongod
```



####  MongoDB 사용을 시작합니다.

```
mongosh
```



---

### MongoDB 패키지 삭제



#### MongoDB 중지

```
sudo service mongod stop
```



#### 패키지 제거

```
sudo apt-get purge "mongodb-org*"
```



#### 데이터 디렉토리 제거

```
# MongoDB database 및 로그 파일을 제거
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
```