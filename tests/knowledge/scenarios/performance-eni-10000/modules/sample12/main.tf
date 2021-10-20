locals {


  name                    = "vpcB"
  nameB                   = local.name
  ecs_instances_service_1 = 10 #250 Check your service quotas
  ecs_instances_service_2 = 10 #250 Check your service quotas
  ecs_instances_service_3 = 10 #250 Check your service quotas
  ecs_instances_service_4 = 10 #250 Check your service quotas

}

data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_region" "current" {}

module "vpcB" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "~> 2"
  name                 = local.name
  cidr                 = "10.98.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = ["10.98.0.0/24", "10.98.1.0/24"]
  private_subnets      = ["10.98.10.0/24", "10.98.11.0/24", "10.98.12.0/24", "10.98.13.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = true
}
