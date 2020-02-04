variable "eu-west-1__kinesis__ExecuteProcessingSuccess" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

variable "eu-west-2__kinesis__ExecuteProcessingSuccess" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

resource "aws_cloudwatch_metric_alarm" "euw1_cloudwatch_kinesis_execute_processing_success" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-1__kinesis__ExecuteProcessingSuccess)
  provider            = aws.eu-west-1
  alarm_name          = "${var.eu-west-1__kinesis__ExecuteProcessingSuccess[count.index].ResourceName}_ExecuteProcessingSuccess_alarm"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-1__kinesis__ExecuteProcessingSuccess[count.index].Threshold
  alarm_description   = "Tracks the successful execution processes to allow us to correlate against failures."
  metric_name         = "ExecuteProcessing.Success"
  namespace           = "AWS/Kinesis"
  period              = 300
  statistic           = "Minimum"
  dimensions = {
    StreamName = var.eu-west-1__kinesis__ExecuteProcessingSuccess[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
}

resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_kinesis_execute_processing_success" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2__kinesis__ExecuteProcessingSuccess)
  provider            = aws.eu-west-2
  alarm_name          = "${var.eu-west-2__kinesis__ExecuteProcessingSuccess[count.index].ResourceName}_ExecuteProcessingSuccess_alarm"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-2__kinesis__ExecuteProcessingSuccess[count.index].Threshold
  alarm_description   = "Tracks the read position across all shards and consumers in the stream. If an iterator's age passes 50% of the retention period (by default, 24 hours, configurable up to 7 days), there is risk for data loss due to record expiration."
  metric_name         = "ExecuteProcessing.Success"
  namespace           = "AWS/Kinesis"
  period              = 300
  statistic           = "Minimum"
  dimensions = {
    StreamName = var.eu-west-2__kinesis__ExecuteProcessingSuccess[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
}
