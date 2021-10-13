provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "no-https-bucket" {
  bucket = "no-https-bucket"
}

resource "aws_s3_bucket_policy" "bucket_2_policy" {
  bucket = aws_s3_bucket.no-https-bucket.id

  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"NOT-RECOMMENDED-FOR__AWSCONFIG-Rule_s3-bucket-ssl-requests-only",
      "Effect":"Allow",
      "Principal": {"AWS": "*"},
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::no-https-bucket/*"],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "true"
        }
      }
    }
  ]
}
POLICY
}