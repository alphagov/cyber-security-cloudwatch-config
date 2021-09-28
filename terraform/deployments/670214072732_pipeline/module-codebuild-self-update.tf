module "codebuild_self_update" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_apply_terraform"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  deployment_account_id       = data.aws_caller_identity.current.account_id
  deployment_role_name        = "CodePipelineDeployerRole_${data.aws_caller_identity.current.account_id}"
  terraform_directory         = "terraform/deployments/${data.aws_caller_identity.current.account_id}_pipeline"
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "Pipeline"
  action_name                 = "UpdatePipeline"
  environment                 = var.environment
  docker_hub_credentials      = var.docker_hub_creds_secret
  tags                        = local.tags
}
