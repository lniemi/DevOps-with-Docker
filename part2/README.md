# DevOps with Docker part 2

## Exercise 2.1

**output**

docker-compose.yml:
```yaml
version: 3.8"

services:
  simple-web-service:
    image: devopsdockeruh/simple-web-service
    volumes:
      - ./text.log:/usr/src/app/text.log
```

## Exercise 2.2

**output**

docker-compose.yml:
```yaml
version: '3.8'

services:
  simple-web-service:
    image: devopsdockeruh/simple-web-service
    container_name: web-service
    ports:
      - 8080:8080
    command: docker run -d simple-web-service server
```

## Exercise 2.3

**output**

docker-compose.yml:
```yaml
version: '3.8'

services:

  backend:
    image: devopsdockeruh/example-backend
    build:
      context: ./example-backend
      dockerfile: Dockerfile
    container_name: back
    ports:
      - 8080:8080

  frontend:
    image: example-frontend
    build:
      context: ./example-frontend
      dockerfile: Dockerfile
    container_name: front
    ports:
      - 5000:5000
```
This worked when copied the repos 1.13 and 1.14 to the same directory as the docker-compose.yml file.

## Exercise 2.4

**output**

docker-compose.yml:
```yaml
version: '3.8'

services:
  backend:
    image: example-backend
    build:
      context: ./example-backend
      dockerfile: Dockerfile
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "8080:8080"
    depends_on:
      - redis
    container_name: back

  frontend:
    image: example-frontend
    build:
      context: ./example-frontend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - backend
    container_name: front

  redis:
    image: redis
    container_name: redis
```