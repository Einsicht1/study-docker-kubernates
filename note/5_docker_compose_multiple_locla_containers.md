# Docker compose with multiple local containers
## App overview
- number of visits을 알려주는 서비스를 만든다.
- node app, redis 두개가 필요한데, 각각을 독립된 컨테이너로 만든다.
- 하나의 컨테이너 안에 둬도 되지만, 이럴 경우 유지보수가 어렵다.
<img width="500" alt="Screen Shot 2021-07-19 at 3 37 12 PM" src="https://user-images.githubusercontent.com/86581178/126114102-e45e8006-7ffc-4e89-bcc7-d936db6c8f60.png">

## App server starter code

## Assembling a Dockerfile
```
FROM node:alpine

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .

CMD ["npm", "start"]
```
## Introducing docker-compose
- 위에서 node app컨테이너와 redis 컨테이너가 서로 통신해야 하는데, 방법은 두가지다.
  - 하나. use docker CLI's network features
  - 둘. user docker-compose
- 대부분 docker-compose를 사용한다.  
#### docker compose
- separate CLI that gets installed along with docker
- used to start up multiple docker containers at the same time
- automates some of the long-winded arguments we were passing to 'docker run'
## docker-compose files
- <img width="500" alt="Screen Shot 2021-07-19 at 4 41 15 PM" src="https://user-images.githubusercontent.com/86581178/126121699-943eba1a-fe9e-4e22-b97d-0a7bfcca12c4.png">

- <img width="500" alt="Screen Shot 2021-07-19 at 4 41 32 PM" src="https://user-images.githubusercontent.com/86581178/126121730-c0dbbea9-d9b3-4ee8-a364-72daed0215b4.png">
#### docker-compose file 내용
```
  version: '3'
services:
  redis-server:
    image: 'redis'
  node-app:
    build: .
    ports:
      - "4001:8081"

```
- services라는 단어를 보면 container라고 이해하면 된다. (정확히 같은건 아니지만 얼추 비슷하다.)
- redis-server는 image를 지정해줬고, node-app은 그대신 `build: .`을 써줬다.
  - image는 리모트 이미지를 말한다.
  - `build: .`은 현재 디렉토리의 Dockerfile을 사용하라는 의미다.
- ports에 쓰인`-`를 보자. `-`yml파일에서 Array를 의미한다. 여러개의 포트매핑을 할 수 있기 때문에 `-`를 사용한다.  
  - 참고로 이 예시에서는 하나의 포트매핑만 사용했음.

## Networking with docker-compose
- 위 챕터의 docker-compose파일에는 컨테이너끼리의 네트워크 설정이 없다. 이제 해보자.
- index.js 아래처럼 수정.
```
const client = redis.createClient({
    host: 'redis-server',
    port: 6379
});
```

## docker-compose commands
#### `docker-compose up` ==`docker run <image>`
- docker-compose up엔 이미지를 명시해줄 필요가 없다.
- 명령어 쳐지는 순간 현재 디렉토리의 docker-compose파일에 있는 이미지를 모두 실행시킨다.
####  'docker-compose up --build' == `docker build .` + `docker run <image>`
- asdf asdf

#### 실습
- `docker-compose up `명령어를 쳐보자.
- `Creating network "5_section_default" with the default driver` 이 메세지를 볼 수 있다.
  - docker-compose실행하면 네트워크가 생기고, 그안에 컨테이너들이 포함된다.
- 아래처럼 컨테이너 두개가 생기는 것을 볼 수 있다.
```
Creating 5_section_node-app_1     ... done
Creating 5_section_redis-server_1 ... done

```
## Stopping docker-compose containers
#### Launch in background
- `docker-compose up -d`
#### Stop containers
- `docker-compose down`
## Container maintenance with compose
- node-app에서 에러가 나면 컨테이너를 종료하는 시나리오를 테스트해보자.
- 에러를 내기 어려우니, 정상적으로 request가 오면 에러코드 0을 내면서 프로세스가 종료되도록 해보자.
- 아래처럼 index.js를 수정.
- docker-compose up --build로 변경된 코드를 새롭게 빌드한 후 실행명령어를 치자.
```
const express = require('express');
const redis = require('redis');
const process = require('process');

const app = express();
const client = redis.createClient({
    host: 'redis-server',
    port: 6379
});
client.set('visits', 0);

app.get('/', (req, res) => {
    process.exit(0);
   client.get('visits', (err, visits) => {
       res.send('Number of visits is' + visits);
       client.set('visits', parseInt(visits) + 1)
   });
});

app.listen(8081, () => {
    console.log('Listening on port 8081');
});
```
- 크롬창에서 localhost:4001에 접속하면 에러가 나면서 터미널에서 아래 메세지를 볼 수 있다.
- `5_section_node-app_1 exited with code 0`
- `docker ps`로 확인해보면 redis만 떠있는 것을 볼 수 있다.
- 에러가 나면 컨테이너를 종료시키고 새로운 컨테이너를 자동으로 띄울 수 있을까? 다음 챕터에서 알아보자.
## Automatic container restarts
### status code
- 0: we exited and everything is OK
- 1,2,3, etc: We exited because something went wrong!
### restart policy
- <img width="500" alt="Screen Shot 2021-07-19 at 5 12 43 PM" src="https://user-images.githubusercontent.com/86581178/126126187-e0130f39-f261-4d36-b675-7cac590c30fc.png">
- 다른 3개는 quote없이 적지만, no는 ***"no"*** 이렇게 적어줘야 한다.!
- 우선 always정책으로 아래처럼 docker-compose 파일을 수정한다.
- localhost:4001에 접속하고 터미널을 보자.
- code 0과 함께 컨테이너가 내려간다. 그 후 즉시 컨테이너가 다시 생성된다.
``` 
version: '3'
services:
  redis-server:
    image: 'redis'
  node-app:
    restart: always
    build: .
    ports:
      - "4001:8081"

```
## Container status with docker-compose
- `docker-compose ps` 명령어는 현재 위치에서 docker-compose을 찾은뒤 해당하는 컨테이너들에 대한 정보를 보여준다.
- 따라서 docker-compose파일이 없는 곳에서 위 명령어를 치면 에러가 난다!