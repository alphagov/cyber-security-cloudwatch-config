/*
module "sqs__ApproximateAgeOfOldestMessge" {
  source                = "../modules/cloudwatch_alarms/sqs/standard_queue/approx_age_of_oldest_message"
  count                 = length(var.sqs__ApproximateAgeOfOldestMessage)
  alarm_name            = "${var.sqs__ApproximateAgeOfOldestMessage[*].ResourceName}_alarm"
  comparison_operator   = "GreaterThanOrEqualToThreshold"
  evaluation_periods    = 2
  period                = 300
  enable_alarm          = true
  threshold             = var.sqs__ApproximateAgeOfOldestMessage[*].Threshold
  alarm_description     = "Check that messages are being processed in a reasonable time frame."
  # alarm_actions         =
  queue_name            = var.sqs__ApproximateAgeOfOldestMessage[*].ResourceName
  tags                  = var.sqs__ApproximateAgeOfOldestMessage[*].Tags
  providers             = {
    aws                 = "aws.${var.sqs__ApproximateAgeOfOldestMessage[*].Region}"
  }
}
*/

resource "aws_cloudwatch_metric_alarm" "cloudwatch_metric_alarm" {
  # iterate over count to setup multiple alarms
  count 		            = length(var.sqs__ApproximateAgeOfOldestMessage)
  provider                  = "aws.${var.sqs__ApproximateAgeOfOldestMessage[count.index].Region}"
  alarm_name                = "${var.sqs__ApproximateAgeOfOldestMessage[count.index].ResourceName}_alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 2
  #metric_name               = "ApproximateAgeOfOldestMessage"
  #namespace                 = "AWS/SQS"
  #period                    = 300
  #statistic                 = "Maximum"
  threshold                 = var.sqs__ApproximateAgeOfOldestMessage[count.index].Threshold
  alarm_description         = "Check that messages are being processed in a reasonable time frame."
  #alarm_actions		        = [var.alarm_actions]
  #dimensions		        = local.sqs_dimensions
  #ok_actions                = var.ok_actions
  #insufficient_data_actions  = var.insufficient_data_actions
  #datapoints_to_alarm       = var.datapoints_to_alarm
  #unit			     = var.unit
  #extended_statistic        = var.extended_statistic
  #treat_missing_data        = var.treat_missing_data
  #evaluate_low_sample_count_percentiles = var.evaluate_low_sample_count_percentiles
  #metric_query		     = var.metric_query
  #tags                      = local.sqs_alarm_tags

  metric_query {
    id = "m1"

    metric {
      metric_name = "ApproximateAgeOfOldestMessage"
      namespace   = "AWS/SQS"
      period      = 300
      stat        = "Maximum"

      dimensions = {
	    QueueName = var.sqs__ApproximateAgeOfOldestMessage[count.index].ResourceName
      }
    }
   }
}
