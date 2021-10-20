provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "test" {
  force_destroy = true
  acl           = "private"
}

resource "aws_athena_database" "test" {
  name          = "athena_test_non_encrypted"
  bucket        = aws_s3_bucket.test.bucket
  force_destroy = true
}
