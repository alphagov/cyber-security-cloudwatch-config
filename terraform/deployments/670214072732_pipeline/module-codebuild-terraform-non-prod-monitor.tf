locals {
  test_monitor = lookup(var.monitor_environments, "test")
}
module "codebuild_terraform_non_prod_monitor" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_apply_terraform"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  deployment_account_id       = local.test_monitor
  deployment_role_name        = "CodePipelineDeployerRole_${local.test_monitor}"
  terraform_version           = "0.12.31"
  terraform_directory         = "terraform/deployments/${local.test_monitor}_health_monitor"
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "NonProd"
  action_name                 = "TerraformMonitor"
  environment                 = var.environment
  docker_hub_credentials      = var.docker_hub_creds_secret
  tags                        = local.tags
  copy_artifacts              = [
    {
      artifact = "ssh_config",
      source   = ".ssh"
      target   = "/root/.ssh"
    },
    {
      artifact = "lambda",
      source   = "health_package.zip"
      target   = "lambda/health_package"
    }
  ]
}
