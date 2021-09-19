resource "aws_s3_bucket" "logging" {
  acl = "log-delivery-write"
}

resource "aws_s3_bucket" "test" {
  acl = "private"

  logging {
    target_bucket = aws_s3_bucket.logging.id
    target_prefix = "log/"
  }
}
