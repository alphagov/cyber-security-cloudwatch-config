variable "LOG_LEVEL" {
  type    = string
  default = "DEBUG"
}

variable "LAMBDA_FILENAME" {
  type    = string
  default = "../../lambda/cloudwatch_forwarder/cloudwatch_forwarder_lambda.zip"
}

variable "DEF_ENVIRONMENT" {
    type    = string
    default = "Test"
}

variable "TARGET_LAMBDA" {
  type    = string
  default = "health_monitor_lambda"
}

variable "TARGET_ROLE" {
  type    = string
  default = "health_monitor_forwarder_role"
}

variable "TARGET_REGION" {
  type    = string
  default = "eu-west-2"
}

variable "RUNTIME" {
  type    = string
  default = "python3.7"
}