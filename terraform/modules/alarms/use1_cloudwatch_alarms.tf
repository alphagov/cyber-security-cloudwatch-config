resource "aws_cloudwatch_metric_alarm" "use1_cloudwatch_alarms" {
  # iterate over count to setup multiple alarms
  count               = length(var.us-east-1_alarms)
  provider            = aws.us-east-1
  alarm_name          = join("_", [
    var.us-east-1_alarms[count.index].ResourceName,
    var.us-east-1_alarms[count.index].MetricName,
    "alarm"
  ])
  comparison_operator = var.us-east-1_alarms[count.index].ComparisonOperator
  evaluation_periods  = var.us-east-1_alarms[count.index].EvaluationPeriods
  threshold           = var.us-east-1_alarms[count.index].Threshold
  alarm_description   = var.us-east-1_alarms[count.index].Description
  metric_name         = var.us-east-1_alarms[count.index].MetricName
  namespace           = var.us-east-1_alarms[count.index].Namespace
  period              = var.us-east-1_alarms[count.index].Period
  statistic           = var.us-east-1_alarms[count.index].Statistic
  dimensions = jsondecode(
    format(
      "{\"%s\": \"%s\"}",
      var.us-east-1_alarms[count.index].DimensionName,
      var.us-east-1_alarms[count.index].DimensionValue
    )
  )
  alarm_actions       = [local.use1_sns_cloudwatch_forwarder_topic]
  ok_actions          = [local.use1_sns_cloudwatch_forwarder_topic]
  tags                = merge(
    module.tags.tags,
    map("Name", join("_", [
      var.us-east-1_alarms[count.index].ResourceName,
      var.us-east-1_alarms[count.index].MetricName,
      "alarm"
    ]))
  )
}
