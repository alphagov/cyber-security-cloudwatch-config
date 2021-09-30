resource "aws_cloudwatch_metric_alarm" "euw2_cloudwatch_alarms" {
  # iterate over count to setup multiple alarms
  count               = length(var.eu-west-2_alarms)
  provider            = aws.eu-west-2
  alarm_name          = join("_", [
    var.eu-west-2_alarms[count.index].ResourceName,
    var.eu-west-2_alarms[count.index].MetricName,
    "alarm"
  ])
  comparison_operator = var.eu-west-2_alarms[count.index].ComparisonOperator
  evaluation_periods  = var.eu-west-2_alarms[count.index].EvaluationPeriods
  threshold           = var.eu-west-2_alarms[count.index].Threshold
  alarm_description   = var.eu-west-2_alarms[count.index].Description
  metric_name         = var.eu-west-2_alarms[count.index].MetricName
  namespace           = var.eu-west-2_alarms[count.index].Namespace
  period              = var.eu-west-2_alarms[count.index].Period
  statistic           = var.eu-west-2_alarms[count.index].Statistic
  dimensions = jsondecode(
    format(
      "{\"%s\": \"%s\"}",
      var.eu-west-2_alarms[count.index].DimensionName,
      var.eu-west-2_alarms[count.index].DimensionValue
    )
  )
  alarm_actions       = [local.euw2_sns_cloudwatch_forwarder_topic]
  ok_actions          = [local.euw2_sns_cloudwatch_forwarder_topic]
  tags                = merge(
    module.tags.tags,
    map("Name", join("_", [
      var.eu-west-2_alarms[count.index].ResourceName,
      var.eu-west-2_alarms[count.index].MetricName,
      "alarm"
    ]))
  )
}
