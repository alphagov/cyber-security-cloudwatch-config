variable "LAMBDA_FILENAME" {
  type    = string
  default = "health_monitor_lambda.zip"
}

variable "FUNCTION_NAME" {
  type    = string
  default = "health_monitor_lambda"
}

variable "ROLE" {
  type    = string
  default = "health_monitor_role"
}

variable "HANDLER" {
  type    = string
  default = "health_monitor.handler"
}

variable "TIMEOUT" {
  type    = number
  default = 60
}

variable "RUNTIME" {
  type    = string
  default = "python3.7"
}

variable "sns_topic_names" {
  description = "SNS topic names"
  type        = list(string)
  default     = ["health_monitoring_lambda", "notify_slack_lambda", "notify_pagerduty_lambda", "notify_dashboard_lambda"]
}

resource "aws_lambda_function" "health_monitor_lambda" {
  filename         = var.LAMBDA_FILENAME
  source_code_hash = filebase64sha256(var.LAMBDA_FILENAME)
  function_name    = var.FUNCTION_NAME
  role             = var.ROLE
  handler          = var.HANDLER
  timeout          = var.TIMEOUT
  runtime          = var.RUNTIME
}

resource "aws_sns_topic" "sns_topic" {
  count = length(var.sns_topic_names)
  name  = var.sns_topic_names[count.index]
}

output "all_sns_arns" {
  value       = aws_sns_topic.sns_topic[*].arn
  description = "The ARNs for SNS topics"
}

resource "aws_iam_policy" "policy" {
  name        = "health_monitor_"
  path        = "/"
  description = "Invoke Health Monitor Lambda from SNS"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "SNS:Publish*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
