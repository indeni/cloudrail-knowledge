################################################################################
# This template will create the following resources:
#
# Region: us-east-1 (2520 ENIs)
#
#   - 1 VPC with (1514 ENIs in total):
#     - Public and Private subnets
#     - Internet Gateway
#     - 2 NAT Gateways
#     - 1 public-facing LB logging to S3 bucket
#     - 1 AutoScaling Group with launch configuration (1500 "t2.micro" EC2 instances)
#     - CloudWatch Logs endpoint with default policy and default security group
#     - SSM endpoint with default policy and default security group
#     - EC2 instance roles with permissions to access those endpoints
#
#   - 1 VPC with (1006 ENIs in total):
#     - Public and Private subnets
#     - Internet Gateway
#     - 2 NAT Gateways
#     - 1 public-facing LB with several listeners serving traffic to ECS services
#     - 1 ECS cluster with 4 ECS services (250 ENIs each) using FARGATE type:
#         - Security Groups
#         - ECS Task definition with IAM roles
#         - Cloudwatch groups
#         - Source/Target S3 bucket
#         - Kinesis streams
#
#
# Region: eu-west-1 (2003 ENIs)
#
#   - 1 VPC (prod) with (1003 ENIs):
#     - Public and Private Subnets
#     - Internet Gateway
#     - NAT Gateway
#     - 1 EKS cluster with
#       - Security groups
#       - 2 worker groups with 250 instances each
#
#   - Included the sample case for 1000-ENIs here also
#
# Region: eu-central-1 (4507 ENIs)
#
#   - 1 VPC with (1007 ENIs in total):
#     - Public and Private subnets
#     - Internet Gateway
#     - NAT Gateways
#     - Public-facing LB with several listeners serving traffic to ECS services
#     - ASG for EC2 instances (10) used in ECS service
#     - 1 ECS cluster with 4 ECS services using EC2 type (10 instances c5.18xlarge):
#         - Security Groups
#         - ECS Task definition with IAM roles
#         - Cloudwatch groups
#         - Source/Target S3 bucket
#         - Kinesis streams
#
#   - 1 VPC (Mgmt) with (400 ENIs):
#     - 2 private subnets
#     - Peering connection with VPC Middle and VPC Back
#     - 200 EC2 instances in each subnet
#     - Security groups
#     - Instance profiles
#
#   - 1 VPC (Middleware) with (1500 ENIs)
#     - 6 Private subnets
#     - Peering connection with VPC Mgmt and VPC Back
#     - 250 EC2 instances in each subnet with 2 network interfaces
#     - Security groups
#     - Instance profiles
#
#   - 1 VPC (Backoffice) with (1500 ENIs)
#     - 6 Private subnets
#     - Peering connection with VPC Mgmt and VPC MIddle
#     - 250 EC2 instances in each subnet with 2 network interfaces
#     - Security groups
#     - Instance profiles
#
#
# Region: eu-west-3 (1003 ENIs)
#
#   - 1 API Gateway with private integration (API VPC Link)
#   - 1 VPC with NLB and 1000 EC2 instances in the backend
#   - Security groups and IAM roles with default values
#
# 
# with a total of 10,000 ENIs
#
################################################################################

terraform {
  required_version = "> 0.13.0"
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu-west-1"
  region = "eu-west-1"
}

provider "aws" {
  alias  = "eu-central-1"
  region = "eu-central-1"
}

provider "aws" {
  alias  = "eu-west-3"
  region = "eu-west-3"
}


module "sample11" {
  source = "./modules/sample11"
}

module "sample12" {
  source = "./modules/sample12"
}

module "sample21" {
  source = "./modules/sample21"

  providers = {
    aws = aws.eu-west-1
  }
}

module "sample22" {
  source = "./modules/sample22"

  providers = {
    aws = aws.eu-west-1
  }
}

module "sample31" {
  source = "./modules/sample31"

  providers = {
    aws = aws.eu-central-1
  }
}

module "sample32" {
  source = "./modules/sample32"

  providers = {
    aws = aws.eu-central-1
  }
}

module "sample41" {
  source = "./modules/sample41"

  providers = {
    aws = aws.eu-west-3
  }
}
