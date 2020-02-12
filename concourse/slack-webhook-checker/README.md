# Slack webhook checker  pipeline

This is not the pipeline for this service. 

It's a pipeline using this service to report on the health of 
the configured slack webhooks. 

It runs once per day, gets the slack hooks configured under 
/slack/channels in SSM and then iterates through checking it 
can successfully post to each of them (response status=200)

If any webhook fails the pipeline fails and reports to the 
health monitoring service. 

## Deploy

```fly
fly -t cd sp -p slack-webhook-checker -c slack-webhook-checker-pipeline.yml
```