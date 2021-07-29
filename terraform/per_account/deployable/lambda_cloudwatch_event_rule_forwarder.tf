resource "aws_lambda_function" "cloudwatch_event_rule_forwarder_lambda" {
  provider          = aws.eu-west-2
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_event_rule_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_event_rule_handler"
  runtime           = "python3.7"
  timeout           = 30
  tags              = merge(module.tags.tags, map("Name", "cloudwatch_event_rule_forwarder_${data.aws_caller_identity.current.account_id}"))

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

data "aws_sns_topic" "codepipeline_health_notification" {
  name = "codepipeline-health-notification"
}

resource "aws_lambda_permission" "cloudwatch_forwarder_codepipeline_sns_invoke" {
  statement_id  = "CloudForwarderCodepipelineAllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cloudwatch_event_rule_forwarder_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = data.aws_sns_topic.codepipeline_health_notification.arn
}

resource "aws_sns_topic_subscription" "health_monitor_codepipeline_sns_subscription" {
  topic_arn = data.aws_sns_topic.codepipeline_health_notification.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_event_rule_forwarder_lambda.arn
}
