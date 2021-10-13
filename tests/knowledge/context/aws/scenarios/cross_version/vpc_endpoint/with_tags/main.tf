locals {
  region  = "us-east-1"
  https_port = 443
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}


resource "aws_vpc" "test-vpc" {
  cidr_block           = local.cidr_block
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "VPC Cloudrail test"
  }
}

resource "aws_vpc_endpoint" "sns-vpce" {
  vpc_id            = aws_vpc.test-vpc.id
  service_name      = "com.amazonaws.${local.region}.sns"
  vpc_endpoint_type = "Interface"
  subnet_ids = [aws_subnet.private-subnet.id]
  security_group_ids = [aws_security_group.https-sg.id]
  private_dns_enabled = true
  tags = {
    Name = "VPC Endpoint Testing cloudrail"
  }
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block
  availability_zone = "${local.region}a"
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

resource "aws_sns_topic" "cloudrail_1" {
  name              = "sns_not_ecnrypted-1"
  tags = {
    Name = "Sns Topic Cloudrail Test"
  }
}
