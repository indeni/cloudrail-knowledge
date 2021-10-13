provider "aws" {
  region = "us-east-1"
}

locals {
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}
resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
  enable_dns_support = true
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.100.128/25"

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_route_table" "private-rtb" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = local.s3_prefix_list_cidr_block
    gateway_id = "pl-fake-id"
  }

  tags = {
    Name = "private-rtb"
  }
}

resource "aws_route_table_association" "private-rtb-assoc" {
  subnet_id      = aws_subnet.private-subnet.id
  route_table_id = aws_route_table.private-rtb.id
}

resource "aws_network_acl" "allow-public-outbound-nacl" {
  vpc_id = aws_vpc.main.id
  subnet_ids = [aws_subnet.private-subnet.id]

  egress {
    protocol   = "tcp"
    rule_no    = 200
    action     = "allow"
    cidr_block = local.s3_prefix_list_cidr_block
    from_port  = 443
    to_port    = 443
  }

  tags = {
    Name = "allow-public-outbound-nacl"
  }
}

resource "aws_security_group" "allow-public-outbound-sg" {
  name        = "allow-public-outbound-sg"
  description = "Allow HTTPS outbound traffic"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [local.s3_prefix_list_cidr_block]
  }

}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "test" {
  ami = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.allow-public-outbound-sg.id]
  subnet_id = aws_subnet.private-subnet.id
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = "public-bucket"
  acl = "public-read"
  tags = {
    Name = "public-bucket"
  }
}