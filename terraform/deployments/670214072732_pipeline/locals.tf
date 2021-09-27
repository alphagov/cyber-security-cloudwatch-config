locals {
  tags = {
    Service       = var.service_name
    Environment   = var.environment
    SvcOwner      = "Cyber"
    DeployedUsing = "Terraform_v12"
    SvcCodeURL    = "https://github.com/alphagov/cyber-security-concourse-base-image"
  }

  docker_hub_creds    = jsondecode(data.aws_secretsmanager_secret_version.dockerhub_creds.secret_string)
  docker_hub_username = lookup(local.docker_hub_creds,"username")
  docker_hub_password = lookup(local.docker_hub_creds,"password")
}
