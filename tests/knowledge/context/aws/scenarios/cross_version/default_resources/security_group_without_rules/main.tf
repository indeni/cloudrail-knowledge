
resource "aws_default_security_group" "default" {
  vpc_id = "vpc-0bb120e294ef53f94"

  tags = {
    TerraformTag = "TerraformValue"
  }
}