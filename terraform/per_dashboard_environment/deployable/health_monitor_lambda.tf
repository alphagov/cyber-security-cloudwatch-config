resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = local.zipfile
  source_code_hash = filebase64sha256(local.zipfile)
  function_name    = "health_monitor_lambda"
  role             = aws_iam_role.health_monitor_role.arn
  handler          = "lambda_handler.health_monitor_handler"
  timeout          = 60
  runtime          = "python3.7"

  environment {
    variables = {
      LOGLEVEL          = "DEBUG"
      PAGERDUTY_SNS_ARN = local.pagerduty_sns_arn
      SLACK_SNS_ARN     = local.slack_sns_arn
      DASHBOARD_SNS_ARN = local.dashboard_sns_arn
    }
  }
}

