# Creating a production-grade
## Development workflow
- Develpoment -> Testing -> Deployment
## Flow specifics
- feature branch -> pr -> master -> Travis CI -> AWS Hosting
## Docker's purpose
## Proejct generation
- react app만들기!
## More on product generaion
- node 다운받기(google node download)
- `npx create-react-app frontend`
## Necessary commands
- `npm run start`: Starts up a development server. for development use only
- `npm run test`: Runs tests associated with the project
- `npm run build`: Builds a prod version of the application
## Creating the dev Dockerfile
- Dockerfile.dev를 아래처럼 만든다.
```
FROM node:alpine

WORKDIR '/app'

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "run", "start"]
```
- `docker build -f Dockerfile.dev . `로 빌드
## Duplicating dependencies
- node_modules폴더 때문에 빌드 시간이 엄청 걸린다.
- 이건 사실 필요없는 거라, 지운 다음에 다시 빌드해준다. (속도 엄청 빨라짐)

## Starting the container
- `docker run -it -p 3000:3000 IMAGE_ID`
- src/App.js에서 디폴트 값을 수정해보자.
## Docker volumes
- 소스코드 변경할 때마다 build할필요 없이 바로 반영되게 해보자.
- 도커는 빌드할 때 FS를 스냅샷을 떠서 컨테이너 안에 보관한다.
- volume은 스냅샷을 뜨지 않고 reference를 저장해서 거길 바라보게 한다.
- 예를 들어 로컬 폴더를 바라보게 하면 local이 변경될 떄마다 컨테이너 파일도 자동으로 변경된다.
- 명령어: `docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image id>`
  - `-v /app/node_moduels`: put a bookmark on the node_modules folder. "이 폴더는 매핑하지 말아라!"
  - `-v $(pwd):/app`: map the pwd into the '/app' folder. 로컬 현재경로 파일을 컨테이너 app폴더 안과 매핑해라.
- `-v /app/node_modules` 요부분은 무슨 역할을 하는지 잘 모르겠다. 그런데 저 부분만 빼놓고 run하면 에러가 난다. 
## Bookmarking volumes
- 위 강의에서 로컬 node_module을 지웠기 때문에 `-v $(pwd):/app`로 로컬과 컨테이너 매핑해도 node_module은 없고, 그래서 에러가 난다.
- 따라서 `-v /app/node_modules` 로 컨테이너 안의 node_modules를 만들어준다. 로컬과 mapping하는 것이 아니다. 로컬엔 저 폴더가 없음.
- 이제 `docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image id>` 명령어로 로컬 변경이 컨테이너상에서 바로 반영된다.
## Shorthand with Docker compose
- 매번 `docker run -p 3000:3000 -v /app/node_modules -v $(pwd):/app <image id>` 명령어를 치는건 부담된다.
- docker-compose로 실행을 간소화해보자. 비록 컨테이너가 하나지만 docker-compose를 사용할 수 있다. 
```
version: '3'
services: 
  web:
    stdin_open: true
    build: .
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
```
- `build .`명령어는 현재 경로의 Dockerfile을 참조한다. 하지만 현재 도커파일 이름이 Docker.dev기 때문에 에러가 난다.
- 해결법은 아래 챕터에서.
## Overrding Dockerfile selection
```
version: '3'
services: 
  web:
    stdin_open: true
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
```
- 이제 docker-compose up으로 실행.
## Do we need copy?
- 볼륨 mount를 사용하니, Dockerfile에 `COPY . .명령어는 더이상 없어도 되지 않을까?
- 없어도 작동은 한다.
- 하지만 놔두는걸 추천한다. 왜냐면, 나중에 docker-compose를 사용하지 않을수도 있고, <br>
위 파일을 prod에 올릴 수도 있기 때문.
## Executing tests
- `docker run <image id > npm run test`
- `docker run -it <image id> npm run test`
- 이 방법의 단점은 테스트가 변경될 때마다 매번 수동으로 명령어를 입력해야 한다는 것.
- 다음챕터에서 테스트가 바뀔떄 마다 자동으로 테스트가 실행되도록 해보자.
## Live updating tests
- `docker exec -it <container id> npm run test`
- 컨테이너를 띄어놓고 두번째 터미널에서 위 명령어를 실행하면 테스트가 변경될 때마다 자동으로 실행된다.
- 하지만 이것도 수동으로 명령어를 입력해야 하고, 컨테이너 아이디를 기억해야 해서 불편하다.
- 다음 챕터에서는 compose로 간단하게 하는 방법을 알아보자.
## Docker compose for running tests
- docker-compose파일을 사용해서 테스트가 변경될 때마다 자동으로 테스트가 실행되도록 해보자.
- 컨테이너를 두개 띄우는 방식이다. 하나는 기존 컨테이너, 하나는 테스트만을 위한 컨테이너.
- 테스트가 변경될 때마다 테스트 컨테이너에서 자동으로 테스트를 재실행한다.
- docker-compose up --build로 실행한다.
- 잘 작동한다. 한가지 단점은, 터미널 상에서 명령어를 입력할 수 없다는 것이다.
- ls, w, pwd 혹은 커맨드로 테스트를 재시작한다던지 하는 것을 할 수 없다.
- 다음 챕터에서는 이걸 가능하게 하는 방법을 알아보자.
``` 
version: '3'
services: 
  web:
    stdin_open: true
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app
  tests:
    stdin_open: true
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - /app/node_modules
      - .:/app
    command: ["npm", "run", "test"]
```
## Attaching to web container

## Shortcomings on testing
- ?? 다시 듣기. 결국 완벽한 해답이 없다고 하는듯?
## Need for Nginx
- production에서는 nginx가 컨테이너 안에 있는 index.html, main.js를 serving하는 역할을 해야함.
<img width="400" alt="Screen Shot 2021-07-20 at 4 58 57 PM" src="https://user-images.githubusercontent.com/60768642/126283922-f9c3c9db-7d81-44a4-b467-43b9b9a656b1.png">
## Multi-step docker builds
- <img width="400" alt="Screen Shot 2021-07-20 at 4 59 35 PM" src="https://user-images.githubusercontent.com/60768642/126284002-2ebd5662-aa09-4da9-b02a-8f0e1409f466.png">
#### two issues
- install dependency는 빌드를 위해서만 필요하다. 실제 prod컨테이너가 돌 때는 해당 파일들이 없어도 된다. 있으면 메모리 낭비.
- nginx를 어떻게 실행시키지?
  - nginx이미지를 사용해야 함. 즉 base image가 두개 필요
- 결과적으로 할 내용
- <img width="400" alt="Screen Shot 2021-07-20 at 5 07 05 PM" src="https://user-images.githubusercontent.com/60768642/126284953-e13a91c7-9cd4-4c67-add9-c160b7780c7e.png">


## Implementing Multi-step builds
1. 도커파일 생성. 
```
FROM node:alpine as builder
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build 
```
2. 이렇게 하면 build폴더가 생긴다. 즉, 나머지는 다 필요없고 /app/build폴더만 결과적으로 중요하다.

3. 위에서 만든 이미지 내의 app/build파일을 물려받는 nginx이미지를 추가한다.
```
FROM node:alpine as builder
WORKDIR '/app'
COPY package.json .
RUN npm install
COPY . .
RUN npm run build 

FROM nginx
COPY --from=builder /app/build usr/share/nginx/html
```

## Running Nginx
4. `docker build .` 으로 이미지 빌드
5. `docker run -p 8080:80 <image id>`으로 서버 실행
