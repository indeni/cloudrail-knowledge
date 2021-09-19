
provider "aws" {
  region = "us-east-1"
}

locals {
  test_description = "resource (ec2) is accessible from the Internet on port 22 - using TF complete VPC module"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 1"
  cidr_block       = "10.10.0.0/16"
}

module "vpc_example_complete-vpc" {
  source  = "terraform-aws-modules/vpc/aws//examples/complete-vpc"
}

resource "aws_security_group" "sg" {
  vpc_id = module.vpc_example_complete-vpc.vpc_id

  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "test" {
  ami           = "ami-07cda0db070313c52"
  instance_type = "t2.micro"
  subnet_id     = module.vpc_example_complete-vpc.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.sg.id]
  associate_public_ip_address = true

  tags = {
    Name = local.test_name
  }
}