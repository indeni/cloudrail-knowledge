locals {
  name-mgmt   = "mgmt"
  name-middle = "middleware"
  name-back   = "backoffice"

  instances_middle_per_subnet = 250
  instances_mgmt_per_subnet   = 200
  instances_back_per_subnet   = 250
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ami" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name = "name"

    values = [
      "amzn-ami-hvm-*-x86_64-gp2",
    ]
  }
}

module "mgmt" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.name-mgmt
  cidr                 = "10.50.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.50.10.0/24", "10.50.11.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = false
}

module "middle" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.name-middle
  cidr                 = "10.40.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.40.11.0/24", "10.40.12.0/24", "10.40.13.0/24", "10.40.14.0/24", "10.40.15.0/24", "10.40.16.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = false
}

module "back" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.name-back
  cidr                 = "10.30.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.30.11.0/24", "10.30.12.0/24", "10.30.13.0/24", "10.30.14.0/24", "10.30.15.0/24", "10.30.16.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = false
}


