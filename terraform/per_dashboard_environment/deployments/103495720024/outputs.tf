output "euw1_sns_arns" {
  value       = module.health_monitor.euw1_sns_arns
  description = "The ARNs for SNS topics"
}

output "euw1_sns_arn_map" {
  value       = module.health_monitor.euw1_sns_arn_map
  description = "A lookup for SNS topic ARNs"
}

output "euw2_sns_arns" {
  value       = module.health_monitor.euw2_sns_arns
  description = "The ARNs for SNS topics"
}

output "euw2_sns_arn_map" {
  value       = module.health_monitor.euw2_sns_arn_map
  description = "A lookup for SNS topic ARNs"
}
