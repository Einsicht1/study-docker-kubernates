# Dive into Docker

## why Use docker?
> Docker makes it really easy to install and run software without worrying about setup or dependencies
- redis를 설치한다고 치자. 운영체제마다 설치 방법도 다르고, 설치하다가 에러나면 검색해야 되고, 그러다 안되면 또 검색하고....
- 심지어 로컬에서 설치해서 잘 됐는데, cloud에 배포하려하면 에러가 날수도 있다.
- 도커는 이런 문제를 해결하기 위해 태어났다. 
- 도커로 뭔가를 쉽게, 어느 운영체제에서나 설치가 가능하다.
## What is Docker?
<img width="600" alt="Screen Shot 2021-07-13 at 10 09 40 PM" src="https://user-images.githubusercontent.com/86581178/125457341-fcbdb961-2c08-4939-8c82-d9fd27814e7f.png">
<img width="600" alt="Screen Shot 2021-07-13 at 10 10 41 PM" src="https://user-images.githubusercontent.com/86581178/125457426-ca847cd7-8095-44d8-badd-e7cbcd8f72ad.png">
<img width="600" alt="Screen Shot 2021-07-13 at 10 11 59 PM" src="https://user-images.githubusercontent.com/86581178/125457620-d49b2614-face-4366-81ba-d9fa55092377.png">

## Using the Docker Client
#### `docker run hello-world` 를 치면 일어나는 일
1.  docker cli가 명령어를 받아 docker server로 넘긴다. (실제 복잡한 일들은 docker server에서 일어난다.)
2. docker server가 local의 image cache에 image가 있는지 확인한다.
3. 없다면 docker hub에 가서 이미지를 다운받고, local의 image cache에 저장한다.
4. docker server가 해당 이미지 파일을 메모리에 올려 컨테이너를 만들고 프로그램을 실행시킨다.

- `docker run hello-world`를 처음 실행하면 아래와 같이 이미지를 찾을 수 없어 다운받는다는 멘트가 나온다.
- 두번째 부턴 아래 메세지를 볼 수 없다. 로컬에 이미 있기 때문이다.
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete 
Digest: sha256:df5f5184104426b65967e016ff2ac0bfcd44ad7899ca3bbcf8e44e4461491a9e
Status: Downloaded newer image for hello-world:latest
```
## What's a container
- container 개념을 이해하기 위해선 OS가 컴퓨터에서 어떻게 돌아가는지 알아야 한다.
- 커널은 프로세스와 하드웨어 사이에서 중개하는 역할을 한다.
<img width="600" alt="Screen Shot 2021-07-13 at 10 26 10 PM" src="https://user-images.githubusercontent.com/86581178/125459806-4bbdfde2-a444-4a5c-bf60-42973f756908.png">
#### 상황 가정
- 만약 크롬은 python 2, NodeJS는 python3가 있어야만 작동한다고 해보자.
- hard disk에는 하나의 파이썬 버전만이 설치될 수 있는 상황이다.
- 현재 하드에 파이썬 2가 설치돼있다면, 크롬은 실행가능하고, NodeJS는 실패한다.
- 이를 해결할 수 있는 방법 중 하나가 Namespacing이다.
- Hard disk에 공간을 나눠 각 파이썬 버전을 위한 공간을 놓는다.
- Control Groups로도 비슷한 역학을 할 수 있다.
- 여하간 둘 다 프로세스를 격리시키고, 프로세스에게 독립된 리소스를 할당하는 방법이다.
<img width="600" alt="Screen Shot 2021-07-13 at 10 28 51 PM" src="https://user-images.githubusercontent.com/86581178/125460249-130c1f2a-5adc-40fd-a9d1-5e7dc80e1a74.png">
<img width="600" alt="Screen Shot 2021-07-13 at 10 30 40 PM" src="https://user-images.githubusercontent.com/86581178/125460534-fd6092b9-d703-48aa-94ce-24a775c691a3.png">

#### container
- container는 격리된 프로세스로 독립된 리소스를 할당받는다.
<img width="600" alt="Screen Shot 2021-07-13 at 10 33 07 PM" src="https://user-images.githubusercontent.com/86581178/125460912-a9adfbe4-718f-46d9-a2f4-41bf492395b8.png">
<img width="600" alt="Screen Shot 2021-07-13 at 10 34 09 PM" src="https://user-images.githubusercontent.com/86581178/125461057-1c09c53e-6e25-48f0-afb9-e136586c26ae.png">
  
- Image는 file system에 있는 snapshot이고, container를 실행하면 그 안에 존재한다.

## How's Docker running on Your Computer
- 위에서 말한 namespacing과 control groups는 linux에만 존재한다. (not windows, not macOS)
- 도커를 로컬에 깔 때 Linux Virtual Machine이 깔린다.
- 그 안에 Linux Kernel이 있고 이 커널이 컨테이너(프로세스)들을 컨트롤한다.
- `docker version`을 치면 OS/Arch: linux/amd64로 나온다. linux VM이 깔렸다는 뜻이다.
<img width="600" alt="Screen Shot 2021-07-13 at 10 39 52 PM" src="https://user-images.githubusercontent.com/86581178/125461985-1c90fae7-2ada-4ee5-9ab7-f6c239b5d39d.png">
