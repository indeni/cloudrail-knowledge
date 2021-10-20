provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = "bucket-with-public-policy-1"
}

resource "aws_s3_bucket_policy" "bucket_1_policy" {
  bucket = aws_s3_bucket.public-bucket.id

  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"PublicRead",
      "Effect":"Allow",
      "Principal": "*",
      "Action":["s3:ListBucket","s3:ListBucketMultipartUploads"],
      "Resource":["arn:aws:s3:::bucket-with-public-policy-1"]
    }
  ]
}
POLICY
}