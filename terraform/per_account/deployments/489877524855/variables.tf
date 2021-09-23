variable "LOG_LEVEL" {
  description = "Python log level passed to lambda environments"
  type        = string
  default     = "DEBUG"
}

variable "DEF_ENVIRONMENT" {
  description = "What is the status of the deployed service"
  type        = string
  default     = "test"
}

variable "TARGET_LAMBDA" {
  description = "What is the status of the deployed service"
  type        = string
  default     = "health_monitor_lambda"
}

variable "TARGET_ROLE" {
  description = "What is the status of the deployed service"
  type        = string
  default     = "health_monitor_forwarder_role"
}

variable "TARGET_REGION" {
  description = "What is the status of the deployed service"
  type        = string
  default     = "eu-west-2"
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
