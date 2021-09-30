variable "LOG_LEVEL" {
  description = "Python log level passed to lambda environments"
  type        = string
  default     = "INFO"
}

variable "DEF_ENVIRONMENT" {
  description = "What is the status of the deployed service"
  type        = string
  default     = "prod"
}


variable "lambda_zip" {
  description = "Path to the zipped lambda package"
  type        = string
  default     = "../../../../lambda/health_package/health_package.zip"
}

variable "monitored_accounts" {
  description = "Account to accept forwarded data from"
  type        = list(string)
  default     = [
    "103495720024",
    "489877524855",
    "779799343306",
    "885513274347"
  ]
}
