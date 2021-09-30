##
# config to store terraform state in S3

terraform {
  backend "s3" {
    bucket  = "gds-security-terraform"
    key     = "terraform/state/account/779799343306/service/health-monitor.tfstate"
    region  = "eu-west-2"
    encrypt = true
  }
}
