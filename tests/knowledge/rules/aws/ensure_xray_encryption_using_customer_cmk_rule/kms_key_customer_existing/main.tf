provider "aws" {
  region = "us-east-1"
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/test-xray"
}

resource "aws_xray_encryption_config" "test" {
  type   = "KMS"
  key_id = data.aws_kms_key.by_alias.arn
}
