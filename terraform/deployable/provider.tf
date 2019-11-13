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