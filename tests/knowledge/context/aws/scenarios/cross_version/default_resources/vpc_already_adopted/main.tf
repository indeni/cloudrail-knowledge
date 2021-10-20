resource "aws_default_vpc" "default" {

  enable_dns_hostnames = false

  tags = {
    TerraformTag = "TerraformValue"
  }
}