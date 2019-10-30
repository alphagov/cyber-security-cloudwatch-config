output "kinesis_data_stream_metric_alarm_id" {
        value = aws_cloudwatch_metric_alarm.kinesis_data_stream_metric_alarm.id
}

output "kinesis_data_stream_metric_alarm_arn" {
	value = aws_cloudwatch_metric_alarm.kinesis_data_stream_metric_alarm.arn
}
