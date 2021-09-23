variable "DEF_ENVIRONMENT" {
    type    = string
    default = "Test"
}

output "tags" {
  value = {
    Service       = "health"
    Environment   = var.DEF_ENVIRONMENT
    SvcOwner      = "cyber.security@digital.cabinet-office.gov.uk"
    DeployedUsing = "Terraform12"
    SvcCodeURL    = "https://github.com/alphagov/cyber-security-cloudwatch-config"
  }
}
