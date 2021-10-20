
resource "aws_default_vpc" "default" {
  tags = {
    Name = "default-vpc"
  }
}

resource "aws_default_route_table" "default_route_table" {
  default_route_table_id = aws_default_vpc.default.default_route_table_id
  tags = {
    Name = "default table"
  }
}

resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_default_vpc.default.id
  cidr_block = "172.31.96.0/20"
  availability_zone =  "us-east-1a"

}

resource "aws_default_network_acl" "public-nacl" {
  default_network_acl_id     = aws_default_vpc.default.default_network_acl_id
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_default_network_acl.public-nacl.id
  rule_number    = 90
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 2
  to_port        = 50
}