# Building Custom images through docker server
## Creating docker images
- Dockerfile
  - configuration to define how our container should behave
<img width="600" alt="Screen Shot 2021-07-14 at 3 14 22 PM" src="https://user-images.githubusercontent.com/86581178/125572251-b3bd954d-1c32-492d-87cb-47d53f37a00d.png">
<img width="600" alt="Screen Shot 2021-07-14 at 3 14 35 PM" src="https://user-images.githubusercontent.com/86581178/125572275-883be1f2-89cd-4a47-83ec-af400f3bc408.png">
## Building a dockerfile
- let's create and image tha runs redis-server
- 아래 내용을 담은 Dockerfile을 만들고, `docker build .`으로 이미지를 생성한 뒤, `docker run <image>`로 실행하면 redis가 실행된다.
```
# Use an existing docker image as a base
FROM alpine

# Download and install a dependency
RUN apk add --update redis

# Tell the image what to do when it starts as a container
CMD ["redis-server"]
```
## Dockerfile teardown
- FROM, RUN, CMD등은 instruction telling docker server what to do
- alpine, apk add --update redis, ["redis-server] 등은 argument to the instruction

## What's base image?
- Writing a dockerfile is like being given a computer with no OS and being told to install Chrome
- OS없이 텅텅빈 컴퓨터에 크롬을 깔아야 한다면?
  - 먼저는 운영체제를 깔것이다.
  - 그다음 디폴트 브라우저를 실행해서, 구글링 크롬을 한 뒤 다운받고 실행한다.
  - 이 과정이 dockerfile과 비슷하다. 아래 그림을 참고하자.
<img width="400" alt="Screen Shot 2021-07-14 at 3 41 35 PM" src="https://user-images.githubusercontent.com/86581178/125575386-623a83cf-cd4e-4172-982a-a3c04c871c7d.png">
- 왜 base image로 alpine을 사용하냐는 질문은 왜 windows, MacOS, Ubuntu를 사용하냐는 질문과 비슷하다.
  - we use it because they come with a preinstalled set of programs that are useful to us!
## The build process in detail
```
FROM alpine

RUN apk add --update redis

CMD ["redis-server"]
```
- FROM 
  - remote에서 alpine이미지를 받는다.
- RUN
  - 위에서 받은 alpine이미지를 기반으로 임시 컨테이너를 만들고 그 안에서 RUN 명령어를 수행한다.
  - 여기까지 완료한 상태를 이미지로 만들고, 위의 임시 컨테이너를 삭제한다.
- CMD
  - RUN에서 만들어진 이미지로 임시 컨테이너를 만든뒤 CMD명령어를 추가한다.
  - 여기까지 완료한 상태를 이미지로 만들고, 위의 임시 컨테이너를 삭제한다.
  - 완료
- 최종상태


<img width="480" alt="Screen Shot 2021-07-14 at 4 22 13 PM" src="https://user-images.githubusercontent.com/86581178/125580350-9b5bdea6-c6ff-4b80-bce4-a5a9ea757374.png">
  
#### 정리
- 각 단계마다 image가 생성된다. 최종적으로는 마지막 이미지만 남는다.
- FROM alpine
  - download alpine image
- RUN apk add -update redis
  - get image from previous step
  - create a container out of it
  - Run 'apk add --update redis' in it
  - Shut down that temporary container
  - get image ready for next instruction
- CMD ["redis-server"]
  - get image from last step
  - create a container out of it
  - tell container it should frun 'redis'server' when started
  - shut down that temporary container
  - get image ready for next instruction
- No more step
  - output is the image generated from previous step
## Rebuilds with cache
- `RUN apk add --update gcc`를 위 dockerfile RUN apk add --update redis 명령어 아래에 추가하고 빌드한다.
```
FROM alpine
RUN apk add --update redis
RUN apk add --update gcc
CMD ["redis-server"]
```

<img width="500" alt="Screen Shot 2021-07-14 at 5 12 11 PM" src="https://user-images.githubusercontent.com/86581178/125587432-bb9f1c93-c142-4847-b315-f28cd60a75b2.png">

- docker는 cache를 사용한다.
- step 2까지는 이미 빌드가 됐었기 때문에 cache가 사용되고, step3부터 새로 시작된다.

- 반면, 새 명령어를 FROM 바로 직전에 놓으면 어떻게 될까?
```
FROM alpine
RUN apk add --update gcc
RUN apk add --update redis
CMD ["redis-server"]
```
- 이때는 step 1까지만 캐시가 적용되고 step2부터 새로 시작된다.
#### 결론
도커파일 명령어 순서에 따라 빌드 시간이 크게 좌우된다.
## Tagging an image
- 도커 이미지 이름이 랜덤생성되는 것을 막기 위해서 -t(tag)옵션을 주자.
- `docker build -t docker_id/repo_or_proejct_name:version .`
- 예시: `docker build -t stephengrider/shoppingmall:latest .`
- 버전 명시 안하면 알아서 latest버전이 붙는다.
## Manual image generation with docker commit