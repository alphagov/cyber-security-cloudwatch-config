module "codebuild_get_changed_file_list" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_get_changed_file_list"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  deployment_account_id       = data.aws_caller_identity.current.account_id
  deployment_role_name        = "CodePipelineDeployerRole_${data.aws_caller_identity.current.account_id}"
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "Prep"
  action_name                 = "GetChangedFiles"
  environment                 = var.environment
  github_pat                  = var.ssm_github_pat
  repo_name                   = "cyber-security-alert-processor"
  docker_hub_credentials      = var.docker_hub_creds_secret
  output_artifact_path        = "changed_files.json"
  tags                        = local.tags
}
