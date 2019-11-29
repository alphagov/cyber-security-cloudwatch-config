variable "sns_topic_names" {
  description = "SNS topic names"
  type        = list(string)
  default     = ["notify_slack_lambda", "notify_pagerduty_lambda", "notify_dashboard_lambda"]
}

resource "aws_sns_topic" "euw1_sns_topics" {
  count     = length(var.sns_topic_names)
  provider  = aws.eu-west-1
  name      = var.sns_topic_names[count.index]
}

output "euw1_sns_arns" {
  value       = aws_sns_topic.euw1_sns_topics[*].arn
  description = "The ARNs for SNS topics"
}

output "euw1_sns_arn_map" {
  value       = zipmap(aws_sns_topic.euw1_sns_topics[*].name, aws_sns_topic.euw1_sns_topics[*].arn)
  description = "A lookup for SNS topic ARNs"
}

resource "aws_sns_topic" "euw2_sns_topics" {
  count     = length(var.sns_topic_names)
  provider  = aws.eu-west-2
  name      = var.sns_topic_names[count.index]
}

output "euw2_sns_arns" {
  value       = aws_sns_topic.euw2_sns_topics[*].arn
  description = "The ARNs for SNS topics"
}

output "euw2_sns_arn_map" {
  value       = zipmap(aws_sns_topic.euw2_sns_topics[*].name, aws_sns_topic.euw2_sns_topics[*].arn)
  description = "A lookup for SNS topic ARNs"
}

locals {
  euw1_sns_health_topic = lookup(element(aws_sns_topic.euw1_sns_topics, index(var.sns_topic_names, "health_monitoring_lambda")), "arn")
  euw2_sns_health_topic = lookup(element(aws_sns_topic.euw2_sns_topics, index(var.sns_topic_names, "health_monitoring_lambda")), "arn")
}