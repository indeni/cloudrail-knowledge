resource "aws_default_vpc" "default" {
  tags = {
    Name = "default-vpc"
  }
}

resource "aws_default_route_table" "ido_default_route_table" {
  default_route_table_id = aws_default_vpc.default.default_route_table_id
  tags = {
    Name = "default table"
  }
}