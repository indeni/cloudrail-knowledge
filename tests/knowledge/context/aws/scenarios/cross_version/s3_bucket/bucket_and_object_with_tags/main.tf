
resource "aws_s3_bucket" "cloudrail" {
  bucket = "cloudrail-non-encrypted-czx7zxchs"
  acl    = "private"
  tags = {
    Name = "S3-bucket-testing-tags"
  }
}

resource "aws_s3_bucket_public_access_block" "cloudrail" {
  bucket                  = aws_s3_bucket.cloudrail.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "object" {
  bucket  = aws_s3_bucket.cloudrail.id
  key     = "example_file_non_encrypted"
  content = "Cloudrail example"
  tags = {
    Name = "S3-bucket-object-testing-tags"
  }
}
