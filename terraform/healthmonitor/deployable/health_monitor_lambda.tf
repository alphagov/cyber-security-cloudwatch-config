locals {
  zipfile = "../../../lambda/health_monitor/health_monitor_lambda.zip"
}

resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = local.zipfile
  source_code_hash = filebase64sha256(local.zipfile)
  function_name    = "health_monitor_lambda"
  role             = aws_iam_role.health_monitor_role.arn
  handler          = "health_monitor.lambda_handler"
  timeout          = 60
  runtime          = "python3.7"
}

