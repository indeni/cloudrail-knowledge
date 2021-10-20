provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "logging" {
  bucket = "testing-cloud-logging"
  acl    = "log-delivery-write"

  logging {
    target_bucket = "testing-cloud-logging"
    target_prefix = "log-testB/"
  }
}
