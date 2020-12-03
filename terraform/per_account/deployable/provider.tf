terraform {
  required_version = ">= 0.12.19"
  required_providers {
    aws = "<= 3.16.0"
  }
}

provider "aws" {
  # default
  region = "eu-west-2"
}

provider "aws" {
  # eu-west-1 provider
  region = "eu-west-1"
  alias  = "eu-west-1"
}

provider "aws" {
  # eu-west-2 provider
  region = "eu-west-2"
  alias  = "eu-west-2"
}

provider "aws" {
  # us-east-1 instance
  region = "us-east-1"
  alias  = "us-east-1"
}