provider "aws" {
  region = "us-east-1"
}

resource "aws_kms_key" "test" {
  description             = "KMS key for XRay - creating"
  deletion_window_in_days = 7
}

resource "aws_xray_encryption_config" "test" {
  type   = "KMS"
  key_id = aws_kms_key.test.arn
}
