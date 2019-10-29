#output "approx_age_of_oldest_message_arn" {
#	description = "ARN for ApproximateAgeOfOldestMessage Cloudwatch alarm"
#	value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.arn
#}

#output "approx_age_of_oldest_message_id" {
#        description = "id for ApproximateAgeOfOldestMessage Cloudwatch alarm"
#        value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm.id
#}

# all ARNs
#output "approx_age_of_oldest_message_all_arns" {
#        description = "ARNs for all ApproximateAgeOfOldestMessage Cloudwatch alarms"
#        value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm[*].arn
#}

# all IDs
#output "approx_age_of_oldest_message_all_arns" {
#        description = "IDs for all ApproximateAgeOfOldestMessage Cloudwatch alarms"
#        value = aws_cloudwatch_metric_alarm.cloudwatch_metric_alarm[*].id
#}
