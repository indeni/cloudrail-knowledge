
resource "aws_default_subnet" "default_az1" {
  availability_zone = "us-east-1c"
  map_public_ip_on_launch = true

  tags = {
    TerraformTag = "TerraformValue"
  }
}