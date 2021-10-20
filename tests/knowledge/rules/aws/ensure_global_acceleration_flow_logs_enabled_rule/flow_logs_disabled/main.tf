provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "logging" {
  acl           = "private"
  force_destroy = true
}

resource "aws_globalaccelerator_accelerator" "test" {
  name            = "tes-flow-logs"
  ip_address_type = "IPV4"
  enabled         = true

  attributes {
    flow_logs_enabled   = false
    flow_logs_s3_bucket = aws_s3_bucket.logging.id
    flow_logs_s3_prefix = "flow-logs/"
  }
}
