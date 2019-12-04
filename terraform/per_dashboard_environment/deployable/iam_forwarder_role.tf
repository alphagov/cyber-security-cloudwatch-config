data "aws_iam_policy_document" "health_monitor_forwarder_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = [
        "arn:aws:iam::${module.reference_accounts.staging}:role/cloudwatch_forwarder_role"
      ]
    }
  }
}

resource "aws_iam_role" "health_monitor_forwarder_role" {
  name               = "health_monitor_forwarder_role"
  assume_role_policy = data.aws_iam_policy_document.health_monitor_forwarder_assume_role.json
}

# Publish events to SNS topic
data "aws_iam_policy_document" "health_monitor_forwarder_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "lambda:Invoke"
    ]

    resources = [
      aws_lambda_function.health_monitor_lambda.arn
    ]
  }
}

resource "aws_iam_policy" "health_monitor_forwarder_policy" {
  name   = "HealthMonitorForwarderPolicy"
  policy = data.aws_iam_policy_document.health_monitor_forwarder_policy_document.json
}

resource "aws_iam_role_policy_attachment" "health_monitor_forwarder_policy_attachment" {
  role       = aws_iam_role.health_monitor_forwarder_role.name
  policy_arn = aws_iam_policy.health_monitor_forwarder_policy.arn
}