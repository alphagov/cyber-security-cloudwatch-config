locals {
  slack_sns_arn     = try(
    element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_slack_lambda")),
    "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:none"
  )
  pagerduty_sns_arn = try(
    element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_pagerduty_lambda")),
    "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:none"
  )
  dashboard_sns_arn = try(
    element(aws_sns_topic.euw2_sns_topics.*.arn, index(var.sns_topic_names, "notify_dashboard_lambda")),
    "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:none"
  )
}
