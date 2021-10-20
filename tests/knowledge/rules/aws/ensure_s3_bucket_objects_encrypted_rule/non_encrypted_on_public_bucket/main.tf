provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "cloudrail" {
  bucket = "tomer-bucket-test-cr"
  acl    = "public-read-write"
}

resource "aws_s3_bucket_public_access_block" "cloudrail" {
  bucket                  = aws_s3_bucket.cloudrail.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_object" "object" {
  bucket  = aws_s3_bucket.cloudrail.id
  key     = "example_file_non_encrypted"
  content = "Cloudrail example"
}
