data "aws_iam_policy_document" "cloudwatch_forwarder_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = [
        "lambda.amazonaws.com",
        "sns.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "cloudwatch_forwarder_role" {
  name               = "cloudwatch_forwarder_role"
  assume_role_policy = data.aws_iam_policy_document.cloudwatch_forwarder_assume_role.json
}

# Publish events to SNS topic
data "aws_iam_policy_document" "cloudwatch_forwarder_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "sns:Publish"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole"
    ]

    resources = [
      "arn:aws:iam::*:role/health_monitor_forwarder_role"
    ]
  }

}

resource "aws_iam_policy" "cloudwatch_forwarder_policy" {
  name   = "CloudWatchForwarderPolicy"
  policy = data.aws_iam_policy_document.cloudwatch_forwarder_policy_document.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_forwarder_policy_attachment" {
  role       = aws_iam_role.cloudwatch_forwarder_role.name
  policy_arn = aws_iam_policy.cloudwatch_forwarder_policy.arn
}

resource "aws_iam_role_policy_attachment" "cloudwatch_forwarder_canned_policy_attachment" {
  role       = aws_iam_role.cloudwatch_forwarder_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "security_audit_role_policy_attachment" {
  role       = aws_iam_role.cloudwatch_forwarder_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}
