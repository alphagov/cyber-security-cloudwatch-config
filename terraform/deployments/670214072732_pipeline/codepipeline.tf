resource "aws_codepipeline" "cloudwatch_config" {
  name     = var.service_name
  role_arn = data.aws_iam_role.pipeline_role.arn
  tags     = merge(local.tags, { Name = var.service_name })

  artifact_store {
    type     = "S3"
    location = data.aws_s3_bucket.artifact_store.bucket
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["git_cloudwatch_config"]
      configuration = {
        ConnectionArn    = "arn:aws:codestar-connections:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:connection/${var.codestar_connection_id}"
        FullRepositoryId = "alphagov/cyber-security-cloudwatch-config"
        BranchName       = var.github_branch_name
      }
    }
  }

  stage {
    name = "Prep"

    action {
      name             = "BuildSSHConfig"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_cloudwatch_config"]
      output_artifacts = ["ssh_config"]
      configuration = {
        ProjectName = module.codebuild_build_ssh_config.project_name
      }
    }

    action {
      name             = "GetChangedFiles"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_cloudwatch_config"]
      output_artifacts = ["changed_files"]
      configuration = {
        ProjectName = module.codebuild_get_changed_file_list.project_name
      }
    }

    action {
      name             = "GetActionsRequired"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 2
      input_artifacts  = ["git_cloudwatch_config", "changed_files"]
      output_artifacts = ["actions_required"]
      configuration = {
        PrimarySource = "git_cloudwatch_config"
        ProjectName = module.codebuild_get_actions_required.project_name
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "RunTests"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_cloudwatch_config"]
      configuration = {
        PrimarySource = "git_cloudwatch_config"
        ProjectName = aws_codebuild_project.codebuild_run_tests.name
      }
    }

    action {
      name             = "BuildLambda"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_cloudwatch_config", "changed_files"]
      output_artifacts = ["lambda"]
      configuration = {
        PrimarySource = "git_cloudwatch_config"
        ProjectName = aws_codebuild_project.codebuild_build_lambda.name
      }
    }
  }

  stage {
    name = "Alarms"

    dynamic "action" {
      for_each         = toset(concat(var.non_prod_accounts, var.prod_accounts))
      content {
        name             = "GenerateAlarms${action.value}"
        category         = "Build"
        owner            = "AWS"
        provider         = "CodeBuild"
        version          = "1"
        run_order        = 1
        input_artifacts  = [
          "git_cloudwatch_config"
        ]
        output_artifacts = [
          "alarms_${action.value}"
        ]

        configuration = {
          PrimarySource         = "git_cloudwatch_config"
          ProjectName           = aws_codebuild_project.codebuild_generate_alarms.name
          EnvironmentVariables  = jsonencode([
            {"name":"AWS_ACCOUNT_ID", "value": action.value},
            {"name":"IAM_ROLE_NAME", "value": "CodePipelineDeployerRole_${action.value}"}
          ])
        }
      }
    }
  }

  stage {
    name = "NonProd"
    dynamic "action" {
      for_each         = toset(var.non_prod_accounts)
      content {
        name             = "TerraformAlarms${action.value}"
        category         = "Build"
        owner            = "AWS"
        provider         = "CodeBuild"
        version          = "1"
        run_order        = 1
        input_artifacts  = [
          "git_cloudwatch_config",
          "ssh_config",
          "lambda",
          "alarms_${action.value}"
        ]

        configuration = {
          PrimarySource = "git_cloudwatch_config"
          ProjectName   = module.codebuild_terraform_non_prod_alarms[action.key].project_name
        }
      }
    }

    action {
      name             = "TerraformMonitor"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 2
      input_artifacts  = [
        "git_cloudwatch_config",
        "ssh_config",
        "lambda",
      ]
      configuration = {
        PrimarySource = "git_cloudwatch_config"
        ProjectName   = module.codebuild_terraform_non_prod_monitor.project_name
      }
    }
  }

  # stage {
  #   name = "Pipeline"
  #
  #   action {
  #     name             = "UpdatePipeline"
  #     category         = "Build"
  #     owner            = "AWS"
  #     provider         = "CodeBuild"
  #     version          = "1"
  #     run_order        = 1
  #     input_artifacts  = ["git_cloudwatch_config"]
  #     output_artifacts = []
  #
  #     configuration = {
  #       ProjectName = module.codebuild_self_update.project_name
  #     }
  #   }
  # }
}
