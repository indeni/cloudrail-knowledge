
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "public-bucket" {
  bucket = "bucket-with-over-privileged-policy-1"
  policy = <<POLICY
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "S3FullAccess",
                  "Effect": "Allow",
                  "Principal": {
                      "AWS": "*"
                  },
                  "Action": "s3:*",
                  "Resource": [
                      "arn:aws:s3:::bucket-with-over-privileged-policy-1",
                      "arn:aws:s3:::bucket-with-over-privileged-policy-1/*"
                  ]
              }
          ]
      }
POLICY
}

resource "aws_s3_bucket_public_access_block" "block_public_bucket_3" {
  bucket = aws_s3_bucket.public-bucket.id
  restrict_public_buckets = true
}
