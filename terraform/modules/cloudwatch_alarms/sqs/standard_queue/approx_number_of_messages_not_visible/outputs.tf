output "approx_num_of_messages_not_visibile_arn" {
	description = "ARN for ApproximateNumberOfMessagesNotVisible Cloudwatch alarm"
	value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn
}
