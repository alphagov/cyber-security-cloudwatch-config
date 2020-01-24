variable "LOG_LEVEL" {
  type    = string
  default = "DEBUG"
}

variable "DEF_ENVIRONMENT" {
    type    = string
    default = "Test"
}

variable "TARGET_LAMBDA" {
  type    = string
  default = "health_monitor_lambda"
}

variable "TARGET_SQS_QUEUE" {
  type    = string
  default = "incoming_health_events"
}

variable "TARGET_ROLE" {
  type    = string
  default = "health_monitor_forwarder_role"
}

variable "TARGET_REGION" {
  type    = string
  default = "eu-west-2"
}