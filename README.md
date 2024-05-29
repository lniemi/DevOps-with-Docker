# DevOps with Docker

## Exercise 1.1: Getting started

**output**

![Exercise 1.1](exercises/1.1.png)

## Exercise 1.2: Hello, Docker Hub

**output**

![Exercise 1.2](exercises/1.2.png)

## Exercise 1.3: Secret message

**output**

![Exercise 1.3](exercises/1.3.png)

## Exercise 1.4: Missing dependencies

**output**  
smart solution:
![Exercise 1.4](exercises/1.4.png)

```markdown
docker run -it -e WEBSITE=helsinki.fi ubuntu /bin/bash -c 'apt-get update && apt-get install curl -y && echo "Searching.." && sleep 1 && curl http://$WEBSITE'
```

output:  
![Exercise 1.4](<exercises/1.4(2).png>)
