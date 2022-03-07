# data "aws_iam_policy_document" "health_monitor_concourse_assume_role" {
#   statement {
#     effect  = "Allow"
#     actions = ["sts:AssumeRole"]

#     principals {
#       type        = "AWS"
#       identifiers = [
#         "arn:aws:iam::${module.reference_accounts.concourse}:role/cd-cybersecurity-tools-concourse-worker"
#       ]
#     }
#   }
# }

# resource "aws_iam_role" "health_monitor_concourse_role" {
#   name               = "health_monitor_concourse_role"
#   assume_role_policy = data.aws_iam_policy_document.health_monitor_concourse_assume_role.json
# }

# data "aws_iam_policy" "ssm_read_only_policy" {
#   arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
# }

# resource "aws_iam_role_policy_attachment" "ssm_read_only_policy_attach" {
#   role       = aws_iam_role.health_monitor_concourse_role.name
#   policy_arn = data.aws_iam_policy.ssm_read_only_policy.arn
# }
