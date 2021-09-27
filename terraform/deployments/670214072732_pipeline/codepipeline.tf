resource "aws_codepipeline" "alert_processor" {
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
      output_artifacts = ["git_alert_processor"]
      configuration = {
        ConnectionArn    = "arn:aws:codestar-connections:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:connection/${var.codestar_connection_id}"
        FullRepositoryId = "alphagov/cyber-security-alert-processor"
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
      input_artifacts  = ["git_alert_processor"]
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
      input_artifacts  = ["git_alert_processor"]
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
      input_artifacts  = ["git_alert_processor", "changed_files"]
      output_artifacts = ["actions_required"]
      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = module.codebuild_get_actions_required.project_name
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "TestAlertController"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_alert_processor", "changed_files"]
      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = aws_codebuild_project.codebuild_run_tests_alert_controller.name
      }
    }

    action {
      name             = "TestReportNetcraft"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_alert_processor", "changed_files"]
      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = aws_codebuild_project.codebuild_run_tests_report_netcraft.name
      }
    }

    action {
      name             = "BuildAlertController"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_alert_processor", "changed_files"]
      output_artifacts = ["alert_controller_lambda"]
      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = aws_codebuild_project.codebuild_build_lambda_alert_controller.name
      }
    }

    action {
      name             = "BuildReportNetcraft"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_alert_processor", "changed_files"]
      output_artifacts = ["report_netcraft_lambda"]
      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = aws_codebuild_project.codebuild_build_lambda_report_netcraft.name
      }
    }
  }

  stage {
    name = "Staging"
    action {
      name             = "TerraformApply"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = [
        "git_alert_processor",
        "ssh_config",
        "alert_controller_lambda",
        "report_netcraft_lambda"
      ]
      output_artifacts = [
        "staging_terraform_output"
      ]

      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = module.codebuild_terraform_staging.project_name
      }
    }
  }

  stage {
    name = "Production"
    action {
      name             = "TerraformApply"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = [
        "git_alert_processor",
        "ssh_config",
        "alert_controller_lambda",
        "report_netcraft_lambda"
      ]
      output_artifacts = [
        "production_terraform_output"
      ]

      configuration = {
        PrimarySource = "git_alert_processor"
        ProjectName = module.codebuild_terraform_production.project_name
      }
    }
  }

  stage {
    name = "Pipeline"

    action {
      name             = "UpdatePipeline"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      run_order        = 1
      input_artifacts  = ["git_alert_processor"]
      output_artifacts = []

      configuration = {
        ProjectName = module.codebuild_self_update.project_name
      }
    }
  }
}
