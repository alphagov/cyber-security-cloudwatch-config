output "kinesis_firehose_metric_alarm_id" {
        value = aws_cloudwatch_metric_alarm.kinesis_firehose_metric_alarm.id
}

output "kinesis_firehose_metric_alarm_arn" {
	value = aws_cloudwatch_metric_alarm.kinesis_firehose_metric_alarm.arn
}
