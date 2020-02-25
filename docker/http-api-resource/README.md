# Docker http-api-resource container 

We use `aequitas/http-api-resource` to POST notifications to our 
health monitoring. The problem is that that container is listed here: 
https://vulnerablecontainers.org/

The vulnerabilities are largely because of the container kernel version
so we've made a multi-stage Dockerfile that installs the `aequitas`
base image and then replaces the kernel.

```
docker build --no-cache -t gdscyber/http-api-resource -t gdscyber/http-api-resource:1.0 .
``` 

Then to push to DockerHub:

```
docker push gdscyber/http-api-resource:1.0
docker push gdscyber/http-api-resource:latest 
```