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

variable "lambda_zip" {
  description = "Path to the zipped lambda package"
  type        = string
}

variable "metrics_cron" {
  description = "Frequency to run metric forwarder lambda - on the hour"
  type        = string
}

variable "eu-west-1_alarms" {
  type    = list(map(string))
  default = []
}

variable "eu-west-2_alarms" {
  type    = list(map(string))
  default = []
}

variable "us-east-1_alarms" {
  type    = list(map(string))
  default = []
}
