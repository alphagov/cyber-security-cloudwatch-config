variable "service_name" {
  description = "The name of the pipeline"
  type        = string
  default     = "cloudwatch-config"
}

variable "repository_name" {
  description = "The name of the github source repository"
  type        = string
  default     = "alphagov/cyber-security-cloudwatch-config"
}

variable "environment" {
  description = "Environment for health monitoring classification"
  type        = string
  default     = "production"
}


variable "codestar_connection_id" {
  description = "The ID of the codestar connection"
  type        = string
  default     = "51c5be90-8c8f-4d32-8be4-18b8f05c802c"
}

variable "docker_hub_creds_secret" {
  description = "The name of the Docker Hub creds Secrets Manager secret"
  type        = string
  default     = "docker_hub_credentials"
}

variable "default_container_image" {
  description = "The default image to use for any codebuild projects"
  type        = string
  default     = "gdscyber/cyber-security-cd-base-image:latest"
}

variable "ssm_github_pat" {
  description = "The SSM path to the github PAT"
  type        = string
  default     = "/github/pat"
}

variable "ssm_deploy_key" {
  description = "The SSM path to a readonly deploy key for cyber-security-terraform"
  type        = string
  default     = "/github/deploy-keys/cyber-security-terraform"
}

variable "aws_account_id_staging" {
  description = "The AWS account for the staging deployment"
  type        = string
  default     = "103495720024"
}

variable "aws_account_id_production" {
  description = "The AWS account for the production deployment"
  type        = string
  default     = "779799343306"
}

variable "github_branch_name" {
  description = "The Github branch to trigger the pipeline from"
  type        = string
  default     = "ce-287-refactor-terraform"
}

variable "non_prod_accounts" {
  type        = list(string)
  default     = [
    "103495720024",
    "489877524855"
  ]
}

variable "prod_accounts" {
  type        = list(string)
  default     = [
    "670214072732",
    "779799343306",
    "885513274347"
  ]
}
