resource "aws_vpc" "external" {
  cidr_block = "172.27.0.0/16"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
}

resource "aws_subnet" "subnet1" {
  vpc_id = aws_vpc.external.id
  cidr_block = "127.27.1.0/24"
}

resource "aws_network_acl" "test"{
  vpc_id = aws_vpc.external.id
  subnet_ids = [aws_subnet.subnet1.id]
}