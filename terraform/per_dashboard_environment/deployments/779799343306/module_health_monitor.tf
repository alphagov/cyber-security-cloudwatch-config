module "health_monitor" {
  source              = "../../../modules/health_monitor"
  LOG_LEVEL           = var.LOG_LEVEL
  DEF_ENVIRONMENT     = var.DEF_ENVIRONMENT
  lambda_zip          = var.lambda_zip
  monitored_accounts  = var.monitored_accounts
}
