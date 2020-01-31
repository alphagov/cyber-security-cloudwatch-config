resource "aws_lambda_function" "cloudwatch_metric_forwarder_euw1_lambda" {
  provider          = aws.eu-west-1
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_metric_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_metric_event_handler"
  runtime           = "python3.7"
  timeout           = 60

  environment {
    variables = {
      LOGLEVEL          = ""
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

resource "aws_cloudwatch_event_rule" "every_hour_euw1" {
  provider            = aws.eu-west-1
  name                = "every-hour"
  description         = "Fires every hour"
  schedule_expression = local.metric_cron
}

resource "aws_cloudwatch_event_target" "run_every_hour_euw1" {
  provider    = aws.eu-west-1
  rule        = aws_cloudwatch_event_rule.every_hour_euw1.name
  target_id   = aws_lambda_function.cloudwatch_metric_forwarder_euw1_lambda.function_name
  arn         = aws_lambda_function.cloudwatch_metric_forwarder_euw1_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_euw1" {
  provider        = aws.eu-west-1
  statement_id    = "AllowExecutionFromCloudWatch"
  action          = "lambda:InvokeFunction"
  function_name   = aws_lambda_function.cloudwatch_metric_forwarder_euw1_lambda.function_name
  principal       = "events.amazonaws.com"
  source_arn      = aws_cloudwatch_event_rule.every_hour_euw1.arn
}

resource "aws_lambda_function" "cloudwatch_metric_forwarder_euw2_lambda" {
  provider          = aws.eu-west-2
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_metric_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_metric_event_handler"
  runtime           = "python3.7"
  timeout           = 30

  environment {
    variables = {
      LOGLEVEL          = ""
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

resource "aws_cloudwatch_event_rule" "every_hour_euw2" {
  provider            = aws.eu-west-2
  name                = "every-hour"
  description         = "Fires every hour"
  schedule_expression = local.metric_cron
}

resource "aws_cloudwatch_event_target" "run_every_hour_euw2" {
  provider    = aws.eu-west-2
  rule        = aws_cloudwatch_event_rule.every_hour_euw2.name
  target_id   = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.function_name
  arn         = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_euw2" {
  provider        = aws.eu-west-2
  statement_id    = "AllowExecutionFromCloudWatch"
  action          = "lambda:InvokeFunction"
  function_name   = aws_lambda_function.cloudwatch_metric_forwarder_euw2_lambda.function_name
  principal       = "events.amazonaws.com"
  source_arn      = aws_cloudwatch_event_rule.every_hour_euw2.arn
}