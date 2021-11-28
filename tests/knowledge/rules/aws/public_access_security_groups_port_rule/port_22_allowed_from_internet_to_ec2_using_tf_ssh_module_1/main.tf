
provider "aws" {
  region = "eu-west-2"
}

locals {
  test_description = "resource (ec2) is using a SG with port 22 allowed, but on a private subnet - using TF complete VPC and SSH modules"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 5"
  cidr_block       = "10.10.0.0/16"
}

module "vpc_example_complete-vpc" {
  source  = "terraform-aws-modules/vpc/aws//examples/complete-vpc"
}

module "ssh_security_group" {
  source = "terraform-aws-modules/security-group/aws//modules/ssh"
  vpc_id = module.vpc_example_complete-vpc.vpc_id
  ingress_cidr_blocks = ["0.0.0.0/0"]
  name = "somename"
}

resource "aws_instance" "test" {
  ami           = "ami-07cda0db070313c52"
  instance_type = "t2.micro"
  subnet_id     = module.vpc_example_complete-vpc.public_subnets[0]
  associate_public_ip_address = true
  vpc_security_group_ids = [module.ssh_security_group.security_group_id]
  tags = {
    Name = local.test_name
  }
}