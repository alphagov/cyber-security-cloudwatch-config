# Cyber Security CloudWatch Config

The aim of this repository is to automate the generation of CloudWatch
alarm config.

This repository uses `cloudwatch list-metrics` to identify resources to be monitored, queries the tags for those resources in order to classify them into services and environments.

The aim is to produce a set of `tfvar` files containing lists of maps
containing the config for the standard modules.

We specify a list of metrics we are interested in [metric-settings.json](lambda/health_package/metric-settings.json).

When we find a metric in an account that matches our settings an
appropriate alarm threshold is generated based on recent data and
that defines a var file which is passed to the terraform to create
the alarms.

The pipeline runs once per day to redefine new alarms and thresholds.

If new resources have been added in a monitored account which match
one of our metric definitions, health monitoring is automatically
set up.

By tagging the resources with a `Service` we can group component
resources into a definition of the health status for a whole service.

For any metric which has a configured alarm, the metric forwarder collects the
data for that metric on a cron schedule and forwards it so that we have both
the alarm state change and the metric data in splunk to help debug. 

## How to

### Add a CloudWatch metric alarm

To add a metric you just need to create the config for how to calculate the
health threshold in [metric-settings.json](lambda/health_package/metric-settings.json)

The config for a metric looks like this:
```
{
  "Namespace": "AWS/SQS",
  "MetricName": "ApproximateNumberOfMessagesVisible",
  "Statistic": "Maximum",
  "ComparisonOperator": "GreaterThanOrEqualToThreshold",
  "EvaluationPeriods": 2,
  "Period": 300,
  "Multiplier": 1.1,
  "Minimum": 500,
  "Maximum": 5000,
  "Description" : "This is an initial guess to be tuned later"
},
```

You can get a list of available metrics from `aws cloudwatch list-metrics` or
from the AWS docs or the cloudwatch console.

You need to set the `Statistic` and `ComparisonOperator` so in most cases it will
be the max is too high or the min is too low but it could be average or whatever.

Then you need to set the `Multiplier`. If you're interested in the maximum value
then `generate_metric_alarms.py` will get the max value for that metric in the
previous 2 weeks and then use the multiplier to add some headroom. So in this case
we're adding 10% on top of whatever the max value is.

You can optionally hard code minimum and maximum thresholds so in this case we
don't care if the queue has up to 500 messages and we always care if it goes above

If the `Minimum|Maximum` is set and the calculated threshold falls outside that
the appropriate min/max value will be used. If not the calculated value will be
used.

In the case of lambda duration the 90% of the lambda timeout is used as the
Maximum so it reports as unhealthy before it hits the limit.

This does mean that the the health threshold can creep up over time but only to
the limit and if it goes higher than the calculated headroom between resets it
will still report as unhealthy.


### Add a monitored AWS account

To add a new account you need to do 3 things:

#### 1. create a new terraform deployment

The alarms deployments are not suffixed (just named with the account id)

You can copy an existing deployment and just change the `backend.tf` state file
path and the `LOG_LEVEL` and `DEF_ENVIRONMENT` in `variables.tf`

#### 2. allow forwarding to the health monitors

Add the account ID to the list of monitored accounts in the 2 `_health_monitor`
terraform's `variables.tf`

```
variable "monitored_accounts" {
  description = "Account to accept forwarded data from"
  type        = list(string)
  default     = [
    ..
    <your account here>
  ]
}
```

You could choose to only add it to the prod or non-prod health monitor. It doesn't
have to be in both but if a resource in an account is tagged with `prod` it will
always try to forward to the prod health monitor the `DEF_ENVIRONMENT` is just
the default environment to forward to if a resource is untagged.

#### 3. add the account to the CodePipeline config

In the `_pipeline` terraform deployment there is a `variables.tf` indicating
which accounts to monitor:

```
variable "non_prod_accounts" {
  type        = list(string)
  default     = [
    ..
    <your account here>
  ]
}

variable "prod_accounts" {
  type        = list(string)
  default     = [
    ..
    <or here>
  ]
}
```

In this case you only need add your account in one list.

### Add a monitored AWS region

In terraform the provider doesn't support interpolation so you have to create
terraform resources to deploy things into each region you want to monitor.

To add a new region you have to do 2 things:

#### 1 create a provider alias

```
provider "aws" {
  # eu-west-1 provider
  region = "eu-west-1"
  alias  = "eu-west-1"
}
```

#### 2 create a set of resources for the region

I've grouped the per-region resouces together prefixed with a short version of
the region name. You can copy these files and then change the resource names
and providers to point to the new provider alias.

SNS can't notify cross-region so if you create alarms in a new region,
you have to create the forwarder lambdas and SNS topics to the deal with the
notifications from those alarms.

```
euw2_cloudwatch_alarms.tf
euw2_lambda_cloudwatch_alarm_forwarder.tf
euw2_lambda_cloudwatch_event_rule_forwarder.tf
euw2_lambda_cloudwatch_metric_forwarder.tf
euw2_sns.tf
```

## Lambda / python

### Generate Metric Alarms
This has been written as a lambda but potentially it could be run locally
by the concourse pipeline.

[README.md](lambda/health_package/README.md)

### Health Monitor
This lambda subscribes to an SNS health topic and routes the alarm to
appropriate notification SNS topics.

[README.md](lambda/health_package/README.md)

## Terraform

There are a number of deployments in `terraform/deployments`

### [account_id]

These deployments define the cloudwatch alarms and the cloudwatch
forwarder lambdas. Alarms, metrics and events are all forwarded
cross-account to either the prod or non-prod health monitors via
an SQS queue.

The alarm config is generated by `generate_metric_alarms.py` as above.

The terraform needs to be applied with the `alarms.tfvars` var file.
The file should be generated into the terraform deployments folder.

```
terraform apply --var-file=alarms.tfvars
```

Without the alarms file all cloudwatch alarms will be destroyed.

### [account_id]_health_monitor

The health monitor defines the lambdas that deal with the health event
data - forward it to slack and splunk and the queues and sns topics.

### [account_id]_pipeline

There is also a deployment for the codepipeline deployment

## Docker

There are 2 Dockerfiles:
1. terraform-container - [README.md](docker/concourse-worker-health/README.md)
    Installs a specified version of terraform and contains scripts
    to perform an STS:AssumeRole operation to assume the role for
    a given pipeline.

2. http-api-container - [README.md](docker/http-api-resource/README.md)
    Replaces the standard `aequitas/http-api-resource` container
    kernel with a more recent version to patch vulnerabilities.
