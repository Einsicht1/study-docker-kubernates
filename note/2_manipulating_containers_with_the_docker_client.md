# Manipulating Containers with the Docker Client
## Docker run detail
- creating and running a container from an image
- `docker run <image name>`을 치면 무슨일이 일어나는지 알아보자.
    - docker: Reference the docker client
    - run: try to create and run a container
    - image name: Name of image to use for this container
    
- 이미지는 FS에 있는 snapshot이다. run 명령어가 들어오면 이 스냅샷을 컨테이너 안에서 실행시킨다.

## Overriding Default commands
- `docker run <image name> command` 의 형태로 디폴트 command를 오버라이드 할 수 있다.
    - command: override default command
  
- 예시: `docker run busybox echo hi there` -> hi there이 출력된다.
- 예시: `docker run busybox ls` -> 파일 리스트가 출력된다.
- 근데 echo, ls명령어를 hello-world이미지에 치면 에러가 나는데, 이유는 hello-world파일안에는 해당 명령어를 실행할 수 있는 파일들이 없기 때문이다.(거의 빈 파일임)
<img width="1305" alt="Screen Shot 2021-07-14 at 9 42 41 AM" src="https://user-images.githubusercontent.com/86581178/125543050-ec13d971-7ebc-42f1-96b6-436bfb633566.png">
  
## Listing Running containers
- `docker ps` : listing all running containers
- `docker ps -a` or `docker ps --all`: running + 종료된 컨테이너 listing
## Container Lifecycle
- `docker run` command는 docker create + docker start명령어 두개를 내포한다. create과 start는 별개의 동작이다.
    - create: create a container. `docker create <image name>`
    - start: start a container. `docker start <container id>`
        - start할때 startup command가 작동한다.
  
#### 실습
1. `docker create hello-world` 명령어를 친다. container id가 반환된다. (8fe5910e78e37f30ad8ba9e0127d19b64e884a317d98b3d3edfeb692345ee15a )
2. `docker start -a 8fe5910e78e37f30ad8ba9e0127d19b64e884a317d98b3d3edfeb692345ee15a`: 실행
    - -a 옵션은 container실행시 output을 터미널에 print시키는 명령어.
## Restarting stopped containers
- start명령어로 Exited(stop)된 컨테이너를 재실행할 수 있다.
- `docker start f08bf6e809fb`
## Removing stopped containers
#### `docker system prune`
  - remove all stopped containers
  - remove all networks not used by at least one container
  - remove all dangling images
  - remove all dangling build cache

## Retrieving log outputs
- `docker logs <container id>`: get logs from a container
## Stopping containers
#### docker stop \<container id\>
- container에 terminate signal을 보낸다.
- nice하게, but takes time
- 명령을 받은 container는 종료를 위해 몇가지 작업을 진행한 뒤 종료된다.
- 특별한 경우가 아니라면 kill말고 stop을 권한다.(강사가)
<img width="600" alt="Screen Shot 2021-07-14 at 11 18 13 AM" src="https://user-images.githubusercontent.com/86581178/125550273-d6cc1466-a343-4c2d-be9a-780de0251c9a.png">

#### docker kill \<container id\>
- container에 kill signal을 보낸다.
- 명령을 받은 container는 종료 작업을 못하고 즉시로 종료된다.
<img width="600" alt="Screen Shot 2021-07-14 at 11 18 44 AM" src="https://user-images.githubusercontent.com/86581178/125550318-74d4f2c3-670c-4ddc-b6da-64931f189cd2.png">

## Multi-command containers
- 도커로 실행한 redis에 redis-cli로 접근하려고 한다.
- 로컬에서 redis-cli를 쳐선 안된다. container안에서 redis-cli를 쳐야한다.
- 즉 한 컨테이너 안에서 redis서버를 키는 명령어와, redis-cli명령어 두개를 쳐야하는 상황. 어떻게 해야할까?
## Executing commands in running containers
#### execute an additional command in a container
- `docker exec -it <container id> <command>`
    - `-it`: allow us to provide input to the container
    
#### 실습
- redis컨테이너가 이미 돌고있는 상황이라 가정(container id: 1262e6b001ac)
- `docker exec -it 1262e6b001ac redis-cli`로 해당 컨테이너안으로 들어가 redis-cli명령을 실행한다.
## The purpose of the "it" flag
- 리눅스 환경 안에서 생성된 process는 3개의 커뮤니케이션 채널 STDIN, STDOUT, STDERR를 갖는다.
    - STDIN: stuff you type
    - STDOUT: stuff that shows up on screen
    
- `-it`는 -i와 -t로 이뤄져있다.
    - `-i`는 STDIN과 연결시켜준다. "지금 내가 -i뒤에 치는 명령어를 STDIN으로 보내라!"
    - `-t`는 명령어를 좀 더 예쁘고 가지런하게 정렬해주는 기능이라고 한다.(사실 그거보다 많은 일이 일어나긴 하는데 일단 이렇게 알면 된다고 한다.)
  
- `-t`명령어 없어도 작동하긴 하는데 어색하다.
  
## Getting a command prompt in a container
- `docker exec -it <container id> sh`
- debugging에 좋다.
- sh는 command processors다. (bash, powershell, zsh, sh 등등)
## Starting with a shell
- `docker run -it <image> sh`
- 컨테이너를 만들면서 동시에 안으로 진입하는 명령어. 
- container를 먼저 실행해 놓고 그 후에 진입하는 것이 더 일반적이다. 
## Container isolation
- 컨테이너는 독립된 FS를 갖는다. 