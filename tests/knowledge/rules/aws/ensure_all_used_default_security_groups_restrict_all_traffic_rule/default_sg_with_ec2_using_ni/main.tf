# Test case(need to move): resource (ec2) use default sg from a VPC that is connected to the resource using network interface
# This is not a new use case for the rule, it's a use case for the context builder, that can need to know how to handle
# different tf ec2 deceleration
# Expected: alert on the use of default sg

provider "aws" {
  region = "eu-west-2"
}


locals {
  test_description  = "resource (ec2) use default sg from a VPC that is connected to the resource using network interface. This is not a new use case for the rule, its a use case for the context builder, that can need to know how to handle"
  test_name         = "Integration test - use case 4"
  cidr_block        = "10.12.0.0/16"
  network_interface = "10.12.1.100"
}

resource "aws_vpc" "vpc" {
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_subnet" "subnet" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = local.cidr_block

  tags = {
    Name = local.test_name
  }
}

resource "aws_network_interface" "ni" {
  subnet_id = aws_subnet.subnet.id
  private_ips = [
  local.network_interface]

  tags = {
    Name = local.test_name
  }
}

resource "aws_instance" "ec2" {
  ami           = "ami-06ae154e20eef72a6"
  instance_type = "t2.micro"

  tags = {
    Name = local.test_name
  }

  network_interface {
    network_interface_id = aws_network_interface.ni.id
    device_index         = 0
  }
}
