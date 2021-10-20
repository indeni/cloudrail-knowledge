provider "aws" {
  region = "us-east-1"
}

resource "aws_xray_encryption_config" "test" {
  type = "NONE"
}
