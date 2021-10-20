provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = "bucket-with-public-policy-3"
  policy = <<POLICY
      {
        "Version":"2012-10-17",
        "Statement":[
          {
            "Sid":"PublicRead",
            "Effect":"Allow",
            "Principal": "*",
            "Action":["s3:DeleteObject","s3:PutObject"],
            "Resource":["arn:aws:s3:::bucket-with-public-policy-3"]
          }
        ]
      }
POLICY
}

resource "aws_s3_bucket_public_access_block" "block_public_bucket_3" {
  bucket = aws_s3_bucket.public-bucket.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
