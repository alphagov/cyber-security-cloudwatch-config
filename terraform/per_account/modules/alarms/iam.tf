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
  tags                = merge(module.tags.tags, map("Name", "cloudwatch_forwarder_role_${data.aws_caller_identity.current.account_id}"))
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

  statement {
    effect = "Allow"

    actions = [
      "cloudwatch:DescribeAlarms",
      "cloudwatch:GetMetricStatistics"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "lambda:GetFunction",
      "lambda:ListTags"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sqs:SendMessage"
    ]

    resources = [
      "arn:aws:sqs:${var.TARGET_REGION}:${module.reference_accounts.production}:${var.TARGET_SQS_QUEUE}",
      "arn:aws:sqs:${var.TARGET_REGION}:${module.reference_accounts.staging}:${var.TARGET_SQS_QUEUE}"
    ]
  }

   statement {
    effect = "Allow"

    actions = [
      "codepipeline:ListTagsForResource"
    ]

    resources = [
      "*"
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
