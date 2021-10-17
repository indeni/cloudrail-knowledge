
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 1.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 2.2"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}
