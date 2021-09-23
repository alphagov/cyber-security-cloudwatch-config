##
# config to store terraform state in S3

terraform {
  backend "s3" {
    bucket  = "gds-security-terraform"
    key     = "terraform/state/account/489877524855/service/cloudwatch-config.tfstate"
    region  = "eu-west-2"
    encrypt = true
  }
}
