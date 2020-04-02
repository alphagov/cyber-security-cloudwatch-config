# Docker concourse-worker-health container 

This container installs a specified version of terraform and some 
helper script to enable assuming and IAM role. 

In order to make changes to the Docker image, simply push changes to the Dockerfile in this repository to master and the `cyber-security-concourse-base-image` concourse pipeline will be triggered, rebuilding the image and pushing it to DockerHub at `gdscyber/concourse-worker-health`.
