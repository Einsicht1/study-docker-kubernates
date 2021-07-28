## The why's and what's of kubernetes
- scale up 에 대해 생각해보자. 아래는 EB구조인데, worker만 sale up이 가능할까?
- <img width="500" alt="Screen Shot 2021-07-26 at 3 22 20 PM" src="https://user-images.githubusercontent.com/60768642/126942295-4ab42c71-ddda-4f17-b273-b61d7b19b2f4.png">
- 정답은 no다. 아래처럼 모든 컨테이너가 다 sale-up되버린다. control능력이 부족함. 
- <img width="500" alt="Screen Shot 2021-07-26 at 3 23 26 PM" src="https://user-images.githubusercontent.com/60768642/126942426-011566cf-d5e7-4fa1-afc3-f4be6eabce39.png">
- 우리가 원하는건 아래같은 상황이다.  
- <img width="500" alt="Screen Shot 2021-07-26 at 3 24 15 PM" src="https://user-images.githubusercontent.com/60768642/126942508-8d249387-05d7-4d94-b132-003e09033f90.png">
- 이걸 가능하게 해주는 게 쿠버니티스다. 아래는 쿠버네티스의 대략적 구조. 이를 통해 "worker 컨테이너 5개 추가해라"같은 명령이 가능해짐.
- <img width="500" alt="Screen Shot 2021-07-26 at 3 24 55 PM" src="https://user-images.githubusercontent.com/60768642/126942578-cba3e5a5-055c-40d6-b84e-19d93ad1475f.png">
## Kubernetes in development and production
- dev에선 minikube를 사용하면 된다.
- prod에선 EKS, GKE(google cloud kubernetes enging)등을 사용하면 된다.
- <img width="500" alt="Screen Shot 2021-07-27 at 11 40 28 AM" src="https://user-images.githubusercontent.com/60768642/127086536-bbca358e-89b4-4804-861a-0d5578d893e2.png">
- minikube는 로컬에서 kubernetes cluster를 만들고 run하기 위한 CLI다.(local only)
- kubectl은 생성된 cluster안에서 노드, 컨테이너를 동작하는 역할을 한다.(local, prod)
#### 세팅
- install kubectl(CLI for interacting with our master)
- install VM driver virtualbox(used to make a VM that will be your single node)
- install minikube(Runs a single node on that VM)
## Minikube setup on Macos
## Mapping existing knowledge
- ` kubectl cluster-info`
#### goal
- get the multi-client image running on our local Kubernetes cluster running as a container
##### kubernetes와 docker-compose 
- K8S에는 이미지 build과정이 없다. 
- K8S는 한 object당 하나의 config파일이 있다. docker-compose.yml하나로 다 처리되는 것과 다름.
  - objects는 꼭 컨테이너만을 위한건 아니다. 나중에 부연설명 함.
- docker-compose는 네트워크가 자동으로 생기는 반면, K8S는 메뉴얼로 작업해줘야 함.  
- <img width="500" alt="Screen Shot 2021-07-27 at 2 53 32 PM" src="https://user-images.githubusercontent.com/60768642/127102754-edef8934-bfda-4f9e-8951-e2bd65d1af4a.png">
- <img width="500" alt="Screen Shot 2021-07-27 at 2 53 01 PM" src="https://user-images.githubusercontent.com/60768642/127102700-d899737e-80af-41c1-baac-8b89313fb81b.png">
- <img width="500" alt="Screen Shot 2021-07-27 at 3 05 03 PM" src="https://user-images.githubusercontent.com/60768642/127103931-87fec107-83e1-4d7b-9c9b-4794a33692d1.png">
## Adding configuration files
- client-node-port.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: client-node-port
spec:
  type: NodePort
  ports:
    - port: 3050
      targetPort: 3000
      nodePort: 31515
  selector:
    component: web

```
-client-pod.yaml 
```
apiVersion: v1
kind: Pod
metadata:
  name: client-pod
  labels:
    component: web
spec:
  containers:
    - name: client
      image: stephengrider/multi-client
      ports:
        - containerPort: 3000

```
## Object types and API versions
- kind: type of object를 명시함. 위 예시에선 Service, Pod
- service는 setting up networking역할  
- objects serve different purposes
  - running a container
  - monitoring a container
  - setting up networking, etc
#### API version
- apiVersion을 명시하는 것은, scopes or limits the types of objects that we can specify that we want to create within a given configuration file.
- So inside of both of our configuration files, we specified an API version of the one that essentially opens up access to us to a predefined set of different object types. 
- 각각 버전마자 내용이 다르다.
- <img width="500" alt="Screen Shot 2021-07-27 at 3 30 47 PM" src="https://user-images.githubusercontent.com/60768642/127106602-30312acf-485e-4759-946c-65269364430c.png">

## Running containers in pods
- K8S에서는 컨테이너를 단독으로 띄울 수 없다. (컨테이너가 최소단위가 아님)
- 컨테이너는 반드시 pod안에 속해야 한다. 즉 컨테이너 하나를 띄울 때에도 pod을 띄어야 함.
## Service config files in depth
#### Ojbects types
- Pods: Runs one or more closely related containers
- Services: Sets up networking in a Kubernetes cluster
  - sub type of services
    - ClusterIP
    - NodePort: exposes a container to the outside world(only good for dev purposes)
    - LoadBalancer
    - Ingress

- client-pod.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: client-pod
  labels:
    component: web
spec:
  containers:
    - name: client
      image: stephengrider/multi-client
      ports:
        - containerPort: 3000
```  

- client-node-port.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: client-node-port
spec:
  type: NodePort
  ports:
    - port: 3050
      targetPort: 3000
      nodePort: 31515
  selector:
    component: web


```
- client-node-port는 포트 설정을 한다.
- client-pod은 pod 설정을 한다.
- client-node-port에 맨 아래 selector.conponent=web이부분이 바로 pod와 connect하는 부분이다.
- pod이나 objects중에 component:web이라는 곳으로 트래픽을 보내라는 뜻.
- 실제로 client-pod.yaml에 labels.component=web부분이 명시되어 있다. 일로 보내라는 뜻이다.
- 꼭 component라는 키를 가질 필요는 없다. 아무거나 쓰면 됨.
- <img width="500" alt="Screen Shot 2021-07-28 at 8 34 15 PM" src="https://user-images.githubusercontent.com/86581178/127316589-7f743518-f8c5-4bb2-af13-8c8053cb19d3.png">
#### port
- ports안에 있는 port, targetPort, nodePort 에대해 알아보자.
- port: cluster안에 있는 다른 pod에서 이 pod에 접근할 때 사용하는 port(현재는 pod이 하나기 때문에 무쓸모)
- targetPort: targeting하는 컨테이너의 포트
- nodeport: 실제 이 노드로 접근하기 위해 사용하는 포트. `localhost:31515` 이런식으로. 프로덕션에선 잘 안쓴다.(google.com:31515이런식으로 접근하는게 오바라서..)
<img width="500" alt="Screen Shot 2021-07-28 at 8 46 02 PM" src="https://user-images.githubusercontent.com/86581178/127317011-40c106a5-9a6c-480f-bcc4-b2f18c403958.png">

## connecting to running containers
- <img width="400" alt="Screen Shot 2021-07-28 at 8 49 07 PM" src="https://user-images.githubusercontent.com/86581178/127317377-4a3f3468-061a-4e09-ac54-505b00079d51.png">
- 
```
kubectl apply -f client-pod.yaml
pod/client-pod created

kubectl apply -f client-node-port.yaml
service/client-node-port created
```
- <img width="500" alt="Screen Shot 2021-07-28 at 8 51 52 PM" src="https://user-images.githubusercontent.com/86581178/127317687-adaf4b88-0462-474c-868c-b48601e2bd18.png">
``` 
kubectl get pods  

NAME         READY   STATUS    RESTARTS   AGE
client-pod   1/1     Running   0          87s
```

```
kubectl get services

client-node-port   NodePort    10.102.165.51   <none>        3050:31515/TCP   2m21s
kubernetes         ClusterIP   10.96.0.1       <none>        443/TCP          30h
```

- http://localhost:31515 로 접속가능
- 혹은 minikube를 사용한다면 `minikube ip` 로 얻은 ip:31515로 접근 가능.

## the entire deployment flow
- <img width="500" alt="Screen Shot 2021-07-28 at 9 08 23 PM" src="https://user-images.githubusercontent.com/86581178/127319660-346c2a9b-4aa7-496e-95a5-991011e6230f.png">
- master는 유지해야 하는 컨테이너 수(여기서는 4개)를 유지하는 역할을 한다.
- `docker kill container_id` 로 하나를 죽여도 즉시 새로운 컨테이너가 뜬다. matser가 모니터링 하고 컨테이너 수를 유지하는 역할을 해주기 때문.
## Imperative vs Declarative deployments
- Kubernetes is a system to deploy containerized apps
- Nodes are individual machines(or vm's) that run containers
- Masters are machines (or vm's) with a set of programs to manage nodes
- Kubernetes didn't build our images - it got them from somewhere else
- Kubernetes (the master) decided where to run each container - each node can run a dissimilar set of containers
- To deploy something, we update the desired state of the master with a config file(important)
- The master works constantly to meet your desired state(important)

#### Imperative vs Declarative
- Imperative Deployments: "Do exactly these steps to arrive at this container setup" <br> -> very descriptive
- Declarative Deployments: "Our conatiner setup should look like this, make it happen"
<img width="600" alt="Screen Shot 2021-07-28 at 9 33 24 PM" src="https://user-images.githubusercontent.com/86581178/127322776-87756aae-5ba6-43ba-b665-49a6c3a7d8df.png">

#### 결론
- 이 강의에선 declarative 방법을 사용할 것이다.
- 실제 prod세계에서도 declarative방법을 사용한다.
- 블로그 포스팅중엔 imperative 식으로 적어놓은 것도 있고 실제도 가능하지만, 우린 declarative로 간다.
<img width="500" alt="Screen Shot 2021-07-28 at 9 35 35 PM" src="https://user-images.githubusercontent.com/86581178/127323034-ee41bfde-f60c-48d6-acab-b69524130104.png">
