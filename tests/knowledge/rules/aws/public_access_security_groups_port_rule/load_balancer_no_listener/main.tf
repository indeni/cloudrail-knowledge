
provider "aws" {
  region = "eu-west-2"
}

locals {
  test_description = "resource (load balancer) is not accessible from internet because he has no listener"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 12"
  cidr_block       = "10.10.0.0/16"
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

resource "aws_network_acl" "nondefault" {
  subnet_ids = [aws_subnet.subnet.id]
  vpc_id = aws_vpc.vpc.id
  ingress {
    action = "allow"
    from_port = 22
    protocol = "tcp"
    rule_no = 100
    to_port = 22
    cidr_block = "0.0.0.0/0"
  }
}

resource "aws_security_group" "sg" {
  vpc_id = aws_vpc.vpc.id
  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "toinet" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "toinet" {
  subnet_id = aws_subnet.subnet.id
  route_table_id = aws_route_table.toinet.id
}

resource "aws_lb" "test" {
  subnets = [aws_subnet.subnet.id]
  load_balancer_type = "application"
  security_groups = [aws_security_group.sg.id]
}