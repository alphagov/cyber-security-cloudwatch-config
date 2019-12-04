# Terraform module to setup a Cloudwatch alarm to monitor the SentMessageSize for a standard SQS queue

locals {
  namespace = "AWS/SQS"
}

locals {
  metric_name = "SentMessageSize"
}

locals {
  threshold = 256
}

locals {
  statistic = "Maximum"
}

locals {
  sqs_dimensions = {
    QueueName = var.queue_name
  }
}

# locals {
#    sqs_alarm_tags = {
#    }
#}


resource "aws_cloudwatch_metric_alarm" "cloudwatch_metric_alarm" {
  alarm_name                = var.alarm_name
  comparison_operator       = var.comparison_operator
  evaluation_periods        = var.evaluation_periods
  metric_name               = local.metric_name
  namespace                 = local.namespace
  period                    = var.period
  statistic                 = local.statistic
  threshold                 = local.threshold
  alarm_description         = var.alarm_description
  alarm_actions		    = [var.alarm_actions]
  dimensions		    = local.sqs_dimensions
  # following variables commented out TBD if required
  # how to use if set in TF which calls this module ?
  #ok_actions               = var.ok_actions
  #insufficient_data_actions = var.insufficient_data_actions
  #datapoints_to_alarm      = var.datapoints_to_alarm
  #unit			    = var.unit
  #extended_statistic       = var.extended_statistic
  #treat_missing_data       = var.treat_missing_data
  #evaluate_low_sample_count_percentiles = var.evaluate_low_sample_count_percentiles
  #metric_query		    = var.metric_query
  #tags                     = local.sqs_alarm_tags
}
