# cyber-security-cloudwatch-config
Analyse list-metrics to create an automated set of cloudwatch alarms as a tfvars implementing a set of modules defined in cyber-security-shared-terraform-modules

## Run 

```
make run
```
You need to wrap this in appropriate aws credentials. 

Generates output/[account]/alarms.tfvars 

Creates a list of metrics per region/service/metric according to the 
naming convention: 

`[region]__[service]__[metric]`

For example:
 
`eu-west-1__sqs__ApproximateAgeOfOldestMessage`

## Test 

It may be this doesn't end up in lambda at all. 

We probably want to run a cron'd concourse task that generates the 
TF config and then runs the apply all in one step. 
(plus triggered on merge to master)
```
cd lambda/generate_metric_alarms
make test 
```
Runs pylint, flake8 and pytest 

## Terraform 

```
cd terraform/deployable 
terraform init -reconfigure -backend-config=../deployments/[account]/backend.tfvars
# change script to generate alarms into tf/deployments folder
terraform apply -var-file=../../lambda/generate_metric_alarms/output/[account]/alarms.tfvars 
```
