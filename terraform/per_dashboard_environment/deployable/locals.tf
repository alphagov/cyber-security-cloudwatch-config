locals {
  zipfile           = "../../../lambda/health_package/health_package.zip"
  slack_sns_arn     = element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_slack_lambda"))
  pagerduty_sns_arn = element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_pagerduty_lambda"))
  dashboard_sns_arn = element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_dashboard_lambda"))
}