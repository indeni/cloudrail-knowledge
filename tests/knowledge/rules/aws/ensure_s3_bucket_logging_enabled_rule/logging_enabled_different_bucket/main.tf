provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "logging" {
  bucket = "xxadsfdsfdsfz98734-logging"
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket" "source" {
  bucket = "zzadsfdsfdsfz98734-logging"
  acl    = "private"

  logging {
    target_bucket = "xxadsfdsfdsfz98734-logging"
    target_prefix = "log-testB/"
  }
}
