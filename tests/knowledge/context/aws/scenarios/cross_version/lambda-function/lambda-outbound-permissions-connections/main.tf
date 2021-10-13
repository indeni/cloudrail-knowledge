locals {
  region  = "us-east-1"
  https_port = 443
  max_port = 65535
  cidr_block = "192.168.100.128/25"
  zero_cidr_block = "0.0.0.0/0"
  s3_prefix_list_cidr_block = "54.231.0.0/17"
}

data "aws_caller_identity" "current" {}

resource "aws_iam_role_policy_attachment" "AWSLambdaVPCAccessExecutionRole" {
    role       = aws_iam_role.lambda-role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "my-lambda" {
  filename = "lambda.zip"
  function_name = "my-lambda"
  role          = aws_iam_role.lambda-role.arn
  handler       = "lambda_function.lambda_handler"
  runtime = "python3.8"

  vpc_config {
    security_group_ids = [aws_security_group.allow-https.id, aws_security_group.allow-all-local.id]
    subnet_ids = [aws_subnet.private-subnet.id]
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

resource "aws_iam_policy" "policy" {
  name        = "allow_role_s3_operations"
  description = "allow_role_s3_operations"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:*"
        ],
        "Effect": "Allow",
        "Sid": "",
        "Resource": "*"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "attach-policy-to-s3-bucket-role" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = local.cidr_block

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_security_group" "allow-https" {
  description = "allow https"
  vpc_id     = aws_vpc.main.id
  ingress {
    from_port = local.https_port
    protocol = "tcp"
    to_port = local.https_port
    cidr_blocks = [local.zero_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }
}

resource "aws_security_group" "allow-all-local" {
  description = "allow-all-local"
  vpc_id     = aws_vpc.main.id
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private-subnet.cidr_block]
  }
}

resource "aws_s3_bucket" "test-bucket" {
  bucket = "randombucketname132423"
  policy =  <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:GetObject",
      "Effect": "Deny",
      "Sid": "",
      "Principal": {
          "AWS": "${data.aws_caller_identity.current.account_id}"
      },
      "Resource": ["arn:aws:s3:::randombucketname132423", "arn:aws:s3:::randombucketname132423/*"]
    }
  ]
}
EOF
}
