locals {
  cloudwatch_alarm_sns_topic = "cloudwatch_forwarder"
}
resource "aws_sns_topic" "euw1_cloudwatch_alarm_sns_topic" {
  #checkov:skip=CKV_AWS_26:Ensure all data stored in the SNS topic is encrypted
  provider  = aws.eu-west-1
  name      = local.cloudwatch_alarm_sns_topic
}

output "euw1_sns_arn" {
  value       = aws_sns_topic.euw1_cloudwatch_alarm_sns_topic.arn
  description = "The ARNs for SNS topic"
}

resource "aws_sns_topic" "euw2_cloudwatch_alarm_sns_topic" {
  #checkov:skip=CKV_AWS_26:Ensure all data stored in the SNS topic is encrypted
  provider  = aws.eu-west-2
  name      = local.cloudwatch_alarm_sns_topic
}

output "euw2_sns_arn" {
  value       = aws_sns_topic.euw2_cloudwatch_alarm_sns_topic.arn
  description = "The ARNs for SNS topics"
}

locals {
  euw1_sns_cloudwatch_forwarder_topic = aws_sns_topic.euw1_cloudwatch_alarm_sns_topic.arn
  euw2_sns_cloudwatch_forwarder_topic = aws_sns_topic.euw2_cloudwatch_alarm_sns_topic.arn
}
