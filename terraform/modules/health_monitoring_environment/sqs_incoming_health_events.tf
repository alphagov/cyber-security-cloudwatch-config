resource "aws_sqs_queue" "incoming_health_events" {
  name                        = "incoming_health_events"
  visibility_timeout_seconds  = 60
  tags     = merge(module.tags.tags, map("Name", "incoming_health_events"))
}

data "aws_iam_policy_document" "incoming_health_events_resource_policy_data" {
  statement {
    effect  = "Allow"
    actions = ["sqs:SendMessage"]

    principals {
      type = "AWS"
      identifiers = formatlist(
        "arn:aws:iam::%s:role/cloudwatch_forwarder_role",
        var.monitored_accounts
      )
    }

    resources = list(aws_sqs_queue.incoming_health_events.arn)
  }
}

resource "aws_sqs_queue_policy" "incoming_health_events_sqs_resource_policy" {
  queue_url = aws_sqs_queue.incoming_health_events.id
  policy    = data.aws_iam_policy_document.incoming_health_events_resource_policy_data.json
}