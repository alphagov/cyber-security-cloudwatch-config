module "codebuild_get_actions_required" {
  source                      = "github.com/alphagov/cyber-security-shared-terraform-modules//codebuild/codebuild_get_actions_required"
  codebuild_service_role_name = data.aws_iam_role.pipeline_role.name
  deployment_account_id       = data.aws_caller_identity.current.account_id
  deployment_role_name        = "CodePipelineDeployerRole_${data.aws_caller_identity.current.account_id}"
  docker_hub_credentials      = var.docker_hub_creds_secret
  codebuild_image             = var.default_container_image
  pipeline_name               = var.service_name
  stage_name                  = "Prep"
  action_name                 = "GetActionsRequired"
  environment                 = var.environment
  changed_files_json          = "/changed_files.json"
  action_triggers_json        = "/terraform/deployments/670214072732_pipeline/action_triggers.json"
  output_artifact_path        = "actions_required.json"
  tags                        = local.tags
}
