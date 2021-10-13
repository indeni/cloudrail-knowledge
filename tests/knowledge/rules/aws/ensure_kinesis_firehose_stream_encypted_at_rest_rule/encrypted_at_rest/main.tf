provider "aws" {
  region = "us-east-1"
}

locals {
  name = "cloudrail-firehose-test-encrypted"
}

resource "aws_iam_role" "firehose_role" {
  name = local.name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_s3_bucket" "bucket" {
  bucket = local.name
  acl    = "private"
}

resource "aws_kinesis_firehose_delivery_stream" "test" {
  name        = local.name
  destination = "extended_s3"

  server_side_encryption {
    enabled = true
  }

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn
  }
}
