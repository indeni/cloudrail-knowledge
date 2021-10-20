locals {
  nameA         = "vpcA"
  asg_instances = 1500
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_region" "current" {}

module "vpcA" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.nameA
  cidr                 = "10.99.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = ["10.99.0.0/24", "10.99.1.0/24"]
  private_subnets      = ["10.99.10.0/23", "10.99.12.0/23", "10.99.14.0/23", "10.99.16.0/23"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = true
}
