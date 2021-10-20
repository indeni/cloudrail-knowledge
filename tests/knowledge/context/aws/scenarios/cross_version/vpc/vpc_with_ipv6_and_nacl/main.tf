
resource "aws_vpc" "test-vpc" {
  cidr_block           = "192.168.10.0/24"
  assign_generated_ipv6_cidr_block = true
}

resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = "192.168.10.0/24"
  availability_zone =  "us-east-1a"

}

resource "aws_network_acl" "public-nacl" {
  vpc_id     = aws_vpc.test-vpc.id
  subnet_ids = [aws_subnet.public-subnet.id]
}

resource "aws_network_acl_rule" "inbound-rule" {
  network_acl_id = aws_network_acl.public-nacl.id
  rule_number    = 90
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 2
  to_port        = 50
}