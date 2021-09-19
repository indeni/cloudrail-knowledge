resource "aws_vpc" "external" {
  cidr_block = "172.27.0.0/16"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
    tags = {
    Name = "igw-vpc"
  }
}

resource "aws_egress_only_internet_gateway" "igw" {
  vpc_id = aws_vpc.external.id
}

resource "aws_default_route_table" "ido_default_route_table" {
  default_route_table_id = aws_vpc.external.default_route_table_id

  route {
    ipv6_cidr_block        = "::/0"
    egress_only_gateway_id = aws_egress_only_internet_gateway.igw.id
  }
  tags = {
    Name = "default table"
  }
}