resource "aws_lambda_function" "cloudwatch_metric_forwarder_euw2_lambda" {
  provider          = aws.eu-west-2
  filename          = var.lambda_zip
  source_code_hash  = filebase64sha256(var.lambda_zip)
  function_name     = "cloudwatch_metric_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_metric_event_handler"
  runtime           = "python3.7"
  timeout           = 300
  tags              = merge(module.tags.tags, map("Name", "cloudwatch_metric_forwarder_euw2_${data.aws_caller_identity.current.account_id}"))

  environment {
    variables = {
      LOG_LEVEL         = var.LOG_LEVEL
      PROD_ACCOUNT      = module.reference_accounts.production
      TEST_ACCOUNT      = module.reference_accounts.staging
      TARGET_ROLE       = var.TARGET_ROLE
      TARGET_LAMBDA     = var.TARGET_LAMBDA
      TARGET_SQS_QUEUE  = var.TARGET_SQS_QUEUE
      TARGET_REGION     = var.TARGET_REGION
      DEF_ENVIRONMENT   = var.DEF_ENVIRONMENT
    }
  }
}

resource "aws_cloudwatch_event_rule" "cron_euw2" {
  provider            = aws.eu-west-2
  name                = "metrics_cron_euw2"
  description         = "Fires every hour"
  schedule_expression = var.metrics_cron
  tags                = merge(module.tags.tags, map("Name", "every_hour_health_monitoring_euw2_${data.aws_caller_identity.current.account_id}"))
}

resource "aws_cloudwatch_event_target" "cron_euw2" {
  provider    = aws.eu-west-2
  rule        = aws_cloudwatch_event_rule.cron_euw2.name
  target_id   = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.function_name
  arn         = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_euw2" {
  provider        = aws.eu-west-2
  statement_id    = "AllowExecutionFromCloudWatch"
  action          = "lambda:InvokeFunction"
  function_name   = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.function_name
  principal       = "events.amazonaws.com"
  source_arn      = aws_cloudwatch_event_rule.cron_euw2.arn
}
