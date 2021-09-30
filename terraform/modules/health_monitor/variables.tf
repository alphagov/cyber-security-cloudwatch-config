variable "DEF_ENVIRONMENT" {
    type    = string
    default = "test"
}

variable "monitored_accounts" {
    type    = list(string)
    default = []
}

variable "LOG_LEVEL" {
  type    = string
  default = "DEBUG"
}

variable "lambda_zip" {
  description = "Path to the zipped lambda package"
  type        = string
}
