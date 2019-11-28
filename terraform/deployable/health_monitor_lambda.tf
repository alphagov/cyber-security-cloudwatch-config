resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = var.LAMBDA_FILENAME
  source_code_hash = filebase64sha256(var.LAMBDA_FILENAME)
  function_name    = var.FUNCTION_NAME
  role             = aws_iam_role.health_monitor_role.arn
  handler          = var.HANDLER
  timeout          = var.TIMEOUT
  runtime          = var.RUNTIME
}


/*
resource "aws_sns_topic_subscription" "health_monitor_euw1_sns_subscription" {
  topic_arn = local.euw1_sns_health_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.health_monitor_lambda.arn
}
*/

resource "aws_sns_topic_subscription" "health_monitor_euw2_sns_subscription" {
  topic_arn = local.euw2_sns_health_topic
  protocol  = "lambda"
  endpoint  = aws_lambda_function.health_monitor_lambda.arn
}
