locals {
  region  = "us-east-1"
  https_port = 443
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}



resource "aws_vpc" "test-vpc" {
  cidr_block           = local.cidr_block
}

resource "aws_vpc_endpoint" "s3-vpce" {
  vpc_id            = aws_vpc.test-vpc.id
  service_name      = "com.amazonaws.${local.region}.s3"
  vpc_endpoint_type = "Gateway"
}

resource "aws_route_table_association" "private-rtb-assoc" {
  subnet_id      = aws_subnet.private-subnet.id
  route_table_id = aws_route_table.private-rtb.id
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block
  availability_zone = "${local.region}b"
}

resource "aws_route_table" "private-rtb" {
  vpc_id = aws_vpc.test-vpc.id

  tags = {
    Name = "private-rtb"
  }
}

resource "aws_vpc_endpoint_route_table_association" "example" {
  route_table_id  = aws_route_table.private-rtb.id
  vpc_endpoint_id = aws_vpc_endpoint.s3-vpce.id
}

resource "aws_network_acl" "private-subnet-nacl" {
  vpc_id     = aws_vpc.test-vpc.id
  subnet_ids = [aws_subnet.private-subnet.id]
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_network_acl.private-subnet-nacl.id
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = local.cidr_block
  from_port      = local.https_port
  to_port        = local.https_port
}

resource "aws_network_acl_rule" "outbound-rule" {
  network_acl_id = aws_network_acl.private-subnet-nacl.id
  rule_number    = 100
  egress         = true
  protocol       = -1
  rule_action    = "allow"
  cidr_block     = local.zero_cidr_block
  from_port      = 0
  to_port        = 0
}

resource "aws_security_group" "https-sg" {
  name   = "https-sg"
  vpc_id = aws_vpc.test-vpc.id

  ingress {
    description = "https"
    from_port   = local.https_port
    to_port     = local.https_port
    protocol    = "tcp"
    cidr_blocks = [local.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [local.zero_cidr_block]
  }

}
