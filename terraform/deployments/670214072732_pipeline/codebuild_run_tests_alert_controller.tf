locals {
  test_alert_controller_project_name = "${var.service_name}-Build-TestAlertController"
}

resource "aws_codebuild_project" "codebuild_run_tests_alert_controller" {
  name        = local.test_alert_controller_project_name
  description = "Run Terraform init and validate"

  service_role = data.aws_iam_role.pipeline_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = var.default_container_image
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "SERVICE_ROLE"
    privileged_mode             = false

    registry_credential {
      credential_provider = "SECRETS_MANAGER"
      credential          = data.aws_secretsmanager_secret.dockerhub_creds.arn
    }

  }

  source {
    type      = "CODEPIPELINE"
    buildspec = file("${path.module}/codebuild_run_tests_alert_controller.yml")
  }

  tags = merge(local.tags, { "Name" : local.test_alert_controller_project_name })
}
