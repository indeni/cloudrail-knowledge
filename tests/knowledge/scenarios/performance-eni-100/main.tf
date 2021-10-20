################################################################################
# This template will create the following resources:
#
#   - 1 "production" VPC with:
#       - 2 public subnets
#       - 2 private subnets
#       - 1 IGW
#       - 50 EC2 instances
#       - 1 ELBs
#       - 3 route tables
#       - 1 Security Group for EC2 instances
#       - 1 Security Group for ELB
#       - 1 RDS cluster (Aurora MySQL) with 10 instances
#
#   - 1 "staging" VPC with:
#       - 2 public subnets
#       - 2 private subnets
#       - 1 IGW
#       - 34 EC2 instances
#       - 1 ELBs
#       - 3 route tables
#       - 1 Security Group for EC2 instances
#       - 1 Security Group for ELB
#       - 1 RDS cluster (Aurora MySQL) with 5 instances
#
# with a total of 101 ENIs
#
################################################################################

terraform {
  required_version = "> 0.13.0"
}

provider "aws" {
  region = "us-east-1"
}

locals {

  project = {
    production = {
      cidr_block           = "10.10.0.0/16",
      public_subnets       = ["10.10.0.0/24", "10.10.1.0/24"]
      private_subnets      = ["10.10.10.0/24", "10.10.11.0/24", "10.10.12.0/24", "10.10.13.0/24"]
      instances_per_subnet = 25
      instance_type        = "t2.micro",
      db_instances         = 10
      db_instance_type     = "db.t2.medium",
      environment          = "production"
    },
    staging = {
      cidr_block           = "10.20.0.0/16",
      public_subnets       = ["10.20.0.0/24", "10.20.1.0/24"]
      private_subnets      = ["10.20.10.0/24", "10.20.11.0/24", "10.20.12.0/24", "10.20.13.0/24"]
      instances_per_subnet = 17,
      instance_type        = "t2.micro",
      db_instances         = 5,
      db_instance_type     = "db.t2.medium",
      environment          = "staging"
    }
  }
}


data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "2.77.0"
  for_each           = local.project
  cidr               = each.value.cidr_block
  azs                = data.aws_availability_zones.available.names
  private_subnets    = each.value.private_subnets
  public_subnets     = each.value.public_subnets
  enable_nat_gateway = false
  enable_vpn_gateway = false
}

module "app_security_group" {
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  for_each            = local.project
  name                = "web-server-sg-${each.key}"
  description         = "Security group for web-servers with HTTP ports open within VPC"
  vpc_id              = module.vpc[each.key].vpc_id
  ingress_cidr_blocks = module.vpc[each.key].public_subnets_cidr_blocks
}

module "lb_security_group" {
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  for_each            = local.project
  name                = "load-balancer-sg-${each.key}"
  description         = "Security group for load balancer with HTTP ports open within VPC"
  vpc_id              = module.vpc[each.key].vpc_id
  ingress_cidr_blocks = ["0.0.0.0/0"]
}

resource "random_string" "lb_id" {
  length  = 4
  special = false
}

module "elb_http" {
  source              = "terraform-aws-modules/elb/aws"
  version             = "2.4.0"
  for_each            = local.project
  name                = trimsuffix(substr(replace(join("-", ["lb", random_string.lb_id.result, each.key, each.value.environment]), "/[^a-zA-Z0-9-]/", ""), 0, 32), "-")
  internal            = false
  security_groups     = [module.lb_security_group[each.key].this_security_group_id]
  subnets             = module.vpc[each.key].public_subnets
  number_of_instances = length(module.ec2_instances[each.key].instance_ids)
  instances           = module.ec2_instances[each.key].instance_ids

  listener = [{
    instance_port     = "80"
    instance_protocol = "HTTP"
    lb_port           = "80"
    lb_protocol       = "HTTP"
  }]

  health_check = {
    target              = "HTTP:80/index.html"
    interval            = 10
    healthy_threshold   = 3
    unhealthy_threshold = 10
    timeout             = 5
  }
}

resource "aws_db_parameter_group" "aurora_db_57_parameter_group" {
  name        = "test-aurora-db-57-parameter-group"
  family      = "aurora-mysql5.7"
  description = "test-aurora-db-57-parameter-group"
}

resource "aws_rds_cluster_parameter_group" "aurora_57_cluster_parameter_group" {
  name        = "test-aurora-57-cluster-parameter-group"
  family      = "aurora-mysql5.7"
  description = "test-aurora-57-cluster-parameter-group"
}

module "db-cluster" {
  source                          = "terraform-aws-modules/rds-aurora/aws"
  version                         = "~> 3.0"
  for_each                        = local.project
  name                            = lower(each.key)
  engine                          = "aurora-mysql"
  engine_version                  = "5.7.12"
  vpc_id                          = module.vpc[each.key].vpc_id
  subnets                         = slice(module.vpc[each.key].private_subnets[*], 2, 4)
  skip_final_snapshot             = true
  apply_immediately               = true
  replica_count                   = each.value.db_instances
  db_parameter_group_name         = aws_db_parameter_group.aurora_db_57_parameter_group.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_57_cluster_parameter_group.id
  instance_type                   = each.value.db_instance_type
  monitoring_interval             = 10
  allowed_security_groups         = [module.app_security_group[each.key].this_security_group_id]
}

module "ec2_instances" {
  source             = "./modules/aws-instance"
  for_each           = local.project
  instance_count     = each.value.instances_per_subnet * (length(module.vpc[each.key].private_subnets)) / 2
  instance_type      = each.value.instance_type
  subnet_ids         = slice(module.vpc[each.key].private_subnets[*], 0, 2)
  security_group_ids = [module.app_security_group[each.key].this_security_group_id]
  project_name       = each.key
  environment        = each.value.environment
}
