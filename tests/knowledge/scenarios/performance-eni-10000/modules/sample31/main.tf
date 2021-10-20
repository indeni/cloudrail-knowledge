locals {
  name                    = "sample31"
  instance_type           = "c5.18xlarge"
  ec2_instances           = 10
  ecs_instances_service_1 = 250
  ecs_instances_service_2 = 250
  ecs_instances_service_3 = 250
  ecs_instances_service_4 = 250
}

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
  single_nat_gateway   = true
}


resource "null_resource" "enable_new_ecs_features" {
  provisioner "local-exec" {
    command = <<EOF
aws ecs put-account-setting-default --name awsvpcTrunking --value enabled --region ${data.aws_region.current.name}
aws ecs put-account-setting-default --name containerInstanceLongArnFormat --value enabled --region ${data.aws_region.current.name}
aws ecs put-account-setting-default --name serviceLongArnFormat --value enabled --region ${data.aws_region.current.name}
aws ecs put-account-setting-default --name taskLongArnFormat --value enabled --region ${data.aws_region.current.name}
EOF
  }
}
