locals {
  zipfile = "../../../lambda/health_package.zip"
}

resource "aws_lambda_function" "cloudwatch_forwarder_euw1_lambda" {
  provider          = aws.eu-west-1
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.cloudwatch_event_handler"
  runtime           = "python3.7"

  environment {
    variables = {
      LOGLEVEL = ""
      PROD_ACCOUNT = module.reference_accounts.production
      TEST_ACCOUNT = module.reference_accounts.staging
      TARGET_ROLE = var.TARGET_ROLE
      TARGET_LAMBDA = var.TARGET_LAMBDA
      TARGET_REGION = var.TARGET_REGION
      DEF_ENVIRONMENT = var.DEF_ENVIRONMENT
    }
  }
}

resource "aws_sns_topic_subscription" "cloudwatch_forwarder_euw1_sns_subscription" {
  provider  = aws.eu-west-1
  topic_arn = local.euw1_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_forwarder_euw1_lambda.arn
}

resource "aws_lambda_function" "cloudwatch_forwarder_euw2_lambda" {
  provider          = aws.eu-west-2
  filename          = local.zipfile
  source_code_hash  = filebase64sha256(local.zipfile)
  function_name     = "cloudwatch_forwarder"
  role              = aws_iam_role.cloudwatch_forwarder_role.arn
  handler           = "lambda_handler.lambda_handler"
  runtime           = "python3.7"

  environment {
    variables = {
      LOGLEVEL = ""
      PROD_ACCOUNT = module.reference_accounts.production
      TEST_ACCOUNT = module.reference_accounts.staging
      TARGET_ROLE = "health_monitor_forwarder"
      TARGET_LAMBDA = "health_monitor_lambda"
      TARGET_REGION = "eu-west-2"
    }
  }
}

resource "aws_sns_topic_subscription" "health_monitor_euw2_sns_subscription" {
  provider  = aws.eu-west-2
  topic_arn = local.euw2_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_forwarder_euw1_lambda.arn
}
