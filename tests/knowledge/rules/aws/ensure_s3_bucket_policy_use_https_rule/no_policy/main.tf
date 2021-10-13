provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "no-policy-bucket" {
  bucket = "no-policy-bucket"
}
