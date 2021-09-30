# SNS for cloudwatch alarms
resource "aws_sns_topic" "euw1_cloudwatch_alarm_sns_topic" {
  provider  = aws.eu-west-1
  name      = local.cloudwatch_alarm_sns_topic
  tags      = merge(module.tags.tags, map("Name", "euw1_cloudwatch_alarm_sns_topic_${data.aws_caller_identity.current.account_id}"))
}

output "euw1_sns_arn" {
  value       = aws_sns_topic.euw1_cloudwatch_alarm_sns_topic.arn
  description = "The ARNs for SNS topic"
}

locals {
  euw1_sns_cloudwatch_forwarder_topic = aws_sns_topic.euw1_cloudwatch_alarm_sns_topic.arn
}

# SNS for cloudwatch events

resource "aws_sns_topic" "euw1_cloudwatch_event_sns_topic" {
  provider  = aws.eu-west-1
  name      = local.cloudwatch_event_sns_topic
  tags      = merge(module.tags.tags, map("Name", "euw1_cloudwatch_event_sns_topic_${data.aws_caller_identity.current.account_id}"))
}

output "euw1_sns_event_arn" {
  value       = aws_sns_topic.euw1_cloudwatch_event_sns_topic.arn
  description = "The ARNs for SNS topic"
}

locals {
  euw1_sns_cloudwatch_event_forwarder_topic = aws_sns_topic.euw1_cloudwatch_event_sns_topic.arn
}
