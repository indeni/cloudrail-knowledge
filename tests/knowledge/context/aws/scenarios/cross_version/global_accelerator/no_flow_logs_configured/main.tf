
resource "aws_s3_bucket" "logging" {
  acl           = "private"
  force_destroy = true
}

resource "aws_globalaccelerator_accelerator" "test" {
  name            = "tes-flow-logs"
  ip_address_type = "IPV4"
  enabled         = true
}
