# Test case: resource (ec2) use a decelerated default sq with out rules in a newly created VPC
# Expected: no issue found

provider "aws" {
  region = "eu-west-1"
}

locals {
  test_description = "resource (ec2) use a decelerated default sq with out rules in a newly created VPC"
  test_name        = "Integration test - use case 2"
  cidr_block       = "10.10.0.0/16"
}

resource "aws_vpc" "vpc" {
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_subnet" "subnet" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_instance" "test_customized_no_rules_default_sg_ec2" {
  ami           = "ami-07cda0db070313c52"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet.id

  tags = {
    Name = local.test_name
  }
}