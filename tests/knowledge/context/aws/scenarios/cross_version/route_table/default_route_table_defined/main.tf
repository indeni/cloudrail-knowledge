resource "aws_vpc" "external" {
  cidr_block = "172.27.0.0/16"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
    tags = {
    Name = "external"
  }
}

resource "aws_default_route_table" "ido_default_route_table" {
  default_route_table_id = aws_vpc.external.default_route_table_id
  tags = {
    Name = "default table"
  }
}

resource "aws_route" "use_vpc_default_id" {
  route_table_id         =  aws_vpc.external.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.external.id
}

resource "aws_route" "use_aws_default_route_table_default_route_table" {
  route_table_id         =  aws_default_route_table.ido_default_route_table.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "use_aws_default_route_table_id" {
  route_table_id         =  aws_default_route_table.ido_default_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "external_subnet_to_internet" {
  subnet_id      = aws_subnet.external.id
  route_table_id = aws_vpc.external.main_route_table_id
}

resource "aws_subnet" "external" {
  vpc_id     = aws_vpc.external.id
  cidr_block = "172.27.65.0/24"
      tags = {
    Name = "external"
  }
}
