variable "eu-west-1__firehose__KinesisMillisBehindLatest" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

variable "eu-west-2__firehose__KinesisMillisBehindLatest" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

resource "aws_cloudwatch_metric_alarm" "euw1_cloudwatch_kinesis_millis_behind_latest" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-1__firehose__KinesisMillisBehindLatest)
  provider            = aws.eu-west-1
  alarm_name          = "${var.eu-west-1__firehose__KinesisMillisBehindLatest[count.index].ResourceName}_KinesisMillisBehindLatest_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-1__firehose__KinesisMillisBehindLatest[count.index].Threshold
  alarm_description   = "Tracks whether data is backing up in Kinesis"
  metric_name         = "KinesisMillisBehindLatest"
  namespace           = "AWS/Firehose"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    DeliveryStreamName = var.eu-west-1__firehose__KinesisMillisBehindLatest[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
}

resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_kinesis_millis_behind_latest" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2__firehose__KinesisMillisBehindLatest)
  provider            = aws.eu-west-2
  alarm_name          = "${var.eu-west-2__firehose__KinesisMillisBehindLatest[count.index].ResourceName}_KinesisMillisBehindLatest_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-2__firehose__KinesisMillisBehindLatest[count.index].Threshold
  alarm_description   = "Tracks whether data is backing up in Kinesis"
  metric_name         = "KinesisMillisBehindLatest"
  namespace           = "AWS/Firehose"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    DeliveryStreamName = var.eu-west-2__firehose__KinesisMillisBehindLatest[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
}
