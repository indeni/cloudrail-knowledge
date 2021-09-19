provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "192.168.100.0/24"
  enable_dns_support = true
}

resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "192.168.100.128/25"

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_s3_bucket" "private-bucket" {
  bucket = "private-bucket"
  tags = {
    Name = "private-bucket"
  }
  policy = <<POLICY
      {
        "Version": "2012-10-17",
        "Id": "BUCKET_POLICY",
        "Statement": [
          {
            "Sid": "VpceAllow",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::111111111111:role/some-role" },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::private-bucket/*",
            "Condition": {
               "StringEquals": {"aws:SourceVpce": "vpce-some-id"}
            }
          }
        ]
      }
    POLICY

}

resource "aws_s3_bucket_public_access_block" "block_public_bucket_3" {
  bucket = aws_s3_bucket.private-bucket.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}