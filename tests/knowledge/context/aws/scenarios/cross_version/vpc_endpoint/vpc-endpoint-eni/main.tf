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
  enable_dns_hostnames = true
  enable_dns_support = true
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.test-vpc.id
}

resource "aws_default_route_table" "default_route_table" {
  default_route_table_id = aws_vpc.test-vpc.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "default table"
  }
}

resource "aws_vpc_endpoint" "lambda-vpce" {
  vpc_id            = aws_vpc.test-vpc.id
  service_name      = "com.amazonaws.${local.region}.lambda"
  vpc_endpoint_type = "Interface"
  subnet_ids = [aws_subnet.private-subnet.id]
  security_group_ids = [aws_security_group.https-sg.id]
  private_dns_enabled = true
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.test-vpc.id
  cidr_block = local.cidr_block
  availability_zone = "${local.region}b"
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
resource "aws_lambda_function" "my-lambda" {
  filename         = "${path.module}/example_lambda_code/golang-example.zip"
  function_name    = "my-lambda"
  handler          = "main"
  role             = aws_iam_role.lambda-role.arn
  source_code_hash = filebase64sha256("${path.module}/example_lambda_code/golang-example.zip")
  runtime          = "go1.x"

    vpc_config {
    subnet_ids         = [aws_subnet.private-subnet.id]
    security_group_ids = [aws_security_group.https-sg.id]
  }

}

resource "aws_iam_role" "lambda-role" {
  name = "lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole" {
    role       = aws_iam_role.lambda-role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}