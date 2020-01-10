# Concourse Heartbeat pipeline

This is not the pipeline for this service. 

It's a pipeline using this service to report on the health of 
concourse. It was developed as a test of a standard way of 
reporting health events from other concourse pipelines. 

It runs once a day to check that our concourse workers are up 
and correctly responding to non-zero exit statuses. 

It's also there as an example of how to add the health monitoring 
resources to other pipelines. 

## Deploy 

```fly
fly -t cd sp -p heartbeat \
    -c concourse-heartbeat-pipeline.yml
```