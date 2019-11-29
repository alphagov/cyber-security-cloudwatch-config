resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = var.LAMBDA_FILENAME
  source_code_hash = filebase64sha256(var.LAMBDA_FILENAME)
  function_name    = var.FUNCTION_NAME
  role             = aws_iam_role.health_monitor_role.arn
  handler          = var.HANDLER
  timeout          = var.TIMEOUT
  runtime          = var.RUNTIME
}