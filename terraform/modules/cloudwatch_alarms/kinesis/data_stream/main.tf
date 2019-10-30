locals {
  kinesis_dimensions          = {
    StreamName = var.stream_name
  }
}

resource "aws_cloudwatch_metric_alarm" "kinesis_data_stream_metric_alarm" {
  alarm_name                = var.alarm_name
  comparison_operator       = var.comparison_operator
  evaluation_periods        = var.evaluation_periods
  metric_name               = var.metric_name
  namespace                 = var.namespace
  period                    = var.period
  statistic                 = var.statistic
  threshold                 = var.threshold
  alarm_description         = var.alarm_description
  alarm_actions		    = var.alarm_action
  dimensions		    = local.kinesis_dimensions
}
