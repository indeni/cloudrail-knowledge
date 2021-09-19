provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "secure-https-bucket" {
  bucket = "secure-https-bucket"
}

resource "aws_s3_bucket_policy" "bucket_2_policy" {
  bucket = aws_s3_bucket.secure-https-bucket.id

  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"AllowSSLRequestsOnly",
      "Effect":"Deny",
      "Principal": {"AWS": "*"},
      "Action":["s3:*"],
      "Resource":["arn:aws:s3:::secure-https-bucket/*"],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
POLICY
}