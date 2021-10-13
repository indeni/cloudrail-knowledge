
provider "aws" {
  region = "eu-west-2"
}

locals {
  test_description = "resource (ec2) is accessible from the Internet on port 22 - explicit resources defined"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 2"
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
  vpc_id     = aws_vpc.vpc.id
  ingress {
    action     = "allow"
    from_port  = 0
    protocol   = -1
    rule_no    = 100
    to_port    = 0
    cidr_block = "0.0.0.0/0"
  }
}

resource "aws_security_group" "sg" {
  vpc_id = aws_vpc.vpc.id
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
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
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.toinet.id
}

resource "aws_instance" "test" {
  ami                         = "ami-07cda0db070313c52"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.subnet.id
  vpc_security_group_ids      = [aws_security_group.sg.id]
  associate_public_ip_address = true

  tags = {
    Name = local.test_name
  }
}
