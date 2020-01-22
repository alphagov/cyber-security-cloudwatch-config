resource "aws_sqs_queue" "incoming_health_events" {
  name                        = "incoming_health_events"
  visibility_timeout_seconds  = 60
}

data "aws_iam_policy_document" "incoming_health_events_resource_policy_data" {
  statement {
    effect  = "Allow"
    actions = ["sqs:SendMessage"]

    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${module.reference_accounts.staging}:role/cloudwatch_forwarder_role",
        "arn:aws:iam::${module.reference_accounts.csls}:role/cloudwatch_forwarder_role",
        "arn:aws:iam::${module.reference_accounts.demo}:role/cloudwatch_forwarder_role"
      ]
    }

    resources = list(aws_sqs_queue.incoming_health_events.arn)
  }
}

resource "aws_sqs_queue_policy" "incoming_health_events_sqs_resource_policy" {
  queue_url = aws_sqs_queue.incoming_health_events.id
  policy    = data.aws_iam_policy_document.incoming_health_events_resource_policy_data.json
}