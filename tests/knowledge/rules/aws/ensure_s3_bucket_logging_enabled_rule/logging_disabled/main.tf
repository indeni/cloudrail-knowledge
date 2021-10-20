provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "logging" {
  acl = "log-delivery-write"
}

resource "aws_s3_bucket" "test" {
  acl = "private"
}
