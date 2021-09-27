module "codebuild_build_ssh_config" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_build_ssh_config"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "Prep"
  action_name                 = "BuildSSHConfig"
  environment                 = var.environment
  deploy_key                  = var.ssm_deploy_key
  tags                        = local.tags
}
