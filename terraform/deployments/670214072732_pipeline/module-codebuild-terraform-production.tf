module "codebuild_terraform_production" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_apply_terraform"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  deployment_account_id       = var.aws_account_id_production
  deployment_role_name        = "CodePipelineDeployerRole_${var.aws_account_id_production}"
  terraform_directory         = "terraform/deployments/${var.aws_account_id_production}"
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "Production"
  action_name                 = "TerraformApply"
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
      artifact = "alert_controller_lambda",
      source   = "alert_controller.zip"
      target   = "lambda/alert_controller"
    },
    {
      artifact = "report_netcraft_lambda",
      source   = "report_netcraft.zip"
      target   = "lambda/report_netcraft"
    }
  ]
}
