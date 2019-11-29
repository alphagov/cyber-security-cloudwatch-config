resource "aws_lambda_function" "cloudwatch_forwarder_euw1_lambda" {
  provider          = aws.eu-west-1
  filename          = var.LAMBDA_FILENAME
  source_code_hash  = filebase64sha256(var.LAMBDA_FILENAME)
  function_name     = var.FUNCTION_NAME
  role              = aws_iam_role.health_monitor_role.arn
  handler           = var.HANDLER
  timeout           = var.TIMEOUT
  runtime           = var.RUNTIME
}

resource "aws_sns_topic_subscription" "cloudwatch_forwarder_euw1_sns_subscription" {
  provider  = aws.eu-west-1
  topic_arn = local.euw1_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_forwarder_euw1_lambda.arn
}

resource "aws_lambda_function" "cloudwatch_forwarder_euw2_lambda" {
  provider          = aws.eu-west-2
  filename          = var.LAMBDA_FILENAME
  source_code_hash  = filebase64sha256(var.LAMBDA_FILENAME)
  function_name     = var.FUNCTION_NAME
  role              = aws_iam_role.health_monitor_role.arn
  handler           = var.HANDLER
  timeout           = var.TIMEOUT
  runtime           = var.RUNTIME
}

resource "aws_sns_topic_subscription" "health_monitor_euw2_sns_subscription" {
  provider  = aws.eu-west-2
  topic_arn = local.euw2_sns_cloudwatch_forwarder_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloudwatch_forwarder_euw1_lambda.arn
}
