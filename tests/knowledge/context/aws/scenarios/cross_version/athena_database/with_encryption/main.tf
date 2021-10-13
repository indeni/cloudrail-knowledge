
resource "aws_s3_bucket" "test" {
  force_destroy = true
  acl           = "private"
}

resource "aws_athena_database" "test" {
  name          = "athena_test_encrypted"
  bucket        = aws_s3_bucket.test.bucket
  force_destroy = true

  encryption_configuration {
    encryption_option = "SSE_S3"
  }
}
