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

## Exercise 2.5

**output**

command:
```bash
docker-compose up --scale compute=3
```
## Exercise 2.6

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
      - POSTGRES_HOST=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "8080:8080"
    depends_on:
      - redis
      - postgres
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
    restart: unless-stopped

  postgres:
    image: postgres:latest
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    restart: unless-stopped
    container_name: postgres
```

## Exercise 2.7

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
      - POSTGRES_HOST=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "8080:8080"
    depends_on:
      - redis
      - postgres
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
    restart: unless-stopped

  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      - ./hostDB:/var/lib/postgresql/data
    restart: unless-stopped
    container_name: postgres

volumes:
  hostDB:
    name: hostDB

```
## Exercise 2.8

**output**

docker-compose.yml:
```yaml
version: "3.8"

services:

  backend:
    build:
      context: ./example-backend
      dockerfile: Dockerfile
    environment:
      REDIS_HOST: redis
      POSTGRES_HOST: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis
    container_name: example-backend

  frontend:
    container_name: example-frontend
    build:
      context: ./example-frontend
      dockerfile: Dockerfile
    depends_on:
      - backend
    ports:
      - "5000:5000"

  redis:
    container_name: redis
    image: redis
    restart: always
    ports:
      - "6379:6379"

  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_HOST: postgres
    volumes:
      - ./hostDB:/var/lib/postgresql/data
    restart: unless-stopped
    container_name: postgres

  nginx:
    container_name: nginx
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend

volumes:
  hostDB:
    name: hostDB
```

## Exercise 2.9

**output** 

docker-compose.yml:
```yaml
version: "3.8"

services:

  backend:
    build:
      context: ./example-backend
      dockerfile: Dockerfile
    environment:
      REDIS_HOST: redis
      POSTGRES_HOST: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
      REQUEST_ORIGIN: http://localhost
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis
    container_name: example-backend

  redis:
    container_name: redis
    image: redis
    restart: always
    ports:
      - "6379:6379"
    environment:
      - ALLOW_EMPTY_PASSWORD=yes
    command: redis-server --loglevel warning

  frontend:
    container_name: example-frontend
    environment:
      - REACT_APP_BACKEND_URL=http://backend/api
    build:
      context: ./example-frontend
      dockerfile: Dockerfile
    depends_on:
      - backend
    ports:
      - "5000:5000"

  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_HOST: postgres
    volumes:
      - ./hostDB:/var/lib/postgresql/data
    restart: unless-stopped
    container_name: postgres
    hostname: postgres
    ports:
      - "5432:5432"

  nginx:
    container_name: reverse_proxy_nginx
    tty: true
    stdin_open: true
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /var/run/docker.sock:/tmp/docker.sock:ro
    depends_on:
      - frontend

volumes:
  hostDB:
    name: hostDB
  nginx.conf:
```

nginx.conf:
```conf
events { worker_connections 1024; }

http {
  server {
    listen 80;

    location / {
      proxy_set_header Host $host;
      proxy_pass http://frontend:5000/;
    }

    location /api/ {
      proxy_set_header Host $host;
      proxy_pass http://backend:8080/;
    }
  }
}
```

This one took lot longer than I thought. However I did not need to make changes to dockerfiles. They are same as before and can be found in the backend and frontend directories. Biggest aha moment happenened when I changed REQUEST_ORIGIN: http://localhost:80 to REQUEST_ORIGIN: http://localhost. This was the only change I needed to make everything work.

## Exercise 2.10

skipped this one

## Exercise 2.11

I decided to dockerize an app that I have been developing. Look [here](./2.11) for more details.