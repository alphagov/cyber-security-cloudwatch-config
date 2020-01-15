data "aws_sns_topic" "health_monitor_sub" {
  name = "alert-controller-health-monitor"
}

resource "aws_lambda_permission" "cloudwatch_forwarder_euw2_sns_invoke" {
  statement_id  = "CloudForwarderEUW2AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.health_monitor_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = data.aws_sns_topic.health_monitor_sub.arn
}

resource "aws_sns_topic_subscription" "health_monitor_euw2_sns_subscription" {
  topic_arn = data.aws_sns_topic.health_monitor_sub.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.health_monitor_lambda.arn
}
