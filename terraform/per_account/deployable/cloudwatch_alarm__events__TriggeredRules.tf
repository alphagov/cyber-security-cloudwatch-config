variable "eu-west-1__events__TriggeredRules" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

variable "eu-west-2__events__TriggeredRules" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

resource "aws_cloudwatch_metric_alarm" "euw1_cloudwatch_events_triggered_rules" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-1__events__TriggeredRules)
  provider            = aws.eu-west-1
  alarm_name          = "${var.eu-west-1__events__TriggeredRules[count.index].ResourceName}_TriggeredRules_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-1__events__TriggeredRules[count.index].Threshold
  alarm_description   = "Check the number of messages added to the queue is not too high."
  metric_name         = "TriggeredRules"
  namespace           = "AWS/Events"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-1__events__TriggeredRules[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw1_sns_cloudwatch_forwarder_topic}"]
}


resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_events_triggered_rules" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2__events__TriggeredRules)
  provider            = aws.eu-west-2
  alarm_name          = "${var.eu-west-2__events__TriggeredRules[count.index].ResourceName}_TriggeredRules_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-2__events__TriggeredRules[count.index].Threshold
  alarm_description   = "Alert if Cloudwatch Event Rule has been triggered."
  metric_name         = "TriggeredRules"
  namespace           = "AWS/Events"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-2__events__TriggeredRules[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
  ok_actions          = ["${local.euw2_sns_cloudwatch_forwarder_topic}"]
}
