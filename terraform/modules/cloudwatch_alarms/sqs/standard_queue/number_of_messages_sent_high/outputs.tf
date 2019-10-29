output "number_of_messages_sent_high_arn" {
	description = "ARN for NumberOfMessagesSent (high) Cloudwatch alarm"
	value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn
}
