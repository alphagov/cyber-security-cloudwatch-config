resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = local.zipfile
  source_code_hash = filebase64sha256(local.zipfile)
  function_name    = "health_monitor_lambda"
  role             = aws_iam_role.health_monitor_role.arn
  handler          = "lambda_handler.health_monitor_handler"
  timeout          = 60
  runtime          = "python3.7"
  tags             = merge(module.tags.tags, map("Name", "health_monitor_lambda"))

  environment {
    variables = {
      DEF_ENVIRONMENT   = var.DEF_ENVIRONMENT
      LOG_LEVEL         = var.LOG_LEVEL
      PAGERDUTY_SNS_ARN = local.pagerduty_sns_arn
      SLACK_SNS_ARN     = local.slack_sns_arn
      DASHBOARD_SNS_ARN = local.dashboard_sns_arn
    }
  }
}

resource "aws_lambda_event_source_mapping" "health_monitor_invoke_from_sqs" {
  event_source_arn = aws_sqs_queue.incoming_health_events.arn
  function_name    = aws_lambda_function.health_monitor_lambda.arn
}
