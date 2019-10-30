module "sqs__ApproximateAgeOfOldestMessge" {
  source                = "../modules/cloudwatch_alarms/sqs/standard_queue/approx_age_of_oldest_message"
  count                 = length(var.sqs__ApproximateAgeOfOldestMessage)
  alarm_name            = "{var.sqs__ApproximateAgeOfOldestMessge[count.index].ResourceName}_alarm"
  comparison_operator   = "GreaterThanOrEqualToThreshold"
  evaluation_periods    = 2
  period                = 300
  enable_alarm          = true
  threshold             = var.sqs__ApproximateAgeOfOldestMessage[count.index].Threshold
  alarm_description     = "Check that messages are being processed in a reasonable time frame."
  # alarm_actions         =
  queue_name            = var.sqs__ApproximateAgeOfOldestMessage[count.index].ResourceName
  tags                  = var.sqs__ApproximateAgeOfOldestMessage[count.index].Tags
}