resource "aws_vpc" "external" {
  cidr_block = "172.27.0.0/16"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  tags = {
    Name = "external"
  }
}

resource "aws_route_table" "ido_main_route_table" {
  vpc_id = aws_vpc.external.id
  tags = {
    Name = "main"
  }
}

resource "aws_main_route_table_association" "a" {
  vpc_id         = aws_vpc.external.id
  route_table_id = aws_route_table.ido_main_route_table.id
}

resource "aws_subnet" "external" {
  vpc_id     = aws_vpc.external.id
  cidr_block = "172.27.65.0/24"
}
