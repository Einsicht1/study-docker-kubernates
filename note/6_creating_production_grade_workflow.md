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
## Bookmarking volumes
## Shorthand with Docker compose
## Overrding Dockerfile selection
## Do we need copy?
## Executing tests
## Live updating tests
## Docker compose for running tests
## Attaching to web container
## Shortcomings on testing
## Need for Nginx
## Multi-step docker builds
## Implementing Multi-step builds
## Running Nginx