# Contents Service Management (CSM)

## Development environment

- python 3.6
- docker 19.03.8
- docker-compose 1.17.1
- influxdb 1.17.10

## nginx + flask + influxdb
- flask : flask + uwsgi
- nginx : uwsgi_pass (proxy pass)
- influxdb

## How to install
---
#### 1. install docker (for Linux) && docker-compose

1-1. docker 
```sh
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
```

after running the command, you can confirm which it works using the command below

```sh
$ docker --version
Docker version 19.03.8, build 1234567890
```

1-2. docker-compose

```sh
$ sudo curl -L https://github.com/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

after running the command, you can confirm which it works using the command below

```sh
$ docker-compose --version
docker-compose version 1.17.1, build 6d101fb
```


#### 2. clone this folder

   ```sh
$ git clone (git url)
   ```

#### 3. run the **docker-compose.yml** in this folder

   ```sh
$ cd uc4_csm
$ docker-compose up -d
   ```

   After running this command, you can see a list of three running containers on docker

   ```sh
$ docker ps
   
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
   f8f244427369        nginx:test          "nginx -g 'daemon of…"   18 seconds ago      Up 17 seconds       0.0.0.0:80->80/tcp       nginx
   7dd1b4ec51f7        flask:test          "/bin/sh -c 'uwsgi u…"   19 seconds ago      Up 18 seconds       0.0.0.0:5000->5000/tcp   flask
   
   ```

#### 4. run a random result generator named 'test.py' (only for test)

   open a new terminal

```sh
$ cd ./uc4_csm/flask/src
$ python test.py
```




#### 5. open the url 'http://localhost:25000'

   you can see the main page of SCM



 