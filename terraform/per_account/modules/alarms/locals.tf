locals {
  zipfile     = "../../../lambda/health_package/health_package.zip"
  # If this is changed the PERIOD in
  # lambda/health_package/cloudwatch_metric_forwarder.py
  # should be updated to match the cron frequency
  metric_cron = "cron(0 * ? * * *)"
}