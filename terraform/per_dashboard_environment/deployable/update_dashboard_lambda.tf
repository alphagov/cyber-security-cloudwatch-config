locals {
  health_monitor_update_splunk_dashboard_zipfile = "../../../lambda/update_dashboard/health_monitor_update_dashboard.zip"
}

data "terraform_remote_state" "health_monitor_state" {
  backend = "s3"
  config = {
    bucket  = "gds-security-terraform"
    key     = "terraform/state/account/${data.aws_caller_identity.current.account_id}/service/health-monitor.tfstate"
    region  = "eu-west-2"
    encrypt = true
  }
}

resource "aws_lambda_function" "health_monitor_update_dashboard_lambda" {
  filename         = local.health_monitor_update_splunk_dashboard_zipfile
  source_code_hash = filebase64sha256(local.health_monitor_update_splunk_dashboard_zipfile)
  function_name    = "health_monitor_update_dashboard_lambda"
  role             = aws_iam_role.health_monitor_update_dashboard_role.arn
  handler          = "health_monitor_update_dashboard.lambda_handler"
  timeout          = 60
  runtime          = "python3.7"
}

resource "aws_lambda_permission" "allow_invocation_from_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.health_monitor_update_dashboard_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = lookup(data.terraform_remote_state.health_monitor_state.outputs.euw2_sns_arn_map, "notify_dashboard_lambda")
}

resource "aws_sns_topic_subscription" "subscribe_lambda_to_sns" {
  topic_arn = lookup(data.terraform_remote_state.health_monitor_state.outputs.euw2_sns_arn_map, "notify_dashboard_lambda")
  protocol  = "lambda"
  endpoint  = aws_lambda_function.health_monitor_update_dashboard_lambda.arn
}
