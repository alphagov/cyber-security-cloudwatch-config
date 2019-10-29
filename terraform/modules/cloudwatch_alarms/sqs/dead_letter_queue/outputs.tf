output "approx_num_of_messages_visible_arn" {
	description = "ARN for ApproximateNumberOfMessagesVisible Cloudwatch alarm - dead-letter queue"
	value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn
}
