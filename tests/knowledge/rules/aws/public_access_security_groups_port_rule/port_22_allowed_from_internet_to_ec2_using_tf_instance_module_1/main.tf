
provider "aws" {
  region = "us-east-1"
}

locals {
  test_description = "resource (ec2) is using a SG with port 22 allowed, but on a private subnet - using TF complete VPC and EC2 instance modules"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 4"
  cidr_block       = "10.10.0.0/16"
}

module "vpc_example_complete-vpc" {
  source  = "terraform-aws-modules/vpc/aws//examples/complete-vpc"
}

resource "aws_security_group" "sg" {
  vpc_id = module.vpc_example_complete-vpc.vpc_id
  ingress {
    from_port = 22
    protocol = "TCP"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "test" {
  source                 = "terraform-aws-modules/ec2-instance/aws"
  name                   = "test"
  instance_count         = 1

  ami                    = "ami-ebd02392"
  instance_type          = "t2.micro"
  key_name               = "user1"
  monitoring             = true
  vpc_security_group_ids = [aws_security_group.sg.id]
  subnet_id              = module.vpc_example_complete-vpc.public_subnets[0]
  associate_public_ip_address = true

  tags = {
    Name = local.test_name
  }
}