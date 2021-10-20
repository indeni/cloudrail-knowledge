provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = "bucket-with-over-privileged-policy-1"
}

resource "aws_s3_bucket_public_access_block" "block_public_bucket_3" {
  bucket = aws_s3_bucket.public-bucket.id
  block_public_acls = false
  block_public_policy = false
  ignore_public_acls = false
  restrict_public_buckets = false
}
