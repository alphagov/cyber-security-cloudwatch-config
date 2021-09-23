module "alarms" {
  source            = "../../modules/alarms"
  LOG_LEVEL         = var.LOG_LEVEL
  DEF_ENVIRONMENT   = var.DEF_ENVIRONMENT
  TARGET_LAMBDA     = var.TARGET_LAMBDA
  TARGET_ROLE       = var.TARGET_ROLE
  TARGET_REGION     = var.TARGET_REGION
  eu-west-1_alarms  = var.eu-west-1_alarms
  eu-west-2_alarms  = var.eu-west-2_alarms
  us-east-1_alarms  = var.us-east-1_alarms
}
