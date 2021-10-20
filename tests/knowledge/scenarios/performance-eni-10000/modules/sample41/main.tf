locals {
  name          = "sample41"
  asg_instances = 1000
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_region" "current" {}

module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.name
  cidr                 = "10.15.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = ["10.15.0.0/24", "10.15.1.0/24"]
  private_subnets      = ["10.15.10.0/24", "10.15.11.0/24", "10.15.12.0/24", "10.15.13.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = true
  single_nat_gateway   = true
}

