variable "LAMBDA_FILENAME" {
  type    = string
  default = "../../../lambda/health_monitor/health_monitor_lambda.zip"
}

variable "FUNCTION_NAME" {
  type    = string
  default = "health_monitor_lambda"
}

variable "ROLE" {
  type    = string
  default = "health_monitor_role"
}

variable "HANDLER" {
  type    = string
  default = "health_monitor.lambda_handler"
}

variable "TIMEOUT" {
  type    = number
  default = 60
}

variable "RUNTIME" {
  type    = string
  default = "python3.7"
}