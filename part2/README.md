# DevOps with Docker part 2

## Exercise 2.1

**output:**

docker-compose.yml:
```yaml
version: 3.8"

services:
  simple-web-service:
    image: devopsdockeruh/simple-web-service
    volumes:
      - ./text.log:/usr/src/app/text.log
```
