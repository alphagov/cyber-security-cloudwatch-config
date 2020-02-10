# Cyber Cloudwatch Pipeline

For access requirements go to Prerequisites.

If you want to build a Docker image, follow the Docker section.

For information about how the Concourse jobs are set up, go to Concourse

If you want to write or amend a Concourse pipeline, follow the Implementing Concourse pipeline section.

For information about the IAM role and policies that have been implemented go to IAM role.

## Prerequisites

Access to DockerHub - Ask the engineering team for access.

Access to Concourse - Alphagov GitHub single sign-on.

Read general info on deploying into PaaS using Concourse.

## Docker

The container to run the pipeline is built from a [Dockerfile](../../docker/Dockerfile)

```
cd ..
docker build -f docker/Dockerfile --no-cache -t gdscyber/concourse-worker-health -t gdscyber/concourse-worker-health:[VERSION] .

docker push gdscyber/concourse-worker-health:[VERSION]
docker push gdscyber/concourse-worker-health:latest
```

## Concourse

https://cd.gds-reliability.engineering/teams/cybersecurity-tools/pipelines/cyber-security-cloudwatch-health

### Updating the pipeline 

Once you've made changes to the yaml file you login to concourse and set your target, in this case "cd":

```
fly login --target cd -c https://cd.gds-reliability.engineering -n cybersecurity-tools    
fly -t cd sp -c pipeline.yml -p cyber-security-cloudwatch-health
```