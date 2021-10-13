provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "cloudrail" {
  bucket = "cloudrail-non-encrypted-czx7zxchs"
  acl    = "public-read-write"
}

resource "aws_s3_bucket_public_access_block" "cloudrail" {
  bucket                  = aws_s3_bucket.cloudrail.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
