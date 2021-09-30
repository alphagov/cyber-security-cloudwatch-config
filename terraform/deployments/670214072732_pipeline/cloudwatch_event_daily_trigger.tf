resource "aws_cloudwatch_event_rule" "cloudwatch_config_event_rule" {
  name                = "cloud-watch-config-cron-schedule"
  description         = "Run the pipeline daily to update alarm config"
  schedule_expression = "cron(0 8 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "cloudwatch_config_daily_trigger" {
  rule     = aws_cloudwatch_event_rule.cloudwatch_config_event_rule.name
  arn      = aws_codepipeline.cloudwatch_config.arn
  role_arn = data.aws_iam_role.pipeline_role.arn
}
