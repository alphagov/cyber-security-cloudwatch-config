output "number_of_messages_sent_low_arn" {
	description = "ARN for NumberOfMessagesSent (low) Cloudwatch alarm"
	value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn
}
