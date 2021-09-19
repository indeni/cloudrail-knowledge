provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.0.0/16"
  enable_dns_support = true
}

resource "aws_subnet" "subnet_2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.1.0/24"
}

resource "aws_security_group" "instance" {
  name        = "some-sg-name"
  description = "sg description"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group_rule" "outbound_internet_access" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["1.1.1.1/32"]
  security_group_id = aws_security_group.instance.id
}

resource "aws_instance" "ec2_2" {
  ami = data.aws_ami.ubuntu_2.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_2.id
  vpc_security_group_ids  = [aws_security_group.instance.id]
}

data "aws_ami" "ubuntu_2" {
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