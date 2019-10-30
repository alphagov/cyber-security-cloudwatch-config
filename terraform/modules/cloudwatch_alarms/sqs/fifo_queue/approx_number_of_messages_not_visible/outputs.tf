output "approx_num_of_messages_not_visible_fifo_arn" {
	description = "ARN for ApproximateNumberOfMessagesNotVisible Cloudwatch alarm (FIFO queue)"
	value = "aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn"
}
