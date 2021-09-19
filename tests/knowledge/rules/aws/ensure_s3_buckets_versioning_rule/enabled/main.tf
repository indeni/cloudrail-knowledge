provider "aws" {
    region = "ca-central-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "my-tf-test-bucket5656"
  acl    = "private"
  versioning {
    enabled = true
  }

}