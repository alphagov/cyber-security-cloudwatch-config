# Terraform module to setup a Cloudwatch alarm to monitor the NumberOfMessagesSent for an SQS queue is 10% over the baseline

locals {
  namespace = "AWS/SQS"
}

locals {
  metric_name = "NumberOfMessagesSent"
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
  #metric_name               = local.metric_name
  #namespace                 = local.namespace
  #period                    = var.period
  #statistic                 = var.statistic
  threshold                 = var.threshold
  alarm_description         = var.alarm_description
  alarm_actions		    = [var.alarm_actions]
  #dimensions		    = local.sqs_dimensions
  #ok_actions               = var.ok_actions
  #insufficient_data_actions = var.insufficient_data_actions
  #datapoints_to_alarm      = var.datapoints_to_alarm
  #unit			    = var.unit
  #extended_statistic       = var.extended_statistic
  #treat_missing_data       = var.treat_missing_data
  #evaluate_low_sample_count_percentiles = var.evaluate_low_sample_count_percentiles
  #metric_query		    = var.metric_query
  #tags                     = local.sqs_alarm_tags

  # calculate 10% above the threshold
  metric_query {
        id = "e2"
        expression = "m1*1.1"
        label = "10_percent_over_threshold"
        return_data = "true"
  }

  metric_query {
    id = "m1"

    metric {
      metric_name = local.metric_name
      namespace   = local.namespace
      period      = var.period
      stat        = "Sum"
      #unit        = ""

      dimensions = {
        QueueName = var.queue_name
      }
    }
   }
}
