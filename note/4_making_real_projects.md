# Making real proejcts with docker
## Project outline
## Node server setup
## A few planned error
## Base image issues
## A few missing files
## Copying build files
- `docker build -t kpl5672/simpleweb .`
- `docker run kpl5672/simpleweb`
## Container port mapping
- `docker run -p 8080: 8080 <image id>`
- 앞의 8080: Route incoming requests to this port on local host to
- 뒤의 8080: this port inside the container
## Specifying a working dir
- 컨테이너 진입: `docker run -it kpl5672/simpleweb sh`
- workdir 설정 없이 ls명령어를 치면 아래와 같다.
- 상황이 좋지 않다. `COPY ./ ./`명령어로 옮겨놓은 파일이 아래 파일명과 겹친다면?
- 그래서 항상 WORKDIR을 지정해준다.
- `WORKDIR /usr/app`
  - any following command will be executed relative to this path in the containe
- 참고로 usr, var, home 어디로 할지는 이견이 많지만, 강사는 usr에 한단다.

![Screen Shot 2021-07-17 at 6 57 32 PM](https://user-images.githubusercontent.com/60768642/126033302-489bfbe7-399d-41fc-a6d1-c27de0a2b403.png)
  

## Unnecessary rebuilds
- index.js파일에서 간단하게 소스코드 한 줄만 변경해도 다시 build하는 과정에서 COPY ./ ./이후과정은 전부 재실행된다.
- 실제 num install은 긴 시간이 걸리기에, 이것은 대단한 낭비다.
- 이를 어떻게 방지할 수 있을까? -> see next chapter
```
# Specify a base image
FROM node:alpine

WORKDIR /usr/app
# Install some dependencies
COPY ./ ./
RUN npm install

# Default command
CMD ["npm", "start"]

```
## Minimizing cache busting and rebuilds
- 도커파일을 아래처럼 수정한다.
- 먼저 npm install은 package.json과만 연관이 있으므로, 먼저 package.json을 copy하고 install 한뒤, 다른 파일을 COPY한다.

```
# Specify a base image
FROM node:alpine

WORKDIR /usr/app
# Install some dependencies
COPY ./package.json ./
RUN npm install
COPY ./ ./

# Default command
CMD ["npm", "start"]
```