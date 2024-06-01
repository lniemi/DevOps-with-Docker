# DevOps with Docker

## Exercise 1.1: Getting started

**output**

![Exercise 1.1](1.1-1.6//1.1.png)

## Exercise 1.2: Hello, Docker Hub

**output**

![Exercise 1.2](1.1-1.6//1.2.png)

## Exercise 1.3: Secret message

**output**

![Exercise 1.3](1.1-1.6//1.3.png)

## Exercise 1.4: Missing dependencies

**output**  
smart solution:
![Exercise 1.4](1.1-1.6//1.4.png)

```markdown
docker run -it -e WEBSITE=helsinki.fi ubuntu /bin/bash -c 'apt-get update && apt-get install curl -y && echo "Searching.." && sleep 1 && curl http://$WEBSITE'
```

output:  
![Exercise 1.4](<1.1-1.6//1.4(2).png>)

## Exercise 1.5: Sizes of images

**output**  
download images:

```markdown
docker pull devopsdockeruh/simple-web-service:ubuntu
docker pull devopsdockeruh/simple-web-service:alpine
```

compare sizes:

```markdown
docker image ls
```

output:
![Exercise 1.5](1.1-1.6//1.5.png)
¨
running the alpine image and finding the secret message:

```markdown
docker run -d --name alpine-test devopsdockeruh/simple-web-service:alpine  
docker exec —it alpine—test sh  
tail -f ./text.log
```

output:
![Exercise 1.5](<1.1-1.6//1.5(2).png>)

## Exercise 1.6: Hello Docker Hub

**output**

![Exercise 1.6](1.1-1.6//1.6.png)

## Exercise 1.7: Image for script

**output**

Dockerfile:

```markdown
FROM ubuntu:22.04

# Install curl
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Add the script file to the container
COPY script.sh /script.sh

# Give execution rights on the script
RUN chmod +x /script.sh

# Command to run on container start
CMD ["/script.sh"]
```

## Exercise 1.8: Two line Dockerfile

**output**

Dockerfile:

```markdown
FROM devopsdockeruh/simple-web-service:alpine

# Set default argument to the ENTRYPOINT
CMD ["server"]
```
command running the container:

```markdown
docker run web-server
```

## Exercise 1.9: Volumes

**output**

Command:

```markdown
touch text.log  && docker run -v "$(pwd)/text.log:/usr/src/app/text.log" devopsdockeruh/simple-web-service
```

## Exercise 1.10: Ports open

**output**

Command:

```markdown
docker run -p 127.0.0.1:8080:8080 devopsdockeruh/simple-web-service
```

## Exercise 1.11: Spring

**output**

Dockerfile:

```markdown
# Use Amazon Corretto for Java support
FROM amazoncorretto:21.0.3-al2023-headless

# Install Maven
RUN yum install -y maven

# Create app directory in container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Build the application using Maven
RUN mvn clean install

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target/my-spring-app-0.0.1-SNAPSHOT.jar"]
```

## Exercise 1.12: Hello, frontend!

**output**

Dockerfile:

```markdown
FROM node:16-alpine

EXPOSE 5000

WORKDIR /usr/src/app

COPY . .

RUN npm install

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "-l", "5000", "build"]
```

## Exercise 1.13: Hello, backend!

**output**

Dockerfile:

```markdown
FROM golang:1.16-alpine

EXPOSE 8080

WORKDIR /usr/src/app

COPY . .

RUN go build

CMD ["./server"]
```

## Exercise 1.14: Environment

**output**

Dockerfile (fronetend):

```markdownFROM node:16-alpine

EXPOSE 5000

WORKDIR /usr/src/app

COPY . .

ENV REACT_APP_BACKEND_URL=http://localhost:8080

RUN npm install

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "-l", "5000", "build"]
```

Dockerfile (backend):

```markdown
FROM ubuntu:latest

COPY . .

RUN apt-get update && apt-get install -y wget gcc && rm -rf /usr/local/go && wget -c https://golang.org/dl/go1.16.3.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz

ENV PATH /usr/local/go/bin:$PATH

ENV REQUEST_ORIGIN http://localhost:5000

RUN go build

RUN go test

CMD ./server

EXPOSE 8080
```

Shell:
```markdown
docker build . -t example-backend
docker run -d -p 8080:8080 example-backend

docker build . -t example-frontend
docker run -d -p 5000:5000 example-frontend
```

## Exercise 1.15: Homework

**output**

### Two Plus Two Equals Five

This simple Python application demonstrates a simple fact that is well known to the Party in George Orwell's novel 1984: two plus two equals five.

#### Dockerhub link

https://hub.docker.com/r/lniemi/dystopiamath

#### Running the Docker Container

To run this application, execute the following command:

```bash
docker run lniemi/dystopiamath
```
it will print 2 + 2 = 5

## Exercise 1.16: Cloud deployment

Skipped this exercise because it is allowed to skip one exercise. Also I am running out of free cloud environments with different cloud providers :D