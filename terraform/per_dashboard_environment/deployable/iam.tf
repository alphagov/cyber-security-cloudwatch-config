data "aws_iam_policy_document" "health_monitor_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "health_monitor_role" {
  name               = "health_monitor_role"
  assume_role_policy = data.aws_iam_policy_document.health_monitor_assume_role.json
}

# Publish events to SNS topic
data "aws_iam_policy_document" "health_monitor_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "sns:Publish"
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "health_monitor_policy" {
  name   = "HealthMonitorPolicy"
  policy = data.aws_iam_policy_document.health_monitor_policy_document.json
}

resource "aws_iam_role_policy_attachment" "health_monitor_policy_attachment" {
  role       = aws_iam_role.health_monitor_role.name
  policy_arn = aws_iam_policy.health_monitor_policy.arn
}

resource "aws_iam_role_policy_attachment" "health_monitor_canned_policy_attachment" {
  role       = aws_iam_role.health_monitor_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


