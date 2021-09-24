# SNS for cloudwatch alarms
resource "aws_sns_topic" "use1_cloudwatch_alarm_sns_topic" {
  provider  = aws.us-east-1
  name      = local.cloudwatch_alarm_sns_topic
  tags      = merge(module.tags.tags, map("Name", "use1_cloudwatch_alarm_sns_topic_${data.aws_caller_identity.current.account_id}"))
}

output "use1_sns_arn" {
  value       = aws_sns_topic.use1_cloudwatch_alarm_sns_topic.arn
  description = "The ARNs for SNS topics"
}

locals {
  use1_sns_cloudwatch_forwarder_topic = aws_sns_topic.use1_cloudwatch_alarm_sns_topic.arn
}

# SNS for cloudwatch events
resource "aws_sns_topic" "use1_cloudwatch_event_sns_topic" {
  provider  = aws.us-east-1
  name      = local.cloudwatch_event_sns_topic
  tags      = merge(module.tags.tags, map("Name", "use1_cloudwatch_event_sns_topic_${data.aws_caller_identity.current.account_id}"))
}

output "use1_sns_event_arn" {
  value       = aws_sns_topic.use1_cloudwatch_event_sns_topic.arn
  description = "The ARNs for SNS topics"
}

locals {
  use1_sns_cloudwatch_event_forwarder_topic = aws_sns_topic.use1_cloudwatch_event_sns_topic.arn
}
