# Test case: resource (ec2) use a decelerated default sq with rules in a newly created VPC
# Expected: alert on the use of default sg
provider "aws" {
  region = "eu-west-1"
}

locals {
  test_description = "resource (ec2) use a decelerated default sq with rules in a newly created VPC"
  test_name        = "Integration test - use case 3"
  cidr_block       = "10.11.0.0/16"
}


resource "aws_vpc" "vpc" {
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = [
    "0.0.0.0/0"]
  }
}

resource "aws_subnet" "subnet" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_instance" "ec2" {
  ami           = "ami-07cda0db070313c52"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet.id

  tags = {
    Name = local.test_name
  }
}