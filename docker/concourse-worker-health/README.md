# Docker concourse-worker-health container 

This container installs a specified version of terraform and some 
helper script to enable assuming and IAM role. 

NOTE: Replace version with the bumped version number
```
docker build --no-cache -t gdscyber/concourse-worker-health -t gdscyber/concourse-worker-health:1.0 .
``` 

Then to push to DockerHub:

```
docker push gdscyber/concourse-worker-health:1.0
docker push gdscyber/concourse-worker-health:latest 
```