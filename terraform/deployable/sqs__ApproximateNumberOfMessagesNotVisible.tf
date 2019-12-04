variable "eu-west-1__sqs__ApproximateNumberOfMessagesNotVisible" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

variable "eu-west-2__sqs__ApproximateNumberOfMessagesNotVisible" {
  description = "List of metrics derived from aws cloudwatch list-metrics"
  type        = list
  default     = []
}

resource "aws_cloudwatch_metric_alarm" "euw1_cloudwatch_sqs_approx_num_of_messages_not_visible" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-1__sqs__ApproximateNumberOfMessagesNotVisible)
  provider            = aws.eu-west-1
  alarm_name          = "${var.eu-west-1__sqs__ApproximateNumberOfMessagesNotVisible[count.index].ResourceName}_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-1__sqs__ApproximateNumberOfMessagesNotVisible[count.index].Threshold
  alarm_description   = "Check that messages are being processed in a reasonable time frame."
  metric_name         = "ApproximateNumberOfMessagesNotVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-1__sqs__ApproximateNumberOfMessagesNotVisible[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw1_sns_health_topic}"]
  ok_actions          = ["${local.euw1_sns_health_topic}"]
}


resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_sqs_approx_num_of_messages_not_visible" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2__sqs__ApproximateNumberOfMessagesNotVisible)
  provider            = aws.eu-west-2
  alarm_name          = "${var.eu-west-2__sqs__ApproximateNumberOfMessagesNotVisible[count.index].ResourceName}_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  threshold           = var.eu-west-2__sqs__ApproximateNumberOfMessagesNotVisible[count.index].Threshold
  alarm_description   = "Check that messages are being processed in a reasonable time frame."
  metric_name         = "ApproximateNumberOfMessagesNotVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Maximum"
  dimensions = {
    QueueName = var.eu-west-2__sqs__ApproximateNumberOfMessagesNotVisible[count.index].ResourceName
  }
  alarm_actions       = ["${local.euw2_sns_health_topic}"]
  ok_actions          = ["${local.euw2_sns_health_topic}"]
}
