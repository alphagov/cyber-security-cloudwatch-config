variable "DEF_ENVIRONMENT" {
    type    = string
    default = "Test"
}

variable "monitored_accounts" {
    type    = list
    default = []
}

variable "LOG_LEVEL" {
  type    = string
  default = "DEBUG"
}
