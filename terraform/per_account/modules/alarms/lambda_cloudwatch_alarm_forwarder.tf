resource "aws_lambda_function" "cloudwatch_alarm_forwarder_euw1_lambda" {
  provider          = aws.eu-west-1
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_alarm_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_alarm_event_handler"
  runtime           = "python3.7"
  timeout           = 30
  tags              = merge(module.tags.tags, map("Name", "cloudwatch_alarm_forwarder_euw1_${data.aws_caller_identity.current.account_id}"))

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

resource "aws_lambda_permission" "cloudwatch_alarm_forwarder_euw1_sns_invoke" {
  provider  = aws.eu-west-1
  statement_id  = "CloudForwarderEUW1AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cloudwatch_alarm_forwarder_euw1_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.euw1_sns_cloudwatch_forwarder_topic
}

resource "aws_sns_topic_subscription" "cloudwatch_alarm_forwarder_euw1_sns_subscription" {
  provider  = aws.eu-west-1
  topic_arn = local.euw1_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_alarm_forwarder_euw1_lambda.arn
}

resource "aws_lambda_function" "cloudwatch_alarm_forwarder_euw2_lambda" {
  provider          = aws.eu-west-2
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_alarm_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_alarm_event_handler"
  runtime           = "python3.7"
  timeout           = 30
  tags              = merge(module.tags.tags, map("Name", "cloudwatch_alarm_forwarder_euw2_${data.aws_caller_identity.current.account_id}"))

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

resource "aws_lambda_permission" "cloudwatch_alarm_forwarder_euw2_sns_invoke" {
  provider  = aws.eu-west-2
  statement_id  = "CloudForwarderEUW2AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cloudwatch_alarm_forwarder_euw2_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.euw2_sns_cloudwatch_forwarder_topic
}

resource "aws_sns_topic_subscription" "health_monitor_euw2_sns_subscription" {
  provider  = aws.eu-west-2
  topic_arn = local.euw2_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_alarm_forwarder_euw2_lambda.arn
}
