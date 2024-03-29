resource "aws_lambda_function" "health_monitor_update_dashboard_lambda" {
  filename         = var.lambda_zip
  source_code_hash = filebase64sha256(var.lambda_zip)
  function_name    = "health_monitor_splunk_forwarder_lambda"
  role             = aws_iam_role.health_monitor_update_dashboard_role.arn
  handler          = "lambda_handler.splunk_forwarder_event_handler"
  timeout          = 60
  runtime          = "python3.7"
  tags     = merge(module.tags.tags, map("Name", "health_monitor_splunk_forwarder_lambda"))
}

resource "aws_lambda_permission" "allow_invocation_from_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.health_monitor_update_dashboard_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = local.dashboard_sns_arn
}

resource "aws_sns_topic_subscription" "subscribe_lambda_to_sns" {
  topic_arn = local.dashboard_sns_arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.health_monitor_update_dashboard_lambda.arn
}
